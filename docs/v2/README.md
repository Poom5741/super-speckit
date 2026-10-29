# Super-SpecKit V2 implementation package

Status: owner-approved implementation alpha. The local core is implemented and fixture-tested; public-alpha certification remains open.

This package turns the 2026-10-30 product grill and primary-source research into a reviewable delivery contract:

- [Product specification](../../design/features/super-speckit-v2/SPEC.draft.md)
- [System architecture](system-architecture.draft.md)
- [Architecture decision register](adrs.draft.md)
- [Implementation roadmap](implementation-roadmap.draft.md)
- [Foundation and Feature card graph](card-graph.draft.md)

Evidence sources:

- [OpenCode runtime and Portfolio research](../research/opencode-runtime-and-portfolio-layer.md)
- [Portfolio architecture-intelligence research](../research/portfolio-architecture-intelligence.md)
- [ADE, Herdr, and Cloudflare runtime research](../research/unattended-runtime-ade-herdr-cloudflare.md)
- `whitelabels-cex` Foundation evidence at `/Users/poom-work/whitelabels-cex/`

The current Super-SpecKit method remains supported. V2 is progressive enhancement: portable skills remain usable in any harness, while OpenCode receives the richer Mission Control experience.

## Implemented locally

- Node 22 TypeScript/pnpm workspace, protocol schemas, deterministic revisions, SQLite WAL coordinator, event journal, outbox, fencing, heartbeat, cancellation ambiguity, checkpoints, exact-candidate evidence, guarded completion, and approval-bound handoff.
- `ssk2` public command families, supervised local daemon boundary, GitHub managed contracts, external idempotent sync journal, ordinary branch/PR/CI import, reversible V1 adoption, AGENTS guidance, Foundation/Feature graph generation, provider SDK/conformance, native runner, persistent WSL bridge, Herdr/ADE boundaries, Cloudflare hostname guardrails, and 30-day evidence retention.
- Prebuilt OpenCode 2.2.2 server/TUI/RPC plugin with Home, Card, Agent lanes, Environment, Evidence, and Release views. Unverified versions degrade with writer controls disabled.
- Installer registration for all four portable skills and the OpenCode V2 plugin.

## Still required for public alpha

- Clean Windows 11/WSL acceptance, installed Herdr and ADE journeys, live Cloudflare Browser Run with protected preview and takeover, three real `whitelabels-cex` cards, GitHub Project field publication/re-import, a live ordinary-contributor import journey, accessibility and security review, and independent exact-candidate review.
- These are evidence gates, not TODOs that local mocks can satisfy. The runtime must continue to report them as unverified.

## Local commands

```bash
pnpm build:v2
pnpm test:v2
pnpm ssk2 doctor
pnpm ssk2 cards preview --repository owner/repo --alpha-graph
```
