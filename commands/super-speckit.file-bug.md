---
description: Turn a reproducible independent QA failure into a durable super-speckit bug artifact.
---

Input: feature ID, QA run ID, and failed matrix row. Preserve the original evidence. Re-run the smallest reliable reproduction up to `qa.reproduction_attempts`; label a non-reproduced report `suspected-flake` and do not create a confirmed bug. Deterministic failures may be confirmed after one preserved run.

For a confirmed failure, create `.super-speckit/bugs/BUG-<id>.md` from the schema. Include expected/actual behavior, exact candidate SHA, environment, reproduction steps, linked evidence, severity, and affected requirement. Create a tracker issue only if the configured external integration is authorized. Set status `confirmed`, then route a distinct maker to `super-speckit.fix`.
