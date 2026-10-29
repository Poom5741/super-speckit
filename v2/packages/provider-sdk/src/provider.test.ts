import assert from "node:assert/strict";
import test from "node:test";
import { AttemptId, OperationId, WorkspaceId } from "@super-speckit/protocol";
import { FakeProvider, applyProviderOperation, scoreProvider } from "./index.ts";

test("provider operations reuse the first observation for one operation ID", async () => {
  const provider = new FakeProvider();
  const operation = { kind: "start", operationId: new OperationId("operation-1"), attemptId: new AttemptId("attempt-1"), workspaceId: new WorkspaceId("workspace-1") } as const;
  const first = await applyProviderOperation(provider, operation);
  const second = await applyProviderOperation(provider, operation);
  assert.deepEqual(second, first);
  assert.deepEqual(first, { kind: "completed", operationId: operation.operationId, result: { operation: "start" } });
});

test("coordinator policy rejects a provider missing a required capability", async () => {
  const report = await new FakeProvider().probeCapabilities();
  const score = scoreProvider(report, [{ name: "desktop-control", required: true, weight: 10 }]);
  assert.deepEqual(score, { providerId: report.providerId, eligible: false, score: 0, reasons: ["desktop-control is unavailable"] });
});
