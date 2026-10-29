import { request as httpRequest } from "node:http";
import { randomUUID } from "node:crypto";
import { CardId, CommandReceiptSchema, type CardSnapshotWire, type CommandReceipt, type CoordinatorQuery, type RuntimeEvent, parse } from "@super-speckit/protocol";
import { Coordinator, type CardSnapshot } from "@super-speckit/coordinator";

export interface CoordinatorClient {
  execute(command: unknown): Promise<CommandReceipt>;
  query(query: Extract<CoordinatorQuery, { kind: "card" }>): Promise<CardSnapshotWire | null>;
  query(query: Extract<CoordinatorQuery, { kind: "events" }>): Promise<readonly RuntimeEvent[]>;
  watch(input: Readonly<{ after: number; signal?: AbortSignal; pollMilliseconds?: number }>): AsyncIterable<RuntimeEvent>;
}

export class DirectCoordinatorClient implements CoordinatorClient {
  readonly #coordinator: Coordinator;

  constructor(coordinator: Coordinator) {
    this.#coordinator = coordinator;
  }

  async execute(command: unknown): Promise<CommandReceipt> {
    return this.#coordinator.execute(command);
  }

  async query(query: Extract<CoordinatorQuery, { kind: "card" }>): Promise<CardSnapshotWire | null>;
  async query(query: Extract<CoordinatorQuery, { kind: "events" }>): Promise<readonly RuntimeEvent[]>;
  async query(query: CoordinatorQuery): Promise<CardSnapshotWire | null | readonly RuntimeEvent[]> {
    if (query.kind === "card") return snapshotWire(this.#coordinator.queryCard(query.cardId));
    return this.#coordinator.eventsAfter(query.after, query.limit);
  }

  async *watch(input: Readonly<{ after: number; signal?: AbortSignal; pollMilliseconds?: number }>): AsyncIterable<RuntimeEvent> {
    let cursor = input.after;
    const poll = input.pollMilliseconds ?? 250;
    while (input.signal?.aborted !== true) {
      const events = this.#coordinator.eventsAfter(cursor);
      if (events.length === 0) {
        await delay(poll, input.signal);
        continue;
      }
      for (const event of events) {
        cursor = event.cursor;
        yield event;
      }
    }
  }
}

export class SocketCoordinatorClient implements CoordinatorClient {
  readonly #socketPath: string;
  readonly #token: string;

  constructor(input: Readonly<{ socketPath: string; token: string }>) {
    this.#socketPath = input.socketPath;
    this.#token = input.token;
  }

  async execute(command: unknown): Promise<CommandReceipt> {
    const raw = await this.#call("execute", command);
    return parse(CommandReceiptSchema, raw);
  }

  async query(query: Extract<CoordinatorQuery, { kind: "card" }>): Promise<CardSnapshotWire | null>;
  async query(query: Extract<CoordinatorQuery, { kind: "events" }>): Promise<readonly RuntimeEvent[]>;
  async query(query: CoordinatorQuery): Promise<CardSnapshotWire | null | readonly RuntimeEvent[]> {
    if (query.kind === "card") {
      const raw = await this.#call("query.card", { cardId: query.cardId.value });
      return raw === null ? null : parseCardSnapshot(raw);
    }
    const raw = await this.#call("query.events", { after: query.after, limit: query.limit ?? 100 });
    if (!Array.isArray(raw)) throw new Error("coordinator events response is not an array");
    return raw.map(parseRuntimeEvent);
  }

  async *watch(input: Readonly<{ after: number; signal?: AbortSignal; pollMilliseconds?: number }>): AsyncIterable<RuntimeEvent> {
    let cursor = input.after;
    const poll = input.pollMilliseconds ?? 250;
    while (input.signal?.aborted !== true) {
      const events = await this.query({ kind: "events", after: cursor });
      if (events.length === 0) {
        await delay(poll, input.signal);
        continue;
      }
      for (const event of events) {
        cursor = event.cursor;
        yield event;
      }
    }
  }

  #call(method: string, params: unknown): Promise<unknown> {
    const body = JSON.stringify({ jsonrpc: "2.0", id: randomUUID(), method, params });
    return new Promise((resolve, reject) => {
      const request = httpRequest({
        socketPath: this.#socketPath,
        path: "/rpc",
        method: "POST",
        headers: { authorization: `Bearer ${this.#token}`, "content-type": "application/json", "content-length": Buffer.byteLength(body) },
      }, (response) => {
        const chunks: Buffer[] = [];
        response.on("data", (chunk: Buffer) => chunks.push(chunk));
        response.on("end", () => {
          try {
            const payload: unknown = JSON.parse(Buffer.concat(chunks).toString("utf8"));
            if (payload === null || Array.isArray(payload) || typeof payload !== "object") throw new Error("coordinator response is not an object");
            const record = Object.fromEntries(Object.entries(payload));
            if (record["error"] !== undefined) throw new Error(JSON.stringify(record["error"]));
            resolve(record["result"]);
          } catch (error) {
            reject(error);
          }
        });
      });
      request.on("error", reject);
      request.end(body);
    });
  }
}

