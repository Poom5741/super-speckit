#!/usr/bin/env python3
"""Minimal, dependency-free state/worktree helper for super-speckit."""
from __future__ import annotations
import argparse, html, json, re, subprocess, sys
from pathlib import Path

STATES = {"planned", "maker_running", "candidate_ready", "qa_running", "qa_failed", "bug_fixing", "retest_running", "ready_for_merge", "merged", "blocked"}
SHA = re.compile(r"^[0-9a-f]{7,64}$")

def root(value: str) -> Path: return Path(value).resolve()
def state_path(repo: Path, feature: str) -> Path: return repo / ".super-speckit/state/features" / f"{feature}.json"
def manifest_path(repo: Path) -> Path: return repo / ".super-speckit/state/work-state.yml"
def load(repo: Path, feature: str) -> dict: return json.loads(state_path(repo, feature).read_text())
def save(repo: Path, feature: str, data: dict) -> None:
    p = state_path(repo, feature); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(data, indent=2) + "\n")

def render_work_state_manifest(repo: Path) -> str:
    """Render a dependency-free YAML index that humans and other tools can inspect."""
    records=[]
    for path in sorted((repo / ".super-speckit/state/features").glob("*.json")):
        records.append(json.loads(path.read_text()))
    lines=["schema_version: 1", "authority: files-and-commands", "generated_from: .super-speckit/state/features/*.json", "features:"]
    if not records:
        lines[-1]="features: []"
    for data in records:
        lines.extend([
            f"  - id: {json.dumps(data.get('id'))}",
            f"    state: {json.dumps(data.get('state'))}",
            f"    candidate_sha: {json.dumps(data.get('candidate_sha'))}",
            f"    maker: {json.dumps(data.get('maker'))}",
            f"    checker: {json.dumps(data.get('checker'))}",
            f"    matrix: {json.dumps(data.get('matrix'))}",
            f"    purpose_status: {json.dumps(data.get('purpose', {}).get('status', 'not_started'))}",
            f"    purpose_map: {json.dumps(data.get('purpose', {}).get('map'))}",
            f"    grill_status: {json.dumps(data.get('grill', {}).get('status', 'not_started'))}",
            f"    grill_artifact: {json.dumps(data.get('grill', {}).get('artifact'))}",
            f"    route: {json.dumps(data.get('route', {}).get('kind', 'unclassified'))}",
            f"    atlas: {json.dumps(data.get('atlas', {}).get('path'))}",
            f"    change_story: {json.dumps(data.get('change_story', {}).get('path'))}",
            f"    latest_handoff: {json.dumps(data.get('handoff', {}).get('path'))}",
            f"    decision_trail: {json.dumps(data.get('decision_trail', {}).get('path'))}",
            f"    verification_harness: {json.dumps(data.get('verification_harness', {}).get('path'))}",
            f"    static_review: {json.dumps(data.get('static_review', {}).get('artifact'))}",
            f"    corrective_enforcement: {json.dumps(data.get('corrective_enforcement', {}).get('artifact'))}",
            f"    ui_change: {json.dumps(data.get('ui_change', False))}",
            f"    journey_ux_status: {json.dumps(data.get('journey_ux', {}).get('status', 'not_required'))}",
            f"    journey_ux_report: {json.dumps(data.get('journey_ux', {}).get('report'))}",
            f"    runs: {json.dumps(data.get('runs', []))}",
            f"    bugs: {json.dumps(data.get('bugs', []))}",
        ])
    return "\n".join(lines)+"\n"

def write_work_state_manifest(repo: Path) -> None:
    manifest_path(repo).parent.mkdir(parents=True, exist_ok=True)
    manifest_path(repo).write_text(render_work_state_manifest(repo))

def git_value(repo: Path, *args: str) -> str | None:
    result=subprocess.run(["git","-C",str(repo),*args],text=True,capture_output=True)
    return result.stdout.strip() if result.returncode == 0 else None

