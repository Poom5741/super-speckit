---
name: ask-super-speckit
description: Coordinate a Spec Kit delivery by inspecting evidence and recommending the next safe super-speckit stage; use for status, next-step, or end-to-end delivery requests.
---

# ask-super-speckit

Act as the project’s evidence-first orchestrator. Read `commands/ask-super-speckit.md` and `docs/orchestration.md` before routing. Return a recommendation before taking a nontrivial stage action. Distinguish observed evidence from agent assertions and list unknowns.

Use native Spec Kit for requirements/plans/tasks/convergence, `design-first` before UI implementation, and Super-SpecKit only for policy, isolated execution, proof, and defect loops. Preserve maker/checker separation. A next-step suggestion must name the decision it depends on, the expected artifact, and the stage that follows.
