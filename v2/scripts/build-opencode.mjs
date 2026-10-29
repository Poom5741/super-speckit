import { build } from "esbuild";
import { rm } from "node:fs/promises";

const outdir = new URL("../packages/opencode/dist/", import.meta.url).pathname;
await rm(outdir, { recursive: true, force: true });
await build({
  entryPoints: {
    index: new URL("../packages/opencode/src/index.ts", import.meta.url).pathname,
    tui: new URL("../packages/opencode/src/tui.tsx", import.meta.url).pathname,
    rpc: new URL("../packages/opencode/src/rpc.ts", import.meta.url).pathname,
  },
  outdir,
  bundle: true,
  format: "esm",
  platform: "node",
  target: "node22",
  sourcemap: false,
  jsx: "automatic",
  jsxImportSource: "@opentui/solid",
  external: ["@opencode/plugin", "@opencode/plugin/tui", "@opentui/solid", "@opentui/solid/*", "solid-js", "solid-js/*"],
});
