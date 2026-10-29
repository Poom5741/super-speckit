import assert from "node:assert/strict";
import test from "node:test";
import { CardId } from "@super-speckit/protocol";
import { Coordinator } from "./index.ts";

const REVISION_A = "a".repeat(64);
const REVISION_B = "b".repeat(64);
const DIGEST_C = "c".repeat(64);

function command(input: Readonly<{ request: string; version: number; command: Readonly<Record<string, unknown>> }>): Readonly<Record<string, unknown>> {
  return {
    protocolVersion: 1,
    requestId: input.request,
    principal: "builder-a",
    expectedVersion: input.version,
    command: input.command,
  };
}

function observe(coordinator: Coordinator): void {
  const receipt = coordinator.execute(command({
    request: "observe-1",
    version: 0,
    command: { kind: "observeCard", cardId: "card-1", revision: REVISION_A, observedAt: "2026-10-30T00:00:00.000Z" },
  }));
  assert.deepEqual(receipt, { kind: "accepted", version: 1, cursor: 1, operationId: null });
}

function claim(coordinator: Coordinator, request = "claim-1", version = 1): ReturnType<Coordinator["execute"]> {
  return coordinator.execute(command({
    request,
    version,
    command: {
      kind: "claimCard",
      card: { cardId: "card-1", revision: REVISION_A },
      attemptId: `attempt-${request}`,
      workspaceId: `workspace-${request}`,
      providerId: "provider-fake",
      runnerId: "runner-local",
      leaseSeconds: 3600,
      budget: { wallTimeSeconds: 3600, paidUsdCents: 0 },
    },
  }));
}

test("commands are idempotent and stale versions are rejected", () => {
  const coordinator = new Coordinator({ databasePath: ":memory:" });
  observe(coordinator);
  const first = claim(coordinator);
  assert.equal(first.kind, "accepted");
  const duplicate = claim(coordinator);
  assert.deepEqual(duplicate, { kind: "duplicate", version: 2, cursor: 2 });
  const stale = claim(coordinator, "claim-stale", 1);
  assert.deepEqual(stale, { kind: "rejected", code: "version_conflict", message: "expected card version 1, found 2" });
  coordinator.close();
});

test("an unknown stop keeps the writer slot occupied", () => {
  const coordinator = new Coordinator({ databasePath: ":memory:" });
  observe(coordinator);
  const claimed = claim(coordinator);
  assert.equal(claimed.kind, "accepted");
  if (claimed.kind !== "accepted" || claimed.operationId === null) return;
  const started = coordinator.execute(command({
    request: "started-1",
    version: 2,
    command: { kind: "recordProviderStarted", attemptId: "attempt-claim-1", operationId: claimed.operationId.value, sessionRef: "session-1" },
  }));
  assert.equal(started.kind, "accepted");
  const cancelOperation = "cancel-operation-1";
  const requested = coordinator.execute(command({
    request: "cancel-1",
    version: 3,
    command: { kind: "requestCancellation", attemptId: "attempt-claim-1", operationId: cancelOperation, reason: "test cancellation" },
  }));
  assert.equal(requested.kind, "accepted");
  const unknown = coordinator.execute(command({
    request: "cancel-unknown-1",
    version: 4,
    command: { kind: "recordStopUnknown", attemptId: "attempt-claim-1", operationId: cancelOperation, reason: "runner disconnected" },
  }));
  assert.equal(unknown.kind, "accepted");
  const replacement = claim(coordinator, "replacement", 5);
  assert.deepEqual(replacement, {
    kind: "rejected",
    code: "ownership_unresolved",
    message: "writer attempt-claim-1 still owns or may own the card",
  });
  coordinator.close();
});

