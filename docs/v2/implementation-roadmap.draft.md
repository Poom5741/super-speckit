# Super-SpecKit V2 implementation roadmap

Status: draft. Phases are evidence gates, not date promises.

## Delivery principles

- Preserve V1 behavior and historical meaning throughout migration.
- Build contracts before provider adapters or visual polish.
- Prove one vertical journey per phase through the public seam.
- Keep one writer per coupled card; parallelize only dependency-independent cards.
- Test provider absence and interruption, not only happy paths.
- Treat `whitelabels-cex` as the adoption and migration proof.

## Phase 0 — Baseline and legal/compatibility audit

Outcome: a frozen current-system baseline and safe implementation envelope.

- Inventory current schemas, installer surfaces, state, host discovery and licenses.
- Pin a testable OpenCode V2 revision/API and define compatibility probes.
- Decide public package boundaries and complete ADE/third-party license review.
- Capture current `whitelabels-cex` GitHub/repository/state snapshot without secrets.

Gate: current tests pass; V1 install/upgrade is reproducible; no V2 code begins with an unknown licensing or compatibility blocker.

## Phase 1 — Provider-neutral Foundation

Outcome: card/attempt/lease/checkpoint/evidence/handoff contracts work without a UI.

- Add versioned schemas and atomic runtime ledger.
- Add migration preview, backup and rollback.
- Add secret-safe artifact descriptors, budgets and cancellation state.
- Add GitHub contract-revision fingerprint and field-ownership protocol.
- Prove stale writer, duplicate completion, ambiguous cancellation and interrupted handoff fixtures.

Gate: CLI fixture imports a V1 project, claims a card, checkpoints, hands off, rejects stale completion and restores without history loss.

## Phase 2 — OpenCode Mission Control vertical slice

Outcome: installing the plugin visibly transforms OpenCode.

- Server plugin, shared RPC and supervised background service.
- TUI home, card detail, agent lane, environment and evidence views.
- Capability discovery and degradation explanations.
- Coordinator plus Builder/Verifier session lifecycle.
- Quiet notifications and reconnect replay.

Gate: close/reopen the client during a fixture card; the supervised attempt continues and the TUI reconstructs exact state.

## Phase 3 — Cross-platform Environment Runner

Outcome: reliable warm execution on macOS/Linux and Windows/WSL.

- Structured command/process protocol and ownership receipts.
- WSL-resident runner and WSL-native worktrees.
- Container-engine discovery, warm Compose lifecycle, cache/port/test namespace management.
- macOS/Linux native runner.
- Failure diagnosis for bridge, path, permission, port and daemon layers.

Gate: the same reference card passes on a clean macOS host and Windows 11/WSL host; unrelated containers and dirty worktrees survive cleanup.

## Phase 4 — GitHub Portfolio adoption

Outcome: `whitelabels-cex` appears correctly in Mission Control and can continue delivery.

- Import Project cards, dependencies, acceptance discussion and branch context.
- Reconstruct Foundation/Feature gates from repository evidence without inventing facts.
- Reconcile drift among issue, Project, PR and V1 state.
- Implement pivot/revision activation and evidence staleness.
- Import ordinary developer PR/CI contributions.

Gate: owner approves a read-only import diff; one real card is claimed and completed without rewriting historical evidence.

## Phase 5 — Adaptive team and provider handoff

Outcome: parallel work and provider switching reduce elapsed delivery time safely.

- Permanent role roster and dependency-frontier scheduler.
- Multiple isolated card lanes; one writer lease per lane.
- Provider adapter SDK.
- Herdr adapter for terminals, panes, warm environments and SSH machines.
- Handoff acknowledgement, ambiguity fencing and recovery.

Gate: two independent real cards run in parallel; one interrupted Herdr-backed card resumes without duplicate work; metrics compare against the current flow.

## Phase 6 — ADE integration

Outcome: ADE Brain/lanes can execute Super-SpecKit attempts without owning card truth.

- Capability probe and reviewed CLI/RPC boundary.
- Map lane/worktree, automation, proof and cross-machine handoff.
- Redact/describe ADE artifacts without copying credentials or private raw proof into Git.

Gate: one card moves between two owned machines through an idempotent handoff; source and destination attempts remain attributable and recoverable.

## Phase 7 — Cloudflare Browser Specialist

Outcome: a headless SSH coding environment gains guarded, observable web QA.

- Protected per-run preview route and cleanup.
- Browser session, hostname guardrails, synthetic authentication, recording and budget accounting.
- Agent journey plus human Live View takeover/handback.
- Replaceable-session recovery and redacted evidence descriptors.

Gate: a real `whitelabels-cex` web card is tested from a non-graphical Linux host; candidate, recording descriptor, screenshots, result and cleanup are independently verified.

## Phase 8 — Architecture intelligence and greenfield Portfolio

Outcome: start a new repository with evidence-backed architecture and a tested Foundation graph.

- Question ledger separating facts from owner decisions.
- Architecture Researcher evidence schema and freshness.
- Principal Architect quality scenarios, alternatives, tradeoff/threat/operability review and ADRs.
- Universal + domain + project-specific Foundation generator.
- Independent card-readiness review and GitHub publication.

Gate: generate and execute a small greenfield walking skeleton, then re-import it without semantic loss.

## Phase 9 — Public-alpha proof

Outcome: evidence supports an honest alpha claim.

- Three real `whitelabels-cex` card shapes.
- macOS and Windows/WSL.
- Herdr, ADE and Cloudflare paths.
- interruption, card pivot, opt-out contributor and negative gate fixtures.
- accessibility, security, installer, upgrade, license and documentation review.

Gate: independent proof pack satisfies `AC-12`; known limitations are visible in product and release notes.

## Explicitly deferred

Hosted coding with every owned host offline; non-technical PM portal; GitLab/Jira/Linear; enterprise identity; production auto-deploy; cross-client analytics; additional project archetypes; managed commercial control plane.