def validation_failures(repo: Path) -> list[str]:
    failures=[]
    for p in (repo / ".super-speckit/state/features").glob("*.json"):
        try:
            d=json.loads(p.read_text()); assert d["state"] in STATES; assert d["maker"] != d["checker"]
            assert d.get("purpose", {}).get("status") in {"not_started", "draft", "confirmed", "rework"}
            assert d.get("grill", {}).get("status") in {"not_started", "complete"}
            assert d.get("route", {}).get("kind", "unclassified") in {"unclassified", "micro", "normal", "milestone"}
            if d["state"] in {"candidate_ready","qa_running","ready_for_merge","merged"}: assert SHA.match(d.get("candidate_sha") or "")
            if d.get("ui_change") and d["state"] in {"ready_for_merge", "merged"}:
                journey=d.get("journey_ux", {})
                assert journey.get("status") == "passed", "UI release requires passing Journey UX Loop"
                assert journey.get("candidate_sha") == d.get("candidate_sha"), "Journey UX result must match latest candidate SHA"
                assert (repo / (journey.get("report") or "")).exists(), "Journey UX report is required"
            if d["state"] not in {"planned", "blocked"}:
                assert d.get("purpose", {}).get("status") == "confirmed", "human purpose confirmation is required"
                assert d.get("grill", {}).get("status") == "complete", "spec grill is required"
                assert d.get("route", {}).get("kind") in {"micro", "normal", "milestone"}, "scope route is required"
                assert (repo / (d.get("atlas", {}).get("path") or "")).exists(), "Project Atlas is required"
                assert (repo / (d.get("change_story", {}).get("path") or "")).exists(), "Change Story is required"
            assert (repo / d["matrix"]).exists()
        except Exception as e: failures.append(f"{p}: {e}")
    manifest=manifest_path(repo)
    if not manifest.exists():
        failures.append(f"missing required state manifest: {manifest}")
    elif manifest.read_text() != render_work_state_manifest(repo):
        failures.append(f"stale state manifest: {manifest}; run state mutation or regenerate it")
    return failures

def cmd_init(args):
    repo = root(args.repo)
    for path in [".super-speckit/state/features", ".super-speckit/qa", ".super-speckit/bugs"]: (repo / path).mkdir(parents=True, exist_ok=True)
    write_work_state_manifest(repo)
    print(f"initialized {repo / '.super-speckit'}")

def cmd_create(args):
    repo = root(args.repo)
    if args.maker == args.checker: raise ValueError("maker and checker must be distinct")
    data = {"id": args.feature, "state": "planned", "candidate_sha": None, "maker": args.maker, "checker": args.checker, "matrix": args.matrix, "ui_change": args.ui_change, "journey_ux": {"status": "not_required", "report": None, "candidate_sha": None}, "purpose": {"status": "not_started", "map": None, "decision": None}, "grill": {"status": "not_started", "artifact": None}, "route": {"kind": "unclassified", "rationale": None}, "atlas": {"path": None}, "change_story": {"path": None}, "handoff": {"path": None}, "decision_trail": {"path": None}, "verification_harness": {"path": None}, "static_review": {"artifact": None}, "corrective_enforcement": {"artifact": None}, "runs": [], "bugs": []}
    save(repo, args.feature, data); write_work_state_manifest(repo); print(state_path(repo,args.feature))

def cmd_transition(args):
    repo = root(args.repo); data = load(repo,args.feature)
    if args.state not in STATES: raise ValueError("unknown state")
    if args.sha:
        if not SHA.match(args.sha): raise ValueError("candidate SHA must be 7-64 lowercase hex characters")
        data["candidate_sha"] = args.sha
    if args.state in {"candidate_ready", "qa_running", "ready_for_merge"} and not data.get("candidate_sha"): raise ValueError("state requires a candidate SHA")
    if args.state == "qa_running" and data["maker"] == data["checker"]: raise ValueError("QA requires distinct maker/checker")
    if args.state not in {"planned", "blocked"} and data.get("purpose", {}).get("status") != "confirmed": raise ValueError("human purpose confirmation is required before work begins")
    if args.state not in {"planned", "blocked"} and data.get("grill", {}).get("status") != "complete": raise ValueError("a completed evidence-labeled spec grill is required before work begins")
    if args.state not in {"planned", "blocked"} and data.get("route", {}).get("kind") not in {"micro", "normal", "milestone"}: raise ValueError("scope route is required before work begins")
    if args.state not in {"planned", "blocked"} and not (repo / (data.get("atlas", {}).get("path") or "")).exists(): raise ValueError("Project Atlas is required before work begins")
    if args.state not in {"planned", "blocked"} and not (repo / (data.get("change_story", {}).get("path") or "")).exists(): raise ValueError("Change Story is required before work begins")
    if data.get("ui_change") and args.state in {"ready_for_merge", "merged"}:
        journey=data.get("journey_ux", {})
        if journey.get("status") != "passed" or journey.get("candidate_sha") != data.get("candidate_sha") or not (repo / (journey.get("report") or "")).exists():
            raise ValueError("UI release requires a passing Journey UX report for the latest candidate SHA")
    data["state"] = args.state; save(repo,args.feature,data); write_work_state_manifest(repo); print(json.dumps(data, indent=2))

