---
description: Run a blinded, evidence-based A/B evaluation to determine whether a Project Atlas improves agent change comprehension and delivery.
---

Do not claim that an Atlas helps merely because it exists, is readable, or an agent says it liked it. Use at least three representative, independently QA-able holdout changes. For every task, use the same immutable base SHA, task brief, model/configuration, authority, and time/token budget.

Run two independently scoped conditions in randomized order:

1. **Control:** repository search and normal project files only; do not expose Atlas/Change Story files.
2. **Atlas:** identical task plus the relevant, evidence-linked Atlas and Change Story.

Use `templates/atlas-evaluation.json` per condition. The expected impacted components and requirements are defined before comparing runs and independently scored. Record duration/tokens if available, correctly covered requirements, correctly identified impacted components, unsupported claims, and independent QA outcome. A pass from the implementing agent does not count as QA.

Run `python3 scripts/atlas_eval.py --control <control.json> --atlas <atlas.json> --output <report.md>`. It reports `benefit-supported`, `no-clear-benefit`, or `inconclusive`; fewer than three paired completed runs, unmatched task/base/configuration, or missing independent QA is always `inconclusive`. Use results to improve or remove Atlas requirements. Never turn an evaluation result into a release gate for a product feature.
