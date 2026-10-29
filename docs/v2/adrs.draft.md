# Super-SpecKit V2 architecture decision register

Status: proposed as a set; conversation decisions are recorded, but each ADR becomes accepted only after this artifact is reviewed.

## ADR-001 — Progressive enhancement, not an OpenCode-only fork

- Decision: retain portable method/skills and add a shared Runtime plus premium OpenCode Mission Control.
- Alternatives: skills only; OpenCode-only rewrite; independent products.
- Consequences: more adapter work, but one card/evidence model and graceful opt-out.
- Revisit when: portable mode prevents a required Runtime guarantee or OpenCode cannot expose a stable plugin contract.

## ADR-002 — GitHub owns work intent by field

- Decision: GitHub Issues/Projects own active card contract, revision, priority, assignment, dependency and status. Repository files own technical contracts. Runtime owns live attempts and leases.
- Alternatives: `.super-speckit/` owns everything; hosted database owns everything; dual mutable truth.
- Consequences: PM and ordinary developer workflows remain native; sync needs explicit field ownership and revision fencing.
- Revisit when: GitHub APIs cannot represent a required contract or atomic transition.

## ADR-003 — Provider-neutral attempts and handoffs

- Decision: OpenCode, Herdr, ADE, browser providers and ordinary contributors create attempts under one card identity. Handoffs freeze a checkpoint and start a new attempt.
- Alternatives: transfer provider chat/session as canonical state; one harness only.
- Consequences: more schema discipline; no provider lock-in; interrupted work is recoverable.
- Revisit when: a provider-neutral field cannot preserve a demonstrated critical capability.

## ADR-004 — Permanent roles, ephemeral sessions, adaptive parallelism

- Decision: roles are stable UI/configuration identities; sessions activate only on the dependency frontier. One writer owns a coupled card/worktree.
- Alternatives: five always-running agents; single agent for every task; unrestricted shared writers.
- Consequences: lower idle cost and collision risk; scheduler must measure when parallelism helps.
- Revisit when: dogfood metrics show role setup costs exceed saved wall time.

## ADR-005 — Local-first execution with WSL-native Windows worktrees

- Decision: V1 continues while at least one owned host is online. Windows UI may delegate through typed RPC to a persistent WSL runner using WSL-native worktrees. macOS/Linux run natively.
- Alternatives: `wsl.exe` per command; `/mnt/c` heavy execution; hosted-first compute.
- Consequences: faster, more reliable execution; Git/GitHub synchronize distinct checkouts.
- Revisit when: a safe hosted worker is proven or WSL-native worktrees obstruct required Windows tooling.

## ADR-006 — Two readiness gates

- Decision: distinguish Feature Delivery Ready from Production Release Ready.
- Alternatives: one ambiguous “Foundation done” state.
- Consequences: feature delivery begins early without overstating release safety; production capability work remains visible.
- Revisit when: a project archetype legitimately has no external release boundary.

## ADR-007 — External provider boundaries

- Decision: Herdr and ADE remain optional peer installations; Cloudflare Browser Run is a browser provider. Super-SpecKit does not fork or embed ADE Runtime in V1.
- Alternatives: make ADE/Herdr mandatory; copy their runtime; use Cloudflare Browser Run as a general computer.
- Consequences: lower licensing and maintenance risk; integration depends on public capability probes.
- Revisit when: a stable SDK offers a materially safer or more complete integration after license review.

## ADR-008 — Repository-safe evidence

- Decision: Git stores typed, redacted evidence descriptors; sensitive raw artifacts stay in controlled local/provider storage.
- Alternatives: commit all logs/recordings; store no evidence.
- Consequences: public/private repositories remain safe and auditable; artifact retention and access must be managed.
- Revisit when: a project explicitly requires an approved encrypted in-repository artifact format.

## ADR-009 — Open core and proposed Apache-2.0 licensing

- Decision: open the protocol, portable skills, local Runtime, OpenCode plugin and basic adapters; reserve future hosted/enterprise operations for commercial delivery. Apache-2.0 is the candidate license for newly authored code pending audit.
- Alternatives: proprietary product; AGPL core; MIT-only.
- Consequences: adoption and commercial integrations are easier; dependency notices and boundaries require continuous review.
- Revisit when: legal inventory, contributor strategy or commercial model recommends another license.

## ADR-010 — Evidence-backed self-improvement

- Decision: project lessons may produce method changes only as reviewable pull requests with evidence, applicability, counterexamples, blast radius and evaluation fixtures.
- Alternatives: silent self-modification; no learning.
- Consequences: the operating system improves without erasing accountability or leaking client data.
- Revisit when: a formally sandboxed auto-accept class is demonstrated safe.
