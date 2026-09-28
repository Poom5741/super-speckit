---
description: Draft a visual Purpose Map and obtain the one required human confirmation before autonomous delivery.
---

Create a planned feature state, then use `python3 scripts/super_speckit.py purpose-gate <feature> --title ... --outcome ... --people ... --success ... --non-goals ...`. It creates `.super-speckit/purpose/<feature>/purpose-map.md`, a visual `purpose-map.html`, and a draft decision record.

The human gates only the intended outcome, people affected, success signal, and non-goals. They do not choose technical implementation. On their confirmation, record it exactly with `confirm-purpose --decision confirmed --confirmed-by <human> --confirmed-at <ISO-8601> --confirmation <summary>`. A correction uses `--decision rework`, updates the map, and must be reconfirmed. Never have an agent write a human confirmation on its own behalf.

The resulting file record is required before maker work can begin. If later discovery materially contradicts the confirmed purpose, return here; otherwise proceed autonomously.
