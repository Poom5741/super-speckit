---
name: rakazo-manual-qa
description: Run a repeatable Rakazo browser testing workflow that asks for the instance on first use, remembers project session details, prepares isolated data, and exercises user journeys with bounded stress and recovery checks.
---

# Rakazo manual QA

Use Rakazo as a persistent independent checker with its own computer. The supervising agent prepares the environment and testing strategy, sends a bounded assignment through the configured Rakazo UI, and validates the returned evidence. Use the host's available browser skill or browser tools, including ZCode's browser skill. Detect those capabilities; do not assume a specific tool name or invent an API.

For Super-SpecKit runs, read `commands/super-speckit.rakazo-journey.md` and use its candidate, environment, isolation, and defect-loop contracts. For standalone requests, apply the same preparation and evidence principles without creating unrelated delivery state.

## Remember the instance

On first testing use, ask for the Rakazo instance or direct bot link unless the user already supplied it or this project has a usable session record. Creating or installing the skill does not require the user's live link. While awaiting it, prepare the test strategy and fixtures. Store supplied non-secret connection details in `.super-speckit/qa/rakazo-session.json` under the target project, which is ignored by Git. For a standalone run use the selected local QA artifact directory. Reuse the session across related runs and resumptions; ask again only when the link is missing, the bot is ambiguous, or the user requests a different instance. Do not create a global personal profile.

An explicit project URL/bot setting in `super-speckit.yml` can bootstrap an empty session. A new user-supplied selection takes precedence. Preserve unrelated session fields on updates. The session records where and how to communicate; each candidate still needs fresh test state and evidence.

Use this profile shape, with absent values represented by null:

```json
{
  "instance_url": null,
  "bot_url": null,
  "bot_name": null,
  "transport": "browser",
  "conversation_url": null,
  "active_task_id": null,
  "last_run_id": null,
  "dispatch_status": "not-sent"
}
```

Persist a link only when the user supplies or identifies it. The upstream repository URL is not an instance. Reject URLs containing embedded credentials or token-bearing query strings; save the clean instance address and use the authenticated browser session. Keep passwords, API keys, and cookies outside the profile and task packet. If no URL is known, ask for it while preparing the strategy. Do not treat an empty profile as configured.

Open the saved URL and inspect the actual UI. Verify the intended instance and bot, then record the observed bot/conversation link for this run. If login is required, preserve the packet and request the user's login through the normal UI. Do not overwrite a known URL because the service is temporarily unavailable.

## Repeatable testing lifecycle

Treat the skill as a testing driver with setup, preflight, execution, evidence collection, teardown, and retest phases. Maintain a run directory containing the strategy, fixture manifest, dispatched packet, communication receipt, report, and retrieved evidence. Record phase and task identity in the session so another agent can resume without redispatching. Session memory never carries an earlier candidate's pass forward.

Default to declared user journeys plus risk-based exploratory stress checks. Select and record iteration counts, time budgets, input ranges, session variants, and concurrency bounds before dispatch. Stress here exercises product behavior under repeated or disrupted interactions. Claims about throughput, saturation, or many simultaneous users require a separately configured load tool and measurements; a manual browser agent alone cannot establish them.

## Prepare before dispatch

Read [test preparation](references/test-preparation.md). Derive the plan from the intended user outcomes, changed behavior, risk, and existing bugs. Prepare the QA deployment, isolated database fixtures, identities, and evidence destination before asking Rakazo to test. Rakazo's machine must be able to reach the app; supervisor localhost is not its localhost. Verify reachability from Rakazo's computer in an initial preflight.

Use `templates/rakazo-journey-task.md` for Super-SpecKit. Include task ID, candidate SHA or deployment identity, explicit allowed actions, fixtures/reset receipt, time budget, required journeys, exploratory charters, stop conditions, and return contract. Supply expected user outcomes and observable checks while leaving Rakazo free to vary actions within the boundaries. Do not send maker conclusions as expected findings.

## Communicate through the browser

The user request to use Rakazo for QA authorizes sending the scoped testing assignment to their identified QA bot. Confirm additional authority only for actions outside that scope. Use the observed conversation controls to paste or attach the packet and send it once. Retain the conversation URL, task ID, send time, and visible acknowledgment. Local task-packet paths are not remote attachments; transmit their contents or use an actual supported upload.

Before retrying an uncertain send, inspect the conversation for the task ID. Reuse an acknowledged assignment instead of launching a duplicate. Request a preflight acknowledgment naming the candidate, private computer, browser state, accessible app, and fixture readiness. If any fails, resolve the environment or mark the affected scope blocked before testing.

Read progress in the same conversation at bounded intervals and keep the user informed about material findings. Reply with scoped clarification or data fixes when needed. Send a cancellation if the candidate changes during the run; stop accepting its results for the new candidate. Browser access failures preserve the packet and explicit dispatch status. A reviewed project-local command adapter remains supported where configured.

## Collect and verify

Require a result for each declared journey and each exploratory charter, exact reproduction actions, expected/observed results, fixture identifiers, and sanitized evidence. Distinguish product defects, environment failures, and test-data mistakes. Exploratory testing expands coverage but does not replace the declared acceptance checks or establish exhaustive coverage.

Rakazo's filesystem paths are remote. Retrieve evidence using available download/upload or workspace transfer capabilities, preserve it under the local run's QA directory, and map remote paths to retrieved files. If transfer is unavailable, retain accessible evidence links and mark any unverifiable requirement accordingly. Never claim a file exists locally from its remote path alone. Require only capture formats supported by the actual tools; explicitly record unavailable trace/video capture.

Validate candidate/deployment identity, setup receipt, journey coverage, and evidence accessibility before recording a pass. Route confirmed bugs into the existing fix loop. After a fix, prepare fresh fixtures and a new task for the new candidate, rerun affected checks and the full declared journey set, and add focused exploration around the failure. Keep original failure evidence. A summary saying "all good" without supporting observations does not satisfy the return contract.
