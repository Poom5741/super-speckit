# Pi skill optimization pilot

Date: 2026-10-08. Nine completed comparison trials used pure Pi 0.84.1 with `minimax/MiniMax-M3`, medium thinking, and only read/bash/edit/write. Each task had a 20-minute cap; these trials took 72–302 seconds. No global skills, extensions, context files, or prompt templates were loaded.

The conditions are experimental Pi-native interpretations of pstack and Super-SpecKit. They do not test either complete system. Frozen upstream skills and global installations were not changed.

Validation: all 67 repository tests passed after the final runner change, all four experimental skills passed frontmatter validation, and diff checks passed. The test transcript is retained at `.skill-sandbox/final-tests.log`.

## Observed results

| Task | Profile | Repeat | CLI checks | Seconds | Tool calls | Relocated verifier | Rejects known-bad app |
| --- | --- | --- | --- | --- | --- | --- | --- |
| import | baseline | 3 | 10/10 | 71.91 | 14 | absent | not run |
| import | pstack | 3 | 10/10 | 265.42 | 13 | passes | yes |
| import | superspeckit | 3 | 10/10 | 235.03 | 32 | passes | yes |
| repair | pstack | 1 | 10/10 | 269.57 | 20 | passes | yes |
| repair | pstack-v2 | 1 | 10/10 | 299.5 | 16 | passes | yes |
| repair | superspeckit | 1 | 10/10 | 231.16 | 27 | passes | yes |
| repair | superspeckit-v2 | 1 | 10/10 | 301.55 | 31 | passes | yes |
| repair | pstack | 2 | 10/10 | 203.2 | 15 | passes | yes |
| repair | pstack-v2 | 2 | 10/10 | 129.88 | 15 | passes | yes |

All nine artifacts passed the ten private checks through the public CLI. The no-skill build left one-off verification commands and fixture inputs but no saved verifier, despite the request for executable checks. The skill builds left scripts; all selected scripts were independently rerun from relocated copies and rejected their known-bad starting implementations. This demonstrates an artifact/workflow difference in this case, not a functional-correctness advantage.

The first twelve launches were infrastructure/bootstrap or exploratory runs. Six could not start Pi because the initial filesystem profile denied its Node runtime. Earlier fixture/manifest versions also needed corrections. They are retained separately and excluded from this comparison. The all-history table remains in `.skill-sandbox/comparison.md`.

## Skill revision and actual compliance

Recorded final verification commands in both original build profiles piped output through tail/tee without preserving the underlying status. A separate failing command returned status 0 through tail and status 7 with pipefail. The v2 profiles therefore add preservation of actual check status, a rerunnable project-relative verifier, and demonstration that the verifier rejects known-bad behavior.

Both pstack-v2 repair trials deliberately restored faulty behavior to test their verifier, then restored the fix. The second preserved the final pipeline status using pipefail and PIPESTATUS. The Super-SpecKit-v2 trial also demonstrated rejection of a deliberately reintroduced dry-run regression and retained the final check status/output. It still used unguarded head/tail pipelines in intermediate steps. The instruction influenced behavior but did not enforce universal compliance.

The original Super-SpecKit repair trial already captured PIPESTATUS on its final logged run. The correction therefore cannot be credited with inventing that behavior. Correctness was unchanged, and timings varied. Keep both v2 profiles experimental; this evidence supports the narrow mechanism, not promotion or a claim that one system is better.

## Harness corrections and provenance

Independent forward testing found and helped correct an oracle that skipped invalid duplicate-row validation, incomplete tool-read receipts accepted as skill loads, symlinks omitted from manifests, and sibling temporary-runtime reads left accessible. Verification scratch artifacts now survive freezing. A recovered provider interruption is retained as a recovery event rather than mistaken for terminal failure; normal completion requires final stop and agent_end. Original classifications remain in evaluation-original.json where applicable.

A later parser regression check also ensures that a verifier mentioning notes.py is not counted as an edit to notes.py. Command-shaped workflow signals remain separate from semantic compliance; bash can change files without a write/edit event, and a Python version command is not a behavioral assertion.

The independent evaluator checked fixtures and mocked Pi-shaped transport. Live Pi trials provide separate host evidence. Filesystem containment was exercised; isolation of provider credentials from Pi itself, exhaustive inputs, live timeout behavior, and cross-model results are not certified.

Evidence: [structured comparison](evidence/skill-sandbox/pilot.json), [independent harness evaluation](evidence/skill-sandbox/independent-harness-evaluation.md), and [terminal-state recheck](evidence/skill-sandbox/independent-terminal-results.json). Full scrubbed traces, exact command receipts, frozen outputs, hashes, replay logs and original classification receipts remain under `.skill-sandbox/runs/<run-id>/` as linked by the JSON.

Reproduction and supported controls: [experiment instructions](../experiments/skill-sandbox/README.md). Candidate instructions: [pstack v2](../experiments/skill-sandbox/skills/pi-small-task-pstack-v2/SKILL.md) and [Super-SpecKit v2](../experiments/skill-sandbox/skills/pi-small-task-superspeckit-v2/SKILL.md).
