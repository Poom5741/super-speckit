---
description: Generate an HTML design decision artifact before UI implementation.
---

Read the feature spec, users, flows, existing components, accessibility requirements, and declared design-system sources. Create `.super-speckit/design/<feature>/design-brief.md`, `prototype.html`, and `decision.json`. The HTML must be a static, navigable prototype using only synthetic content and clearly labelled assumptions—not production application code or a claim that the flow is implemented.

Before the local artifact, use the pinned design routing in `skills/design-first/SKILL.md`: foundation/spec skills first, then one UI/UX Pro Max direction for new surfaces, and only the relevant specialist UX skills. Record the chosen visual thesis, token/design-system source, and specialist constraints in the brief. Do not combine incompatible style directions or let an upstream skill replace the project's framework, component library, or approved design system.

Include problem, target users, information hierarchy, primary/error/empty/loading states, responsive behavior, keyboard/accessibility notes, components/tokens reused, and acceptance assumptions. Produce at least one concrete direction; produce alternatives only when the decision is genuinely open.

If configured, create an adapter-neutral `handoff-prompt.md` for v0, Stitch, or Claude Design. Do not call a vendor unless separately configured and authorized. Importing a generated design requires recording source, version/link, license/brand constraints, and a human design decision: `approved`, `revise`, or `not-required`. Only `approved` permits UI implementation.
