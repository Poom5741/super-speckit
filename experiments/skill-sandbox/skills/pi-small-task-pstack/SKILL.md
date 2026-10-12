---
name: pi-small-task-pstack
description: Implement or repair a small local CLI feature with direct behavioral verification, within the user's time budget.
---

# Small task, direct verification

Inspect the existing code and commands. Reuse their structure and installed dependencies. Make the smallest implementation that satisfies the request.

If fixing a bug, reproduce it first and fix the cause rather than hiding the symptom. Check for the same pattern at other relevant call sites.

Call the CLI as its user would. Assert literal expected outputs and actual file effects, rather than internal calls or successful compilation. Script repeatable checks when practical, execute them, and retain their output for review.

Before declaring completion, check the real final artifact. Report what you observed and what remains unverified. Keep the verification proportional to this small task.
