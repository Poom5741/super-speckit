---
description: Obtain command-backed repository and feature state before or after an autonomous workflow stage.
---

Run `python3 scripts/super_speckit.py status --repo . --feature <id> --strict` and `python3 scripts/super_speckit.py validate --repo .`. Read the real `.super-speckit/state/work-state.yml` index and its per-feature JSON records. Use their command/file evidence—not chat history—to determine feature state, candidate SHA, matrix availability, validation status, Git commit, dirty worktree, and worktree inventory.

Run this before every material stage and after every material mutation. A failed strict status or validation check routes to diagnosis/recovery; it does not become an assertion that the state is fine. Preserve the result in the stage receipt or proof pack, redacting only secrets.
