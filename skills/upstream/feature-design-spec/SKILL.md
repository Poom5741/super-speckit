---
name: feature-design-spec
description: Turn a concrete product, page, workflow, or feature request into an evidence-backed interaction specification before UI generation begins. Use this skill whenever a user asks to design a new feature, screen, flow, dashboard, form, agent interaction, or substantial redesign and the functional success conditions are not already captured in an approved SPEC.md. Also use it to reconstruct or update a missing feature specification from an existing product. Do not use it for a purely cosmetic change whose behavior and acceptance criteria are already approved.
---

# Feature Design Spec

Convert an ambiguous request into an executable definition of what must be true for the experience to work. This skill produces the feature-level declaration consumed by information-architecture, interface-generation, implementation, and evaluation skills.

Read `assets/SPEC.template.md` before drafting.

## Modes

- `create`: define a new feature or workflow.
- `reconstruct`: infer a draft from an existing UI, prototype, code, support history, or product behavior.
- `update`: revise an approved spec because scope, evidence, policy, or product behavior changed.

Do not infer the mode from the user's wording alone. Inspect the target project's documents and artifacts first.

## Inputs

Prefer approved versions of:

- `design/PRODUCT.md` and `design/DOMAIN.md`;
- the request, research, analytics, support evidence, policy, and success measures;
- relevant `DESIGN.md`, `design/CRAFT.md`, `COMPONENTS.md`, `PATTERNS.md`, and `TEMPLATES.md`;
- existing feature specs, UI, prototypes, code, tests, and review findings;
- accessibility, security, privacy, localization, and platform requirements.

If a foundation document is absent, continue only where the evidence is sufficient. Record the missing dependency and its consequence rather than inventing it.

## Outputs

Default outputs:

- `design/features/<feature-id>/SPEC.draft.md`;
- feature-level evidence and open questions inside the spec;
- updates to project `design/GAPS.md` when the request exposes a reusable system gap;
- a short decision request for material unresolved choices.

Promote the draft to `SPEC.md` after the authorized product/design owner approves it. Preserve the previous approved file in update mode and show the proposed change.

## Workflow

### 1. Establish the request boundary

Define:

- user and context;
- triggering situation;
- job and desired outcome;
- problem evidence;
- scope and non-goals;
- maturity target: exploration, prototype, or release;
- known risks, dependencies, and decisions.

Separate requested output from the underlying user need. A request for “a dashboard” does not prove a dashboard is the correct experience.

### 2. Write the six-layer specification

#### L1 — Positioning and intent

State who the experience serves, what changes for them, why it matters now, and which product principles constrain the solution.

#### L2 — Information requirements

Define the information users need to perceive, compare, decide, or act. Describe hierarchy and decision priority without prematurely fixing a page layout.

#### L3 — Core journey

Describe entry conditions, steps, system responses, decision points, completion, cancellation, resumption, and recovery. Use a state table or flow when sequence matters.

#### L4 — Functional responsibilities

List the capabilities the interface must provide. Describe semantic responsibility, content, data, action, and feedback; do not choose a visually convenient component before its responsibility is clear.

#### L5 — Boundary and non-ideal states

Cover applicable states:

- first use and empty;
- loading, long-running, and partial results;
- validation and recoverable error;
- unavailable dependency or offline;
- permission denied and authorization required;
- stale, conflicting, uncertain, or low-confidence data;
- destructive or irreversible action;
- interruption, retry, undo, and rollback;
- localization, long content, responsive, keyboard, and assistive-technology conditions.

Do not create a “screenshot-ready” happy path while leaving operational states undefined.

#### L6 — Acceptance contract

Write observable acceptance criteria for:

- task completion and critical path;
- required information and provenance;
- state coverage and feedback;
- domain, permission, privacy, and safety rules;
- accessibility and responsive behavior;
- design-system and component conformance;
- evaluation evidence required at the stated maturity.

Avoid criteria such as “clean,” “intuitive,” or “modern” unless they are translated into observable consequences or linked to an approved source document.

### 3. Resolve contradictions and uncertainty

For every material claim distinguish:

- confirmed fact;
- evidence-backed observation;
- inference needing confirmation;
- proposed decision;
- unresolved conflict or gap.

When sources disagree, expose the decision and its impact. Frequency alone does not decide correctness.

### 4. Check downstream executability

Confirm that another Agent can answer:

- what must be designed and what must not;
- what the primary task and decision order are;
- which data, states, actions, and permissions matter;
- where human confirmation is required;
- how failure, uncertainty, recovery, and completion behave;
- what evidence will demonstrate acceptance.

If these questions cannot be answered, keep the document as a draft and identify the owner needed.

## Human approval gate

Require approval for:

- feature scope and non-goals;
- critical journey and information priority;
- domain, permission, sensitive-data, and destructive-action rules;
- success and acceptance criteria;
- deliberate exclusions or deferred states.

## Boundaries

- Do not select final visual styling; consume `DESIGN.md` and `CRAFT.md` later.
- Do not turn the first imagined layout into an information requirement.
- Do not manufacture research, metrics, policy, or technical capability.
- Do not implement the interface; hand the approved spec to `design-template-and-variants` or `vibe-design-execute`.
- Do not silently absorb a reusable product/system gap into one feature spec.
