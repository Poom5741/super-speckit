## Independent verification

Changes SHALL be specified, planned, and task-broken using native Spec Kit artifacts. A feature is not merge-ready merely because code review, OCR, or unit tests pass. Each requirement SHALL map to verification evidence or an explicit `not-verified`/`not-applicable` rationale. Candidate commits SHALL be checked in an independent clean QA worktree. Confirmed defects SHALL receive durable bug artifacts, regression coverage when practical, and independent retest before closure.

## Native feedback loops

Before any material implementation, the orchestrator SHALL discover and run the cheapest real feedback loop available for the changed behavior. Tests use red-green development at an agreed public seam when possible. Other work SHALL use an equivalent observable loop such as API/DB assertions, browser or visual checks, trace replay, simulator, fixture, differential, performance, or bounded human observation. A successful command exit, static analysis, or source reading alone is not proof. Missing feedback capability is a tracked engineering gap, not permission to guess.
