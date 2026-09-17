---
description: Write a durable factual handoff whenever a super-speckit lane pauses, fails, or completes.
---

Write `durable-handoff.md` from the template and link it from feature state. Include immutable candidate SHA, role, verified evidence, work completed, next smallest safe action, blocker/resume condition, and required human input. The next agent must read the handoff and re-check references before acting. A blocked handoff causes ask-super-speckit to wait; it does not justify a retry loop or an inferred pass.
