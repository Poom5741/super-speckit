---
name: super-speckit-installer
description: Install the complete Super-SpecKit evidence-first autonomous delivery kit into a software project.
---

# Install Super-SpecKit

Use this skill when a project needs the complete Super-SpecKit workflow rather than a single standalone instruction file.

Run `scripts/install_project.py --target <project-root>`. It downloads the public Super-SpecKit bundle, installs it to `<project-root>/.super-speckit/`, creates `<project-root>/super-speckit.yml` when absent, initializes the real YAML work-state manifest, and registers exactly four discoverable project entry points in `<project-root>/.agents/skills/`: `$super-speckit`, `$ask-super-speckit`, `$super-speckit-design-first`, and `$super-speckit-final-manual-review`.

The installer refuses to overwrite an existing `.super-speckit` directory or existing conflicting skill entry point unless `--force` is explicitly supplied. If an older installation has the kit but no entry points, run `scripts/install_project.py --target <project-root> --register-only`. Internal roles such as the skill evaluator remain inside the installed kit and are selected by `$ask-super-speckit`; users still use one normal entry point. After installation, verify files with:

```bash
python3 .super-speckit/scripts/super_speckit.py validate --repo .
python3 .super-speckit/scripts/super_speckit.py status --repo . --strict
```

For reproducibility, pass `--ref <tag-or-commit>` instead of relying on `main`.
