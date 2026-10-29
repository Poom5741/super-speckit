# Super-SpecKit V2 runtime rationale

## Problem

V1 defines delivery behavior but does not own durable provider execution, writer fencing, cross-machine continuation, or a live OpenCode view. V2 must add those capabilities without turning OpenCode, GitHub, or a provider session into a second execution authority.

## Usage

Every client uses one coordinator API.

```ts
const card = await client.query({ kind: "card", cardId });
const receipt = await client.execute({
  requestId,
  expectedVersion: card.version,
  command: { kind: "claimCard", card: card.activeRevision, provider, runner },
});

for await (const event of client.watch({ after: receipt.cursor, cardId })) {
  render(event);
}
```

The alpha exposes the API through `ssk2`, JSON-RPC, and the OpenCode plugin. Existing Python commands keep their V1 meaning.

## Shape

One supervised coordinator opens the SQLite WAL database. It validates commands, updates current state, appends events, and records external operations in one transaction. Provider workers execute committed operations after the transaction and submit observations through the same command path. Adapters never write runtime tables.

The public client has `execute`, `query`, and `watch`. Domain states use discriminated unions. Provider and runner data enter through schema parsers. A journal supports event replay and audit, but current state remains authoritative. V2 does not require full event sourcing or snapshot upcasters.

Lease expiry blocks more writes but does not prove that a process stopped. A replacement writer requires a trusted quiescence receipt or a new isolated workspace whose old credentials cannot write. A provider that cannot establish this condition is read-only or degraded.

GitHub owns card intent. Git owns technical contracts. The coordinator owns attempts, leases, handoffs, budgets, and evidence state. V1 owns unadopted work. Digest-checked adoption gives V2 exclusive ownership of new runtime transitions while preserving V1 history.

## Synthesis decision

Candidate A is the base because its transactional current state and journal keep the call chain short. Candidate B contributed the explicit V1 authority rule, model-based transition testing, and stricter execution and handoff unions. Full event sourcing was rejected because replay migrations and upcasters add work without improving the alpha's authority guarantees.

## Tradeoffs accepted

- One elected coordinator sacrifices disconnected multi-writer availability to preserve exclusive writer authority.
- SQLite keeps deployment local but requires a drained transfer protocol before another coordinator can take ownership.
- `ssk2` adds a temporary command name in exchange for V1 compatibility during alpha.
- External adapters can report degraded capability when their native API cannot prove ownership or quiescence.

## Alternatives considered

- An OpenCode-owned ledger makes portable and external providers secondary and ties runtime durability to the plugin lifecycle.
- A coordinator per host cannot use GitHub as an atomic lease service and permits split-brain writers.
- Independent services for leases, attempts, handoffs, and evidence require distributed transactions that the local alpha does not need.

## Open risks

- Live provider certification requires installed Herdr and ADE environments, Cloudflare credentials, and a clean Windows 11 with WSL host.
- The OpenCode V2 API remains pinned to one observed commit until its compatibility fixture passes against a stable release.
- Coordinator transfer cannot proceed while any writer lacks a verified quiescence receipt.

## Next step

Implement the protocol schemas, transactional coordinator, fake provider, and fault tests before adding native provider adapters.
