import { CardContractWireSchema, parse, type CardContractWire } from "@super-speckit/protocol";

export type ArchitectureQuestion = Readonly<{
  id: string;
  kind: "fact" | "owner-decision";
  question: string;
  status: "open" | "answered";
  answer: string | null;
  evidence: readonly string[];
}>;

export type QualityScenario = Readonly<{
  stimulus: string;
  environment: string;
  response: string;
  measure: string;
}>;

export type ArchitectureDecision = Readonly<{
  id: string;
  title: string;
  drivers: readonly string[];
  alternatives: readonly Readonly<{ name: string; benefits: readonly string[]; costs: readonly string[] }>[];
  selected: string;
  rationale: string;
  scenarios: readonly QualityScenario[];
  threats: readonly string[];
  operations: readonly string[];
}>;

export type FoundationInput = Readonly<{
  repository: string;
  baseRef: string;
  domain: "web-service" | "web-application" | "cli";
  decisions: readonly ArchitectureDecision[];
}>;

export function generateFoundationCards(input: FoundationInput): readonly CardContractWire[] {
  const universal = [
    card(input, "Build and test the walking skeleton", "A fresh operator starts the system and completes one public-seam request.", "delivery-runway", "high"),
    card(input, "Establish unit, integration, and end-to-end feedback", "Each test layer catches one historical or seeded failure through a public seam.", "test", "high"),
    card(input, "Establish CI and exact-candidate evidence", "CI binds required checks to one immutable candidate and reports missing proof.", "delivery", "high"),
    card(input, "Establish secrets and configuration boundaries", "A clean environment starts through logical secret handles without committed credentials.", "security", "high"),
    card(input, "Establish observability and recovery", "An operator detects, diagnoses, and recovers one injected failure.", "operations", "medium"),
  ];
  const domain = input.domain === "web-application"
    ? [card(input, "Establish accessible application shell and browser journey", "Keyboard and browser checks complete the walking-skeleton journey.", "frontend", "medium")]
    : input.domain === "web-service"
      ? [card(input, "Establish API contract and durable data migration", "A versioned API request persists through one reversible migration.", "backend", "high")]
      : [card(input, "Establish CLI contract and isolated fixture", "A fresh process completes the primary command with deterministic output.", "cli", "medium")];
  const decisions = input.decisions.map((decision) => card(
    input,
    `Prove ${decision.title}`,
    `Executable evidence confirms the selected architecture decision: ${decision.rationale}`,
    "architecture",
    "high",
  ));
  return [...universal, ...domain, ...decisions];
}

