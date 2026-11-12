# Elephant/Goldfish discipline gate inside Super-SpecKit

Read this contract together with the selected pinned skill, loaded through
`python3 scripts/egm_adapter.py read <skill>`. Super-SpecKit owns the pipeline,
canonical state, candidates, QA and release authority. The Elephant/Goldfish
Model (EGM) supplies one mandatory method: **fresh, zero-context review of the
design intent before maker work**. EGM is never a second coordinator, and its
harness plugins/commands are not installed or registered.

## What is enforced, in code

Every feature record created with `gates_contract=discipline-v1` (the
`create-feature` default) must hold a digest-bound `goldfish-review`
prerequisite receipt before `maker_running`, before any new candidate, and at
release. `scripts/discipline_contract.py` validates it; a scripted harness that
only runs the Python CLI is blocked until it exists.

- The receipt binds the repository-relative path and bytes of the design beside
  the matrix. Use `spec.md` for normal/milestone and `playbook.md` for micro,
  with `spec.md` supported for older micro layouts. Changes to the reviewed
  file require a fresh review.
- The receipt binds the pinned `egm-review` skill revision and SHA-256 from
  `vendor/elephant-goldfish`. Follow that protocol when dispatching.
- `harness_subagents` must be declared explicitly. When the harness can spawn
  subagents, **every reviewer must be dispatched as a fresh subagent**
  (`dispatch: "subagent"`, `fresh_context: true`). The validator checks these
  declarations and the integrity of the supplied evidence. Keep the reports
  and actual dispatch records as evidence of the review.
- When the harness truly has no subagents, a disclosed
  `dispatch: "sequential-fresh"` fallback is accepted only as mode
  `goldfish-equivalent`, with digest-bound `capability_absence` evidence, and
  only while `discipline_gates.allow_sequential_fresh_fallback` is true.
  Setting it false makes subagent capability a hard requirement (otherwise the
  feature stays truthfully blocked).
- Findings carry `disposition` (`fixed`, `accepted-risk`, `dismissed`), a
  reason and digest-bound evidence, like lens findings. A `resolution` records
  how they were settled.

## How EGM maps onto this pipeline

- The Elephant role is the existing context holder: `ask-super-speckit`
  investigation, purpose map, Spec Grill and native spec/plan (or playbook)
  drafting. `egm-brainstorm`/`egm-draft` methods may shape the draft; their
  artifacts fold into native intent, never a parallel spec ledger.
- The Goldfish role is the gate: at least `goldfish_min_reviewers` fresh
  reviewers (default 2) receive only the design artifact and its source
  references — no conversation history, no maker rationale. Each reviewer reads
  its pinned persona file from `vendor/elephant-goldfish/agents/` when the
  harness registers named subagent types, otherwise a general-purpose subagent
  reads it first.
- `egm-resolve` discipline governs how findings are fixed or explicitly
  accepted; `egm-review-loop` motivates re-review after intent changes (the
  digest binding enforces this mechanically).
- `egm-bootstrap` and `egm-drift-report` are Atlas-maintenance methods:
  they inform Project Atlas cards and Change Stories; a diagram check never
  proves runtime behavior.
- EGM's artifact-first, plain-English, no-flattery communication rules apply to
  every review report written under this gate.

EGM's disclaimer is preserved: it is not an officially supported Google
product. Inventory coverage does not certify live Google endpoints or plugins.
