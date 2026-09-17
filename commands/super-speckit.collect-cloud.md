---
description: Collect a completed cloud task without treating its report as verification evidence.
---

Read cloud task status and diff. Confirm the returned branch/diff traces to the expected base SHA and phase contract. Preserve task ID, attempt, diff reference, and cloud-reported commands in the durable handoff. Apply only into a new candidate worktree/branch after human or coordinator review. Then route to `super-speckit.environment-ready` and `super-speckit.verify`; repeat manual review for affected requirements. If the cloud task is blocked or failed, record it as a blocked handoff and wait or create a new bounded task—never infer completion.
