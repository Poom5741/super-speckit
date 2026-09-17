---
description: Create a clean-environment receipt before runtime verification.
---

In the QA worktree, execute configured readiness checks: dependency/image identity, service health, migration state, fixture reset, isolated namespace allocation, test account creation, and redaction check. Write `environment-receipt.json` with candidate SHA, commands/statuses, endpoint identities, namespace, timestamps, and secret-free logs. A failed or incomplete receipt blocks runtime claims; it is an environment issue, not product pass/fail evidence.
