# Architecture intelligence for the portfolio layer

Research snapshot: 2026-10-30. This note uses first-party repositories, official documentation, and original framework sources. Repository links use inspected commits where possible so later changes do not silently rewrite the evidence.

## Recommendation

The portfolio layer needs two separate intelligence stages:

1. **Decision research** finds current facts about candidate technologies and records what each source can prove. It answers questions such as whether Go, Java, Rust, or TypeScript fits the team's workload, deployment target, latency target, security obligations, and operating budget.
2. **Architecture reasoning** turns product goals, constraints, and research into system options. It tests boundaries, data ownership, failure behavior, security, operability, evolution, and team independence before proposing a decision.

No inspected skill provides both stages at the required depth. The strongest design is to extend Matt Pocock's small primary-source `research` skill into a decision-grade evidence worker, then combine the installed domain-modeling and pinned PStack reasoning skills with selected architecture review methods. GitHub Spec Kit and Superpowers can supply workflow structure, but neither is a knowledge authority.

Do not create a permanent catalogue that says "use Go for backends" or assigns fixed scores to fashionable stacks. For each project, derive candidates from the project's constraints, retrieve current evidence, and compare only viable options. If published evidence cannot resolve a consequential claim, run a bounded spike or benchmark against the intended workload.

## Part 1: decision research

### What the stage must do

The research stage is a fact-finding service, not the architect. It should:

- split the interview into factual unknowns and human decisions;
- search official documentation, specifications, source repositories, release notes, security advisories, support policies, and first-party operational guidance;
- state the workload and constraints before comparing technologies;
- distinguish a documented fact, an inference, and a local measurement;
- record version, retrieval date, applicability conditions, contradictions, and a recheck date;
- return evidence for every option, including evidence that weakens the likely recommendation;
- stop short of choosing an architecture.

