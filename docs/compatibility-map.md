# Complementary workflow map

Super-SpecKit keeps native Spec Kit as the source of requirements, plan, tasks, and convergence. This map records selected upstream practices only where they add a missing control; it does not import competing orchestration commands.

| Source | Adopted part | Super-SpecKit location | Not adopted |
| --- | --- | --- | --- |
| [GSD](https://github.com/gsd-build/get-shit-done) | phase discussion/research, plan checking, execution summaries, milestone audit | phase contract, plan-quality gate, handoff, release evidence audit | GSD command hierarchy, mutable self-certification, provider-specific dispatch |
| [Matt Pocock skills](https://github.com/mattpocock/skills) | repo-local setup, research, domain grilling, TDD, diagnosis, code review, navigation, handoff | pinned upstream skills and ask-super-speckit routing | issue mutations without explicit project setup; replacing native Spec Kit artifacts |
| [MAQA](https://github.com/GenieRobot/spec-kit-maqa-ext) | dependency-aware isolated feature lanes | parallelization plan and maker worktrees | static analysis as release proof |
| [AWO](https://github.com/ystepanoff/awo) / [Orka](https://github.com/Dusttoo/orka) | read-only checking, proof pack, policy/budgets | QA receipts, proof pack, risk policy | automatic merge |
| [vibe-design-skills](https://github.com/nick3/vibe-design-skills) | foundation, design execution, independent visual evaluation | pinned upstream design lane | self-evaluation as release approval |

## GSD-compatible execution rhythm

1. Discuss or research only the uncertainty that blocks a phase; record decisions in native spec/plan or the phase contract.
2. Check the plan for outcome, requirements, dependencies, verification, and bounded scope before creating a worktree.
3. Execute one committed slice in a maker lane, preferably test-first where feasible.
4. Emit a durable handoff when a lane pauses, fails, or completes; never rely only on chat memory.
5. Independently verify the candidate and audit the milestone against its original requirement IDs before a human merge decision.

This gives the useful GSD feedback loop while maintaining Super-SpecKit’s independent checker and evidence rules.
