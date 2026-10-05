# PStack integration evidence

Date: 2026-10-06. Pinned upstream: e5a8186d7b43be8d6ac4452440fbead5f1a51c70 (0.15.13).

## Coverage

- Source integrity: all 164 tracked files preserved byte-for-byte; routes account for all 27 workflow skills, 24 principles, 23 playbooks, two agents and 12 Benny files.
- Behavioral fixtures: real Git candidate/bug/QA flows; false release, stale candidate/attempt/digest/configured gate negatives; CAS/migration; read-only host write auditing/cancellation; runtime service side effects and cleanup; bounded swarm recovery; same-input review/dissent; arena freeze; measurement validity; transcript/decision integrity; optional-event normalization and write reconciliation; reinstall/upgrade preservation.
- Independent evaluation: separate evaluator exercised malicious/sparse inputs and reran the suite. Empty judge and self-reported verification findings were fixed; see [evaluation](evidence/pstack/independent-evaluation.md). Root later tightened pre-maker prerequisites and terminal merge retention; clean-snapshot retest covers final changes.

## Live host checks

| Host | Observed result | Limit |
| --- | --- | --- |
| ZCode 0.16.9 | Actual `pstack_host.plan/dispatch` read calc.py in a clean linked worktree, returned total 5 and marker, no writes. Passed with process-only installed provider paths. | Synthetic read-only investigation/CLI transport only. No global settings changed. |
| Pi | Actual `pstack_host.plan/dispatch` returned correct total and marker from a clean linked worktree, no writes. | CLI transport only; existing configured provider/model inherited. |
| Codex | Failed: configured inherited gpt-6.1-sol is rejected for the signed-in ChatGPT account. | No invented model fallback. Correct eligible model selection is required before live certification. |
| OMP / Cursor | Not exercised. | Optional detected adapters, not certified. |

[Initial host observations](evidence/pstack/host-probes.json) and [actual adapter observations](evidence/pstack/host-adapter-probes.json) exclude provider credentials and raw global configuration.

## Deliberate limits

The independently observed HTTP fixture can earn `verified`. CLI/TUI/library controls without a separately observed public seam remain `controls-passed`, never runtime acceptance; implement their project-specific observation adapter before claiming verification. Actual browser projects still require the existing Playwright/API/DB/Rakazo evidence.

Model-diverse design/review behavior, hidden-rubric physical access isolation, unattended provider scheduling, live GitHub/Origin/Graphite lifecycle, and externally triggered Benny/bot workflows are not certified by fixture tests. Host write auditing detects violations; it is not an OS/credential sandbox. Inherited global skills may shadow project entry points; doctor reports the winning file without editing global configuration.

Source coverage, adapter definitions, fixture behavior and live provider certification are separate claims. Installation does not activate external automations or grant merge/publication authority.

## Final independent snapshot QA

Candidate `980d79d472e0b70455e3756bba13b921a1f2d984` passed **60 tests**, including 14 state-contract tests, in a separate clean Git worktree. Source inventory/hash/executable-mode checks and diff checks passed; the checkout remained clean. The temporary snapshot does not move the user's branch or index. [QA receipt](evidence/pstack/clean-qa.json).

Tests establish the recorded fixture behavior and exact implementation snapshot; they do not establish every provider, optional service, or agent judgment capability. Changes remain in the user's workspace for review and have not been pushed.
