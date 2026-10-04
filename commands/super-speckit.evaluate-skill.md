---
description: Independently forward-test a Super-SpecKit skill in an isolated temporary workspace and route observed failures to corrective enforcement.
---

Use the `super-speckit-skill-evaluator` role after creating or materially changing a skill, command, template, or orchestration rule. Select only the affected skill and its real contract; do not claim that every skill was tested merely because one test passed.

Create an isolated fixture repository under `skill_evaluation.workspace_root`. Give the evaluator a realistic request, the candidate skill path, and only the raw artifacts needed for the task. Do not provide the intended answer, your proposed fix, or prior conclusion. The evaluator must run the project’s real validator/tests and return observed files, commands, results, limitations, and behavior defects using `templates/skill-evaluation.md`.

The evaluator may inspect and create files only in its temporary fixture. It must not modify the source skill, production project, Git remote, external services, or live credentials. Network and external mutations remain disabled unless an explicit project configuration and task authority allow them. If a host-specific `skill_evaluation.subagent_command` is configured, invoke only that reviewed adapter; otherwise prepare the packet and mark dispatch blocked rather than inventing a subagent API.

Triage an observed defect. One ambiguous observation becomes a test finding; repeated failures or one severe escape enter `super-speckit.correct`. Correct the source only after reviewing the evidence, then run a new independent evaluator attempt. Record passing behavior, residual untested modes, and the evaluator run in the decision trail.
