---
description: Fix a confirmed bug through the active playbook and independent retest.
---

Read the bug and original evidence. The single code-writing owner reproduces and fixes it in the current checkout, preserves unrelated changes, adds a regression check or justified exception, and commits a new candidate. Do not close the bug from maker checks. A distinct checker retests the new SHA in a fresh standalone QA clone. Optional separate clones/worktrees are allowed for explicitly isolated parallel makers.
