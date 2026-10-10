---
name: super-speckit
description: Deliver with PStack playbooks, selective Spec Kit planning, Dune-inspired architecture checks, and independent runtime and usability evidence.
---

# super-speckit

Use `ask-super-speckit` as the single coordinator. Read `skills/ask-super-speckit/references/playbook-delivery.md` for routing, architecture, verification, and unattended-run contracts. Read `docs/orchestration.md` and `schemas/README.md` before changing tracked delivery artifacts.

PStack playbooks drive execution. Select native Spec Kit for normal/milestone requirements, plans, and tasks; bounded micro fixes use one persisted playbook and verification matrix. Read-only teaching and investigation create no delivery state. Preserve the user's confirmed purpose and record actual provenance rather than asking again.

Use one code-writing checkout by default. Independent checkers verify a committed exact candidate in a clean temporary clone with isolated data. Worktrees are optional compatibility tools. Checker changes are limited to evidence and bug artifacts. Any new candidate needs fresh proof.

Inspect the real flow and relevant language/framework guidance before code. Encode project-specific dependency boundaries, public interfaces, durable-state ownership, and narrow exceptions in executable checks. Load pinned PStack methods through `adapters/pstack/override-contract.md`; vendor source never becomes another coordinator.

Require both product acceptance and engineering acceptance. Product acceptance uses complete journeys on the running app, with API/DB assertions for effects the browser cannot prove. Engineering acceptance uses configured checks and independent candidate review. Static review cannot satisfy runtime rows. UI changes retain independent Journey UX verification. Label each requirement verified, not-verified, or not-applicable with evidence; missing access is never a pass.

For long runs persist a checkable completion predicate, steps, authority, budget, decision trail, and an observed host wake mechanism. Repair and resume within those limits without routine approval. Do not promise overnight continuation without a functioning runner. Confirm failures before filing bugs; require regression coverage or a justified exception and independent retest. Release only with exact-candidate proof, no blocking defects, configured authority, and current forge readiness.
