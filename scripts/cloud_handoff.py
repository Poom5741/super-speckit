#!/usr/bin/env python3
"""Render a safe, bounded cloud-delegation pack from a factual handoff."""
from __future__ import annotations
import argparse
from pathlib import Path

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--handoff", required=True, help="redacted durable handoff Markdown")
    p.add_argument("--output", required=True)
    p.add_argument("--transport", choices=["codex-cloud", "centillex-desk"], default="codex-cloud")
    p.add_argument("--role", choices=["research", "maker", "bug-fix"], required=True)
    p.add_argument("--base-sha", required=True)
    p.add_argument("--branch", required=True)
    p.add_argument("--objective", required=True)
    p.add_argument("--environment-id", default="")
    a=p.parse_args()
    handoff=Path(a.handoff).read_text()
    forbidden=("BEGIN PRIVATE KEY", "Authorization: Bearer", "ghp_", "sk-")
    if any(token in handoff for token in forbidden):
        raise SystemExit("refusing cloud pack: handoff appears to contain a secret")
    pack=f"""# Cloud delegation pack\n\n- Transport: `{a.transport}`\n- Role: `{a.role}`\n- Base branch and immutable SHA: `{a.branch}` / `{a.base_sha}`\n- Environment ID: `{a.environment_id or 'not-set'}`\n\n## Bounded objective\n\n{a.objective}\n\n## Constraints\n\n- Read the handoff below before changing code.\n- Work only in the isolated cloud task branch.\n- Do not merge, apply changes locally, publish external work, or claim QA approval.\n- Return candidate SHA, changed files, commands/statuses, tests, and unverified items.\n\n## Redacted durable handoff\n\n{handoff}\n\n## Receiver verification\n\nA separate Super-SpecKit QA worktree will verify any returned change.\n"""
    output=Path(a.output); output.parent.mkdir(parents=True, exist_ok=True); output.write_text(pack)
    print(output)
    return 0
if __name__ == "__main__": raise SystemExit(main())
