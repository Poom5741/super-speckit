---
description: Prepare an isolated maker worktree for a Spec Kit feature.
---

Confirm native `spec.md`, `plan.md`, `tasks.md`, and a verification matrix exist. Allocate a feature ID, maker, independent checker, branch and worktree. Create state with `create-feature`; make the maker worktree from the integration baseline, not from another worktree. Move state to `maker_running`. The maker may implement and commit but must not claim final QA or modify QA evidence.
