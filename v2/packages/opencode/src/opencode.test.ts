import assert from "node:assert/strict";
import test from "node:test";
import { OPENCODE_TARGET_COMMIT } from "@super-speckit/protocol";
import { probeOpenCodeCompatibility } from "./rpc.ts";

test("OpenCode compatibility fails into an explicit degraded mode", () => {
  const verified = probeOpenCodeCompatibility("2.2.2");
  assert.equal(verified.status, "verified");
  assert.equal(verified.targetCommit, OPENCODE_TARGET_COMMIT);
  const unknown = probeOpenCodeCompatibility("2.3.0");
  assert.equal(unknown.status, "degraded");
  assert.match(unknown.limitations[0] ?? "", /writer controls are disabled/);
});
