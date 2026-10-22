---
description: Focused performance audit on the current repo. Measures first, finds dominant cost, proposes fixes with budgets and regression guards.
argument-hint: "[optional: path or area to focus, defaults to whole repo]"
---

# Performance audit

Target: $ARGUMENTS (defaults to the whole repo).

Run a focused performance audit. Measure first, optimize second, validate third.

## Agents to dispatch in parallel

1. `perf-investigator`, primary lead. Establish what to measure (p50, p95, p99 latency; throughput; memory; startup; bundle size; energy). Find the dominant cost. Propose the smallest change that addresses it.

2. `code-reviewer`, read the code for perf adversaries: N+1 queries, allocations in hot loops, unnecessary copies, blocking IO on hot paths, missing indexes, missing caches, missing memoization, oversized payloads.

3. The matched stack expert (detected from the repo). Use the right one:
   - `postgres-expert` for query plans, missing indexes, vacuum issues.
   - `redis-expert` for hot keys, eviction policy, persistence cost.
   - `nextjs-expert` for hydration cost, RSC vs Client, cache strategy.
   - `golang-expert`, `rust-expert`, `python-expert`, etc. for language specific perf.
   - `swift-ios-expert`, `flutter-expert`, `react-native-expert` for mobile / native frame budgets.

4. `senior-performance-engineer` skill, methodology and rigor. No optimization without measurement, pick one metric and one target, validate with a repeatable benchmark, set a budget and a regression guard.

5. `architect`, surface level: are perf problems algorithmic, architectural (e.g., chatty service boundary), or operational (e.g., wrong instance size)?

## Output format

### Baseline
What we know today (or what should be measured). If numbers are not available in the repo, list the measurements to collect and how.

### Dominant cost
The single biggest cost identified. Evidence: file:line, code snippet, query plan, estimated frequency.

### Findings ranked by impact
Each row:
- Estimated impact (large / medium / small) on the target metric.
- Cost (low / medium / high) to fix.
- Location.
- Recommended change.
- Owning subagent.

### Concrete patches
For the top three findings, propose a code sketch of the fix.

### Budget and regression guard
What to enforce in CI after the fix lands. Examples: bundle size budget per route, p95 budget per endpoint, query timeout, allocations per request.

### Things to NOT optimize
Spots that look slow but are not on the hot path; do not waste cycles there. Naming them upfront prevents drive by micro optimization.

### Next 5 commits
Ranked by metric movement.

Cite the subagent. Keep it terse.
