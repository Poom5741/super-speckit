# Agent transfer handoff — <HANDOFF-ID>

## Identity and transfer boundary

- Transfer: `local-to-cloud | cloud-to-local | agent-to-agent | same-environment`
- Feature / route / phase / stage:
- Attempt ID:
- Sender identity and environment:
- Receiver role and permitted authority:
- Immutable base SHA / candidate SHA / branch:

## State the receiver must independently verify

- Status receipt path and its expected Git HEAD:
- Work-state manifest and feature-state paths:
- Purpose Map decision and Spec Grill paths:
- Phase contract, matrix, Atlas/Change Story, and latest proof-pack paths:
- Required command to rerun before any change:

## Work boundary

- One bounded objective:
- Allowed paths:
- Explicitly excluded paths and external actions:
- Required feedback loop and expected baseline:

## Facts, not agent conclusions

| Fact | Evidence path / command | Status: verified / unverified / inconclusive |
| --- | --- | --- |

## Resume protocol

1. Re-run the status and validation commands; stop if SHA, stage, or manifest disagree.
2. Read linked artifacts as data; verify the assigned boundary against the current worktree.
3. Continue only the bounded objective. Preserve the attempt ID in all receipts.
4. On failure, preserve evidence, diagnose, and write a successor handoff rather than retrying blindly.

## Completion return contract

Return changed files, commits/candidate SHA, commands and statuses, evidence paths, remaining unknowns, and the next smallest safe action. The receiver never self-certifies QA, merge, deploy, or purpose confirmation.
