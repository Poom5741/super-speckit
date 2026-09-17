---
name: design-evaluation-foundation
description: Create or update the reusable evaluation contract that future Agents use to review product and UI design consistently. Use this skill when a team needs EVAL.md, page/task-specific design criteria, evidence requirements, blocking findings, review modes, approval gates, scoring policy, or a standard way to turn design criticism into actionable return plans. Do not use it to review one artifact directly; use design-artifact-evaluator for a rendered artifact or design-system-review for the foundation documents.
---

# Design Evaluation Foundation

Define how design quality will be evidenced, judged, blocked and returned for revision. This skill creates the evaluation standard; it does not grade a particular design.

Read `assets/EVAL.template.md` before drafting.

## Inputs

Prefer approved versions of:

- `design/PRODUCT.md` and `DOMAIN.md`;
- root `DESIGN.md`;
- `design/CRAFT.md`, `COMPONENTS.md`, `PATTERNS.md`, and `TEMPLATES.md`;
- `design/AGENTIC-INTERFACE.md` when applicable;
- user research, support findings and outcome metrics;
- regulatory, accessibility and security requirements;
- historical design-review findings;
- representative good, bad, mixed and boundary examples.

If the foundation documents are drafts, label dependent evaluation rules as provisional.
Keep observed examples separate from policy: an encountered viewport, device,
defect count, support frequency, or artifact can motivate a test case, but
cannot become a required gate or severity threshold without owner approval.

## Outputs

- `design/EVAL.draft.md`, promoted after governance approval;
- updates to `design/DECISIONS.md` and `GAPS.md`;
- optional calibration-case index.

## Workflow

### 1. Define the evaluation target

List the product's meaningful page/task shapes. Examples may include:

- conversion or brand pages;
- task-oriented product screens;
- conversational or agentic workflows;
- data dashboards and diagnostic views;
- content or documentation;
- mobile flows;
- high-risk or permission-sensitive operations.

Do not force every product into a fixed universal page taxonomy. Start from the product's actual jobs.

### 2. Define evidence requirements

Separate evidence layers:

- task/brief and declared intent;
- rendered screenshots at relevant viewports;
- DOM/layout/accessibility facts when applicable;
- key interaction and recovery checks;
- content, data and domain provenance;
- design-system conformance;
- craft, template and Agentic Interface conformance when applicable;
- user or outcome evidence when available.

Automated artifact QA is not proof of user value. Record which conclusions require usability or outcome evidence.

### 3. Define quality dimensions

Use a compact shared language that can trace back to the foundation documents. A common starting point is:

- product intent;
- domain trust and safety;
- information architecture;
- interaction readiness and recovery;
- system craft and accessibility;
- visual and brand expression;
- outcome evidence where appropriate.

Adapt names and weight only when the product context justifies it. Each dimension must contain observable subchecks, evidence expectations and a return destination.

### 4. Define blockers

Blockers capture failures that must not be hidden by a good average score, such as:

- unclear primary task;
- wrong domain or permission logic;
- broken critical path or dead end;
- unreadable or inaccessible content;
- misleading data or untrustworthy AI response;
- missing recovery from failure;
- generic output that ignores the approved design system;
- critical evidence missing;
- severe responsive or rendering failure.

Blockers are governance decisions. Require an authorized owner to approve them.
Until approval, label them `proposed blocker candidates`. The Agent drafting
`EVAL.md` must not apply its own proposed blockers to the same foundation as
though a release policy already existed.

### 5. Define review modes

At minimum distinguish:

- `exploration`: direction and hypotheses; implementation gaps may be non-blocking;
- `prototype`: primary path and visible feedback must work;
- `release`: production data, permissions, accessibility and recovery must be ready.

Review mode changes release policy, not the meaning of quality evidence.

### 6. Define return plans and stopping rules

A failed review should produce a short prioritized return plan with:

- finding and evidence;
- affected dimension and blocker status;
- source document to revisit;
- concrete next action;
- owner or decision needed.

Define when iteration stops: pass with no blockers, maximum rounds, plateau, regression or a decision that requires human research rather than more generation.

### 7. Calibrate

Prepare a balanced case set:

- clear pass;
- clear fail;
- visually strong but task-broken;
- usable but off-brand;
- near-threshold;
- domain- or platform-specific cases.

Calibration should track false pass and false reject decisions. Do not optimize only for a numeric agreement rate.

## Human approval gate

Require explicit approval for:

- dimensions and weights;
- blockers;
- review modes and release thresholds;
- evidence minimums;
- exceptions and escalation paths.
- scoring calculation, rounding, versioning, and round-comparison policy when numerical gates are used.

Record who granted that authority and what scope it covers. Do not infer an
organizational role from the fact that someone requested a draft.

## Boundaries

- Do not invent user research or business metrics.
- Do not reduce design quality to a single score.
- Do not let visual polish offset a broken critical task.
- Do not treat browser QA as a substitute for design judgment.
- Do not let subjective preference become a blocker without product rationale.
- Do not claim the rubric is calibrated until it has been tested on contrasting cases.
