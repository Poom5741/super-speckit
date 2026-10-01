---
description: Independently run real-browser user journeys, turn confirmed UX defects into isolated fix/retest loops, and rerun the declared journey set before a UI release.
---

Use this for every UI-changing feature after deterministic gates, environment readiness, and the normal independent verification setup. The default manual browser agent is **Rakazo**, prepared through `super-speckit.rakazo-journey`. Rakazo receives an independent task packet and drives the live app deliberately from a clean QA environment rather than relying only on scripted Playwright assertions. It is separate from `super-speckit.final-manual-review`, which remains optional and human-led.

Do not call an imagined Rakazo API. Generate the task packet, dispatch only through the explicitly configured adapter, and inspect its returned report and evidence before recording a result. If Rakazo is unavailable, use another independent browser agent only as a recorded adapter exception; it does not silently become equivalent clean Rakazo evidence.

Create `journey-ux-report.md` from its template. Derive declared journeys from the confirmed Purpose Map, spec, verification matrix, Change Story, and changed routes. Test each journey against the real running app with fresh fixture/test data and capture sanitized screenshots, trace/video/logs, URLs, viewport, exact actions, and observations. At minimum inspect the changed primary journey plus applicable validation/recovery, empty/loading/error, authorization, refresh/persistence, narrow viewport, and keyboard paths.

For every finding:

1. Preserve the evidence and reproduce it under the configured rule.
2. Route a confirmed defect to `super-speckit.file-bug` and a new isolated bug-fix worktree.
3. Require regression coverage when practical, commit a new candidate, and run clean independent QA retest.
4. Rerun the affected journey **and the full declared journey set** against the latest candidate; update the report rather than carrying an earlier pass forward.

Continue this loop while the defined journey scope has a confirmed defect. At the repair-cycle limit, do not release: preserve evidence, diagnose/re-scope/research the root cause, then resume. The only passing conclusion is: **all declared journeys passed against the latest candidate and no confirmed UX defect remains in that declared scope**. It is never a claim that no possible UX bug exists.

Record the final run in feature state only after the orchestrator verifies the evidence and candidate identity: `python3 scripts/super_speckit.py record-journey-ux <feature> --report <report-path> --sha <latest-candidate-sha> --status passed`. `ready_for_merge` rejects a UI-changing feature unless that report exists and matches the latest candidate SHA.
