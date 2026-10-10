# Playbook-led delivery contract

## One coordinator and one plan

`ask-super-speckit` selects and executes a pinned PStack playbook through the adapter. Keep its ordered steps, evidence, and explicit skip reasons in a single persisted playbook. Spec Kit is a planning tool selected by scope, not a second coordinator. Canonical feature state remains the only candidate/proof authority.

Choose micro for bounded fixes or mechanical refactors with known behavior and no uncertain cross-boundary design. Put `playbook.md` beside the verification matrix; include the user's outcome and non-goals, acceptance requirement IDs, ordered steps and dependencies, selected source, done predicate, research, architecture constraints, review, and evidence. Micro does not require native spec/plan/tasks, Spec Grill, Atlas, or Change Story. Escalate to normal before implementation when investigation exposes unclear requirements, new product behavior, security-sensitive design, or cross-boundary uncertainty. Normal and milestone work use native spec.md, plan.md, tasks.md, Spec Grill, and evidence-linked understanding artifacts. For milestones use demoable verified slices. Read-only requests create no delivery state.

Use the existing user instruction as purpose confirmation when it explicitly establishes the outcome; retain the actual text and provenance. Ask only for genuinely missing product intent. Never invent confirmation or require a second approval for an already approved plan.

## Research and architecture before code

Every task inspects the actual flow, callers, state owners, installed dependencies, language idioms, and project conventions. Check current primary documentation for unfamiliar APIs, framework behavior, security constraints, or consequential architecture choices. Record sources, relevance, choice, and uncertainty in the active playbook or native plan. Stable mechanical edits may cite local code and installed documentation; do not require an unrelated web search. Compare designs or run a small experiment when evidence cannot settle a boundary.

Adopt Dune's general rules through a project-specific architecture contract: make the normal path easy; mechanically reject forbidden dependencies; name one owner for every durable value; keep feature additions locally contained; make exceptions narrow and explicit. Record allowed dependency directions, public interfaces, state writers, boundary validation, and executable checks. Do not impose desktop-specific Host/Client concepts, CQRS, or a new framework on unrelated projects. Validate a forbidden example fails and a valid path passes before calling a new rule enforced. Treat weakening checks or adding exceptions as architecture review work.

## One writer and independent candidates

Use the user's existing checkout with one code-writing owner. Do not reset, stash, or commit unrelated user changes. Read-only investigation/review can run concurrently; coupled code and canonical state each have one owner. Separate branches in the same directory do not isolate concurrent writers. Parallel makers need explicitly selected separate clones or existing worktrees; otherwise sequence them.

Commit the candidate before independent QA. Use `qa-clone --path <outside-path> --ref <candidate-sha>` for a disposable local clone, then `transition ... --checkout <path> --attempt-id <id>`. Start the app from that clone with isolated test data. Checker identity must differ from maker; checker cannot edit product code. A new candidate invalidates old proof. Worktree commands/receipt keys remain compatibility interfaces, not the default. A checkout is process isolation, not an OS security sandbox.

## Two acceptance gates

Product acceptance uses the real running candidate and complete user journeys. Verify the primary task, discoverability, feedback, validation/recovery, relevant empty/loading/error states, authorization, persistence after reload/restart, keyboard and relevant screen sizes. Capture observations and evidence. Explain justified non-applicable coverage. Use API/DB assertions when UI alone cannot prove effects. An automated green suite cannot replace this journey assessment. Preserve the existing independent Journey UX contract for UI changes, including its blocked/unverified outcomes.

Engineering acceptance reviews the same candidate for correctness, idiomatic language use, clear naming/ownership, dependencies, coupling, duplication, error handling, boundary validation, and maintainability. Run configured types/schema, architecture, lint, build and behavior checks. Keep concrete review findings/dispositions in the proof pack; reviewer proposes and maker fixes. Never rewrite solely for stylistic preference or add abstraction to meet an imagined clean-code standard. Static review cannot close runtime rows. Usability checks demonstrate the declared scope, not product fit or absence of every bug.

## Unattended runs

Select autonomous-run for one long task and figure-it-out for an unfamiliar multi-phase task. Before departure persist outcome, scope, authority, predicate, dependencies, steps, budget, checkpoint path, and recovery rules. Record the actual supported wake/runner mechanism and observe a resume check before promising unattended continuation. Cursor /loop is host-specific; other hosts need their own reviewed mechanism. Without one, continue the active session and report unattended resume as unavailable. Never silently create an automation or claim copied playbooks are a working service.

Each iteration inspects canonical state and Git, makes the smallest evidence-backed advance, verifies a unit, commits useful work, and appends a decision/checkpoint. Diagnose failures, repair verifiers separately, retain failed trials, and pivot with new evidence within the declared budget. Preserve the original predicate. On interruption resume from actual state, not recollection. External blockers carry evidence and a resume condition. Stop on completion, explicit pause, exhausted budget, or a real external block. The handback reports artifact/commit, predicate result, user journeys, engineering checks, decisions, and unresolved limitations. Publish/deploy/merge only within granted authority.

## Executable receipts

Register new deliveries with create-feature --playbook-led. Before maker_running, use record-prerequisite for baseline-feedback, phase-contract, research and architecture with nonempty evidence files. For micro, phase-contract may point to the active playbook. Receipts freeze file digests; update a changed receipt before continuing. Compact micro playbooks also opt into these gates automatically.

Before ready_for_merge record-prerequisite engineering-review with a JSON file containing candidate_sha, checker, status="passed", blocking_findings=[] and concrete review evidence/dispositions. The validator binds its digest, exact candidate and independent checker. This is an accountable checker attestation, not proof of an unseen review. Real review and journey execution remain required by the skill. Legacy feature records preserve their original contract; normal/milestone records use the flag to enable these gates.
