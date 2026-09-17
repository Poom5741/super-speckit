---
name: design-template-and-variants
description: Create or reconstruct reusable page/app-shell templates, select an appropriate template for an approved feature spec, and generate meaningfully different information-architecture variants before detailed UI work. Use this skill whenever a user asks for page structure, layout strategy, app shell, dashboard/list/detail templates, IA alternatives, multiple design directions, or help deciding how a feature should be organized. Do not use it to generate cosmetic theme variants or to bypass an unresolved feature specification.
---

# Design Template and Variants

Turn product tasks into adaptable structural starting points. A pattern explains a recurring solution; a template provides a callable skeleton with named regions, slots, constraints, and adaptation rules. A variant changes task emphasis or information architecture, not merely colors and decoration.

Read:

- `assets/TEMPLATES.template.md` when creating or updating a reusable template library;
- `assets/IA-VARIANTS.template.md` when exploring a concrete feature.

## Modes

- `library-create`: establish reusable templates from approved product needs.
- `reconstruct`: infer candidate templates from existing screens and code without treating every layout as canonical.
- `select`: map an approved feature spec to an existing template.
- `explore`: generate structural variants when no template clearly satisfies the spec.
- `update`: intentionally revise an approved template after evidence exposes a reusable gap.

## Required context

For feature work, prefer:

- approved feature `SPEC.md`;
- `PRODUCT.md`, `DOMAIN.md`, and `DESIGN.md`;
- `CRAFT.md`, `COMPONENTS.md`, and `PATTERNS.md`;
- existing `TEMPLATES.md`;
- platform, navigation, responsive, accessibility, and implementation constraints.

If the primary task, information requirements, or critical path are unresolved, return to `feature-design-spec`. Layout exploration cannot compensate for missing product decisions.

## Outputs

Depending on mode:

- `design/TEMPLATES.draft.md`;
- `design/features/<feature-id>/IA-VARIANTS.md`;
- selected/synthesized direction and decision record;
- updates to project `GAPS.md` when a needed template, component, or pattern is missing.

Do not promote a new template into the reusable library merely because it appeared in one successful feature.
Use contrasting evidence to establish reuse, but do not invent a required
number of screens, tasks, or states unless the project review policy approves
that minimum.

## Template contract

Each reusable template should define:

- task/page shape and entry conditions;
- global shell and navigation relationship;
- primary, secondary, contextual, and transient regions;
- required and optional slots;
- information and action priority;
- supported component/pattern roles;
- density and content-volume range;
- normal, loading, empty, error, permission, and recovery posture;
- responsive transformation rules;
- extension points and prohibited adaptations;
- evidence, examples, maturity, and owner.

Templates are skeletons, not screenshots. Avoid fixed copy, domain data, or decorative values that belong elsewhere.

## Feature exploration workflow

### 1. Extract structural drivers

From the feature spec identify:

- primary job and decision;
- entry, completion, and recovery;
- information that must coexist versus appear progressively;
- high-frequency versus exceptional actions;
- risk, permission, confidence, and provenance needs;
- content volume, density, and viewport constraints;
- collaboration, real-time, or long-running behavior.

### 2. Inspect existing templates

For each plausible template record:

- what it already satisfies;
- required adaptations;
- violated constraints;
- missing components or patterns;
- whether the adaptation would damage the template's original meaning.

Prefer an approved template when it fits the task. Familiarity is useful when it preserves decision order.

### 3. Generate structural variants when needed

Create at least three variants when the information architecture is materially uncertain. Each variant must have a different organizing thesis, such as:

- overview before action;
- work queue before summary;
- exception/risk before normal state;
- guided sequence before open exploration;
- object detail before cross-object comparison.

For every variant specify:

- attention order;
- regions and relationships;
- primary path;
- progressive disclosure;
- non-ideal state posture;
- responsive transformation;
- advantages, risks, and evidence assumptions.

Changing palette, illustration, corner radius, or card styling does not create an IA variant.

The variant count is an exploration tactic for the Agent, not a target-product
policy or template-promotion threshold. Do not copy it into foundation
governance unless an owner explicitly adopts it.

### 4. Make differences visible

Use small wireframes, diagrams, structured region maps, or comparable previews when a design surface is available. Keep content and fidelity comparable so reviewers judge structure rather than polish.

### 5. Compare against the spec

Evaluate each variant against:

- task clarity and completion;
- information priority;
- domain trust, risk, and permission handling;
- state and recovery coverage;
- component/template feasibility;
- craft and accessibility;
- responsive behavior;
- evidence and implementation risk.

Do not average away a broken critical path.

### 6. Decide, synthesize, and hand off

Record one of:

- selected existing template;
- selected variant;
- synthesis with explicit borrowed strengths;
- no viable direction because a product/system decision is missing.

Update the feature spec only when the chosen direction exposes a real specification decision. Do not rewrite requirements to justify a preferred layout.

## Human approval gate

Require product/design approval for:

- primary information and action order;
- a new canonical app shell or page template;
- structural departures from established navigation;
- synthesized direction;
- responsive transformations that change task order;
- knowingly deferred critical states.

## Boundaries

- Do not create visual moodboards; use a visual-direction skill or design surface for that.
- Do not use three cosmetically different versions to simulate exploration.
- Do not force a new task into the nearest template when the task model conflicts.
- Do not copy sample-project content into a reusable template.
- Do not implement the final interface unless `vibe-design-execute` or another implementation workflow is also in scope.
