---
description: Run the mandatory Elephant/Goldfish fresh-context design review gate before maker work.
---

# Goldfish review gate

This gate is enforced by code, not convention: `scripts/discipline_contract.py` blocks `maker_running`, new candidates and release for every `gates_contract=discipline-v1` record until a valid `goldfish-review` receipt exists. Read the [adapter contract](../adapters/elephant-goldfish/override-contract.md) and the pinned protocol with `python3 scripts/egm_adapter.py read egm-review` before dispatching.

1. Determine the review target from the recorded route: `spec.md` for normal/milestone, `playbook.md` for micro. Resolve its current bytes; the receipt binds them.
2. Inventory the real harness. If it can spawn subagents (named agents, Agent/Task tools, OMP workers), record `harness_subagents: true` and **dispatch every reviewer as a fresh subagent** — a same-context review is not a Goldfish review and the validator rejects it. Each subagent receives only the design artifact path, its source references and its persona file from `vendor/elephant-goldfish/agents/`; never conversation history or maker rationale.
3. If the harness truly has no subagent capability, run at least `discipline_gates.goldfish_min_reviewers` separately booted fresh agent contexts sequentially, record `harness_subagents: false`, mode `goldfish-equivalent`, and digest-bound `capability_absence` evidence (the observed capability inventory). When `allow_sequential_fresh_fallback: false`, stop instead: the feature is truthfully blocked.
4. Run the pinned five-phase review (Initial Zoom Out, Comprehension, Design Critique, Intermediate Zoom Out, Implementation Readiness) per reviewer. Reports are artifacts-first, plain English, critique-led, no flattery.
5. Resolve findings with the maker: `fixed` (already reflected in the bound artifact), `accepted-risk`, or `dismissed`, each with a reason and digest-bound evidence. If fixes changed `spec.md`/`playbook.md`, re-review the new bytes — the digest binding stales automatically.
6. Record the receipt (`templates/goldfish-review.json` shape) via `python3 scripts/super_speckit.py record-prerequisite <feature> goldfish-review --artifact <receipt>`.

The gate never replaces runtime QA, the Spec Grill or human judgment; it exposes hidden assumptions before code exists.
