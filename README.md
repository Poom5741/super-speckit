# Super-SpecKit v2 — kernel

Kernel 4 ชิ้น: **artifact contract · ledger · receipt gate · manifest**
(ลดจาก v1 ที่ 1,189 ไฟล์ — ของเดิมทั้งหมดอยู่บน branch `archive/v1`)

## โครง

```
manifest.schema.json          สัญญากลาง: stage → skills + receipt
manifest.example.yml          ตัวอย่าง manifest ใช้งานจริง (5 stages)
schemas/receipt.schema.json   รูปแบบ receipt ที่ gate ยอมรับ
cli/ssk.py                    CLI: init / add-card / status / add-receipt / verify
cli/yaml_min.py               YAML subset parser (stdlib — ไม่พึ่ง PyYAML)
cli/test_ssk.py               pytest 4 tests (TDD)
registry/                     proto-registry จาก adapters v1
```

## เริ่มใช้

```bash
python3 cli/ssk.py init                       # สร้าง .ssk/ ในโปรเจกต์คุณ
python3 cli/ssk.py add-card T-1 "my card"
python3 cli/ssk.py add-receipt T-1 receipt.json
python3 cli/ssk.py verify T-1                 # GATE PASS → done / GATE BLOCKED
python3 -m pytest cli/test_ssk.py -v          # test suite
```

หลักการ: receipt gate บังคับทุกการ์ด · skills ไม่เก็บใน repo (manifest ชี้ชื่อ/ที่มา) ·
SSK รับ "การ์ด" เป็น input เท่านั้น — รายละเอียดใน `SKILL.md`

Python stdlib ล้วน ไม่ต้องติดตั้งอะไร (ต้องมี pytest สำหรับ run tests เท่านั้น)
