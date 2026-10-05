---
description: Run an independent, multi-lens static review panel and triage its findings without treating it as runtime proof.
---

Use this after a candidate SHA exists and before release. Allocate independent read-only reviewers for the identical-prompt protocol. Run configured correctness/architecture/security/maintainability/UX lenses only as a separate lens-review protocol. Give every reviewer the same immutable candidate SHA, scope, relevant requirements, and change evidence. Where model diversity is available, select different configured models; when it is not, record that limitation rather than claiming independent model diversity.

Each reviewer returns only evidence-backed findings with severity, affected requirement/path, reproducer or reasoning, and recommended disposition. A synthesizer groups agreement and disagreement but must not auto-apply fixes. Persist the panel result from `templates/static-review-panel.md`, then record it with `record-artifact <feature> static-review`.

Route confirmed code findings through OCR triage or the normal bug/fix loop. This panel is static review: it may never mark a runtime matrix row verified, replace Playwright/API/DB evidence, or close the Rakazo Journey UX requirement.

Use the faithful PStack identical-prompt protocol by default: render one immutable packet containing intent, exact diff, candidate SHA and the complete rubric; hash the packet and give identical bytes to every seat. Do not change lenses or stances between these seats. Distinct configured supported models provide model diversity; if unavailable, report that limitation. Lens review remains a separately named protocol and artifact. Preserve lone findings and dissent, with lead dispositions Act On / Consider / Noted / Dismissed and evidence for each. Reviewer findings never disappear merely because other reviewers disagree.
