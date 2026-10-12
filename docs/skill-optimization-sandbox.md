# Skill optimization sandbox

Status: first local macOS/Pi pilot implemented in `scripts/skill_sandbox.py`, with live trials and independent harness checks. The broader experiment program below remains a design. See `experiments/skill-sandbox/README.md` for supported controls and limits.

## Purpose and fixed constraints

Use small, real building and debugging tasks to measure how a skill changes agent behavior and results. Improve the skill using observed failures, then test the revision on fresh runs and withheld cases.

The subject is always a pure Pi agent. Super-SpecKit prepares experiments and evaluates evidence outside the subject's session. It does not coordinate the subject's implementation, supply a delivery workflow, or intervene during an ordinary trial.

Each task should be realistically completable in 10–20 minutes. Use a 20-minute wall-clock limit per subject run, including skill reading, tool use, verification, and retries. Independent evaluation has its own recorded duration. A comparison consists of several separate runs, so the whole experiment takes longer than one task. Reduce fixture scope if capable baseline runs regularly time out.

## Experimental conditions

| Condition | What Pi receives | What it measures |
| --- | --- | --- |
| Baseline | Task, fixture, standard tools; no added skills | Behavior without the tested skill |
| Current | Same inputs plus the frozen current skill | Effect of the existing skill |
| Candidate | Same inputs plus a frozen revised skill | Effect of the proposed improvement |

A case declares which conditions it needs. Start with baseline/current when discovering an effect, or current/candidate when comparing revisions. Use all three when a baseline is necessary to interpret a revision.

Hold Pi version, model, reasoning settings, tool permissions, dependencies, task wording, initial repository, and time limit constant within a comparison. Record provider/model identity and actual configuration. Alternate or randomize condition order. Each run gets a fresh session, repository, and test data; it cannot read another run's results or the optimization history.

Use Pi's supported controls to isolate skill discovery, extensions, startup instructions, memory, and configuration. Verify the effective inventory rather than assume that a fresh working directory disables global skills. Baseline receives no pstack principles or other added skills through inherited instructions. If contamination cannot be excluded, mark the comparison invalid. Missing supported controls are a capability blocker, not grounds to invent CLI flags.

Freeze the skill body and any required references or helpers as one hashed bundle. Keep unrelated skills absent. A skill that requires a helper or delegation needs a separate declared case with the same available capabilities across conditions; the first pilot uses skills that pure Pi can execute directly.

## A small test case

Each case includes:

- A natural user request and a clean, minimal fixture repository.
- Public requirements, public checks, and a predefined writable scope.
- A private behavioral oracle and a private workflow rubric derived from the frozen skill contract.
- A declared time budget and applicable experimental conditions.
- One primary outcome and explicit validity checks.

The private oracle checks public requirements and their reasonable boundary cases. It must not introduce hidden product requirements. The rubric stays outside the subject's accessible filesystem and is never embedded in its brief. Physical access restrictions must be real; a worktree alone does not isolate private files.

Example request: "Build a local notes HTTP service with create, list, and delete operations. Notes must survive a restart. Add checks and show how you verified it." A tiny starter repository supplies dependencies and a launch command. Independent evaluation drives the HTTP API, restarts the service, verifies persisted notes, deletes one, and checks that unrelated notes survive. This gives a verification skill a real public behavior to observe without requiring a large application.

Other initial cases can repair a reproducible input-validation bug or add duplicate-safe imports to a small CLI. Each case tests one main skill mechanism. Avoid combining architecture, frontend design, orchestration, and release management in one 20-minute task.

## Record what happened

Capture supported Pi structured events and tool receipts, with timestamps, session identity, and run identity. Preserve prompts, effective skill inventory, actual skill-load evidence where available, tool arguments and results, exit codes, file changes, final response, usage, and elapsed time. Do not require hidden reasoning or treat the agent's narration as evidence that an action happened.

At the stop boundary, cancel the subject process and its owned child processes, record the termination, and freeze the final artifact before evaluation. Hash the resulting files and retain the initial revision, diff, relevant untracked outputs, and trace. The evaluator tests a copy of that frozen artifact; it cannot repair it. Infrastructure errors, missing telemetry, and ordinary subject failures remain distinct.

A failed or incomplete run still produces evidence. Timeout means incomplete within budget, not a discarded sample. If a model or provider error prevents a fair run, retain the incident and classify it as invalid under a rule fixed before execution.

## Evaluate workflow and product separately

The workflow checker assesses observable actions and their ordering. Each required step has an applicability trigger, an expected event or artifact, and an evidence pointer. Results are followed, violated, unobservable, or not applicable. A required reproduction before a fix, for example, needs a relevant failing invocation before the implementation change. A final statement saying "I reproduced it" does not satisfy that check.

