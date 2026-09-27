# Brownfield Constitution and Change Comprehension Research

**Status:** research for discussion; no workflow behaviour is implemented by this document.

## The problem, clarified

For a large existing repository, an agent and a developer need two different kinds of
understanding:

1. **Governance:** which project principles, constraints, boundaries, evidence standards,
   and decision rights must every change respect?
2. **Comprehension:** what does the product do today; which user/system flow makes it
   happen; and what will a proposed change alter, depend on, and risk?

Raw code remains the executable truth, but it is a poor first interface for either question.
The proposed capability should give a person a navigable, evidence-backed explanation first,
with source links available when detail is needed. It must never turn a generated explanation
into an unsupported claim that the code or running system behaves that way.

## Research findings

### 1. Keep the Spec Kit constitution narrow and live

Spec Kit already positions the constitution as a project-level, live source of governance:
`plan`, `tasks`, and `analyze` read `.specify/memory/constitution.md` at runtime; the plan
contains a Constitution Check rather than freezing its rules in the template. Its normal flow
is Specify -> Plan -> Tasks -> Implement -> Converge, with `analyze` as a cross-artifact
consistency gate. [Spec Kit upgrade and runtime-resolution documentation](https://github.com/github/spec-kit/blob/main/docs/upgrade.md),
[Spec Kit Agentic SDD reference](https://github.github.com/spec-kit/reference/agentic-sdd.html).

That makes the constitution the right home for **normative rules**, not a large catalogue of
facts about a changing codebase. A massive brownfield description placed directly in it will
become stale, expensive to load, and ambiguous about whether a statement is a rule or merely
an observation. Spec Kit's own monorepo guidance also scopes a constitution to a project root
and does not provide built-in base/inheritance; that reinforces using a small stable core plus
separate, scoped context material. [Spec Kit monorepo guide](https://github.github.com/spec-kit/guides/monorepo.html).

### 2. Architecture communication works best at progressive levels of zoom

The C4 model gives a concise, audience-aware hierarchy: system context, containers,
components, and code, plus dynamic and deployment diagrams. It explicitly says most teams
need only context and container diagrams. [C4 diagrams](https://c4model.com/diagrams),
[C4 introduction](https://c4model.com/introduction).

arc42 complements this with a practical documentation structure: goals, constraints, context,
solution strategy, building blocks, runtime scenarios, deployment, cross-cutting concepts,
decisions, quality requirements, risks, and glossary. Its runtime view is specifically intended
to explain important scenarios to stakeholders who cannot or do not want to infer behaviour
from static structure. [arc42 overview](https://arc42.org/overview/),
[arc42 runtime view](https://docs.arc42.org/section-6/).

For a brownfield codebase, this means an atlas should start with product purpose and system
context, then permit progressive drill-down. It should not attempt a code-level diagram of the
whole repository.

### 3. Large systems need a stable vocabulary, ownership, and boundary model

Backstage's system model treats components, APIs, and runtime resources as first-class entities;
systems group those entities and domains group systems. APIs act as the principal discoverable
boundary. [Backstage system model](https://backstage.io/docs/features/software-catalog/system-model/).
Its catalog guidance is also a useful honesty rule: automation can create initial metadata, but
humans should govern it because automated classification can be wrong. [Backstage catalog graph guidance](https://backstage.io/docs/features/software-catalog/creating-the-catalog-graph/).

This supports a Super-SpecKit atlas with explicit **capability**, **system**, **component/API**,
**resource**, **owner**, and **confidence/provenance** fields—not just a directory tree.

### 4. A project map must be commit-anchored and evidence-backed

Recent codebase-atlas tools demonstrate an implementable direction, although they are not
standards. The Loom uses structural extraction for files/symbols/relationships plus optional
semantic enrichment, anchors entities to file and line, and treats the written architecture map
as a projection of a graph tied to a commit. It updates incrementally from the diff and exposes
what it did not inspect. [The Loom map-codebase example](https://github.com/jpwinans/the-loom/tree/main/examples/map-codebase).

CodeAtlas similarly emits a versioned map contract from deterministic parsing and can create a
shareable interactive map. [CodeAtlas](https://github.com/Memnoc/CodeAtlas). ClaudeMap offers
a local-first, deterministic HTML overview using imports, responsibilities, feature tags,
subsystems, and risk heuristics; its architecture inferences remain explicitly heuristic.
[ClaudeMap](https://github.com/ingridtoulotte/claudemap).

These projects support a key design rule: generated narrative and diagrams must show their
**base commit**, sources, confidence, and known blind spots. They are useful discovery aids,
not authority over runtime behaviour.

### 5. Explain the change as a scenario and impact map, not a file list

The post-spec artifact should answer in product and system terms:

| Question a developer asks | Best explanation form |
| --- | --- |
| What will users notice? | Before/after user journey and acceptance outcomes |
| What new logic exists? | Policy/rules table plus a plain-language decision flow |
| How does it happen at runtime? | Sequence diagram: actor -> entry point -> route/API -> handler/service -> data/external dependency -> observable result |
| What current parts may change or break? | Impact/blast-radius graph with direct vs inferred edges and confidence |
| Why was this approach selected? | Linked ADR or feature decision record: options, trade-offs, consequences |
| How will we prove it? | Requirement-to-verification rows and the exact scenario evidence expected |

The runtime sequence is not cosmetic. arc42 calls runtime scenarios the way to communicate
behaviour and building-block responsibility; C4's dynamic diagrams provide the complementary
notation. [arc42 runtime view](https://docs.arc42.org/section-6/),
[C4 diagrams](https://c4model.com/diagrams).

For impact discovery, a code graph can show callers, imports, references, and dependency paths;
for example, `ctx graph` indexes incrementally and offers a symbol impact query. [ctx graph documentation](https://github.com/ctxrs/ctx). This is only one input: external integrations,
runtime message flows, data contracts, and ownership must be declared or confirmed separately.

### 6. Decisions need durable, small records

ADRs are a good complement to a feature story: they record the context, decision, alternatives,
and consequences of a significant architectural choice. [ADR guidance](https://adr.github.io/),
[AWS ADR guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/architectural-decision-records.html).
They should not be required for routine implementation details. A feature can link to an existing
ADR, create a lightweight decision record, or declare that no lasting architectural decision is
being made.

## Recommended Super-SpecKit design for discussion

### A. `super-speckit.project-atlas` — the brownfield comprehension layer

Create a **separate, versioned Project Atlas** that explains the present system at a known commit.
It is descriptive, evidence-backed, and incrementally refreshed. It augments rather than replaces
the Spec Kit constitution.

Suggested minimum durable sources:

```text
project-atlas/
  README.md                    # purpose, freshness, scope, known unknowns
  manifest.yml                 # base commit, generation time, source/evidence inventory
  product-model.md             # mission, actors, capabilities, domain glossary
  system-context.md            # C4 level 1: people, external systems, boundaries
  capability-map.md            # capability -> owning system/component -> user-facing outcome
  architecture.md              # selected C4 container/building-block views
  runtime-scenarios/           # representative flows, errors, operations; sequence diagrams
  dependencies.md              # APIs, queues, databases, third parties, direction and owner
  decisions/                   # ADR index and links
  risks-and-unknowns.md        # stale areas, inferred facts, missing runtime evidence
  evidence/                    # generated structural inventory; do not store secrets
```

The rendered **Atlas HTML** is a convenience view generated from these sources. It should offer:

1. product/capability map as the entry point;
2. a click-through C4 context/container view;
3. selected runtime flows (including error paths);
4. entry point -> route/API -> handler/service -> data/external dependency paths;
5. ownership, contracts, and source/commit provenance on every claim;
6. a clear `inferred`, `verified from runtime`, or `unknown` label;
7. links to code only as optional drill-down, never as the only explanation.

**Generation and maintenance model:** create a deterministic structural inventory (repository
paths, symbols, imports, public routes/contracts, migrations, deployment configuration) at a
specific commit; enrich it with carefully attributed human/agent explanations; then have an
independent reviewer validate the high-value flows against tests, traces, API contracts, or a
running app where possible. After each merged material change, refresh only affected atlas
sections from the diff and declare any still-stale section. This follows the commit anchor and
incremental-update pattern proven by code-atlas tooling, while keeping human stewardship for
semantic claims.

### B. `super-speckit.change-story` — post-spec, pre-plan change comprehension

After `/speckit.specify` and clarification, but **before** technical planning, produce a
reviewable `specs/NNN-feature/change-story.md` plus static `change-story.html`. This is not
another specification; it is the bridge from product intent to a shared mental model of how the
existing product will be changed.

Required sections:

```text
1. One-minute change summary (who gains what and why now)
2. Before / after user journey
3. Business rules and decision table (including exceptions and non-goals)
4. Proposed runtime story
   actor -> UI/CLI/webhook -> entry point/route -> application service
   -> data read/write -> event/API/third party -> user-visible result
5. Affected capability and system map
6. Blast radius
   confirmed direct dependencies | inferred dependencies | unexamined boundaries
7. Data, contract, privacy, security, and operational implications
8. Alternatives / irreversible decisions / ADR links
9. Verification story: each outcome linked to a planned proof
10. Evidence ledger: base commit, sources, confidence, freshness, unknowns
```

The HTML version should present a **change theatre**, not a dashboard: begin with the narrative
and before/after flow, reveal the runtime sequence, then let the reader explore impacts and
evidence. The reader can understand what changes without reading source files; source links
remain available for verification. This keeps it practical for a developer, PM, or reviewer.

### C. A brownfield constitution extension, not a replacement constitution

Add a small composable policy section to the existing Spec Kit constitution, e.g.
`Brownfield Understanding and Change Safety`. Candidate principles:

1. **Evidence before inference:** claims about current behaviour require a commit/path,
   test/contract, trace, or explicit `inferred/unknown` label.
2. **Domain before directory:** organize project understanding around capabilities, users,
   systems, APIs, and ownership; folders are evidence, not the primary model.
3. **Boundary preservation:** a change story must name affected public contracts, data ownership,
   integrations, and compatibility obligations before a plan can pass its constitution check.
4. **Freshness and provenance:** Atlas and change-story artifacts carry base commit, date,
   evidence sources, and stale/unexamined boundaries.
5. **Decision lineage:** durable architecture choices link to ADRs; routine local choices do not
   create ceremony.
6. **Explained change gate:** no implementation begins for a material brownfield change until
   its change story is reviewed, its unknowns are accepted or resolved, and requirements map to
   verification.

This is stronger than merely enlarging `constitution.md`: policies remain live and enforceable;
the Atlas can grow and evolve without turning factual documentation into law.

## Relationship to the current Super-SpecKit workflow

```text
existing codebase
  -> project-atlas bootstrap / refresh (read-only, commit anchored)
  -> native Spec Kit: constitution -> specify -> clarify
  -> change-story (explain intended behaviour and impact)
  -> review/accept unknowns
  -> native Spec Kit: plan -> tasks -> analyze -> implement
  -> independent Super-SpecKit QA and convergence
  -> atlas refresh when the change materially alters the model
```

The existing requirements-to-verification matrix remains the proof mechanism. The change story
cannot call a requirement verified; it only says what proof will be needed. The existing
maker/checker separation also applies: the author of a story may build the feature, but an
independent reviewer validates sources, impact boundaries, and claimed runtime behaviour.

## Important limitations and safeguards

- No generated map can fully infer dynamic configuration, reflection, feature flags, production
  traffic, third-party behaviour, or undocumented business rules. Show these as unknowns.
- Static dependency edges are not runtime proof. Confirm high-risk flows with API contracts,
  traces/logs, integration tests, or Playwright + API/DB evidence as appropriate.
- A repository can have more than one product/domain. Bootstrap at a bounded subsystem first;
  do not attempt a total map before useful work begins.
- Avoid diagram volume. C4 recommends only the levels that add value, and arc42 recommends a
  representative selection of runtime scenarios rather than many diagrams.
- Never put credentials, production identifiers, customer data, or raw sensitive traces into
  the atlas or generated HTML.

## Open design decisions for the user

1. **Primary audience:** should the first Atlas experience optimise for a founder/product owner,
   a new developer, or an AI coding agent? One artifact can serve all three, but the default
   reading depth and language differ.
2. **Initial scope:** begin at a whole-repository product map, or choose one business domain
   / bounded context first? For a massive repository, the latter is safer and more useful.
3. **Truth sources:** may the system read deployed runtime telemetry and production-like data,
   or must it use only local code, tests, fixtures, and staging? This changes evidence quality
   and privacy design.
4. **Review authority:** who accepts an Atlas fact or a change-story unknown before planning:
   human owner only, or an independent checker with human escalation for high-risk claims?
5. **Freshness policy:** refresh automatically after every merged change, only after features
   marked architecturally material, or on demand? Automatic full regeneration can be expensive;
   commit-anchored incremental refresh is the recommended default.
6. **Artifact experience:** should the first version be Markdown-first with a generated static
   HTML explanation (recommended), or should it invest immediately in an interactive graph
   application? The former preserves reviewability and works in normal Git workflows.

## Recommendation

Build this as two linked additions, in this order:

1. **Project Atlas bootstrap + HTML reader** for an existing bounded domain. Make it an honest,
   commit-anchored explanation of the product, architecture, representative runtime paths,
   ownership, and unknowns.
2. **Change Story gate** after Spec Kit specification/clarification and before planning. Make it
   explain before/after behaviour, rules, runtime path, impact, trade-offs, and intended proof.
3. Add the compact **Brownfield Understanding and Change Safety** constitution extension and
   require independent review for material changes.

This fulfils the intended new way to understand code: people start with what the product does,
how a scenario flows through the system, and what a change will alter. They only open raw code
when they need to validate a claim or implement it.
