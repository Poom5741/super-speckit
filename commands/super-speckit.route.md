---
description: Classify a confirmed feature as micro, normal, or milestone and select the smallest safe autonomous delivery route.
---

Classify from purpose, codebase evidence, affected contracts/data, risk, and verification cost. Record it with `python3 scripts/super_speckit.py route <feature> <micro|normal|milestone> --rationale "..."`.

- **micro:** bounded local change with one public seam; use compact Purpose Map, compact grill, feedback loop, independent verification, and reassess if scope expands.
- **normal:** use the complete current Super-SpecKit feature flow.
- **milestone:** split into demoable vertical slices; after each independently verified slice, create `slice-reassessment.md`, record `reassess`, and keep/split/reorder/defer/cancel the next slice based on evidence.

Risk always upgrades the route. A route never removes Purpose Gate, evidence labeling, or independent QA.
