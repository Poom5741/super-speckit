# Independent harness evaluation

Evaluator: external Super-SpecKit skill-evaluator; no live provider or subject-agent trial. Real macOS sandbox-exec and Python subprocess fixtures; mocked Pi process only for trace validity tests. Isolated workspace: /tmp/skill-harness-eval.lp4eWO. Production source, skills, credentials, prior runs and conclusions were not modified or read.

Request: assess the pure-Pi small-task comparison harness's public oracle, output freezing, containment and evidence validity. Candidate source snapshots: runner.py (initial), runner-recheck.py (after coordinator correction).

| Invariant | Procedure | Observed | Status | Evidence |
| --- | --- | --- | --- | --- |
| Public CLI oracle accepts correct implementation | evaluate.py and recheck.py | Original 9/9, corrected 10/10 | pass | results.json, recheck-results.json |
| Oracle detects intentionally faulty importer | evaluate.py | Broken seed 1/9 | pass | results.json |
| Entire CSV validated including skipped duplicate IDs | Mutant validates only after duplicate skip | Originally 9/9 despite invalid CSV accepted and store modified; corrected oracle rejects 1 check | fixed and rechecked | results.json, recheck-results.json |
| Evaluation preserves regular source-file bytes | Hash before/after oracle | Correct, broken and mutant source hashes unchanged | pass for these fixtures | results.json |
| Output manifest captures symlink identity | Replace symlink target /etc/hosts with /etc/services | Manifest unchanged; symlink-only output manifest empty | fail | boundary.py, boundary-results.json, results.json |
| Checkout/private evaluator is unreadable to sandboxed process | Real cat under generated profile | Operation not permitted | pass on tested path | boundary-results.json |
| Outside disposable runtime writes denied | Shell writes outside fixture | Denied; allowed fixture write succeeds | pass on tested paths | boundary-results.json |
| Receipt establishes selected skill was loaded | Mock process emits read-start without read-end, then final text | candidate valid=true and skill_read=true without any receipt | fail | receipt.py, receipt-results.json, receipt-runs/import-candidate-1-699c237e/trace-summary.json |
| Live Pi model/provider run | Excluded by delegated task | Not invoked | not-run | none |

Defects: (1) incomplete tool events are sufficient to establish selected skill read and valid evidence; classify trace-integrity, corrective layer event validation and successful read receipt. (2) hashes excludes symlinks, so it does not establish immutable output identity for all artifact types; classify evidence-integrity, corrective layer reject symlinks or manifest link destinations/types and containment guarantees. The demonstrated symlink to outside /tmp was blocked by evaluator, so this is not a demonstrated escape.

Exact reproduction: python3 /tmp/skill-harness-eval.lp4eWO/evaluate.py (fresh directories required); python3 /tmp/skill-harness-eval.lp4eWO/recheck.py; python3 /tmp/skill-harness-eval.lp4eWO/boundary.py (fresh directories required); python3 /tmp/skill-harness-eval.lp4eWO/receipt.py (fresh directories required). Fixtures, copied runner snapshots, scripts and complete results are retained in this directory.

Limits: no live provider certification, no credential/network boundary claim, no exhaustive oracle assurance, no semantic skill compliance judgment. An assistant-only baseline trace is accepted by the runner; this can represent a legitimate failure-to-act outcome and is not independently classified as infrastructure failure. Public host files such as /etc/hosts remain readable by default; this matches broad runtime access rather than a hermetic sandbox. No additional escape probing performed.

A corrective-enforcement run is justified for receipt validity and manifest identity. The duplicate-invalid gap was corrected and independently rerun. This evaluation proves only the stated fixture behaviors.

## Independent hardened recheck

Source snapshot runner-hardened.py. Executed hardened.py against new default-system-temp fixture. Sibling runtime private file read denied, own runtime file read allowed. Changing a symlink target now changes hashes. These two hardened invariants pass their real behavioral checks; evidence hardened-results.json. Symlink manifest defect above is corrected for target identity. Receipt-completeness defect remains unverified after correction. Source snapshots retained to distinguish evaluation revisions.

