#!/usr/bin/env python3
"""Minimal, dependency-free state/worktree helper for super-speckit."""
from __future__ import annotations
import argparse, html, json, re, subprocess, sys
from pathlib import Path

STATES = {"planned", "maker_running", "candidate_ready", "qa_running", "qa_failed", "bug_fixing", "retest_running", "ready_for_human_merge", "merged", "blocked"}
SHA = re.compile(r"^[0-9a-f]{7,64}$")

def root(value: str) -> Path: return Path(value).resolve()
def state_path(repo: Path, feature: str) -> Path: return repo / ".super-speckit/state/features" / f"{feature}.json"
def load(repo: Path, feature: str) -> dict: return json.loads(state_path(repo, feature).read_text())
def save(repo: Path, feature: str, data: dict) -> None:
    p = state_path(repo, feature); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(data, indent=2) + "\n")

def cmd_init(args):
    repo = root(args.repo)
    for path in [".super-speckit/state/features", ".super-speckit/qa", ".super-speckit/bugs"]: (repo / path).mkdir(parents=True, exist_ok=True)
    print(f"initialized {repo / '.super-speckit'}")

def cmd_create(args):
    repo = root(args.repo)
    if args.maker == args.checker: raise ValueError("maker and checker must be distinct")
    data = {"id": args.feature, "state": "planned", "candidate_sha": None, "maker": args.maker, "checker": args.checker, "matrix": args.matrix, "runs": [], "bugs": []}
    save(repo, args.feature, data); print(state_path(repo,args.feature))

def cmd_transition(args):
    repo = root(args.repo); data = load(repo,args.feature)
    if args.state not in STATES: raise ValueError("unknown state")
    if args.sha:
        if not SHA.match(args.sha): raise ValueError("candidate SHA must be 7-64 lowercase hex characters")
        data["candidate_sha"] = args.sha
    if args.state in {"candidate_ready", "qa_running", "ready_for_human_merge"} and not data.get("candidate_sha"): raise ValueError("state requires a candidate SHA")
    if args.state == "qa_running" and data["maker"] == data["checker"]: raise ValueError("QA requires distinct maker/checker")
    data["state"] = args.state; save(repo,args.feature,data); print(json.dumps(data, indent=2))

def cmd_validate(args):
    repo = root(args.repo); failures=[]
    for p in (repo / ".super-speckit/state/features").glob("*.json"):
        try:
            d=json.loads(p.read_text()); assert d["state"] in STATES; assert d["maker"] != d["checker"]
            if d["state"] in {"candidate_ready","qa_running","ready_for_human_merge","merged"}: assert SHA.match(d.get("candidate_sha") or "")
            assert (repo / d["matrix"]).exists()
        except Exception as e: failures.append(f"{p}: {e}")
    if failures: print("\n".join(failures)); return 1
    print("super-speckit state valid"); return 0

def cmd_worktree(args):
    repo=root(args.repo); dest=Path(args.path).resolve()
    if dest.exists(): raise ValueError(f"destination exists: {dest}")
    branch=args.branch
    subprocess.run(["git","-C",str(repo),"worktree","add","-b",branch,str(dest),args.ref],check=True)

