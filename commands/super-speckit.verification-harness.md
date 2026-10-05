---
description: Create or refresh the project-local runtime verification harness and feature map before runtime QA.
---

Run `python3 scripts/super_speckit.py harness-init --repo .` before the first runtime QA run. It creates the project-local verification harness and feature map without guessing project commands. Configure launch, readiness, fixture reset, browser, API, and DB commands in `super-speckit.yml`; then replace template rows with discovered, executable project facts.

The harness must specify launch, health/readiness, isolated test data, public behavior seams, evidence destinations, and cleanup. Add each requirement or capability to the feature map and bind it to deterministic and runtime evidence as appropriate. Run at least a live smoke path before declaring the harness usable. On a changed route, app startup, test-data model, or runtime failure, refresh only the affected rows and retain the prior evidence.

For a feature, record the verified harness link with `python3 scripts/super_speckit.py record-artifact <feature> verification-harness --artifact .super-speckit/verification/verification-harness.md`. The harness enables QA; it does not replace independent clean-worktree verification.

Expose executable Launch / Doctor / Drive / Evidence / Cleanup controls for the actual browser, CLI/TUI, service or library surface. Generated templates stay draft until the live smoke completes and retained artifacts still exist after cleanup. Full maintenance runs every declared feature against source and the running application, even if documentation appears current. Product regressions enter the bug lane; update documentation only after preserving the failed behavior evidence.
