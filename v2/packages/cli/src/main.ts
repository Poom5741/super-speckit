#!/usr/bin/env node
import { randomBytes, randomUUID } from "node:crypto";
import { access, chmod, mkdir, readFile, writeFile } from "node:fs/promises";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { Command } from "commander";
import { generateFoundationCards, generateV2AlphaCardGraph, type FoundationInput } from "@super-speckit/architecture";
import { SocketCoordinatorClient } from "@super-speckit/client";
import { Coordinator } from "@super-speckit/coordinator";
import { CoordinatorDaemon } from "@super-speckit/daemon";
import { GhCliTransport, agentsGuidance, applyGitHubSyncPlan, applyV1Adoption, parseGitHubSyncPlan, previewV1Adoption, rollbackV1Adoption } from "@super-speckit/github";
import { CardId, OPENCODE_TARGET_COMMIT, fingerprintCard, type CommandReceipt } from "@super-speckit/protocol";

type Output = (value: unknown) => void;
type RuntimePaths = Readonly<{ root: string; database: string; socket: string; token: string; install: string }>;

export function buildProgram(output: Output = print): Command {
  const program = new Command().name("ssk2").description("Super-SpecKit V2 alpha runtime").version("0.1.0-alpha.0");

  program.command("init")
    .description("initialize repository-safe V2 projections")
    .option("--repo <path>", "repository", process.cwd())
    .action(async ({ repo }: { repo: string }) => output(await initializeRepository(resolve(repo))));

  program.command("doctor")
    .description("report runtime and integration readiness without changing the project")
    .option("--opencode-commit <sha>")
    .action(async ({ opencodeCommit }: { opencodeCommit?: string }) => output(await doctor(opencodeCommit)));

  const daemon = program.command("daemon").description("manage the owned coordinator daemon");
  daemon.command("install").action(async () => output(await installDaemon()));
  daemon.command("start").description("run the coordinator in the foreground for supervision").action(async () => startDaemon(output));
  daemon.command("status").action(async () => output(await daemonStatus()));

  const portfolio = program.command("portfolio").description("preview and reconcile GitHub-authoritative portfolio state");
  portfolio.command("preview").option("--repo <path>", "repository", process.cwd()).action(async ({ repo }: { repo: string }) => output(await previewV1Adoption(resolve(repo))));
  portfolio.command("adopt").requiredOption("--source-digest <digest>").option("--repo <path>", "repository", process.cwd())
    .action(async ({ repo, sourceDigest }: { repo: string; sourceDigest: string }) => output(await adoptPreview(resolve(repo), sourceDigest)));
  portfolio.command("rollback").requiredOption("--source-digest <digest>").option("--repo <path>", "repository", process.cwd())
    .action(async ({ repo, sourceDigest }: { repo: string; sourceDigest: string }) => output(await rollbackV1Adoption({ repository: resolve(repo), stateRoot: runtimePaths().root, expectedDigest: sourceDigest })));
  portfolio.command("sync").requiredOption("--plan <path>", "reviewed sync plan JSON").option("--apply", "apply the reviewed plan")
    .action(async ({ plan, apply }: { plan: string; apply?: boolean }) => output(await syncPortfolio(resolve(plan), apply === true)));

  program.command("grill").description("create an architecture question ledger for owner discussion")
    .option("--repo <path>", "repository", process.cwd())
    .action(async ({ repo }: { repo: string }) => output(await createQuestionLedger(resolve(repo))));

  const cards = program.command("cards").description("preview or publish Foundation cards");
  cards.command("preview").requiredOption("--repository <owner/name>").option("--base-ref <ref>", "base ref", "main")
    .option("--domain <domain>", "web-service, web-application, or cli", "web-application")
    .option("--alpha-graph", "render the complete 17 Foundation and 10 Feature graph")
    .action(({ repository, baseRef, domain, alphaGraph }: { repository: string; baseRef: string; domain: FoundationInput["domain"]; alphaGraph?: boolean }) => {
      if (alphaGraph === true) {
        const graph = generateV2AlphaCardGraph(repository, baseRef);
        output({ foundation: graph.foundation.map(withRevision), features: graph.features.map(withRevision) });
        return;
      }
      output(generateFoundationCards({ repository, baseRef, domain, decisions: [] }).map(withRevision));
    });
  cards.command("publish").action(() => output({ status: "blocked", reason: "Run cards preview and configure a GitHub Project before publication; alpha never guesses a mutation target." }));

  const card = program.command("card").description("operate one durable card attempt");
  card.command("claim").requiredOption("--card <id>").requiredOption("--revision <sha256>").requiredOption("--version <number>")
    .requiredOption("--workspace <id>").requiredOption("--provider <id>").requiredOption("--runner <id>")
    .option("--principal <name>", "principal", "local-user").option("--lease <seconds>", "lease", "3600")
    .action(async (options: Record<string, string>) => output(await executeRuntime(Number(options["version"]), options["principal"] ?? "local-user", {
      kind: "claimCard", card: { cardId: options["card"], revision: options["revision"] }, attemptId: randomUUID(), workspaceId: options["workspace"],
      providerId: options["provider"], runnerId: options["runner"], leaseSeconds: Number(options["lease"]), budget: { wallTimeSeconds: Number(options["lease"]), paidUsdCents: 0 },
    })));
  card.command("checkpoint").requiredOption("--attempt <id>").requiredOption("--version <number>").requiredOption("--next <action>")
    .option("--completed <criteria...>").option("--principal <name>", "principal", "local-user")
    .action(async (options: Record<string, string | string[]>) => output(await executeRuntime(Number(options["version"]), String(options["principal"]), {
      kind: "saveCheckpoint", attemptId: options["attempt"], dirtyDigest: null, completedCriteria: options["completed"] ?? [], nextAction: options["next"],
    })));
  card.command("ack-revision").requiredOption("--card <id>").requiredOption("--revision <sha256>").requiredOption("--version <number>")
    .option("--principal <name>", "principal", "local-user")
    .action(async (options: Record<string, string>) => output(await executeRuntime(Number(options["version"]), String(options["principal"]), { kind: "observeCard", cardId: options["card"], revision: options["revision"], observedAt: new Date().toISOString() })));
  card.command("cancel").requiredOption("--attempt <id>").requiredOption("--version <number>").requiredOption("--reason <reason>")
    .option("--principal <name>", "principal", "local-user")
    .action(async (options: Record<string, string>) => output(await executeRuntime(Number(options["version"]), String(options["principal"]), { kind: "requestCancellation", attemptId: options["attempt"], operationId: randomUUID(), reason: options["reason"] })));
  card.command("handoff").requiredOption("--phase <phase>", "prepare, approve, activate, ack, or unknown").requiredOption("--version <number>")
    .option("--handoff <id>").option("--attempt <id>").option("--provider <id>").option("--runner <id>").option("--capsule <sha256>")
    .option("--destination-attempt <id>").option("--workspace <id>").option("--revision <sha256>").option("--reason <reason>")
    .option("--approved-by <name>").option("--expires-at <instant>").option("--principal <name>", "principal", "local-user")
    .action(async (options: Record<string, string>) => output(await executeRuntime(Number(options["version"]), String(options["principal"]), handoffCommand(options))));
  card.command("complete").requiredOption("--attempt <id>").requiredOption("--version <number>").requiredOption("--candidate <commit>")
    .requiredOption("--criterion <criteria...>").requiredOption("--summary <summary>").option("--principal <name>", "principal", "local-user")
    .action(async (options: Record<string, string | string[]>) => output(await executeRuntime(Number(options["version"]), String(options["principal"]), {
      kind: "completeAttempt", attemptId: options["attempt"], candidate: options["candidate"], requiredCriteria: options["criterion"], summary: options["summary"],
    })));

  const evidence = program.command("evidence").description("inspect evidence through the runtime event journal");
  evidence.command("list").option("--after <cursor>", "cursor", "0").action(async ({ after }: { after: string }) => output((await runtimeClient()).query({ kind: "events", after: Number(after) })));
  evidence.command("inspect").requiredOption("--card <id>").action(async ({ card }: { card: string }) => output(await (await runtimeClient()).query({ kind: "card", cardId: new CardId(card) })));
  program.command("release").command("status").action(() => output({ featureDeliveryReady: false, productionReleaseReady: false, alphaCertified: false, reason: "Live cross-platform and provider gates remain unverified." }));
  return program;
}

