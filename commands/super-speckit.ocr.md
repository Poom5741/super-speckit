---
description: Run or ingest Alibaba OpenCodeReview findings as a separate static review lane.
---

Input: candidate SHA. Run the configured OCR adapter or import its immutable output into `ocr-findings.json`. Triaging reviewer records every finding as `fix`, `accepted-risk`, `false-positive`, or `needs-human` with rationale and owner. `fix` blocks release; the other outcomes require rationale. OCR results may reveal risks or create work, but may not mark a runtime matrix row verified and may not replace Playwright/API/DB evidence.
