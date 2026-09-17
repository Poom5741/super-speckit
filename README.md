# super-speckit

`super-speckit` is a Spec Kit companion that makes **independent runtime verification** a release condition. It retains Spec Kit's `spec.md`, `plan.md`, `tasks.md`, and `converge` artifacts; it adds a controlled maker/checker loop around each implementation slice.

Static review is evidence about code. A passing runtime verification is evidence about behavior. Neither is a proof of every possible behavior; both are recorded separately.

## What this first version includes

- feature and bug-fix worktrees isolated from the integration checkout;
- disposable QA worktrees created from the candidate commit, never from the maker's dirty tree;
- a requirements-to-verification matrix and machine-readable run state;
- deterministic gates (format, lint, unit, integration, build), Playwright E2E, optional API/DB assertions, and exploratory browser QA;
- OCR as an independent static-review lane with triage, never as a runtime pass;
- evidence capture and a reproducibility rule before a QA failure becomes a bug;
- a design-first HTML preview, design-system brief, and approval record before UI implementation;
- policy-selected gates, environment-readiness receipts, immutable proof packs, and bounded repair loops;
- a human follow-along final review that reports each observed result to `ask-super-speckit`, waits truthfully on blockers, and routes confirmed failures to isolated repair/retest loops.
- GSD-style phase contracts, plan-quality checks, durable handoffs, and milestone audits—without replacing Spec Kit’s core artifacts or independent QA.
- optional Codex Cloud delegation for bounded research, maker, and bug-fix work; cloud output returns through a fresh local independent QA lane.
- a durable bug artifact, regression test obligation, independent retest, project QA summary, and explicit unverified items.

It is intentionally an extension, not a competing fork of the Spec Kit CLI. The upstream project changes quickly; install normal Spec Kit first and keep its commands current.

## Install into a Spec Kit repository

1. Initialise or update native Spec Kit for your chosen agent (`specify init ...`).
2. Copy this directory into the repository as `.super-speckit/`, or place it in your agent's skills directory and invoke `$super-speckit`.
3. Copy `config/super-speckit.yml` to the repository root as `super-speckit.yml` and set real commands, URLs, seed/reset behavior, design-system sources, and any protected data rules.
4. Add the short policy in `templates/constitution-addon.md` to `.specify/memory/constitution.md`.
5. Run `python3 scripts/super_speckit.py init --repo .` and commit the generated baseline state/config.

Optionally install the native workflow with `specify workflow add workflows/` (or package this directory); it pauses at design, implementation, and release decisions. The workflow deliberately invokes Super-SpecKit by prompt so it remains portable across agent integrations.

Requirements: Git worktrees, Python 3.9+, a test runner, and for browser gates Playwright plus an application start command. OCR is configured as an external command/API adapter; no credentials are stored in this kit.

## Start with `ask-super-speckit`

`ask-super-speckit` is the only normal entry point. It reads current Spec Kit artifacts and Super-SpecKit state, gives a short evidence-backed **next-step suggestion**, then executes only the stage requested or approved by the operator. It never silently merges, creates external issues, or dispatches a vendor design tool.

For a UI-facing change it begins with `design-first`: produce a static HTML prototype and `design-brief.md`, compare it against any declared design system, and wait for a recorded design decision. The prototype is a decision artifact—not production code. If an external designer is available, it emits a portable prompt/hand-off bundle for v0, Google Stitch, or Claude Design; their output is imported and reviewed like any other untrusted design input.

## Daily flow

```text
ask-super-speckit → speckit.specify → clarify/checklist → design-first (UI) → design decision
      ↓
speckit.plan → speckit.tasks → analyze → risk/parallelism plan
      ↓
super-speckit.start FEATURE-123 → maker worktree → commit candidate
      ↓
super-speckit.verify FEATURE-123 → clean QA worktree → gates + E2E + exploration
      ├─ confirmed failure → bug artifact → bug maker worktree → independent retest
      └─ pass + OCR triage resolved/accepted → merge decision
      ↓
speckit.converge → project QA summary (including unverified scope and proof-pack)
```

Use `commands/` as agent slash-command definitions or adapt them to your integration. The orchestrator is deliberately a small, inspectable state/evidence tool—not an autonomous merger.

## Safety and operating rules

- QA may write only `.super-speckit/qa/`, `.super-speckit/bugs/`, and ephemeral files in its own worktree. It must not edit, commit, or rebase the maker worktree.
- QA checks out an immutable candidate SHA in a freshly created worktree. It must reset fixtures, use isolated test accounts/namespaces, and delete the worktree afterward unless evidence requires preservation.
- A failed automated test with stable evidence can be filed immediately. A flaky or exploratory observation must be reproduced under the configured rule before becoming a confirmed bug.
- OCR findings are triaged as `fix`, `accepted-risk`, `false-positive`, or `needs-human`; only `fix` blocks merge. OCR cannot satisfy any runtime matrix row.
- A confirmed bug cannot close until its regression test is added or an explicit exception is recorded, the fix is independently retested, and required gates pass.
- A human (or separately authorized merge system) makes the final merge; this kit only emits a merge-readiness decision.

## Commands and artifacts

See [commands](commands/README.md), [design-first skill](skills/design-first/SKILL.md), [orchestrator skill](skills/ask-super-speckit/SKILL.md), [schemas](schemas/README.md), [orchestration rules](docs/orchestration.md), [state machine](docs/state-machine.md), and the [worked example](examples/feature-042.md).

The shipped upstream design skills and their pinned source revisions are listed in [sources.lock.json](sources.lock.json). The locally authored final review procedure is [final-manual-review](skills/final-manual-review/SKILL.md); it is intentionally limited to human/AI handoff, evidence, waiting, and bug-routing mechanics.

See [compatibility map](docs/compatibility-map.md) for what was selectively adopted from GSD, Matt Pocock’s engineering skills, MAQA, AWO/Orka, and the design workflow suite—and what was intentionally kept out to avoid conflicts.

## Codex Cloud delegation

Enable `delegation.enabled` and set a Codex Cloud environment ID in the project configuration. `super-speckit.delegate-cloud` creates a redacted, bounded pack from a durable handoff, submits it with `codex cloud exec`, and records the cloud task ID. `collect-cloud` reviews the diff before any application. Cloud work is a maker lane only: its result always enters a fresh independent QA worktree, so a cloud agent never grades its own implementation. Centillex Desk can use the same pack as an optional local cross-vendor transport.

## Verify the kit itself

```bash
python3 -m unittest discover -s tests -v
python3 scripts/super_speckit.py validate --repo .
```

## Upstream influences

This design preserves Spec Kit's artifact-driven SDD and convergence model. It takes the isolated per-feature worktree/coordinator idea from MAQA, but replaces its static-only QA gate with an independent clean runtime lane. Its exploratory role split is inspired by `sdlc-skills` manual-qa, condensed into a portable role protocol. See `docs/references.md` for pinned links and integration notes.