async function initializeRepository(repository: string): Promise<Readonly<Record<string, unknown>>> {
  const projection = join(repository, ".super-speckit", "v2");
  await mkdir(projection, { recursive: true });
  const config = join(projection, "config.json");
  await writeFile(config, `${JSON.stringify({ schemaVersion: 1, githubCanonical: true, rawEvidenceInGit: false }, null, 2)}\n`, { flag: "wx" }).catch(ignoreExists);
  const agents = join(repository, "AGENTS.md");
  let current = "";
  try { current = await readFile(agents, "utf8"); } catch (error) { if (!isMissing(error)) throw error; }
  if (!current.includes("## Super-SpecKit project context")) await writeFile(agents, `${current.trimEnd()}${current.trim() === "" ? "" : "\n\n"}${agentsGuidance()}`);
  return { status: "initialized", repository, projection, credentialsStoredInRepository: false };
}

async function doctor(opencodeCommit: string | undefined): Promise<Readonly<Record<string, unknown>>> {
  const paths = runtimePaths();
  const checks = [
    { name: "node", status: process.versions.node.startsWith("22.") ? "pass" : "fail", observed: process.versions.node, required: "22.x" },
    { name: "platform", status: ["darwin", "linux", "win32"].includes(process.platform) ? "pass" : "fail", observed: process.platform },
    { name: "opencode", status: opencodeCommit === undefined ? "degraded" : opencodeCommit === OPENCODE_TARGET_COMMIT ? "pass" : "degraded", observed: opencodeCommit ?? "not supplied", target: OPENCODE_TARGET_COMMIT },
    { name: "daemon", ...(await daemonStatus()) },
  ];
  return { checks, stateRoot: paths.root, publicListener: false };
}

