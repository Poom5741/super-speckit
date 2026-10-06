---
description: Prepare, dispatch, and verify an independent Rakazo manual-browser Journey UX review without inventing a Rakazo integration.
---

Use this as the default adapter for `super-speckit.journey-ux` when `manual_journey_agent.provider: rakazo` is enabled.

Read `skills/rakazo-manual-qa/SKILL.md` for saved-instance discovery, browser communication, data preparation, and remote evidence retrieval.

First re-check feature state, immutable candidate SHA, environment receipt, open bugs, and the clean QA environment. Create `rakazo-journey-task.md` from `templates/rakazo-journey-task.md` beneath the configured QA report root. It must name the candidate SHA, run ID, declared journeys, test-data namespace, app URL, evidence destination, and report destination. It must contain no secrets.

Rakazo is the independent checker, never the maker. Use a **private Rakazo Computer** and clean browser profile. It may use only fresh test accounts/fixtures and may write only QA artifacts under `.super-speckit/qa/<run-id>/`; it must not edit product code, write to the maker worktree, commit, rebase, merge, or change the candidate. A shared computer, persistent logged-in browser profile, or peer delegation is an explicit environment exception and cannot count as clean independent QA.

If `manual_journey_agent.rakazo.dispatch_command` is non-empty, run that reviewed project-local adapter with the task-packet path and retain its invocation/result as evidence. Otherwise use the saved instance and identified bot through the host's available browser skill/tools, following `skills/rakazo-manual-qa/SKILL.md`. Record actual send acknowledgment and the conversation link. If neither transport is usable, retain the packet and mark the run blocked with the specific missing URL, login, browser capability, or unavailable service. Never infer a generic Rakazo REST endpoint, command line, or credential format.

Require Rakazo to return the structured report and exact evidence paths. The orchestrator independently checks that the report's candidate SHA equals the current candidate, the environment receipt is current, all declared journeys have an outcome, and every reported failure has actions and reproducibility evidence. Only then continue through `super-speckit.journey-ux` and record the final state. A live-model or browser run marked unavailable is `not-run`/blocked, never pass.

Confirmed UX failures enter the normal isolated bug worktree → regression coverage → independent QA retest loop. After every confirmed fix, send Rakazo a new packet for the latest candidate and rerun the **full declared journey set**.
