# Scoring and gate runtime

Primary inspiration:

- Vibe Designing Playbook, page shapes and dimensions: https://alibaba-cloud-design.github.io/vibe-designing-playbook/#sec-3.2
- Vibe Designing Playbook, gate and return plan: https://alibaba-cloud-design.github.io/vibe-designing-playbook/#sec-3.4
- Vibe Designing Playbook, isolation and calibration: https://alibaba-cloud-design.github.io/vibe-designing-playbook/#sec-3.5

The project’s approved `EVAL.md` is authoritative. Use this reference only as a compatible default or diagnostic fallback.

## Provisional shared dimensions

1. Product intent.
2. Domain trust and safety.
3. Information architecture.
4. Interaction readiness and recovery.
5. System craft and accessibility.
6. Visual and brand expression.

Add outcome evidence only when real user or business evidence is available. Do not infer it from artifact polish.

## Subcheck model

A compatible provisional scale is:

- `0`: failed or contradicted by evidence;
- `1`: partial, fragile, or incompletely evidenced;
- `2`: meets the defined criterion with sufficient evidence.

When the approved project scale differs, use it instead.

If a dimension uses the 0–2 model:

```text
dimension_score = sum(subcheck_score) / sum(subcheck_max) * 10
```

If page-shape weights sum to 1:

```text
overall_score = sum(dimension_score * dimension_weight)
```

Keep full precision in calculation and apply the project’s display rounding only at the end.

## Gate order

1. Check required evidence.
2. Calculate subchecks.
3. Aggregate dimensions.
4. Apply page/task-shape weights.
5. Compare threshold for the declared review mode.
6. Apply blocker overrides.
7. Apply missing-evidence and authority policy.
8. Produce verdict and return plan.

Scores and blockers answer different questions. Report both.

## Blocker characteristics

A blocker is an approved policy condition such as:

- unclear or contradicted primary task;
- broken critical path;
- wrong permission, risk, or domain behavior;
- misleading or untrustworthy result;
- inaccessible critical content/action;
- missing recovery from material failure;
- severe rendering failure;
- unsupported design-system substitution;
- required evidence absent.

Do not invent a blocker from personal taste.

## Round comparison

Compare stable identifiers for subchecks and findings. If the scope, fixture, or policy changed, disclose that the scores are not directly comparable. Preserve the best artifact that satisfies blockers and scope, not merely the highest rounded number.
