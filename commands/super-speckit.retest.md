---
description: Independently retest a confirmed bug fix from a clean QA worktree.
---

Create a fresh QA worktree from the bug-fix candidate SHA. Execute the original minimal reproduction first, then its regression test and affected matrix journeys. Record pass/fail and evidence. On pass, close the bug only after required feature gates and OCR triage remain satisfactory; on fail, reopen `bug_fixing` with a new evidence run. Never reuse the maker environment as retest evidence.
