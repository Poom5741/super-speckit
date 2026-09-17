---
description: Classify task slices, risks, conflicts, and required gates before creating agent worktrees.
---

Build a branch map from native tasks and repository evidence. Label every slice `parallel-safe`, `integration-serialized`, `sequential`, or `needs-design-decision`; list shared files, migrations, APIs, fixtures, and test namespaces. Assign risk from policy and choose gates proportionately. Protected/high/critical paths require the configured escalation and cannot be silently parallelized. Respect concurrency and heavy-process limits; each lane needs a committed baseline SHA.
