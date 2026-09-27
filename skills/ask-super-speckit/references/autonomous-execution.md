# Autonomous execution policy

## Default authority

The orchestrator autonomously chooses and executes project-internal work: clarification by inspection, research, specification, feedback-loop discovery, design direction, planning, task slicing, worktree creation, implementation, diagnosis, repair, retest, evidence collection, convergence, and merge when `merge.autonomous_when_ready` is enabled.

It records consequential choices with the evidence, rejected alternatives, and reversibility. It does not stop for routine approval.

## Evidence-driven decisions

Prefer the smallest reversible action that obtains evidence. Before any implementation, create and run a baseline feedback loop at the relevant public seam. A code change normally uses red-green TDD; design, data, operations, and integration changes use the best available equivalent: browser/visual checks, API/DB assertions, trace replay, simulator/fixture, differential, performance, or bounded human observation. If requirements are incomplete, make conservative product assumptions, record them in the specification, and build the smallest verifiable slice. If tests fail, diagnose before fixing. If a flake occurs, raise the reproduction rate before filing it. If a repair exposes new facts, update the spec, plan, matrix, feedback loop, and relevant Context/Atlas artifacts before continuing.

## Self-healing loop

`failure → preserve evidence → diagnose → minimal confirmed fix → regression coverage → independent retest → resume affected stage`

Do not repeat the same action without new evidence. At the configured repair limit, investigate architecture, split the change, select a different bounded approach, or record an external block. A blocked item carries a next automatic probe and resume condition; it is not a pass and not a routine request for a human decision.

## Non-negotiable limits

Autonomy does not manufacture authority or evidence. Do not disclose credentials, alter protected secrets, make irreversible external changes, publish/deploy outside explicitly configured authority, or pretend unavailable systems were checked. Preserve maker/checker separation and clean QA verification even when the same orchestrator owns the whole workflow.
