---
description: Deep multi agent review of a backend API or service for contract, schema, idempotency, auth, observability, perf, and OSS readiness.
argument-hint: "[optional: path to repo, defaults to current directory]"
---

# Backend API / service deep review

Target: $ARGUMENTS (defaults to the current directory if blank).

Run a parallel multi agent review of the backend service at the target path. Detect the stack (language, framework, datastore) first. Dispatch the matching stack expert plus the generalists below.

## Detect first

1. Language and framework from manifests (`package.json`, `Cargo.toml`, `go.mod`, `Gemfile`, `requirements.txt`, `pom.xml`, etc.).
2. Datastore from connection strings, ORM config, migration directories.
3. Deployment target (k8s, ECS, Cloud Run, Vercel, bare metal).

## Agents to dispatch in parallel

1. `code-reviewer` plus the matched stack expert (`rails-expert`, `django-expert`, `golang-expert`, `rust-expert`, `python-expert`, `java-expert`, `csharp-dotnet-expert`, `nextjs-expert` for API routes, etc.), code quality with severity labels.

2. `security-reviewer`, auth boundary, authz per object (IDOR), input validation, secrets handling, SSRF, deserialization, SQL injection, rate limiting, audit logging, raw query exposure.

3. `api-contract-designer`, review the API contract: idempotency keys on mutating endpoints, pagination strategy (cursor vs offset), error code stability, versioning policy, OpenAPI / GraphQL schema quality, request/response shape, status code correctness.

4. `data-modeler` plus the matched datastore expert (`postgres-expert`, `redis-expert`), schema review: types, FKs, indexes, partitioning, soft delete policy, N+1 risk, missing constraints.

5. `perf-investigator`, hot paths, N+1 queries, missing indexes, network round trips, lock contention, queue saturation, cache strategy.

6. `senior-devops-sre` skill, observability (structured logs, metrics, traces), SLO definitions, runbook readiness, deploy strategy, env var hygiene, secrets rotation.

7. `test-engineer`, unit / integration / contract / e2e mix, test data hygiene, flake risk, CI gates.

8. `dependency-auditor`, lockfile review, CVE alerts, postinstall hooks, license obligations.

9. `tech-writer`, README, API reference quality, runbook, changelog.

10. `architect`, overall topology: service boundary, dependency graph, async vs sync, eventual consistency boundaries, idempotency from end to end.

## Output format

### Verdict
**Ship / Hold / Block** in one sentence.

### Top 5 blockers
Ranked, with severity, file:line or endpoint, owning subagent, recommended action.

### Strong suggestions
Grouped by area: contract, schema, security, perf, observability, code quality, docs.

### Contract score
Quick rating on each: idempotency, pagination, error codes, versioning, auth declaration, OpenAPI quality.

### Open source readiness
LICENSE, README, SECURITY, secrets check, contribution path, example env file, local dev quickstart.

### Next 5 commits
Ranked by impact.

Cite the subagent that produced each finding. Keep it terse.
