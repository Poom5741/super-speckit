# Artifact schemas

Artifacts are human-readable Markdown plus JSON for orchestration. IDs are stable and references are relative to the repository root.

| Artifact | Location | Required invariant |
| --- | --- | --- |
| Feature state | `.super-speckit/state/features/<id>.json` | Candidate SHA and maker/checker identities are immutable per run. |
| Verification matrix | `specs/<feature>/verification-matrix.md` | Each requirement has at least one verification row or an explicit exception. |
| QA run | `.super-speckit/qa/<run-id>/run.json` | Every command/evidence reference records status and sanitization. |
| OCR findings | `.super-speckit/qa/<run-id>/ocr-findings.json` | Findings have a triage outcome/rationale. |
| Bug | `.super-speckit/bugs/BUG-<id>.md` | Confirmed failures have reproducibility and evidence. |
| Project summary | `.super-speckit/qa/summary.md` | Explicitly names unverified scope. |
| Proof pack | `.super-speckit/qa/<run-id>/proof-pack.json` | Binds all evidence to one immutable candidate and environment receipt. |
| Design decision | `.super-speckit/design/<feature>/decision.json` | UI work cannot start until `approved` or explicitly `not-required`. |

JSON shape used by the included validator:

```json
{"id":"FEATURE-042","state":"qa_running","candidate_sha":"40+ hex chars","maker":"agent-a","checker":"agent-b","matrix":"specs/042-foo/verification-matrix.md","runs":["QA-042-001"],"bugs":[]}
```

Allowed states: `planned`, `maker_running`, `candidate_ready`, `qa_running`, `qa_failed`, `bug_fixing`, `retest_running`, `ready_for_human_merge`, `merged`, `blocked`.

Proof pack minimum shape:

```json
{"candidate_sha":"abcdef1","run_id":"QA-42-001","environment_receipt":"environment-receipt.json","gates":[{"name":"unit","status":"pass","log":"unit.log"}],"matrix":"specs/042/verification-matrix.md","evidence":["trace.zip"],"ocr":{"status":"triaged","findings":"ocr-findings.json"},"unverified":[]}
```
