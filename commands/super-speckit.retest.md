---
description: Independently retest a committed bug fix in a fresh QA clone.
---

Create a fresh outside-repository QA clone at the fix SHA. Run the original reproduction, regression check, affected matrix journeys, and relevant engineering gates. Retain evidence. On pass close the bug only with required independent proof and satisfactory OCR/Journey UX dispositions; on failure resume bug_fixing. Never reuse the maker environment as retest evidence.

Follow `skills/ask-super-speckit/references/shared-understanding.md`. Update the Bug Story with supported cause, corrected path, candidate and evidence. Encode scoped prevention in regression coverage or structure when justified; otherwise retain a reasoned scoped follow-up/no-broader-lesson decision. Human-added lessons require investigation before generalization. Knowledge-v2 resolve-bug consumes a digest-bound JSON resolution, not a maker assertion. New candidates require refreshed independent retest; continue bounded repair until verified or truthfully blocked.
