# Feature Specification — Super-SpecKit V2

## Document status

- Status: draft
- Feature ID: SSK-V2
- Owner: Poom5741
- Approvers: product owner; architecture and license review before implementation
- Last reviewed: 2026-10-30
- Maturity target: release
- Foundation sources: V2 research notes, current Super-SpecKit contracts, and `whitelabels-cex` Foundation evidence

## Request and evidence

- Original request: evolve Super-SpecKit from a portable skill-led method into a gorgeous OpenCode-native engineering operating system comparable in product impact to OMO, Superpowers, Oh My ClaudeCode, or OMP, while retaining portable skills and ordinary GitHub contribution paths.
- User/problem evidence: current work is slowed more by Docker, Windows-to-WSL execution, environment recovery, browser access, and handoffs than by model generation. Existing installations can also leave only the bootstrap installer visible to host-specific skill discovery.
- Constraints: GitHub Project is canonical for work intent; committed `.super-speckit/` content contains no credentials or confidential raw evidence; the product remains agent- and harness-neutral; OpenCode is the first premium host; existing installations and history must migrate safely.
- Known assumptions: technical-founder/tech-lead users are the first audience; `whitelabels-cex` is the first dogfood project; at least one owned machine remains online for V1 unattended execution.
- Open questions: exact pinned OpenCode V2 API; final license inventory; public ADE integration surface; evidence-retention defaults; GitHub Project field schema; final visual design.

## L1 — Positioning and intent

### User and context

The first user is a technical founder, product owner, or tech lead responsible for turning product intent into a production-deployable first release with a 2–4-person human/agent team. Developers may use different harnesses or no Super-SpecKit runtime at all.

### Job and desired outcome

Install one product that makes serious engineering feel like cooperative mission control: establish architecture and a tested Foundation, expose independently claimable GitHub cards, route work to the best available harness, continue safely in the background, switch harnesses without losing card identity, and produce trustworthy evidence through release.

### Problem and opportunity

Portable skills define good behavior but do not provide persistent orchestration, live agent lanes, environment ownership, model/harness routing, cross-machine continuation, or a coherent control surface. Host-specific systems provide pieces of that runtime but should not own product intent or evidence truth. The opportunity is one open engineering protocol with progressively richer host integrations.

### Scope

- Portable method and skill layer: Architecture Researcher, Principal Architect, Portfolio/Foundation planning, implementation, verification, release, and learning.
- GitHub-authoritative Portfolio with versioned card contracts, dependency frontier, pivots, risk routing, and two readiness gates.
- Provider-neutral Runtime for attempts, leases, checkpoints, budgets, cancellation, evidence, worktrees, and handoffs.
- OpenCode Mission Control with server plugin, TUI, later GUI, shared RPC, permanent role roster, adaptive agents, and live project views.
- Local-first runners for macOS, Linux, and persistent Windows/WSL execution.
- Optional Herdr, ADE, and Cloudflare Browser Run adapters.
- Safe adoption and migration of existing Super-SpecKit projects, beginning with `whitelabels-cex`.

### Non-goals for V1

- Hosted coding when every owned machine is offline.
- Non-technical PM portal.
- GitLab, Jira, or Linear integration.
- Enterprise identity, multi-organization administration, or cross-client analytics.
- Automatic production deployment.
- Native mobile, embedded, game, data-platform, or ML project archetypes.
- Making ADE, Herdr, OpenCode session state, or Cloudflare the canonical work ledger.

### Success signals

- A user installs V2 and immediately sees project capability, card, environment, and evidence state rather than another instruction to invoke a skill.
- `whitelabels-cex` imports without history loss and completes at least three materially different real cards.
- An active card survives UI closure, interruption, harness switch, and one mid-card GitHub revision without duplicate writers or stale evidence passing.
- Windows/WSL and macOS both complete the acceptance journey.
- A developer who opts out can contribute through GitHub, branch/PR, tests, and CI; V2 imports the result.
- Local metrics demonstrate reduced environment wait, context reconstruction, or end-to-end card time without higher escaped-defect rate.

## L2 — Information requirements

| Information/decision | Why it matters | Priority | Source/provenance | Freshness/confidence |
| --- | --- | --- | --- | --- |
| Active GitHub card revision, owner and dependencies | Prevent stale or duplicate implementation | Critical | GitHub Issue/Project API | Live; canonical |
| Architecture decisions and inherited contracts | Let any harness act consistently | Critical | Repository ADRs/contracts | Commit-bound |
| Available harness, model and environment capabilities | Route to what can actually perform the work | Critical | Runtime capability probes | Recheck on startup/drift |
| Attempt, worktree, lease and checkpoint state | Resume and fence concurrent writers | Critical | Runtime ledger and redacted repo projection | Revisioned |
| Candidate SHA and evidence freshness | Prevent false completion | Critical | Git, CI, verifier receipts | Candidate-bound |
| Budget and cancellation state | Bound unattended authority | High | Project policy and provider observations | Live |
| Foundation and Production readiness | Avoid confusing runway with release | High | Computed capability/evidence graph | Recompute on change |
| Provider limitations and costs | Choose Herdr/ADE/Cloudflare honestly | High | Pinned official sources and probes | Volatile |
| Local delivery metrics | Prove the product improves flow | Medium | Local-only telemetry | Per run/project |

