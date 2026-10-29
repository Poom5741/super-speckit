# OpenCode runtime and portfolio layer research

Research snapshot: 2026-10-30. This note uses only first-party repositories and official product documentation. Repository claims are pinned to the inspected commits so later changes do not silently rewrite the evidence.

## Decision summary

Super-SpecKit should become three related but separable layers:

1. **Method core** — the existing skills, playbooks, gates, and evidence rules. This stays portable across harnesses.
2. **Runtime adapters** — an installable OpenCode v2 plugin first, followed by Codex, Claude Code, ACP, and computer-use adapters. An adapter turns the method into agents, tools, hooks, background runs, model routing, UI, and worktree operations.
3. **Portfolio control plane** — a layer above Super-SpecKit that starts with an empty repository, interviews the owner about product and architecture, publishes foundation and feature cards to GitHub, exposes the unblocked frontier, and keeps a durable card-scoped run ledger that any harness can resume.

The important architectural boundary is that **a harness session is an execution attempt, not the identity or source of truth for a card**. Slim explicitly documents that aliases and reusable-session history are process-local and only partially recover after restart, which makes session state unsuitable as the portable handoff authority ([Slim background orchestration, lines 94-127](https://github.com/alvinunreal/oh-my-opencode-slim/blob/fbd9de5694c3fdde0138d79e6f465d83d45cf3d6/docs/background-orchestration.md#L94-L127)). OpenCode does provide durable plugin-scoped JSON storage, but that storage is still OpenCode-specific ([OpenCode server plugin storage, lines 927-963](https://github.com/anomalyco/opencode/blob/1eea2d4d606b3688d243033446d6ab83113431c8/services/www/src/docs/content/build/plugins/server.mdx#L927-L963)). Neither should become the cross-harness truth.

The practical recommendation is therefore:

- Ship an npm package that installs as an OpenCode v2 plugin and exports server, TUI, GUI, and RPC parts.
- Keep orchestration state in a harness-neutral card store keyed by the GitHub issue's immutable node identity, with adapters storing only their own session references.
- Use a real GitHub issue as each card's durable contract; add the issue to a GitHub Project as the portfolio view. Do not use a Project draft item as the only work identity.
- Treat Oh My OpenAgent, Oh My ClaudeCode, Slim, and Nexus as implementation references, not as workflow foundations to import wholesale.

## What “not just skills” means in OpenCode v2

OpenCode v2's official plugin contract is already the runtime substrate Super-SpecKit needs. A single package may expose:

- a **server** part for tools, hooks, integrations, commands, and agents;
- a **TUI** part for terminal routes, commands, tabs, slots, and panels;
- a **GUI** part for Desktop panels, commands, settings, and native integrations;
- a typed **RPC** contract shared by those parts and external clients.

Those are official package entry points, not conventions invented by Slim or Nexus ([OpenCode plugin overview, lines 22-51](https://github.com/anomalyco/opencode/blob/1eea2d4d606b3688d243033446d6ab83113431c8/services/www/src/docs/content/build/plugins/index.mdx#L22-L51)). Published packages or local plugin directories are loaded from the `plugins` array in `opencode.json(c)`, while project-local plugins under `.opencode/plugins/` load automatically ([OpenCode plugin loading, lines 57-90](https://github.com/anomalyco/opencode/blob/1eea2d4d606b3688d243033446d6ab83113431c8/services/www/src/docs/content/build/plugins/index.mdx#L57-L90)).

That gives a concrete install target:

```text
opencode plugin add @super-speckit/opencode
```

The package should have these parts:

| Part | Super-SpecKit responsibility |
| --- | --- |
| Server | Register the orchestrator and specialists; expose card, run, evidence, handoff, GitHub, routing, and verification tools; observe session/tool/shell lifecycle; create child sessions; manage OpenCode worktrees. |
| TUI | Portfolio/card dashboard, active runs, card frontier, evidence status, lease owner, background child tabs, and model-routing visibility. |
| GUI | The same control plane in Desktop, plus richer architecture/card/evidence panels and browser/computer-use run visibility. |
| RPC | A stable contract so the UI and non-OpenCode harness bridges use the same card/run operations. |

OpenCode v2 exposes the necessary mechanics:

- custom agents have model, prompt, mode, and permission profiles; subagents run in fresh foreground or background child sessions ([OpenCode agents, lines 100-130](https://github.com/anomalyco/opencode/blob/1eea2d4d606b3688d243033446d6ab83113431c8/services/www/src/docs/content/agents.mdx#L100-L130));
- plugins can create, list, prompt, switch model/agent, interrupt, wait for, and remove sessions ([OpenCode session API, lines 771-831](https://github.com/anomalyco/opencode/blob/1eea2d4d606b3688d243033446d6ab83113431c8/services/www/src/docs/content/build/plugins/server.mdx#L771-L831));
- plugins can register namespaced tools with progress and cancellation ([OpenCode tools, lines 966-1017](https://github.com/anomalyco/opencode/blob/1eea2d4d606b3688d243033446d6ab83113431c8/services/www/src/docs/content/build/plugins/server.mdx#L966-L1017));
- session, permission, shell, and tool hooks can transform requests and observe execution ([OpenCode session/tool hooks, lines 1345-1437](https://github.com/anomalyco/opencode/blob/1eea2d4d606b3688d243033446d6ab83113431c8/services/www/src/docs/content/build/plugins/server.mdx#L1345-L1437), [lines 1673-1759](https://github.com/anomalyco/opencode/blob/1eea2d4d606b3688d243033446d6ab83113431c8/services/www/src/docs/content/build/plugins/server.mdx#L1673-L1759));
- worktrees are a first-class project API with saved ownership and non-forced removal by default ([OpenCode worktrees, lines 1141-1219](https://github.com/anomalyco/opencode/blob/1eea2d4d606b3688d243033446d6ab83113431c8/services/www/src/docs/content/build/plugins/server.mdx#L1141-L1219));
- TUI plugins can open child sessions in tabs and contribute a session side panel, avoiding a dependence on tmux for the basic experience ([OpenCode TUI tabs, lines 455-483](https://github.com/anomalyco/opencode/blob/1eea2d4d606b3688d243033446d6ab83113431c8/services/www/src/docs/content/build/plugins/cli.mdx#L455-L483), [session panels, lines 547-623](https://github.com/anomalyco/opencode/blob/1eea2d4d606b3688d243033446d6ab83113431c8/services/www/src/docs/content/build/plugins/cli.mdx#L547-L623)).

The runtime should use the v2 APIs directly rather than adding a compatibility shell first. Slim's compatibility layer is substantial because it carries one codebase across v1 and v2; Super-SpecKit does not need that complexity unless v1 support becomes an explicit requirement.

## What is reusable from each project

### Oh My OpenAgent

The current repository is broader than an OpenCode plugin. Its package contains separate cores for delegation, models, config, prompts, tmux, teams, memory, isolation, skills, Codex, OpenCode, Senpi, and a native runtime ([Oh My OpenAgent package workspaces, lines 8-42](https://github.com/code-yeongyu/oh-my-openagent/blob/97ae220dcfddbd8f31afbd388a07b01d2c1723eb/package.json#L8-L42)). Its current README leads with a standalone `omo` binary running on a Senpi fork, with OpenCode migration rather than OpenCode as the sole host ([Oh My OpenAgent README, lines 45-62](https://github.com/code-yeongyu/oh-my-openagent/blob/97ae220dcfddbd8f31afbd388a07b01d2c1723eb/README.md#L45-L62)).

Reusable ideas:

- **Capability/category routing instead of model names in workflow logic.** The task tool delegates to categories, and config resolves category defaults, user fallbacks, provider chains, and system defaults ([configuration, lines 337-395](https://github.com/code-yeongyu/oh-my-openagent/blob/97ae220dcfddbd8f31afbd388a07b01d2c1723eb/docs/reference/configuration.md#L337-L395)). Super-SpecKit should route `architecture`, `quick-fix`, `browser-qa`, `visual-design`, `deep-debug`, and `review` capabilities, then let each adapter map them to available models/harnesses.
- **Separate reusable cores from host adapters.** The repository's workspace layout is direct evidence that model routing, task state, memory, isolation, and skills can be packaged independently of OpenCode.
- **Resumability is an engine concern.** OmO claims long work records what was checked so a restarted session can continue ([README, lines 68-78](https://github.com/code-yeongyu/oh-my-openagent/blob/97ae220dcfddbd8f31afbd388a07b01d2c1723eb/README.md#L68-L78)). Super-SpecKit should implement this as explicit card/run/evidence state, not copy OmO's opaque engine state.

Do not copy:

- the full prompt/process layer, because it overlaps with Super-SpecKit's method;
- its provider/model tables, which are fast-moving policy data;
- its current install shape as the OpenCode architecture: the project has evolved into a multi-harness/native system, so “copy Oh My OpenAgent” no longer means “write one OpenCode plugin.”

### Oh My ClaudeCode

Oh My ClaudeCode demonstrates how a method becomes an actual host runtime. Installation is a Claude Code marketplace/plugin flow; it exposes in-session skills plus a separate npm CLI and SDK surface ([Oh My ClaudeCode README, lines 55-99](https://github.com/Yeachan-Heo/oh-my-claudecode/blob/eaa36ef9fc6ba12387ae9e7b8cd8f650c9dfbba7/README.md#L55-L99)). Its terminal `omc team` runtime launches real Claude/Codex/Gemini/etc. CLI workers in tmux, while `/team` is a distinct native in-session team runtime ([README, lines 142-177](https://github.com/Yeachan-Heo/oh-my-claudecode/blob/eaa36ef9fc6ba12387ae9e7b8cd8f650c9dfbba7/README.md#L142-L177)).

Its strongest reusable architecture is the durable-state discipline:

- small orchestration metadata lives in a **control plane** and large plans, results, prompts, and traces in a **data plane**;
- large artifacts are referenced by descriptors containing kind, durable path, hash, producer, size, retention, and expiry;
- session state is isolated per session;
- centralized state can survive worktree deletion ([OMC architecture, lines 458-610](https://github.com/Yeachan-Heo/oh-my-claudecode/blob/eaa36ef9fc6ba12387ae9e7b8cd8f650c9dfbba7/docs/ARCHITECTURE.md#L458-L610)).

Its worktree contract is also directly relevant. Workers receive explicit persisted fields for state root, cwd, repo root, worktree path/branch, and creation mode; dirty worktrees are preserved, branch/path mismatches fail, and forced shutdown does not bypass ownership checks ([OMC native team worktrees, lines 1-56](https://github.com/Yeachan-Heo/oh-my-claudecode/blob/eaa36ef9fc6ba12387ae9e7b8cd8f650c9dfbba7/docs/TEAM-WORKTREE-MODE.md#L1-L56)). This is a better safety baseline than treating a worktree path as sufficient ownership evidence.

OMC's “Software Factory” design is unusually close to the requested higher layer: issue/cron/session triggers start headless sessions, human gates remain named, run ledgers record outcomes, and the design distinguishes foundation, chain, gate, ledger, and reflection layers ([factory design, lines 1-52](https://github.com/Yeachan-Heo/oh-my-claudecode/blob/eaa36ef9fc6ba12387ae9e7b8cd8f650c9dfbba7/docs/design/FACTORY-FINAL-DESIGN.md#L1-L52)). It should be mined for state and gate mechanics, but not imported as the product workflow: it already contains its own intake, planning, implementation, and review method, which would compete with Super-SpecKit.

### mattpocock/skills

This repository supplies most of the missing portfolio method, but as skills rather than a runtime.

- `grilling` builds a decision tree, asks the current frontier in rounds, recommends answers, and keeps facts as agent work while decisions remain human work ([grilling, lines 6-30](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/productivity/grilling/SKILL.md#L6-L30)). This is the correct interaction model for the initial product/architecture interview.
- `wayfinder` makes a tracker issue the canonical map, uses child issues for decision tickets, assigns claims before work, and uses native dependency edges to render the frontier ([wayfinder, lines 19-71](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/wayfinder/SKILL.md#L19-L71)). It also explicitly keeps planning tickets separate from implementation work ([lines 7-13](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/wayfinder/SKILL.md#L7-L13)).
- `to-tickets` turns a spec into independently verifiable vertical slices, sizes each to a fresh context, declares blockers, and publishes tracker-native dependencies ([to-tickets, lines 25-65](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/to-tickets/SKILL.md#L25-L65)).
- Its GitHub tracker adapter already knows sub-issues, native `blocked by` edges, frontier queries, and assignment-as-claim ([GitHub tracker adapter, lines 7-19](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/setup-matt-pocock-skills/issue-tracker-github.md#L7-L19), [lines 41-50](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/setup-matt-pocock-skills/issue-tracker-github.md#L41-L50)).

The missing piece is the user's two implementation-card classes. Wayfinder tickets are decisions, not implementation cards, and `to-tickets` does not distinguish foundational capability work from feature slices. Super-SpecKit's portfolio layer should add that distinction while retaining Wayfinder's planning map and `to-tickets`' vertical slicing.

### Oh My OpenCode Slim

Slim is the closest OpenCode runtime reference. It installs as a plugin, writes its plugin location into OpenCode config, supplies an orchestrator and specialist team, maps models per role, and makes background delegation the default ([Slim README, lines 30-57](https://github.com/alvinunreal/oh-my-opencode-slim/blob/fbd9de5694c3fdde0138d79e6f465d83d45cf3d6/README.md#L30-L57), [lines 92-159](https://github.com/alvinunreal/oh-my-opencode-slim/blob/fbd9de5694c3fdde0138d79e6f465d83d45cf3d6/README.md#L92-L159)).

Reusable ideas:

- scheduler-first orchestration: plan, dispatch specialists, monitor, reconcile, verify ([background orchestration, lines 1-19](https://github.com/alvinunreal/oh-my-opencode-slim/blob/fbd9de5694c3fdde0138d79e6f465d83d45cf3d6/docs/background-orchestration.md#L1-L19));
- per-session model presets, while already-created children retain their own configuration ([README, lines 179-193](https://github.com/alvinunreal/oh-my-opencode-slim/blob/fbd9de5694c3fdde0138d79e6f465d83d45cf3d6/README.md#L179-L193));
- an ACP wrapper that launches external Claude/Gemini-compatible runtimes, validates model selection, streams progress, and restricts wrapper tools ([ACP agents, lines 1-22](https://github.com/alvinunreal/oh-my-opencode-slim/blob/fbd9de5694c3fdde0138d79e6f465d83d45cf3d6/docs/acp-agents.md#L1-L22), [lines 76-97](https://github.com/alvinunreal/oh-my-opencode-slim/blob/fbd9de5694c3fdde0138d79e6f465d83d45cf3d6/docs/acp-agents.md#L76-L97));
- live panes as **views of existing child sessions**, not the process that owns dispatch ([multiplexer guide, lines 34-78](https://github.com/alvinunreal/oh-my-opencode-slim/blob/fbd9de5694c3fdde0138d79e6f465d83d45cf3d6/docs/multiplexer-integration.md#L34-L78));
- a conservative worktree skill that keeps a registry, asks before mutating Git, and refuses dirty or unmerged cleanup by default ([worktrees, lines 21-73](https://github.com/alvinunreal/oh-my-opencode-slim/blob/fbd9de5694c3fdde0138d79e6f465d83d45cf3d6/docs/worktrees.md#L21-L73)).

Do not use Slim's internal job board as the card ledger. Its documented restart behavior is explicitly partial, and its worktree registry is local and git-ignored. Both are useful runtime projections, not shared team truth.

### OpenCode Nexus

Nexus is useful as a compact reference for DAG execution, role/model scoring, real child sessions, retries, dashboards, and OpenCode plugin tooling ([Nexus README, lines 22-47](https://github.com/serkanalgur/opencode-nexus/blob/65f56b41a89afaa496b7cd89cc9f814fede2eb42/README.md#L22-L47)). Its install shape is also simple: a pure OpenCode plugin registered in `plugins`, with generated agent files and per-role config ([lines 51-82](https://github.com/serkanalgur/opencode-nexus/blob/65f56b41a89afaa496b7cd89cc9f814fede2eb42/README.md#L51-L82)).

Use it for ideas, not as a base:

- the README says goals persist across sessions, but the inspected `GoalManager` is in-memory; `goal.complete` writes a snapshot to plugin storage, while the inspected setup contains no restoration into the manager ([GoalManager](https://github.com/serkanalgur/opencode-nexus/blob/65f56b41a89afaa496b7cd89cc9f814fede2eb42/src/goal.ts#L13-L86), [goal storage on completion](https://github.com/serkanalgur/opencode-nexus/blob/65f56b41a89afaa496b7cd89cc9f814fede2eb42/src/index.ts#L2417-L2438)). That is not a demonstrated durable handoff contract.
- its worktree manager shells through interpolated strings, accepts `echo "Worktree exists"` as success, and removes worktrees and branches with force flags before dropping its in-memory record even on failure ([worktree manager, lines 25-70](https://github.com/serkanalgur/opencode-nexus/blob/65f56b41a89afaa496b7cd89cc9f814fede2eb42/src/worktree.ts#L25-L70)). This conflicts with the required preservation and ownership semantics.
- cost-aware routing is promising, but its own documentation distinguishes advisory per-task cost from an actually enforced run cap; a plugin should not present predicted or advisory values as enforcement ([Nexus budget, lines 357-397](https://github.com/serkanalgur/opencode-nexus/blob/65f56b41a89afaa496b7cd89cc9f814fede2eb42/README.md#L357-L397)).

## The higher-level portfolio lifecycle

The layer above Super-SpecKit should own this lifecycle:

```text
empty repo
  → owner grilling and domain model
  → product boundary and architecture decisions
  → quality/test strategy
  → foundation capability graph
  → feature vertical slices
  → GitHub issue + Project publication
  → unblocked-card frontier
  → per-card claim/lease
  → best-harness execution attempts
  → evidence and handoffs
  → review/merge/close
```

### Planning artifacts

Use three levels of tracker artifact:

1. **Initiative/map issue** — destination, scope, principles, major decisions, and links to decision issues. This is Wayfinder's planning map.
2. **Spec issue** — the settled product/architecture/testing contract from which implementation cards are cut.
3. **Implementation issues/cards** — independently claimable work units added to the GitHub Project.

The implementation issues have two types:

| Type | Purpose | Sizing and dependency rule |
| --- | --- | --- |
| Foundation | Establish a reusable capability or safe seam: repo layout, build, deploy, frontend/backend skeleton, database/migrations, auth boundary, test harness, unit/integration/E2E layers, observability, CI, fixtures, or shared contracts. | Must produce a verifiable capability, not “set up some files.” It may block feature cards. Use expand-contract for wide changes. |
| Feature | Deliver a narrow end-to-end user behavior through all required layers and tests. | Sized for one fresh implementation context and ideally dependency-free. If another card genuinely gates it, represent that with a native dependency rather than hiding the coupling in prose. |

“All feature cards independent” should be a design target, not a false invariant. The planner should actively redesign slices to remove unnecessary coupling, but when a dependency is real it must be explicit. GitHub now exposes native sub-issues and blocked-by relationships through its official APIs ([sub-issues API](https://docs.github.com/en/rest/issues/sub-issues), [issue dependencies API](https://docs.github.com/en/rest/issues/issue-dependencies)).

### GitHub Project model

Use **issues as contracts** and **Project items as projections**. GitHub's official Projects API adds an issue with `addProjectV2ItemById` and then updates Project-specific fields with `updateProjectV2ItemFieldValue`; these are separate operations ([GitHub Projects API guide](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects)).

Suggested Project fields:

| Field | Values or meaning |
| --- | --- |
| Type | Foundation / Feature |
| Phase | Discovery / Ready / In progress / Review / Done / Blocked |
| Capability | Architecture, backend, frontend, data, test, infra, DX, browser QA, etc. |
| Parallel lane | A stable lane or subsystem ownership label. |
| Harness | OpenCode / Codex / Claude Code / Browser / Human / Unassigned. |
| Risk | Low / Medium / High. |
| Evidence | Missing / Partial / Passing / Stale. |
| Lease until | Human-visible expiry time; the real lease still needs machine-enforced state. |

## Native, durable per-card handoff

A handoff must be a **live card record**, not a prose file written once at the end of a session. Each card needs a stable identity, versioned contract, active ownership, attempt history, checkpoints, evidence, and next action.

### Portable card contract

The minimum harness-neutral schema is:

```text
Card
  identity: repository + issue node id + issue number
  kind: foundation | feature
  contract_revision: immutable revision/hash of accepted scope
  status: planned | ready | claimed | running | blocked | review | done
  dependencies: card identities + edge kind
  acceptance: observable criteria
  verification_plan: test/evidence requirements by surface
  base: repository, base ref, base commit
  ownership: lease record
  attempts: ordered RunAttempt records
  checkpoints: ordered resumable states
  evidence: content-addressed ArtifactDescriptor records
  blockers: current facts requiring action
  next_action: one concrete continuation pointer
```

Each `RunAttempt` should record `run_id`, `card_id`, `harness`, adapter version, model/capability route, native session/thread ID, workspace/worktree identity, start/base commit, state, heartbeat, terminal reason, produced commits/PR, and evidence descriptors. A new harness creates a new attempt against the same card; it never rewrites the previous harness's session as though it were its own.

### Checkpoints, not summaries

A resumable checkpoint should be structured and incremental:

- contract revision consumed;
- last verified repository commit and dirty-state digest;
- completed acceptance criteria;
- pending criteria and exact next action;
- commands/tests already run with outcomes and timestamps;
- artifact descriptors and hashes;
- unresolved questions/blockers;
- workspace/worktree locator and ownership evidence;
- tool/harness-specific opaque resume token, stored as an adapter extension rather than a required portable field.

This follows OMC's control-plane/data-plane split and bounded artifact descriptors, while avoiding its `.omc`-specific format. Large screenshots, traces, browser recordings, logs, and reports should live in an artifact store; the card state contains a descriptor and digest.

### Lease and ownership rules

Assignment alone is a good human-visible claim, as Wayfinder uses, but it is not enough for an autonomous multi-harness runtime. The machine lease should contain:

```text
lease_id, card_id, owner_principal, harness, run_id,
workspace_id, acquired_at, heartbeat_at, expires_at,
contract_revision, fencing_token
```

Required behavior:

- acquire with compare-and-swap against the current card version;
- renew only with the same lease and fencing token;
- reject writes from expired or superseded owners;
- permit read-only/reviewer attempts without a write lease;
- never infer ownership from a session name, worktree path, pane ID, or branch alone;
- cleanup only resources whose instance, process/session, and workspace ownership evidence all match;
- preserve dirty worktrees and surface them for recovery.

OMC's instance-bound cleanup and worktree rules are the strongest source precedent here. Its design explicitly refuses cleanup when ownership receipts are absent and binds tmux ownership to more than a reusable pane name ([OMC migration notes, lines 102-162](https://github.com/Yeachan-Heo/oh-my-claudecode/blob/eaa36ef9fc6ba12387ae9e7b8cd8f650c9dfbba7/docs/MIGRATION.md#L102-L162)).

### Evidence contract

Evidence should be append-only and attributable. Each item needs:

```text
evidence_id, card_id, attempt_id, criterion_id,
kind, producer, command/tool, environment,
started_at, completed_at, outcome,
artifact descriptor, repository commit, stale_after/change_scope
```

The control plane must distinguish:

- claimed success from observed evidence;
- current evidence from evidence made stale by later edits;
- automated evidence from required human judgment;
- a harness timing out from the underlying task definitely stopping;
- a test report from the raw log/trace that supports it.

### Cross-harness execution

The core should expose an adapter interface resembling:

```text
probeCapabilities()
score(card, phase, constraints)
start(attempt, checkpoint)
observe(run_id)
checkpoint(run_id)
send(run_id, instruction)
interrupt(run_id)
collectEvidence(run_id)
release(run_id)
```

Routing then chooses a **harness plus capability**, not merely a model:

- OpenCode for plugin-native background teams and TUI/GUI visibility;
- Codex for repository implementation/review where its runtime is strongest;
- Claude Code for a Claude-native workflow or existing plugin/team capability;
- ACP when an external runtime speaks the protocol;
- browser/computer-use for manual QA, visual checks, and interactions that code-only harnesses cannot establish.

Slim's ACP bridge is reusable as one adapter path, but it is not the entire portability design: each ACP call creates a new subprocess/session and model selection is partly mediated through wrapper instructions ([Slim ACP, lines 76-127](https://github.com/alvinunreal/oh-my-opencode-slim/blob/fbd9de5694c3fdde0138d79e6f465d83d45cf3d6/docs/acp-agents.md#L76-L127)). The card checkpoint remains authoritative even when an ACP session cannot be resumed.

## What overlaps with Super-SpecKit and should stay out of the runtime

The compared projects bundle their own opinions about planning, implementation, review, and completion. Those are the parts most likely to fight Super-SpecKit.

Do not import as runtime policy:

- Ultrawork/Autopilot/Deepwork end-to-end methods;
- specialist prompts that redefine when planning, TDD, review, or completion happens;
- issue triage vocabularies that replace the portfolio/card state machine;
- memory that injects unverified conclusions as code truth;
- automatic worktree cleanup without fencing and dirty-state preservation;
- a model router whose costs, quality weights, or fallback list are hardcoded into task semantics.

Do reuse as runtime mechanics:

- plugin installation and multi-part packaging;
- tool/session/hook/event registration;
- background child lifecycle and result reconciliation;
- capability-based model/harness routing;
- UI projections of the same machine state;
- worktree inventory and ownership;
- control-plane/data-plane state separation;
- content-addressed evidence descriptors;
- GitHub sub-issues, dependency edges, Project fields, and frontier queries;
- ACP as one optional external-harness transport.

## Unresolved decisions to grill

These decisions materially change the architecture and should be settled with the user before implementation:

1. **Canonical machine state location.** GitHub-only state is universally reachable but weak for atomic leases and high-frequency events. A local SQLite daemon is strong on one machine but not a shared team control plane. A hosted service/GitHub App supports real leases and webhooks but creates operations and authentication work.
2. **Team topology.** Are the 2-4 developers on one machine, separate machines against one GitHub repository, or a mixture of humans and autonomous harnesses? This determines whether a local coordinator is sufficient.
3. **GitHub object model.** One initiative issue + spec issue + sub-issues is recommended, but the desired relationship between GitHub Project, milestones, releases, and PRs is not yet settled.
4. **Foundation-card gate.** Must all foundation cards finish before any feature starts, or can feature cards begin as soon as their specific capability blockers are closed? The latter gives more parallelism and is recommended.
5. **Definition of independently claimable.** Does one card own one branch/worktree and one PR, or may several cards share an integration branch? One card/branch/PR is safer; wide expand-contract migrations need an explicit exception.
6. **Contract mutability.** Who may revise scope after a card is claimed, and does a revision invalidate the lease or merely require acknowledgement? A changed contract should fence the old attempt until it explicitly accepts the new revision.
7. **Harness authority.** May the router automatically move a card between harnesses, or must the user approve every cross-harness handoff? Automatic read-only routing is low risk; moving a write lease should be explicit until the system earns trust.
8. **Evidence retention.** Where should screenshots, browser recordings, test logs, and traces live, for how long, and which are safe to publish to GitHub?
9. **Browser/computer-use boundary.** Is browser automation only a verification harness, or may it implement configuration and deployment changes too?
10. **Compatibility target.** Build OpenCode v2 only first, or carry v1 from day one? V2-only is recommended because the official API already covers the required runtime and UI surfaces.

## Suggested first implementation slice

The smallest slice that proves the product is not “just skills” is:

1. an OpenCode v2 package with server + TUI + RPC exports;
2. `ssk init` to connect a repository and GitHub Project;
3. `ssk grill` to run the decision-tree interview and create one initiative/spec issue;
4. `ssk cards publish` to create foundation/feature issues, Project fields, sub-issue links, and blocker edges;
5. `ssk card claim` to acquire a fenced per-card lease and create an OpenCode worktree/session attempt;
6. hooks that append checkpoint and evidence events;
7. a TUI card panel showing contract revision, lease, attempt, tests/evidence, and next action;
8. `ssk card handoff --to <adapter>` that checkpoints the current attempt and starts a new attempt in another adapter without changing the card identity.

This slice proves installation, real runtime behavior, GitHub portfolio planning, team-safe card ownership, and cross-harness continuation before adding autonomous DAG scheduling or elaborate model-cost optimization.
