---
description: Decide whether an independently verified candidate is merge-ready and produce the project QA summary.
---

Input: feature candidate SHA plus its latest QA/OCR/bug artifacts. Validate required gates, matrix coverage, OCR triage, and open confirmed bugs. Write `summary.md` with decision `ready-for-human-merge` or `not-ready`; list every unverified item, exception, and evidence link. Do not merge automatically. Hand the result to native `speckit.converge` so remaining spec work is appended rather than forgotten.
