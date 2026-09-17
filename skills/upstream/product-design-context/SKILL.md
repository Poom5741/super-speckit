---
name: product-design-context
description: Create or reconstruct the product and domain documents that ground later Agent-assisted product and UI design. Use this skill when starting a design foundation, extracting product rules from an existing product, clarifying business semantics, documenting users and jobs, or creating PRODUCT.md and DOMAIN.md for a Vibe Design workflow. Do not use it to choose visual tokens or produce UI styling.
---

# Product Design Context

Create the product and domain truth that other design skills must read before making structural, visual or interaction decisions.

## Outputs

Default outputs:

- `design/PRODUCT.draft.md`
- `design/DOMAIN.draft.md`
- updates to `design/EVIDENCE.md`
- updates to `design/GAPS.md`

After human approval, promote the drafts to `design/PRODUCT.md` and `design/DOMAIN.md`. Never overwrite approved files without showing the proposed diff or replacement scope.

Read the templates in `assets/PRODUCT.template.md` and `assets/DOMAIN.template.md` before drafting.

## Modes

- `reconstruct`: infer a draft from product artifacts, while preserving evidence and uncertainty.
- `create`: establish product and domain rules from a new brief and stakeholder decisions.
- `update`: revise approved context because the product, audience, domain or policy changed.

## Evidence priority

Use this order when sources disagree:

1. explicit decisions from the authorized product/design owner;
2. current legal, security, accessibility and regulatory requirements;
3. approved product strategy and research;
4. current production behavior and authoritative domain systems;
5. repeated patterns in approved designs;
6. isolated legacy copy, screens or implementation details.

Do not silently resolve a meaningful conflict using frequency alone. Record the conflict, its impact and the decision needed.
Treat a role or approval authority as evidence only when it is explicitly
supplied. A request to create a draft authorizes that scoped work; it does not
by itself establish that the requester is the product or design owner.
An unspecified permission is unknown, not an approved denial. The authoring
Agent must not infer authorization or introduce/execute a new action from an
unknown permission, but it also must not rewrite the domain model as “denied by
default.” Record the unresolved action/role cell and return it to the
authoritative policy owner.
In `DOMAIN.md`, record only the unknown cell and its consequence. Put temporary
Agent execution safeguards or UI hypotheses in the feature/component layer and
label them provisional; do not make hidden, disabled, unavailable, or
non-executable presentation an approved domain rule. Never enable a new action
from an unknown permission.

## Workflow

### 1. Establish the product boundary

Determine:

- what the product is and is not;
- target users and contexts;
- primary jobs and desired outcomes;
- business model or organizational purpose where relevant;
- supported platforms and environments;
- non-goals and prohibited behavior;
- success signals and known risks.

Separate product facts from proposed positioning language.
Derived product principles remain inferred or proposed unless an authoritative
source explicitly states them. Do not label an interpretation “confirmed”
merely because it is compatible with an approved job or outcome.

### 2. Model the domain

Identify:

- core entities and relationships;
- canonical terminology and forbidden synonyms;
- states and state transitions;
- roles, permissions and authorization boundaries;
- sensitive data and default exposure rules;
- destructive, irreversible or high-risk actions;
- confidence, provenance and uncertainty requirements;
- compliance and audit expectations;
- locale, language and content constraints.

Do not reduce `DOMAIN.md` to a glossary. Domain rules must explain the consequences of presenting or acting on information incorrectly.

### 3. Mark evidence and confidence

For every material rule, include one of:

- source or evidence reference;
- explicit owner approval;
- confidence level plus an open question.

Use `design/GAPS.md` for unresolved items. A missing fact is not permission for the agent to invent it.

### 4. Check downstream usefulness

Confirm that future agents can answer:

- who is this feature for;
- what task matters most;
- what language should the UI use;
- what data may be shown;
- what actions require confirmation;
- what failure or uncertainty means;
- what the product must never imply or promise.

If these questions remain unanswered, the context is not ready for final approval.

## Human approval gate

Request approval for:

- target-user and product-scope changes;
- business terminology;
- risk and permission rules;
- data sensitivity and disclosure;
- non-goals and success measures.

After approval, record the decision, date and owner in `design/DECISIONS.md` if that file exists, otherwise append an approval record to the relevant document.

## Boundaries

- Do not choose colors, typography, spacing or visual style.
- Do not define detailed component styling.
- Do not turn an aspirational marketing claim into a domain fact.
- Do not infer permissions from visual affordances alone.
- Do not present inferred research conclusions as user evidence.
- Do not invent a risk/severity taxonomy when the organization has not supplied
  one; describe consequence and uncertainty instead.
- Do not extend an approved deprecated/forbidden synonym list by analogy.
  Record additional inconsistent terms as observed migration candidates until
  the domain owner approves their disposition.
