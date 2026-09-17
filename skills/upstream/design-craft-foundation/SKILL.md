---
name: design-craft-foundation
description: Create, reconstruct, or update the product's explicit craft standard for hierarchy, composition, typography usage, density, content, motion, feedback, accessibility, and resistance to generic AI-looking output. Use this skill whenever a team needs CRAFT.md, wants to turn subjective critique such as “too generic,” “not refined,” or “lacks hierarchy” into executable rules, or needs reusable quality guidance beyond tokens and component semantics. Do not use it to choose brand tokens, define business meaning, or critique only one artifact.
---

# Design Craft Foundation

Create the shared judgment source for how approved design ingredients are composed with quality. `DESIGN.md` defines visual identity and values; `CRAFT.md` defines how those values are used to create hierarchy, rhythm, clarity, feedback, and an appropriate distinctive character.

Read:

- `assets/CRAFT.template.md`;
- `references/craft-dimensions.md`.

Consult the referenced Playbook lexicon only when a term needs precise clarification. Treat it as vocabulary, not as a universal style mandate.

## Modes

- `reconstruct`: derive candidate craft rules from representative artifacts and review history.
- `create`: establish a craft thesis from product intent, domain needs, brand direction, accessibility, and deliberate examples.
- `update`: revise approved rules after repeated findings, a platform change, new evidence, or an intentional quality-direction change.

## Inputs

Prefer:

- approved `PRODUCT.md`, `DOMAIN.md`, and `DESIGN.md`;
- representative good, weak, and edge-case screens;
- design-review comments and recurring implementation failures;
- content guidelines and localization constraints;
- platform, accessibility, performance, and motion requirements;
- approved component and pattern documents;
- user research or outcome evidence where available.

Existing polish is evidence, not proof. A repeated “card wall” can be a repeated mistake.

## Outputs

Default outputs:

- `design/CRAFT.draft.md`, promoted after approval;
- updates to `design/EVIDENCE.md`, `DECISIONS.md`, and `GAPS.md`;
- a compact before/after or pass/fail specimen brief when visual rendering is available.

Do not silently overwrite an approved craft standard.

## Rule model

Every material craft rule should identify:

- purpose and quality risk;
- observable guidance;
- applicability and exceptions;
- positive and negative evidence;
- related token, component, pattern, or domain rule;
- evaluation check;
- owner and approval status.

Translate adjectives into consequences. “Calm” might mean fewer simultaneous emphasis levels and restrained motion in one product, but greater whitespace in another; the adjective alone is not executable.

## Workflow

### 1. Establish the craft thesis

Define:

- the attention and reading behavior the product should support;
- the appropriate relationship between utility, expression, trust, and density;
- which category conventions help comprehension;
- where the product should be distinctive;
- which generic generation tendencies would damage product fit.

Avoid treating novelty as quality. Distinctiveness must serve product intent.

### 2. Define craft dimensions

Cover the dimensions relevant to the product:

- typography in use;
- information hierarchy and emphasis;
- composition, grouping, alignment, and whitespace;
- density, rhythm, and repetition;
- surfaces, borders, depth, and material restraint;
- iconography, imagery, data visualization, and decorative effects;
- content design, labels, numbers, provenance, and empty-state language;
- motion purpose, timing roles, continuity, and reduced-motion behavior;
- feedback, progress, confirmation, interruption, and recovery;
- responsive composition, zoom, keyboard, contrast, touch, and assistive technology;
- anti-template and product-specific expression.

Do not force irrelevant categories into the document for completeness.

### 3. Convert critique into checks

Replace vague feedback with observable questions. Examples:

- Can a first-time user identify the primary task before secondary metrics?
- Does each emphasis treatment correspond to a real difference in importance or action?
- Are repeated containers communicating groups, or merely filling space?
- Does motion explain state, continuity, or causality?
- Are data source, freshness, units, uncertainty, and comparison bases legible?
- Does responsive behavior preserve decision order instead of only shrinking geometry?

These examples illustrate the form of a check; adapt them to the target product.

### 4. Define anti-default safeguards

Identify likely generic output patterns for the product, such as:

- equal-weight cards without task hierarchy;
- ornamental gradients or glow without semantic purpose;
- decorative oversized copy that displaces essential information;
- excessive pills, badges, borders, or shadows;
- uniform section rhythm that makes unlike content look equivalent;
- motion added for spectacle rather than comprehension;
- invented marketing copy, metrics, or imagery.

Record the product-specific alternative. Do not ban a visual technique universally; ban unsupported use.
When evidence does not establish product-specific harm, keep the item as a
review question or example rather than promoting it to a normative rule.
In reconstruct mode, do not invent prohibitions against pills, gradients, glow,
illustration, large headings, cards, or motion merely because they are common
generic-output risks. A normative prohibition needs product-specific evidence,
an approved direction, or a recorded owner decision.

### 5. Validate on contrasting artifacts

Use at least:

- one primary or high-frequency task;
- one dense, constrained, or data-heavy state;
- one non-ideal or recovery state;
- one narrow or alternative viewport when relevant.

When possible include one intentionally weak fixture. A craft standard that only explains an already polished hero screen is not reusable.

### 6. Connect craft to evaluation

For each rule identify:

- required evidence;
- related quality dimension and subcheck;
- what constitutes pass, partial, or fail;
- whether failure can block release or only reduce quality;
- where a finding should return.

Keep actual scoring and release policy in `EVAL.md`.
Do not assign high/medium/low risk or release-blocking status unless an approved
evaluation policy defines it. A draft `EVAL.md` can propose a classification,
but the authoring Agent must not apply that proposal as if it were approved.

## Human approval gate

Require design-owner approval for:

- craft thesis and deliberate category departures;
- rules that constrain visual exploration;
- release-blocking craft findings;
- deprecated conventions;
- exceptions that will be reused across features.

## Boundaries

- Keep exact normative values and visual roles in `DESIGN.md`.
- Keep component selection meaning in `COMPONENTS.md`.
- Keep page structures in `PATTERNS.md` and `TEMPLATES.md`.
- Keep feature success conditions in the feature `SPEC.md`.
- Do not encode one designer's taste as a universal law without product rationale and contrasting evidence.
- Do not claim the rules are calibrated until reviewers have tested them on mixed-quality examples.
