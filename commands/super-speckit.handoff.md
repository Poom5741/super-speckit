---
description: Write a durable factual handoff whenever a super-speckit lane pauses, fails, or completes.
---

Write `durable-handoff.md` from the template and link it from feature state. Include immutable candidate SHA, role, verified evidence, work completed, next smallest safe action, autonomous decision/rationale, and blocker/resume condition. The next agent must read the handoff and re-check references before acting. A blocked handoff records its next automatic probe; it does not justify a blind retry or an inferred pass.

For a change of agent or environment, use `super-speckit.transfer` instead. It adds an immutable SHA, stage, attempt ID, strict state receipt, exact resume checks, authority/path boundary, and return contract; a generic narrative handoff is insufficient for local↔cloud continuity.
