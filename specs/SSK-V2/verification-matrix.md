# Verification matrix

| ID | Requirement | Verification | Status |
| --- | --- | --- | --- |
| REQ-AC-01 | All public skills install in supported harness roots. | Existing Python installer suite. | Verified on local fixtures |
| REQ-AC-02 | V1 adoption preserves history and supports rollback. | Digest, preview, repeat, and rollback tests. | Verified on local fixtures |
| REQ-AC-03 | Mission Control renders card, agent, environment, and evidence state. | Installed OpenCode TUI journey. | Implemented; live journey not verified |
| REQ-AC-04 | Work survives client closure. | Supervised daemon interruption test. | Implemented; supervision journey not verified |
| REQ-AC-05 | Windows uses one persistent WSL runner. | Clean Windows 11 and WSL journey. | Not verified |
| REQ-AC-06 | Writer handoff preserves identity and prevents duplicate writers. | Fault-injection handoff suite and two-provider journey. | Locally verified; live provider journey not verified |
| REQ-AC-07 | Cloudflare supports guarded QA and human takeover. | Live Browser Run journey. | Not verified |
| REQ-AC-08 | Failed or stale proof cannot render as passed. | Negative transition fixtures. | Verified on local fixtures |
| REQ-AC-09 | Ordinary PR and CI contributions import without runtime adoption. | Contributor fixture plus `gh` adapter boundary. | Locally verified; live GitHub journey not verified |
| REQ-AC-10 | Delivery and production readiness remain separate. | State and UI assertions. | Verified on local fixtures |
| REQ-AC-11 | Git projections contain no credentials or raw private evidence. | Schema allowlist and secret scan. | Locally verified; security review pending |
| REQ-AC-12 | Full ecosystem proof covers every required platform and provider. | Independent alpha proof pack. | Not verified |
