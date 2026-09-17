---
description: Generate an HTML design decision artifact before UI implementation.
---

Read the feature spec, users, flows, existing components, accessibility requirements, and declared design-system sources. Create `.super-speckit/design/<feature>/design-brief.md`, `prototype.html`, and `decision.json`. The HTML must be a static, navigable prototype using only synthetic content and clearly labelled assumptions—not production application code or a claim that the flow is implemented.

Include problem, target users, information hierarchy, primary/error/empty/loading states, responsive behavior, keyboard/accessibility notes, components/tokens reused, and acceptance assumptions. Produce at least one concrete direction; produce alternatives only when the decision is genuinely open.

If configured, create an adapter-neutral `handoff-prompt.md` for v0, Stitch, or Claude Design. Do not call a vendor unless separately configured and authorized. Importing a generated design requires recording source, version/link, license/brand constraints, and a human design decision: `approved`, `revise`, or `not-required`. Only `approved` permits UI implementation.
