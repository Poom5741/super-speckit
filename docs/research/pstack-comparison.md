# PStack comparison

**Research date:** 2026-10-05  
**Compared revisions:** Cursor `pstack` at [`e43c7ee`](https://github.com/cursor/plugins/tree/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack); Super-SpecKit at local commit `1bc2743`.

## What the referred project is

The project is **PStack**, a Cursor plugin in Cursor's public [`cursor/plugins`](https://github.com/cursor/plugins/tree/main/pstack) repository, not a separate product called “PStack from Cursor.” Its plugin manifest names **Lauren Tan** as author, and its own README identifies her as [`@poteto` on X](https://x.com/poteto). The public Cursor marketplace source describes it as rigorous workflows that can be parallelized with confidence. [Plugin manifest](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/.cursor-plugin/plugin.json), [PStack README](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/README.md).

Its normal entry point is `/poteto-mode`. That sticky mode selects one of 23 task playbooks, creates an explicit task list, and routes specialist skills as needed. It is a real, coherent engineering operating style, not just a collection of prompts. [Mode implementation](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/poteto-mode/SKILL.md), [playbooks](https://github.com/cursor/plugins/tree/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/poteto-mode/playbooks).

## Where PStack is genuinely better today

| Area | Why PStack is stronger | Why it matters |
| --- | --- | --- |
| Daily usability | `/poteto-mode` is a very small mental model, stays active across a session, and dispatches concrete playbooks for investigation, bugs, performance, refactors, shipping, PR babysitting, and session pickup. | An engineer can adopt it immediately without first learning a full delivery state machine. [Guide](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/docs/guide/02-poteto-mode.md) |
| Production maturity inside Cursor | It is a native Cursor plugin with declared agents, automations, model setup, task primitives, and a marketplace installation path. | The integration is more polished than Super-SpecKit's portable Markdown-command adapter model. [Plugin source](https://github.com/cursor/plugins/tree/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack) |
| Explicit model-role design | `/setup-pstack` detects usable models and records model/reasoning assignments for code delegates, judgment, panels, and swarm workers. | It makes model diversity an intentional part of execution, rather than a best-effort environment choice. [Setup skill](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/setup-pstack/SKILL.md) |
| Engineering judgment | Its principles are unusually concrete: model the domain, reduce reader load, make operations idempotent, test behavior rather than implementation, and challenge a failed premise after repeated repairs. | These habits improve the quality of individual code decisions before a QA gate is reached. [Principle index](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/poteto-mode/SKILL.md) |
| Adversarial code review | `interrogate` runs independent reviewers, synthesizes agreement/disagreement, and explicitly says not to auto-apply the findings. | This is a sharper, ready-to-use static-review workflow than Super-SpecKit's current generic optional code-review lane. It remains static review, not proof of app behavior. [Interrogate skill](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/interrogate/SKILL.md) |
| Self-improvement | `correct` turns recurring agent mistakes into architecture, types, lint, CI, or tests, and requires proof that a new check catches a historical error. `reflect` mines completed work for durable skill improvements. | This directly attacks repeated agent failure, an important missing operational loop in Super-SpecKit. [Correct](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/correct/SKILL.md), [Reflect](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/reflect/SKILL.md) |
| Project-specific verification | `create-verification-skill` creates a project-local harness with launch, health check, real-user driving, evidence, cleanup, and a maintained feature map; it insists the generated verifier is run before handoff. | This is a practical way to make real runtime verification easy enough to happen repeatedly. [Verification-skill creator](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/create-verification-skill/SKILL.md) |
| Day-two operations | PStack includes purpose-built playbooks for babysitting PRs, shipping verified stacks, safe pauses, session pickup, long autonomous runs, and per-PR ownership. | Super-SpecKit has handoffs and state records, but PStack is currently richer for the operational reality after implementation starts. [Playbook directory](https://github.com/cursor/plugins/tree/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/poteto-mode/playbooks) |

## Where Super-SpecKit is stronger or intentionally different

This is not a general win for PStack. Super-SpecKit is more opinionated about **independent release evidence**:

- It makes immutable candidate SHAs, clean QA worktrees, maker/checker separation, requirements-to-verification matrices, proof packs, confirmed-bug artifacts, regression-test obligations, and independent retest explicit release conditions.
- It distinguishes static review (including OCR) from runtime proof, and adds API/DB assertions, Playwright gates, exploratory QA, and the Rakazo private-browser Journey UX loop.
- It preserves Spec Kit's `spec.md`, `plan.md`, `tasks.md`, and convergence artifacts, and adds a human purpose gate, visual Project Atlas, Change Stories, and machine-checked work state.
- It is designed to be portable across agent runtimes. That portability is useful, but it also means it cannot assume Cursor's native task, cloud-agent, sticky-mode, and model-selection primitives.

Those are design claims about the local Super-SpecKit checkout, not claims that either system has been empirically proven superior. Neither project provides a published controlled comparison demonstrating that its workflow raises delivery quality.

## Important differences, not defects

PStack deliberately says that “the best spec is code” and does not make a planning artifact its default. Super-SpecKit deliberately begins with Spec Kit artifacts and a purpose confirmation. PStack will feel faster for a seasoned engineer with a clear task. Super-SpecKit is better aligned with a non-coder or a large, unfamiliar codebase where traceable intent, scope, and independent evidence are more valuable than minimizing ceremony. [PStack rationale](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/README.md#why-are-there-no-planning-skills).

PStack's swarm is designed around Cursor cloud workers and its own task integration. Super-SpecKit's worktree and evidence constraints are stronger boundaries for maker/checker separation, but PStack's built-in cloud execution is more convenient in Cursor. [Swarm skill](https://github.com/cursor/plugins/blob/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack/skills/swarm/SKILL.md).

## Recommendation for Super-SpecKit

Do not copy PStack wholesale or claim Super-SpecKit replaces it. Keep Super-SpecKit's evidence-first release contract and add only compatible proven ideas:

1. Add a **project verification-harness bootstrap and maintenance lane**, modeled on PStack's feature-map, launch/doctor/drive/evidence/cleanup contract. It should feed Super-SpecKit's existing matrix and proof packs.
2. Add a **recurring-mistake-to-enforcement lane** modeled on `correct`: promote repeated corrections first into architecture, then types/lint/CI/tests, with a counterexample proving each new rule.
3. Add a **decision-trail artifact** for long autonomous runs, then validate it against recorded state and evidence. This complements, rather than replaces, the YAML state authority.
4. Add a **configurable multi-model static-review panel** modeled on `interrogate`, explicitly classified as a reviewer lane that cannot pass runtime requirements.
5. Keep PStack as a compatible optional upstream skill source. Use PStack for deep engineering judgment and agent operations; use Super-SpecKit to enforce release evidence, independent QA, and the Spec Kit artifact lifecycle.

## Bottom line

PStack is better right now at making one skilled engineer-agent pair productive every day: tighter ergonomics, mature Cursor integration, role-aware model orchestration, operational playbooks, and mechanisms that turn repeated mistakes into enforcement. Super-SpecKit is stronger where its promise is most distinct: it defines an auditable release protocol where the maker cannot grade itself and runtime/user-journey evidence cannot be replaced by a good-looking code review. The best direction is interoperability, not a feature-count contest.
