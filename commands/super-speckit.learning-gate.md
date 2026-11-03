---
description: Run the mandatory VibeWise learning checkpoint gate — the human reasons through approach and design and authorizes implementation.
---

# Learning checkpoint gate

This gate is enforced by code, not convention: `scripts/discipline_contract.py` blocks `maker_running`, new candidates and release for every `gates_contract=discipline-v1` record until a valid `learning-checkpoint` receipt exists. Read the [adapter contract](../adapters/vibe-wise/override-contract.md) and the pinned skill with `python3 scripts/vibe_wise_adapter.py read learn` first.

1. After the purpose gate confirms outcome/people/success/non-goals, offer the learning checkpoint in the main conversation (upstream keeps it out of subagents). The human leads: ask for their approach and wait. Give concise feedback on their reasoning and explain unfamiliar concepts; offer approaches only when they ask or are stuck, then return decisions to them.
2. Adapt to the declared `level` (beginner/intermediate/advanced). Learning and learner control take priority over build speed inside this checkpoint.
3. Cover both required checkpoints — `approach` and `design` — recording the human's own reasoning, not an agent summary. Keep prior `.vibe-wise/` learning state if present; never invent learning history.
4. Obtain explicit implementation authorization from the human (`human`, `ts`, `scope`). Never record maker/checker agent identities as the human. If the human declines learning mode, record `status: human-declined` with `declined_by` exactly the purpose-gate confirmer and their reason; only that human may decline.
5. Record the receipt (`templates/learning-checkpoint.json` shape) via `python3 scripts/super_speckit.py record-prerequisite <feature> learning-checkpoint --artifact <receipt>`.

The checkpoint adds the human's approach/design reasoning and authorization; it never replaces the purpose gate and never weakens independent QA, exact-candidate proof, Journey UX or convergence.
