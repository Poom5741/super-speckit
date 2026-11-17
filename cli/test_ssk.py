"""TDD tests for SSK v2 CLI (receipt gate).

Run: python3 -m pytest cli/test_ssk.py -v
4 tests:
  1. init สร้าง .ssk/ ครบ (manifest + ledger)
  2. add-receipt ผนวก receipt เข้า ledger ถูก stage
  3. verify BLOCK เมื่อขาด stage
  4. verify PASS เมื่อ receipt ครบทุก stage และ result=pass
"""
import json
import os
import subprocess
import sys

import pytest

CLI = os.path.join(os.path.dirname(__file__), "ssk.py")

MANIFEST_STAGES = ["plan", "implement", "verify", "deploy", "review"]


def run_ssk(root, *args):
    """Run the CLI exactly as a user would."""
    return subprocess.run(
        [sys.executable, CLI, *args],
        cwd=root, capture_output=True, text=True,
    )


def receipt(stage, result="pass", card_id="T-TEST"):
    return {
        "card_id": card_id,
        "stage": stage,
        "type": "test-report",
        "result": result,
        "artifacts": ["artifacts/{}.json".format(stage)],
        "timestamp": "2026-11-17T12:00:00Z",
    }


@pytest.fixture
def repo(tmp_path):
    """An initialized SSK workspace with card T-TEST."""
    r = run_ssk(str(tmp_path), "init")
    assert r.returncode == 0, r.stderr
    r = run_ssk(str(tmp_path), "add-card", "T-TEST", "add button")
    assert r.returncode == 0, r.stderr
    return tmp_path


def add_receipt(root, stage, result="pass"):
    path = root / "r-{}.json".format(stage)
    path.write_text(json.dumps(receipt(stage, result)))
    return run_ssk(str(root), "add-receipt", "T-TEST", str(path))


def test_init_creates_ssk(tmp_path):
    r = run_ssk(str(tmp_path), "init")
    assert r.returncode == 0, r.stderr
    ssk = tmp_path / ".ssk"
    assert (ssk / "manifest.yml").is_file()
    assert (ssk / "ledger.json").is_file()
    import sys

    sys.path.insert(0, os.path.dirname(CLI))
    from yaml_min import load as yload

    manifest = yload(str(ssk / "manifest.yml"))
    assert manifest["version"] == "2.0"
    for stage in MANIFEST_STAGES:
        assert stage in manifest["stages"], stage
    ledger = json.loads((ssk / "ledger.json").read_text())
    assert ledger["cards"] == {}


def test_add_receipt_merges_into_ledger(repo):
    r = add_receipt(repo, "plan")
    assert r.returncode == 0, r.stderr
    ledger = json.loads((repo / ".ssk" / "ledger.json").read_text())
    got = ledger["cards"]["T-TEST"]["receipts"]["plan"]
    assert got["result"] == "pass"
    assert got["card_id"] == "T-TEST"


def test_verify_blocks_when_stage_missing(repo):
    r = add_receipt(repo, "plan")
    assert r.returncode == 0, r.stderr
    r = run_ssk(str(repo), "verify", "T-TEST")
    assert r.returncode == 1
    assert "GATE BLOCKED" in r.stdout + r.stderr
    ledger = json.loads((repo / ".ssk" / "ledger.json").read_text())
    assert ledger["cards"]["T-TEST"]["status"] != "done"


def test_verify_passes_when_all_receipts_pass(repo):
    for stage in MANIFEST_STAGES:
        r = add_receipt(repo, stage)
        assert r.returncode == 0, (stage, r.stderr)
    r = run_ssk(str(repo), "verify", "T-TEST")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "GATE PASS" in r.stdout
    ledger = json.loads((repo / ".ssk" / "ledger.json").read_text())
    assert ledger["cards"]["T-TEST"]["status"] == "done"
