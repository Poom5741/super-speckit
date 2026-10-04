---
description: Prepare an isolated maker worktree for a Spec Kit feature.
---

Confirm native `spec.md`, `plan.md`, `tasks.md`, and a verification matrix exist. Allocate a feature ID, maker, independent checker, branch and worktree. Create state with `create-feature`; pass `--ui-change` when the feature changes a user-facing interface so the required Journey UX Loop can be enforced. Make the maker worktree from the integration baseline, not from another worktree. Before implementation, run `super-speckit.ponytail` to choose the smallest safe implementation after understanding the affected flow. Move state to `maker_running`. The maker may implement and commit but must not claim final QA or modify QA evidence.
