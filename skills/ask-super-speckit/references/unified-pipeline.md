# One Super-SpecKit pipeline

For every new delivery, `create-feature` defaults to `pipeline_contract=unified-v1`,
`delivery_contract=knowledge-v2` and `gates_contract=discipline-v1`. Old records
retain their original gates. `--pipeline legacy` and `--gates legacy` exist for
explicit compatibility fixtures/imports; do not select them to bypass missing
personas, convergence, verification, the goldfish review or the learning
checkpoint.

```text
purpose → learning-checkpoint (VibeWise) → investigate (PStack methods + feature expertise) → scope
  ├─ micro: playbook + matrix
  └─ normal/milestone: native specify/clarify → plan → tasks
→ goldfish-review (fresh zero-context reviewers of the frozen design intent)
→ select feature-specific Lude maker persona + relevant specialists
→ design/architecture + public-seam baseline → implement selected tasks
→ committed candidate → independent runtime QA + engineering acceptance
→ PStack lens + Lude specialist lens → reconcile findings
→ convergence
  ├─ remaining work: append tasks → implement → NEW candidate → fresh QA/lenses
  └─ converged: exact-candidate release checks → authorized merge → handback
```

## Discipline gates (code-enforced in every harness)

`scripts/discipline_contract.py` blocks `maker_running`, new candidates and
release for `discipline-v1` records until both receipts exist and stay
digest-fresh. This is true for a scripted harness that only runs the Python
CLI: the checks live in the state contract, not in skill prose.

**Learning checkpoint (pinned vibe-wise `learn` method).** The human reasons
through `approach` and `design`, and explicitly authorizes implementation;
guidance is feedback and concept explanations, not agent-led design. Receipt:

```json
{
  "status": "engaged", "level": "intermediate",
  "purpose_digest": "<SHA-256 of the confirmed purpose decision.json>",
  "vibe": {"skill": "learn", "source_revision": "<pinned>", "skill_digest": "<SHA-256>"},
  "checkpoints": [
    {"topic": "approach", "human": "<human identity>", "ts": "<RFC3339>",
     "summary": "<the human's own reasoning>", "agent_role": "feedback and concept explanations only"},
    {"topic": "design", "human": "<human identity>", "ts": "<RFC3339>",
     "summary": "<the human's design decisions>", "agent_role": "feedback and concept explanations only"}
  ],
  "authorization": {"human": "<human identity>", "ts": "<RFC3339>", "scope": "<authorized implementation>"},
  "evidence": [{"path": "...", "digest": "<SHA-256>"}]
}
```

`status: "human-declined"` is valid only when `declined_by` equals the
purpose-gate confirmer and a reason is recorded; maker/checker agent identities
are never accepted as the human.

**Goldfish review (pinned `egm-review` protocol).** At least
`discipline_gates.goldfish_min_reviewers` (default 2) fresh reviewers see only
the design beside the matrix plus source references in fresh contexts. Use
`spec.md` for normal/milestone and `playbook.md` for micro. Older micro
layouts may use `spec.md`. The receipt uses the repository-relative path.

```json
{
  "status": "passed", "mode": "goldfish",
  "reviewed": {"path": "specs/001-export/spec.md", "digest": "<SHA-256 of reviewed design>"},
  "harness_subagents": true,
  "reviewers": [
    {"id": "goldfish-1", "dispatch": "subagent", "fresh_context": true},
    {"id": "goldfish-2", "dispatch": "subagent", "fresh_context": true}
  ],
  "egm": {"skill": "egm-review", "source_revision": "<pinned>", "skill_digest": "<SHA-256>"},
  "findings": [{"summary": "...", "disposition": "fixed", "reason": "...",
                "evidence": [{"path": "...", "digest": "<SHA-256>"}]}],
  "resolution": "<how findings were settled>",
  "evidence": [{"path": "...", "digest": "<SHA-256>"}]
}
```

**Subagent enforcement.** `harness_subagents: true` requires every reviewer to
declare `dispatch: "subagent"` and `fresh_context: true`. The validator checks
these declarations. Use fresh contexts for actual dispatch and retain the
reports as evidence. Without subagent capability, a disclosed `sequential-fresh`
fallback is mode `goldfish-equivalent` with digest-bound `capability_absence`
evidence, accepted only while `discipline_gates.allow_sequential_fresh_fallback`
is true (set it false to make subagents a hard requirement). Findings use the
lens-finding discipline (`fixed`/`accepted-risk`/`dismissed` with reasons).
Intent changed after review stales the digest and requires a fresh review;
resolve findings before persona selection or re-select personas afterward.

```bash
python3 scripts/egm_adapter.py inventory && python3 scripts/egm_adapter.py read egm-review
python3 scripts/vibe_wise_adapter.py inventory && python3 scripts/vibe_wise_adapter.py read learn
python3 scripts/super_speckit.py record-prerequisite F learning-checkpoint --artifact evidence/learn-1.json
python3 scripts/super_speckit.py record-prerequisite F goldfish-review --artifact evidence/goldfish-1.json
```

`next-stage` exposes `learning-checkpoint` and `goldfish-review` as stages.
Both sources are pinned in `sources.lock.json` and the vendor manifests with
SHA-256 inventories; the adapter catalogs cross-check them on every load.

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
