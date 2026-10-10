---
description: Independently retest a committed bug fix in a fresh QA clone.
---

Create a fresh outside-repository QA clone at the fix SHA. Run the original reproduction, regression check, affected matrix journeys, and relevant engineering gates. Retain evidence. On pass close the bug only with required independent proof and satisfactory OCR/Journey UX dispositions; on failure resume bug_fixing. Never reuse the maker environment as retest evidence.
