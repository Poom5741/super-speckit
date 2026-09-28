---
description: Run an evidence-backed adversarial Builder/Examiner/Investigator/Resolver grill after purpose confirmation and before implementation.
---

Use the pinned upstream Matt `grill-with-docs` and `domain-modeling` capabilities where useful, but preserve this output contract. Create `.super-speckit/grills/<feature>/spec-grill.md` from `templates/spec-grill.md` after the Purpose Gate and native specify/clarify artifacts exist.

Use distinct roles or independent runs:

1. **Builder** proposes the smallest coherent reading of the confirmed purpose.
2. **Examiner** adversarially challenges requirements and failure modes.
3. **Investigator** verifies material answers against repository evidence.
4. **Resolver** records each answer as `proven`, `inferred`, `assumed`, or `unknown`, then updates spec, matrix, plan, or tasks.

Self-answering is allowed; unsupported agreement is not. A `proven` answer must link evidence. An `inferred` or `assumed` answer must add a verification or reversal path. Only a finding that changes purpose, affected people, success signal, or non-goals returns to `super-speckit.purpose-gate`; ordinary technical decisions are resolved autonomously. After a ready result, record it with `python3 scripts/super_speckit.py record-grill <feature> --artifact .super-speckit/grills/<feature>/spec-grill.md`.
