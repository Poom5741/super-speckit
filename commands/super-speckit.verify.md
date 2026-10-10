---
description: Independently verify an exact candidate in a disposable QA clone.
---

Input: feature ID and committed immutable SHA. Create an outside-repository clone with `python3 scripts/super_speckit.py qa-clone --repo . --path <path> --ref <sha>`. Start QA with `transition <feature> qa_running --checkout <path> --attempt-id <id>`. Legacy --worktree and receipt worktree keys accept clones too.

1. Reset fixtures and establish isolated identities/namespaces. Confirm exact SHA and clean checkout.
2. Run configured architecture, types/schema, format, lint, unit, integration and build gates; retain commands, outcomes and evidence.
3. Start the actual app from the clone. Execute complete matrix-linked user journeys with screenshots/traces and sanitized logs. Assess discoverability, feedback, error recovery, persistence, authorization, keyboard and relevant screen sizes. Record justified non-applicable coverage.
4. Assert API/DB effects that UI alone cannot prove. Run bounded exploration separately. UI candidates retain the independent Journey UX contract.
5. Obtain independent engineering review of this candidate, dispose every blocking finding, and record the JSON engineering-review prerequisite described in playbook-delivery.md. Static review never closes runtime rows.
6. Write run.json/report.md and proof receipts. Mark requirements verified, not-verified or not-applicable with evidence. Classify/reproduce failures before filing bugs. Any product change needs a new candidate and proof.
7. Retain evidence outside the disposable checkout before cleanup. Never edit maker/product code or merge as checker. Linked worktrees remain explicit compatibility options.
