import assert from "node:assert/strict";
import test from "node:test";
import { FakeProvider } from "@super-speckit/provider-sdk";
import { assertProviderConformance, runProviderConformance } from "./index.ts";

test("the fake provider establishes the provider conformance contract", async () => {
  const report = await runProviderConformance(new FakeProvider());
  assert.doesNotThrow(() => assertProviderConformance(report));
  assert.equal(report.checks.length, 8);
  assert.equal(report.checks.every((check) => check.status === "passed"), true);
});
