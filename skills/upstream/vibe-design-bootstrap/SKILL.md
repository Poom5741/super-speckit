---
name: vibe-design-bootstrap
description: Coordinate the creation or reconstruction of a complete, reusable Vibe Design documentation foundation for a product. Use this skill whenever a team wants to standardize design work, bootstrap design documentation, rebuild standards from existing UI, start a design system for a new product, or prepare a project for Agent-assisted product and UI design. Do not use it for a routine single-screen design task when approved foundation documents already exist.
---

# Vibe Design Bootstrap

Create the documentation foundation that future design and implementation agents will use. This is an orchestration skill: it coordinates specialized skills and protects the dependency order between their outputs.

## Scope

Use one of three modes:

- `reconstruct`: the product has existing designs, code, components, or brand assets but lacks reliable documentation.
- `create`: the product is new and needs a design foundation from first principles.
- `update`: approved foundation documents exist and a deliberate revision is required.

Do not choose a mode from a keyword alone. Inspect the supplied evidence and existing documents first. If multiple modes are plausible, state the evidence and ask the user to confirm the mode before writing final files.

## Required specialized skills

Run these workflows in order when available:

1. `product-design-context`
2. `design-system-foundation`
3. `design-craft-foundation`
4. `component-pattern-foundation`
5. `design-template-and-variants` in library/reconstruction mode
6. `agentic-interface-foundation` when the product includes AI/Agent/GenUI behavior
7. `design-evaluation-foundation`
8. `design-system-review`

If a specialized skill is unavailable, do not pretend it ran. Report the missing capability and either stop or complete only the explicitly authorized subset.

## Phase 1: Intake and evidence inventory

Inspect the target project's available sources:

- product brief, research, analytics, requirements and business rules;
- approved brand guidance;
- Figma files, variables, components and prototypes;
- production screenshots and representative flows;
- code tokens, CSS variables, themes and component implementations;
- accessibility or regulatory requirements;
- historical design review comments;
- existing `DESIGN.md` or companion documents.
- Agent capabilities, renderer constraints, and action/authorization policy when relevant.

Create or update `design/EVIDENCE.md`. For each source record its location, authority, freshness, scope and reliability.

Classify every important observation as one of:

- `confirmed`: explicitly approved or present in an authoritative source;
- `observed`: consistently present but not formally approved;
- `inferred`: a reasoned interpretation that requires confirmation;
- `conflicting`: credible sources disagree;
- `missing`: required information is unavailable.

Never turn `observed` or `inferred` evidence into a final standard without an approval record.
Treat a source that was not supplied as `missing` or `not provided`, not as proof that
the source or artifact does not exist. Record absence as `confirmed` only when an
authoritative source explicitly establishes it.

Keep product evidence separate from workflow provenance. A user request can
authorize the requested draft work, but it does not establish the requester's
organizational role, design-owner status, or authority to approve product rules
unless that role and authority are explicitly supplied. Likewise, this suite's
document shapes, Google `DESIGN.md` compatibility, and validation methods are
method constraints—not evidence about the target product. Record them as such.
Keep method provenance in the concise generation handoff or foundation front
door, not in the target product's evidence ledger or decision register. Do not
present internal workflow labels such as Gate A/B/C as the organization's
policy unless an authorized owner has adopted them.
Never place Vibe Design, Skill, Google-format, CLI, or validator provenance in
`EVIDENCE.md`, `PRODUCT.md`, `DOMAIN.md`, or the product decision ledger. Those
files describe the target product. If method provenance is useful, keep it in a
clearly separate generation note and omit it when the recipient only needs the
foundation.

## Gate A: Confirm scope and mode

Before creating standards, present:

- selected mode and why;
- target products/platforms;
- evidence coverage and blind spots;
- intended output files;
- decisions that will require design-team approval.

Continue after the user or designated design owner confirms the scope.

## Phase 2: Establish product and domain truth

Use `product-design-context` to produce draft `PRODUCT.md` and `DOMAIN.md` before visual-system work. Visual choices need a product purpose and domain boundary; otherwise they become decoration without responsibility.

## Phase 3: Establish visual identity and craft

