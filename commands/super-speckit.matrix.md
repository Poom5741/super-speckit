---
description: Map Spec Kit requirements to independent verification before implementation.
---

Read the feature's spec acceptance criteria and plan. Create `specs/<feature>/verification-matrix.md` from the template. Every functional requirement gets one or more observable methods: unit/integration where useful, Playwright for user behavior, and API/DB checks when persistence, identity, or external effects matter. Mark non-testable/excluded requirements explicitly with reason and approval; do not defer this work until after implementation.
