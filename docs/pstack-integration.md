# PStack methods in Super-SpecKit

PStack 0.15.13 is pinned at `e5a8186d7b43be8d6ac4452440fbead5f1a51c70`. All 164 tracked files and MIT notices remain unchanged under `vendor/pstack/`, outside discovery. The manifest accounts for every source file. The route register covers 27 workflow skills, 24 principle skills, 23 playbooks, two bounded agent roles and 12 dormant Benny files. Source inventory does not establish execution certification; see `pstack-certification.md` for observed coverage.

`ask-super-speckit` remains the single coordinator. Native Spec Kit owns requirements/plans/tasks/convergence; canonical state owns candidates/proof/authority. Read-only questions, teaching/help and investigations return cited results without creating delivery state. Delivery still requires confirmed purpose and independent exact-candidate proof. Configured merge autonomy remains authoritative.

## Load a method progressively

```sh
python3 scripts/pstack_adapter.py --kit . verify-source
python3 scripts/pstack_adapter.py --kit . inventory
python3 scripts/pstack_adapter.py --kit . route architect --group skills
python3 scripts/pstack_adapter.py --kit . read architect --group skills
python3 scripts/pstack_adapter.py --kit . read feature --group playbooks
```

Read returns pinned source together with the active override contract. Record selected source steps, completed evidence and explicit skip reasons in native artifacts. All 24 principles have concrete applicability triggers and expected observable results in `adapters/pstack/routes.json`; apply them only when relevant. Installation/upgrade preserves user configuration and evidence and detects source drift; upgrades are deliberate revision changes.

## Executable interfaces

`python3 scripts/pstack_runtime.py <operation> --input request.json` consumes JSON and emits JSON receipts. It never grants delivery authority. Operations are `panel`, `review-panel`, `arena`, `freeze`, `judge`, `swarm`, `decision`, `benchmark`, `verify`, `watcher`, `normalize-event`, `claim-event`, `reconcile-writes`, and `audit`. Inputs are the named function keyword arguments; implementations also provide importable stdlib Python functions:

| Method | Inputs and observable contract |
|---|---|
| `panel` | `intent`, `diff`, `rubric`, `sha`, actual distinct `models`; identical rendered prompt/hash per model. |
| `review_panel` | seats, returned receipts and all-finding dispositions; dropout/input drift/missing lone-finding disposition fails. |
| `arena_brief`, `freeze_candidate`, `judge` | identical briefs/base, retained frozen artifact hashes and separate private rubric; modified outputs fail judging. Keep rubric physically outside candidate access. |
| `Swarm`, `swarm_operation` | required units/dependencies/base, declared mode/selection and concurrency; rolling dispatch and attempt/SHA/evidence-bound completion, no coverage loss on dropout. |
| `verify` | `recipe`, `cwd`, `output`; explicit argv controls, live feature driving, cleanup and retained-artifact receipts. Missing/failed controls return `draft`. Passing control commands without an independent observed seam return `controls-passed` with CLI exit 1. `verified` requires a runner-observed HTTP `probe` bound to instance/build/health and per-feature `observations` asserting expected persisted fields plus changed fields (or explicitly read-only behavior). |
| `benchmark` | samples, equivalent tuning and measured limiter; at least five alternating samples per side with completed work/errors. |
| `append_decision`, `audit_decisions` | run-bound append-only claims/evidence/correction target and available transcript; unsupported claims remain findings. |
| `watcher` | structured watcher payload; readiness, ledger hit, behavioral verification and observed merge are distinct fields. |
| `normalize_event`, `claim_event`, `reconcile_writes` | immutable source coordinates, trusted triage/human ownership, durable deduplication and external-write compensation receipts. `event-receipt` durably records each external write result, rejects conflicting retries, and reports required compensation. No external messages are sent by these helpers. |

