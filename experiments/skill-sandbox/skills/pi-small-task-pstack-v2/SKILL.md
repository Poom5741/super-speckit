---
name: pi-small-task-pstack-v2
description: Implement or repair a small local CLI feature with direct behavioral verification, within the user's time budget.
---

# Small task, direct verification

Inspect the existing code and commands. Reuse their structure and installed dependencies. Make the smallest implementation that satisfies the request.

If fixing a bug, reproduce it first and fix the cause rather than hiding the symptom. Check for the same pattern at other relevant call sites.

Call the CLI as its user would. Assert literal expected outputs and actual file effects, rather than internal calls or successful compilation. Script repeatable checks when practical, execute them, and retain their output for review.

Before declaring completion, check the real final artifact. Report what you observed and what remains unverified. Keep the verification proportional to this small task.

## Preserve the check result

Keep a rerunnable verifier in the project, with paths resolved from its own location and scratch data isolated from retained evidence. Run it as an actual command and retain its output plus its exit status.

Logging must not turn a failed check into a successful command. With shell pipelines, enable pipefail and capture the verifier status before another command overwrites it; with a subprocess, check its return code. Commands such as `verify | tail`, `verify | tee`, or `verify; echo done` can otherwise report success after verification failed. Confirm a newly written verifier can reject a known-bad behavior before trusting its green result. Report the observed failure or success, rather than inferring it from output-file existence.
