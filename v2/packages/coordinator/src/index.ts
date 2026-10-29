import { randomUUID } from "node:crypto";
import { mkdirSync } from "node:fs";
import { dirname } from "node:path";
import Database from "better-sqlite3";
import {
  AttemptId,
  CardId,
  CardRevision,
  CommandEnvelopeSchema,
  CommandReceiptSchema,
  HandoffId,
  OperationId,
  type CommandEnvelope,
  type CommandReceipt,
  type RuntimeCommand,
  type RuntimeEvent,
  encode,
  parse,
  sha256,
  stableJson,
  assertNever,
} from "@super-speckit/protocol";

type Clock = () => Date;

type CardRow = Readonly<{ card_id: string; revision: string; version: number; observed_at: string }>;
type AttemptRow = Readonly<{
  attempt_id: string;
  card_id: string;
  revision: string;
  workspace_id: string;
  provider_id: string;
  runner_id: string;
  principal: string;
  state_kind: string;
  state_json: string;
  fence: number;
  lease_expires_at: string;
}>;
type HandoffRow = Readonly<{
  handoff_id: string;
  card_id: string;
  source_attempt_id: string;
  destination_provider_id: string;
  destination_runner_id: string;
  capsule_digest: string;
  state_kind: string;
  state_json: string;
}>;
type CommandRow = Readonly<{ payload_digest: string; receipt_json: string }>;
type EventRow = Readonly<{
  cursor: number;
  aggregate_id: string;
  aggregate_version: number;
  kind: string;
  payload_json: string;
  occurred_at: string;
}>;

export type CardSnapshot = Readonly<{
  cardId: CardId;
  revision: CardRevision;
  version: number;
  observedAt: string;
  attempts: readonly AttemptSnapshot[];
  handoffs: readonly HandoffSnapshot[];
}>;

export type AttemptSnapshot = Readonly<{
  attemptId: AttemptId;
  cardId: CardId;
  revision: CardRevision;
  workspaceId: string;
  providerId: string;
  runnerId: string;
  principal: string;
  state: Readonly<{ kind: string; details: Readonly<Record<string, unknown>> }>;
  fence: number;
  leaseExpiresAt: string;
}>;

export type HandoffSnapshot = Readonly<{
  handoffId: HandoffId;
  sourceAttemptId: AttemptId;
  capsuleDigest: string;
  state: Readonly<{ kind: string; details: Readonly<Record<string, unknown>> }>;
}>;

export class Coordinator {
  readonly #database: Database.Database;
  readonly #clock: Clock;

  constructor(input: Readonly<{ databasePath: string; clock?: Clock }>) {
    if (input.databasePath !== ":memory:") mkdirSync(dirname(input.databasePath), { recursive: true, mode: 0o700 });
    this.#database = new Database(input.databasePath);
    this.#clock = input.clock ?? (() => new Date());
    this.#migrate();
  }

  close(): void {
    this.#database.close();
  }