## L3 — Core journey

### Entry conditions

The user is in an existing or empty Git repository with GitHub access. OpenCode enhancement is optional; portable mode remains valid. Sensitive credentials are available only through approved local/provider secret stores.

### Primary path

| Step/state | User intent | System behavior | Visible feedback | Exit/recovery |
| --- | --- | --- | --- | --- |
| Install | Enable the product once | Install method, Runtime and host entry points; pin/probe compatibility | Installed components and limitations | Idempotent repair or uninstall guidance |
| Discover/adopt | Understand an existing project | Read GitHub, Git, contracts, `.super-speckit/`, tests and providers without mutation | Capability map, contradictions, migration preview | User resolves only material authority conflicts |
| Architect/Foundation | Establish a development runway | Research current evidence, reason from domain/quality drivers, publish Foundation graph | Decisions, evidence, risks and walking-skeleton target | Reopen only affected decisions/cards |
| Select/claim | Start the next useful work | Compute dependency frontier, acquire fenced lease, create owned worktree/attempt | Mission, owner, harness, budget and expected proof | Release or transfer lease safely |
| Execute | Complete the card | Activate the smallest useful role set; run warm environment and targeted feedback | Live lanes, environment and test progress | Checkpoint, retry, interrupt or handoff |
| Verify | Prove the exact candidate | Separate verifier and browser specialist execute required public-seam checks | Typed evidence and defects | New candidate receives fresh verification |
| Merge/release | Advance safely | Update GitHub, merge/deploy within policy, require human production approval | Readiness and risk state | Contain or rollback only when proven safe |
| Learn | Improve future work | Propose evidence-backed method changes as pull requests | Proposal, blast radius and fixture | Human review; no silent self-modification |

### Completion, cancellation and resumption

Completion requires the active GitHub card revision, exact candidate, required evidence, and policy authority. Cancellation is a durable transition with provider acknowledgement. A handoff creates a new attempt under the same card; ambiguous delivery fences duplicate execution. Closing a client does not stop a supervised run, but powering off every execution host ends V1 compute and requires checkpoint recovery.

## L4 — Functional responsibilities

| Responsibility | Required content/data | User action | System response | Candidate semantic role |
| --- | --- | --- | --- | --- |
| Portfolio | Card revisions, status, dependencies, priority, ownership | Shape/approve work in GitHub | Reconcile and compute frontier | Portfolio service |
| Architecture intelligence | Drivers, evidence, alternatives, risks, ADRs | Decide only consequential tradeoffs | Research, compare and review | Researcher + Principal Architect |
| Mission Control | Cards, lanes, agents, environment, proof | Direct or observe work | Live TUI/GUI and quiet notifications | OpenCode UI/RPC |
| Scheduler | Dependencies, capabilities, budgets, leases | Start/stop autonomous run | Activate smallest useful team | Coordinator |
| Environment runner | Worktree, tools, Docker, ports, caches | Approve bounded ownership | Warm and recover owned resources | macOS/Linux/WSL runner |
| Handoff | Contract revision, checkpoint, evidence, workspace | Choose target harness | Fence source and acknowledge destination | Runtime handoff service |
| Browser verification | Preview route, journey, synthetic account | Observe/take over if desired | Cloud/local browser evidence | Browser Specialist |
| Evidence | Candidate, criterion, environment, artifact descriptor | Review/accept risk | Append, stale and render proof | Evidence service |
| Portable participation | `AGENTS.md`, card, commands, CI | Work without Runtime | Import commits and CI evidence | Compatibility path |

## L5 — Boundary and non-ideal states

| State/condition | Trigger | Required treatment | Recovery/next action | Evidence/owner |
| --- | --- | --- | --- | --- |
| Bootstrap visible but product skills missing | Host-specific discovery root absent | Repair every supported project root idempotently | `--register-only`; restart host discovery | Installer receipt |
| GitHub and repository disagree | Card pivot or stale projection | GitHub wins for work contract; technical conflict is surfaced | Reconcile new revision and invalidate affected proof | Coordinator |
| Lease owner disappears | Host crash, timeout or network split | Expire with fencing token; preserve dirty worktree | Inspect and resume/transfer | Runtime |
| Provider unavailable | Herdr/ADE/Cloudflare/OpenCode capability missing | Degrade to supported local/portable path | Re-probe or choose provider | Capability receipt |
| WSL/Docker failure | Bridge, filesystem, daemon or port problem | Runner diagnoses owned layer; never modify unrelated resources | Repair/restart owned resources | Environment runner |
| Browser cannot reach app | Private preview or tunnel failure | Do not mark journey passed | Create protected route or use local provider | Browser Specialist |
| Card changes mid-run | New canonical revision activates | Fence old attempt until explicit acknowledgement | Reassess, preserve or restart | Portfolio/Coordinator |
| Paid budget reached | Provider usage reaches cap | Stop new paid work safely | Owner approves extension | Budget ledger |
| Evidence contains sensitive material | Transcript/recording/log capture | Keep raw artifact outside Git; commit redacted descriptor only | Redact, restrict or delete | Evidence policy |
| Human overrides a failure | Authorized risk acceptance | Preserve failed result and record scope/expiry | Follow-up card; no false pass | Release owner |
| Client/UI closes | Supervised service remains online | Continue explicitly authorized run | Replay on reconnect | Runtime |
| Every host powers off | V1 has no hosted coder | Preserve checkpoint; report paused | Resume on owned host | Coordinator |
| Accessibility or narrow terminal | TUI/GUI constraint | Keyboard-first, textual equivalents, responsive panels | Fall back to portable CLI/state | Mission Control |

