#!/usr/bin/env python3
"""Install a complete Super-SpecKit bundle without overwriting an existing project kit."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path

BUNDLE_PATHS = ("SKILL.md", "commands", "config", "docs", "schemas", "scripts", "templates", "workflows", "skills", "sources.lock.json")
ENTRYPOINTS = {
    "super-speckit": (".super-speckit/SKILL.md", "Run the complete evidence-first Super-SpecKit workflow."),
    "ask-super-speckit": (".super-speckit/skills/ask-super-speckit/SKILL.md", "Autonomously route a feature, bug, or idea through Super-SpecKit."),
    "super-speckit-design-first": (".super-speckit/skills/design-first/SKILL.md", "Create and review an HTML design decision before UI implementation."),
    "super-speckit-final-manual-review": (".super-speckit/skills/final-manual-review/SKILL.md", "Guide independent human final review and route defects safely."),
}

def register_entrypoints(target: Path, force: bool) -> None:
    """Expose the small public skill surface while keeping the full kit in .super-speckit."""
    root=target / ".agents/skills"
    for name, (canonical, description) in ENTRYPOINTS.items():
        directory=root / name; skill=directory / "SKILL.md"
        if directory.exists() and not force:
            if skill.exists() and canonical in skill.read_text():
                continue
            raise ValueError(f"refusing to overwrite existing skill entry point: {directory}; use --force only after reviewing it")
        if directory.exists(): shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)
        skill.write_text(f"""---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n\nThe canonical Super-SpecKit instructions live at `{canonical}` in this project. Read that file completely before acting, then resolve every referenced project path from the repository root. This wrapper exists only to make the installed entry point discoverable; it is not a second source of workflow truth.\n""")

def bundle_source(args: argparse.Namespace, temp: Path) -> Path:
    if args.source:
        source=Path(args.source).resolve()
        if not (source / "SKILL.md").exists():
            raise ValueError(f"not a Super-SpecKit repository: {source}")
        return source
    archive=temp / "super-speckit.zip"
    url=f"https://github.com/{args.repository}/archive/{args.ref}.zip"
    urllib.request.urlretrieve(url, archive)
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(temp / "archive")
    roots=[path for path in (temp / "archive").iterdir() if path.is_dir()]
    if len(roots) != 1 or not (roots[0] / "SKILL.md").exists():
        raise ValueError("downloaded archive does not contain one valid Super-SpecKit root")
    return roots[0]

def install(args: argparse.Namespace) -> None:
    target=Path(args.target).resolve()
    destination=target / ".super-speckit"
    if args.register_only:
        if not (destination / "SKILL.md").exists():
            raise ValueError(f"cannot register entry points: missing installed kit at {destination}")
        register_entrypoints(target, args.force)
        subprocess.run(["python3", str(destination / "scripts/super_speckit.py"), "validate", "--repo", str(target)], check=True)
        print(f"registered Super-SpecKit entry points in {target / '.agents/skills'}")
        return
    if destination.exists() and not args.force:
        raise ValueError(f"refusing to overwrite {destination}; use --force only after reviewing it")
    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="super-speckit-install-") as directory:
        source=bundle_source(args, Path(directory))
        if destination.exists():
            shutil.rmtree(destination)
        destination.mkdir()
        for item in BUNDLE_PATHS:
            origin=source / item
            if not origin.exists():
                raise ValueError(f"bundle is missing required path: {item}")
            copied=destination / item
            if origin.is_dir():
                shutil.copytree(origin, copied, ignore=shutil.ignore_patterns("__pycache__", ".super-speckit"))
            else:
                shutil.copy2(origin, copied)
    project_config=target / "super-speckit.yml"
    if not project_config.exists():
        shutil.copy2(destination / "config/super-speckit.yml", project_config)
    subprocess.run(["python3", str(destination / "scripts/super_speckit.py"), "init", "--repo", str(target)], check=True)
    subprocess.run(["python3", str(destination / "scripts/super_speckit.py"), "validate", "--repo", str(target)], check=True)
    register_entrypoints(target, args.force)
    print(f"installed Super-SpecKit to {destination}")

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--target", default=".")
    parser.add_argument("--repository", default="Poom5741/super-speckit")
    parser.add_argument("--ref", default="main")
    parser.add_argument("--source", help="local repository path; useful for offline or test installation")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--register-only", action="store_true", help="register project skill entry points for an existing kit without downloading it")
    args=parser.parse_args()
    try:
        install(args); return 0
    except Exception as error:
        print(f"error: {error}", file=__import__("sys").stderr); return 2

if __name__ == "__main__":
    raise SystemExit(main())
