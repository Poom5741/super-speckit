import assert from "node:assert/strict";
import test from "node:test";
import { generateFoundationCards, generateV2AlphaCardGraph } from "./index.ts";

test("a web application Foundation includes universal and browser capabilities", () => {
  const cards = generateFoundationCards({ repository: "owner/repo", baseRef: "main", domain: "web-application", decisions: [] });
  assert.deepEqual(cards.map((card) => card.capability), ["delivery-runway", "test", "delivery", "security", "operations", "frontend"]);
  assert.equal(cards.every((card) => card.kind === "foundation"), true);
});

test("the alpha graph contains all 17 Foundation and 10 Feature cards", () => {
  const graph = generateV2AlphaCardGraph("Poom5741/super-speckit", "main");
  assert.equal(graph.foundation.length, 17);
  assert.equal(graph.features.length, 10);
  assert.deepEqual(graph.features.find((card) => card.title.startsWith("P05 "))?.dependencies, ["P04", "F11", "F12"]);
  assert.match(graph.foundation[16]?.acceptance[0] ?? "", /AC-01 through AC-12/);
});
