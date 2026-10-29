---
name: super-speckit-installer
description: Install the complete Super-SpecKit evidence-first autonomous delivery kit into a software project.
---

# Install Super-SpecKit

Use this skill when a project needs the complete Super-SpecKit workflow rather than a single standalone instruction file.

Run `scripts/install_project.py --target <project-root>`. It downloads the public Super-SpecKit bundle, installs it to `<project-root>/.super-speckit/`, creates `<project-root>/super-speckit.yml` when absent, initializes the real YAML work-state manifest, and registers exactly four discoverable entry points—`$super-speckit`, `$ask-super-speckit`, `$super-speckit-design-first`, and `$super-speckit-final-manual-review`. The default `--entrypoint-scope both` exposes them in every supported project-local harness root and in the native user-level roots for Agent Skills, Codex, Claude Code, Cursor, OpenCode, Pi, and ZCode. The user-level wrappers are project-independent: they locate the nearest active project containing `.super-speckit/`. It also registers the prebuilt provider-neutral V2 server/TUI/RPC plugin under `.opencode/plugins/super-speckit/`; the plugin reads its daemon token from user state and never commits it to the repository.

Identical installs are idempotent and preserve project configuration and runtime evidence. Use `--entrypoint-scope project` when user-level registration is intentionally unwanted, or `global` to repair only user-level discovery. Existing unrelated user skills are never silently overwritten: conflicts are reported and skipped; reviewed `--force` replacement retains a backup. Project-local conflicts still stop installation. Use `--upgrade` for a deliberate bundle revision change. Vendor PStack remains outside discovery, including dormant Benny workflows. If an older installation exposes only `$super-speckit-installer` or is missing wrappers for one harness, run `scripts/install_project.py --target <project-root> --register-only`; its default `both` scope repairs project and user discovery. Internal roles such as the skill evaluator remain inside the installed kit and are selected by `$ask-super-speckit`; users still use one normal entry point. After installation, verify files with:

```bash
python3 .super-speckit/scripts/super_speckit.py validate --repo .
python3 .super-speckit/scripts/super_speckit.py status --repo . --strict
```

For reproducibility, pass `--ref <tag-or-commit>` instead of relying on `main`.
