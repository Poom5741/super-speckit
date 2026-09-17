---
name: super-speckit-final-manual-review
description: Guide a human step by step through final independent product review, report each result back to the orchestrator, and route confirmed failures to isolated bug-fix worktrees.
---

# Super-SpecKit final manual review

Use only after a candidate has passed its required automated gates and has a clean QA environment receipt. Read `references/review-protocol.md` and use `templates/manual-review-log.md`.

Act as a follow-along reviewer: present one concrete step at a time, wait for the reviewer’s observed result, then write it into the review log and report the structured result to `ask-super-speckit`. Do not invent observations, mark unperformed steps as passed, modify product code, or access the maker worktree.

When a step fails, preserve safe evidence and classify it. A deterministic failure may become a confirmed bug; an ambiguous failure follows the configured reproduction rule. Confirmed defects are sent to `super-speckit.fix` in a new bug worktree, then returned to a fresh QA worktree for independent retest. If the environment, access, or dependency prevents further testing, record `blocked`, state exactly what is needed, and wait—do not skip forward or convert it to pass. Continue only after the blocking condition clears or an authorized exception is recorded.

Finish by reporting verified, failed, blocked, and unverified requirements plus evidence links to `ask-super-speckit`, which may then recommend release or another repair loop.
