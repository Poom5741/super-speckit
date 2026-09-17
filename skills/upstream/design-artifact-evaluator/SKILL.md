---
name: design-artifact-evaluator
description: Independently evaluate a rendered product or UI artifact by collecting browser/device evidence, checking real structure and interactions, applying the project's EVAL.md subchecks and blockers, producing a deterministic verdict and prioritized return plan, and comparing iteration rounds. Use this skill whenever a user asks to review, QA, score, validate, approve, release-gate, or iteratively improve a real screen, flow, prototype, website, app, or generated interface. Do not use it to author the evaluation standard or silently fix the artifact while judging it.
---

# Design Artifact Evaluator

Operate the evidence and release side of the Vibe Design loop:

```text
freeze artifact → collect facts → review visible experience
→ compute policy → apply blockers → report → return/stop
```

Read:

- `references/evidence-protocol.md`;
- `references/scoring-runtime.md`;
- `assets/EVALUATION-REPORT.template.md`;
- `assets/evaluation-output.schema.json` when structured output is needed.

Use `scripts/recompute-scores.mjs` when numerical subcheck scores are present. It recomputes the ledger and detects inconsistencies without deciding the governance verdict.

## Role isolation

Evaluate only:

- task/request and approved feature `SPEC.md`;
- declared review mode and scope;
- visible/runnable artifact at an identified version;
- approved foundation documents;
- collected browser/device evidence;
- previous evaluation result when comparing rounds.

Do not rely on the generator’s hidden plan, private reasoning, effort, or post-hoc explanation. Missing visible evidence remains missing.

Default to report-only. The evaluator must not modify the artifact or governing standards in the same review unless the user separately authorizes a clearly separated fix-and-rerun phase.

## Review modes

Read the project's `EVAL.md`. Common modes are:

- `exploration`: assess direction and major risks; incomplete implementation may be allowed when explicit.
- `prototype`: require a real primary path, visible feedback, and representative recovery.
- `release`: require production-appropriate data, behavior, accessibility, permissions, recovery, and evidence.

The mode changes readiness policy, not the truth of the evidence.

## Outputs

Create a round-specific record:

```text
design/features/<feature-id>/evaluations/round-<n>/
├── evidence/
│   ├── manifest.md
│   ├── screenshots/
│   ├── dom-layout.md
│   ├── page-profile.md
│   └── interaction-smoke.md
├── evaluation.json
├── score-calculation.json
└── EVALUATION.md
```

Adapt paths when the project has an established convention. Never overwrite prior rounds.

## Workflow

### 1. Establish evaluation authority and scope

Record:

- artifact location, version/commit/frame, and source of truth;
- task, feature spec, and maturity;
- required states, paths, viewports, themes, locales, and modalities;
- evaluation standard and policy version;
- allowed test accounts/data and prohibited side effects;
- previous round and current best version.

If release-critical scope or authority is unknown, return `BLOCKED` rather than inventing it.

### 2. Freeze and render the target

Use the environment’s available browser, device, preview, or design-inspection capability. Confirm that the rendered target corresponds to the stated source version.

Wait for meaningful stability without hiding long-running behavior. Record network, font, fixture, authentication, feature-flag, and environment limitations that could change evidence.

Do not run destructive, paid, external-message, or real-user actions merely to complete a smoke test. Use a safe test environment, fixture, mock, or mark the evidence unavailable.

### 3. Collect deterministic evidence

Follow `references/evidence-protocol.md` and collect applicable layers:

- DOM/layout/accessibility facts;
- page/content profile;
- key interaction and recovery smoke;
- screenshots or device captures;
- console, page, resource, and runtime failures;
- data provenance and content truth checks;
- design-system conformance facts.

Evidence collection must identify viewport/state/path and reproducible steps. A screenshot without context is not a complete finding.

### 4. Establish evidence sufficiency

For every required subcheck mark evidence:

- `present`;
- `partial`;
- `conflicting`;
- `missing`;
- `not_applicable` with rationale.

Apply the `EVAL.md` missing-evidence policy. Do not award a pass because a state was never inspected.

### 5. Evaluate subchecks

Use the project’s page/task shape, dimensions, subchecks, and weights. For each subcheck provide:

- verdict or score on the approved scale;
- direct evidence reference;
- deduction reason;
- why the result is not stronger;
- recommendation;
- return destination.

Browser QA provides facts; design judgment explains their product impact. Neither substitutes for the other.

If no approved `EVAL.md` exists, produce a clearly labeled diagnostic review using the provisional dimensions in `references/scoring-runtime.md`. It cannot authorize release.

### 6. Recompute policy deterministically

Use the calculation and blocker policy approved in `EVAL.md`. When numerical scoring is enabled:

- calculate from recorded subchecks rather than asking the review model for an intuitive total;
- apply page/task-shape weights exactly;
- record all inputs and formulas;
- apply blocker and missing-evidence overrides after score calculation;
- validate structured output against the schema when tooling is available.

Run:

```bash
node scripts/recompute-scores.mjs <path-to-evaluation.json>
```

Save the returned ledger as `score-calculation.json`. Resolve every reported inconsistency before issuing a verdict. The helper deliberately does not choose `PASS`, `REVISE`, or `BLOCKED`; apply the approved `EVAL.md` threshold, blocker, and missing-evidence policy to the verified calculations.

If weights, thresholds, or mappings are absent, report dimension-level results and governance gaps; do not invent a precise overall score.

### 7. Decide the gate

Use the project’s verdict vocabulary. Unless overridden, the compatible set is:

- `PASS`;
- `PASS_WITH_FOLLOW_UP`;
- `REVISE`;
- `BLOCKED`.

State the score, threshold, mode, and blocker result separately. A high average cannot cancel a blocker.

### 8. Produce a prioritized return plan

For a non-pass result, return a small ordered set containing:

- finding and evidence;
- affected task/dimension and blocker status;
- user/product impact;
- source or generation stage to revisit;
- concrete next action;
- owner or human decision required;
- expected evidence for the next round.

Avoid broad instructions such as “improve UX” or an unranked list of every imperfection.

### 9. Compare rounds and stop

When a previous round exists:

- compare the same subchecks and evidence scope;
- identify fixed, unchanged, regressed, and newly exposed findings;
- retain the best valid artifact/version;
- distinguish real improvement from missing evidence or changed scope.

Apply approved stop rules: pass, maximum rounds, plateau, regression, unavailable evidence, or human research/decision required. The evaluator recommends the stop state; the authorized owner decides exceptions.

### 10. Return learning candidates

Classify recurring findings as possible updates to:

- SPEC;
- PRODUCT or DOMAIN;
- DESIGN or CRAFT;
- COMPONENTS, PATTERNS, or TEMPLATES;
- AGENTIC-INTERFACE;
- EVAL or evidence tooling.

A repeated failure is a candidate for governance review, not automatic permission to rewrite the standard.

## Boundaries

- Do not give PASS from a static source-code reading when rendered evidence is required.
- Do not reduce design quality to browser lint or a single score.
- Do not let visual polish offset a broken path, unsafe domain logic, or inaccessible content.
- Do not fabricate screenshots, clicks, user research, analytics, or test results.
- Do not penalize unsupported platforms outside the declared scope; record the limitation.
- Do not expose private generator reasoning in the report.
- Do not mutate the artifact during the independent evaluation phase.
