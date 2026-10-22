# One Super-SpecKit pipeline

For every new delivery, `create-feature` defaults to `pipeline_contract=unified-v1`
and the existing knowledge-v2 delivery contract. Old records retain their original
gates. `--pipeline legacy` exists for explicit compatibility fixtures/imports; do
not select it to bypass missing personas, convergence or verification.

```text
purpose → investigate (PStack methods + feature expertise) → scope
  ├─ micro: playbook + matrix
  └─ normal/milestone: native specify/clarify → plan → tasks
→ select feature-specific Lude maker persona + relevant specialists
→ design/architecture + public-seam baseline → implement selected tasks
→ committed candidate → independent runtime QA + engineering acceptance
→ PStack lens + Lude specialist lens → reconcile findings
→ convergence
  ├─ remaining work: append tasks → implement → NEW candidate → fresh QA/lenses
  └─ converged: exact-candidate release checks → authorized merge → handback
```

`ask-super-speckit` is the only coordinator. Native Spec Kit owns normal/milestone
intent and convergence, Lude supplies feature-specific developer expertise, PStack
supplies investigation and implementation/review methods, and Super-SpecKit owns
state, reconciliation, isolation, independent proof and release. Lude is a distinct
lens, not subordinate to PStack's stylistic preferences. Conflicts are resolved
against actual requirements and evidence, not by voting or adding both designs.

## Native Spec Kit execution

Use the project's installed Spec Kit integration and actual host invocation syntax.
Confirm installed specify/plan/tasks/implement/converge capabilities and relevant
hooks before promising native delivery. Read the installed commands completely;
the pinned reference in `vendor/spec-kit/templates/commands/` documents the reviewed
interface, not a second executable CLI or an automatically current installation.
Normal/milestone work retains constitution-governed spec.md, plan.md and tasks.md.
Use installed clarify/analyze/checklist when the selected scope needs them.
Unavailable native commands block normal/milestone delivery; do not relabel a
custom scan as native convergence. Upstream bug and assessment extensions can feed
diagnosis/discovery artifacts into the same pipeline when installed; they do not
start another state machine or authorize delivery by themselves.

After implement and independent candidate QA/lenses, run native converge against
the feature artifacts and current implementation. Preserve its intent authority,
buildable scope and append-only behavior. It assesses all existing tasks regardless
of checkbox state. Never rewrite spec/plan or existing tasks to make code pass.
If gaps remain, native converge appends traceable tasks with new IDs and reports
`tasks_appended`. Preserve the old intent and update the phase-contract receipt
before implementing the appended tasks. Repeat within the existing run budget.
A failed hook, unknown prerequisite or exhausted budget remains blocked/unverified.

Micro uses a scoped compact completion assessment of playbook.md and every matrix
requirement. Record mode `compact`; never claim native Spec Kit convergence for
this route. Escalate to native planning when unresolved consequential scope or
cross-boundary design appears. Compact remaining work stays in the same playbook.

Convergence is before merge. Every changed candidate invalidates prior proof and
requires fresh runtime QA, both lenses and convergence. Pure evidence records live
outside tracked candidate intent. Never change candidate code during convergence.

## Commands and receipt shapes

Paths below are target-project relative; invoke scripts from the installed kit.

```bash
python3 scripts/lude_adapter.py inventory
python3 scripts/lude_adapter.py catalog
python3 scripts/lude_adapter.py read golang-expert
python3 scripts/super_speckit.py select-personas F --repo . \
  --persona senior-backend-engineer --specialist golang-expert \
  --rationale "Go export endpoint uses the existing service boundary"
python3 scripts/super_speckit.py record-prerequisite F lens-review --artifact evidence/lenses-1.json
python3 scripts/super_speckit.py record-convergence F --receipt evidence/convergence-1.json
```

`select-personas` writes a digest-bound canonical selection; it does not execute
the selected skills. Read and apply their source, document relevant decisions,
and retain observed results. Paths must name real nonempty repository files.

The independent lens receipt shape is:

```json
{
  "candidate_sha": "<full SHA>", "checker": "<independent checker identity>",
  "status": "passed", "personas_digest": "<selection artifact SHA-256>",
  "lenses": [
    {"id":"pstack", "summary":"<scoped assessment>", "findings":[],
     "evidence":[{"path":"evidence/pstack-1.md","digest":"<SHA-256>"}]},
    {"id":"lude-kit", "summary":"<selected specialist assessment>", "findings":[],
     "evidence":[{"path":"evidence/lude-1.md","digest":"<SHA-256>"}]}
  ],
  "reconciliation":"<agreements, disagreements and their evidence-based resolution>"
}
```

Each finding contains `disposition` (`fixed`, `accepted-risk`, `dismissed`), `reason`
and digest-bound `evidence`. Fixed findings describe a fix already in this candidate,
not a promise to edit it after review.

A convergence receipt contains `candidate_sha`, `checker`, `mode` (`native` or
`compact`), `outcome` (`converged` or `tasks_appended`), `remaining` (empty only for
converged), observed host `invocation`, `summary` and digest-bound `evidence` rows.
Its `intent` maps project-relative matrix and planning artifact paths to their
SHA-256 digests, including `.specify/memory/constitution.md` when present. Native
mode adds `tasks_before_digest` and `tasks_after_digest`: they are identical on
`converged`; on `tasks_appended` the old candidate tasks must be an unchanged prefix
of the new tasks. Use a distinct immutable receipt/evidence path for every run.

`record-convergence` requires existing independent proof. Remaining work reopens
`maker_running` and removes current proof, QA attempt, lens review, engineering
review, shared result and convergence acceptance; archived run history is retained.
A new candidate commit is required. `ready_for_merge` rejects missing/stale
personas, either missing lens, unfinished convergence, changed intent or a report
for a different candidate/checker. `next-stage` exposes personas/lens-review/
convergence/release as appropriate. These are accountable evidence receipts,
not proof of unseen model reasoning or a guarantee of defect-free software.

Sources and license notices are pinned in `sources.lock.json` and the two new
vendor manifests. The installer checks all source bytes before installation.
Inventory coverage does not imply live certification of every specialist or host.
