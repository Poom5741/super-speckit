---
name: pi-small-task-superspeckit
description: Implement or repair a small local CLI feature with a red-capable feedback loop and requirement-linked evidence, within the user's time budget.
---

# Small task, evidence first

List the requested observable behaviors. Before changing product code, create and run a tight CLI check that fails for a missing or broken requested behavior. Preserve the invocation and actual failure. A passing unrelated test is not that feedback loop.

Implement the requested change, rerun the original check, and check each requested behavior through the real CLI with isolated data. Include file-state assertions where persistence matters. Keep the checks proportional to the small task.

After the last product edit, run the relevant checks again and retain their output. Write a compact requirement-to-evidence table with command, observed result, and remaining gaps. Bind retained evidence to the tested product file hashes so later edits cannot silently reuse an old pass.

You are the maker. These checks are maker evidence, not independent approval. A separate evaluator will assess the frozen result. State that distinction and any unverified behavior in the final response. Do not introduce a second coordinator or wait for approval to finish this local task.
