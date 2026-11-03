# VibeWise learning checkpoint gate inside Super-SpecKit

Read this contract together with the pinned skill, loaded through
`python3 scripts/vibe_wise_adapter.py read learn`. Super-SpecKit owns the
pipeline, canonical state, candidates, QA and release authority. VibeWise
supplies one mandatory method: **the human reasons through the approach and
design, and explicitly authorizes implementation, before maker work** — the
opposite of passive vibe-coding. VibeWise is never a second coordinator; its
plugin/hooks are not installed or registered.

## What is enforced, in code

Every feature record created with `gates_contract=discipline-v1` (the
`create-feature` default) must hold a digest-bound `learning-checkpoint`
prerequisite receipt before `maker_running`, before any new candidate, and at
release. `scripts/discipline_contract.py` validates it.

- The receipt binds the current confirmed purpose decision (`purpose_digest`),
  so the checkpoint reflects the purpose the human actually confirmed.
- The receipt binds the pinned vibe-wise `learn` skill revision and SHA-256
  from `vendor/vibe-wise`.
- `status: "engaged"` requires: a declared `level` (beginner/intermediate/
  advanced, adapting explanation depth per upstream), checkpoints covering
  both `approach` and `design` where the recorded `human` explains their
  reasoning and the agent's role is feedback and concept explanations, plus an
  explicit `authorization` (`human`, `ts`, `scope`) for implementation.
  Checkpoint and authorization identities must never equal the maker or
  checker agent identities.
- `status: "human-declined"` is a real human decision, not an agent shortcut:
  `declined_by` must equal the identity that confirmed the purpose gate, and a
  `reason` is required. The agent may offer the checkpoint; only that human
  may decline it.

## How VibeWise maps onto this pipeline

- The learning conversation happens in the coordinator's main context (upstream
  explicitly keeps it out of subagents). The learner owns the design; guidance
  stays minimal: feedback on their reasoning, explanations of unfamiliar
  concepts, approaches offered only when asked for or when stuck.
- The checkpoint sits after the purpose gate and before scope routing/maker
  work. It does not replace the purpose gate (outcome, people, success signal,
  non-goals) — it adds the human's approach/design reasoning and
  implementation authorization.
- `.vibe-wise/` state conventions (profile, project map, progress, pending
  decisions) are optional evidence the receipt may cite; Super-SpecKit state
  remains canonical and checkpoint evidence lives under the project evidence
  root, not in plugin-owned state.
- Learning and learner control take priority over build speed inside the
  checkpoint, but they never weaken any downstream gate: independent QA,
  exact-candidate proof, Journey UX and convergence all still apply unchanged.
- `reset` exists only in the vendored source; resetting learning state never
  resets delivery state or evidence.