def cmd_design(args):
    """Create an intentionally static decision prototype, never app code."""
    repo=root(args.repo); directory=repo / ".super-speckit/design" / args.feature
    directory.mkdir(parents=True, exist_ok=True)
    title=html.escape(args.title); summary=html.escape(args.summary)
    prototype = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} — design prototype</title><style>:root{{--ink:#18212f;--muted:#526170;--surface:#fff;--wash:#f2f6fa;--accent:#075bcc;--danger:#b42318}}*{{box-sizing:border-box}}body{{margin:0;font:16px/1.5 system-ui,sans-serif;color:var(--ink);background:var(--wash)}}main{{max-width:960px;margin:auto;padding:32px 20px}}header,section{{background:var(--surface);padding:24px;border-radius:14px;margin:16px 0;box-shadow:0 1px 3px #18212f18}}h1{{margin-top:0}}.eyebrow{{color:var(--accent);font-weight:700}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}button{{background:var(--accent);color:white;border:0;border-radius:8px;padding:10px 14px;font:inherit}}.state{{border-left:4px solid var(--accent)}}.error{{border-color:var(--danger)}}a:focus,button:focus{{outline:3px solid #f6c945;outline-offset:3px}}@media(max-width:620px){{.grid{{grid-template-columns:1fr}}main{{padding:16px}}}}</style></head><body><main><header><p class="eyebrow">DESIGN DECISION DRAFT · {html.escape(args.feature)}</p><h1>{title}</h1><p>{summary}</p><p><strong>Prototype only.</strong> It represents assumptions for review; it is not implemented product behavior.</p></header><section><h2>Primary path</h2><div class="grid"><div><h3>Task context</h3><p>Give people the information and next action they need, with a clear hierarchy.</p><button type="button">Primary action</button></div><div><h3>Confirmation</h3><p>Show a specific, accessible result after the action. Never use colour alone to convey status.</p></div></div></section><section><h2>Required states</h2><div class="grid"><article class="state"><h3>Loading</h3><p>Describe what is loading and preserve context.</p></article><article class="state"><h3>Empty</h3><p>Explain why there is no content and offer a next action.</p></article><article class="state error"><h3>Error</h3><p>Explain what happened, what was not changed, and how to recover.</p></article><article class="state"><h3>Permission denied</h3><p>State access limitation without exposing restricted data.</p></article></div></section><section><h2>Review checklist</h2><ul><li>Keyboard focus and labels are visible.</li><li>Narrow-screen layout is intentional.</li><li>Content is synthetic; no personal or secret data appears.</li><li>Existing component/token sources must be applied before implementation.</li></ul></section></main></body></html>'''
    (directory / "prototype.html").write_text(prototype)
    (directory / "design-brief.md").write_text(f"# {args.feature} — {args.title}\n\n## Problem\n{args.summary}\n\n## Assumptions to review\n\n- User, hierarchy, and state behavior need product confirmation.\n- Reuse the repository design system when one is declared.\n- This prototype is not production code.\n")
    decision={"feature":args.feature,"status":"draft","prototype":"prototype.html","brief":"design-brief.md","design_system_sources":[],"external_sources":[],"decision_by":None,"decision_at":None,"notes":"Awaiting review."}
    (directory / "decision.json").write_text(json.dumps(decision,indent=2)+"\n")
    print(directory / "prototype.html")

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True)
    for name, fn in [("init",cmd_init),("validate",cmd_validate)]:
        x=sub.add_parser(name); x.add_argument("--repo",default="."); x.set_defaults(fn=fn)
    x=sub.add_parser("create-feature"); x.add_argument("feature"); x.add_argument("--repo",default="."); x.add_argument("--maker",required=True); x.add_argument("--checker",required=True); x.add_argument("--matrix",required=True); x.set_defaults(fn=cmd_create)
    x=sub.add_parser("transition"); x.add_argument("feature"); x.add_argument("state"); x.add_argument("--repo",default="."); x.add_argument("--sha"); x.set_defaults(fn=cmd_transition)
    x=sub.add_parser("worktree"); x.add_argument("--repo",default="."); x.add_argument("--path",required=True); x.add_argument("--branch",required=True); x.add_argument("--ref",default="HEAD"); x.set_defaults(fn=cmd_worktree)
    x=sub.add_parser("design-first"); x.add_argument("feature"); x.add_argument("--title",required=True); x.add_argument("--summary",required=True); x.add_argument("--repo",default="."); x.set_defaults(fn=cmd_design)
    a=p.parse_args()
    try: result=a.fn(a); return result or 0
    except Exception as e: print(f"error: {e}",file=sys.stderr); return 2
if __name__ == "__main__": raise SystemExit(main())
