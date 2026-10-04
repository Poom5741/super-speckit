---
description: Run an independent, multi-lens static review panel and triage its findings without treating it as runtime proof.
---

Use this after a candidate SHA exists and before release. Allocate independent, read-only reviewers using the configured lenses: correctness, architecture/domain boundaries, security/data safety, and maintainability/minimality; add UX/accessibility only for UI changes. Give every reviewer the same immutable candidate SHA, scope, relevant requirements, and change evidence. Where model diversity is available, select different configured models or stances; when it is not, record that limitation rather than claiming independent model diversity.

Each reviewer returns only evidence-backed findings with severity, affected requirement/path, reproducer or reasoning, and recommended disposition. A synthesizer groups agreement and disagreement but must not auto-apply fixes. Persist the panel result from `templates/static-review-panel.md`, then record it with `record-artifact <feature> static-review`.

Route confirmed code findings through OCR triage or the normal bug/fix loop. This panel is static review: it may never mark a runtime matrix row verified, replace Playwright/API/DB evidence, or close the Rakazo Journey UX requirement.
