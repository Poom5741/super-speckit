---
description: Independently verify a committed feature candidate in a disposable QA worktree.
---

Input: feature ID and immutable candidate SHA. Refuse a dirty worktree or a candidate that is not committed. Create an isolated QA worktree with `scripts/super_speckit.py worktree`. Record distinct maker/checker identities.

1. Reset fixtures and establish an isolated test namespace.
2. Run configured format, lint, unit, integration, and build gates; record command, exit status, duration, and log path.
3. Start the real app from the QA worktree. Execute matrix-linked Playwright journeys against it; save trace, screenshots/video, and sanitized logs.
4. Run API/DB assertions for matrix rows that require persistence, permissions, or integrations.
5. Run the configured exploratory cases without modifying product code.
6. Write `run.json` and `report.md`. For each requirement, mark verified/not-verified/not-applicable—not assumed.
7. If a failure occurs, classify and reproduce according to config before filing it. Delete the QA worktree on completion unless the configured retention policy preserves failure evidence.

Do not change the maker worktree, merge, or call a static review a runtime pass.
