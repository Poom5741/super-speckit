#!/usr/bin/env node

import fs from "node:fs";

const inputPath = process.argv[2];

if (!inputPath) {
  console.error("Usage: node recompute-scores.mjs <evaluation.json|->");
  process.exit(2);
}

const raw = inputPath === "-"
  ? fs.readFileSync(0, "utf8")
  : fs.readFileSync(inputPath, "utf8");

let evaluation;

try {
  evaluation = JSON.parse(raw);
} catch (error) {
  console.error(`Invalid JSON: ${error.message}`);
  process.exit(2);
}

if (!Array.isArray(evaluation.dimensions) || evaluation.dimensions.length === 0) {
  console.error("evaluation.dimensions must be a non-empty array");
  process.exit(2);
}

const tolerance = 0.005;
const discrepancies = [];
const dimensions = evaluation.dimensions.map((dimension, dimensionIndex) => {
  if (!Array.isArray(dimension.subchecks) || dimension.subchecks.length === 0) {
    console.error(`dimensions[${dimensionIndex}].subchecks must be a non-empty array`);
    process.exit(2);
  }

  let earned = 0;
  let possible = 0;

  for (const [subcheckIndex, subcheck] of dimension.subchecks.entries()) {
    if (
      typeof subcheck.score !== "number"
      || !Number.isFinite(subcheck.score)
      || typeof subcheck.max_score !== "number"
      || !Number.isFinite(subcheck.max_score)
      || subcheck.max_score <= 0
      || subcheck.score < 0
      || subcheck.score > subcheck.max_score
    ) {
      console.error(
        `dimensions[${dimensionIndex}].subchecks[${subcheckIndex}] requires `
        + "0 <= score <= max_score and max_score > 0",
      );
      process.exit(2);
    }

    earned += subcheck.score;
    possible += subcheck.max_score;
  }

  const computedScore = (earned / possible) * 10;

  if (
    typeof dimension.score === "number"
    && Math.abs(dimension.score - computedScore) > tolerance
  ) {
    discrepancies.push({
      field: `dimensions.${dimension.id ?? dimensionIndex}.score`,
      recorded: dimension.score,
      computed: computedScore,
    });
  }

  return {
    id: dimension.id ?? String(dimensionIndex),
    label: dimension.label ?? dimension.id ?? String(dimensionIndex),
    earned,
    possible,
    computed_score: computedScore,
    weight: typeof dimension.weight === "number" ? dimension.weight : null,
  };
});

const weightedDimensions = dimensions.filter(
  (dimension) => typeof dimension.weight === "number"
    && Number.isFinite(dimension.weight)
    && dimension.weight >= 0,
);

let overallScore = null;
let weightTotal = null;

if (weightedDimensions.length === dimensions.length) {
  weightTotal = weightedDimensions.reduce(
    (sum, dimension) => sum + dimension.weight,
    0,
  );

  if (weightTotal <= 0) {
    console.error("Dimension weights must have a positive total");
    process.exit(2);
  }

  overallScore = weightedDimensions.reduce(
    (sum, dimension) => sum + dimension.computed_score * dimension.weight,
    0,
  ) / weightTotal;

  if (
    typeof evaluation.overall_score === "number"
    && Math.abs(evaluation.overall_score - overallScore) > tolerance
  ) {
    discrepancies.push({
      field: "overall_score",
      recorded: evaluation.overall_score,
      computed: overallScore,
    });
  }
} else if (weightedDimensions.length > 0) {
  discrepancies.push({
    field: "dimensions.weight",
    recorded: `${weightedDimensions.length}/${dimensions.length} dimensions weighted`,
    computed: "all dimensions must declare weights before overall score is calculated",
  });
}

const activeBlockers = Array.isArray(evaluation.blockers)
  ? evaluation.blockers
    .filter((blocker) => blocker?.active === true)
    .map((blocker) => blocker.id)
  : [];

const result = {
  calculation_version: "1",
  source: inputPath,
  dimensions,
  weight_total: weightTotal,
  computed_overall_score: overallScore,
  evidence_sufficiency: evaluation.evidence_sufficiency ?? null,
  active_blockers: activeBlockers,
  consistency: {
    matches_recorded_scores: discrepancies.length === 0,
    discrepancies,
  },
  governance_note:
    "Apply the approved EVAL.md threshold, blocker, missing-evidence, and exception policy. "
    + "This calculation does not issue a release verdict.",
};

process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
