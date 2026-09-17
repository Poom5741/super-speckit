# Follow-along review protocol

## Each step

1. State the exact action, test data/account, expected visible result, and evidence to capture.
2. Wait for the reviewer to perform it and return one of: `pass`, `fail`, `blocked`, `not-applicable`.
3. Record actual result, timestamp, URL/route, candidate SHA, and sanitized evidence path in the log.
4. Send `ask-super-speckit` a receipt: `{step, status, requirement_ids, evidence, next_action}`.

## Failure branches

| Result | Action |
| --- | --- |
| Pass | Continue to the next planned review step. |
| Fail with stable reproduction | Preserve evidence, create confirmed bug artifact, request a new `ss/bug/<id>` maker worktree, then independent retest. |
| Fail but ambiguous | Run the minimum reproduction attempts configured in `qa.reproduction_attempts`; label it suspected flake until confirmed. |
| Blocked | Record environment/dependency/access condition and wait for it to be fixed. Do not continue dependent steps. |
| Not applicable | Record rationale and authorized decision; surface it as unverified if it weakens acceptance coverage. |

## Suggested final route order

1. Environment identity and reset receipt
2. Primary user journey
3. Changed validation/error/empty state
4. Refresh/persistence or approved API/DB check
5. Authorization/role boundary
6. Narrow viewport and keyboard path when UI changed
7. Regression paths linked to repaired bugs
8. Summary and explicit unverified items

The reviewer may stop at any point. “Wait” is an explicit, truthful state, not inactivity or a pass.
