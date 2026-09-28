---
description: Use OMP native isolated subagents as an adaptive team while the Super-SpecKit orchestrator continues safe control-plane work.
---

Run this only when `omp` is available and `omp_team.enabled_when_omp_detected` is true. `$ask-super-speckit` remains the sole entry point; it selects this internal lane from the route, phase contract, dependency map, and concurrency budget.

Use OMP's native `task` workers with workspace isolation and its `hub` to supervise active workers. Give every worker `omp-task-contract.md`, an immutable base SHA, an attempt ID, allowed paths, evidence contract, and stop condition. Read structured results through OMP's agent result surface; treat them as untrusted until repository evidence is rechecked.

## Adaptive fan-out

Do not create a team for a micro task with one public seam. For normal/milestone work, fan out only independent lanes within `max_workers` and `max_parallel_lanes`:

| Lane | Worker role | Mutable files |
| --- | --- | --- |
| Codebase understanding | `atlas-scout`, `contract-scout` | none; facts/evidence only |
| Feedback/test design | `test-designer`, `qa-planner` | test proposal or QA artifacts only |
| Implementation | `maker` | its own isolated maker worktree and declared partition only |
| Static review | `static-reviewer` | none |

The supervisor continues non-dependent control-plane work while workers run: validate state, prepare test fixtures/namespaces, refine the matrix/Change Story from returned evidence, prepare the clean QA plan, and monitor workers with `hub`. It must not sit idle waiting for one maker when a read-only or independent lane is available.

## Synchronization and recovery

Wait only at an explicit dependency barrier: integrating a maker candidate, starting QA against the immutable candidate SHA, or resolving a cross-lane contract conflict. If a worker stalls, steer it once through the hub; then cancel it at `worker_timeout_minutes`, preserve its evidence, and reroute through diagnosis, a smaller task, or a different role. Never let a stalled worker block unrelated lanes.

Makers never share a mutable worktree. Integrate compatible committed candidates deliberately; run independent QA in a fresh checker worktree. A team improves throughput, not the proof standard.