## Final corrected coverage recheck

Source snapshot runner-final.py, SHA256 c9be2a650a358e8b116d80e905baa8850f51cf3316f92fc2e9b97c6cd571aadf. Reproduction: python3 /tmp/skill-harness-eval.lp4eWO/final-recheck.py in a fresh copy of its fixture directories. Evidence final-recheck-results.json and final-recheck-runs.

| Corrected invariant | Independent observed behavior | Status |
| --- | --- | --- |
| Incomplete normal read invalidates evidence | read-start without end -> valid=false, skill_read=false, incomplete_tool_calls=['read-1'] | pass |
| Failed read never establishes skill loaded | completed isError=true -> skill_read=false | pass |
| Successful read receipt establishes skill loaded | completed isError=false -> skill_read=true | pass |
| Failed skill loading remains an observable agent outcome | failed completed read -> valid=true, skill_read=false | observed; consistent with behavior-outcome distinction |
| Verification artifacts retained | mock subject wrote .tmp/verification.txt; frozen output retains exact content | pass |
| Verification artifacts manifested | .tmp/verification.txt present in artifact manifest for all 3 fixtures | pass |
| Public oracle distinguishes corrected versus duplicate-validation mutant | correct 10/10; mutant 9/10 | pass |
| Sibling runtime containment | actual default-temp sibling read denied; own read succeeds | pass |
| Symlink target identity | link target replacement changes manifest | pass |

No remaining concrete defect observed within this final bounded recheck. Original findings and source snapshots remain above as a record of fixes. No live Pi/provider execution, real trace schema certification, adversarial process escape certification, exhaustive input coverage, or semantic workflow compliance was tested. Timeout evidence handling was not exercised in this recheck. No source or production artifacts changed by evaluator.

## Terminal-session and verifier replay recheck

Source runner-terminal.py SHA256 3e71c8b532ade723e31afa22d8c9bc1731ea70107e06959e0655dff5893449c9. Independent new mocked-Pi fixture terminal-config and terminal-runs; no live traces/conclusions accessed. Actual-shaped events include agent_start, intermediate assistant error, paired skill read start/end, final assistant message, agent_end and agent_settled.

Recovered provider interruption followed by terminal stop: valid=true, prior error retained and separately recorded as recovered. Terminal error: valid=false, both errors retained. These two requested invariants pass.

Additional concrete defect: terminal stopReason=toolUse followed by agent_end/agent_settled is accepted valid=true despite absence of a final stop. Complete read receipt was present, so incomplete-tool detection cannot catch it. This is a mock trace integrity failure; whether a real Pi transport can emit this malformed terminal sequence remains untested. Candidate correction: explicitly allowlist normal final stop reasons rather than rejecting only error.

Verifier replay: generated independent verifier against copied correct CLI; as-built exits zero and prints 'import retry verified'. Known-bad repair baseline exits one on retry assertion (added=1/skipped=0 instead of added=0/skipped=1). Both execute in new relocated sandbox fixtures. Frozen original manifest remains identical. Evidence terminal-results.json, replay-fixture/verifier-replay.json and replay-fixture/verifier-negative-control.json. Reproduction terminal-recheck.py (fresh fixture directories required).

Limits remain: mocked Pi event-schema coverage rather than live Pi/provider certification, no timeout replay test, no semantic verification claim from arbitrary exit status. Replay success here proves only the independently generated import/retry assertions.

## Final terminal correction

Fresh source snapshot runner-terminal-final.py SHA256 1e52a2cecaf6c7d1ecf49f9225e0041989909cc9cbb676b57f02a35edda4d3dd. Fresh isolated mock fixtures terminal-final-config and terminal-final-runs; no live provider or prior trial conclusions used. Executed terminal-final-recheck.py.

Recovered error with final stop and agent_end: valid=true, prior error retained. Final error: valid=false. Unexpected final toolUse with agent_end/settled: valid=false. All three terminal-classification invariants pass; previously observed unexpected-terminal defect corrected and independently rechecked. Evidence terminal-final-results.json. No further work performed. Limits from previous fixture evaluations remain.
