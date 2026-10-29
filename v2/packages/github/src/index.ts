import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { copyFile, mkdir, readFile, readdir, rename, stat, unlink, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { promisify } from "node:util";
import { parse as parseYaml, stringify as stringifyYaml } from "yaml";
import {
  CardContractWireSchema,
  CardRevision,
  fingerprintCard,
  parse,
  type CardContractWire,
} from "@super-speckit/protocol";

const executeFile = promisify(execFile);
const START = "<!-- super-speckit:contract:v1 -->";
const END = "<!-- /super-speckit:contract -->";

export const PROJECT_FIELDS = [
  "Type",
  "Phase",
  "Capability",
  "Parallel lane",
  "Harness",
  "Risk",
  "Evidence",
  "Contract revision",
  "Lease expiry",
] as const;

export type ParsedIssueContract = Readonly<{
  contract: CardContractWire;
  revision: CardRevision;
  bodyBefore: string;
  bodyAfter: string;
}>;

export function renderContractBlock(contract: CardContractWire): string {
  const yaml = stringifyYaml(contract, { lineWidth: 0 }).trimEnd();
  return `${START}\n\`\`\`yaml\n${yaml}\n\`\`\`\n${END}`;
}

export function upsertContractBlock(body: string, contract: CardContractWire): string {
  const block = renderContractBlock(contract);
  const start = body.indexOf(START);
  const end = body.indexOf(END);
  if (start < 0 && end < 0) return `${body.trimEnd()}\n\n${block}\n`;
  if (start < 0 || end < start) throw new Error("issue contains an incomplete Super-SpecKit contract block");
  return `${body.slice(0, start)}${block}${body.slice(end + END.length)}`;
}

export function parseContractBlock(body: string): ParsedIssueContract {
  const start = body.indexOf(START);
  const end = body.indexOf(END);
  if (start < 0 || end < start) throw new Error("issue does not contain one complete Super-SpecKit contract block");
  const block = body.slice(start + START.length, end).trim();
  const match = /^```yaml\n([\s\S]*)\n```$/.exec(block);
  if (match?.[1] === undefined) throw new Error("contract block must contain one YAML code block");
  const raw: unknown = parseYaml(match[1]);
  const contract = parse(CardContractWireSchema, raw);
  return { contract, revision: fingerprintCard(contract), bodyBefore: body.slice(0, start), bodyAfter: body.slice(end + END.length) };
}

export interface GitHubTransport {
  readIssue(repository: string, issueNumber: number): Promise<Readonly<{ nodeId: string; title: string; body: string; state: string }>>;
  updateIssueBody(repository: string, issueNumber: number, body: string): Promise<void>;
  graphql(query: string, variables: Readonly<Record<string, string | number | boolean>>): Promise<unknown>;
}

export type IssueBodySyncOperation = Readonly<{
  kind: "issue_body";
  operationKey: string;
  repository: string;
  issueNumber: number;
  expectedBodyDigest: string;
  body: string;
}>;

export type GitHubSyncPlan = Readonly<{
  schemaVersion: 1;
  operations: readonly IssueBodySyncOperation[];
}>;

type SyncJournalEntry =
  | Readonly<{ kind: "pending"; operationDigest: string }>
  | Readonly<{ kind: "applied"; operationDigest: string; observedBodyDigest: string }>;

type SyncJournal = Readonly<{
  schemaVersion: 1;
  planDigest: string;
  entries: Readonly<Record<string, SyncJournalEntry>>;
}>;

export type GitHubSyncResult = Readonly<{
  planDigest: string;
  applied: readonly string[];
  alreadyApplied: readonly string[];
}>;

export function parseGitHubSyncPlan(value: unknown): GitHubSyncPlan {
  const record = externalRecord(value, "GitHub sync plan");
  if (record["schemaVersion"] !== 1 || !Array.isArray(record["operations"])) throw new Error("invalid GitHub sync plan");
  const operations = record["operations"].map((item): IssueBodySyncOperation => {
    const operation = externalRecord(item, "GitHub sync operation");
    if (operation["kind"] !== "issue_body") throw new Error("unsupported GitHub sync operation");
    const issueNumber = operation["issueNumber"];
    if (typeof issueNumber !== "number" || !Number.isSafeInteger(issueNumber) || issueNumber < 1) throw new Error("invalid GitHub issue number");
    const body = operation["body"];
    if (typeof body !== "string") throw new Error("invalid GitHub issue body");
    return {
      kind: "issue_body",
      operationKey: requiredString(operation, "operationKey", "GitHub sync operation"),
      repository: requiredString(operation, "repository", "GitHub sync operation"),
      issueNumber,
      expectedBodyDigest: requiredString(operation, "expectedBodyDigest", "GitHub sync operation"),
      body,
    };
  });
  const plan = { schemaVersion: 1, operations } satisfies GitHubSyncPlan;
  validateSyncPlan(plan);
  return plan;
}

export async function applyGitHubSyncPlan(input: Readonly<{
  stateRoot: string;
  transport: GitHubTransport;
  plan: GitHubSyncPlan;
}>): Promise<GitHubSyncResult> {
  validateSyncPlan(input.plan);
  const planDigest = createHash("sha256").update(JSON.stringify(input.plan)).digest("hex");
  const journalPath = join(input.stateRoot, "github-sync", `${planDigest}.json`);
  let journal = await readSyncJournal(journalPath, planDigest);
  const applied: string[] = [];
  const alreadyApplied: string[] = [];

  for (const operation of input.plan.operations) {
    const operationDigest = digestIssueBodyOperation(operation);
    const prior = journal.entries[operation.operationKey];
    if (prior !== undefined && prior.operationDigest !== operationDigest) {
      throw new Error(`sync operation key was reused with different intent: ${operation.operationKey}`);
    }
    const issue = await input.transport.readIssue(operation.repository, operation.issueNumber);
    const currentDigest = digestText(issue.body);
    const desiredDigest = digestText(operation.body);
    if (currentDigest === desiredDigest) {
      journal = withJournalEntry(journal, operation.operationKey, { kind: "applied", operationDigest, observedBodyDigest: desiredDigest });
      await writeSyncJournal(journalPath, journal);
      alreadyApplied.push(operation.operationKey);
      continue;
    }
    if (currentDigest !== operation.expectedBodyDigest) {
      throw new Error(`GitHub issue changed since preview: ${operation.repository}#${operation.issueNumber}`);
    }
    journal = withJournalEntry(journal, operation.operationKey, { kind: "pending", operationDigest });
    await writeSyncJournal(journalPath, journal);
    await input.transport.updateIssueBody(operation.repository, operation.issueNumber, operation.body);
    const observed = await input.transport.readIssue(operation.repository, operation.issueNumber);
    const observedDigest = digestText(observed.body);
    if (observedDigest !== desiredDigest) {
      throw new Error(`GitHub did not confirm the requested issue body: ${operation.repository}#${operation.issueNumber}`);
    }
    journal = withJournalEntry(journal, operation.operationKey, { kind: "applied", operationDigest, observedBodyDigest: observedDigest });
    await writeSyncJournal(journalPath, journal);
    applied.push(operation.operationKey);
  }
  return { planDigest, applied, alreadyApplied };
}

export interface ContributorTransport {
  listBranches(repository: string): Promise<unknown>;
  listPullRequests(repository: string): Promise<unknown>;
}

export type OrdinaryContribution = Readonly<{
  pullRequestNumber: number;
  title: string;
  state: "open" | "closed" | "merged";
  url: string;
  headRef: string;
  headSha: string;
  baseRef: string;
  issueNumbers: readonly number[];
  checks: readonly Readonly<{ name: string; status: "queued" | "in_progress" | "completed"; conclusion: string | null; url: string | null }>[];
}>;

export type OrdinaryContributionPreview = Readonly<{
  repository: string;
  branches: readonly Readonly<{ name: string; sha: string }>[];
  contributions: readonly OrdinaryContribution[];
  sourceDigest: string;
  runtimeAdoptionRequired: false;
}>;

export async function previewOrdinaryContributions(input: Readonly<{
  repository: string;
  transport: ContributorTransport;
}>): Promise<OrdinaryContributionPreview> {
  const branches = parseBranches(await input.transport.listBranches(input.repository));
  const contributions = parsePullRequests(await input.transport.listPullRequests(input.repository));
  const normalized = {
    repository: input.repository,
    branches: [...branches].sort((left, right) => left.name.localeCompare(right.name)),
    contributions: [...contributions].sort((left, right) => left.pullRequestNumber - right.pullRequestNumber),
  };
  return {
    ...normalized,
    sourceDigest: createHash("sha256").update(JSON.stringify(normalized)).digest("hex"),
    runtimeAdoptionRequired: false,
  };
}

export class GhCliTransport implements GitHubTransport {
  async readIssue(repository: string, issueNumber: number): Promise<Readonly<{ nodeId: string; title: string; body: string; state: string }>> {
    const { stdout } = await executeFile("gh", ["issue", "view", String(issueNumber), "--repo", repository, "--json", "id,title,body,state"]);
    const raw: unknown = JSON.parse(stdout);
    if (raw === null || Array.isArray(raw) || typeof raw !== "object") throw new Error("gh issue output is not an object");
    const value = Object.fromEntries(Object.entries(raw));
    if (typeof value["id"] !== "string" || typeof value["title"] !== "string" || typeof value["body"] !== "string" || typeof value["state"] !== "string") {
      throw new Error("gh issue output is missing required fields");
    }
    return { nodeId: value["id"], title: value["title"], body: value["body"], state: value["state"] };
  }

  async updateIssueBody(repository: string, issueNumber: number, body: string): Promise<void> {
    await executeFile("gh", ["issue", "edit", String(issueNumber), "--repo", repository, "--body", body]);
  }

  async graphql(query: string, variables: Readonly<Record<string, string | number | boolean>>): Promise<unknown> {
    const args = ["api", "graphql", "-f", `query=${query}`];
    for (const [key, value] of Object.entries(variables)) args.push("-F", `${key}=${String(value)}`);
    const { stdout } = await executeFile("gh", args);
    const response: unknown = JSON.parse(stdout);
    return response;
  }

  async listBranches(repository: string): Promise<unknown> {
    const { stdout } = await executeFile("gh", ["api", `repos/${repository}/branches`, "--paginate"]);
    const raw: unknown = JSON.parse(stdout);
    if (!Array.isArray(raw)) throw new Error("gh branches output is not an array");
    return raw.map((item) => {
      const branch = externalRecord(item, "gh branch");
      const commit = externalRecord(branch["commit"], "gh branch commit");
      return { name: requiredString(branch, "name", "gh branch"), sha: requiredString(commit, "sha", "gh branch commit") };
    });
  }

  async listPullRequests(repository: string): Promise<unknown> {
    const fields = "number,title,state,url,headRefName,headRefOid,baseRefName,closingIssuesReferences,statusCheckRollup";
    const { stdout } = await executeFile("gh", ["pr", "list", "--repo", repository, "--state", "all", "--limit", "1000", "--json", fields]);
    const raw: unknown = JSON.parse(stdout);
    if (!Array.isArray(raw)) throw new Error("gh pull request output is not an array");
    return raw.map(normalizeGhPullRequest);
  }
}

export type AdoptionEntry = Readonly<{ path: string; digest: string; bytes: number }>;
export type AdoptionPreview = Readonly<{ repository: string; sourceDigest: string; entries: readonly AdoptionEntry[]; warnings: readonly string[] }>;
export type AdoptionResult = Readonly<{ status: "adopted" | "already-adopted"; sourceDigest: string; entryCount: number; v1HistoryChanged: false }>;

export async function previewV1Adoption(repository: string): Promise<AdoptionPreview> {
  const roots = [".super-speckit", "super-speckit.yml", "AGENTS.md"];
  const entries: AdoptionEntry[] = [];
  for (const root of roots) await collect(repository, root, entries);
  entries.sort((left, right) => left.path.localeCompare(right.path));
  const sourceDigest = createHash("sha256").update(entries.map((entry) => `${entry.path}:${entry.digest}:${entry.bytes}`).join("\n")).digest("hex");
  const warnings = entries.some((entry) => entry.path === ".super-speckit/state/work-state.yml")
    ? ["V1 history will remain immutable. V2 owns only transitions created after adoption."]
    : ["No V1 work-state projection was found."];
  return { repository, sourceDigest, entries, warnings };
}

export async function applyV1Adoption(input: Readonly<{ repository: string; stateRoot: string; expectedDigest: string; now?: Date }>): Promise<AdoptionResult> {
  const preview = await previewV1Adoption(input.repository);
  if (preview.sourceDigest !== input.expectedDigest) throw new Error(`adoption source changed: expected ${input.expectedDigest}, observed ${preview.sourceDigest}`);
  const externalRoot = join(input.stateRoot, "adoptions", preview.sourceDigest);
  const externalManifest = join(externalRoot, "manifest.json");
  const repositoryManifest = join(input.repository, ".super-speckit", "v2", "adoption.json");
  try {
    const prior = parseAdoptionManifest(await readFile(repositoryManifest, "utf8"));
    if (prior.sourceDigest !== preview.sourceDigest) throw new Error("repository already contains a different V2 adoption");
    await verifyAdoptionBackup(externalRoot, prior.entries);
    return { status: "already-adopted", sourceDigest: preview.sourceDigest, entryCount: prior.entries.length, v1HistoryChanged: false };
  } catch (error) {
    if (!isMissing(error)) throw error;
  }
  for (const entry of preview.entries) {
    const destination = join(externalRoot, "snapshot", entry.path);
    await mkdir(dirname(destination), { recursive: true, mode: 0o700 });
    await copyFile(join(input.repository, entry.path), destination);
  }
  const manifest = { schemaVersion: 1, adoptedAt: (input.now ?? new Date()).toISOString(), sourceDigest: preview.sourceDigest, entries: preview.entries, v1HistoryImmutable: true };
  await mkdir(externalRoot, { recursive: true, mode: 0o700 });
  await writeFile(externalManifest, `${JSON.stringify(manifest, null, 2)}\n`, { mode: 0o600, flag: "wx" });
  await verifyAdoptionBackup(externalRoot, preview.entries);
  await mkdir(dirname(repositoryManifest), { recursive: true });
  await writeFile(repositoryManifest, `${JSON.stringify(manifest, null, 2)}\n`, { flag: "wx" });
  return { status: "adopted", sourceDigest: preview.sourceDigest, entryCount: preview.entries.length, v1HistoryChanged: false };
}

export async function rollbackV1Adoption(input: Readonly<{ repository: string; stateRoot: string; expectedDigest: string }>): Promise<Readonly<{ status: "rolled-back"; sourceDigest: string; backupRetained: true }>> {
  const repositoryManifest = join(input.repository, ".super-speckit", "v2", "adoption.json");
  const manifest = parseAdoptionManifest(await readFile(repositoryManifest, "utf8"));
  if (manifest.sourceDigest !== input.expectedDigest) throw new Error("rollback digest does not match the active adoption");
  await verifyAdoptionBackup(join(input.stateRoot, "adoptions", manifest.sourceDigest), manifest.entries);
  await unlink(repositoryManifest);
  return { status: "rolled-back", sourceDigest: manifest.sourceDigest, backupRetained: true };
}

async function collect(repository: string, relative: string, entries: AdoptionEntry[]): Promise<void> {
  if (relative === ".super-speckit/v2" || relative.startsWith(".super-speckit/v2/")) return;
  const absolute = `${repository}/${relative}`;
  let metadata;
  try {
    metadata = await stat(absolute);
  } catch (error) {
    if (isMissing(error)) return;
    throw error;
  }
  if (metadata.isDirectory()) {
    for (const child of await readdir(absolute)) await collect(repository, `${relative}/${child}`, entries);
    return;
  }
  if (!metadata.isFile()) return;
  const bytes = await readFile(absolute);
  entries.push({ path: relative, digest: createHash("sha256").update(bytes).digest("hex"), bytes: bytes.byteLength });
}

function isMissing(error: unknown): boolean {
  return error instanceof Error && "code" in error && error.code === "ENOENT";
}

async function verifyAdoptionBackup(externalRoot: string, entries: readonly AdoptionEntry[]): Promise<void> {
  for (const entry of entries) {
    const bytes = await readFile(join(externalRoot, "snapshot", entry.path));
    const digest = createHash("sha256").update(bytes).digest("hex");
    if (digest !== entry.digest || bytes.byteLength !== entry.bytes) throw new Error(`adoption backup digest mismatch: ${entry.path}`);
  }
}

function parseAdoptionManifest(raw: string): Readonly<{ sourceDigest: string; entries: readonly AdoptionEntry[] }> {
  const value: unknown = JSON.parse(raw);
  if (value === null || Array.isArray(value) || typeof value !== "object") throw new Error("adoption manifest is not an object");
  const record = Object.fromEntries(Object.entries(value));
  if (typeof record["sourceDigest"] !== "string" || !Array.isArray(record["entries"])) throw new Error("adoption manifest is incomplete");
  const entries = record["entries"].map((item): AdoptionEntry => {
    if (item === null || Array.isArray(item) || typeof item !== "object") throw new Error("adoption manifest entry is invalid");
    const entry = Object.fromEntries(Object.entries(item));
    if (typeof entry["path"] !== "string" || typeof entry["digest"] !== "string" || typeof entry["bytes"] !== "number") throw new Error("adoption manifest entry is incomplete");
    return { path: entry["path"], digest: entry["digest"], bytes: entry["bytes"] };
  });
  return { sourceDigest: record["sourceDigest"], entries };
}

function validateSyncPlan(plan: GitHubSyncPlan): void {
  if (plan.schemaVersion !== 1 || !Array.isArray(plan.operations)) throw new Error("invalid GitHub sync plan");
  const keys = new Set<string>();
  for (const operation of plan.operations) {
    if (operation.kind !== "issue_body" || operation.operationKey.length === 0 || operation.repository.length === 0) throw new Error("invalid GitHub sync operation");
    if (!Number.isSafeInteger(operation.issueNumber) || operation.issueNumber < 1) throw new Error("invalid GitHub issue number");
    if (!/^[0-9a-f]{64}$/.test(operation.expectedBodyDigest)) throw new Error("invalid expected GitHub body digest");
    if (keys.has(operation.operationKey)) throw new Error(`duplicate sync operation key: ${operation.operationKey}`);
    keys.add(operation.operationKey);
  }
}

function digestText(value: string): string {
  return createHash("sha256").update(value).digest("hex");
}

function digestIssueBodyOperation(operation: IssueBodySyncOperation): string {
  return createHash("sha256").update(JSON.stringify(operation)).digest("hex");
}

async function readSyncJournal(path: string, planDigest: string): Promise<SyncJournal> {
  try {
    const raw: unknown = JSON.parse(await readFile(path, "utf8"));
    if (raw === null || Array.isArray(raw) || typeof raw !== "object") throw new Error("GitHub sync journal is not an object");
    const record = Object.fromEntries(Object.entries(raw));
    if (record["schemaVersion"] !== 1 || record["planDigest"] !== planDigest) throw new Error("GitHub sync journal does not match the plan");
    if (record["entries"] === null || Array.isArray(record["entries"]) || typeof record["entries"] !== "object") throw new Error("GitHub sync journal entries are invalid");
    const entries: Record<string, SyncJournalEntry> = {};
    for (const [key, item] of Object.entries(record["entries"])) entries[key] = parseSyncJournalEntry(item);
    return { schemaVersion: 1, planDigest, entries };
  } catch (error) {
    if (isMissing(error)) return { schemaVersion: 1, planDigest, entries: {} };
    throw error;
  }
}

function parseSyncJournalEntry(value: unknown): SyncJournalEntry {
  if (value === null || Array.isArray(value) || typeof value !== "object") throw new Error("GitHub sync journal entry is invalid");
  const record = Object.fromEntries(Object.entries(value));
  if (record["kind"] === "pending" && typeof record["operationDigest"] === "string") {
    return { kind: "pending", operationDigest: record["operationDigest"] };
  }
  if (record["kind"] === "applied" && typeof record["operationDigest"] === "string" && typeof record["observedBodyDigest"] === "string") {
    return { kind: "applied", operationDigest: record["operationDigest"], observedBodyDigest: record["observedBodyDigest"] };
  }
  throw new Error("GitHub sync journal entry is incomplete");
}

function withJournalEntry(journal: SyncJournal, key: string, entry: SyncJournalEntry): SyncJournal {
  return { ...journal, entries: { ...journal.entries, [key]: entry } };
}

async function writeSyncJournal(path: string, journal: SyncJournal): Promise<void> {
  await mkdir(dirname(path), { recursive: true, mode: 0o700 });
  const temporary = `${path}.${process.pid}.tmp`;
  await writeFile(temporary, `${JSON.stringify(journal, null, 2)}\n`, { mode: 0o600 });
  await rename(temporary, path);
}

function parseBranches(value: unknown): readonly Readonly<{ name: string; sha: string }>[] {
  if (!Array.isArray(value)) throw new Error("GitHub branches response is not an array");
  return value.map((item) => {
    const record = externalRecord(item, "GitHub branch");
    const name = requiredString(record, "name", "GitHub branch");
    const sha = requiredString(record, "sha", "GitHub branch");
    if (!/^[0-9a-f]{40,64}$/.test(sha)) throw new Error("GitHub branch SHA is invalid");
    return { name, sha };
  });
}

function normalizeGhPullRequest(value: unknown): OrdinaryContribution {
  const record = externalRecord(value, "gh pull request");
  const number = record["number"];
  if (typeof number !== "number" || !Number.isSafeInteger(number) || number < 1) throw new Error("gh pull request number is invalid");
  const rawState = requiredString(record, "state", "gh pull request").toLowerCase();
  if (rawState !== "open" && rawState !== "closed" && rawState !== "merged") throw new Error("gh pull request state is invalid");
  const rawIssues = record["closingIssuesReferences"];
  const rawChecks = record["statusCheckRollup"];
  if (!Array.isArray(rawIssues) || !Array.isArray(rawChecks)) throw new Error("gh pull request relationships are invalid");
  return {
    pullRequestNumber: number,
    title: requiredString(record, "title", "gh pull request"),
    state: rawState,
    url: requiredString(record, "url", "gh pull request"),
    headRef: requiredString(record, "headRefName", "gh pull request"),
    headSha: requiredString(record, "headRefOid", "gh pull request"),
    baseRef: requiredString(record, "baseRefName", "gh pull request"),
    issueNumbers: rawIssues.map((issue) => {
      const issueRecord = externalRecord(issue, "gh closing issue");
      const issueNumber = issueRecord["number"];
      if (typeof issueNumber !== "number" || !Number.isSafeInteger(issueNumber) || issueNumber < 1) throw new Error("gh closing issue number is invalid");
      return issueNumber;
    }),
    checks: rawChecks.map(normalizeGhCheck),
  };
}

function normalizeGhCheck(value: unknown): OrdinaryContribution["checks"][number] {
  const record = externalRecord(value, "gh check");
  const name = optionalString(record, "name") ?? optionalString(record, "context") ?? "unnamed-check";
  const rawStatus = (optionalString(record, "status") ?? optionalString(record, "state") ?? "completed").toLowerCase();
  const status = rawStatus === "queued" || rawStatus === "pending"
    ? "queued"
    : rawStatus === "in_progress"
      ? "in_progress"
      : "completed";
  const rawConclusion = optionalString(record, "conclusion") ?? optionalString(record, "state");
  return {
    name,
    status,
    conclusion: status === "completed" && rawConclusion !== undefined ? rawConclusion.toLowerCase() : null,
    url: optionalString(record, "detailsUrl") ?? optionalString(record, "targetUrl") ?? null,
  };
}

function parsePullRequests(value: unknown): readonly OrdinaryContribution[] {
  if (!Array.isArray(value)) throw new Error("GitHub pull request response is not an array");
  return value.map((item) => {
    const record = externalRecord(item, "GitHub pull request");
    const number = record["number"];
    if (typeof number !== "number" || !Number.isSafeInteger(number) || number < 1) throw new Error("GitHub pull request number is invalid");
    const state = record["state"];
    if (state !== "open" && state !== "closed" && state !== "merged") throw new Error("GitHub pull request state is invalid");
    const issueNumbers = record["issueNumbers"];
    if (!Array.isArray(issueNumbers) || !issueNumbers.every((issue) => typeof issue === "number" && Number.isSafeInteger(issue) && issue > 0)) throw new Error("GitHub pull request issue links are invalid");
    const checks = record["checks"];
    if (!Array.isArray(checks)) throw new Error("GitHub pull request checks are invalid");
    return {
      pullRequestNumber: number,
      title: requiredString(record, "title", "GitHub pull request"),
      state,
      url: requiredString(record, "url", "GitHub pull request"),
      headRef: requiredString(record, "headRef", "GitHub pull request"),
      headSha: requiredString(record, "headSha", "GitHub pull request"),
      baseRef: requiredString(record, "baseRef", "GitHub pull request"),
      issueNumbers,
      checks: checks.map(parseCheck),
    };
  });
}

function parseCheck(value: unknown): Readonly<{ name: string; status: "queued" | "in_progress" | "completed"; conclusion: string | null; url: string | null }> {
  const record = externalRecord(value, "GitHub check");
  const status = record["status"];
  if (status !== "queued" && status !== "in_progress" && status !== "completed") throw new Error("GitHub check status is invalid");
  const conclusion = record["conclusion"];
  const url = record["url"];
  if (conclusion !== null && typeof conclusion !== "string") throw new Error("GitHub check conclusion is invalid");
  if (url !== null && typeof url !== "string") throw new Error("GitHub check URL is invalid");
  return { name: requiredString(record, "name", "GitHub check"), status, conclusion, url };
}

function externalRecord(value: unknown, name: string): Readonly<Record<string, unknown>> {
  if (value === null || Array.isArray(value) || typeof value !== "object") throw new Error(`${name} is not an object`);
  return Object.fromEntries(Object.entries(value));
}

function requiredString(record: Readonly<Record<string, unknown>>, key: string, name: string): string {
  const value = record[key];
  if (typeof value !== "string" || value.length === 0) throw new Error(`${name} ${key} is invalid`);
  return value;
}

function optionalString(record: Readonly<Record<string, unknown>>, key: string): string | undefined {
  const value = record[key];
  return typeof value === "string" && value.length > 0 ? value : undefined;
}

export function agentsGuidance(): string {
  return `## Super-SpecKit project context\n\nRead \`.super-speckit/portfolio/\` for the GitHub card projection and \`.super-speckit/evidence/\` for redacted evidence descriptors. Treat GitHub as canonical for card scope, status, dependencies, and pivots. Treat repository ADRs, code, and tests as canonical technical truth. Do not edit generated projections or copy credentials, raw logs, recordings, or customer data into \`.super-speckit/\`. Use ordinary branches, pull requests, and CI when the V2 runtime is unavailable; the runtime can import that work later.\n`;
}
