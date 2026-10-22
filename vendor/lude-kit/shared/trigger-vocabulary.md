# Trigger vocabulary

When writing a skill's `description`, pull from these word lists so triggers stay consistent across the library and overlap is conscious. Front load the verb, then add the artifact noun, then add synonyms.

## Universal action verbs

`design` · `plan` · `review` · `write` · `draft` · `audit` · `refactor` · `implement` · `ship` · `debug` · `triage` · `investigate` · `estimate` · `prioritize` · `break down` · `delegate` · `unblock` · `migrate` · `harden` · `optimize` · `validate` · `verify`

## Role / persona triggers

| Role | Triggers |
|---|---|
| Architect | architect, system design, high level design, HLD, topology, ADR, RFC, build vs buy, capacity, scaling plan |
| Tech lead | tech lead, team lead, eng lead, sprint, standup, ticket, breakdown, delegate, 1:1, retro |
| Frontend | frontend, front end, UI, React, Next.js, Vue, Svelte, component, accessibility, a11y, Lighthouse, Core Web Vitals |
| Backend | backend, back end, API, REST, GraphQL, endpoint, schema, migration, queue, worker, idempotency |
| Security | security, threat model, STRIDE, OWASP, secret, vulnerability, CVE, AppSec, secure code review |
| DevOps / SRE | DevOps, SRE, CI, CD, pipeline, Terraform, Kubernetes, deploy, rollback, on call, SLO, incident, postmortem |
| QA / Test | QA, test, testing, e2e, unit, integration, regression, flake, coverage, pyramid |
| PM | product, PM, PRD, spec, roadmap, prioritization, RICE, user story, acceptance criteria |
| UX | UX, UI design, wireframe, flow, IA, information architecture, usability, heuristic, persona |
| Tech writer | docs, documentation, README, changelog, API reference, onboarding, tutorial, runbook |

## Capability triggers (for batch 2+)

| Capability | Triggers |
|---|---|
| Code review | review, PR, pull request, diff, lgtm, nit, blocking comment |
| Debugging | bug, broken, error, stack trace, repro, reproduce, isolate |
| Refactoring | refactor, clean up, extract, rename, dedupe, simplify |
| Perf tuning | slow, latency, p95, hot path, profile, flamegraph, memory leak |
| Postmortem | postmortem, RCA, root cause, incident writeup, blameless |
| API design | endpoint, contract, OpenAPI, GraphQL schema, idempotent, pagination, versioning |
| Data modeling | schema, ERD, normalize, denormalize, index, foreign key, cardinality |

## Antitriggers

Common false positive overlaps to call out explicitly in a skill's description when relevant:

- "Not for X" disclaimers, short, name the right skill.
- Example: `senior-frontend-engineer` description should include "Not for visual / interaction design, see `senior-ux-designer`."
- Example: `principal-security-engineer` description should include "Not for general code review, see `senior-code-reviewer`."

## House style for descriptions

Template:

> Use when {action verbs}, {artifact nouns}, or {situations}. Produces {outputs}. {Antitrigger if needed}.

Examples, good and bad:

**Good** (`staff-software-architect`):
> Use when designing a system, choosing a database or framework, writing an ADR or RFC, deciding build vs buy, planning capacity, or reviewing an architecture diagram. Produces ADRs, RFCs, system diagrams, and capacity plans. Not for implementation work, hands off to senior-backend-engineer / senior-frontend-engineer.

**Bad**:
> Expert software architect with decades of experience leveraging cutting edge patterns to deliver world class systems.

The good one matches the words a user actually types. The bad one matches nothing.
