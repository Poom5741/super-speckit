#!/usr/bin/env python3
"""SSK v2 CLI — init / add-card / status / add-receipt / verify

receipt gate: การ์ดจะ done ได้ต่อเมื่อมี receipt ครบทุก stage ตาม manifest
และทุก receipt มี result=pass — CLI เป็นผู้บังคับ ไม่ใช่ความจำของ agent

Python stdlib ล้วน (YAML subset parser อยู่ใน yaml_min.py ข้างกัน)
"""
import datetime
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yaml_min import load as yaml_load  # noqa: E402

RECEIPT_TYPES = ("test-report", "evidence", "diff", "deploy-url", "human-verdict")
RECEIPT_RESULTS = ("pass", "fail", "pending")
RECEIPT_REQUIRED = ("card_id", "stage", "type", "result", "artifacts", "timestamp")


def die(msg, code=1):
    print(msg)
    sys.exit(code)


def ssk_dir(root="."):
    return os.path.join(root, ".ssk")


def load_manifest(root="."):
    return yaml_load(os.path.join(ssk_dir(root), "manifest.yml"))


def load_ledger(root="."):
    with open(os.path.join(ssk_dir(root), "ledger.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def save_ledger(root, ledger):
    with open(os.path.join(ssk_dir(root), "ledger.json"), "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)


def cmd_init(root="."):
    d = ssk_dir(root)
    os.makedirs(d, exist_ok=True)
    mpath = os.path.join(d, "manifest.yml")
    if not os.path.exists(mpath):
        example = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               os.pardir, "manifest.example.yml")
        shutil.copyfile(example, mpath)
    lpath = os.path.join(d, "ledger.json")
    if not os.path.exists(lpath):
        save_ledger(root, {"cards": {}})
    print("SSK init · .ssk/ ready (manifest.yml + ledger.json)")


def cmd_add_card(root, card_id, title=""):
    ledger = load_ledger(root)
    if card_id in ledger["cards"]:
        die("card already exists: %s" % card_id)
    ledger["cards"][card_id] = {
        "id": card_id,
        "title": title,
        "status": "open",
        "receipts": {},
    }
    save_ledger(root, ledger)
    print("card added · %s (%s)" % (card_id, title))


def validate_receipt(root, receipt, card_id):
    for field in RECEIPT_REQUIRED:
        if field not in receipt:
            die("receipt missing field: %s" % field)
    if receipt["card_id"] != card_id:
        die("receipt card_id %r != target card %r" % (receipt["card_id"], card_id))
    if receipt["type"] not in RECEIPT_TYPES:
        die("receipt type %r not in %s" % (receipt["type"], list(RECEIPT_TYPES)))
    if receipt["result"] not in RECEIPT_RESULTS:
        die("receipt result %r not in %s" % (receipt["result"], list(RECEIPT_RESULTS)))
    manifest = load_manifest(root)
    stage = receipt["stage"]
    if stage not in manifest.get("stages", {}):
        die("receipt stage %r not defined in manifest" % stage)
    return stage, manifest


def cmd_add_receipt(root, card_id, receipt_path):
    with open(receipt_path, "r", encoding="utf-8") as f:
        receipt = json.load(f)
    stage, _manifest = validate_receipt(root, receipt, card_id)
    ledger = load_ledger(root)
    card = ledger["cards"].get(card_id)
    if card is None:
        die("no card %s" % card_id)
    card.setdefault("receipts", {})[stage] = receipt
    save_ledger(root, ledger)
    print("receipt added · %s / %s → %s" % (card_id, stage, receipt["result"]))


def cmd_status(root="."):
    manifest = load_manifest(root)
    ledger = load_ledger(root)
    stages = list(manifest.get("stages", {}))
    print("SSK status · stages=%s" % ", ".join(stages))
    cards = ledger.get("cards", {})
    if not cards:
        print("  (no cards)")
    for card_id, card in cards.items():
        marks = " ".join(
            {"pass": "✔", "fail": "✘", "pending": "…", None: "·"}[
                (card.get("receipts", {}).get(stage) or {}).get("result")
            ]
            for stage in stages
        )
        print("  %-12s [%s] %s · %s" % (card_id, card.get("status", "?"), marks, card.get("title", "")))


def cmd_verify(root, card_id):
    manifest = load_manifest(root)
    ledger = load_ledger(root)
    card = ledger["cards"].get(card_id)
    if card is None:
        die("no card %s" % card_id)
    receipts = card.get("receipts", {})
    missing, failed = [], []
    for stage in manifest.get("stages", {}):
        r = receipts.get(stage)
        if not r:
            missing.append(stage)
        elif r.get("result") != "pass":
            failed.append(stage)
    if missing or failed:
        print("GATE BLOCKED · %s · missing=%s failed=%s" % (card_id, missing, failed))
        sys.exit(1)
    card["status"] = "done"
    save_ledger(root, ledger)
    print("GATE PASS · %s → done" % card_id)


def main(argv):
    commands = {
        "init": (cmd_init, "[]"),
        "add-card": (cmd_add_card, "<card-id> [title]"),
        "status": (cmd_status, "[]"),
        "add-receipt": (cmd_add_receipt, "<card-id> <receipt.json>"),
        "verify": (cmd_verify, "<card-id>"),
    }
    if not argv or argv[0] not in commands:
        die("usage: ssk.py %s" % " | ".join(
            "%s %s" % (name, sig) for name, (_fn, sig) in sorted(commands.items())))
    name = argv[0]
    fn, _sig = commands[name]
    root = os.environ.get("SSK_ROOT", ".")
    args = argv[1:]
    if name == "init":
        fn(args[0] if args else root)
    elif name == "add-card":
        fn(root, args[0], " ".join(args[1:]) if len(args) > 1 else "")
    elif name == "status":
        fn(args[0] if args else root)
    elif name == "add-receipt":
        if len(args) != 2:
            die("usage: ssk.py add-receipt <card-id> <receipt.json>")
        fn(root, args[0], args[1])
    elif name == "verify":
        if len(args) != 1:
            die("usage: ssk.py verify <card-id>")
        fn(root, args[0])


if __name__ == "__main__":
    main(sys.argv[1:])
