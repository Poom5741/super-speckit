---
description: Convert recurring agent or delivery failures into the smallest verified structural enforcement.
---

Use after the same failure class occurs at least `continuous_improvement.repeated_failure_threshold` times, or after one severe escape. Do not turn a single subjective preference into a permanent rule.

Create `corrective-enforcement.md` from its template. State the historical counterexample, recurrence evidence, root cause, and the first enforcement layer that can prevent it: architecture/API boundary, type/schema, lint/static rule, CI gate, regression test, then documentation only if no enforceable mechanism exists. Implement the smallest chosen guard and prove that it fails on the historical bad example while allowing the valid path.

Record the artifact with `record-artifact <feature> corrective-enforcement`. If no guard can be proven, retain the failed attempt and leave the risk explicit. Do not use this lane to silently expand scope or weaken a release gate.

Maintain a rule-to-enforcement register linking historical bad example, chosen guard, valid control, observed commands/results and remaining prose. Retire redundant instructions only after enforcement makes the historical failure impossible on its declared seam. `reflect` is a separate evidence-based improvement proposal; global skill changes require explicit selection.