Swarm JSON is `{ "path": "scheduler.json", "operation": "init|dispatch|complete|retry|status", "data": {} }`; initialization data contains units (`id`, `base`, optional `depends`/`required`), optional limit/mode/selection. Completion data contains unit/attempt/sha/evidence/passed. Verification JSON contains recipe/cwd/output; recipe supplies build_id, declared features, per-feature drive argv and launch/doctor/evidence/cleanup argv. Controls receive PSTACK_INSTANCE/PSTACK_BUILD_ID/PSTACK_EVIDENCE; doctor must emit matching JSON instance/build_id and healthy true. Every feature is driven and retained artifacts must survive cleanup; draft verification exits one.

Use actual input contracts from the script/help rather than guessing invocation flags. Arena/swarm/learning/automation helpers are evidence primitives, not a provider orchestration service. Host dispatch must still execute and return real receipts; source-step completion cannot be inferred from helper availability.

## Host boundaries and continuation

`python3 scripts/pstack_host.py doctor --input hosts.json` takes a mapping keyed by `zcode`, `codex`, `pi`, optional `omp` and `cursor`. A configured host entry contains explicit reviewed `argv`, declared `isolation: git-worktree`, and optional `model` and process-only `env` provider-path overrides. Only the two installed ZCode provider configuration path variables are accepted; contents and credentials are not printed. Argv placeholders are `{brief}`, `{worktree}` and `{model}`; no shell string or inferred host flags. Doctor reports executable/configuration/isolation and leaves live certification unverified.

`plan --input request.json` takes `config`, `host`, a nonempty immutable `brief`, a clean linked `worktree`, and optional `model`, `role`, `allowed_writes`, `stop_condition`, `attempt`. It returns the exact base, brief hash and dispatch argv. `dispatch --input request.json` takes that result under `request` and optional bounded `timeout`; it rejects changed brief/base/worktree and returns observed process outcome. Completion audits the declared allowed write scope. The host worker must obey its immutable role/write contract; these declared limits are not an OS security sandbox.

ZCode is primary. Configure only supported Codex/Pi CLI controls; OMP/Cursor remain detected extras. Missing controls use separately scoped sequential workers with truthful independence limitations. Resume validates real Git/state and evidence before work; do not duplicate completed work or claim model diversity from different personas. No global host configuration is overwritten; discovery checks detect user-level skill shadowing.

## Fidelity and limits

The override contract preserves upstream methods while replacing incompatible operational assumptions: one coordinator, adaptive configured concurrency, inherited/supported models, cloud opt-in, native Git/forge, configured merge authority, selective comment edits, exact-SHA proof and dormant external automation. Upstream scripts/tests remain provenance and may need Bun; importing a source tool is not approval to install packages.

Benny and make-bot-ui require explicit configuration and external-action authority. Coordinate normalized source events, trusted triage, reproduction before fix, existing-fix verification, human ownership, two baseline/two patched runs, coordinator-only posting, write receipts and compensation. Authentication, server-side secrets, isolated artifacts and idempotency remain required. This release supplies contracts/helpers; it does not silently activate a hosted bot or contact external services.

Runtime fixture tests prove their declared seams. Real browser/product runs, actual ZCode/Codex/Pi dispatch and live GitHub merge must be separately observed. Never present route completeness, copied files, or prompt-string checks as those capabilities.

## Installed project paths and migration

Inside an installed project use `python3 .super-speckit/scripts/pstack_adapter.py ...` (kit defaults to its installation) and `python3 .super-speckit/scripts/super_speckit.py ... --repo .`. References in pinned leaf instructions resolve relative to their `vendor/pstack` source directory; the active override contract always accompanies them. No global user skill is overwritten. If ZCode reports user-scope shadowing, invoke/read the project canonical entry explicitly until the user chooses a global update.

Existing v1 state requires explicit `migrate-state`; historical delivery claims become blocked for revalidation with preserved migration backups. Incoming checker proof includes candidate/checker/worktree/attempt, environment path, immutable matrix/evidence digests, exact requirement IDs with runtime/public-behavior seams, and configured passing command receipts. `record-proof` binds the environment digest before persistence. These are trusted independent-checker attestations, not cryptographic proof that arbitrary reported commands ran.

Native commands remain public compatibility facades. Source/route coverage includes raw scripts, guides and assets through the manifest; only runtime methods and hosts listed in the certification report have observed execution coverage. Optional live forge, bot, browser and model-diverse flows remain capability gated.