test("writer handoff requires source quiescence and approval for the exact capsule", () => {
  const clock = new Date("2026-10-30T00:00:00.000Z");
  const coordinator = new Coordinator({ databasePath: ":memory:", clock: () => clock });
  observe(coordinator);
  const claimed = claim(coordinator);
  assert.equal(claimed.kind, "accepted");
  if (claimed.kind !== "accepted" || claimed.operationId === null) return;
  assert.equal(coordinator.execute(command({
    request: "started-1",
    version: 2,
    command: { kind: "recordProviderStarted", attemptId: "attempt-claim-1", operationId: claimed.operationId.value, sessionRef: "session-1" },
  })).kind, "accepted");
  const prepared = coordinator.execute(command({
    request: "handoff-prepare",
    version: 3,
    command: {
      kind: "prepareHandoff",
      handoffId: "handoff-1",
      sourceAttemptId: "attempt-claim-1",
      destinationProviderId: "provider-ade",
      destinationRunnerId: "runner-remote",
      capsuleDigest: DIGEST_C,
    },
  }));
  assert.equal(prepared.kind, "accepted");
  if (prepared.kind !== "accepted" || prepared.operationId === null) return;
  const tooEarly = coordinator.execute(command({
    request: "handoff-approve-early",
    version: 4,
    command: {
      kind: "approveHandoff",
      handoffId: "handoff-1",
      capsuleDigest: DIGEST_C,
      approvedBy: "poom",
      approvedAt: "2026-10-30T00:00:00.000Z",
      expiresAt: "2026-10-30T00:10:00.000Z",
    },
  }));
  assert.equal(tooEarly.kind, "rejected");
  assert.equal(coordinator.execute(command({
    request: "handoff-stopped",
    version: 4,
    command: { kind: "recordStopped", attemptId: "attempt-claim-1", operationId: prepared.operationId.value, receiptDigest: DIGEST_C },
  })).kind, "accepted");
  const wrongCapsule = coordinator.execute(command({
    request: "handoff-approve-wrong",
    version: 5,
    command: {
      kind: "approveHandoff",
      handoffId: "handoff-1",
      capsuleDigest: REVISION_B,
      approvedBy: "poom",
      approvedAt: "2026-10-30T00:00:00.000Z",
      expiresAt: "2026-10-30T00:10:00.000Z",
    },
  }));
  assert.equal(wrongCapsule.kind, "rejected");
  assert.equal(coordinator.execute(command({
    request: "handoff-approve",
    version: 5,
    command: {
      kind: "approveHandoff",
      handoffId: "handoff-1",
      capsuleDigest: DIGEST_C,
      approvedBy: "poom",
      approvedAt: "2026-10-30T00:00:00.000Z",
      expiresAt: "2026-10-30T00:10:00.000Z",
    },
  })).kind, "accepted");
  const activated = coordinator.execute(command({
    request: "handoff-activate",
    version: 6,
    command: { kind: "activateHandoff", handoffId: "handoff-1", destinationAttemptId: "attempt-destination", destinationWorkspaceId: "workspace-destination" },
  }));
  assert.equal(activated.kind, "accepted");
  const pending = coordinator.queryCard(new CardId("card-1"));
  assert.equal(pending?.handoffs[0]?.state.kind, "awaiting_ack");
  assert.equal(pending?.attempts.find((attempt) => attempt.attemptId.value === "attempt-destination")?.state.kind, "handoff_pending");
  const wrongRevision = coordinator.execute(command({
    request: "handoff-ack-wrong-revision",
    version: 7,
    command: { kind: "acknowledgeHandoff", handoffId: "handoff-1", destinationAttemptId: "attempt-destination", revision: REVISION_B, capsuleDigest: DIGEST_C },
  }));
  assert.equal(wrongRevision.kind, "rejected");
  const acknowledged = coordinator.execute(command({
    request: "handoff-ack",
    version: 7,
    command: { kind: "acknowledgeHandoff", handoffId: "handoff-1", destinationAttemptId: "attempt-destination", revision: REVISION_A, capsuleDigest: DIGEST_C },
  }));
  assert.equal(acknowledged.kind, "accepted");
  if (acknowledged.kind === "accepted") assert.notEqual(acknowledged.operationId, null);
  const snapshot = coordinator.queryCard(new CardId("card-1"));
  assert.equal(snapshot?.handoffs[0]?.state.kind, "active");
  assert.equal(snapshot?.attempts.find((attempt) => attempt.attemptId.value === "attempt-destination")?.state.kind, "starting");
  coordinator.close();
});

test("missing destination acknowledgement fences the handoff as unknown", () => {
  const clock = new Date("2026-10-30T00:00:00.000Z");
  const coordinator = new Coordinator({ databasePath: ":memory:", clock: () => clock });
  observe(coordinator);
  const claimed = claim(coordinator);
  if (claimed.kind !== "accepted" || claimed.operationId === null) return;
  coordinator.execute(command({ request: "unknown-start", version: 2, command: { kind: "recordProviderStarted", attemptId: "attempt-claim-1", operationId: claimed.operationId.value, sessionRef: "session-unknown" } }));
  const prepared = coordinator.execute(command({ request: "unknown-prepare", version: 3, command: { kind: "prepareHandoff", handoffId: "handoff-unknown", sourceAttemptId: "attempt-claim-1", destinationProviderId: "provider-ade", destinationRunnerId: "runner-remote", capsuleDigest: DIGEST_C } }));
  if (prepared.kind !== "accepted" || prepared.operationId === null) return;
  coordinator.execute(command({ request: "unknown-stop", version: 4, command: { kind: "recordStopped", attemptId: "attempt-claim-1", operationId: prepared.operationId.value, receiptDigest: DIGEST_C } }));
  coordinator.execute(command({ request: "unknown-approve", version: 5, command: { kind: "approveHandoff", handoffId: "handoff-unknown", capsuleDigest: DIGEST_C, approvedBy: "poom", approvedAt: "2026-10-30T00:00:00.000Z", expiresAt: "2026-10-30T00:10:00.000Z" } }));
  coordinator.execute(command({ request: "unknown-activate", version: 6, command: { kind: "activateHandoff", handoffId: "handoff-unknown", destinationAttemptId: "attempt-unknown", destinationWorkspaceId: "workspace-unknown" } }));
  const unknown = coordinator.execute(command({ request: "unknown-record", version: 7, command: { kind: "recordHandoffUnknown", handoffId: "handoff-unknown", reason: "destination acknowledgement timed out" } }));
  assert.equal(unknown.kind, "accepted");
  const snapshot = coordinator.queryCard(new CardId("card-1"));
  assert.equal(snapshot?.handoffs[0]?.state.kind, "handoff_unknown");
  assert.equal(snapshot?.attempts.find((attempt) => attempt.attemptId.value === "attempt-unknown")?.state.kind, "stop_unknown");
  assert.deepEqual(claim(coordinator, "unknown-replacement", 8), { kind: "rejected", code: "ownership_unresolved", message: "writer attempt-unknown still owns or may own the card" });
  coordinator.close();
});

