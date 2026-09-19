# Debugging skill landscape

Researched 2026-09-19 against upstream source repositories. The goal is a single, clear general debugging authority plus a browser-runtime complement—not several competing “debug everything” skills.

| Candidate | Fit | License / pin checked | Decision |
| --- | --- | --- | --- |
| [Matt Pocock `diagnosing-bugs`](https://github.com/mattpocock/skills/tree/74ca5fe077456a0b3b2f5310cf9430999fd0b5fd/skills/engineering/diagnosing-bugs) | Requires a tight red-capable loop before a theory; supports tests, HTTP, Playwright, trace replay, harnesses, fuzzing, bisection, differential runs, and human-in-the-loop; requires minimisation, ranked falsifiable hypotheses, regression proof, and cleanup. | Already pinned in `sources.lock.json`; consult upstream notices before redistribution. | **Primary, already included.** |
| [Superpowers `systematic-debugging`](https://github.com/obra/superpowers/tree/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/systematic-debugging) | Excellent four-phase root-cause-first rule, data-flow tracing, condition-based waiting, and architectural stop after repeated failed fixes. | MIT; commit `5bf4e78011075bcfc0dc295f0724994cd123ee71`. | **Do not duplicate.** Matt covers its general role and adds stronger reproduction/replay options. It remains a useful reference. |
| [OpenAI `frontend-testing-debugging`](https://github.com/openai/plugins/tree/1dc195897af4161d039b80d8471ec0a10c9bbc89/plugins/build-web-apps/skills/frontend-testing-debugging) | Concrete rendered-app loop: target flow, nonblank/overlay checks, console health, screenshots, interaction proof, responsive checks, and rerun after edits. | OpenAI repo commit `1dc195897af4161d039b80d8471ec0a10c9bbc89`; GitHub reports no repository license. | **Optional external integration, not vendored.** Use when its plugin is installed; otherwise capture equivalent Playwright evidence. |
| [agulli `local-replay`](https://github.com/agulli/skills-evolve/tree/f90ec246566059573da8388fc8fe8c952b3b6deb/skills/dev/local-replay) | Replays a captured single agent/LLM trajectory using pinned config and tool stubs, then promotes the case to an eval regression. | MIT; commit `f90ec246566059573da8388fc8fe8c952b3b6deb`. | Optional future add-on only for agent-product failures; not needed for ordinary code or web-app defects. |
| [Waza `hunt`](https://github.com/tw93/Waza/tree/2cb5d0c6cc69333c1575cd72f2585f1c7eb0d703/skills/hunt) | Git-bisect and visual-regression investigation. | MIT; commit `2cb5d0c6cc69333c1575cd72f2585f1c7eb0d703`. | Do not add; its bisection role overlaps Matt and its workflow is too prescriptive for this kit. |

## Routing adopted by Super-SpecKit

| Failure shape | First diagnosis method | Required outcome before fix lane |
| --- | --- | --- |
| Unit, integration, API, DB, build, CI, or performance failure | Matt `diagnosing-bugs` | A red-capable reproducer, evidence-backed cause, and correct regression-test seam (or recorded exception). |
| Rendered web-app interaction, visual state, browser console, or network failure | Matt `diagnosing-bugs` plus the OpenAI browser workflow if that plugin is installed; otherwise Playwright | Target-flow evidence plus screenshot/trace and console/network receipt, then the same root-cause/reproducer obligation. |
| Flake | Matt loop with elevated reproduction rate, deterministic controls, and attempt count | Classified reproducibility and preserved evidence before durable bug filing. |
| Old-good/new-bad regression | Matt bisection harness | A candidate commit range and reproducible verdict. |
| Agent/LLM run with an available trace | Optional `local-replay` if installed | Replay fixture and an evaluation regression. |

The orchestrator uses `super-speckit.diagnose` before a repair worktree. Diagnosis itself does not authorize a modification in QA; confirmed fixes still enter an isolated maker worktree and a clean independent retest.
