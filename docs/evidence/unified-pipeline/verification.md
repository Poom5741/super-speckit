# Unified pipeline verification

Reviewed base: `9b7ccfa4148c1b5fe97a8e17de9a1822066151c7`.

## Source and authority

- Lude Kit: `b41c7a6a40c4960d687779227137b25be585ef55`; all 64 specialist skills available progressively, with commands/subagents dormant.
- Native Spec Kit reference: `27d14e20c187c1f2916540ea201ecbdc9f8ed588`; installed native integration remains the execution owner.
- PStack: existing pinned revision and adapter retained. Super-SpecKit is the only coordinator and state authority.
- Source manifests preserve upstream bytes and notices. A trailing space in the original Lude style guide is preserved intentionally; authored files pass diff whitespace checks.

## Executed checks

On WSL/Linux, from a clean source snapshot exported from the Git index with its
tracked file modes:

```text
python3 -m unittest discover -s tests -q
Ran 87 tests in 68.178s
OK (skipped=7)
```

80 passed; seven pre-existing macOS sandbox tests were skipped on Linux.
The nine new tests exercise real Git candidates, canonical CLI state changes,
feature-bound persona selection, full specialist inventory, source tampering,
independent dual-lens review, native and compact completion, stale/self-review
rejection, append-only remaining work, frozen specification intent and a complete
second-candidate QA/convergence cycle before release readiness.

Also passed: PStack inventory, Lude inventory, kit state validation, skill-creator
validation of the root and ask-super-speckit entry points, installer/reinstall/
upgrade tests in the full suite, and authored-file Git whitespace checks.

An initial run directly against the Windows checkout exposed line-ending and mode
differences in existing PStack integrity checks. Verification used a clean Linux
snapshot with original source bytes and tracked modes; this is not native Windows
certification. No PStack source hashes were changed to suppress the discrepancy.

## Independent forward-test

An isolated evaluator followed the changed skill with disposable Git fixtures:

- Go retry-safe refund: selected senior-backend-engineer, golang-expert and
  fintech-engineer, preserving the established app/billing boundary.
- React dashboard: selected senior-frontend-engineer and typescript-expert.
  An invented react-expert role was rejected because it is absent from the pinned catalog.
- Simulated unfinished native convergence accepted appended work while rejecting
  release, maker-as-checker, false convergence, rewritten existing tasks and changed
  specification intent.

The evaluator identified a sequencing gap: record-convergence checked independent
proof but did not itself require the lens receipt. This was fixed, and a regression
now verifies that convergence cannot be recorded before independent lens review.
The final full test run above includes this fix.

## Limits

Fixtures test the pipeline contracts, not a running Go/React product or a live
installed Spec Kit host. Fixture invocation receipts explicitly identify simulated
native execution. No claim is made that all 64 personas, every provider, native
Windows, actual browser journeys or production release have been certified.
Real deliveries must execute installed native commands and candidate-specific QA;
inventory and accountable receipts do not prove unseen reasoning.
