# OMP team task contract — <ATTEMPT-ID>

- Feature / phase / immutable base SHA:
- Role: `atlas-scout | contract-scout | test-designer | maker | static-reviewer | qa-planner`
- Worktree / read-only boundary:
- Allowed files and explicit exclusions:
- Bounded objective:
- Required evidence and output schema:
- Stop / escalation condition:

## Structured return

Return a typed result, not a narrative-only report:

```json
{
  "attempt_id": "...",
  "status": "complete|blocked|failed|inconclusive",
  "base_sha": "...",
  "changed_files": [],
  "evidence_paths": [],
  "facts": [],
  "unknowns": [],
  "next_safe_action": "..."
}
```

No worker may certify merge, release, human purpose confirmation, or its own QA.
