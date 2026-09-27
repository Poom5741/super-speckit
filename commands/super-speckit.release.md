---
description: Decide whether an independently verified candidate is merge-ready and produce the project QA summary.
---

Input: feature candidate SHA plus its latest QA/OCR/bug artifacts. Validate required gates, matrix coverage, OCR triage, and open confirmed bugs. Write `summary.md` with decision `ready-for-merge` or `not-ready`; list every unverified item, exception, and evidence link. When `merge.autonomous_when_ready` is enabled and the configured merge action is within project authority, merge the verified candidate and record the resulting SHA. Then hand the result to native `speckit.converge` so remaining spec work is appended rather than forgotten.