async function installDaemon(): Promise<Readonly<Record<string, unknown>>> {
  const paths = runtimePaths();
  await mkdir(paths.root, { recursive: true, mode: 0o700 });
  try { await access(paths.token); } catch { await writeFile(paths.token, `${randomBytes(32).toString("hex")}\n`, { mode: 0o600, flag: "wx" }); }
  await chmod(paths.token, 0o600);
  await writeFile(paths.install, `${JSON.stringify({ schemaVersion: 1, database: paths.database, socket: paths.socket, transport: "owned-local-socket", publicListener: false }, null, 2)}\n`);
  return { status: "installed", root: paths.root, supervision: "foreground; OS service registration is not yet certified" };
}

async function startDaemon(output: Output): Promise<void> {
  const paths = runtimePaths();
  await installDaemon();
  const token = (await readFile(paths.token, "utf8")).trim();
  const coordinator = new Coordinator({ databasePath: paths.database });
  const daemon = new CoordinatorDaemon({ coordinator, token, socketPath: paths.socket });
  await daemon.start();
  output({ status: "running", socket: paths.socket, publicListener: false });
  const stop = async () => { await daemon.stop(); coordinator.close(); };
  await new Promise<void>((resolvePromise) => {
    process.once("SIGINT", () => void stop().then(resolvePromise));
    process.once("SIGTERM", () => void stop().then(resolvePromise));
  });
}

async function daemonStatus(): Promise<Readonly<Record<string, unknown>>> {
  try {
    const events = await (await runtimeClient()).query({ kind: "events", after: 0, limit: 1 });
    return { status: "pass", state: "running", reachable: true, eventJournalReadable: Array.isArray(events) };
  } catch (error) {
    return { status: "degraded", state: "stopped-or-unreachable", reachable: false, reason: error instanceof Error ? error.message : "unknown error" };
  }
}

async function adoptPreview(repository: string, expectedDigest: string): Promise<Readonly<Record<string, unknown>>> {
  return applyV1Adoption({ repository, stateRoot: runtimePaths().root, expectedDigest });
}

async function syncPortfolio(planPath: string, apply: boolean): Promise<Readonly<Record<string, unknown>>> {
  const plan = parseGitHubSyncPlan(JSON.parse(await readFile(planPath, "utf8")));
  if (!apply) {
    return {
      status: "preview",
      plan: planPath,
      operations: plan.operations.map((operation) => ({ operationKey: operation.operationKey, kind: operation.kind, repository: operation.repository, issueNumber: operation.issueNumber })),
      mutationPerformed: false,
    };
  }
  return { status: "applied", ...(await applyGitHubSyncPlan({ stateRoot: runtimePaths().root, transport: new GhCliTransport(), plan })) };
}

