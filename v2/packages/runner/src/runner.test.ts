import assert from "node:assert/strict";
import test from "node:test";
import { AttemptId, OperationId, WorkspaceId } from "@super-speckit/protocol";
import { NativeRunner, WslPersistentRunner, type RunnerBridge } from "./index.ts";

test("the native runner streams a command without a shell", async () => {
  const runner = new NativeRunner("test-runner");
  const events = [];
  for await (const event of runner.execute({
    operationId: new OperationId("operation-run"),
    attemptId: new AttemptId("attempt-run"),
    workspaceId: new WorkspaceId("workspace-run"),
    fence: 1,
    executable: process.execPath,
    arguments: ["-e", "process.stdout.write('hello')"],
    workingDirectory: process.cwd(),
    environment: {},
  })) events.push(event);
  const output = Buffer.concat(events.filter((event) => event.kind === "stdout").map((event) => Buffer.from(event.bytes))).toString("utf8");
  assert.equal(output, "hello");
  assert.equal(events.at(-1)?.kind, "exited");
});

test("quiesce refuses an operation without an ownership receipt", async () => {
  const runner = new NativeRunner("test-runner");
  const result = await runner.quiesce({ operationId: new OperationId("missing"), receiptId: "wrong", fence: 1 });
  assert.deepEqual(result, { kind: "unknown", reason: "runner has no matching owned process" });
});

test("WSL uses one persistent typed bridge instead of per-command wsl.exe calls", async () => {
  const payloads: Readonly<Record<string, unknown>>[] = [];
  let closed = false;
  const bridge: RunnerBridge = {
    async request(payload) { payloads.push(payload); return { kind: "accepted" }; },
    close() { closed = true; },
  };
  const runner = new WslPersistentRunner({ distribution: "Ubuntu", bridge });
  await runner.probe();
  await runner.execute({
    operationId: new OperationId("operation-wsl"), attemptId: new AttemptId("attempt-wsl"), workspaceId: new WorkspaceId("workspace-wsl"),
    fence: 4, executable: "/usr/bin/node", arguments: ["--version"], workingDirectory: "/home/ssk/worktree", environment: {},
  });
  assert.deepEqual(payloads.map((payload) => payload["kind"]), ["probe", "execute"]);
  assert.equal(payloads[1]?.["protocolVersion"], 1);
  runner.close();
  assert.equal(closed, true);
});
