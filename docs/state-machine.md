# State machine

```text
planned → Purpose Gate (human-confirmed) → Spec Grill (evidence-labeled) → Route + Atlas + Change Story → maker_running → candidate_ready → qa_running ──pass──> ready_for_merge → merged
                                      │              │
                                      │              ├─blocked──> blocked
                                      │              └─failure──> qa_failed → bug_fixing → retest_running ──pass──┘
                                      │                                                    └─fail──> bug_fixing
```

`maker_running` and later states require recorded user-confirmed purpose and a scope route. Compact micro delivery uses playbook.md plus a matrix; normal/milestone and legacy routes retain native planning, Spec Grill, Atlas and Change Story. New playbook-led records require research and architecture receipts before code and exact-candidate independent engineering review before release. The human confirms purpose only: intended outcome, affected people, success signal, and non-goals. `candidate_ready` requires a committed SHA and a completed matrix. `qa_running` requires a clean separate clone or optional registered worktree and a distinct checker. `ready_for_merge` requires all configured gates passing, no untriaged blocking OCR finding, no open confirmed bug, and no matrix row silently omitted. In autonomous mode, the orchestrator merges when the configured merge action is within its authority. `blocked` is a truthful terminal pause for unavailable dependencies, secrets, or environments; it is never converted to pass.

Transitions are append-only in run evidence. A new candidate after a fix receives a new QA run; old evidence is retained.

Read-only investigation/help routes do not enter this delivery state machine. Candidate identities are immutable and resolve to real commits. A fix creates a new candidate and independent QA run; patch-id equivalence does not transfer runtime acceptance. Invalid or stale receipts, empty/null/directory evidence, omitted coverage, failed gates and open confirmed bugs block release. State writes use atomic revisioned updates; attempt-bound receipts reject duplicate/stale worker completions. Scheduler priority is recovery/defects, missing prerequisites, candidate QA, then remaining maker work. Host continuation reconciles canonical state and real Git before dispatch.