  execute(raw: unknown): CommandReceipt {
    const envelope = parse(CommandEnvelopeSchema, raw);
    const wire = encode(CommandEnvelopeSchema, envelope);
    const payloadDigest = sha256(stableJson(wire));
    const prior = this.#database.prepare<[string, string], CommandRow>("SELECT payload_digest, receipt_json FROM commands WHERE principal = ? AND request_id = ?")
      .get(envelope.principal, envelope.requestId.value);
    if (prior !== undefined) {
      if (prior.payload_digest !== payloadDigest) {
        return { kind: "rejected", code: "policy_violation", message: "request ID was reused with a different payload" };
      }
      const original = parse(CommandReceiptSchema, JSON.parse(prior.receipt_json));
      if (original.kind === "accepted") return { kind: "duplicate", version: original.version, cursor: original.cursor };
      return original;
    }

    const transaction = this.#database.transaction((command: CommandEnvelope): CommandReceipt => {
      const result = this.#apply(command);
      const receiptJson = JSON.stringify(encode(CommandReceiptSchema, result));
      this.#database.prepare("INSERT INTO commands(principal, request_id, payload_digest, receipt_json, created_at) VALUES (?, ?, ?, ?, ?)")
        .run(command.principal, command.requestId.value, payloadDigest, receiptJson, this.#clock().toISOString());
      return result;
    });
    return transaction(envelope);
  }

  queryCard(cardId: CardId): CardSnapshot | null {
    const card = this.#card(cardId.value);
    if (card === undefined) return null;
    const attempts = this.#database.prepare<[string], AttemptRow>("SELECT * FROM attempts WHERE card_id = ? ORDER BY created_at, attempt_id")
      .all(cardId.value);
    const handoffs = this.#database.prepare<[string], HandoffRow>("SELECT * FROM handoffs WHERE card_id = ? ORDER BY created_at, handoff_id")
      .all(cardId.value);
    return {
      cardId,
      revision: new CardRevision(card.revision),
      version: card.version,
      observedAt: card.observed_at,
      attempts: attempts.map((attempt) => this.#attemptSnapshot(attempt)),
      handoffs: handoffs.map((handoff) => ({
        handoffId: new HandoffId(handoff.handoff_id),
        sourceAttemptId: new AttemptId(handoff.source_attempt_id),
        capsuleDigest: handoff.capsule_digest,
        state: { kind: handoff.state_kind, details: parseJsonRecord(handoff.state_json) },
      })),
    };
  }

  eventsAfter(cursor: number, limit = 100): readonly RuntimeEvent[] {
    if (!Number.isSafeInteger(cursor) || cursor < 0) throw new Error("cursor must be a nonnegative safe integer");
    if (!Number.isSafeInteger(limit) || limit < 1 || limit > 1000) throw new Error("limit must be between 1 and 1000");
    const rows = this.#database.prepare<[number, number], EventRow>("SELECT * FROM events WHERE cursor > ? ORDER BY cursor LIMIT ?")
      .all(cursor, limit);
    return rows.map((row) => ({
      cursor: row.cursor,
      aggregateId: row.aggregate_id,
      aggregateVersion: row.aggregate_version,
      kind: row.kind,
      payload: parseJsonRecord(row.payload_json),
      occurredAt: row.occurred_at,
    }));
  }

  pendingOperations(): readonly Readonly<{ operationId: OperationId; kind: string; payload: Readonly<Record<string, unknown>> }>[] {
    const rows = this.#database.prepare<[], Readonly<{ operation_id: string; kind: string; payload_json: string }>>("SELECT operation_id, kind, payload_json FROM operations WHERE state = 'pending' ORDER BY created_at")
      .all();
    return rows.map((row) => ({ operationId: new OperationId(row.operation_id), kind: row.kind, payload: parseJsonRecord(row.payload_json) }));
  }

  #apply(envelope: CommandEnvelope): CommandReceipt {
    const cardId = this.#resolveCardId(envelope.command);
    if (cardId === null && envelope.command.kind !== "observeCard") {
      return { kind: "rejected", code: "not_found", message: "the referenced attempt or handoff does not exist" };
    }
    if (envelope.command.kind === "observeCard") return this.#observeCard(envelope);
    const card = this.#card(cardId?.value ?? "");
    if (card === undefined) return { kind: "rejected", code: "not_found", message: "card has not been observed" };
    if (card.version !== envelope.expectedVersion) {
      return { kind: "rejected", code: "version_conflict", message: `expected card version ${envelope.expectedVersion}, found ${card.version}` };
    }
    return this.#applyToCard(envelope.principal, envelope.command, card);
  }

  #applyToCard(principal: string, command: Exclude<RuntimeCommand, { kind: "observeCard" }>, card: CardRow): CommandReceipt {
    switch (command.kind) {
      case "claimCard": return this.#claim(principal, card, command);
      case "recordProviderStarted": return this.#recordProviderStarted(card, command);
      case "saveCheckpoint": return this.#saveCheckpoint(card, command);
      case "heartbeatAttempt": return this.#heartbeatAttempt(card, command);
      case "requestCancellation": return this.#requestCancellation(card, command);
      case "recordStopped": return this.#recordStopped(card, command);
      case "recordStopUnknown": return this.#recordStopUnknown(card, command);
      case "prepareHandoff": return this.#prepareHandoff(card, command);
      case "approveHandoff": return this.#approveHandoff(card, command);
      case "activateHandoff": return this.#activateHandoff(card, command);
      case "acknowledgeHandoff": return this.#acknowledgeHandoff(card, command);
      case "recordHandoffUnknown": return this.#recordHandoffUnknown(card, command);
      case "recordEvidence": return this.#recordEvidence(card, command);
      case "completeAttempt": return this.#completeAttempt(card, command);
      default: return assertNever(command);
    }
  }

  #observeCard(envelope: CommandEnvelope): CommandReceipt {
    const command = envelope.command;
    if (command.kind !== "observeCard") throw new Error("observeCard command required");
    const existing = this.#card(command.cardId.value);
    if (existing === undefined) {
      if (envelope.expectedVersion !== 0) return { kind: "rejected", code: "version_conflict", message: "new cards require expected version 0" };
      this.#database.prepare("INSERT INTO cards(card_id, revision, version, observed_at) VALUES (?, ?, 1, ?)")
        .run(command.cardId.value, command.revision.value, command.observedAt);
      const cursor = this.#event(command.cardId.value, 1, "card.observed", { revision: command.revision.value });
      return { kind: "accepted", version: 1, cursor, operationId: null };
    }
    if (existing.version !== envelope.expectedVersion) {
      return { kind: "rejected", code: "version_conflict", message: `expected card version ${envelope.expectedVersion}, found ${existing.version}` };
    }
    if (existing.revision === command.revision.value) return { kind: "accepted", version: existing.version, cursor: this.#latestCursor(), operationId: null };
    const version = existing.version + 1;
    this.#database.prepare("UPDATE cards SET revision = ?, version = ?, observed_at = ? WHERE card_id = ?")
      .run(command.revision.value, version, command.observedAt, command.cardId.value);
    const active = this.#database.prepare<[string], AttemptRow>("SELECT * FROM attempts WHERE card_id = ? AND state_kind IN ('starting','running','stop_requested','stop_unknown')")
      .all(command.cardId.value);
    for (const attempt of active) {
      const operation = new OperationId(randomUUID());
      this.#database.prepare("UPDATE attempts SET state_kind = 'stop_requested', state_json = ? WHERE attempt_id = ?")
        .run(JSON.stringify({ operationId: operation.value, reason: "card revision changed" }), attempt.attempt_id);
      this.#operation(operation, "interrupt", { attemptId: attempt.attempt_id, reason: "card revision changed" });
    }
    const cursor = this.#event(command.cardId.value, version, "card.revision_changed", { previous: existing.revision, current: command.revision.value });
    return { kind: "accepted", version, cursor, operationId: null };
  }

  #claim(principal: string, card: CardRow, command: Extract<RuntimeCommand, { kind: "claimCard" }>): CommandReceipt {
    if (command.card.revision.value !== card.revision) return { kind: "rejected", code: "revision_conflict", message: "claim uses a stale card revision" };
    const active = this.#database.prepare<[string], Readonly<{ attempt_id: string }>>("SELECT attempt_id FROM attempts WHERE card_id = ? AND state_kind IN ('handoff_pending','starting','running','stop_requested','stop_unknown') LIMIT 1")
      .get(card.card_id);
    if (active !== undefined) return { kind: "rejected", code: "ownership_unresolved", message: `writer ${active.attempt_id} still owns or may own the card` };
    const duplicate = this.#database.prepare<[string], Readonly<{ attempt_id: string }>>("SELECT attempt_id FROM attempts WHERE attempt_id = ?")
      .get(command.attemptId.value);
    if (duplicate !== undefined) return { kind: "rejected", code: "policy_violation", message: "attempt ID already exists" };
    const fenceRow = this.#database.prepare<[string], Readonly<{ fence: number }>>("SELECT COALESCE(MAX(fence), 0) AS fence FROM attempts WHERE card_id = ?")
      .get(card.card_id);
    if (fenceRow === undefined) throw new Error("fence query returned no row");
    const operation = new OperationId(randomUUID());
    const expires = new Date(this.#clock().getTime() + command.leaseSeconds * 1000).toISOString();
    this.#database.prepare(`INSERT INTO attempts(
      attempt_id, card_id, revision, workspace_id, provider_id, runner_id, principal,
      state_kind, state_json, fence, lease_expires_at, budget_json, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, 'starting', ?, ?, ?, ?, ?)`).run(
      command.attemptId.value, card.card_id, card.revision, command.workspaceId.value,
      command.providerId.value, command.runnerId.value, principal,
      JSON.stringify({ operationId: operation.value }), fenceRow.fence + 1, expires,
      JSON.stringify(command.budget), this.#clock().toISOString(),
    );
    this.#operation(operation, "start", { attemptId: command.attemptId.value, workspaceId: command.workspaceId.value, fence: fenceRow.fence + 1 });
    return this.#advance(card, "attempt.claimed", { attemptId: command.attemptId.value, operationId: operation.value }, operation);
  }

  #recordProviderStarted(card: CardRow, command: Extract<RuntimeCommand, { kind: "recordProviderStarted" }>): CommandReceipt {
    const attempt = this.#attempt(command.attemptId.value);
    if (attempt === undefined || attempt.state_kind !== "starting") return { kind: "rejected", code: "policy_violation", message: "attempt is not waiting for provider start" };
    const details = parseJsonRecord(attempt.state_json);
    if (details["operationId"] !== command.operationId.value) return { kind: "rejected", code: "policy_violation", message: "provider observation uses the wrong operation" };
    this.#database.prepare("UPDATE attempts SET state_kind = 'running', state_json = ? WHERE attempt_id = ?")
      .run(JSON.stringify({ sessionRef: command.sessionRef }), command.attemptId.value);
    this.#completeOperation(command.operationId);
    return this.#advance(card, "attempt.running", { attemptId: command.attemptId.value, sessionRef: command.sessionRef }, command.operationId);
  }

  #saveCheckpoint(card: CardRow, command: Extract<RuntimeCommand, { kind: "saveCheckpoint" }>): CommandReceipt {
    const attempt = this.#attempt(command.attemptId.value);
    if (attempt === undefined || !["running", "stop_requested", "paused"].includes(attempt.state_kind)) {
      return { kind: "rejected", code: "policy_violation", message: "attempt cannot checkpoint in its current state" };
    }
    this.#database.prepare("INSERT INTO checkpoints(attempt_id, dirty_digest, completed_json, next_action, created_at) VALUES (?, ?, ?, ?, ?)")
      .run(command.attemptId.value, command.dirtyDigest, JSON.stringify(command.completedCriteria), command.nextAction, this.#clock().toISOString());
    return this.#advance(card, "attempt.checkpointed", { attemptId: command.attemptId.value, nextAction: command.nextAction }, null);
  }

  #heartbeatAttempt(card: CardRow, command: Extract<RuntimeCommand, { kind: "heartbeatAttempt" }>): CommandReceipt {
    const attempt = this.#attempt(command.attemptId.value);
    if (attempt === undefined || !["starting", "running"].includes(attempt.state_kind)) {
      return { kind: "rejected", code: "policy_violation", message: "attempt is not heartbeat-eligible" };
    }
    if (attempt.fence !== command.fence) return { kind: "rejected", code: "ownership_unresolved", message: "heartbeat carries a stale fencing token" };
    const expiresAt = new Date(this.#clock().getTime() + command.leaseSeconds * 1000).toISOString();
    this.#database.prepare("UPDATE attempts SET lease_expires_at = ? WHERE attempt_id = ?").run(expiresAt, command.attemptId.value);
    return this.#advance(card, "attempt.heartbeat", { attemptId: command.attemptId.value, fence: command.fence, leaseExpiresAt: expiresAt }, null);
  }

  #requestCancellation(card: CardRow, command: Extract<RuntimeCommand, { kind: "requestCancellation" }>): CommandReceipt {
    const attempt = this.#attempt(command.attemptId.value);
    if (attempt === undefined || !["starting", "running"].includes(attempt.state_kind)) return { kind: "rejected", code: "policy_violation", message: "attempt is not cancellable" };
    this.#database.prepare("UPDATE attempts SET state_kind = 'stop_requested', state_json = ? WHERE attempt_id = ?")
      .run(JSON.stringify({ operationId: command.operationId.value, reason: command.reason }), command.attemptId.value);
    this.#operation(command.operationId, "interrupt", { attemptId: command.attemptId.value, reason: command.reason });
    return this.#advance(card, "attempt.stop_requested", { attemptId: command.attemptId.value, operationId: command.operationId.value }, command.operationId);
  }

  #recordStopped(card: CardRow, command: Extract<RuntimeCommand, { kind: "recordStopped" }>): CommandReceipt {
    const attempt = this.#attempt(command.attemptId.value);
    if (attempt === undefined || attempt.state_kind !== "stop_requested") return { kind: "rejected", code: "policy_violation", message: "attempt has no pending stop" };
    const details = parseJsonRecord(attempt.state_json);
    if (details["operationId"] !== command.operationId.value) return { kind: "rejected", code: "policy_violation", message: "stop receipt uses the wrong operation" };
    this.#database.prepare("UPDATE attempts SET state_kind = 'paused', state_json = ? WHERE attempt_id = ?")
      .run(JSON.stringify({ quiescenceReceipt: command.receiptDigest }), command.attemptId.value);
    this.#completeOperation(command.operationId);
    return this.#advance(card, "attempt.stopped", { attemptId: command.attemptId.value, receiptDigest: command.receiptDigest }, command.operationId);
  }

  #recordStopUnknown(card: CardRow, command: Extract<RuntimeCommand, { kind: "recordStopUnknown" }>): CommandReceipt {
    const attempt = this.#attempt(command.attemptId.value);
    if (attempt === undefined || attempt.state_kind !== "stop_requested") return { kind: "rejected", code: "policy_violation", message: "attempt has no pending stop" };
    this.#database.prepare("UPDATE attempts SET state_kind = 'stop_unknown', state_json = ? WHERE attempt_id = ?")
      .run(JSON.stringify({ operationId: command.operationId.value, reason: command.reason }), command.attemptId.value);
    this.#database.prepare("UPDATE operations SET state = 'unknown', updated_at = ? WHERE operation_id = ?")
      .run(this.#clock().toISOString(), command.operationId.value);
    return this.#advance(card, "attempt.stop_unknown", { attemptId: command.attemptId.value, reason: command.reason }, command.operationId);
  }

  #prepareHandoff(card: CardRow, command: Extract<RuntimeCommand, { kind: "prepareHandoff" }>): CommandReceipt {
    const attempt = this.#attempt(command.sourceAttemptId.value);
    if (attempt === undefined || !["running", "paused"].includes(attempt.state_kind)) return { kind: "rejected", code: "policy_violation", message: "source attempt is not handoff-ready" };
    const existing = this.#database.prepare<[string], Readonly<{ handoff_id: string }>>("SELECT handoff_id FROM handoffs WHERE handoff_id = ?").get(command.handoffId.value);
    if (existing !== undefined) return { kind: "rejected", code: "policy_violation", message: "handoff ID already exists" };
    const operation = new OperationId(randomUUID());
    this.#database.prepare(`INSERT INTO handoffs(
      handoff_id, card_id, source_attempt_id, destination_provider_id, destination_runner_id,
      capsule_digest, state_kind, state_json, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, 'awaiting_approval', ?, ?)`).run(
      command.handoffId.value, card.card_id, command.sourceAttemptId.value,
      command.destinationProviderId.value, command.destinationRunnerId.value, command.capsuleDigest,
      JSON.stringify({ capsuleDigest: command.capsuleDigest }), this.#clock().toISOString(),
    );
    if (attempt.state_kind === "running") {
      this.#database.prepare("UPDATE attempts SET state_kind = 'stop_requested', state_json = ? WHERE attempt_id = ?")
        .run(JSON.stringify({ operationId: operation.value, reason: "writer handoff" }), command.sourceAttemptId.value);
      this.#operation(operation, "interrupt", { attemptId: command.sourceAttemptId.value, reason: "writer handoff" });
    }
    return this.#advance(card, "handoff.prepared", { handoffId: command.handoffId.value, capsuleDigest: command.capsuleDigest }, operation);
  }

  #approveHandoff(card: CardRow, command: Extract<RuntimeCommand, { kind: "approveHandoff" }>): CommandReceipt {
    const handoff = this.#handoff(command.handoffId.value);
    if (handoff === undefined || handoff.state_kind !== "awaiting_approval") return { kind: "rejected", code: "policy_violation", message: "handoff is not awaiting approval" };
    const source = this.#attempt(handoff.source_attempt_id);
    if (source === undefined || source.state_kind !== "paused") return { kind: "rejected", code: "ownership_unresolved", message: "source writer has not produced a quiescence receipt" };
    if (handoff.capsule_digest !== command.capsuleDigest) return { kind: "rejected", code: "policy_violation", message: "approval does not match the frozen capsule" };
    const approvedAt = Date.parse(command.approvedAt);
    const expiresAt = Date.parse(command.expiresAt);
    if (expiresAt <= approvedAt || expiresAt <= this.#clock().getTime()) return { kind: "rejected", code: "policy_violation", message: "handoff approval is expired" };
    this.#database.prepare("UPDATE handoffs SET state_kind = 'approved', state_json = ? WHERE handoff_id = ?")
      .run(JSON.stringify({ capsuleDigest: command.capsuleDigest, approvedBy: command.approvedBy, approvedAt: command.approvedAt, expiresAt: command.expiresAt }), command.handoffId.value);
    return this.#advance(card, "handoff.approved", { handoffId: command.handoffId.value, approvedBy: command.approvedBy }, null);
  }

  #activateHandoff(card: CardRow, command: Extract<RuntimeCommand, { kind: "activateHandoff" }>): CommandReceipt {
    const handoff = this.#handoff(command.handoffId.value);
    if (handoff === undefined || handoff.state_kind !== "approved") return { kind: "rejected", code: "policy_violation", message: "handoff lacks user approval" };
    const approval = parseJsonRecord(handoff.state_json);
    if (typeof approval["expiresAt"] !== "string" || Date.parse(approval["expiresAt"]) <= this.#clock().getTime()) {
      return { kind: "rejected", code: "policy_violation", message: "handoff approval expired before activation" };
    }
    const source = this.#attempt(handoff.source_attempt_id);
    if (source === undefined || source.state_kind !== "paused") return { kind: "rejected", code: "ownership_unresolved", message: "source ownership is unresolved" };
    const duplicate = this.#attempt(command.destinationAttemptId.value);
    if (duplicate !== undefined) return { kind: "rejected", code: "policy_violation", message: "destination attempt already exists" };
    const fenceRow = this.#database.prepare<[string], Readonly<{ fence: number }>>("SELECT COALESCE(MAX(fence), 0) AS fence FROM attempts WHERE card_id = ?").get(card.card_id);
    if (fenceRow === undefined) throw new Error("fence query returned no row");
    this.#database.prepare(`INSERT INTO attempts(
      attempt_id, card_id, revision, workspace_id, provider_id, runner_id, principal,
      state_kind, state_json, fence, lease_expires_at, budget_json, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, 'handoff_pending', ?, ?, ?, ?, ?)`).run(
      command.destinationAttemptId.value, card.card_id, card.revision, command.destinationWorkspaceId.value,
      handoff.destination_provider_id, handoff.destination_runner_id, String(approval["approvedBy"]),
      JSON.stringify({ handoffId: command.handoffId.value, capsuleDigest: handoff.capsule_digest }), fenceRow.fence + 1,
      new Date(this.#clock().getTime() + 3600_000).toISOString(), JSON.stringify({ inherited: true }), this.#clock().toISOString(),
    );
    this.#database.prepare("UPDATE handoffs SET state_kind = 'awaiting_ack', state_json = ? WHERE handoff_id = ?")
      .run(JSON.stringify({ destinationAttemptId: command.destinationAttemptId.value, revision: card.revision, capsuleDigest: handoff.capsule_digest }), command.handoffId.value);
    return this.#advance(card, "handoff.awaiting_ack", { handoffId: command.handoffId.value, destinationAttemptId: command.destinationAttemptId.value, revision: card.revision }, null);
  }

  #acknowledgeHandoff(card: CardRow, command: Extract<RuntimeCommand, { kind: "acknowledgeHandoff" }>): CommandReceipt {
    const handoff = this.#handoff(command.handoffId.value);
    if (handoff === undefined || handoff.state_kind !== "awaiting_ack") return { kind: "rejected", code: "policy_violation", message: "handoff is not awaiting destination acknowledgement" };
    const details = parseJsonRecord(handoff.state_json);
    if (details["destinationAttemptId"] !== command.destinationAttemptId.value) return { kind: "rejected", code: "policy_violation", message: "acknowledgement names the wrong destination attempt" };
    if (command.revision.value !== card.revision || details["revision"] !== command.revision.value) return { kind: "rejected", code: "revision_conflict", message: "destination did not acknowledge the canonical card revision" };
    if (command.capsuleDigest !== handoff.capsule_digest || details["capsuleDigest"] !== command.capsuleDigest) return { kind: "rejected", code: "policy_violation", message: "destination did not acknowledge the frozen capsule" };
    const destination = this.#attempt(command.destinationAttemptId.value);
    if (destination === undefined || destination.state_kind !== "handoff_pending") return { kind: "rejected", code: "ownership_unresolved", message: "destination writer state is unresolved" };
    const operation = new OperationId(randomUUID());
    this.#database.prepare("UPDATE attempts SET state_kind = 'starting', state_json = ? WHERE attempt_id = ?")
      .run(JSON.stringify({ operationId: operation.value, handoffId: command.handoffId.value }), command.destinationAttemptId.value);
    this.#database.prepare("UPDATE handoffs SET state_kind = 'active', state_json = ? WHERE handoff_id = ?")
      .run(JSON.stringify({ destinationAttemptId: command.destinationAttemptId.value, operationId: operation.value, revision: command.revision.value, capsuleDigest: command.capsuleDigest }), command.handoffId.value);
    this.#operation(operation, "start", { attemptId: command.destinationAttemptId.value, workspaceId: destination.workspace_id, handoffId: command.handoffId.value, fence: destination.fence });
    return this.#advance(card, "handoff.acknowledged", { handoffId: command.handoffId.value, destinationAttemptId: command.destinationAttemptId.value }, operation);
  }

  #recordHandoffUnknown(card: CardRow, command: Extract<RuntimeCommand, { kind: "recordHandoffUnknown" }>): CommandReceipt {
    const handoff = this.#handoff(command.handoffId.value);
    if (handoff === undefined || handoff.state_kind !== "awaiting_ack") return { kind: "rejected", code: "policy_violation", message: "handoff is not awaiting destination acknowledgement" };
    const details = parseJsonRecord(handoff.state_json);
    const destinationAttemptId = details["destinationAttemptId"];
    if (typeof destinationAttemptId !== "string") return { kind: "rejected", code: "ownership_unresolved", message: "destination attempt cannot be reconciled" };
    this.#database.prepare("UPDATE attempts SET state_kind = 'stop_unknown', state_json = ? WHERE attempt_id = ?")
      .run(JSON.stringify({ reason: command.reason, handoffId: command.handoffId.value }), destinationAttemptId);
    this.#database.prepare("UPDATE handoffs SET state_kind = 'handoff_unknown', state_json = ? WHERE handoff_id = ?")
      .run(JSON.stringify({ reason: command.reason, destinationAttemptId }), command.handoffId.value);
    return this.#advance(card, "handoff.unknown", { handoffId: command.handoffId.value, reason: command.reason }, null);
  }

  #recordEvidence(card: CardRow, command: Extract<RuntimeCommand, { kind: "recordEvidence" }>): CommandReceipt {
    const attempt = this.#attempt(command.attemptId.value);
    if (attempt === undefined) return { kind: "rejected", code: "not_found", message: "evidence attempt does not exist" };
    if (attempt.principal === command.verifier) return { kind: "rejected", code: "policy_violation", message: "the writer cannot verify its own candidate" };
    this.#database.prepare(`INSERT INTO evidence(
      evidence_id, card_id, attempt_id, candidate, criterion, verifier, outcome, artifact_ids_json, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`).run(
      command.evidenceId.value, card.card_id, command.attemptId.value, command.candidate.value,
      command.criterion, command.verifier, command.outcome,
      JSON.stringify(command.artifactIds.map((artifact) => artifact.value)), this.#clock().toISOString(),
    );
    return this.#advance(card, "evidence.recorded", { evidenceId: command.evidenceId.value, outcome: command.outcome, candidate: command.candidate.value }, null);
  }

  #completeAttempt(card: CardRow, command: Extract<RuntimeCommand, { kind: "completeAttempt" }>): CommandReceipt {
    const attempt = this.#attempt(command.attemptId.value);
    if (attempt === undefined || !["running", "paused"].includes(attempt.state_kind)) {
      return { kind: "rejected", code: "policy_violation", message: "attempt is not completion-eligible" };
    }
    const evidence = this.#database.prepare<[string, string], Readonly<{ criterion: string; outcome: string }>>(
      "SELECT criterion, outcome FROM evidence WHERE attempt_id = ? AND candidate = ? ORDER BY created_at",
    ).all(command.attemptId.value, command.candidate.value);
    const passed = new Set(evidence.filter((row) => row.outcome === "passed").map((row) => row.criterion));
    const missing = [...new Set(command.requiredCriteria)].filter((criterion) => !passed.has(criterion));
    if (missing.length > 0) return { kind: "rejected", code: "policy_violation", message: `exact candidate lacks passing evidence for: ${missing.join(", ")}` };
    this.#database.prepare("UPDATE attempts SET state_kind = 'completed', state_json = ? WHERE attempt_id = ?")
      .run(JSON.stringify({ candidate: command.candidate.value, summary: command.summary, requiredCriteria: command.requiredCriteria }), command.attemptId.value);
    return this.#advance(card, "attempt.completed", { attemptId: command.attemptId.value, candidate: command.candidate.value, summary: command.summary }, null);
  }

  #resolveCardId(command: RuntimeCommand): CardId | null {
    switch (command.kind) {
      case "observeCard": return command.cardId;
      case "claimCard": return command.card.cardId;
      case "recordProviderStarted":
      case "saveCheckpoint":
      case "heartbeatAttempt":
      case "requestCancellation":
      case "recordStopped":
      case "recordStopUnknown":
      case "prepareHandoff":
      case "recordEvidence": {
        const attemptId = command.kind === "prepareHandoff" ? command.sourceAttemptId : command.attemptId;
        const attempt = this.#attempt(attemptId.value);
        return attempt === undefined ? null : new CardId(attempt.card_id);
      }
      case "completeAttempt": {
        const attempt = this.#attempt(command.attemptId.value);
        return attempt === undefined ? null : new CardId(attempt.card_id);
      }
      case "approveHandoff":
      case "activateHandoff":
      case "acknowledgeHandoff":
      case "recordHandoffUnknown": {
        const handoff = this.#handoff(command.handoffId.value);
        return handoff === undefined ? null : new CardId(handoff.card_id);
      }
      default: return assertNever(command);
    }
  }

  #advance(card: CardRow, kind: string, payload: Readonly<Record<string, unknown>>, operationId: OperationId | null): CommandReceipt {
    const version = card.version + 1;
    this.#database.prepare("UPDATE cards SET version = ? WHERE card_id = ?").run(version, card.card_id);
    const cursor = this.#event(card.card_id, version, kind, payload);
    return { kind: "accepted", version, cursor, operationId };
  }

  #event(aggregateId: string, version: number, kind: string, payload: Readonly<Record<string, unknown>>): number {
    const result = this.#database.prepare("INSERT INTO events(aggregate_id, aggregate_version, kind, payload_json, occurred_at) VALUES (?, ?, ?, ?, ?)")
      .run(aggregateId, version, kind, JSON.stringify(payload), this.#clock().toISOString());
    return Number(result.lastInsertRowid);
  }

  #operation(operationId: OperationId, kind: string, payload: Readonly<Record<string, unknown>>): void {
    this.#database.prepare("INSERT INTO operations(operation_id, kind, payload_json, state, created_at, updated_at) VALUES (?, ?, ?, 'pending', ?, ?)")
      .run(operationId.value, kind, JSON.stringify(payload), this.#clock().toISOString(), this.#clock().toISOString());
  }

  #completeOperation(operationId: OperationId): void {
    this.#database.prepare("UPDATE operations SET state = 'completed', updated_at = ? WHERE operation_id = ?")
      .run(this.#clock().toISOString(), operationId.value);
  }

  #card(cardId: string): CardRow | undefined {
    return this.#database.prepare<[string], CardRow>("SELECT * FROM cards WHERE card_id = ?").get(cardId);
  }

  #attempt(attemptId: string): AttemptRow | undefined {
    return this.#database.prepare<[string], AttemptRow>("SELECT * FROM attempts WHERE attempt_id = ?").get(attemptId);
  }

  #handoff(handoffId: string): HandoffRow | undefined {
    return this.#database.prepare<[string], HandoffRow>("SELECT * FROM handoffs WHERE handoff_id = ?").get(handoffId);
  }

  #attemptSnapshot(attempt: AttemptRow): AttemptSnapshot {
    return {
      attemptId: new AttemptId(attempt.attempt_id),
      cardId: new CardId(attempt.card_id),
      revision: new CardRevision(attempt.revision),
      workspaceId: attempt.workspace_id,
      providerId: attempt.provider_id,
      runnerId: attempt.runner_id,
      principal: attempt.principal,
      state: { kind: attempt.state_kind, details: parseJsonRecord(attempt.state_json) },
      fence: attempt.fence,
      leaseExpiresAt: attempt.lease_expires_at,
    };
  }

  #latestCursor(): number {
    const row = this.#database.prepare<[], Readonly<{ cursor: number }>>("SELECT COALESCE(MAX(cursor), 0) AS cursor FROM events").get();
    if (row === undefined) throw new Error("cursor query returned no row");
    return row.cursor;
  }

  #migrate(): void {
    this.#database.pragma("journal_mode = WAL");
    this.#database.pragma("foreign_keys = ON");
    this.#database.pragma("busy_timeout = 5000");
    this.#database.pragma("synchronous = FULL");
    this.#database.exec(`
      CREATE TABLE IF NOT EXISTS cards (
        card_id TEXT PRIMARY KEY,
        revision TEXT NOT NULL,
        version INTEGER NOT NULL,
        observed_at TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS attempts (
        attempt_id TEXT PRIMARY KEY,
        card_id TEXT NOT NULL REFERENCES cards(card_id),
        revision TEXT NOT NULL,
        workspace_id TEXT NOT NULL,
        provider_id TEXT NOT NULL,
        runner_id TEXT NOT NULL,
        principal TEXT NOT NULL,
        state_kind TEXT NOT NULL,
        state_json TEXT NOT NULL,
        fence INTEGER NOT NULL,
        lease_expires_at TEXT NOT NULL,
        budget_json TEXT NOT NULL,
        created_at TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS handoffs (
        handoff_id TEXT PRIMARY KEY,
        card_id TEXT NOT NULL REFERENCES cards(card_id),
        source_attempt_id TEXT NOT NULL REFERENCES attempts(attempt_id),
        destination_provider_id TEXT NOT NULL,
        destination_runner_id TEXT NOT NULL,
        capsule_digest TEXT NOT NULL,
        state_kind TEXT NOT NULL,
        state_json TEXT NOT NULL,
        created_at TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS checkpoints (
        checkpoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
        attempt_id TEXT NOT NULL REFERENCES attempts(attempt_id),
        dirty_digest TEXT,
        completed_json TEXT NOT NULL,
        next_action TEXT NOT NULL,
        created_at TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS evidence (
        evidence_id TEXT PRIMARY KEY,
        card_id TEXT NOT NULL REFERENCES cards(card_id),
        attempt_id TEXT NOT NULL REFERENCES attempts(attempt_id),
        candidate TEXT NOT NULL,
        criterion TEXT NOT NULL,
        verifier TEXT NOT NULL,
        outcome TEXT NOT NULL,
        artifact_ids_json TEXT NOT NULL,
        created_at TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS operations (
        operation_id TEXT PRIMARY KEY,
        kind TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        state TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS commands (
        principal TEXT NOT NULL,
        request_id TEXT NOT NULL,
        payload_digest TEXT NOT NULL,
        receipt_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        PRIMARY KEY(principal, request_id)
      );
      CREATE TABLE IF NOT EXISTS events (
        cursor INTEGER PRIMARY KEY AUTOINCREMENT,
        aggregate_id TEXT NOT NULL,
        aggregate_version INTEGER NOT NULL,
        kind TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        occurred_at TEXT NOT NULL
      );
      CREATE INDEX IF NOT EXISTS attempts_card_state ON attempts(card_id, state_kind);
      CREATE INDEX IF NOT EXISTS events_aggregate ON events(aggregate_id, cursor);
    `);
  }
}

function parseJsonRecord(raw: string): Readonly<Record<string, unknown>> {
  const value: unknown = JSON.parse(raw);
  if (value === null || Array.isArray(value) || typeof value !== "object") throw new Error("stored JSON is not an object");
  return Object.fromEntries(Object.entries(value));
}
