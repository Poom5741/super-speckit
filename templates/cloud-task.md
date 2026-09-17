# Cloud delegation pack — <PACK-ID>

- Transport: `codex-cloud | centillex-desk`
- Role: `research | maker | bug-fix`
- Feature / phase / bug:
- Base branch and immutable SHA:
- Source handoff: `<durable handoff path>`
- Environment ID: `<configured Codex Cloud environment>`

## Bounded objective

<One outcome from the phase contract.>

## Constraints

- Read the cited native Spec Kit artifacts and handoff before changing code.
- Work only in the cloud task’s isolated branch/worktree.
- Do not merge, apply a diff to the local checkout, publish an issue, or claim QA approval.
- Do not include credentials, production data, or unredacted logs in the task.

## Required return evidence

- Candidate branch/SHA and changed files
- Commands actually run and their exit status
- Tests added or changed
- Open questions, failures, and unverified items
- Updated durable handoff for the independent checker

## Receiver verification

After applying any cloud diff locally, Super-SpecKit SHALL create a fresh independent QA worktree and repeat the relevant gates. A cloud completion report is advisory, not a release pass.
