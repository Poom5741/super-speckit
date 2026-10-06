# Manual test strategy and data preparation

## Environment receipt

Identify the QA deployment and immutable candidate. Record app URL, build identity check, database isolation boundary, schema/migration version, setup commands actually executed, fixture namespace, and reset verification. Use the project's existing QA setup commands. Do not guess database credentials, run migrations against production, or reset an unverified database target.

Use a disposable database, schema, or tenant scoped to the run. Apply required migrations and seed through existing scripts or supported APIs. If these are missing, prepare a reviewable setup procedure and use the smallest supported mechanism. Verify seeded state with read-only assertions or API responses. A seed command exiting successfully does not prove all required fixtures exist.

Keep privileged database setup with the supervisor or a separately scoped setup process. Rakazo tests through normal user interfaces unless a case explicitly authorizes a supporting API or read-only database observation. Report queries can corroborate persistence; database edits must not bypass the behavior being tested.

## Fixtures selected by risk

Include applicable states rather than every possible permutation:

| Risk | Useful starting data and observation |
| --- | --- |
| Authentication and authorization | Fresh signed-out state, distinct roles, two isolated owners/tenants, expired session; verify forbidden data remains inaccessible. |
| Creation and persistence | Empty account, one valid item, duplicate/conflicting item; verify reload and second-session visibility through the intended interface. |
| Forms and recovery | Missing, invalid, boundary-length, Unicode, and whitespace input; verify errors preserve correct data and recovery works. |
| Lists and workflow state | Empty and populated lists, enough items to exercise pagination, records in relevant lifecycle states. |
| External services | Sandbox integrations, controlled failure fixture, test inbox/webhook sink; distinguish simulated outages from actual observations. |
| Payments and blockchain | Test provider or testnet, disposable wallets, funded/insufficient-funds states, rejection and pending/failure cases; no real spending implied. |
| Files and timing | Allowed and rejected file cases, controlled slow/failure state where supported, double-submit and interrupted navigation. |

Generate unique fixture identifiers per run. Provide a safe account access mechanism separately from the packet. Record roles and account aliases in evidence, not credentials. Separate accounts or namespaces for cases that mutate the same records. Reset between destructive cases, verify the reset, and preserve evidence before cleanup. Cleanup must be scoped to created fixtures and must not delete the failure evidence.

## Declared checks and exploratory charters

Map each requirement to starting state, user goal, expected observable outcome, and evidence. Include the main journey and relevant validation/recovery, empty/loading/error, role boundaries, refresh/persistence, responsive, and keyboard paths. Supply checks for side effects that screenshots cannot establish, such as saved records or webhook delivery.

Give Rakazo bounded charters chosen from actual risks. For example, "Spend ten minutes varying navigation and refresh during checkout in the sandbox; look for duplicate orders and lost state." Specify scope, budget, allowed mutations, observations to collect, and forbidden side effects. Ask it to vary order of actions, input, session state, viewport, and recovery paths where relevant. Record variants actually attempted and untouched areas. Do not promise greater coverage solely because the bot controls a computer.

Use a preflight phase, declared checks, targeted exploration, and reporting phase. Choose budgets from the project's configured timeout. Stop on wrong candidate, cross-tenant exposure, environment contamination, or an action beyond authorized scope; preserve the observation and report the block. Product bugs within scope should be documented and testing may continue in unaffected cases.

## Bounded behavioral stress

Choose relevant stress cases based on the changed flow and likely failure modes. Specify attempts or duration and the outcome invariant for each case. Use reproducible input sets or record generated inputs. Increase variation after the baseline journey works; distinguish a baseline failure from one introduced by stress.

| Exercise | Invariant and evidence |
| --- | --- |
| Repeated clicks, retries, and repeated workflow cycles | No duplicate side effects or corrupted records; record attempts and resulting record identifiers/counts. |
| Back/forward, refresh, tab close/reopen during a mutation | Committed state survives; unfinished work recovers according to the product contract. |
| Two tabs or two test sessions updating the same record | Permissions and conflict handling remain correct; record action order and final state. Only use supported session isolation. |
| Long, Unicode, pasted, malformed, and boundary inputs | Validation handles actual inputs and the UI remains usable; preserve the exact reproducing input. |
| Session expiration and role changes mid-flow | The app stops unauthorized work and gives a usable recovery path without leaking another user's data. |
| Controlled network interruption or slow response | Recovery does not duplicate operations or silently lose committed work; record how the interruption was induced. |
| Repeated navigation with populated fixtures | State and responsiveness remain usable across the declared cycles; report measured timings only when captured. |

Set maximum records, actions, parallel sessions, and duration appropriate to the QA environment. Use controlled sandbox failures where available. Do not claim to have exercised an outage, race, or volume that the available tools could not produce. Run a bounded pilot before extending expensive cycles, stop for contamination or scope violations, and preserve failed state before reset. Every stress result reports planned and completed attempts, observed invariant, failures, and unexplored variants.

After evidence collection, clean only the run's fixtures according to the agreed retention policy. Record cleanup completion or retained fixtures needed for diagnosis. Retests use fresh fixtures and the new candidate while preserving the original failing sequence.

## Upstream context

[Rakazo's upstream repository](https://github.com/elie222/rakazo) documents persistent bots, browser/terminal/file access, and both shared Team Computers and isolated Private computers. Verify the user's deployed version and actual available UI rather than assuming main-branch behavior. This skill uses its browser interface and does not define an unverified Rakazo API contract.
