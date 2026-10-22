---
description: Deep multi agent review of a CLI tool for UX, error handling, signal handling, distribution, and OSS readiness.
argument-hint: "[optional: path to repo, defaults to current directory]"
---

# CLI tool deep review

Target: $ARGUMENTS (defaults to the current directory if blank).

Detect the language and CLI framework first (Go cobra, Rust clap, Python click / typer, Node commander / oclif, Ruby thor, etc.). Dispatch the matching stack expert plus the generalists.

## Agents to dispatch in parallel

1. `code-reviewer` plus matched stack expert, code quality with severity labels.

2. `senior-ux-designer` skill, CLI UX heuristics: command grammar, flag conventions (POSIX vs GNU), help output quality, error messages with next steps, color and Unicode handling, terminal width awareness, tab completion availability.

3. `security-reviewer`, argument injection, environment variable handling, secret leakage in logs and error messages, file path traversal, signal handling and graceful shutdown, supply chain of self update mechanism if any.

4. `debugger`, adversarial read for crashes on weird input, edge cases (empty stdin, broken pipe, no TTY, very long lines, binary input).

5. `perf-investigator`, startup time, allocation in hot loops, streaming vs buffering for large inputs, memory cap.

6. `test-engineer`, unit tests, golden / snapshot tests for CLI output, integration tests against the real binary, exit code coverage.

7. `tech-writer`, `--help` output quality, man page or equivalent, README quickstart, examples that run, install instructions per platform.

8. `dependency-auditor`, supply chain for the build (Go modules, Cargo, npm, etc.), license obligations, binary attribution if shipping prebuilt.

9. `senior-devops-sre` skill, release pipeline (cross compile matrix, signing, distribution channels: Homebrew, Scoop, apt / yum, AUR, direct downloads, container image), reproducible builds, versioning policy.

10. `architect`, overall structure: command tree, plugin model if any, config file strategy, env var hygiene, exit code stability as part of the API.

## Output format

### Verdict
**Ship / Hold / Block** in one sentence.

### Top 5 blockers
Ranked, with severity, file:line, owning subagent, recommended action.

### CLI UX score
Quick rating on: help quality, error messages, exit code discipline, flag conventions, completion, color / Unicode, terminal awareness.

### Distribution readiness
Per channel: Homebrew formula, Scoop manifest, apt/yum, AUR, container, prebuilt binaries, install script.

### Open source readiness
LICENSE, README, SECURITY, contribution path, demo gif or asciinema link.

### Next 5 commits
Ranked by impact.

Cite the subagent that produced each finding. Keep it terse.
