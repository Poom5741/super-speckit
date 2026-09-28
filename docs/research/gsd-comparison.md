# GSD comparison: what to adopt without losing Super-SpecKit's guarantees

Researched 2026-09-28 against GSD-owned public repositories and documentation only. This is a design input, not a vendored workflow.

## Scope and provenance

The original [`gsd-build/get-shit-done`](https://github.com/gsd-build/get-shit-done) repository is archived and directs active work to Open GSD's [`gsd-core`](https://github.com/open-gsd/gsd-core). The newer [`gsd-build/gsd-2`](https://github.com/gsd-build/gsd-2) is also a redirect: its current continuation is Open GSD's [`gsd-pi`](https://github.com/open-gsd/gsd-pi). Consequently, historical GSD is useful for its workflow ideas, while GSD Pi is the current implementation to compare against.

## Confirmed GSD strengths

| GSD mechanism | Confirmed behavior | Why it stands out |
| --- | --- | --- |
| Durable project memory | Historical GSD's planning tree separates project vision, requirements, roadmap, state, research, brownfield maps, phase plans, summaries, verification, UI review, and UAT. [Architecture](https://github.com/gsd-build/get-shit-done/blob/main/docs/ARCHITECTURE.md) | It turns a long conversation into legible project artifacts rather than relying on a context window. |
| Living position record | Its `STATE.md` is read at workflow start and records current position, decisions, blockers, and resume context. [State template](https://github.com/gsd-build/get-shit-done/blob/main/get-shit-done/templates/state.md) | A later agent can continue work without reconstructing intent from chat. |
| Plan quality loop | `plan-phase` has researcher, planner, and plan-checker roles, with a bounded revision cycle; plans are the execution contract. [Plan workflow](https://github.com/gsd-build/get-shit-done/blob/main/get-shit-done/workflows/plan-phase.md) | This is the most relevant precedent for a self-grilling spec: the critic is structurally distinct from the author. |
| Scope-sized workflow | Historical GSD documents quick/fast/full modes, rather than making every small task bear full planning overhead. [Features](https://github.com/gsd-build/get-shit-done/blob/main/docs/FEATURES.md) | It preserves momentum for trivial work while keeping a route to deep planning. |
| Assumption-first discovery | Discussion can produce confidence-labelled assumptions from the codebase, asking a person to correct errors rather than answer every question. [Configuration](https://github.com/gsd-build/get-shit-done/blob/main/docs/CONFIGURATION.md) | Closely matches Super-SpecKit's intended human gate: correct purpose, not technical trivia. |
| Reassessment and milestone validation | GSD Pi defines a milestone → demoable vertical slice → task hierarchy; after each slice it reassesses the roadmap, and after all slices it checks milestone success criteria. [Project structure](https://github.com/open-gsd/gsd-pi/blob/main/gitbook/core-concepts/project-structure.md) | It treats the plan as a living hypothesis and checks the delivered outcome, not merely task completion. |
| Stateful autonomous control plane | GSD Pi supports auto and step modes, Git worktrees, resumable sessions, a headless JSON query, and local project state with readable projections. [README](https://github.com/open-gsd/gsd-pi/blob/main/README.md), [step mode](https://github.com/open-gsd/gsd-pi/blob/main/gitbook/core-concepts/step-mode.md) | It makes orchestration observable and interruptible, instead of a black-box autonomous run. |
| Cost and failure policy | GSD Pi documents per-phase/slice cost tracking, budgets, timeout handling, and a distinction between a failed runnable check and an inconclusive missing command. [Cost management](https://github.com/open-gsd/gsd-pi/blob/main/gitbook/features/cost-management.md), [preferences](https://github.com/open-gsd/gsd-pi/blob/main/gitbook/configuration/preferences.md) | This is a practical model for autonomy that does not silently burn budget or treat unavailable tooling as a pass. |
| Context packets | GSD's sibling [`context-packet`](https://github.com/gsd-build/context-packet) uses file-based JSON DAG packets with execution dependencies distinct from data-consumption edges, input hashes, token-budgeted resolution, and same-level parallelism. [README](https://github.com/gsd-build/context-packet/blob/main/README.md) | This is a concrete, lightweight interpretation of the proposed “knowledge as nodes” idea. |

## Comparison with Super-SpecKit today

Super-SpecKit already keeps the parts GSD does **not** make central:

- Native Spec Kit `spec.md`, `plan.md`, `tasks.md`, and convergence remain the requirements backbone.
- A confirmed Purpose Map gives a human one meaningful gate: intended outcome, affected people, success signal, and non-goals.
- The Builder / Examiner / Investigator / Resolver Spec Grill labels claims `proven`, `inferred`, `assumed`, or `unknown` and returns to the purpose gate only for a purpose-level conflict.
- Feature makers and independent clean QA worktrees are distinct. Runtime Playwright/API/DB evidence, exploratory QA, flake reproduction, and regression obligations prevent an implementer from grading their own work.
- YAML state is validated by command against native artifacts and Git; it is deliberately not agent memory. OCR is a separate static-review lane, never runtime proof.

GSD is stronger today at **productizing continuity and operating ergonomics**: a readable project ledger, scope-sized routes, bounded critic loops, explicit reassessment, session recovery, cost controls, and a visual control plane. Super-SpecKit is stronger at **trust boundaries**: purpose confirmation, evidence provenance, clean independent runtime QA, and no self-certifying merge.

## Compatible adoptions

1. **Project Atlas + phase ledger (first).** Add a stable, committed, diagram-first project surface: purpose, bounded architecture map, requirement IDs, component contracts, decisions, risks, and links to evidence. Generate a small current-state digest from existing YAML/Spec Kit files; never make prose the authoritative execution state.
2. **Grill as a bounded planner/checker loop.** Make the Spec Grill explicitly use research → builder → examiner → investigator → resolver, with a maximum revision count and an “evidence or uncertainty label” exit rule. This takes GSD's quality loop but preserves the Purpose Gate.
3. **Task-size router.** Let `ask-super-speckit` classify a request as micro, normal, or milestone. Micro work may use a compact purpose/grill/matrix; normal work uses the present flow; milestones get slice/reassessment/audit artifacts. Classification must be evidence-backed and upgrade to a deeper route when risk rises.
4. **Reassessment after each verified slice.** Compare what was learned in implementation and independent QA to the roadmap, then explicitly keep, split, reorder, defer, or cancel remaining slices. Preserve requirement IDs and the reason for any change.
5. **Control-plane hardening.** Add machine-readable attempt IDs, bounded retries, explicit `inconclusive` evidence for unavailable tools, resume receipts, time/token budgets, and deterministic next-action output. These are orchestration safeguards, not permission to infer success.
6. **Knowledge packets (experimental).** Implement a file-backed graph node schema with stable IDs, `depends_on` versus `consumes` edges, source links, input/content hashes, confidence, and a token budget. Render Mermaid from the schema. Start with project/feature/component/contract/test/evidence/decision nodes; do not introduce a GraphRAG service or database in v1.

## Conflicts and non-adoptions

| GSD pattern | Why not adopt it as-is |
| --- | --- |
| Replace Spec Kit artifacts with `.planning/` or `.gsd/` | Super-SpecKit is a companion, not a replacement. Duplicated plans would drift; keep Spec Kit canonical and add projections/links. |
| Markdown or a local database as unchecked state authority | Super-SpecKit's direction is command-checked YAML plus native Git/artifact evidence. Readable Atlas pages may be projections, never proof by themselves. |
| One worktree per milestone as both implementation and verification environment | It conflicts with independent, ephemeral QA. A candidate must still be verified from an immutable SHA in a freshly prepared QA worktree. |
| Generic approval pauses | The user requested autonomy. Retain the purpose-only human gate and escalate only unresolvable product/safety choices. |
| Auto-fix retries as evidence of correctness | Retrying can be useful, but a final pass needs saved command/runtime evidence; flakes must still reproduce before becoming bugs. |
| Full GSD runtime, provider routing, database, web UI, or Cloud daemon | These solve a different product problem and would turn this portable skill set into a competing agent platform. Integrate through small adapters only if a project already uses GSD Pi. |

## Staged recommendation

**Stage A — adopt now:** bounded Spec Grill contract, project/phase ledger templates, micro/normal/milestone routing, reassessment record, and `inconclusive` evidence semantics. These are low-risk extensions to existing files and validate the core learning goal.

**Stage B — prove value:** add an Atlas generator that reads repository facts and produces a compact HTML/Markdown/Mermaid Change Story before implementation. Require an agent to update only affected component context cards and verify links/hashes. Test it on a brownfield feature.

**Stage C — optional scale-out:** introduce the typed packet graph and deterministic digest resolver. Measure whether it reduces repeated exploration and token use without missing relevant constraints. Keep a file-only fallback.

**Stage D — only on demonstrated need:** a dashboard, richer session recovery, or a GSD Pi adapter. These should consume Super-SpecKit's evidence ledger, not replace the purpose gate or independent checker lane.

The north star is not “make non-developers write code faster.” It is to let them own **purpose, trade-offs, and evidence of outcome**, while the system makes engineering knowledge inspectable through maps, contracts, tests, and independent verification. That is the useful bridge from vibe coding to durable product development.
