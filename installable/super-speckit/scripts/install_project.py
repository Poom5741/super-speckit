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
    print(f"installed Super-SpecKit to {destination}")

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--target", default=".")
    parser.add_argument("--repository", default="Poom5741/super-speckit")
    parser.add_argument("--ref", default="main")
    parser.add_argument("--source", help="local repository path; useful for offline or test installation")
    parser.add_argument("--force", action="store_true")
    args=parser.parse_args()
    try:
        install(args); return 0
    except Exception as error:
        print(f"error: {error}", file=__import__("sys").stderr); return 2

if __name__ == "__main__":
    raise SystemExit(main())