async function createQuestionLedger(repository: string): Promise<Readonly<Record<string, unknown>>> {
  const path = join(repository, ".super-speckit", "architecture", "questions.json");
  await mkdir(dirname(path), { recursive: true });
  const questions = [
    { id: "Q-001", kind: "owner-decision", question: "What production outcome defines the first release?", status: "open", answer: null, evidence: [] },
    { id: "Q-002", kind: "fact", question: "Which quality scenario has the strictest measurable target?", status: "open", answer: null, evidence: [] },
    { id: "Q-003", kind: "fact", question: "Which failure must operators detect and recover first?", status: "open", answer: null, evidence: [] },
  ];
  await writeFile(path, `${JSON.stringify({ schemaVersion: 1, questions }, null, 2)}\n`, { flag: "wx" }).catch(ignoreExists);
  return { status: "ready", path, questions };
}

async function executeRuntime(expectedVersion: number, principal: string, command: Readonly<Record<string, unknown>>): Promise<CommandReceipt> {
  return (await runtimeClient()).execute({ protocolVersion: 1, requestId: randomUUID(), principal, expectedVersion, command });
}

async function runtimeClient(): Promise<SocketCoordinatorClient> {
  const paths = runtimePaths();
  const token = (await readFile(paths.token, "utf8")).trim();
  return new SocketCoordinatorClient({ socketPath: paths.socket, token });
}

function runtimePaths(): RuntimePaths {
  const base = process.env["XDG_STATE_HOME"] ?? (process.platform === "win32" ? process.env["LOCALAPPDATA"] : undefined) ?? join(homedir(), ".local", "state");
  const root = join(base, "super-speckit", "v2");
  return { root, database: join(root, "runtime.sqlite"), socket: join(root, "coordinator.sock"), token: join(root, "daemon.token"), install: join(root, "daemon.json") };
}

function ignoreExists(error: unknown): void { if (!(error instanceof Error && "code" in error && error.code === "EEXIST")) throw error; }
function isMissing(error: unknown): boolean { return error instanceof Error && "code" in error && error.code === "ENOENT"; }
function print(value: unknown): void { process.stdout.write(`${JSON.stringify(value, null, 2)}\n`); }
function withRevision(contract: Parameters<typeof fingerprintCard>[0]): Readonly<{ contract: Parameters<typeof fingerprintCard>[0]; revision: string }> { return { contract, revision: fingerprintCard(contract).value }; }

function handoffCommand(options: Readonly<Record<string, string>>): Readonly<Record<string, unknown>> {
  const phase = required(options, "phase");
  if (phase === "prepare") return { kind: "prepareHandoff", handoffId: options["handoff"] ?? randomUUID(), sourceAttemptId: required(options, "attempt"), destinationProviderId: required(options, "provider"), destinationRunnerId: required(options, "runner"), capsuleDigest: required(options, "capsule") };
  if (phase === "approve") return { kind: "approveHandoff", handoffId: required(options, "handoff"), capsuleDigest: required(options, "capsule"), approvedBy: required(options, "approvedBy"), approvedAt: new Date().toISOString(), expiresAt: required(options, "expiresAt") };
  if (phase === "activate") return { kind: "activateHandoff", handoffId: required(options, "handoff"), destinationAttemptId: required(options, "destinationAttempt"), destinationWorkspaceId: required(options, "workspace") };
  if (phase === "ack") return { kind: "acknowledgeHandoff", handoffId: required(options, "handoff"), destinationAttemptId: required(options, "destinationAttempt"), revision: required(options, "revision"), capsuleDigest: required(options, "capsule") };
  if (phase === "unknown") return { kind: "recordHandoffUnknown", handoffId: required(options, "handoff"), reason: required(options, "reason") };
  throw new Error(`unsupported handoff phase: ${phase}`);
}

function required(options: Readonly<Record<string, string>>, name: string): string {
  const value = options[name];
  if (value === undefined || value.trim() === "") throw new Error(`--${name.replace(/[A-Z]/g, (letter) => `-${letter.toLowerCase()}`)} is required for this handoff phase`);
  return value;
}

if (process.argv[1] !== undefined && import.meta.url === new URL(`file://${resolve(process.argv[1])}`).href) {
  await buildProgram().parseAsync(process.argv);
}
