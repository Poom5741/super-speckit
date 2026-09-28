---
description: Create and maintain a diagram-first, evidence-linked Project Atlas and per-feature Change Story before implementation.
---

Run `python3 scripts/super_speckit.py atlas-init <feature> --summary "<confirmed purpose>"`. This creates a committed `.super-speckit/atlas/README.md`, Mermaid `system-map.mmd`, and `.super-speckit/atlas/changes/<feature>/change-story.md`.

The Atlas answers what the product/system does and how it does it: entry points, components, contracts, data and external boundaries, evidence links, and unknowns. The Change Story explains the proposed change as a visual path before raw code: what changes, protected behavior, downstream effects, verification, and uncertainty. Populate it by inspecting the repository; mark unresolved paths `unknown` rather than inventing them. Update only affected component cards after verified slices. These files are context projections, never proof or execution authority.
