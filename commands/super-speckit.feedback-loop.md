---
description: Find, run, and record the smallest real feedback loop for any proposed change before implementation begins.
---

Read the relevant Context Cards, Atlas nodes, specification, and verification matrix. Before planning implementation detail or editing production code, create `.super-speckit/feedback/<feature-or-bug>/feedback-loop.md` from `templates/feedback-loop.md`.

Choose the cheapest loop that can observe the intended behavior at a public seam. Search available project tools and evidence sources before declaring that no loop exists: existing tests, API/CLI commands, local runtime, Playwright/browser tooling, screenshots/visual diffs, API/DB assertions, traces, event payload replay, simulators, fixtures, property/fuzz harnesses, benchmark/profiler output, git-bisect/differential runs, and bounded human observation.

Run the baseline once and retain only safe, redacted evidence. State the assertion that would be red before the change or that will distinguish correct from incorrect behavior afterward. Make the loop fast and deterministic where practical. A green build, static review, or source inspection alone is not a feedback loop.

If no loop is available, keep searching for a narrower seam or create a throwaway harness. Only record `blocked` after documenting attempts, required missing access, and the next automatic probe. Do not implement against a guessed loop.

For substantive performance comparisons use equivalent competitor tuning, actual completed work/error counts, a measured limiter and at least five alternating samples per side. Rejected/no-op operations cannot count as completed work or a performance win. For hillclimbing change one hypothesis per trial, retain unsuccessful evidence and revert rejected candidates.
