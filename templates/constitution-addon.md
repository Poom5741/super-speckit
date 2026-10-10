## Independent verification

Changes SHALL follow a persisted PStack playbook. Normal/milestone work SHALL use native Spec Kit specification, plan, and tasks; bounded micro work SHALL use a compact playbook and requirement matrix. A feature is not merge-ready merely because code review, OCR, or unit tests pass. Each requirement SHALL map to verification evidence or an explicit `not-verified`/`not-applicable` rationale. Candidate commits SHALL be checked in an independent clean QA clone or explicitly selected worktree. Confirmed defects SHALL receive durable bug artifacts, regression coverage when practical, and independent retest before closure.

## Native feedback loops

Before any material implementation, the orchestrator SHALL discover and run the cheapest real feedback loop available for the changed behavior. Tests use red-green development at an agreed public seam when possible. Other work SHALL use an equivalent observable loop such as API/DB assertions, browser or visual checks, trace replay, simulator, fixture, differential, performance, or bounded human observation. A successful command exit, static analysis, or source reading alone is not proof. Missing feedback capability is a tracked engineering gap, not permission to guess.

## Purpose and adversarial understanding

Before technical implementation begins, the intended outcome, affected people, success signal, and non-goals SHALL be human-confirmed in a Purpose Map. For normal/milestone scope a separate evidence-labeled Spec Grill SHALL challenge the resulting spec; agents may resolve technical questions autonomously but SHALL return to the Purpose Gate when discovery would materially alter the confirmed purpose.

## Architecture and engineering acceptance

Every delivery SHALL inspect relevant local structure and language/framework guidance before choosing its implementation. New playbook-led deliveries SHALL retain research and architecture receipts, executable project-specific boundaries, durable-state owners and narrow exceptions. Release SHALL require independent engineering review of the exact candidate and real user-journey evidence. Green tests alone SHALL NOT establish usability. One code writer SHALL own each checkout. Unattended continuation SHALL require an observed host runner, persisted predicate, authority, budget and checkpoints.
