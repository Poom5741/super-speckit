# Design-first protocol

## Purpose

Translate intent into a reviewable visual decision before implementation. This reduces the common agent failure mode of silently choosing hierarchy, navigation, and edge states while writing code.

## Required artifacts

`design-brief.md` defines user, job, flow, assumptions, constraints, design-system sources, and acceptance implications. `prototype.html` is a local static prototype that makes flow/state choices visible. `decision.json` records approver, status, timestamp, source inputs, and exceptions. `handoff-prompt.md` is optional and portable.

## Quality bar

Use repository components and tokens if they exist. Otherwise document provisional tokens instead of pretending they are brand decisions. Show desktop and narrow-screen behavior where relevant; ensure semantic structure, focus order, labels, error messaging, and non-color status cues. The prototype must cover primary, loading, empty, error, and permission-denied states when the feature has them.

## Optional design adapters

v0’s Design Mode supports visual refinements against a running preview and returns reviewable changes. [v0 Design Mode](https://v0.app/docs/design-mode)

Google Stitch supports high-fidelity prompt-driven UI and design-system interchange through `DESIGN.md`. [Google Stitch](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/)

Claude Design supports prototype/wireframe exploration and handoff to Claude Code or a design system. [Claude Design](https://claude.com/product/design)

Use any of them only as a source of options. Save the source/version and review the result against product constraints, accessibility, licensing, and the local design system. No adapter output is merged directly into production code.
