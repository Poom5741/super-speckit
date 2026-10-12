# Pi skill experiments

The first experiment tests two Pi-native interpretations of a small-task workflow. It does not execute or compare the complete Super-SpecKit and pstack systems. Upstream files remain unchanged.

The pstack profile draws from `principle-prove-it-works`, `principle-test-behavior-not-implementation`, `principle-fix-root-causes`, and the small-change preference. The Super-SpecKit profile draws from its red-capable feedback loop, requirement-linked public behavior checks, final-candidate evidence, and maker/checker distinction. The profiles are experimental skills, not replacements for their sources.

Run the stdlib harness from the repository root:

```sh
python3 scripts/skill_sandbox.py run --condition baseline --case import --repeat 1
python3 scripts/skill_sandbox.py run --condition pstack --case import --repeat 1
python3 scripts/skill_sandbox.py run --condition superspeckit --case import --repeat 1
python3 scripts/skill_sandbox.py report
```

`run` uses the installed Pi and its configured provider/model, but gives it a fresh configuration directory with only authentication/provider definitions and explicit model settings. Discovery of extensions, skills, context files, prompt templates, themes, and packages is disabled. A selected skill is loaded explicitly; the baseline loads none. No extra orchestration extension is installed. All conditions have the same four standard Pi tools and common task brief. Selected conditions receive the same short instruction to read and apply the selected skill. This tests explicitly invoked skills, not automatic discovery.

Each run has a 20-minute maximum and a fresh fixture. macOS `sandbox-exec` restricts writes to disposable runtime directories and blocks reads of the checkout, other runs, and the private evaluator. The same Pi process still needs provider credentials; this is filesystem containment, not credential isolation from its own bash tool or a network security sandbox. No external services are part of the tasks. Retained JSON events are scrubbed for known credential values. Raw runtime configuration is deleted and never archived.

The private oracle runs after output freezing, in a copy of the output. Workflow evidence comes from actual tool events; automated signals are labeled as signals, not semantic proof. Infrastructure errors and incomplete normal traces invalidate a comparison. Ignoring a selected skill remains an observable agent outcome. Timeouts remain task outcomes. The `repair` case starts with an existing faulty importer. Its results are withheld until the candidate is frozen, but its fixture was designed by the author. This is a same-domain transfer check, not an independently authored unseen-task holdout.

The v2 profiles add a narrow correction motivated by recorded commands in both profiles: logging through shell pipelines must preserve the verifier's actual exit status. The original profiles stay frozen for comparisons. No v2 profile is globally installed or promoted based on this pilot.

Replay the subject's declared verifier in a relocated copy, then check that it rejects the known-bad starting implementation:

```sh
python3 scripts/skill_sandbox.py replay --run .skill-sandbox/runs/RUN_ID --command '["bash", ".tmp/verify.sh"]'
python3 scripts/skill_sandbox.py replay --run .skill-sandbox/runs/RUN_ID --command '["bash", ".tmp/verify.sh"]' --negative-control import
```

Use the actual verifier command from that run's artifacts; the example path is not universal. Replay changes only a disposable copy. Exit status alone does not establish sufficient test coverage; inspect assertions and retain the independent public oracle.

See `docs/skill-optimization-sandbox.md` for the experiment contract. A pilot identifies concrete failures and validates measurement; it cannot establish general superiority.
