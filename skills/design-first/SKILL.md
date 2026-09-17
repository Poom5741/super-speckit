---
name: super-speckit-design-first
description: Bridge upstream design skills to a reviewable static HTML decision artifact before implementing a UI feature.
---

# Super-SpecKit design-first bridge

This is deliberately not a new design doctrine. It is a small orchestration bridge around the pinned upstream skills recorded in `sources.lock.json`.

1. Use upstream `vibe-design-bootstrap` only when product/design foundations are missing; otherwise use `feature-design-spec` for the feature and `vibe-design-execute` for the design workflow.
2. Use upstream Anthropic `frontend-design` for implementation art direction, respecting the repository’s actual design system.
3. Use the upstream PaulRBerg `frontend-design` in the independent checker lane for rendered browser review; it must not certify its own generated design.
4. Run the local `design-first` helper only to render `prototype.html`, `design-brief.md`, and `decision.json` as review/handoff artifacts. It does not replace the upstream skills or generate production UI.

Read `commands/super-speckit.design-first.md` for the artifact contract. Require a human design decision before UI implementation.
