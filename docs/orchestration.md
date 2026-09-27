# Orchestration rules

## 1. Native Spec Kit stays authoritative

The autonomous orchestrator runs native `specify`, `plan`, `tasks`, and optionally `clarify`, `checklist`, `analyze` as evidence requires. Translate each testable requirement into `verification-matrix.md`; update the native plan/tasks if the matrix exposes missing work. `converge` is run after verification to record remaining scope.

## 1.1 Files and commands are the work-state authority

Conversation is never a state store. Before and after every material stage, the orchestrator runs the configured `status` and `validate` commands, then reads the real `.super-speckit/state/work-state.yml` index, per-feature JSON, native artifacts, proof pack, and Git state they identify. The resulting command receipt—not an agent summary—decides whether a stage may advance. A mismatch, missing artifact, dirty unexpected worktree, or invalid state routes to recovery and is recorded as evidence.

## 2. Feedback loop before work

Before changing production code, configuration, data behavior, or UI, the autonomous orchestrator creates a feedback-loop receipt. It searches existing project tools and selects the smallest public-seam signal that can distinguish correct from incorrect behavior. Use red-green TDD for code where a test seam exists; otherwise use API/DB assertions, browser/visual evidence, replay, fixtures, simulator, property/fuzz, differential, performance, or bounded human observation. Source inspection, a clean exit status, and static review alone are never sufficient.

## 3. Maker lane

Coordinator allocates one branch/worktree per dependency-ready feature. The maker implements only the selected task slice, adds targeted tests, updates the matrix's proposed assets, runs local checks, and commits a candidate SHA. Makers do not self-certify QA.

## 4. Checker lane

Coordinator creates `ss/qa/<feature>-<run>` from the candidate SHA. Checker resets test data, generates unique identities/namespaces, runs deterministic gates, starts the app, then executes matrix journeys and needed API/DB assertions. Exploratory QA is a separate timeboxed charters: happy path, empty/error states, authorization, responsive/keyboard, and changed boundary conditions as applicable. The checker writes only QA artifacts.

## 5. OCR lane

OCR runs on the same candidate commit (before or alongside runtime QA). Triage records outcome/rationale; `fix` re-enters maker work. OCR answers “does the code have a static concern?”, not “does the app work?”

## 6. Bug loop

No durable bug is created from one ambiguous observation. Preserve evidence, reproduce using the smallest path, then classify. A confirmed bug is a persistent artifact (and optionally a linked issue). A different maker fixes it in `ss/bug/<bug>`, adds regression coverage, and commits. A checker who did not make the fix retests in a new QA worktree. Repeat until verified or explicitly blocked/wont-fix by authorized decision.

## 7. Autonomous merge decision

The coordinator validates the state and renders `summary.md`. When autonomous merge is enabled, it merges a verified candidate and records the resulting SHA. QA worktrees are cleaned only after evidence retention rules are met.

## Parallelism

Features may run in parallel only when their task dependencies and test data namespaces do not overlap. QA is per committed candidate, never a shared mutable staging checkout. Queue integration/merge candidates when their changes conflict or their test environments are not isolated.
