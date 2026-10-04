---
description: Apply the pinned Ponytail minimal-solution ladder to a bounded maker or bug-fix slice without weakening requirements or verification.
---

Use the pinned upstream `skills/upstream/ponytail/SKILL.md` after the agent has read the native spec, Atlas/Change Story, affected code path, and feedback-loop receipt. Default to configured `full` intensity for maker, bug-fix, and refactor work.

Evaluate the solution ladder in order: avoid speculative work; reuse existing code; standard library; native platform; installed dependency; one line; then the smallest new code. Trace the real flow before choosing a rung. For a bug, find and fix the common root cause rather than adding symptom guards at callers.

Record the chosen rung and a brief rejected-alternative note in the decision trail. Apply Ponytail only to the implementation shape. It may never remove or shorten: confirmed requirements, security/privacy controls, trust-boundary validation, data-loss protection, accessibility, migration safety, requested behavior, the feedback loop, independent QA, or evidence artifacts. A trivial one-liner may have a proportionate check, but all existing Super-SpecKit gates still apply.

If a simplification has a real ceiling, record it with a `ponytail:` comment only where the project’s coding style permits comments, naming the limitation and upgrade condition. Do not use `ultra` mode for protected/high-risk paths unless the project explicitly configures it.