def cmd_validate(args):
    repo = root(args.repo); failures=validation_failures(repo)
    if failures: print("\n".join(failures)); return 1
    print("super-speckit state valid"); return 0

def cmd_status(args):
    """Print a machine-readable evidence snapshot; never infer state from conversation."""
    repo=root(args.repo); failures=validation_failures(repo)
    feature=None
    if args.feature:
        path=state_path(repo,args.feature)
        feature={"id":args.feature,"state_file":str(path.relative_to(repo)),"exists":path.exists()}
        if path.exists():
            data=json.loads(path.read_text())
            feature.update({"state":data.get("state"),"candidate_sha":data.get("candidate_sha"),"maker":data.get("maker"),"checker":data.get("checker"),"matrix":data.get("matrix"),"matrix_exists":(repo / data.get("matrix","")).exists(),"ui_change":data.get("ui_change",False),"journey_ux":data.get("journey_ux"),"purpose":data.get("purpose"),"grill":data.get("grill"),"route":data.get("route"),"atlas":data.get("atlas"),"change_story":data.get("change_story"),"handoff":data.get("handoff")})
    status={
        "schema_version":1,
        "repository":str(repo),
        "git":{"head":git_value(repo,"rev-parse","HEAD"),"branch":git_value(repo,"branch","--show-current"),"dirty":bool(git_value(repo,"status","--porcelain")),"worktrees":(git_value(repo,"worktree","list","--porcelain") or "").count("worktree ")},
        "feature":feature,
        "state_validation":{"status":"pass" if not failures else "fail","failures":failures},
        "artifacts":{"config_exists":(repo/"super-speckit.yml").exists() or (repo/"config/super-speckit.yml").exists(),"native_specify_exists":(repo/".specify").exists(),"qa_root_exists":(repo/".super-speckit/qa").exists(),"work_state_manifest":str(manifest_path(repo).relative_to(repo)),"work_state_manifest_exists":manifest_path(repo).exists()},
    }
    print(json.dumps(status,indent=2))
    return 1 if args.strict and failures else 0

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

