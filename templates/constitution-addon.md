## Independent verification

Changes SHALL be specified, planned, and task-broken using native Spec Kit artifacts. A feature is not merge-ready merely because code review, OCR, or unit tests pass. Each requirement SHALL map to verification evidence or an explicit `not-verified`/`not-applicable` rationale. Candidate commits SHALL be checked in an independent clean QA worktree. Confirmed defects SHALL receive durable bug artifacts, regression coverage when practical, and independent retest before closure.
