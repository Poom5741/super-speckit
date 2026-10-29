#!/usr/bin/env python3
"""Install a complete Super-SpecKit bundle without overwriting an existing project kit."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

BUNDLE_PATHS = ("SKILL.md", "commands", "config", "docs", "schemas", "scripts", "templates", "workflows", "skills", "sources.lock.json", "vendor", "adapters", "package.json", "pnpm-lock.yaml", "pnpm-workspace.yaml", "v2")
ENTRYPOINTS = {
    "super-speckit": (".super-speckit/SKILL.md", "Run the complete evidence-first Super-SpecKit workflow."),
    "ask-super-speckit": (".super-speckit/skills/ask-super-speckit/SKILL.md", "Autonomously route a feature, bug, or idea through Super-SpecKit."),
    "super-speckit-design-first": (".super-speckit/skills/design-first/SKILL.md", "Create and review an HTML design decision before UI implementation."),
    "super-speckit-final-manual-review": (".super-speckit/skills/final-manual-review/SKILL.md", "Guide independent human final review and route defects safely."),
}
PROJECT_SKILL_ROOTS = (
    ".agents/skills",
    ".codex/skills",
    ".claude/skills",
    ".cursor/skills",
    ".opencode/skills",
    ".pi/skills",
    ".zcode/skills",
)

def user_skill_roots() -> tuple[Path, ...]:
    """Return native user-level skill roots without requiring a harness CLI."""
    home=Path.home()
    xdg_config=Path(os.environ.get("XDG_CONFIG_HOME", home / ".config"))
    return (
        home / ".agents/skills",
        home / ".codex/skills",
        home / ".claude/skills",
        home / ".cursor/skills",
        xdg_config / "opencode/skills",
        home / ".pi/agent/skills",
        home / ".zcode/skills",
    )

def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    files = [path] if path.is_file() else sorted(p for p in path.rglob("*") if p.is_file() and "__pycache__" not in p.parts and "node_modules" not in p.parts)
    for file in files:
        digest.update((file.name if path.is_file() else file.relative_to(path).as_posix()).encode())
        digest.update(str(bool(file.stat().st_mode & stat.S_IXUSR)).encode())
        digest.update(file.read_bytes())
    return digest.hexdigest()

def verify_bundle(source: Path) -> None:
    # Every newly bundled specialist and native reference is pinned byte-for-byte.
    for name in ('lude-kit', 'spec-kit'):
        manifest=json.loads((source / f'vendor/{name}-manifest.json').read_text())
        vendor=source / manifest['root']
        expected={row['path']:row['sha256'] for row in manifest['files']}
        actual={p.relative_to(vendor).as_posix() for p in vendor.rglob('*') if p.is_file()}
        if actual!=set(expected): raise ValueError(f'incomplete or unexpected {name} source')
        for name_,checksum in expected.items():
            path=vendor/name_
            if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest()!=checksum:
                raise ValueError(f'{name} source integrity failed: {name_}')
    manifest = json.loads((source / "vendor/pstack-manifest.json").read_text())
    vendor = source / manifest["root"]
    modes = {row["path"]: row.get("mode", "100644") for row in manifest["files"]}
    expected = {row["path"]: row["sha256"] for row in manifest["files"]}
    actual = {p.relative_to(vendor).as_posix() for p in vendor.rglob("*") if p.is_file()}
    if actual != set(expected): raise ValueError("incomplete or unexpected PStack source")
    for name, digest in expected.items():
        file=vendor/name
        if file.is_symlink() or hashlib.sha256(file.read_bytes()).hexdigest() != digest:
            raise ValueError(f"PStack source integrity failed: {name}")
        if bool(file.stat().st_mode & stat.S_IXUSR) != (modes[name] == "100755"):
            raise ValueError(f"PStack source mode drift: {name}")

def write_entrypoints(root: Path, entrypoints: dict[str, tuple[str, str]], force: bool, *, skip_conflicts: bool = False) -> list[Path]:
    skipped=[]
    for name, (canonical, description) in entrypoints.items():
        directory=root / name; skill=directory / "SKILL.md"
        if directory.exists() and not force:
            if skill.exists() and canonical in skill.read_text():
                continue
            if skip_conflicts:
                skipped.append(directory)
                continue
            raise ValueError(f"refusing to overwrite existing skill entry point: {directory}; use --force only after reviewing it")
        if directory.exists():
            backup=directory.with_name(directory.name + ".pre-super-speckit")
            if backup.exists(): raise ValueError(f"entrypoint backup already exists: {backup}")
            directory.rename(backup)
        directory.mkdir(parents=True, exist_ok=True)
        skill.write_text(f"""---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n\nLocate the active project root as the nearest ancestor containing `.super-speckit/`. The canonical Super-SpecKit instructions live at `{canonical}` relative to that root. If no ancestor contains `.super-speckit/`, explain that Super-SpecKit must first be installed into the active project and stop. Read the canonical file completely before acting, then resolve source/adapter paths inside `.super-speckit/` and state/artifact paths from the project root. Invoke bundled tools as `python3 .super-speckit/scripts/<tool>.py --repo .` from the project root where supported; the adapter CLI derives its kit path from its installation and uses `--kit .super-speckit` only when overriding it. This wrapper exists only to make the installed entry point discoverable; it is not a second source of workflow truth.\n""")
    return skipped

def register_entrypoints(target: Path, force: bool, scope: str) -> None:
    """Expose the public surface at project scope, user scope, or both."""
    if scope in ("project", "both"):
        for relative_root in PROJECT_SKILL_ROOTS:
            write_entrypoints(target / relative_root, ENTRYPOINTS, force)
    if scope in ("global", "both"):
        for root in user_skill_roots():
            for conflict in write_entrypoints(root, ENTRYPOINTS, force, skip_conflicts=not force):
                print(f"warning: skipped conflicting user skill {conflict}; review it and rerun with --force to replace it with a backup", file=sys.stderr)
    register_opencode_plugin(target, force)

def register_opencode_plugin(target: Path, force: bool) -> None:
    """Register the prebuilt V2 plugin without copying credentials into the project."""
    runtime=target / ".super-speckit/v2/packages/opencode/dist"
    if not (runtime / "index.js").exists() or not (runtime / "tui.js").exists() or not (runtime / "rpc.js").exists():
        raise ValueError("installed bundle is missing the prebuilt OpenCode V2 plugin")
    directory=target / ".opencode/plugins/super-speckit"
    marker="super-speckit-managed-opencode-plugin"
    package=directory / "package.json"
    if directory.exists() and not force:
        if package.exists() and marker in package.read_text():
            return
        raise ValueError(f"refusing to overwrite existing OpenCode plugin: {directory}; use --force only after reviewing it")
    if directory.exists():
        backup=directory.with_name(directory.name + ".pre-super-speckit")
        if backup.exists(): raise ValueError(f"OpenCode plugin backup already exists: {backup}")
        directory.rename(backup)
    directory.mkdir(parents=True)
    package.write_text(json.dumps({
        "name": marker,
        "private": True,
        "type": "module",
        "exports": {".": "./index.js", "./tui": "./tui.js", "./rpc": "./rpc.js"},
    }, indent=2)+"\n")
    (directory / "index.js").write_text('export { default } from "../../../.super-speckit/v2/packages/opencode/dist/index.js";\n')
    (directory / "tui.js").write_text('export { default } from "../../../.super-speckit/v2/packages/opencode/dist/tui.js";\n')
    (directory / "rpc.js").write_text('export * from "../../../.super-speckit/v2/packages/opencode/dist/rpc.js";\n')

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
        archive_root=(temp / "archive").resolve()
        for entry in zf.infolist():
            if not (archive_root / entry.filename).resolve().is_relative_to(archive_root):
                raise ValueError("unsafe path in bundle archive")
        zf.extractall(archive_root)
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
        register_entrypoints(target, args.force, args.entrypoint_scope)
        subprocess.run(["python3", str(destination / "scripts/super_speckit.py"), "validate", "--repo", str(target)], check=True)
        print(f"registered Super-SpecKit entry points at {args.entrypoint_scope} scope")
        return
    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="super-speckit-install-") as directory:
        source=bundle_source(args, Path(directory))
        verify_bundle(source)
        for item in BUNDLE_PATHS:
            if not (source/item).exists(): raise ValueError(f"bundle is missing required path: {item}")
        if destination.exists():
            drift=[]
            receipt=destination / "install-receipt.json"
            installed=json.loads(receipt.read_text()).get("digests",{}) if receipt.exists() else {}
            for item, digest in installed.items():
                if not (destination/item).exists() or tree_digest(destination/item)!=digest: drift.append(item)
            if drift and not args.force:
                raise ValueError(f"installed bundle was modified: {', '.join(drift)}; preserve/review changes before --force")
            same=all((destination/item).exists() and tree_digest(destination/item)==tree_digest(source/item) for item in BUNDLE_PATHS)
            if not same and not (args.upgrade or args.force):
                raise ValueError("bundle revision differs; use --upgrade for a deliberate update")
            if not same:
                backup=target / ".super-speckit-upgrade-backup"
                if backup.exists(): raise ValueError(f"upgrade backup already exists: {backup}")
                backup.mkdir()
                for item in BUNDLE_PATHS:
                    prior=destination/item
                    if prior.exists():
                        if prior.is_dir(): shutil.copytree(prior,backup/item)
                        else: shutil.copy2(prior,backup/item)
        destination.mkdir(exist_ok=True)
        for item in BUNDLE_PATHS:
            origin=source/item; copied=destination/item
            if not origin.exists(): raise ValueError(f"bundle is missing required path: {item}")
            if copied.exists() and tree_digest(copied)==tree_digest(origin): continue
            if copied.exists():
                if copied.is_dir(): shutil.rmtree(copied)
                else: copied.unlink()
            if origin.is_dir():
                shutil.copytree(origin,copied,ignore=shutil.ignore_patterns("__pycache__", ".super-speckit", "node_modules"))
            else: shutil.copy2(origin,copied)
        (destination / "install-receipt.json").write_text(json.dumps({"schema_version":1,"digests":{item:tree_digest(destination/item) for item in BUNDLE_PATHS}},indent=2)+"\n")
    project_config=target / "super-speckit.yml"
    if not project_config.exists():
        shutil.copy2(destination / "config/super-speckit.yml", project_config)
    subprocess.run(["python3", str(destination / "scripts/super_speckit.py"), "init", "--repo", str(target)], check=True)
    subprocess.run(["python3", str(destination / "scripts/super_speckit.py"), "validate", "--repo", str(target)], check=True)
    register_entrypoints(target, args.force, args.entrypoint_scope)
    print(f"installed Super-SpecKit to {destination}; registered entry points at {args.entrypoint_scope} scope")

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--target", default=".")
    parser.add_argument("--repository", default="Poom5741/super-speckit")
    parser.add_argument("--ref", default="main")
    parser.add_argument("--source", help="local repository path; useful for offline or test installation")
    parser.add_argument("--force", action="store_true", help="preserve backup and replace reviewed bundle/entrypoint drift")
    parser.add_argument("--upgrade", action="store_true", help="deliberately update a clean installed bundle without replacing project config/state")
    parser.add_argument("--register-only", action="store_true", help="register skill entry points for an existing project kit without downloading it")
    parser.add_argument("--entrypoint-scope", choices=("project", "global", "both"), default="both", help="register public skills in the project, user harness roots, or both (default: both)")
    args=parser.parse_args()
    try:
        install(args); return 0
    except Exception as error:
        print(f"error: {error}", file=sys.stderr); return 2

if __name__ == "__main__":
    raise SystemExit(main())
