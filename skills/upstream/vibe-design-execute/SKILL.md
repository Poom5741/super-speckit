---
name: vibe-design-execute
description: >-
  Execute a concrete product or UI design request end to end using the project's
  approved Vibe Design foundation: clarify the feature, choose or explore
  structure, create or update the real design/prototype, cover interaction
  states, evaluate rendered evidence, and iterate to a governed stopping point.
  Use this skill whenever a user asks an Agent to design, redesign, prototype,
  or substantially extend a screen, flow, dashboard, app, website, or agentic
  experience—not merely to author foundation documents. Do not use it to deploy,
  ship, or rewrite production systems unless the user separately authorizes
  those actions.
---

# Vibe Design Execute

Run the project’s design knowledge through a real delivery chain:

```text
understand → structure → fill → refine → render → evaluate → return or deliver
```

This is an orchestration skill. It consumes approved declarations and coordinates specialized skills; it does not replace their judgment sources.

Read:

- `references/delivery-routes.md`;
- `assets/FEATURE-RUN.template.md`.

## Specialized skills

Use when relevant:

1. `feature-design-spec`;
2. `design-template-and-variants`;
3. `agentic-interface-foundation` for AI/Agent/GenUI/A2UI work;
4. the appropriate design or prototyping surface available in the environment;
5. `design-artifact-evaluator`.

Consume, rather than recreate:

- `PRODUCT.md`, `DOMAIN.md`, and `DESIGN.md`;
- `CRAFT.md`, `COMPONENTS.md`, `PATTERNS.md`, `TEMPLATES.md`, and `EVAL.md`;
- the approved feature `SPEC.md`.

If a required specialized skill or source is unavailable, state the limitation. Do not pretend a workflow ran.

## Modes

- `exploration`: clarify hypotheses and compare directions; implementation completeness may remain provisional.
- `prototype`: produce a rendered, testable primary flow with visible feedback and representative states.
- `delivery`: produce implementation-ready design detail for the stated scope; release evaluation still determines readiness.
- `update`: change an existing design while preserving approved behavior and documenting the diff.

Confirm the artifact type and maturity before investing in high fidelity.

## Default outputs

Use the project’s native design/code location for the artifact. Keep the process record under:

```text
design/features/<feature-id>/
├── SPEC.md
├── IA-VARIANTS.md          # when explored
├── VISUAL-SPEC.md          # decisions not obvious from the artifact
├── RUN.md                  # sources, gates, gaps, rounds and handoff
└── evaluations/            # evaluator outputs and evidence
```

Do not duplicate information that already has an authoritative source; link to it.

## Phase 0 — Establish readiness

Inspect:

- the request and target artifact;
- existing product and feature documents;
- relevant screens, components, code, prototypes, and review history;
- the available design/prototype/runtime tools;
- intended audience, platform, viewport, and maturity;
- what is authorized: design only, prototype, implementation, or delivery.

Use progressive discovery. Inspect the supplied project entry point before asking
the user for information that the project may already contain. If no project,
design, or runtime entry point is available, ask first for only:

- the smallest artifact or repository access needed to inspect the work; and
- any safety-critical scope ambiguity that would authorize a materially
  different or destructive capability.

At this point, do not also request a role matrix, API contract, design-system
inventory, test plan, or evaluation policy that could be discovered after
access. Do not propose detailed temporary domain rules as a shortcut. If the
request already makes the destructive boundary clear, ask only for the entry
point (or separate authorization to create an isolated, no-side-effect
prototype).

The minimal unblock response should briefly name the evidence-backed work that
will follow—inspection of the existing structure, comparison of structural
alternatives when the task shape is unresolved, non-ideal and accessibility
states, and independent evaluation of a frozen rendered artifact—but must not
draft those decisions before access.

Do not require a complete governance questionnaire merely to obtain project
access. After inspection, group only the still-material gaps into the smallest
decision gate that can safely unlock the next phase.

Create the feature run record. Mark each dependency `approved`, `draft`, `missing`, or `conflicting`.

### Gate A — Scope

Confirm:

- feature boundary and non-goals;
- target artifact and platform;
- maturity and validation expectation;
- evidence gaps that materially affect direction;
- decisions requiring a human owner.

Do not expand design authorization into deployment or production release.
Scale the gate to the requested maturity and actual risk. A missing project
`EVAL.md` does not block a clearly labeled diagnostic review; it only prevents a
governance-grade pass until an evaluation contract is established.

## Phase 1 — Understand and specify

If no approved, adequate feature spec exists, use `feature-design-spec`.

Before moving on, verify:

- primary user, job, and outcome;
- information and decision priority;
- critical journey;
- actions, data, permissions, and risks;
- boundary, failure, recovery, and accessibility states;
- observable acceptance criteria.

An incomplete spec may support exploration, but label which conclusions remain provisional.

## Phase 2 — Choose or explore structure

Use approved templates when they fit. Use `design-template-and-variants` when:

- the page/task shape is new;
- information or action priority is disputed;
- multiple structures have plausible advantages;
- a requested template conflicts with the task.

Compare structural variants at similar fidelity. Record the selected or synthesized direction and approver.

### Gate B — Direction

Confirm the information architecture, primary path, major responsive transformation, and any new template/pattern before detailed visual refinement.

## Phase 3 — Choose the delivery route

Select a direct prototype, professional design-tool, or hybrid route using `references/delivery-routes.md`.

Route by the work’s uncertainty and deliverable—not by habit:

- established system + clear structure favors direct rendered prototyping;
- high visual novelty, illustration, complex spatial composition, or explicit design-file delivery favors a design tool;
- uncertain interaction plus high visual craft may use a hybrid route.

Record which artifact is the current source of truth and how decisions will be synchronized.

## Phase 4 — Build through explicit layers

### A. Skeleton

Establish shell, regions, hierarchy, navigation relationship, reading/decision order, and responsive posture.

### B. Semantic fill

Map real information, domain states, and actions to approved component and pattern roles. Use realistic content supplied by evidence; do not invent production claims or business data.

### C. Interaction and state

Implement or specify:

- primary and alternate paths;
- loading, empty, partial, error, permission, uncertainty, and recovery;
- validation, confirmation, cancellation, retry, undo, and completion;
- keyboard, focus, screen-reader, touch, localization, zoom, and reduced-motion behavior as applicable;
- Agent progress, authorization, provenance, and fallback when agentic.

### D. Visual and craft refinement

Apply `DESIGN.md` tokens and roles and `CRAFT.md` composition rules. Every material choice should trace to an approved rule, a feature-specific proposal, or a visible gap.

### Runtime gap policy

When an approved token, component, pattern, template, behavior, or content rule is missing:

1. confirm that it is genuinely absent;
2. record the gap and affected feature;
3. propose the smallest temporary, clearly labeled decision;
4. obtain the required approval;
5. route reusable learning to the relevant foundation update.

Do not hide the gap in a one-off literal or silently imitate a nearby project.

## Phase 5 — Render and inspect

Produce a real view of the artifact at the relevant viewport and state. Validate that the environment actually renders the latest source of truth.

Before formal evaluation, perform a creator self-check for:

- critical path completeness;
- obvious overflow, broken content, dead actions, and missing feedback;
- declared tokens, components, patterns, and domain semantics;
- representative non-ideal and responsive states;
- unsupported assumptions and unresolved gaps.

Self-check is not the independent gate.

## Phase 6 — Independent artifact evaluation

Use `design-artifact-evaluator` with:

- the original task and approved spec;
- the visible artifact;
- foundation documents;
- required states/viewports;
- current review mode;
- previous round result when iterating.

Keep generation and evaluation roles separate. The evaluator judges visible evidence, not the generator’s hidden plan or persuasive explanation.

## Phase 7 — Iterate under governance

If evaluation returns revision:

1. prioritize blockers and the smallest high-impact return plan;
2. route each finding to spec, structure, component/domain, craft/visual, implementation, or missing evidence;
3. revise the artifact and any explicitly authorized source document;
4. rerender and reevaluate;
5. compare against the best previous round.

Stop according to `EVAL.md`: pass, maximum rounds, plateau, regression, or a question requiring human research/decision. Preserve the best valid version; do not keep a degraded last attempt merely because it is newest.

## Phase 8 — Handoff and learning

Report:

- delivered artifact and maturity;
- source documents and decisions used;
- states, viewports, and paths covered;
- evaluation verdict and evidence;
- unresolved gaps, limitations, and owners;
- approved temporary exceptions;
- reusable findings proposed for PRODUCT, DOMAIN, DESIGN, CRAFT, COMPONENTS, PATTERNS, TEMPLATES, AGENTIC-INTERFACE, or EVAL updates.

Repeated findings are candidates for system improvement, not automatic new standards.

## Boundaries

- Do not skip specification because a prompt sounds visually clear.
- Do not use polish to hide a broken task, unsafe domain rule, or missing state.
- Do not replace approved system assets without a visible proposal and authorization.
- Do not let a design tool, code artifact, or screenshot drift into an undeclared source of truth.
- Do not claim release readiness without the required evaluation evidence.
- Do not deploy, publish, merge, or message external stakeholders unless separately requested and authorized.