function snapshotWire(snapshot: CardSnapshot | null): CardSnapshotWire | null {
  if (snapshot === null) return null;
  return {
    cardId: snapshot.cardId.value,
    revision: snapshot.revision.value,
    version: snapshot.version,
    observedAt: snapshot.observedAt,
    attempts: snapshot.attempts.map((attempt) => ({
      attemptId: attempt.attemptId.value,
      revision: attempt.revision.value,
      workspaceId: attempt.workspaceId,
      providerId: attempt.providerId,
      runnerId: attempt.runnerId,
      principal: attempt.principal,
      state: attempt.state,
      fence: attempt.fence,
      leaseExpiresAt: attempt.leaseExpiresAt,
    })),
    handoffs: snapshot.handoffs.map((handoff) => ({
      handoffId: handoff.handoffId.value,
      sourceAttemptId: handoff.sourceAttemptId.value,
      capsuleDigest: handoff.capsuleDigest,
      state: handoff.state,
    })),
  };
}

function parseCardSnapshot(raw: unknown): CardSnapshotWire {
  const record = recordOf(raw, "card snapshot");
  const attemptsRaw = record["attempts"];
  const handoffsRaw = record["handoffs"];
  if (!Array.isArray(attemptsRaw) || !Array.isArray(handoffsRaw)) throw new Error("card snapshot collections are invalid");
  return {
    cardId: stringField(record, "cardId"),
    revision: stringField(record, "revision"),
    version: numberField(record, "version"),
    observedAt: stringField(record, "observedAt"),
    attempts: attemptsRaw.map((attempt) => {
      const item = recordOf(attempt, "attempt");
      return {
        attemptId: stringField(item, "attemptId"),
        revision: stringField(item, "revision"),
        workspaceId: stringField(item, "workspaceId"),
        providerId: stringField(item, "providerId"),
        runnerId: stringField(item, "runnerId"),
        principal: stringField(item, "principal"),
        state: stateField(item),
        fence: numberField(item, "fence"),
        leaseExpiresAt: stringField(item, "leaseExpiresAt"),
      };
    }),
    handoffs: handoffsRaw.map((handoff) => {
      const item = recordOf(handoff, "handoff");
      return {
        handoffId: stringField(item, "handoffId"),
        sourceAttemptId: stringField(item, "sourceAttemptId"),
        capsuleDigest: stringField(item, "capsuleDigest"),
        state: stateField(item),
      };
    }),
  };
}

function parseRuntimeEvent(raw: unknown): RuntimeEvent {
  const record = recordOf(raw, "runtime event");
  return {
    cursor: numberField(record, "cursor"),
    aggregateId: stringField(record, "aggregateId"),
    aggregateVersion: numberField(record, "aggregateVersion"),
    kind: stringField(record, "kind"),
    payload: recordOf(record["payload"], "event payload"),
    occurredAt: stringField(record, "occurredAt"),
  };
}

function stateField(record: Readonly<Record<string, unknown>>): Readonly<{ kind: string; details: Readonly<Record<string, unknown>> }> {
  const state = recordOf(record["state"], "state");
  return { kind: stringField(state, "kind"), details: recordOf(state["details"], "state details") };
}

function recordOf(value: unknown, name: string): Readonly<Record<string, unknown>> {
  if (value === null || Array.isArray(value) || typeof value !== "object") throw new Error(`${name} is not an object`);
  return Object.fromEntries(Object.entries(value));
}

function stringField(record: Readonly<Record<string, unknown>>, name: string): string {
  const value = record[name];
  if (typeof value !== "string") throw new Error(`${name} is not a string`);
  return value;
}

function numberField(record: Readonly<Record<string, unknown>>, name: string): number {
  const value = record[name];
  if (typeof value !== "number" || !Number.isSafeInteger(value)) throw new Error(`${name} is not a safe integer`);
  return value;
}

async function delay(milliseconds: number, signal: AbortSignal | undefined): Promise<void> {
  if (signal?.aborted === true) return;
  await new Promise<void>((resolve) => {
    const timeout = setTimeout(resolve, milliseconds);
    signal?.addEventListener("abort", () => { clearTimeout(timeout); resolve(); }, { once: true });
  });
}

export function cardId(value: string): CardId {
  return new CardId(value);
}
