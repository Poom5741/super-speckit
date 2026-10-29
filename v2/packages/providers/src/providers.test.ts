import assert from "node:assert/strict";
import test from "node:test";
import { CloudflareBrowserProvider, createAdeProvider, createHerdrProvider } from "./index.ts";

test("external providers report unavailable instead of claiming unconfigured support", async () => {
  const herdr = await createHerdrProvider(null).probeCapabilities();
  const ade = await createAdeProvider(null).probeCapabilities();
  assert.equal(herdr.capabilities["writer"]?.kind, "unavailable");
  assert.equal(ade.capabilities["writer"]?.kind, "unavailable");
});

test("the cloud browser rejects non-HTTPS and non-allowlisted targets", () => {
  const provider = new CloudflareBrowserProvider({ endpoint: "https://api.example.test/", token: "secret", allowedHosts: ["preview.example.test"] });
  assert.equal(provider.assertAllowedTarget("https://preview.example.test/card/1").hostname, "preview.example.test");
  assert.throws(() => provider.assertAllowedTarget("http://preview.example.test/card/1"));
  assert.throws(() => provider.assertAllowedTarget("https://attacker.example/card/1"));
});