export function generateV2AlphaCardGraph(repository: string, baseRef: string): Readonly<{ foundation: readonly CardContractWire[]; features: readonly CardContractWire[] }> {
  const foundationDefinitions: readonly Definition[] = [
    ["F01", "Freeze V1 behavior, source/license inventory and alpha authority boundary", [], "Reproducible baseline, licensing report, and dirty-work preservation are proven.", "governance", "high"],
    ["F02", "Pin and probe one OpenCode V2 plugin contract", [], "Server, TUI, and RPC fixtures report supported or degraded APIs.", "opencode", "high"],
    ["F03", "Publish versioned runtime protocol schemas", ["F01"], "Positive and negative schema fixtures pass without credential-bearing fields.", "protocol", "high"],
    ["F04", "Implement the atomic runtime ledger", ["F03"], "Stale writers, duplicate completion, expiry, and ambiguous cancellation are fenced.", "runtime", "high"],
    ["F05", "Define GitHub ownership and card revision activation", ["F03"], "A canonical pivot fences the old attempt and invalidates affected proof.", "github", "high"],
    ["F06", "Deliver the OpenCode Mission Control vertical slice", ["F02", "F04"], "An active fixture survives client closure and reconstructs in the TUI.", "opencode", "high"],
    ["F07", "Deliver repository-safe evidence and budget policy", ["F03"], "Raw private evidence stays outside Git and retention is enforced.", "evidence", "high"],
    ["F08", "Migrate and roll back V1 state", ["F04", "F07"], "Preview, backup, digest verification, rollback, and repeat adoption pass.", "migration", "high"],
    ["F09", "Publish provider SDK and conformance harness", ["F04"], "Lifecycle idempotency and observation semantics pass against the fake provider.", "provider", "high"],
    ["F10", "Deliver the environment runner protocol", ["F04"], "Structured commands, ownership, streaming, and safe cleanup pass.", "runner", "high"],
    ["F11", "Deliver the persistent Windows and WSL runner", ["F10"], "A clean WSL run uses one bridge and preserves unrelated resources.", "windows", "high"],
    ["F12", "Deliver native macOS and Linux execution", ["F10"], "The reference fixture passes with explicit engine degradation.", "native", "medium"],
    ["F13", "Deliver the Herdr adapter", ["F09", "F10"], "Warm terminals, panes, SSH, and interruption recovery pass.", "herdr", "medium"],
    ["F14", "Deliver the external ADE adapter", ["F09", "F10"], "Lane, proof, and handoff pass without ADE owning canonical state.", "ade", "medium"],
    ["F15", "Deliver Cloudflare Browser Run QA", ["F09", "F07"], "Guardrails, synthetic auth, recording, budget, and cleanup pass.", "browser", "high"],
    ["F16", "Close Feature Delivery Ready independently", ["P05", "P06", "P07", "P08"], "A fresh operator imports, runs, hands off, verifies, and continues real work.", "release", "high"],
    ["F17", "Close public-alpha evidence independently", ["P10"], "AC-01 through AC-12 and exact-candidate review pass.", "release", "high"],
  ];
  const featureDefinitions: readonly Definition[] = [
    ["P01", "Adopt whitelabels-cex through a truthful preview", ["F05", "F08"], "Foundation, cards, branches, decisions, and drift are visible before mutation.", "adoption", "high"],
    ["P02", "Understand the project immediately in Mission Control", ["F06", "F07"], "Keyboard-first project, environment, agent, and evidence views are usable.", "experience", "medium"],
    ["P03", "Claim a GitHub card and survive a pivot", ["P01", "F04"], "Lease, worktree, revision acknowledgement, and stale proof are fenced.", "delivery", "high"],
    ["P04", "Run the smallest useful permanent-role team", ["P02", "P03", "F09"], "Independent lanes run concurrently with one writer per card.", "team", "high"],
    ["P05", "Complete three real whitelabels-cex card shapes", ["P04", "F11", "F12"], "Backend, UI, and infrastructure cards carry exact-candidate proof.", "dogfood", "high"],
    ["P06", "Continue an unattended Herdr-backed card", ["F13", "P03"], "Identity, warm environment, and checkpoint survive without a duplicate writer.", "herdr", "high"],
    ["P07", "Move a card between owned machines through ADE", ["F14", "P03"], "Cross-machine handoff is idempotent and acknowledgement ambiguity is recoverable.", "ade", "high"],
    ["P08", "Test a headless web feature with human takeover", ["F15", "P02"], "Live View, recording descriptor, handback, and route cleanup pass.", "browser", "high"],
    ["P09", "Research and decide architecture at principal level", ["F16"], "Scenarios, alternatives, threats, operations, and owner decisions produce ADRs.", "architecture", "high"],
    ["P10", "Generate and re-import a greenfield Foundation graph", ["P09"], "Universal, domain, and project cards reach Feature Delivery Ready without semantic loss.", "greenfield", "high"],
  ];
  return {
    foundation: foundationDefinitions.map((definition) => alphaCard(repository, baseRef, "foundation", definition)),
    features: featureDefinitions.map((definition) => alphaCard(repository, baseRef, "feature", definition)),
  };
}

type Definition = readonly [id: string, title: string, dependencies: readonly string[], acceptance: string, capability: string, risk: "low" | "medium" | "high"];

function alphaCard(repository: string, baseRef: string, kind: "foundation" | "feature", definition: Definition): CardContractWire {
  const [id, title, dependencies, acceptance, capability, risk] = definition;
  return parse(CardContractWireSchema, {
    schemaVersion: 1,
    repository,
    issueNodeId: `pending:${id}`,
    issueNumber: 1,
    title: `${id} ${title}`,
    kind,
    outcome: acceptance,
    nonGoals: ["Automatic production deployment", "Unreviewed writer handoff"],
    acceptance: [acceptance],
    dependencies,
    baseRef,
    capability,
    risk,
  });
}

function card(input: FoundationInput, title: string, acceptance: string, capability: string, risk: "low" | "medium" | "high"): CardContractWire {
  return parse(CardContractWireSchema, {
    schemaVersion: 1,
    repository: input.repository,
    issueNodeId: `pending:${slug(title)}`,
    issueNumber: 1,
    title,
    kind: "foundation",
    outcome: acceptance,
    nonGoals: ["Automatic production deployment"],
    acceptance: [acceptance],
    dependencies: [],
    baseRef: input.baseRef,
    capability,
    risk,
  });
}

function slug(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}
