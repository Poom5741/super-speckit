---
name: super-speckit
description: Run Spec Kit features through isolated maker worktrees and independent evidence-based QA, including runtime Playwright verification, OCR triage, and confirmed-bug retest loops.
---

# super-speckit

Use this skill after native Spec Kit has a feature specification, plan, and task list, or when an existing feature/bug needs an independent verification loop. Do not use it to replace ordinary planning or to claim that static review proves a running app works.

Read `docs/orchestration.md` before coordinating a feature. Read `schemas/README.md` before creating or changing tracked artifacts. Use the command file matching the requested action.

## Non-negotiable separation

Maker and checker must be different agents or independently scoped runs. The checker receives a committed SHA in a clean QA worktree, not a mutable maker directory. Checker changes are limited to QA evidence and bug artifacts. Never merge automatically.

## Entry and exit criteria

Start only after `spec.md`, `plan.md`, `tasks.md`, and a requirements-to-verification matrix identify the intended scope. End with a QA summary that labels every requirement `verified`, `not-verified`, or `not-applicable`, and lists evidence paths. Missing environment access is an explicit unverified item, not a pass.

## Runtime evidence

Run configured deterministic checks first, then start the actual app from the QA worktree and run Playwright. Include API or database assertions when a browser observation alone cannot demonstrate persistence, authorization, or integration side effects. Run bounded exploratory cases separately; record tested paths and observations. Capture only non-sensitive traces, screenshots, videos, and logs.

## Failure handling

Classify initial failure as deterministic, environment, test defect, or suspected flake. Apply the configured reproduction count before creating a confirmed bug artifact, except for a deterministic failure with preserved evidence. Confirmed bugs get a dedicated worktree, a regression test or documented exception, and an independent retest. OCR is triaged independently and cannot close matrix rows.
