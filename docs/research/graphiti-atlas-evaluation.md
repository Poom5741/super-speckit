# Graphiti evaluation: temporal graph retrieval for the Project Atlas

Researched 2026-09-28 from Graphiti/Zep-owned repository and documentation only. This is an architecture decision input, **not** an instruction to add a database or send project material to a third party.

## Decision

**Recommendation: optional, read-only adapter — not a Super-SpecKit dependency and not an authority.**

Graphiti has ideas that fit the future knowledge-as-nodes direction very well: typed entities, relationship traversal, provenance, and explicit time. But it is a runtime graph-building framework with an LLM/embedding ingestion path and a graph-database dependency. That is the wrong default foundation for a portable skill set whose current trust model is committed files, native repository artifacts, and command-checked YAML.

Use its model as a design reference now. Offer an opt-in adapter later only for large, frequently changing codebases where measured retrieval failures justify operating a graph service.

## What Graphiti actually provides

Graphiti is an Apache-2.0 open-source framework for temporal context graphs. Its own definition is a graph of entities, relationships/facts, and source episodes: each derived fact has a validity window and links back to raw ingested data. It supports both developer-prescribed entity/edge types through Pydantic models and learned structure. [Repository overview](https://github.com/getzep/graphiti#what-is-a-context-graph), [license](https://github.com/getzep/graphiti/blob/main/LICENSE), [package metadata](https://github.com/getzep/graphiti/blob/main/pyproject.toml).

Its retrieval is not merely graph traversal. The project documents hybrid semantic, keyword/BM25, and graph retrieval, with edge search, node search, and graph-distance reranking in the quickstart. New episodes are intended to be ingested incrementally rather than rebuilding the graph in a batch. [Retrieval and incremental construction](https://github.com/getzep/graphiti#why-graphiti), [quickstart capabilities](https://github.com/getzep/graphiti#quick-start).

The temporal part matters: a relationship is not simply deleted when superseded; Graphiti records when it was valid and can query the current or historical view. This is useful for questions such as “which service owned this behavior at the candidate SHA?” or “which decision was superseded by the migration?”—provided the source version is attached accurately. [Temporal fact management](https://github.com/getzep/graphiti#why-graphiti).

Graphiti also includes an MCP server and a FastAPI service, so an agent can add/retrieve episodes, search entities/relationships, use groups, and maintain the graph through a separate service. The MCP server is explicitly described as experimental. [MCP server README](https://github.com/getzep/graphiti/blob/main/mcp_server/README.md), [REST service README](https://github.com/getzep/graphiti/blob/main/server/README.md).

## Where it could improve the Atlas

| Atlas need | Graphiti-compatible contribution | Guardrail |
| --- | --- | --- |
| “What changes if I touch this component?” | Traverse `component → owns → contract → consumed_by → component`, then surface linked test/evidence/decision nodes. | Return source paths, commit SHA, and evidence IDs; never return an ungrounded summary alone. |
| “What was true when this bug was introduced?” | Temporal edges can model a validity interval for ownership, API contracts, and decisions. | Git commits remain the time authority. A graph timestamp cannot substitute for `git show` or a candidate SHA. |
| Large brownfield discovery | Hybrid retrieval can locate related entities even when names differ, then expand concrete dependency edges. | Search is a lead, not proof; the agent must reopen exact files and run repository checks. |
| Cross-session continuity | Episodes can retain rationale and source linkage across sessions. | Store the canonical rationale in committed files first; ingest a derived projection only. |
| Visual maps | A selected subgraph can render to the existing Mermaid/HTML Change Story. | Render from a deterministic exported subgraph, not from an agent's prose. |

These benefits are plausible architecture benefits, not yet proven Super-SpecKit benefits. We should not claim that Graphiti reduces token cost, exploration time, or defects until an adapter is evaluated against a representative brownfield repository with a measured baseline.

## Why it must not replace file-backed evidence

Super-SpecKit currently makes native artifacts and commands authoritative: Git SHA and worktree state, Spec Kit documents, tests, QA evidence, and validated YAML projections. A Graphiti graph is a **derived retrieval index** and can be stale, partially ingested, or incorrectly extracted by an LLM. Its own documentation says that facts are autonomously built from structured and unstructured source episodes; that is useful discovery machinery, but it is not the same as a deterministic fact store. [Context graph construction](https://github.com/getzep/graphiti#what-is-a-context-graph).

Therefore the adapter contract must be:

```text
Committed source / command output (authority)
        │ deterministic extractor + source SHA + content hash
        ▼
Graphiti graph (optional retrieval projection)
        │ ranked candidates with provenance
        ▼
Agent reopens source and runs required checks (verification)
```

If Graphiti is unavailable, stale, lacks credentials, or finds nothing, the Atlas still works from files. Such a result is `inconclusive`, not a pass and not a reason to block a normal project.

## Operating, cost, and privacy implications

Graphiti is not a lightweight local JSON index by default. The documented core requires Python 3.10+, a supported graph database (Neo4j, FalkorDB, or Amazon Neptune plus OpenSearch in the relevant configuration), and defaults to OpenAI for LLM inference and embeddings. It can use other hosted or OpenAI-compatible/local providers, but Graphiti warns that structured-output-capable models work best for its extraction pipeline. [Installation and requirements](https://github.com/getzep/graphiti#installation), [provider options](https://github.com/getzep/graphiti#using-graphiti-with-openai-compatible-providers-and-local-llms).

That creates several costs absent from the file-first Atlas:

- database deployment, backup, upgrades, access control, and index maintenance;
- LLM and embedding requests at ingestion time, rate-limit handling, and possible re-ingestion after repository changes; Graphiti documents a configurable concurrency limit specifically to manage provider `429` errors; [concurrency guidance](https://github.com/getzep/graphiti#default-to-low-concurrency-llm-provider-429-rate-limit-errors)
- a service trust boundary when using its MCP/REST layers; and
- potential sensitive-code exposure if source files, incident logs, customer data, or architecture documents are sent to hosted model/embedding endpoints.

Graphiti supports local OpenAI-compatible endpoints, which can mitigate external transmission, but local processing still requires an explicit security and retention review. The core package also declares a `posthog` dependency; this alone does **not** prove telemetry is sent, but it is enough to require a project-specific runtime/configuration audit before allowing confidential material. [Core dependency list](https://github.com/getzep/graphiti/blob/main/pyproject.toml).

For maturity, the project has a versioned Python package and published container release process, multiple database/provider paths, and a public MCP server; that makes it a credible optional integration candidate. However, its MCP implementation calls itself experimental, Kuzu support is deprecated, and the project expects the adopter to build surrounding tools and operate the selected database. This is mature enough for a bounded pilot, not mature enough to become a mandatory foundation for every project. [MCP status](https://github.com/getzep/graphiti/blob/main/mcp_server/README.md), [Kuzu deprecation and backend guidance](https://github.com/getzep/graphiti#installing-with-kuzu-support), [Graphiti vs. managed Zep](https://github.com/getzep/graphiti#zep-vs-graphiti).

## Proposed typed projection (compatible with both file-only and Graphiti modes)

Start with a repository-owned schema that Graphiti can consume later:

```yaml
id: component:billing:invoice-service
kind: component # project | feature | component | entry_point | contract | decision | test | evidence | risk
title: Invoice service
source:
  path: services/billing/invoice.py
  git_sha: <immutable-sha>
  content_sha256: <hash>
claims:
  - relation: implements
    target: contract:invoice:create-v2
    confidence: proven
    evidence_ids: [evidence:unit:invoice-create-123]
temporal:
  observed_at_sha: <immutable-sha>
  valid_from: <commit-or-release>
  valid_to: null
```

This preserves the distinctions Super-SpecKit needs:

- `depends_on` (execution/deployment dependency) is separate from `consumes` (data/context dependency);
- every relationship has source evidence, a confidence label, and an immutable Git/content reference;
- `unknown` is a first-class state rather than an invented edge; and
- a deterministic exporter can create Mermaid/HTML with no database installed.

Graphiti mapping, if enabled: node `id` becomes an entity identifier; `kind` becomes a prescribed entity type; claims become typed edges; the canonical artifact or captured command output becomes an episode; Git version timestamps are stored as graph temporal metadata. The adapter must not let learned ontology create authoritative relationships without exporting them first as `inferred` candidates for review and source verification.

## Safe staged integration

1. **Stage 0 — file-first Atlas (adopt now).** Build the typed node/edge YAML or JSON schema, deterministic integrity checker, and Mermaid/HTML renderer. No database, model API, or Graphiti dependency.
2. **Stage 1 — retrieval measurement.** On one large consenting repository, record a representative set of Atlas questions. Measure source-opening steps, time/tokens, precision of retrieved candidates, and missed relevant constraints using the file-only resolver. Define a threshold before adding infrastructure.
3. **Stage 2 — local/isolated pilot.** Add a disabled-by-default `knowledge_graph.provider: graphiti` adapter that ingests only allowlisted, hash-versioned derived packets. Prefer a local provider and local graph database for confidential repositories. Keep the full file-only fallback and perform a source verification after every result.
4. **Stage 3 — operational gate.** Enable only when the project explicitly supplies retention, access-control, backup/delete, secret handling, cost budget, provider/data-residency, re-index schedule, health checks, and stale-index behavior. Emit an evidence receipt containing index version, source SHAs, ingestion outcome, and query provenance.
5. **Stage 4 — reassess.** Retain the adapter only if the metrics show better retrieval without increased false confidence, privacy risk, or operational burden. Never require it for normal Super-SpecKit installation.

## Bottom line

Graphiti validates the direction of knowledge as typed, temporal, provenance-linked nodes rather than giant documentation blobs. Its strongest contribution to Super-SpecKit is an **optional retrieval engine** for a schema we own—not a replacement for project files, Git truth, purpose confirmation, or independent QA. The right next implementation is the file-backed node schema and deterministic Atlas renderer; Graphiti should enter only after that foundation has a measured retrieval problem worth solving.
