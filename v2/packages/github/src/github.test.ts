import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";
import { mkdir, mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { CardContractWireSchema, parse } from "@super-speckit/protocol";
import {
  applyGitHubSyncPlan,
  applyV1Adoption,
  parseContractBlock,
  previewOrdinaryContributions,
  previewV1Adoption,
  renderContractBlock,
  rollbackV1Adoption,
  upsertContractBlock,
  type GitHubSyncPlan,
  type GitHubTransport,
} from "./index.ts";

const contract = parse(CardContractWireSchema, {
  schemaVersion: 1,
  repository: "Poom5741/super-speckit",
  issueNodeId: "I_1",
  issueNumber: 1,
  title: "Foundation",
  kind: "foundation",
  outcome: "A tested runtime authority exists.",
  nonGoals: [],
  acceptance: ["A stale writer is rejected."],
  dependencies: [],
  baseRef: "main",
  capability: "runtime",
  risk: "high",
});

test("the managed issue block round-trips without changing surrounding prose", () => {
  const body = upsertContractBlock("Human context stays here.", contract);
  const parsed = parseContractBlock(body);
  assert.equal(parsed.contract.title, "Foundation");
  assert.equal(parsed.bodyBefore.trim(), "Human context stays here.");
  assert.equal(parsed.revision.value.length, 64);
  assert.equal(renderContractBlock(parsed.contract), renderContractBlock(contract));
});

test("an incomplete managed issue block is rejected", () => {
  assert.throws(() => upsertContractBlock("<!-- super-speckit:contract:v1 -->", contract));
});

test("V1 adoption is previewed, backed up, repeatable, and reversible", async () => {
  const directory = await mkdtemp(join(tmpdir(), "ssk-adoption-"));
  const repository = join(directory, "repo");
  const stateRoot = join(directory, "state");
  await writeFile(join(directory, "placeholder"), "unused");
  await mkdir(join(repository, ".super-speckit", "state"), { recursive: true });
  await writeFile(join(repository, ".super-speckit", "state", "work-state.yml"), "schema: v1\n");
  const preview = await previewV1Adoption(repository);
  const applied = await applyV1Adoption({ repository, stateRoot, expectedDigest: preview.sourceDigest, now: new Date("2026-10-30T00:00:00.000Z") });
  assert.equal(applied.status, "adopted");
  assert.equal((await applyV1Adoption({ repository, stateRoot, expectedDigest: preview.sourceDigest })).status, "already-adopted");
  assert.equal(await readFile(join(repository, ".super-speckit", "state", "work-state.yml"), "utf8"), "schema: v1\n");
  const rolledBack = await rollbackV1Adoption({ repository, stateRoot, expectedDigest: preview.sourceDigest });
  assert.equal(rolledBack.backupRetained, true);
  await assert.rejects(readFile(join(repository, ".super-speckit", "v2", "adoption.json"), "utf8"), /ENOENT/);
});

test("GitHub synchronization journals intent and is idempotent after a retry", async () => {
  const directory = await mkdtemp(join(tmpdir(), "ssk-github-sync-"));
  let body = "Human-owned issue context.\n";
  let updates = 0;
  const transport: GitHubTransport = {
    async readIssue() { return { nodeId: "I_1", title: "Foundation", body, state: "OPEN" }; },
    async updateIssueBody(_repository, _issueNumber, nextBody) { updates += 1; body = nextBody; },
    async graphql() { return {}; },
  };
  const desired = upsertContractBlock(body, contract);
  const plan = {
    schemaVersion: 1,
    operations: [{
      kind: "issue_body",
      operationKey: "issue:Poom5741/super-speckit#1:contract:v1",
      repository: "Poom5741/super-speckit",
      issueNumber: 1,
      expectedBodyDigest: createHash("sha256").update(body).digest("hex"),
      body: desired,
    }],
  } satisfies GitHubSyncPlan;
  const first = await applyGitHubSyncPlan({ stateRoot: directory, transport, plan });
  const second = await applyGitHubSyncPlan({ stateRoot: directory, transport, plan });
  assert.deepEqual(first.applied, ["issue:Poom5741/super-speckit#1:contract:v1"]);
  assert.deepEqual(second.alreadyApplied, ["issue:Poom5741/super-speckit#1:contract:v1"]);
  assert.equal(updates, 1);
});

test("ordinary branches, pull requests, and CI import without runtime adoption", async () => {
  const sha = "a".repeat(40);
  const preview = await previewOrdinaryContributions({
    repository: "Poom5741/super-speckit",
    transport: {
      async listBranches() { return [{ name: "feature/auth", sha }]; },
      async listPullRequests() {
        return [{
          number: 42,
          title: "Add authentication",
          state: "open",
          url: "https://github.com/Poom5741/super-speckit/pull/42",
          headRef: "feature/auth",
          headSha: sha,
          baseRef: "main",
          issueNumbers: [7],
          checks: [{ name: "test", status: "completed", conclusion: "success", url: null }],
        }];
      },
    },
  });
  assert.equal(preview.runtimeAdoptionRequired, false);
  assert.equal(preview.contributions[0]?.checks[0]?.conclusion, "success");
  assert.equal(preview.sourceDigest.length, 64);
});
