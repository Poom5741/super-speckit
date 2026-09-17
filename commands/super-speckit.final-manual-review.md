---
description: Run a step-by-step human final review and report every observed result to ask-super-speckit.
---

Use `super-speckit-final-manual-review`. Confirm candidate SHA, QA environment receipt, reviewer identity, and matrix scope. Offer one test step at a time and wait for the human’s observation. Append the exact observed outcome and safe evidence path to `manual-review-log.md`, then report the receipt to `ask-super-speckit`.

On a confirmed failure, preserve evidence and create/route a persistent bug artifact to `super-speckit.fix`; the fixer works only in a new bug worktree. After a committed candidate, launch an independent clean QA retest and resume the manual review at the affected path. On an unrecoverable environment/access dependency, record `blocked` and wait. Do not continue dependent test steps, silently retry forever, alter production code, or declare release readiness.
