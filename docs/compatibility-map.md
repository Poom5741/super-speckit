# Complementary workflow map

Super-SpecKit keeps native Spec Kit as the source of requirements, plan, tasks, and convergence. This map records selected upstream practices only where they add a missing control; it does not import competing orchestration commands.

| Source | Adopted part | Super-SpecKit location | Not adopted |
| --- | --- | --- | --- |
| [GSD](https://github.com/gsd-build/get-shit-done) | phase discussion/research, plan checking, execution summaries, milestone audit | phase contract, plan-quality gate, handoff, release evidence audit | GSD command hierarchy, mutable self-certification, provider-specific dispatch |
| [Matt Pocock skills](https://github.com/mattpocock/skills) | repo-local setup, research, domain grilling, TDD, diagnosis, code review, navigation, handoff | pinned upstream skills and ask-super-speckit routing | issue mutations without explicit project setup; replacing native Spec Kit artifacts |
| [OpenAI frontend testing/debugging](https://github.com/openai/plugins/tree/main/plugins/build-web-apps/skills/frontend-testing-debugging) | rendered-app target flow, console/network, screenshot, and interaction checks | opt-in external browser-plugin integration; equivalent evidence is captured through Playwright when unavailable | vendoring source without a redistribution license; using browser checks as independent QA approval |
| [MAQA](https://github.com/GenieRobot/spec-kit-maqa-ext) | dependency-aware isolated feature lanes | parallelization plan and maker worktrees | static analysis as release proof |
| [AWO](https://github.com/ystepanoff/awo) / [Orka](https://github.com/Dusttoo/orka) | read-only checking, proof pack, policy/budgets | QA receipts, proof pack, risk policy | automatic merge |
| [vibe-design-skills](https://github.com/nick3/vibe-design-skills) | foundation, design execution, independent visual evaluation | pinned upstream design lane | self-evaluation as release approval |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | searchable design intelligence for visual direction, token choices, motion, chart, UX, and stack decisions | pinned premium-design direction lane | mixing catalog styles; replacing project stack or human design approval |
| [Frontend Agent Skills](https://github.com/hueyexe/frontend-agent-skills) | focused composition, interaction, forms, IA, usability, content, accessibility, design-system, and research specialists | selected on demand by the design-first bridge | loading every specialist for every screen; self-approval of rendered UI |
| [Centillex Desk](https://centillex.com/desk) | optional local “pack and move” transport across agent vendors | redacted cloud-task pack and optional Desk adapter | evidence/release authority |
| [Codex Cloud](https://learn.chatgpt.com/docs/codex/cli) | configured cloud execution and local diff collection | primary `codex cloud exec/status/diff/apply` adapter | automatic application into integration or QA approval |

## GSD-compatible execution rhythm

1. Discuss or research only the uncertainty that blocks a phase; record decisions in native spec/plan or the phase contract.
2. Check the plan for outcome, requirements, dependencies, verification, and bounded scope before creating a worktree.
3. Execute one committed slice in a maker lane, preferably test-first where feasible.
4. Emit a durable handoff when a lane pauses, fails, or completes; never rely only on chat memory.
5. Independently verify the candidate and audit the milestone against its original requirement IDs before a human merge decision.

This gives the useful GSD feedback loop while maintaining Super-SpecKit’s independent checker and evidence rules.
