---
name: pi-small-task-superspeckit-v2
description: Implement or repair a small local CLI feature with a red-capable feedback loop and requirement-linked evidence, within the user's time budget.
---

# Small task, evidence first

List the requested observable behaviors. Before changing product code, create and run a tight CLI check that fails for a missing or broken requested behavior. Preserve the invocation and actual failure. A passing unrelated test is not that feedback loop.

Implement the requested change, rerun the original check, and check each requested behavior through the real CLI with isolated data. Include file-state assertions where persistence matters. Keep the checks proportional to the small task.

After the last product edit, run the relevant checks again and retain their output. Write a compact requirement-to-evidence table with command, observed result, and remaining gaps. Bind retained evidence to the tested product file hashes so later edits cannot silently reuse an old pass.

You are the maker. These checks are maker evidence, not independent approval. A separate evaluator will assess the frozen result. State that distinction and any unverified behavior in the final response. Do not introduce a second coordinator or wait for approval to finish this local task.

## Preserve the check result

Keep a rerunnable verifier in the project, with paths resolved from its own location and scratch data isolated from retained evidence. Run it as an actual command and retain its output plus its exit status.

Logging must not turn a failed check into a successful command. With shell pipelines, enable pipefail and capture the verifier status before another command overwrites it; with a subprocess, check its return code. Commands such as `verify | tail`, `verify | tee`, or `verify; echo done` can otherwise report success after verification failed. Confirm a newly written verifier can reject a known-bad behavior before trusting its green result. Report the observed failure or success, rather than inferring it from output-file existence.