Matt Pocock's [`research` skill](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/research/SKILL.md) is the best small base. It requires primary sources, a separate research agent, citations, and a repository artifact. It does not define comparison criteria, provenance fields, freshness, contradiction handling, or measurement rules. Super-SpecKit's pinned copy is from commit [`74ca5fe`](https://github.com/mattpocock/skills/tree/74ca5fe077456a0b3b2f5310cf9430999fd0b5fd/skills/engineering), while the inspected upstream head is `a496f55`. The current repository is MIT-licensed, but an upgrade still needs a source diff and a fresh skill evaluation ([upstream package metadata](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/package.json)).

Context7 can help retrieve version-specific library and framework documentation and documents an OpenCode installation path. Its own README warns that community-contributed projects are not guaranteed accurate or secure, and its crawler and backend are not part of the open client. Use it as a retrieval adapter, then retain and evaluate the owning project's source. Do not treat a Context7 answer as the authority for a stack choice ([Context7 MCP README](https://github.com/upstash/context7/blob/%40upstash/context7-mcp%404.4.4/README.md)).

Two first-party vendor skills are useful specialists:

- AWS Agent Toolkit's `aws-well-architected-review` discovers architecture from code and infrastructure definitions, retrieves the live AWS Well-Architected corpus, checks practices with canonical IDs and file evidence, and audits review coverage. Use it when AWS is a target or candidate. Its own scope excludes general ADR and migration-readiness work, so it cannot be the project architect ([pinned AWS skill](https://github.com/aws/agent-toolkit-for-aws/blob/96a27f273291299666bcc004c7b19f27e7d9986a/skills/core-skills/aws-well-architected-review/SKILL.md)).
- Microsoft's `cloud-solution-architect` packages design principles, architecture styles, patterns, technology-choice guidance, mission-critical guidance, Well-Architected review, and ADR workflow. It is a broad ready-made reference, but it is Azure and PaaS biased. Use it when Azure is in scope or as counterevidence, not as a universal default ([pinned Microsoft skill](https://github.com/microsoft/skills/blob/41138f3cb4825d1ba9812d35358d5513be08c20e/.github/skills/cloud-solution-architect/SKILL.md)).

GitHub Spec Kit has a useful place for research, but its core planning template asks agents to resolve unknowns and write only a decision, rationale, and alternatives. It does not require source authority, version, freshness, or counterevidence ([Spec Kit `plan` workflow](https://github.com/github/spec-kit/blob/03bba71b025ded8507c5e1451bdceab988bdebef/templates/commands/plan.md)). Treat that phase as an integration point, not the research method. Spec Kit is MIT-licensed ([license](https://github.com/github/spec-kit/blob/03bba71b025ded8507c5e1451bdceab988bdebef/LICENSE)).

PStack contributes two useful controls. Its pinned `benchmark-checklist` rejects untuned, non-reproducible comparisons and requires evidence that the measured work happened. Its `blast-radius` skill ranks claims by how directly they were proven. Neither skill performs broad external research. PStack is already pinned at `e5a8186d7b43be8d6ac4452440fbead5f1a51c70`, version `0.15.13`, under MIT, so the portfolio layer can call these controls without importing another copy ([local source manifest](../../sources.lock.json), [upstream pinned tree](https://github.com/cursor/plugins/tree/e5a8186d7b43be8d6ac4452440fbead5f1a51c70/pstack)).

### Source policy for technology selection

Use a source ladder for each claim:

1. A standard or protocol specification for compatibility and semantics.
2. Official project documentation and release or support policy for current capability.
3. The exact source repository, changelog, issue, or security advisory for implementation status and known limitations.
4. First-party operator guidance for deployment and failure behavior.
5. A reproducible project-specific measurement when the decision depends on performance, cost, developer workflow, or an undocumented edge case.

Vendor frameworks are evidence about their platforms, not universal truth. For example, AWS Well-Architected supplies current review questions across operational excellence, security, reliability, performance efficiency, cost, and sustainability ([AWS question index](https://docs.aws.amazon.com/wellarchitected/latest/framework/appendix.html)). Azure Architecture Center supplies technology decision guides and reference architectures for Azure workloads ([Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/)). Use either source when its platform is in scope. Do not let a cloud provider introduce its own services as unstated requirements.

For security, use current OWASP materials as requirement and review inputs. OWASP says threat modeling should be continuous and tied to recognizable representations of the system, while ASVS supplies testable web application security requirements ([OWASP Threat Modeling Project](https://owasp.org/projects/threat-modeling-project), [OWASP ASVS](https://asvs.owasp.org/)). For production readiness, Google's SRE launch checklist covers capacity, failure modes, monitoring, rollout, growth, and external dependencies ([Google SRE launch checklist](https://sre.google/sre-book/launch-checklist/)). These are review sources, not installable skills.

### Evidence and provenance schema

Store one record per claim. Keep excerpts short and link to the source instead of copying whole documents.

```yaml
evidence_id: ev-0042
question_id: arch-backend-runtime
claim: "Candidate A supports the required deployment target through 2029."
claim_type: documented_fact # documented_fact | inference | measurement
source:
  publisher: "project or standards owner"
  title: "support policy"
  url: "https://..."
  kind: official_docs # specification | source | release | advisory | official_docs | measurement
  version_or_revision: "v1.8 or commit SHA"
  published_at: "2026-08-12"
  retrieved_at: "2026-10-30T10:30:00+07:00"
  license_or_terms: "link or SPDX id when known"
  content_digest: "sha256 of the retrieved artifact when retained"
scope:
  applies_when:
    - "Linux amd64 deployment"
  does_not_establish:
    - "application-level latency"
support:
  status: direct # direct | inferred | measured | disputed
  confidence: high # high | medium | low
  rationale: "The publisher owns the support policy."
counterevidence:
  - evidence_id: ev-0045
freshness:
  class: volatile # stable | release_bound | volatile
  recheck_after: "2027-01-30"
  stale_if:
    - "candidate major version changes"
used_by:
  decisions:
    - adr-0003
  cards:
    - foundation-runtime
```

The record must say what a source does not prove. A framework's throughput benchmark does not prove the application's end-to-end latency. A vendor reference architecture does not prove that the team can operate it. A repository star count does not prove maintainability.

## Part 2: architecture reasoning

### What the stage must do

The reasoning stage consumes the approved product intent, the domain model, project constraints, and evidence records. It should produce:

- concrete quality scenarios with a stimulus, operating condition, expected response, and measurable limit;
- domain concepts, ownership, invariants, and context boundaries;
- at least two materially different viable designs when the constraints allow them;
- data consistency and failure semantics, including retries, idempotency, recovery, and degraded operation;
- trust boundaries, sensitive data paths, threats, and required controls;
- capacity assumptions, observability, deployment, rollback, incident response, and operator workload;
- an evolution path for schema, API, dependency, and deployment changes;
- explicit risks, tradeoffs, and rejected options;
- proposed ADRs and card boundaries that several developers can implement independently.

The installed Matt Pocock skills cover the interview and domain record well. `grill-with-docs` combines grilling with domain modeling, while `domain-modeling` challenges overloaded terms, tests edge cases, checks code against claims, updates the glossary, and limits ADRs to hard-to-reverse, surprising, real tradeoffs ([pinned `domain-modeling`](https://github.com/mattpocock/skills/blob/74ca5fe077456a0b3b2f5310cf9430999fd0b5fd/skills/engineering/domain-modeling/SKILL.md)). Current upstream also has `codebase-design` and `improve-codebase-architecture`, but those focus on deep modules and existing-code refactoring rather than greenfield distributed-system design ([current `codebase-design`](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/codebase-design/SKILL.md), [current architecture review skill](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/improve-codebase-architecture/SKILL.md)). They are useful additions after an upgrade audit, not a complete portfolio architect.

The pinned PStack bundle supplies the strongest existing reasoning vocabulary: foundational sequencing, domain-shaped data, system-boundary validation, type discipline, alternative design sketches, interface depth, multi-model challenge, and implementation feedback. Its `architect` workflow grounds an existing system, generates structurally different sketches, screens them, and redesigns when repeated implementation friction disproves the sketch ([pinned `architect`](https://github.com/cursor/plugins/blob/e5a8186d7b43be8d6ac4452440fbead5f1a51c70/pstack/skills/architect/SKILL.md)). This is strong code architecture. It lacks a complete greenfield review of reliability, security, data consistency, migration, and operations, so the portfolio layer must add those concerns before it creates cards.

Obra's Superpowers `brainstorming` skill is a strong conversation shell. It reads existing context first, asks one consequential question at a time, compares real approaches, records the design, uses a fresh builder review, and requires human approval before planning ([Superpowers `brainstorming`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/brainstorming/SKILL.md)). It does not retrieve technical evidence or supply a system architecture rubric. Importing its full method would also overlap with Super-SpecKit. If reused, adapt only its interview and builder-check patterns. Superpowers is MIT-licensed ([license](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/LICENSE)).

Vercel's ADR skill is the best inspected first-party packaging for durable decisions. It treats ADRs as human-approved, agent-readable implementation contracts, supports proposed, accepted, rejected, deprecated, and superseded states, and includes scripts and review checklists ([Vercel ADR skill](https://github.com/vercel/ai/blob/f8507823abe78471d6b3cfa2da91a63118edbff4/skills/adr-skill/SKILL.md), [ADR lifecycle](https://github.com/vercel/ai/blob/f8507823abe78471d6b3cfa2da91a63118edbff4/skills/adr-skill/assets/templates/adr-readme.md)). The Vercel repository is Apache-2.0-licensed ([license](https://github.com/vercel/ai/blob/f8507823abe78471d6b3cfa2da91a63118edbff4/LICENSE)). Its skill is marked internal and assumes its repository conventions, so use its lifecycle and agent-readiness checks as design input. Do not copy it without an integration and license review.

For whole-system work, use a proportional sequence drawn from CMU SEI methods:

1. A Quality Attribute Workshop elicits and prioritizes architecture-driving scenarios before the architecture exists ([SEI QAW collection](https://www.sei.cmu.edu/library/quality-attribute-workshop-collection/)).
2. Attribute-Driven Design selects the next element to decompose, applies the driving qualities and constraints, chooses design concepts, assigns responsibilities, defines interfaces, and verifies the result ([SEI ADD collection](https://www.sei.cmu.edu/library/attribute-driven-design-method-collection/)).
3. The Architecture Tradeoff Analysis Method evaluates candidate architecture against competing quality attributes and exposes risks, sensitivity points, and tradeoffs before implementation ([SEI ATAM overview](https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/), [ATAM collection](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/)).

Adapt these methods to the project's risk. Do not pretend every project needs a formal workshop or copy the SEI publications into a skill.

Use the C4 model only to communicate the chosen structure. The official guidance says context and container diagrams are sufficient for most teams, and the container view shows responsibility distribution and major technology choices ([C4 diagrams](https://c4model.com/diagrams), [C4 container diagram](https://c4model.com/diagrams/container)). A diagram is not an architecture review and cannot replace the tradeoff, threat, or operational analysis.

## Minimal integration architecture

Keep the implementation small. Add two workers and one thin coordinator above the existing method:

```text
portfolio interview
  -> question ledger
       -> fact questions -> evidence researcher -> evidence records
       -> choice questions -----------------------------+
                                                         |
  approved drivers + domain model + evidence ------------+
  -> architecture reasoner
  -> independent architecture review
  -> one-question-at-a-time owner grill
  -> accepted ADRs and architecture snapshot
  -> foundation and feature cards
  -> GitHub Project projection + .super-speckit records
```

The coordinator owns states and handoffs. It does not contain architecture doctrine. Each worker can run in any capable harness because its inputs and outputs are files with stable schemas.

### Proposed decision flow

1. **Frame the product.** Record users, outcomes, non-goals, constraints, risks, team shape, and success measures. Build the domain glossary as terms settle.
2. **Write measurable drivers.** Convert "fast," "reliable," and "secure" into project-specific scenarios and limits. Record workload, data sensitivity, availability, recovery, growth, cost, compliance, and operator constraints.
3. **Split facts from choices.** Send factual unknowns to the research stage. Keep value judgments and hard-to-reverse choices for the owner grill.
4. **Discover candidates.** Generate options from the constraints and existing ecosystem. Do not start with a preferred language, framework, database, or cloud.
5. **Research each viable candidate.** Produce claim-level evidence, counterevidence, and freshness metadata. Use a spike or benchmark when official sources cannot answer a decision-driving question.
6. **Design several system shapes.** Compare boundaries, data ownership, consistency, failure handling, deployment, operations, security, cost, and evolution. Drop an option only with a recorded reason.
7. **Run focused reviews.** Apply proportional QAW, ADD, and ATAM checks, OWASP threat modeling, production-readiness checks, and migration analysis. An independent reviewer challenges unsupported claims and missing failure cases.
8. **Grill the owner.** Ask one consequential question at a time. Present the recommendation, evidence, consequences, and reversibility. The owner chooses hard-to-reverse directions.
9. **Ratify decisions.** Write accepted ADRs with evidence IDs, assumptions, consequences, review triggers, and supersession links. Create C4 context and container views only when they improve communication.
10. **Cut cards.** Create a foundation card only for a shared capability that makes later work safer or unblocks several feature cards. Cut feature cards as end-to-end behavior slices with explicit contracts. Record genuine dependencies as edges instead of hiding them in prose.
11. **Check independence.** A fresh reviewer verifies that each ready card has enough context, an observable result, test and operational acceptance, stable interfaces, and no undeclared dependency.
12. **Publish and refresh.** Mirror card status and key decisions to GitHub Projects. Before implementation, recheck volatile evidence and any decision whose trigger has fired.

### Card-generation rules

A foundation card must deliver a usable capability with proof. "Set up backend" is too vague. "Deploy the smallest authenticated service, with migration, unit, integration, end-to-end, observability, rollback, and local-development paths proven" is a candidate foundation card, but it may need several independently landing cards if one developer cannot finish it in a normal card window.

A feature card should own one user or operator outcome across the required layers. Several developers can work in parallel when cards meet at explicit contracts rather than shared unfinished internals. If feature B cannot be tested until feature A lands, either introduce a stable contract or record a real dependency. Do not label dependent work independent.

## Licensing, pinning, and staleness

- Keep repository URL, commit SHA, paths, license, retained notices, local patches, and evaluation result in `sources.lock.json` for every copied skill.
- Link to changing operational guidance at run time. Do not vendor whole AWS, Azure, Google, OWASP, SEI, or C4 documents unless their terms permit redistribution and the copied version has an update owner.
- A pinned skill gives reproducible behavior, not current knowledge. Research sources need their own retrieved-at, version, and recheck metadata.
- A moving `main` link is suitable for discovery but not for a decision record. An ADR should cite a release, document version, commit, or retained digest.
- Refresh skills separately from refreshing knowledge. Skill changes require behavioral evaluation. Source refreshes require claim revalidation and may reopen decisions or cards.
- The installed Matt Pocock bundle predates current architecture skills. Upgrade deliberately after diffing invocation semantics and running the skill evaluator. Do not silently replace the pinned copy.
- PStack is reproducibly pinned and licensed, but its model names and provider behavior can age even when the reasoning rules remain useful. Keep runtime routing outside the architecture method.
- Context7's open client is MIT, but the live private backend and changing indexed corpus mean that pinning the client does not make a retrieved answer reproducible. Retain decision evidence separately.
- The inspected AWS Agent Toolkit skill is Apache-2.0 at commit `96a27f2`. The inspected Microsoft skills repository is MIT at commit `41138f3`. Neither inspected project supplied a stable release for these exact skills, so pin the commit and schedule source review.

## Unresolved grill questions

1. Which decisions must the portfolio layer make itself, and which decisions must always wait for your approval?
2. When you give no scale or reliability target, should the system assume a small production workload, or must it keep grilling until every quality target is measurable?
3. Should team familiarity outweigh a technically stronger stack, and how much learning time can a foundation card spend?
4. Are cloud provider, deployment region, monthly operating budget, compliance regime, and data residency known before architecture work begins?
5. What evidence age makes a technology decision stale: a fixed time window, a major release, a security advisory, or any of these?
6. When documentation cannot settle a choice, how much time may the system spend on spikes and benchmarks before asking you to choose under uncertainty?
7. Is `.super-speckit` the canonical machine record with GitHub as a projection, or can GitHub edits change the canonical contract? How should conflicts resolve?
8. Who may accept or supersede an ADR: only you, a designated architect, or a quorum of the developers who will own the system?
9. What is the maximum expected implementation time and context size for one foundation card and one feature card?
10. Must every foundation card unblock at least two feature cards, or can risk reduction alone justify one?
11. Which card acceptance areas are mandatory by default: unit tests, integration tests, end-to-end tests, security checks, observability, deployment, rollback, and operator documentation?
12. When two feature cards need the same interface, who owns that contract, and can either feature developer change it after both cards become ready?
13. Should architecture review run once before card creation, at every major decision, or again before each card enters implementation?
14. When a stronger browser or computer-use harness is needed, what proof must a card checkpoint contain before another harness may continue the same feature?

## Bottom line

Use Matt Pocock's research and grilling patterns as the starting interaction model, the pinned PStack skills as code-design reasoning, and proportional QAW, ADD, ATAM, OWASP, SRE, and ADR review as the missing system-design layer. Add vendor specialists only when their platform is in scope. Keep research evidence separate from recommendations. Make every important recommendation traceable to current evidence and explicit project constraints. That combination can feel much more capable than a static skill while remaining auditable and independent of any one harness.
