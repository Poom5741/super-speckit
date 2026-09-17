# Design references (checked 2026-09-18)

- [GitHub Spec Kit](https://github.com/github/spec-kit) — native artifact-driven SDD; current docs describe Specify → Plan → Tasks → Implement → Converge and optional clarify/analyze/checklist quality gates.
- [Spec Kit workflows reference](https://github.com/github/spec-kit/blob/main/docs/reference/workflows.md) — portable workflow/gate conventions.
- [MAQA v0.3.1](https://github.com/GenieRobot/spec-kit-maqa-ext/tree/maqa-v0.3.1) — coordinator, local state, and isolated feature worktrees. Super-speckit deliberately does not use its static QA alone as release proof.
- [sdlc-skills manual-qa](https://github.com/arozumenko/sdlc-skills) — live Playwright-driven test-run and reporting roles. Super-speckit uses its independent browser-QA principle without taking a dependency on that factory.
- [Playwright trace documentation](https://playwright.dev/docs/trace-viewer) — preferred runtime evidence format where available.
- [AWO](https://github.com/ystepanoff/awo) — useful model for read-only reviewer worktrees, deterministic proof packs, protected paths, and manual merge.
- [Orka](https://github.com/Dusttoo/orka) — useful model for policy-driven transitions, risk gates, and bounded repair/concurrency limits.
- [qrspi-plus](https://github.com/dfrysinger/qrspi-plus) — useful model for plan-time dependency/parallelism classification.
- [OpenTelemetry CI/CD conventions](https://opentelemetry.io/blog/2025/otel-cicd-sig/) — candidate/revision and test evidence correlation concepts.

OCR integration is adapter-based because vendor invocation/authentication and output formats vary. Configure the command to produce `ocr-findings.json`; do not commit credentials or raw sensitive logs.
