# Capabilities

Cross role capabilities focused on a single job. Personas reach for these the way a person reaches for a power tool.

A capability skill is narrower than a persona and broader than a vendor wrapper. It encodes one job, review this PR, debug this stack trace, write this postmortem, and does it excellently regardless of the surrounding role.

## Shipped (batch 2)

- [`senior-code-reviewer`](senior-code-reviewer/SKILL.md), PR review with severity labeled feedback (blocking, strong suggestion, nit).
- [`senior-debugger`](senior-debugger/SKILL.md), root cause diagnosis from logs, repros, and stack traces; no guessing.
- [`senior-refactorer`](senior-refactorer/SKILL.md), behavior preserving structural change in small commits with green tests between.
- [`senior-performance-engineer`](senior-performance-engineer/SKILL.md), latency, throughput, memory; measure first, optimize the dominant cost, validate.
- [`incident-commander`](incident-commander/SKILL.md), realtime IC for live incidents; roles, comms, mitigation, all clear.
- [`api-contract-designer`](api-contract-designer/SKILL.md), contract first REST / GraphQL / gRPC; idempotency, pagination, versioning.
- [`data-modeler`](data-modeler/SKILL.md), schema, types, indexes, identifiers, lifecycle; access patterns first.
- [`migration-planner`](migration-planner/SKILL.md), expand / dual write / shadow read / cutover / contract phasing.
- [`dependency-auditor`](dependency-auditor/SKILL.md), supply chain and CVE review; SBOM, lockfile diff, postinstall audit.
- [`postmortem-author`](postmortem-author/SKILL.md), blameless postmortems with contributing factors and tracked action items.

See the [open roadmap issues](https://github.com/dimitris-di/lude-kit/issues?q=is%3Aissue+label%3Anew-skill) for proposals beyond batch 2.

## Authoring a capability

1. Open a "new skill" issue first.
2. Copy [`shared/skill-template/SKILL.md`](../../shared/skill-template/SKILL.md) into a new folder here.
3. Capabilities lean harder on **Workflow** and **Deliverables** than personas do, the job is narrow, so the steps and outputs should be sharp.
4. Name the personas that typically reach for this capability under **Handoffs**.
