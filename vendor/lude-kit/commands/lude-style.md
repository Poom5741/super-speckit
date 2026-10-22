---
description: Apply Lude Kit style to the current repo. Removes em dashes and English word compound hyphens from prose, preserves identifiers and code.
argument-hint: "[optional: path to repo, defaults to current directory]"
---

# Lude Kit style sweep

Target: $ARGUMENTS (defaults to the current directory if blank).

Apply Lude Kit prose style to every Markdown and YAML file in the target. Remove em dashes (,) and remove hyphens between English words in prose. Preserve identifiers, code, URLs, file paths, license names, model names, and standard tech tokens.

## What to remove (in prose only)

- Every em dash (U+2014).
- Compound hyphens between English words:
  - `open-source` → `open source`
  - `multi-agent` → `multi agent`
  - `self-contained` → `self contained`
  - `third-party` → `third party`
  - `on-call` → `on call`
  - `real-time` → `real time`
  - `senior-grade` → `senior grade`
  - `step-by-step` → `step by step`
  - `well-known` → `well known`
  - `cross-platform` → `cross platform`
  - `first-class` → `first class`
  - `anti-patterns` → `antipatterns` (one word)
  - `trade-off` → `tradeoff` (one word)
  - `postmortem` (one word)
  - `subsystem` (one word)
  - `nontrivial` (one word)
  - And so on. Apply judgment.

## What to KEEP (preserve)

- Identifiers in backticks: `senior-frontend-engineer`, `architect`, etc.
- Code blocks (fenced ` ``` `).
- Inline code (single backticks).
- URLs.
- File paths.
- License names: `Apache-2.0`, `MIT`, `GPL-3.0`.
- Standard tech tokens: HTTP header names (`Idempotency-Key`), AWS regions (`us-east-1`), CSS (`prefers-reduced-motion`), date formats (`YYYY-MM-DD`), model names (`claude-sonnet-4-6`, `gpt-4o`, `Llama-3.1-70B`), industry standards (`LTI-1.3`, `ISO-26262`, `B-tree`), markdown table separators (`|---|---|`), CLI flags (`--dry-run`).

## How to run it

Use the Bash tool to invoke the Lude Kit dehyphen scripts that ship with this library. If not installed locally, fall back to manual edits.

If you have access to the Lude Kit repo at `~/Desktop/Builds/LudeSkills/` (or your local clone of `dimitris-di/lude-kit`):

```bash
python3 <path-to-lude-kit>/scripts/validate-skills.py  # this lints, not strips; for context
# The strip scripts at /tmp/dehyphen.py and /tmp/dehyphen2.py are session-scoped;
# author equivalents inline if needed.
```

If running standalone, write a one off Python script that walks `*.md`, `*.yml`, `*.yaml` in the target directory and:
1. Splits each file into prose vs fenced code blocks (only edit prose).
2. Replaces `, ` (em dash with surrounding spaces) with `, `.
3. Applies the compound hyphen substitutions above as word boundary regex.
4. Skips files inside `.git/`, `node_modules/`, `vendor/`, build outputs.

## Output format

### Summary
- Files scanned.
- Files changed.
- Em dashes removed.
- Compound hyphens removed.

### Sample diffs
Three before / after snippets so the reviewer can sanity check the style.

### What was preserved
A list of identifiers / tokens you intentionally left hyphenated, so the reviewer can confirm the call.

### Next step
After the sweep, run the validator if available, or grep for any remaining em dashes (`grep -rn "," --include='*.md' .`).

Cite no agent. This is a mechanical pass.