def cmd_purpose_gate(args):
    """Draft a visual purpose map. Only confirm-purpose can mark it confirmed."""
    repo=root(args.repo); data=load(repo,args.feature)
    directory=repo / ".super-speckit/purpose" / args.feature; directory.mkdir(parents=True, exist_ok=True)
    title=html.escape(args.title); outcome=html.escape(args.outcome); people=html.escape(args.people); success=html.escape(args.success); non_goals=html.escape(args.non_goals)
    markdown=f"""# Purpose Map — {args.feature}\n\n## Intended outcome\n{args.outcome}\n\n## People affected\n{args.people}\n\n## Success signal\n{args.success}\n\n## Non-goals\n{args.non_goals}\n\n## Human purpose gate\nThis map is a draft. A human confirms that this is the intended purpose, or corrects it. Technical implementation choices are deliberately outside this gate.\n"""
    (directory / "purpose-map.md").write_text(markdown)
    page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Purpose Map — {title}</title><style>body{{margin:0;background:#f4f7fb;color:#172033;font:16px/1.5 system-ui,sans-serif}}main{{max-width:960px;margin:auto;padding:32px 20px}}header,section{{background:#fff;border-radius:14px;padding:24px;margin:16px 0;box-shadow:0 1px 3px #17203318}}.tag{{font-weight:700;color:#075bcc}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}@media(max-width:650px){{.grid{{grid-template-columns:1fr}}}}</style><main><header><p class="tag">HUMAN PURPOSE GATE · DRAFT</p><h1>{title}</h1><p>{outcome}</p></header><section class="grid"><div><h2>Who this serves</h2><p>{people}</p></div><div><h2>How success is recognized</h2><p>{success}</p></div></section><section><h2>Explicit non-goals</h2><p>{non_goals}</p></section><section><h2>What confirmation means</h2><p>Confirm the intent, affected people, success signal, and boundaries. The agent owns technical discovery and delivery after this gate.</p></section></main>'''
    (directory / "purpose-map.html").write_text(page)
    decision={"feature":args.feature,"status":"draft","map":"purpose-map.md","visual":"purpose-map.html","confirmed_by":None,"confirmed_at":None,"confirmation":None}
    (directory / "decision.json").write_text(json.dumps(decision,indent=2)+"\n")
    data["purpose"]={"status":"draft","map":str((directory / "purpose-map.md").relative_to(repo)),"decision":str((directory / "decision.json").relative_to(repo))}; save(repo,args.feature,data); write_work_state_manifest(repo)
    print(directory / "purpose-map.html")

def cmd_confirm_purpose(args):
    repo=root(args.repo); data=load(repo,args.feature); purpose=data.get("purpose", {}); decision_path=repo / (purpose.get("decision") or "")
    if not decision_path.exists(): raise ValueError("create a purpose map before recording a human purpose decision")
    decision=json.loads(decision_path.read_text()); decision.update({"status":args.decision,"confirmed_by":args.confirmed_by,"confirmed_at":args.confirmed_at,"confirmation":args.confirmation})
    decision_path.write_text(json.dumps(decision,indent=2)+"\n")
    purpose["status"]="confirmed" if args.decision == "confirmed" else "rework"; data["purpose"]=purpose; save(repo,args.feature,data); write_work_state_manifest(repo); print(json.dumps(data["purpose"],indent=2))

def cmd_record_grill(args):
    repo=root(args.repo); data=load(repo,args.feature)
    if data.get("purpose", {}).get("status") != "confirmed": raise ValueError("human purpose confirmation is required before the spec grill")
    artifact=repo / args.artifact
    if not artifact.exists(): raise ValueError(f"missing grill artifact: {artifact}")
    data["grill"]={"status":"complete","artifact":args.artifact}; save(repo,args.feature,data); write_work_state_manifest(repo); print(json.dumps(data["grill"],indent=2))

def cmd_route(args):
    repo=root(args.repo); data=load(repo,args.feature)
    data["route"]={"kind":args.kind,"rationale":args.rationale}; save(repo,args.feature,data); write_work_state_manifest(repo); print(json.dumps(data["route"],indent=2))

def cmd_atlas_init(args):
    repo=root(args.repo); data=load(repo,args.feature); directory=repo / ".super-speckit/atlas"
    directory.mkdir(parents=True, exist_ok=True)
    readme=directory / "README.md"; graph=directory / "system-map.mmd"
    if not readme.exists():
        readme.write_text("# Project Atlas\n\nThis is a diagram-first, evidence-linked map of the codebase. It is a guide, not execution authority. Each statement links to a path, command result, or explicit unknown.\n\n## Update rule\n\nUpdate only the affected component cards after a verified change. Preserve unknowns rather than inventing architecture.\n")
    if not graph.exists(): graph.write_text("flowchart LR\n  User[User / external actor] --> Entry[Entry points: discover from repository]\n  Entry --> Components[Components: add evidence-linked cards]\n  Components --> Evidence[Runtime / test evidence]\n")
    feature_dir=directory / "changes" / args.feature; feature_dir.mkdir(parents=True, exist_ok=True)
    story=feature_dir / "change-story.md"
    story.write_text(f"# Change Story — {args.feature}\n\n## Confirmed purpose\n{args.summary}\n\n## Route\n{data.get('route', {}).get('kind', 'unclassified')}\n\n## Diagram-first path\n\n```mermaid\nflowchart LR\n  Request[Confirmed purpose] --> Entry[Known entry point: investigate]\n  Entry --> Logic[Changed logic: investigate]\n  Logic --> Data[Data / external boundary: investigate]\n  Data --> Proof[Verification evidence]\n```\n\n## What will change\n\n- Not yet verified. Link affected entry points, components, contracts, and data paths after repository investigation.\n\n## What stays protected\n\n- Preserve the Purpose Map non-goals and existing contracts until evidence supports a change.\n\n## Evidence and unknowns\n\n| Claim | Classification | Evidence / next probe |\n| --- | --- | --- |\n| Change path | unknown | inspect codebase and Atlas cards |\n")
    data["atlas"]={"path":str(readme.relative_to(repo)),"graph":str(graph.relative_to(repo))}; data["change_story"]={"path":str(story.relative_to(repo))}; save(repo,args.feature,data); write_work_state_manifest(repo); print(story)

def cmd_reassess(args):
    repo=root(args.repo); data=load(repo,args.feature); path=repo / args.artifact
    if not path.exists(): raise ValueError(f"missing reassessment artifact: {path}")
    data["reassessment"]={"path":args.artifact,"decision":args.decision}; save(repo,args.feature,data); write_work_state_manifest(repo); print(json.dumps(data["reassessment"],indent=2))

def cmd_record_handoff(args):
    repo=root(args.repo); data=load(repo,args.feature); path=repo / args.artifact
    if not path.exists(): raise ValueError(f"missing handoff artifact: {path}")
    data["handoff"]={"path":args.artifact,"transfer":args.transfer,"stage":args.stage,"attempt_id":args.attempt_id}; save(repo,args.feature,data); write_work_state_manifest(repo); print(json.dumps(data["handoff"],indent=2))

def cmd_record_journey_ux(args):
    repo=root(args.repo); data=load(repo,args.feature); report=repo / args.report
    if not data.get("ui_change"): raise ValueError("Journey UX results are only tracked for UI-changing features")
    if not report.exists(): raise ValueError(f"missing Journey UX report: {report}")
    if not SHA.match(args.sha): raise ValueError("candidate SHA must be 7-64 lowercase hex characters")
    data["journey_ux"]={"status":args.status,"report":args.report,"candidate_sha":args.sha}; save(repo,args.feature,data); write_work_state_manifest(repo); print(json.dumps(data["journey_ux"],indent=2))

def cmd_record_artifact(args):
    repo=root(args.repo); data=load(repo,args.feature); path=repo / args.artifact
    if not path.exists(): raise ValueError(f"missing artifact: {path}")
    if args.kind == "decision-trail": data["decision_trail"]={"path":args.artifact}
    elif args.kind == "verification-harness": data["verification_harness"]={"path":args.artifact}
    elif args.kind == "static-review": data["static_review"]={"artifact":args.artifact}
    elif args.kind == "corrective-enforcement": data["corrective_enforcement"]={"artifact":args.artifact}
    save(repo,args.feature,data); write_work_state_manifest(repo); print(json.dumps(data.get(args.kind.replace("-", "_"), data),indent=2))

def cmd_harness_init(args):
    repo=root(args.repo); directory=repo / ".super-speckit/verification"; directory.mkdir(parents=True, exist_ok=True)
    harness=directory / "verification-harness.md"; feature_map=directory / "feature-map.md"
    if (harness.exists() or feature_map.exists()) and not args.replace: raise ValueError("verification harness exists; use --replace only after reviewing runtime drift")
    harness.write_text("# Project Verification Harness\n\n## Launch and readiness\n\n- App start command: configure `gates.app_start` in `super-speckit.yml`.\n- App URL: configure `gates.app_url`.\n- Health/readiness checks: configure `qa.readiness_checks`.\n\n## Test-data isolation\n\n- Reset command: configure `qa.fixture_reset_command`.\n- Namespace each run with `qa.isolated_test_namespace`; do not use production identities.\n\n## Real behavior proof\n\n- Map each capability in `feature-map.md` to a real public seam.\n- Browser checks use configured Playwright plus exploratory/Journey UX review where applicable.\n- Add API/DB assertions when UI alone cannot prove a side effect.\n\n## Evidence and cleanup\n\n- Store sanitized commands, logs, traces, screenshots, video, and environment receipt under `.super-speckit/qa/<run-id>/`.\n- Stop app processes, clear only the isolated namespace, and record cleanup outcome.\n- A missing live run is `not-verified`, never pass.\n")
    feature_map.write_text("# Verification Feature Map\n\n| Capability / requirement | Entry point | Public seam | Deterministic check | Runtime journey | API / DB assertion | Evidence | Status |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n| Add project capabilities here |  |  |  |  |  |  | unverified |\n")
    print(harness)

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True)
    for name, fn in [("init",cmd_init),("validate",cmd_validate)]:
        x=sub.add_parser(name); x.add_argument("--repo",default="."); x.set_defaults(fn=fn)
    x=sub.add_parser("status"); x.add_argument("--repo",default="."); x.add_argument("--feature"); x.add_argument("--strict",action="store_true"); x.set_defaults(fn=cmd_status)
    x=sub.add_parser("create-feature"); x.add_argument("feature"); x.add_argument("--repo",default="."); x.add_argument("--maker",required=True); x.add_argument("--checker",required=True); x.add_argument("--matrix",required=True); x.add_argument("--ui-change",action="store_true"); x.set_defaults(fn=cmd_create)
    x=sub.add_parser("transition"); x.add_argument("feature"); x.add_argument("state"); x.add_argument("--repo",default="."); x.add_argument("--sha"); x.set_defaults(fn=cmd_transition)
    x=sub.add_parser("worktree"); x.add_argument("--repo",default="."); x.add_argument("--path",required=True); x.add_argument("--branch",required=True); x.add_argument("--ref",default="HEAD"); x.set_defaults(fn=cmd_worktree)
    x=sub.add_parser("design-first"); x.add_argument("feature"); x.add_argument("--title",required=True); x.add_argument("--summary",required=True); x.add_argument("--repo",default="."); x.set_defaults(fn=cmd_design)
    x=sub.add_parser("purpose-gate"); x.add_argument("feature"); x.add_argument("--repo",default="."); x.add_argument("--title",required=True); x.add_argument("--outcome",required=True); x.add_argument("--people",required=True); x.add_argument("--success",required=True); x.add_argument("--non-goals",required=True); x.set_defaults(fn=cmd_purpose_gate)
    x=sub.add_parser("confirm-purpose"); x.add_argument("feature"); x.add_argument("--repo",default="."); x.add_argument("--decision",choices=["confirmed","rework"],required=True); x.add_argument("--confirmed-by",required=True); x.add_argument("--confirmed-at",required=True); x.add_argument("--confirmation",required=True); x.set_defaults(fn=cmd_confirm_purpose)
    x=sub.add_parser("record-grill"); x.add_argument("feature"); x.add_argument("--repo",default="."); x.add_argument("--artifact",required=True); x.set_defaults(fn=cmd_record_grill)
    x=sub.add_parser("route"); x.add_argument("feature"); x.add_argument("kind",choices=["micro","normal","milestone"]); x.add_argument("--repo",default="."); x.add_argument("--rationale",required=True); x.set_defaults(fn=cmd_route)
    x=sub.add_parser("atlas-init"); x.add_argument("feature"); x.add_argument("--repo",default="."); x.add_argument("--summary",required=True); x.set_defaults(fn=cmd_atlas_init)
    x=sub.add_parser("reassess"); x.add_argument("feature"); x.add_argument("--repo",default="."); x.add_argument("--artifact",required=True); x.add_argument("--decision",choices=["keep","split","reorder","defer","cancel"],required=True); x.set_defaults(fn=cmd_reassess)
    x=sub.add_parser("record-handoff"); x.add_argument("feature"); x.add_argument("--repo",default="."); x.add_argument("--artifact",required=True); x.add_argument("--transfer",choices=["local-to-cloud","cloud-to-local","agent-to-agent","same-environment"],required=True); x.add_argument("--stage",required=True); x.add_argument("--attempt-id",required=True); x.set_defaults(fn=cmd_record_handoff)
    x=sub.add_parser("record-journey-ux"); x.add_argument("feature"); x.add_argument("--repo",default="."); x.add_argument("--report",required=True); x.add_argument("--sha",required=True); x.add_argument("--status",choices=["passed","blocked","defects"],required=True); x.set_defaults(fn=cmd_record_journey_ux)
    x=sub.add_parser("record-artifact"); x.add_argument("feature"); x.add_argument("kind",choices=["decision-trail","verification-harness","static-review","corrective-enforcement"]); x.add_argument("--repo",default="."); x.add_argument("--artifact",required=True); x.set_defaults(fn=cmd_record_artifact)
    x=sub.add_parser("harness-init"); x.add_argument("--repo",default="."); x.add_argument("--replace",action="store_true"); x.set_defaults(fn=cmd_harness_init)
    a=p.parse_args()
    try: result=a.fn(a); return result or 0
    except Exception as e: print(f"error: {e}",file=sys.stderr); return 2
if __name__ == "__main__": raise SystemExit(main())
