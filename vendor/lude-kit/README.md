<div align="center">

# Lude Kit

**A library of senior grade Agent Skills for Claude Code and OpenAI Codex.**

*Drop in a whole engineering org. Dispatch the right specialist when you need them.*

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-64-brightgreen.svg)](skills/README.md)
[![Spec](https://img.shields.io/badge/spec-Agent%20Skills-purple.svg)](https://agentskills.io/specification)
[![Status](https://img.shields.io/badge/status-public%20alpha-brightgreen.svg)](#status)

</div>

---

## The pitch in 30 seconds

General purpose AI coding agents are competent at everything and excellent at nothing. They read a lot but never shipped a feature. **Lude Kit fixes that.** Every skill is one role or one job, written to the bar of a senior practitioner, with a precise trigger description that activates it only when relevant.

Install the library once, and the right specialist shows up automatically:

```
> "Help me design a billing system that handles refunds and chargebacks."
  → staff-software-architect + fintech-engineer activate.

> "This Postgres query is slow. EXPLAIN ANALYZE attached."
  → postgres-expert + senior-performance-engineer activate.

> "We had a sev2 yesterday. Need the postmortem by Friday."
  → postmortem-author + incident-commander activate.

> "Build a RAG pipeline over our docs with a real eval set."
  → senior-rag-engineer + senior-eval-engineer activate.
```

Compose them into multi agent flows and your orchestrator hands the work to the right person at every step. No prompt bloat, no generic answers, no role confusion.

## Why this exists

A modern AI agent is a generalist who needs a senior on the team. Without one, you get answers that are technically correct but operationally naive: code that works in dev and burns in prod, designs that look good on a whiteboard and fall over at scale, security advice that's textbook and theatre. The fix is not a longer prompt. The fix is the right specialist on demand.

Lude Kit is that bench. Sixty four senior practitioners, each focused on one role or one job, each with strong opinions about how that work is done well. Drop them into your environment and the work gets better immediately.

## Status

**Public alpha.** Open sourced under Apache-2.0. Sixty four of a planned one hundred skills landed; bar holds across the full catalog. Track the road to one hundred in [ROADMAP.md](ROADMAP.md).

## Quickstart

```bash
git clone git@github.com:dimitris-di/lude-kit.git
cd lude-kit

# Claude Code skills (~/.claude/skills/)
./install/install-claude.sh

# Claude Code subagents (~/.claude/agents/)
./install/install-claude-agents.sh

# OpenAI Codex skills (~/.agents/skills/)
./install/install-codex.sh

# OpenAI Codex subagents as skills (~/.agents/skills/)
./install/install-codex-subagents.sh

# Slash commands (~/.claude/commands/ and ~/.codex/prompts/)
./install/install-claude-commands.sh
./install/install-codex-commands.sh
```

The scripts symlink, so future `git pull`s update your installed skills and subagents without reinstalling.

Custom install location:

```bash
CLAUDE_SKILLS_DIR=/path/to/claude/skills ./install/install-claude.sh
CLAUDE_AGENTS_DIR=/path/to/claude/agents ./install/install-claude-agents.sh
CODEX_SKILLS_DIR=/path/to/agents/skills  ./install/install-codex.sh
CODEX_SKILLS_DIR=/path/to/agents/skills  ./install/install-codex-subagents.sh
```

That's it. Start a conversation and the matchers pull the right skill when its triggers fire. Spawn named subagents with `Agent(subagent_type: "architect", ...)` and similar.

## What's in the library

**Sixty four skills across three categories**, organized so an orchestrator can scan and dispatch.

| Category | Count | What it contains |
|---|---|---|
| [`personas/`](skills/personas/) | 34 | Senior grade role personas an orchestrator can dispatch to. |
| [`capabilities/`](skills/capabilities/) | 10 | Cross role capabilities focused on a single job. |
| [`stacks/`](skills/stacks/) | 20 | Stack and technology specific experts. |

Full catalog with one liners and links: **[`skills/README.md`](skills/README.md)**.

### The personas (34)

**SDLC team** (the people you'd staff a feature with): architect, tech lead, PM, UX, frontend, backend, DevOps/SRE, QA, security, tech writer.

**Specialty roles**: data engineer, ML engineer, data scientist, MLOps, mobile, embedded, game, platform, developer advocate.

**Industry verticals**: fintech, healthcare, edtech, ecommerce, compliance.

**AI engineering**: LLM app, AI agent, RAG, eval, fine tuning, voice AI, computer vision, recommender, model router, AI safety.

### The capabilities (10)

Cross role power tools: code review, debugging, refactoring, performance engineering, incident command, API contract design, data modeling, migration planning, dependency auditing, postmortem authoring.

### The stacks (20)

**Frameworks and platforms**: Rails, Django, Next.js, Kubernetes, Terraform.

**Datastores**: Postgres, Redis.

**Clouds**: AWS, GCP.

**Mobile**: Swift/iOS, Flutter, React Native.

**Languages**: Go, Rust, Python, TypeScript, Java, C#/.NET.

**UI and testing**: Tailwind, Playwright.

## Subagents (30)

Skills load on demand inside a conversation when their triggers match. **Subagents** are named entry points you (or an orchestrator) explicitly dispatch via the `Agent` tool. They restrict tools, pin a model where it matters, and carry a system prompt that locks the right skill into the spawned conversation.

Lude Kit ships 30 curated subagents in [`subagents/`](subagents/), grouped three ways:

**Specialists (10)** mirror the highest leverage skills:
`architect`, `code-reviewer`, `security-reviewer`, `debugger`, `refactorer`, `perf-investigator`, `test-engineer`, `tech-writer`, `ic-coordinator`, `postmortem-writer`.

**Orchestrators (10)** plan and dispatch multi skill flows:
`orchestrate-feature-build`, `orchestrate-incident-response`, `orchestrate-migration`, `orchestrate-launch`, `orchestrate-security-review`, `orchestrate-perf-investigation`, `orchestrate-refactor`, `orchestrate-ai-feature`, `orchestrate-new-service`, `orchestrate-bug-fix`.

**Library maintenance (10)** keep the skill library healthy:
`skill-author-persona`, `skill-author-capability`, `skill-author-stack`, `skill-reviewer`, `skill-trigger-tightener`, `skill-deduplicator`, `skill-handoff-auditor`, `skill-freshness-checker`, `skill-catalog-updater`, `skill-eval-runner`.

Install them with `./install/install-claude-agents.sh`. After installation, dispatch with `Agent(subagent_type: "architect", prompt: "design the billing service")` and the subagent spawns with the right tools, model, and skill pre loaded.

Codex has no native subagent primitive equivalent to Claude Code's named dispatchable types. Each subagent is functionally a skill (description + system prompt), so `./install/install-codex-subagents.sh` wraps every subagent as a Codex skill folder under `~/.agents/skills/<name>/SKILL.md`. They auto activate via description matching on the Codex side instead of explicit dispatch.

## Slash commands (10)

Pre written prompts you invoke with `/<name>` inside Claude Code or Codex. Each one dispatches the right specialist subagents in parallel and returns a synthesized verdict, so you do not have to retype the orchestration logic every time.

| Command | What it does |
|---|---|
| `/review-macos-app` | Deep parallel review of a macOS app (Swift, sandboxing, perf, UX, App Store, OSS readiness). |
| `/review-website` | Web app review (perf, a11y, security, SEO, framework idioms). |
| `/review-api-service` | Backend API review (contract, schema, auth, observability, OSS readiness). |
| `/review-mobile-app` | iOS / Android review (cross platform decisions, offline, push, store policies). |
| `/review-cli-tool` | CLI review (UX, exit codes, signal handling, distribution channels). |
| `/prep-oss-release` | OSS readiness sweep (LICENSE, README, SECURITY, CI, secrets check). |
| `/security-audit` | Focused threat model + secure code review + supply chain. |
| `/perf-audit` | Measure first, find dominant cost, propose budget and regression guard. |
| `/a11y-audit` | WCAG 2.1 AA pass on any UI surface (web, native, mobile). |
| `/lude-style` | Apply Lude Kit prose rules (em dash + hyphen sweep), identifiers preserved. |

Install once with `./install/install-claude-commands.sh` and `./install/install-codex-commands.sh`. Then in a Claude Code or Codex session, type `/review-macos-app` (or any other) and the orchestration runs.

## How a skill works

Each skill is a folder containing a single `SKILL.md` with YAML frontmatter and a Markdown body. The frontmatter holds the trigger description that matchers preload at startup. The body holds the brief that loads only when the description matches the user's intent. This is **progressive disclosure**, your context window stays cheap until the skill is actually needed.

```
skills/personas/staff-software-architect/
└── SKILL.md
```

```yaml
---
name: staff-software-architect
description: >
  Use when designing a system, choosing a database / framework / cloud /
  message bus, writing an ADR or RFC, deciding build vs buy, planning
  capacity or scaling, reviewing an architecture diagram or proposal,
  sequencing a migration, or weighing technical trade-offs at the CTO
  level. Produces ADRs, RFCs, system diagrams, capacity plans. Not for
  implementation work, hands off to senior-backend-engineer /
  senior-frontend-engineer.
license: Apache-2.0
metadata:
  version: "1.0.0"
  category: persona
---

# Staff Software Architect

## Role
...
```

Every skill in this library follows the same nine section structure (Role → When to invoke → Operating principles → Workflow → Deliverables → Quality bar → Antipatterns → Handoffs → Quick reference) so an orchestrator can scan many of them quickly and reviewers know exactly what's missing.

The format follows the open [Agent Skills specification](https://agentskills.io/specification), so the same folder runs on Claude Code and OpenAI Codex with no per platform duplication.

## Multi agent composition

Lude Kit is designed for orchestrator style setups where a coordinating agent spawns subagents with specific roles. Every skill ends with a **Handoffs** section that names the partner skills for adjacent work, so the library composes:

```
User: "We want to add team SSO to the dashboard."

→ senior-product-manager       writes the one pager + success metric
→ staff-software-architect     picks SAML vs OIDC, writes the ADR
→ principal-security-engineer  threat models the auth flow
→ senior-ux-designer           flows sign in + invite + role switch
→ senior-frontend-engineer     implements the UI
→ senior-backend-engineer      implements endpoints + sessions
→ senior-qa-test-engineer      writes the regression suite
→ senior-devops-sre            rolls out behind a flag, sets SLOs
→ senior-technical-writer      writes admin doc + release notes
```

Each skill knows which skill to hand off to next. The library is a graph, not a list.

## Roadmap

| Batch | Theme | Status |
|---|---|---|
| 1 | SDLC personas (architect → writer) | ✅ shipped |
| 2 | Capability skills (review, debug, refactor, perf, postmortem, …) | ✅ shipped |
| 3 | Stack experts (Rails, Django, Next.js, K8s, Postgres, Terraform, Redis, AWS, GCP, iOS) | ✅ shipped |
| 4 | Specialty personas (data, ML, MLOps, mobile, embedded, game, blockchain, platform, devrel) | ✅ shipped |
| 5 | Industry verticals (fintech, healthcare, gov, edtech, ecommerce, streaming, IoT, automotive, compliance, logistics) | ✅ shipped |
| 6 | AI engineering (LLM apps, agents, RAG, eval, fine tuning, voice, CV, recommender, gateway, safety) | ✅ shipped |
| 7 | Language and framework stacks (Go, Rust, Python, TS, Java, .NET, Flutter, RN, Tailwind, Playwright) | ✅ shipped |
| 8 | More capabilities (a11y, i18n, feature flags, chaos, FinOps, modernization, releases, on call, DX, docs) | planned |
| 9 | AI infra (vector db, GPU infra, serving) + more verticals | planned |
| 10 | Hardening pass: cross skill review, polish, 1.0 release prep | planned |

**Target: 100 skills, then 1.0.** Want to shape what comes next? Open a [new-skill issue](.github/ISSUE_TEMPLATE/new-skill.yml).

## Contributing

PRs welcome. The bar is high and the process is opinionated. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening one.

Quick links:

- [Contributing guide](CONTRIBUTING.md), workflow, structure, commit style.
- [Style guide](shared/style-guide.md), the authoring bar.
- [Trigger vocabulary](shared/trigger-vocabulary.md), house style for descriptions.
- [Skill template](shared/skill-template/SKILL.md), copy paste starting point.
- [Examples](EXAMPLES.md), real prompts and the skills that activate.
- [FAQ](FAQ.md), the questions new visitors actually ask.
- [Roadmap](ROADMAP.md), batches 8 to 10 and beyond.
- [Changelog](CHANGELOG.md), what landed when.
- [Skill linter](SKILL_LINT.md), what CI checks on every PR.
- [Code of Conduct](CODE_OF_CONDUCT.md).
- [Security policy](SECURITY.md).

## Validation

A GitHub Actions workflow runs the linter on every PR. Run it locally with:

```bash
pip install pyyaml
python3 scripts/validate-skills.py
```

It checks every `SKILL.md` and every `subagents/*.md` for YAML validity, name/folder match, description budget (1024 chars), and no em dashes in the body. See [SKILL_LINT.md](SKILL_LINT.md).

Every skill in this repo is hand written, reviewed against the style guide, and verified against real prompts before merging. No autogenerated filler. If you submit a skill that does not change behavior in a useful way when activated, it will be declined with notes.

## Who's behind this

Built and maintained by **Dimitris Dimitriou** ([@dimitris-di](https://github.com/dimitris-di)). Questions, ideas, or pushback: open a [Discussion](https://github.com/dimitris-di/lude-kit/discussions) or reach out at **demetrisd25@gmail.com**.

## Acknowledgments

- The open [Agent Skills specification](https://agentskills.io/specification) for the cross platform format.
- [Anthropic Claude Code](https://docs.claude.com/en/docs/claude-code/skills) and [OpenAI Codex](https://developers.openai.com/codex/skills) for shipping skills as first class primitives.
- Every engineer whose habits, opinions, and war stories made it into these skills.

## License

[Apache-2.0](LICENSE). Use it, fork it, ship it.
