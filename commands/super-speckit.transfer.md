---
description: Create a state-verified, phase-safe handoff for a local-to-cloud or cloud-to-local agent transfer.
---

Before transfer, run strict status/validation and create `agent-transfer-handoff.md` from its template. It must name immutable SHA, feature/route/phase/stage, attempt ID, receiver authority, allowed paths, exact resume commands, evidence paths, known unknowns, and return contract. Redact secrets.

Record it using `python3 scripts/super_speckit.py record-handoff <feature> --artifact <path> --transfer <local-to-cloud|cloud-to-local|agent-to-agent|same-environment> --stage <stage> --attempt-id <id>`. The sender never certifies the receiver's state. The receiver reruns strict status and validation, verifies SHA and manifest, then either resumes the bounded stage or creates a successor handoff with preserved failure evidence.