test("a card revision pivot requests writer stop and rejects stale claims", () => {
  const coordinator = new Coordinator({ databasePath: ":memory:" });
  observe(coordinator);
  claim(coordinator);
  const pivot = coordinator.execute(command({
    request: "observe-pivot",
    version: 2,
    command: { kind: "observeCard", cardId: "card-1", revision: REVISION_B, observedAt: "2026-10-30T00:05:00.000Z" },
  }));
  assert.equal(pivot.kind, "accepted");
  const stale = claim(coordinator, "after-pivot", 3);
  assert.deepEqual(stale, { kind: "rejected", code: "revision_conflict", message: "claim uses a stale card revision" });
  coordinator.close();
});

test("completion requires independent passing evidence for the exact candidate", () => {
  const coordinator = new Coordinator({ databasePath: ":memory:" });
  observe(coordinator);
  const claimed = claim(coordinator);
  assert.equal(claimed.kind, "accepted");
  if (claimed.kind !== "accepted" || claimed.operationId === null) return;
  assert.equal(coordinator.execute(command({
    request: "complete-start",
    version: 2,
    command: { kind: "recordProviderStarted", attemptId: "attempt-claim-1", operationId: claimed.operationId.value, sessionRef: "session-complete" },
  })).kind, "accepted");
  const candidateA = "d".repeat(40);
  const candidateB = "e".repeat(40);
  const premature = coordinator.execute(command({
    request: "complete-premature",
    version: 3,
    command: { kind: "completeAttempt", attemptId: "attempt-claim-1", candidate: candidateA, requiredCriteria: ["auth journey"], summary: "done" },
  }));
  assert.equal(premature.kind, "rejected");
  const evidenceEnvelope = command({
    request: "evidence-independent",
    version: 3,
    command: { kind: "recordEvidence", evidenceId: "evidence-1", attemptId: "attempt-claim-1", candidate: candidateA, criterion: "auth journey", verifier: "checker-b", outcome: "passed", artifactIds: [] },
  });
  assert.equal(coordinator.execute({ ...evidenceEnvelope, principal: "checker-b" }).kind, "accepted");
  const wrongCandidate = coordinator.execute(command({
    request: "complete-wrong-candidate",
    version: 4,
    command: { kind: "completeAttempt", attemptId: "attempt-claim-1", candidate: candidateB, requiredCriteria: ["auth journey"], summary: "done" },
  }));
  assert.equal(wrongCandidate.kind, "rejected");
  const completed = coordinator.execute(command({
    request: "complete-exact",
    version: 4,
    command: { kind: "completeAttempt", attemptId: "attempt-claim-1", candidate: candidateA, requiredCriteria: ["auth journey"], summary: "authentication shipped" },
  }));
  assert.equal(completed.kind, "accepted");
  assert.equal(coordinator.queryCard(new CardId("card-1"))?.attempts[0]?.state.kind, "completed");
  coordinator.close();
});

test("heartbeat rejects stale fencing tokens", () => {
  const clock = new Date("2026-10-30T00:00:00.000Z");
  const coordinator = new Coordinator({ databasePath: ":memory:", clock: () => clock });
  observe(coordinator);
  claim(coordinator);
  const rejected = coordinator.execute(command({
    request: "heartbeat-stale",
    version: 2,
    command: { kind: "heartbeatAttempt", attemptId: "attempt-claim-1", fence: 999, leaseSeconds: 60 },
  }));
  assert.deepEqual(rejected, { kind: "rejected", code: "ownership_unresolved", message: "heartbeat carries a stale fencing token" });
  const renewed = coordinator.execute(command({
    request: "heartbeat-current",
    version: 2,
    command: { kind: "heartbeatAttempt", attemptId: "attempt-claim-1", fence: 1, leaseSeconds: 60 },
  }));
  assert.equal(renewed.kind, "accepted");
  assert.equal(coordinator.queryCard(new CardId("card-1"))?.attempts[0]?.leaseExpiresAt, "2026-10-30T00:01:00.000Z");
  coordinator.close();
});