Use `design-system-foundation` in the selected mode. It must create a Google
`DESIGN.md`-compatible draft and supporting audit, decisions and gaps. Treat
format compatibility as an output constraint; do not use it to fill unsupported
product decisions. In reconstruction mode, distinguish approved rules,
candidate patterns, legacy accidents, and unresolved conflicts. In create mode,
show coherent alternatives before selecting one.

Use `design-craft-foundation` to translate hierarchy, composition, typography usage, density, content, motion, feedback, accessibility, and anti-template judgment into executable rules. Keep exact visual values in `DESIGN.md` and composition quality in `CRAFT.md`.

## Gate B: Confirm design direction

Do not finalize `DESIGN.md` until the design owner confirms:

- visual intent;
- palette and typography roles;
- density, spacing and shape language;
- craft thesis and product-specific expression;
- component visual strategy;
- deliberate exceptions and unresolved gaps.

## Phase 4: Establish component, pattern and template semantics

Use `component-pattern-foundation` after product/domain truth and visual roles are stable. It should describe when components and patterns are correct, not merely list available assets.

Use `design-template-and-variants` in library-create or reconstruct mode to establish a small, evidence-backed set of callable shells and page/task templates. Do not turn every historical screen into a canonical template.

Default the document set's concise front door to `design/README.md`. Tell a
reader what is approved, proposed, usable now, awaiting a decision, and
prohibited. Keep source metadata in `EVIDENCE.md`; keep approved product and
domain rules only in `PRODUCT.md` and `DOMAIN.md`. Other documents may state the
local design consequence and stable rule ID, but must link instead of
retranscribing the rule. Omit empty boilerplate and defer unsupported sections
to `GAPS.md`. This preserves separation without creating a repetitive package
that can drift.

## Phase 5: Establish Agentic Interface contract when relevant

If the product contains conversational Agents, autonomous actions, dynamic UI, generated reports, or human-in-the-loop decisions, use `agentic-interface-foundation`. Define generation freedom, user control, authorization, lifecycle, declaration/rendering boundaries, fallbacks, and evidence requirements.

Do not add this document merely to make a stable product appear “AI-native.”
Absence in the current scope means “not applicable to this draft,” not a
permanent prohibition on a future, separately authorized product change.

## Phase 6: Establish evaluation contract

Use `design-evaluation-foundation` to define evidence requirements, quality dimensions, blockers and approval modes. Thresholds and blockers are governance decisions; require human confirmation.

Observed examples—including viewports, devices, artifacts, defect counts, or
support frequency—may become proposed test cases. They do not become supported
scope, severity levels, promotion requirements, or release gates without an
explicit owner decision.

## Phase 7: Make migration reversible

In reconstruction or update mode, the migration proposal must identify for each
pilot or slice:

- compatibility boundary and affected consumers;
- rollout and rollback mechanism;
- evidence-based rollback triggers proposed for owner approval;
- observation and validation window, without inventing its duration;
- accountable rollout and rollback owner;
- data/content preservation requirements;
- restore verification and residual legacy usage.

If these details depend on engineering discovery, record them as preflight
requirements. Do not call a high-level phase list an executable rollback plan.

## Gate C: Independent review

Freeze and identify the candidate document set, then hand it to a reviewer in a
separate reasoning context who did not author or revise that candidate. Use
`design-system-review` only in that separated context.

The authoring Agent must not create `REVIEW.md`, claim independence, or issue a
formal Gate C verdict in the same reasoning pass that creates the foundation.
It may run a clearly labeled author self-check, but that self-check must not use
the independent-review template or substitute for Gate C. If a separate Agent,
thread, or human reviewer is unavailable, leave `REVIEW.md` absent, record
`Gate C: pending`, and hand off the frozen candidate for later review.

Perform author integrity checks internally and summarize only validation
actually performed. Do not create a separate `SELF-CHECK.md` by default; write
one only when the user or an adopted team process requires a durable record,
and do not repeat the foundation contents inside it.

Only findings backed by an approved review or evaluation policy are formal
blockers. Otherwise report advisory readiness limitations and the decision
needed. Do not imply that design-draft authorization also authorizes release.

## Final report

Report:

- mode used;
- sources inspected and major evidence gaps;
- files created or changed;
- decisions approved;
- unresolved gaps and owners;
- validation actually performed;
- next recommended pilot task.

Keep this report concise and link to the authoritative files instead of
reproducing their contents. Do not claim the foundation is validated merely
because all files exist, and do not describe a proposed control as approved.
