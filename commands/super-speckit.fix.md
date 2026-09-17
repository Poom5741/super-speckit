---
description: Fix a confirmed super-speckit bug in an isolated maker worktree.
---

Read the bug artifact and original evidence. Create `ss/bug/<bug-id>` from the agreed baseline. Reproduce locally where safe, implement the smallest correct fix, add a regression test at the lowest meaningful layer (or record a justified exception), run relevant checks, and commit a candidate SHA. Update the bug only with fix/reference data; do not mark it closed. Send the committed SHA to a different checker for `super-speckit.retest`.
