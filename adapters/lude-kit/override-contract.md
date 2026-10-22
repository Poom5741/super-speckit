# Lude specialist lens inside Super-SpecKit

Read this contract with the selected pinned skill. Super-SpecKit owns the pipeline,
canonical state, task list, candidate, QA and release authority. Lude provides the
feature's developer persona, relevant stack/domain expertise, and an independent
specialist review lens. PStack provides investigation and engineering methods.
Neither upstream coordinates or approves the other.

## Choose from the feature

After investigating the real flow and selecting scope, inspect
`python3 scripts/lude_adapter.py catalog`. Choose one primary implementation
persona from `personas`, then only the relevant stack, domain and capability
specialists. Read each selected skill through `lude_adapter.py read <id>` so
this contract accompanies the original source. Base selection on the actual
feature, installed stack, risk and project conventions, not all keyword matches.
For example, a Go refund endpoint may use senior-backend-engineer,
golang-expert and fintech-engineer; a dashboard may use senior-frontend-engineer
and its actual framework specialist. A documentation or infrastructure task uses
the corresponding owner persona. Do not invent missing blockchain or other roles.

Use `select-personas <feature> --persona <id> --specialist <id> ... --rationale
"<feature-specific reason>"` to bind selection to the maker, scope, current intent
and pinned source. The selected personas guide one maker; personas do not imply
multiple agents. Re-select when intent, scope, stack or primary owner changes.
For dependent slices one owner changes persona as appropriate; independent writers
still need explicit isolation. A handoff suggestion is a routing suggestion, not
permission to message, install, dispatch, modify external systems or change models.

## Apply expertise without competing process

Preserve concrete domain checks and applicable source steps. Reconcile conflicting
advice in the existing plan/playbook with evidence. User requirements, actual
project conventions, native Spec Kit intent and Super-SpecKit safety/evidence
contracts govern. Lude's generic defaults do not replace an established layout,
framework, API convention, supported runtime or architecture. Its example versions
and commands require current primary documentation and local validation.

Only produce artifacts needed for the selected scope. Map a Lude PRD into native
spec.md, architecture into plan.md, work into tasks.md, and verification into the
existing matrix/proof pack; compact work stays in playbook.md. A contract, migration
runbook or threat model is a supporting artifact when the feature needs it, not a
second requirements ledger. Preserve early public-seam feedback rather than moving
all testing after implementation. Existing purpose confirmation remains valid.
Mandatory external communication and sign-off in raw skills remain subject to
actual user authorization; unavailable consumers or tools are disclosed.

The pinned subagents, commands and authoring material are retained for provenance
and useful role guidance. Their dispatch, tool/model pins, global installers,
orchestrators and additional command hierarchy are inactive. The complete skill
catalog is available on demand, never loaded wholesale or registered globally.

## Two distinct review lenses

An independent checker assesses the same immutable candidate with:

- PStack: callers, boundaries, ownership, root causes, simplicity and operational
  evidence using the selected method.
- Lude: the selected persona's domain/stack correctness, failure modes and quality
  criteria using the feature brief and actual code.

Keep summaries, findings and evidence for each lens separately. The coordinator
reconciles disagreements in one `lens-review` receipt, preserving minority findings
and giving each a fixed/accepted-risk/dismissed disposition with reason and evidence.
Unresolved findings do not pass. An accepted risk follows existing project authority.
Different lenses may use the same independent checker; they are not claims of
different models or independent human agreement. Makers cannot grade their own code.
Neither static lens satisfies runtime proof. Any fix produces a new candidate and
fresh independent QA, lens review and convergence.
