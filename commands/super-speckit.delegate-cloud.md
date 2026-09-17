---
description: Delegate a bounded research, maker, or bug-fix slice to Codex Cloud through a verified super-speckit handoff pack.
---

Require `delegation.enabled`, a configured `codex_cloud_environment_id`, committed base SHA, phase contract, and redacted durable handoff. Only allowed roles may be delegated. Create `cloud-task.md` from the template, with one bounded outcome and exact artifact paths. Do not delegate independent release approval.

For Codex Cloud, submit only the generated pack text:

```bash
codex cloud exec --env <environment-id> --branch <base-branch> "$(cat <cloud-task.md>)"
```

Persist returned task ID in feature state/handoff. On completion, inspect `codex cloud diff <task-id>` and create a local candidate branch or worktree deliberately. Do not run `codex cloud apply` into the integration checkout. After application, run a new independent QA worktree and normal Super-SpecKit gates. A cloud task can make code; it cannot certify its own work.

Centillex Desk is an optional local transport. Only invoke its configured command after generating the same redacted pack; record its pack ID and receiver identity. It is transport, not evidence.
