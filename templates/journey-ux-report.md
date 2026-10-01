# Journey UX Loop — {{feature}} / {{candidate_sha}} / {{run_id}}

Environment receipt: {{environment_receipt}}
Independent checker: {{checker}}
Manual browser agent: Rakazo (or recorded adapter exception)
Rakazo task packet: {{rakazo_task_packet}}

## Declared journeys

| Journey ID | User goal | Starting state / test data | Critical path | States and boundaries inspected | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |

Include the changed primary journey and relevant validation/recovery, empty/loading/error, authorization, refresh/persistence, narrow viewport, and keyboard paths. State `not-applicable` only with a rationale.

## Findings

| Finding ID | Journey / step | Observation | Reproduction | Classification | Evidence | Bug artifact / decision |
| --- | --- | --- | --- | --- | --- | --- |

Classify `confirmed`, `suspected-flake`, `environment`, `test-defect`, or `accepted-exception`. A screenshot alone is not a confirmed defect; retain the exact action and observed behavior.

## Retest loop

| Bug ID | Fix candidate SHA | Independent QA run | Affected journey retest | Full declared-set rerun | Status |
| --- | --- | --- | --- | --- | --- |

## Outcome

- [ ] Every declared journey passed after the latest candidate.
- [ ] No confirmed UX defect remains in the declared journey scope.
- [ ] Unverified / blocked items are listed below and block a UI release claim.

### Unverified or blocked scope

{{unverified}}