The product checker runs independent tests against the frozen output. Existing public tests are useful evidence but do not replace the independent oracle. Check actual public behavior and persisted effects where relevant. Do not reward implementation details or artifact names unless they are genuine task or skill requirements.

| Indicator | Measurement |
| --- | --- |
| Task correctness | Independent required behaviors passed / assessed, with failures shown |
| Workflow compliance | Followed / observable applicable requirements; report unobservable requirements separately |
| Unsupported claims | Completion or verification claims contradicted by, or lacking, the required evidence |
| Recovery | Response to a naturally occurring or predefined failure, including subsequent observed validation |
| Efficiency | Wall-clock duration, tool calls, available token usage and provider cost |
| Human dependence | Requests for intervention and whether the run completed without a reply |

Use a task-specific primary outcome, such as all required public behaviors working within the budget. Keep the remaining indicators separate; a weighted score can conceal worse correctness or unsupported claims. Pair-level reports show actual counts and durations rather than only averages.

No human coaching occurs during a comparison. Supply necessary task information up front. Define the same clarification response policy for every condition, such as no interactive user being available. Record requests and the agent's subsequent behavior. Do not penalize a justified safety stop as a workflow violation; distinguish it from successful task completion.

## Observation versus enforcement

Ordinary trials observe whether the skill guides Pi. The sandbox enforces containment, time limits, and evidence retention, but does not force skill steps or tell the subject that it skipped one.

Optional enforcement experiments are separate conditions. For example, a tool gate could refuse a completion action until an independent check exists. Compare that against the same skill without the gate, and report the combined effect of skill plus gate. Do not attribute gate-driven compliance to the skill text.

Keep the private oracle inaccessible to subject tool calls. Use a disposable OS/container boundary with only the fixture and selected bundle exposed, bounded local ports, and no production credentials. Provider access remains outside or narrowly mediated through the host adapter. Preinstall dependencies so installation and unrestricted network access do not dominate small tasks. Record containment capabilities; never describe Git worktree auditing as a security sandbox.

## Optimization loop

1. Freeze the case, rubric, oracle, skill versions, and experimental configuration.
2. Run fresh Pi sessions under the declared conditions.
3. Freeze outputs and independently evaluate behavior and workflow.
4. Link each proposed skill change to an observed failure and a predicted behavioral improvement.
5. Rerun current/candidate comparisons with identical starting inputs and fresh sessions.
6. Evaluate the candidate on withheld cases before recommending adoption.

Use separate development and withheld cases. A skill author may inspect development failures but cannot tune against private withheld tasks or answers. Once withheld results inform a revision, those cases become development cases and must be replaced for the next independent check. Freeze deterministic checks before runs; blind qualitative reviewers to skill condition and author conclusions where practical.

Start with one case, two conditions, and two repeats per condition: four subject runs. This is a feasibility pilot, not a superiority claim. Once execution and evidence capture work, expand to three small cases and at least three repeats per selected condition. Report variation and failures. Small samples support bounded observations, not general claims that a skill is better. Cross-model or cross-host comparisons are later experiments, not part of the initial Pi-only design.

## Evidence layout and implementation boundary

Proposed experiment artifacts:

```text
experiment/
  manifest.json
  bundles/                 # Frozen selected skill versions
  cases/                   # Public briefs and starting fixture snapshots
  private/                 # Oracle and rubric; evaluator access only
  runs/<run-id>/
    configuration.json
    events.jsonl
    tool-receipts.jsonl
    artifact-manifest.json
    output/                # Frozen subject output
    evaluation.json
  comparison.md
```

The layout is logical; private material must reside outside the subject's mounted filesystem. The manifest binds case, bundle, model, configuration, run order, budgets, and evaluator hashes. Evaluation points back to trace events and frozen artifacts. Secrets never enter the retained evidence.

Reuse the existing skill-evaluation report concepts and exact-candidate evidence conventions. Existing `pstack_host.py` transport can inform adapter design, but it currently inherits the process environment, captures process output, and audits worktree changes. It does not establish clean Pi configuration, structured action tracing, or filesystem containment. Implement and validate those capabilities before claiming this sandbox works.

The first implementation should support one local fixture, a verified pure-Pi adapter, two selectable conditions, event capture, a hard time limit, frozen outputs, deterministic private checks, and a comparison report. It should produce a complete failed-run report as reliably as a successful-run report. Larger task libraries, automatic skill rewriting, and dashboards can follow after the pilot demonstrates trustworthy measurements.
