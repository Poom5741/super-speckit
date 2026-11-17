---
name: super-speckit
description: Super-SpecKit v2 kernel (SSK) — evidence-first card pipeline การ์ด → stage → receipt → CLI gate (init / add-card / status / add-receipt / verify) บังคับ receipt result=pass ครบทุก stage (plan → implement → verify → deploy → review) ก่อนปิดการ์ด ใช้เมื่อเริ่มงานเป็น "การ์ด" (ไม่รับ brief ลอย ๆ) หรือเมื่อต้องบังคับ proof ก่อน done
---

# SKILL: Super-SpecKit v2 (SSK)

## ปรัชญา

Pipeline ไม่ได้อยู่ในหัว agent — **อยู่ใน artifacts** สามชิ้น:

1. **manifest** (`.ssk/manifest.yml`) — สัญญากลาง: แต่ละ stage ใช้ skill อะไร และต้องคืน receipt ชนิดใด
2. **ledger** (`.ssk/ledger.json`) — การ์ดทุกใบ + สถานะ + receipts ที่เก็บไว้
3. **receipt gate** (`cli/ssk.py verify`) — การ์ดจะ `done` ได้ต่อเมื่อมี receipt **ครบทุก stage ตาม manifest** และทุกใบ `result=pass` — CLI เป็นผู้บังคับ ไม่ใช่ความจำของ agent

กติกาที่ห้ามฝ่า:
- **receipt gate บังคับทุกการ์ด** — ห้ามปิด stage ด้วยมือ ห้ามแก้ ledger เขียน status=done เอง
- **skills ไม่เก็บใน repo** — manifest ชี้แค่ชื่อ/ที่มา (`skills.sh` / `harness` / `builtin`)
- **evidence ฝั่ง manual-test ให้ dev เป็นผู้ดู** — agent แนบ path ใน receipt ไม่ตัดสินแทน
- **SSK รับ "การ์ด" เป็น input เท่านั้น** — ไม่รับ brief ลอย ๆ

## Workflow: การ์ด → stage → receipt → gate

```
ssk.py init                          # สร้าง .ssk/ จาก manifest.example.yml
ssk.py add-card T-123 "add button"   # เปิดการ์ดใหม่
# ทำงานทีละ stage ตาม manifest: plan → implement → verify → deploy → review
# จบ stage ไหน เขียน receipt json ใบเดียว (ดูรูปแบบด้านล่าง) แล้ว:
ssk.py add-receipt T-123 receipt-plan.json
ssk.py status                        # ตารางการ์ด: ✔ pass · ✘ fail · … pending · · ยังไม่ส่ง
ssk.py verify T-123                  # gate: block ถ้าขาด/ตก · pass → done
```

`verify` เป็น **บล็อก** ระหว่างทางเสมอจนกว่า receipt จะครบ — ตั้งใจให้เป็นอย่างนั้น
(ผ่านไม่ได้ = ยังทำไม่ครบ ไม่ใช่ CLI พัง)

## รูปแบบ receipt

```json
{
  "card_id": "T-123",
  "stage": "verify",
  "type": "test-report",
  "result": "pass",
  "artifacts": ["evidence/T-123/test-report.md"],
  "timestamp": "2026-11-17T12:00:00Z"
}
```

- `type` ∈ test-report | evidence | diff | deploy-url | human-verdict
- `result` ∈ pass | fail | pending — มีแต่ `pass` เท่านั้นที่นับเข้า gate
- schema เต็ม: `schemas/receipt.schema.json` · สัญญา manifest: `manifest.schema.json`

## วิธี agent อ่าน manifest (แทนการจำคำสั่ง)

ก่อนเริ่มการ์ด: อ่าน `.ssk/manifest.yml` แล้วทำตามที่มันบอก เช่น `verify` stage ระบุ
skill `jeffallan/claude-skills@playwright-expert` (skills.sh) + `ssk/evidence` (builtin)
— agent ติดตั้ง/เรียก skill เหล่านั้นตามที่มา ไม่เดาเอง ถ้า skill ไม่มีใน harness
ให้ทำงานด้วยมือตาม skill นั้นและแนบ evidence ใน receipt ให้ครบ

## ตัวอย่าง session จริง 1 รอบ

```
$ ssk.py init
$ ssk.py add-card T-TEST "add button"
$ ssk.py verify T-TEST
GATE BLOCKED · T-TEST · missing=['plan','implement','verify','deploy','review'] failed=[]
$ ssk.py add-receipt T-TEST r-plan.json      # plan pass
$ ssk.py add-receipt T-TEST r-impl.json      # implement pass (type=diff)
$ ssk.py add-receipt T-TEST r-verify.json    # verify pass (type=test-report)
$ ssk.py verify T-TEST
GATE BLOCKED · T-TEST · missing=['deploy','review'] failed=[]
$ ssk.py add-receipt T-TEST r-deploy.json    # deploy-url pass
$ ssk.py add-receipt T-TEST r-review.json    # human-verdict pass (dev กดอนุมัติ)
$ ssk.py verify T-TEST
GATE PASS · T-TEST → done
```

## ขอบเขต repo นี้

- `manifest.schema.json` + `manifest.example.yml` — สัญญา stage→skill+receipt
- `schemas/receipt.schema.json` — รูปแบบ receipt
- `cli/ssk.py` + `cli/yaml_min.py` + `cli/test_ssk.py` — CLI + gate (stdlib ล้วน, `pytest cli/test_ssk.py`)
- `registry/` — proto-registry ดึงมาจาก adapters v1 (catalog เก่า)

ประวัติ v1 เต็ม (1,189 ไฟล์: vendor/skills/commands/docs/...) อยู่บน branch `archive/v1`
— อ่านได้ แต่ไม่ merge กลับ และไม่อ้างอิงในงานปัจจุบัน
