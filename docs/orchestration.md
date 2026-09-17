# Orchestration rules

## 1. Native Spec Kit stays authoritative

Run native `specify`, `plan`, `tasks`, and optionally `clarify`, `checklist`, `analyze` first. Translate each testable requirement into `verification-matrix.md`; update the native plan/tasks if the matrix exposes missing work. `converge` is run after verification to record remaining scope.

## 2. Maker lane

Coordinator allocates one branch/worktree per dependency-ready feature. The maker implements only the selected task slice, adds targeted tests, updates the matrix's proposed assets, runs local checks, and commits a candidate SHA. Makers do not self-certify QA.

## 3. Checker lane

Coordinator creates `ss/qa/<feature>-<run>` from the candidate SHA. Checker resets test data, generates unique identities/namespaces, runs deterministic gates, starts the app, then executes matrix journeys and needed API/DB assertions. Exploratory QA is a separate timeboxed charters: happy path, empty/error states, authorization, responsive/keyboard, and changed boundary conditions as applicable. The checker writes only QA artifacts.

## 4. OCR lane

OCR runs on the same candidate commit (before or alongside runtime QA). Triage records outcome/rationale; `fix` re-enters maker work. OCR answers “does the code have a static concern?”, not “does the app work?”

## 5. Bug loop

No durable bug is created from one ambiguous observation. Preserve evidence, reproduce using the smallest path, then classify. A confirmed bug is a persistent artifact (and optionally a linked issue). A different maker fixes it in `ss/bug/<bug>`, adds regression coverage, and commits. A checker who did not make the fix retests in a new QA worktree. Repeat until verified or explicitly blocked/wont-fix by authorized decision.

## 6. Merge decision

The coordinator validates the state and renders `summary.md`. It may recommend `ready-for-human-merge`; a human or explicitly authorized CI policy merges. QA worktrees are cleaned only after evidence retention rules are met.

## Parallelism

Features may run in parallel only when their task dependencies and test data namespaces do not overlap. QA is per committed candidate, never a shared mutable staging checkout. Queue integration/merge candidates when their changes conflict or their test environments are not isolated.
