# Example — FEATURE-042: Edit a farmer profile

1. Native Spec Kit artifacts define R-001: an admin can edit a farmer's phone number and it persists after reload; R-002: an unauthorised user cannot edit it.
2. `super-speckit.matrix` maps R-001 to Playwright edit/reload plus an API/DB query, and R-002 to a second browser context/API assertion.
3. Maker works in `ss/feature/FEATURE-042`, adds unit tests and commits `abc123…`.
4. Checker receives only `abc123…`, creates `ss/qa/FEATURE-042-QA-001`, resets its seeded database, and runs lint/unit/integration/build. It starts the app, records a Playwright trace for edit/reload, and verifies the persisted phone value through the approved API/DB assertion.
5. Exploration finds the save button remains enabled after a 401 refresh. Checker repeats it twice with fresh sessions; it reproduces. `BUG-117` links the trace/log, R-002, and exact steps.
6. A bug maker uses `ss/bug/BUG-117`, adds a regression test, commits a candidate; a new checker repeats the failure path from a fresh QA worktree. Pass + completed OCR triage means the summary may say `ready-for-human-merge`.

If the database assertion could not run because its safe test endpoint was unavailable, R-001 would be `not-verified`, the summary would be `not-ready` (if required) or explicitly carry that exception—never silently pass.
