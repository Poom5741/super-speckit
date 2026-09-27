---
name: super-speckit-installer
description: Install the complete Super-SpecKit evidence-first autonomous delivery kit into a software project.
---

# Install Super-SpecKit

Use this skill when a project needs the complete Super-SpecKit workflow rather than a single standalone instruction file.

Run `scripts/install_project.py --target <project-root>`. It downloads the public Super-SpecKit bundle, installs it to `<project-root>/.super-speckit/`, creates `<project-root>/super-speckit.yml` when absent, and initializes the real YAML work-state manifest.

The installer refuses to overwrite an existing `.super-speckit` directory unless `--force` is explicitly supplied. After installation, use the installed `$super-speckit` skill from `.super-speckit/SKILL.md` and verify files with:

```bash
python3 .super-speckit/scripts/super_speckit.py validate --repo .
python3 .super-speckit/scripts/super_speckit.py status --repo . --strict
```

For reproducibility, pass `--ref <tag-or-commit>` instead of relying on `main`.