## L6 — Acceptance contract

| ID | Observable criterion | Required evidence | Review mode | Source rule |
| --- | --- | --- | --- | --- |
| AC-01 | One install exposes all four public skills in every supported project-local harness root | Clean fixture install and discovery assertions | Automated | Installer contract |
| AC-02 | Existing `whitelabels-cex` state imports without loss or silent reinterpretation | Migration diff, backup, digest and rollback exercise | Independent | Compatibility decision |
| AC-03 | Mission Control renders GitHub frontier, card revision, agents, environment and proof | TUI journey and accessibility review | Independent runtime | Product grill |
| AC-04 | Closing and reopening OpenCode does not stop an authorized active attempt | Supervised-service interruption test | Runtime | Unattended contract |
| AC-05 | Windows OpenCode can execute through a persistent WSL-native runner without per-command bridge fragility | Clean Windows 11/WSL dogfood evidence | Independent runtime | User bottleneck evidence |
| AC-06 | A card transfers between two harness providers without losing identity or duplicating a writer | Fenced handoff fault-injection test | Independent | Handoff contract |
| AC-07 | Browser Run can test a protected preview, allow human takeover, and return redacted evidence | Recorded public-seam journey, cleanup and budget receipt | Independent browser | Cloudflare research |
| AC-08 | Failed/stale checks cannot be rendered as passed; an override remains visibly failed-but-accepted | Negative fixtures | Automated + review | Evidence policy |
| AC-09 | A non-Runtime developer can complete a card through ordinary GitHub/PR/CI and be imported | Fresh contributor fixture | Independent | Graceful opt-out |
| AC-10 | Feature Delivery Ready and Production Release Ready remain distinct | State-transition and UI assertions | Automated | `whitelabels-cex` evidence |
| AC-11 | No committed V2 artifact contains test credentials, raw private evidence or machine auth | Secret scan, schema validation and fixture review | Automated + security | Repository-safe rule |
| AC-12 | Public alpha evidence covers three real card shapes, macOS, Windows/WSL, Herdr, ADE, Cloudflare, interruption, pivot and opt-out | Alpha proof pack | Independent owner review | Dogfood decision |

## Decision log

| Decision | Status | Evidence/rationale | Owner | Date |
| --- | --- | --- | --- | --- |
| One repository with portable skills and enhanced OpenCode Runtime | confirmed in conversation | Progressive enhancement preserves harness neutrality | Product owner | 2026-10-30 |
| GitHub is canonical for card work; `.super-speckit/` is safe projection/evidence | confirmed in conversation | Supports PM portal and ordinary contributors | Product owner | 2026-10-30 |
| Two readiness gates | confirmed in conversation | `whitelabels-cex` proves runway is not production | Product owner | 2026-10-30 |
| Permanent roles, ephemeral attempts, adaptive parallelism | confirmed in conversation | Avoid idle cost and stale global context | Product owner | 2026-10-30 |
| Herdr and ADE are optional peers; Cloudflare is browser specialist | confirmed in conversation | Provider-neutral Runtime prevents lock-in | Product owner | 2026-10-30 |
| Dogfood existing `whitelabels-cex` before greenfield automation | confirmed in conversation | Real migration is harder and more valuable than a demo | Product owner | 2026-10-30 |
| Open core with candidate Apache-2.0 for new code | proposed pending audit | Adoption plus commercial hosted boundary | Product owner/legal | 2026-10-30 |

## Gaps and dependencies

| Gap/dependency | Impact | Owner | Needed by | Project-level gap? |
| --- | --- | --- | --- | --- |
| Stable/pinned OpenCode V2 plugin API | Blocks reliable plugin implementation | Runtime lead | Foundation F06 | Yes |
| License and notice inventory | Blocks final distribution decision | Legal/maintainer | Public alpha | Yes |
| GitHub Project field/revision protocol | Blocks canonical sync | Portfolio lead | Foundation F04 | Yes |
| ADE public integration and license boundary | Blocks ADE adapter | Runtime lead/legal | Feature P06 | Yes |
| Windows 11/WSL clean-machine proof | Blocks cross-platform claim | Environment lead | Alpha | Yes |
| Protected preview mechanism and retention policy | Blocks Cloudflare acceptance | Browser/security lead | Feature P07 | Yes |
| Final design system and accessibility evaluation | Blocks polished Mission Control release | Product/design | Mission Control feature set | Yes |
