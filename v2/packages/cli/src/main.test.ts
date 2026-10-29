import assert from "node:assert/strict";
import test from "node:test";
import { mkdtemp, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { buildProgram } from "./main.ts";

test("the CLI exposes the complete public alpha command families", () => {
  const program = buildProgram(() => undefined);
  const names = program.commands.map((command) => command.name());
  assert.deepEqual(names, ["init", "doctor", "daemon", "portfolio", "grill", "cards", "card", "evidence", "release"]);
  assert.deepEqual(program.commands.find((command) => command.name() === "card")?.commands.map((command) => command.name()), ["claim", "checkpoint", "ack-revision", "cancel", "handoff", "complete"]);
});

test("portfolio sync previews a reviewed plan without mutating GitHub", async () => {
  const directory = await mkdtemp(join(tmpdir(), "ssk-cli-sync-"));
  const path = join(directory, "plan.json");
  await writeFile(path, JSON.stringify({
    schemaVersion: 1,
    operations: [{
      kind: "issue_body",
      operationKey: "issue:owner/repo#1:contract:v1",
      repository: "owner/repo",
      issueNumber: 1,
      expectedBodyDigest: "a".repeat(64),
      body: "reviewed body",
    }],
  }));
  const output: unknown[] = [];
  await buildProgram((value) => output.push(value)).parseAsync(["node", "ssk2", "portfolio", "sync", "--plan", path]);
  assert.deepEqual(output, [{
    status: "preview",
    plan: path,
    operations: [{ operationKey: "issue:owner/repo#1:contract:v1", kind: "issue_body", repository: "owner/repo", issueNumber: 1 }],
    mutationPerformed: false,
  }]);
});
