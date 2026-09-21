---
name: super-speckit-design-first
description: Bridge upstream design skills to a reviewable static HTML decision artifact before implementing a UI feature.
---

# Super-SpecKit design-first bridge

This is deliberately not a new design doctrine. It is a small orchestration bridge around the pinned upstream skills recorded in `sources.lock.json`.

1. Use upstream `vibe-design-bootstrap` only when product/design foundations are missing; otherwise use `feature-design-spec` for the feature and `vibe-design-execute` for the design workflow.
2. For a new visual direction, query upstream `ui-ux-pro-max` once for an evidence-backed style, token, type, motion, density, and stack direction. Commit to one direction; do not combine several styles because a catalog happens to offer them.
3. Use upstream Huey specialist skills only for the feature's actual need: `ui-visual-composition` for premium visual craft; `interaction-patterns-components`, `forms-inputs-checkout`, or `information-architecture-navigation` for their named UX surfaces; `ux-writing-content-design` for user-facing copy; `accessibility-inclusive-design` for inclusive behavior; and `design-systems-frontend-architecture` for reusable UI foundations. Use `ux-research-discovery-testing` before inventing user assumptions.
4. Use upstream Anthropic `frontend-design` for implementation art direction, respecting the repository’s actual design system. Do not let a skill's preferred component library or stack replace the project stack without authorization.
5. Use the upstream PaulRBerg `frontend-design` and `design-artifact-evaluator` in the independent checker lane for rendered browser review; they must not certify their own generated design.
6. Run the local `design-first` helper only to render `prototype.html`, `design-brief.md`, and `decision.json` as review/handoff artifacts. It does not replace the upstream skills or generate production UI.

Read `commands/super-speckit.design-first.md` for the artifact contract. Require a human design decision before UI implementation.
