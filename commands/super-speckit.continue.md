---
description: Resume one shared Super-SpecKit task on another machine from the rolling continuation YAML record.
---

Use this when opening the same repository on Pi, a server, or a different local machine. The user invokes `$ask-super-speckit`; it reads `.super-speckit/continuation.yml` automatically. This is a single rolling record, not a chain of handoff documents.

Before resuming, pull the shared branch, run `python3 scripts/super_speckit.py status --repo . --feature <feature> --strict` and `python3 scripts/super_speckit.py validate --repo .`, then compare Git HEAD, candidate SHA, feature state, and evidence paths with the continuation. A mismatch is a recovery task; do not blindly continue a stale task.

After every material stage, update the same record with:

`python3 scripts/super_speckit.py continuation <feature> --stage <stage> --next-action "..." --candidate-sha <sha-if-known> --worktree <path-or-branch> --evidence <path> --unknowns "..." --repo .`

Commit and push the continuation with its related state/artifacts. It records the current objective, exact next action, immutable SHA when available, branch/worktree, evidence, and unknowns. Use a separate transfer handoff only when moving to a cloud vendor or when the receiving environment needs an authority boundary beyond this shared repository.
