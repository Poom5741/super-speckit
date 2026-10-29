import assert from "node:assert/strict";
import test from "node:test";
import { CardContractWireSchema, fingerprintCard, parse } from "./index.ts";

test("card fingerprints ignore object key and dependency presentation order", () => {
  const first = parse(CardContractWireSchema, {
    schemaVersion: 1,
    repository: "Poom5741/super-speckit",
    issueNodeId: "I_kwDOExample",
    issueNumber: 42,
    title: "Durable handoff",
    kind: "feature",
    outcome: "A writer moves without duplicate ownership.",
    nonGoals: ["automatic production deployment", "hosted coding"],
    acceptance: ["The source stops before the destination writes."],
    dependencies: ["I_dependency_b", "I_dependency_a"],
    baseRef: "main",
    capability: "runtime",
    risk: "high",
  });
  const second = parse(CardContractWireSchema, {
    risk: "high",
    capability: "runtime",
    baseRef: "main",
    dependencies: ["I_dependency_a", "I_dependency_b"],
    acceptance: ["The source stops before the destination writes."],
    nonGoals: ["hosted coding", "automatic production deployment"],
    outcome: "A writer moves without duplicate ownership.",
    kind: "feature",
    title: "Durable handoff",
    issueNumber: 42,
    issueNodeId: "I_kwDOExample",
    repository: "Poom5741/super-speckit",
    schemaVersion: 1,
  });

  assert.equal(fingerprintCard(first).value, fingerprintCard(second).value);
});

test("card parsing rejects an empty acceptance contract", () => {
  assert.throws(() => parse(CardContractWireSchema, {
    schemaVersion: 1,
    repository: "Poom5741/super-speckit",
    issueNodeId: "I_kwDOExample",
    issueNumber: 42,
    title: "Broken card",
    kind: "feature",
    outcome: "No observable contract.",
    nonGoals: [],
    acceptance: [],
    dependencies: [],
    baseRef: "main",
    capability: "runtime",
    risk: "high",
  }));
});
