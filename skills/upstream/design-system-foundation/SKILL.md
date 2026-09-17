---
name: design-system-foundation
description: Create, reconstruct, or update a project-specific visual design system and a Google DESIGN.md-compatible source of truth for future Agent-assisted design and implementation. Use this skill whenever a user asks to generate DESIGN.md, infer a design system from existing Figma/UI/code, standardize inconsistent legacy styles, define a new visual identity, migrate visual tokens, or update an existing DESIGN.md. Do not use it for a routine feature design that should consume an already approved DESIGN.md.
---

# Design System Foundation

Produce a project-specific visual source of truth using a project-agnostic method. The output belongs to the target project; the method must not inherit visual values from test fixtures or unrelated projects.

## Read before acting

Read:

- `references/google-design-md-format.md`
- the relevant mode reference: `references/extract-mode.md`, `references/create-mode.md`, or `references/update-mode.md`
- `assets/DESIGN.template.md`

If network access is available, verify the current upstream Google specification because it is still marked `alpha`. If it differs from the bundled summary, follow the current official specification and report the difference.

## Modes

- `extract`: reconstruct a system from existing design evidence.
- `create`: establish a system for a product without an approved visual foundation.
- `update`: intentionally revise an approved `DESIGN.md`.

Select the mode from evidence, not wording alone. If an existing product has a `DESIGN.md` but it is incomplete or contradicted by production, use `update` with an evidence audit rather than silently starting over.

## Inputs

Use whatever authoritative sources are available:

- approved `design/PRODUCT.md` and `design/DOMAIN.md`;
- brand guidance and licensed assets;
- Figma variables, styles, components and representative screens;
- production screenshots and interaction states;
- CSS variables, token files, theme configuration and component code;
- accessibility requirements;
- approved design decisions and historical review findings;
- the current `DESIGN.md` in update mode.

If product context is missing, pause visual finalization and request `product-design-context`. A visual system without product intent is only a style sample.

Keep product evidence separate from method provenance. Google `DESIGN.md`
compatibility is a suite output constraint, not evidence for the target
product's brand, values, scope, or approval. A request to draft the foundation
does not prove that the requester is a design owner or can approve exact visual
values unless that authority is explicitly supplied.

## Outputs

Default outputs:

- root `DESIGN.draft.md`, promoted to `DESIGN.md` after approval;
- `design/AUDIT.md` in extract/update mode;
- updates to `design/EVIDENCE.md`;
- updates to `design/DECISIONS.md`;
- updates to `design/GAPS.md`;
- a visual specimen or preview when a rendering surface is available.

Do not overwrite an approved `DESIGN.md` before showing the proposed changes and receiving authorization.

## Evidence model

For every material visual rule, distinguish:

- `observed value`: what exists;
- `source`: where it exists;
- `frequency/scope`: how broadly it occurs;
- `interpretation`: what role it appears to serve;
- `proposal`: what should become standard;
- `decision`: what a human owner approved;
- `confidence`: high, medium or low.

Repeated use is evidence, not automatic approval. An isolated value may be a deliberate exception; a dominant value may be a widespread legacy mistake.

Do not assign organizational risk levels, release severity, or approval status
unless an authoritative policy or decision supplies that classification.
Describe the evidence, consequence, uncertainty, and decision needed instead.

In extract mode, when exact values conflict and no authorized design owner or
comparative rendered evidence supports a selection:

- do not bind one observed value as the preferred candidate because it is newer,
  more frequent, or already named “primary”;
- do not invent missing font sizes, line heights, weights, spacing, radii, or
  fallback claims merely to complete normative YAML;
- either present observed alternatives with equal status in the audit/preview
  or leave the normative field unresolved;
- mark official lint and value-level validation pending if an incomplete draft
  cannot yet satisfy the format.

An exact candidate may be proposed only when its rationale and comparison
evidence are visible. A prominent concrete token block can become a de facto
standard even when labeled draft, so prefer unresolved roles over unsupported
anchoring.

## Shared workflow

### 1. Confirm scope

Define:

- product/platforms covered;
- light/dark or density themes covered;
- intended consumers: designers, coding agents, design tools and code;
- evidence sources and missing areas;
- selected mode;
- required human approvers.

### 2. Establish or audit visual intent

Translate product intent into explicit visual decisions:

- emotional response and brand personality;
- information density;
- language and localization priorities;
- color temperature and contrast strategy;
- typographic voice;
- shape and surface character;
- motion posture;
- where the product deliberately follows or breaks category conventions.

Avoid empty adjectives such as “premium” or “clean” unless each is connected to observable design consequences.

### 3. Build the token and role model

Define exact values and semantic roles for:

- colors;
- typography;
- spacing and layout;
- rounded corners;
- component visual properties supported by the current Google format.

Use prose for rationale and application guidance. Use YAML for normative values. Do not allow prose and tokens to contradict each other.

For areas not fully represented by the Google schema, keep detailed guidance in prose or companion documents rather than inventing incompatible core fields. Examples include motion systems, responsive behavior, iconography, data visualization and component semantics.

### 4. Test on representative artifacts

Apply the proposed system to contrasting representative artifacts when
possible, such as:

- a primary workflow or dashboard;
- a form, settings or high-density state;
- empty/error/loading states;
- a mobile or narrow viewport.

The artifacts are validation fixtures, not content to copy into the reusable skill.

If no rendering surface is available, provide a preview specification and clearly mark visual validation as pending.

An observed viewport or device is a useful reproduction case, not proof of the
supported range and not a mandatory promotion gate. Record support and release
coverage only from an authoritative requirement or explicit owner decision.
Suggested artifact or alternative counts are working tactics for the current
exploration, not organizational promotion minimums. If an exact minimum matters,
an owner must approve it in the evaluation or review policy.

### 5. Human decision gate

Before finalizing, present:

- visual thesis;
- exact token proposal;
- notable normalization or migration decisions;
- deliberate exceptions;
- unresolved gaps;
- preview evidence;
- known downstream impact.

Record approved decisions with owner and date.

### 6. Validate the document

When the official CLI is available, run:

```bash
npx @google/design.md lint DESIGN.draft.md
```

In update mode also run:

```bash
npx @google/design.md diff DESIGN.md DESIGN.draft.md
```

Do not install packages or access the network without the authorization required by the current environment. If the CLI cannot run, perform a manual structural check and state that official linting is pending.

Validation must check more than file syntax:

- token references resolve;
- text/background combinations are accessible;
- prose matches tokens;
- values have semantic roles;
- component examples use the declared values;
- the system works across representative artifacts;
- unresolved agent defaults are visible.

## Boundaries

- Keep business semantics in `DOMAIN.md`.
- Keep product intent and target users in `PRODUCT.md`, referencing them rather than duplicating them.
- Keep composition, hierarchy, motion purpose, content craft and anti-template rules in `CRAFT.md`.
- Keep component meaning and behavior in `COMPONENTS.md`.
- Keep page and interaction patterns in `PATTERNS.md`.
- Keep callable page/app-shell structures in `TEMPLATES.md`.
- Keep scoring and release rules in `EVAL.md`.
- Never silently codify all legacy values.
- Never generate a final design system from one screenshot.
- Never claim a visual direction is approved because the agent prefers it.
- Never hide missing tokens or unresolved decisions inside implementation literals.
