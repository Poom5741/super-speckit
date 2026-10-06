# Rakazo Journey UX Task — {{feature}} / {{candidate_sha}} / {{run_id}}

## Assignment

- Role: independent persistent manual-browser checker (Rakazo)
- Candidate SHA: `{{candidate_sha}}` (immutable; do not change it)
- QA worktree / environment receipt: {{environment_receipt}}
- Live app URL: {{app_url}}
- Test-data namespace / reset receipt: {{test_namespace}}
- Deadline: {{deadline}}

## Preflight and data preparation

{{setup_receipt_and_fixture_manifest}}

Confirm the candidate/build identity, private Computer, clean browser, app reachability from your machine, and fixture readiness before testing. Supervisor localhost is not your localhost. Return a blocked result for an unmet prerequisite.

## Testing boundaries and exploration

{{allowed_actions_stop_conditions_and_time_budget}}

{{risk_based_exploratory_charters}}

Record variants actually attempted and untested scope. Preserve findings before fixture cleanup. Do not use database edits to bypass a user workflow under test.

## Isolation contract

- Use a private Rakazo Computer and a clean browser profile.
- Use only the supplied test identities and fresh isolated fixtures. Do not expose credentials in this file or returned evidence.
- Do not edit product code, the maker worktree, Git history, dependencies, configuration, or the candidate.
- You may write only QA artifacts under `.super-speckit/qa/{{run_id}}/`.
- Do not delegate this assignment to a peer agent. Report an unavailable live model/browser as `not-run`, never `passed`.

## Declared journeys

{{declared_journeys}}

For each journey, preserve the URL, viewport, starting state, exact actions, observed result, and sanitized screenshot/trace/video/log paths. Inspect applicable validation/recovery, empty/loading/error, authorization, refresh/persistence, narrow viewport, and keyboard paths.

## Return contract

Write `journey-ux-report.md` at `.super-speckit/qa/{{run_id}}/journey-ux-report.md` and return:

1. `status`: `passed`, `failed`, `blocked`, or `not-run`.
2. Candidate SHA and environment receipt used.
3. Every declared journey with an outcome and evidence paths.
4. Each finding with exact reproduction steps, observed/expected behavior, classification, and evidence paths.
5. Explicit unverified or blocked scope.
6. Preflight receipt, exploratory charter observations, and remote-to-local evidence transfer instructions or accessible links. Remote filesystem paths alone do not prove evidence reached the supervising agent.

`passed` means only that every declared journey passed against this candidate and no confirmed defect remains in this declared scope. It does not mean the product has no UX bugs.
