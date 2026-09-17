# Command definitions

These are portable Markdown command prompts. Map their filenames to an integration's native command convention (for example, `.codex/skills`, `.claude/commands`, or Spec Kit workflow steps).

| Command | Purpose |
| --- | --- |
| `ask-super-speckit` | Main orchestrator: inspect state, recommend the next safe stage, and coordinate only the chosen stage. |
| `super-speckit.design-first` | Create/review a static HTML design prototype before UI implementation. |
| `super-speckit.parallelize` | Produce risk/dependency-aware lane and gate plan before creating worktrees. |
| `super-speckit.phase-check` | Create a GSD-inspired, Spec-Kit-linked phase contract and plan-quality gate. |
| `super-speckit.handoff` | Persist a factual, resumable handoff when any lane pauses, fails, or completes. |
| `super-speckit.environment-ready` | Prove a clean test environment is ready before runtime QA. |
| `super-speckit.final-manual-review` | Human-led, AI-recorded final review with bug-fix/retest and wait branches. |
| `super-speckit.start` | Create a feature maker worktree and state record from native Spec Kit artifacts. |
| `super-speckit.matrix` | Create/review the requirements-to-verification matrix. |
| `super-speckit.verify` | Create a clean QA worktree and execute independent verification. |
| `super-speckit.explore` | Run bounded browser exploration and record observed coverage. |
| `super-speckit.ocr` | Run/ingest OCR static review and triage findings. |
| `super-speckit.file-bug` | Reproduce, classify, and persist a confirmed QA failure. |
| `super-speckit.fix` | Create a bug-fix worktree and require regression coverage. |
| `super-speckit.retest` | Independently retest a candidate bug fix. |
| `super-speckit.release` | Generate merge-readiness and project QA summary. |
