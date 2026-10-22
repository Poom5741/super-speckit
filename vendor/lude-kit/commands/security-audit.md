---
description: Focused security audit on the current repo. Threat model, secure code review, dependency audit, supply chain. Defensive only.
argument-hint: "[optional: path or area to focus, defaults to whole repo]"
---

# Security audit

Target: $ARGUMENTS (defaults to the whole repo).

Run a focused security audit. Defensive only: own repos, authorized review. Refuse offensive misuse.

## Agents to dispatch in parallel

1. `security-reviewer`, primary lead. Threat model the surface area using STRIDE. Walk inputs from edge to sink. Auth and authz boundaries. Secrets handling. Findings with severity (critical / high / medium / low / informational).

2. `dependency-auditor`, supply chain pass: lockfile diff, CVE alerts, postinstall scripts, license review, transitive risk, CI runner permissions, OIDC vs static keys.

3. `code-reviewer`, secure code review of the diff or whole tree. Look for: input parsing at boundaries, output encoding at sinks, IDOR, SSRF, deserialization, injection, hard coded credentials, log lines that leak secrets.

4. `senior-ai-safety-engineer` skill (only if the repo has LLM / agent surface), prompt injection, output safety, tool authorization, training data leakage, jailbreak surface, EU AI Act / NIST AI RMF classification.

5. `compliance-engineer`, applicable regimes (SOC 2, ISO 27001, HIPAA, PCI DSS, GDPR, FedRAMP) and which controls this repo intersects.

6. `senior-devops-sre` skill, CI / infra security: long lived static credentials, secrets in env vars, branch protection, code signing on releases, container image hygiene.

## Output format

### Executive summary
Two paragraphs an exec or auditor can read in thirty seconds.

### Threat model
- Assets and classification.
- Trust boundaries (data flow diagram in mermaid if useful).
- Top threats per element with STRIDE category and severity.

### Findings
Numbered, each with:
- Severity (critical / high / medium / low / informational)
- Category (OWASP A01 etc, or "supply chain", "secrets handling", etc.)
- Location (file:line if any)
- Description
- Reproduction or evidence
- Recommended fix (concrete, with a code sketch if applicable)

### Accepted risks
Risks the team should explicitly accept and document, with owner and revisit date.

### Hardening plan
Table with: control, threat mitigated, cost (low / medium / high), priority (P0 / P1 / P2), owner, due date.

### Next 5 commits
Ranked by severity reduction.

Defensive only. Never produce offensive tooling, jailbreak prompts targeted at unauthorized systems, evasion guidance, or attack techniques outside an authorized engagement. If the user asks for offensive misuse, decline.

Cite the subagent that produced each finding. Keep it terse.
