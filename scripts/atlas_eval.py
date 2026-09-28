#!/usr/bin/env python3
"""Compare blinded Project Atlas evaluation records without external dependencies."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def load(path: str) -> dict:
    data=json.loads(Path(path).read_text())
    if data.get("schema_version") != 1: raise ValueError(f"unsupported schema in {path}")
    if data.get("condition") not in {"control", "atlas"}: raise ValueError(f"invalid condition in {path}")
    return data

def score(run: dict) -> dict:
    total=run.get("requirements_total") or 0
    covered=run.get("requirements_correctly_covered") or 0
    expected=set(run.get("expected_impacted_components") or [])
    found=set(run.get("identified_impacted_components") or [])
    return {
        "coverage": covered / total if total else None,
        "component_recall": len(expected & found) / len(expected) if expected else None,
        "unsupported_claims": run.get("unsupported_claims") or 0,
        "duration_seconds": run.get("duration_seconds"),
        "token_count": run.get("token_count"),
        "qa_pass": run.get("independent_qa_status") == "pass",
        "completed": bool(run.get("completed")),
    }

def mean(values: list[float | int | None]) -> float | None:
    vals=[float(v) for v in values if v is not None]
    return sum(vals)/len(vals) if vals else None

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--control",required=True); parser.add_argument("--atlas",required=True); parser.add_argument("--output",required=True)
    args=parser.parse_args(); control=load(args.control); atlas=load(args.atlas)
    errors=[]
    for key in ("task_id", "base_sha", "agent_and_model", "blind_task_brief"):
        if control.get(key) != atlas.get(key): errors.append(f"mismatch: {key}")
    pairs=min(len(control.get("runs",[])),len(atlas.get("runs",[])))
    control_scores=[score(run) for run in control.get("runs",[])[:pairs]]; atlas_scores=[score(run) for run in atlas.get("runs",[])[:pairs]]
    valid=[i for i in range(pairs) if control_scores[i]["completed"] and atlas_scores[i]["completed"] and control_scores[i]["qa_pass"] and atlas_scores[i]["qa_pass"]]
    if errors or len(valid) < 3:
        conclusion="inconclusive"
        reason="configuration mismatch" if errors else "fewer than three paired, completed runs with independent QA pass"
    else:
        def avg(side, field): return mean([side[i][field] for i in valid])
        c_cov,a_cov=avg(control_scores,"coverage"),avg(atlas_scores,"coverage")
        c_rec,a_rec=avg(control_scores,"component_recall"),avg(atlas_scores,"component_recall")
        c_bad,a_bad=avg(control_scores,"unsupported_claims"),avg(atlas_scores,"unsupported_claims")
        if a_cov is not None and c_cov is not None and a_rec is not None and c_rec is not None and a_bad is not None and c_bad is not None and a_cov >= c_cov and a_rec >= c_rec and a_bad <= c_bad and (a_cov > c_cov or a_rec > c_rec or a_bad < c_bad):
            conclusion="benefit-supported"; reason="Atlas improved or matched coverage and component recall while not increasing unsupported claims"
        else:
            conclusion="no-clear-benefit"; reason="paired QA-passing runs did not show a consistent comprehension-quality improvement"
    report=["# Project Atlas evaluation", "", f"- Conclusion: **{conclusion}**", f"- Reason: {reason}", f"- Comparable paired runs: {len(valid)} / {pairs}"]
    if errors: report += ["", "## Comparability issues", *[f"- {e}" for e in errors]]
    report += ["", "## Per-run scores", "", "| Condition | Run | Coverage | Component recall | Unsupported claims | QA pass |", "| --- | --- | --- | --- | --- | --- |"]
    for name, scores in [("control",control_scores),("atlas",atlas_scores)]:
        for index, item in enumerate(scores,1):
            def fmt(value): return "n/a" if value is None else f"{value:.2f}" if isinstance(value,float) else str(value)
            report.append(f"| {name} | {index} | {fmt(item['coverage'])} | {fmt(item['component_recall'])} | {item['unsupported_claims']} | {item['qa_pass']} |")
    Path(args.output).write_text("\n".join(report)+"\n")
    print(args.output)
    return 0
if __name__ == "__main__": raise SystemExit(main())
