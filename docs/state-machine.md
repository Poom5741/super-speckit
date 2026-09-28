# State machine

```text
planned → Purpose Gate (human-confirmed) → Spec Grill (evidence-labeled) → maker_running → candidate_ready → qa_running ──pass──> ready_for_merge → merged
                                      │              │
                                      │              ├─blocked──> blocked
                                      │              └─failure──> qa_failed → bug_fixing → retest_running ──pass──┘
                                      │                                                    └─fail──> bug_fixing
```

`maker_running` and every later delivery state require a human-confirmed Purpose Map and a completed evidence-labeled Spec Grill. The human confirms purpose only: intended outcome, affected people, success signal, and non-goals. `candidate_ready` requires a committed SHA and a completed matrix. `qa_running` requires a clean worktree and a distinct checker. `ready_for_merge` requires all configured gates passing, no untriaged blocking OCR finding, no open confirmed bug, and no matrix row silently omitted. In autonomous mode, the orchestrator merges when the configured merge action is within its authority. `blocked` is a truthful terminal pause for unavailable dependencies, secrets, or environments; it is never converted to pass.

Transitions are append-only in run evidence. A new candidate after a fix receives a new QA run; old evidence is retained.
