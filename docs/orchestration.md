# Orchestration rules

## 1. Playbooks lead execution; Spec Kit plans selected scopes

Read `skills/ask-super-speckit/references/playbook-delivery.md` for the current delivery contract. Select and persist a PStack playbook first. Micro fixes and mechanical refactors use playbook.md plus a requirements matrix; normal and milestone work retain native spec.md, plan.md, tasks.md, Spec Grill, Atlas and Change Story. Escalate micro scope when uncertain product or cross-boundary design appears. Read-only requests have no delivery ceremony. Preserve explicit user purpose confirmation and provenance; technical choices remain autonomous.

Before code, record relevant research and a project-specific architecture contract with dependency checks, state ownership, public interfaces and narrow exceptions. Before release, require both independent user-journey evidence and independent engineering review for the exact candidate. Existing state remains compatible; new deliveries use `create-feature --playbook-led` and its research/architecture/review receipts.

## 1.1 Files and commands are the work-state authority

Conversation is never a state store. Before and after every material stage, the orchestrator runs the configured `status` and `validate` commands, then reads the real `.super-speckit/state/work-state.yml` index, per-feature JSON, native artifacts, proof pack, and Git state they identify. The resulting command receipt—not an agent summary—decides whether a stage may advance. A mismatch, missing artifact, dirty unexpected worktree, or invalid state routes to recovery and is recorded as evidence.

## 2. Feedback loop before work

Before changing production code, configuration, data behavior, or UI, the autonomous orchestrator creates a feedback-loop receipt. It searches existing project tools and selects the smallest public-seam signal that can distinguish correct from incorrect behavior. Use red-green TDD for code where a test seam exists; otherwise use API/DB assertions, browser/visual evidence, replay, fixtures, simulator, property/fuzz, differential, performance, or bounded human observation. Source inspection, a clean exit status, and static review alone are never sufficient.

## 2.1 Verification harness and learning loop

Before runtime QA, create or refresh a project-local verification harness and feature map. It documents executable launch/readiness, isolated test data, public seams, evidence, and cleanup; a live smoke path demonstrates the harness is usable. A static review panel is independent and read-only, but cannot satisfy runtime matrix rows or apply its own findings. When the same failure recurs or a severe escape occurs, create corrective enforcement at the first viable layer—architecture, types/schema, static/lint, CI, regression test, documentation—and prove it catches the historical counterexample. For material changes to this kit, an isolated evaluator subagent forward-tests the affected skill against a realistic fixture before any correction is accepted.

## 3. Maker lane

Coordinator assigns one code-writing owner to the current checkout. Sequence dependent slices; parallel writers require explicitly selected separate clones or worktrees. The maker implements only the selected task slice, adds targeted tests, updates the matrix's proposed assets, runs local checks, and commits a candidate SHA. Makers do not self-certify QA.

## 4. Checker lane

Coordinator creates a disposable standalone QA clone outside the maker repository from the candidate SHA with `qa-clone`; optional registered worktrees remain supported. Checker resets test data, generates unique identities/namespaces, runs deterministic gates, starts the app, then executes matrix journeys and needed API/DB assertions. Exploratory QA is a separate timeboxed charters: happy path, empty/error states, authorization, responsive/keyboard, and changed boundary conditions as applicable. The checker writes only QA artifacts.

## 5. OCR lane

OCR runs on the same candidate commit (before or alongside runtime QA). Triage records outcome/rationale; `fix` re-enters maker work. OCR answers “does the code have a static concern?”, not “does the app work?”

## 6. Bug loop

No durable bug is created from one ambiguous observation. Preserve evidence, reproduce using the smallest path, then classify. A confirmed bug is a persistent artifact (and optionally a linked issue). The code-writing owner fixes it in the current checkout, adds regression coverage, and commits. A checker who did not make the fix retests in a new QA clone. Repeat until verified or explicitly blocked/wont-fix by authorized decision.

## 7. Autonomous merge decision

The coordinator validates the state and renders `summary.md`. When autonomous merge is enabled, it merges a verified candidate and records the resulting SHA. QA checkouts are cleaned only after evidence retention rules are met.

## Parallelism

Features may run in parallel only when their task dependencies and test data namespaces do not overlap. QA is per committed candidate, never a shared mutable staging checkout. Queue integration/merge candidates when their changes conflict or their test environments are not isolated.

## PStack integration protocols

Load selected pinned source together with `adapters/pstack/override-contract.md`; the vendor tree never becomes a second coordinator or state store. See `docs/pstack-integration.md` for exact runtime CLI input contracts. Use configured/inherited supported models and adaptive concurrency; unsupported host/model diversity remains an explicit limitation.

Caller-first architecture compares structurally different alternatives; two independent same-shape implementation deviations trigger reassessment. Arena uses identical immutable briefs, frozen isolated outputs and a private judge rubric; swarm declares mode/selection before a verified pilot and bounded rolling refill. Every required partition remains required after dropout. Faithful interrogation uses identical intent/diff/rubric/SHA, preserves lone dissent and records every disposition; lens review is separate.

Launch/Doctor/Drive/Evidence/Cleanup controls remain draft until live smoke and evidence-survival checks. Full verification maintenance drives every declared feature even when documents look current. Performance claims require equivalent tuning, completed work/errors, a measured limiter and five alternating samples per side. Decision trails are append-only, run-bound and audited against available same-run transcripts. Historical correction is structural and distinct from reflection proposals.

Defects, recovery and missing prerequisites precede maker work; an existing candidate awaiting QA precedes another maker slice. Merge needs configured authority, exact candidate behavioral proof and current forge readiness; watcher success or ledger presence alone proves neither verification nor merge. Observe actual merged state. Optional Benny/control UI automation remains dormant until explicitly configured and externally authorized.
