---
name: skill-name-here
description: >
  Use when {trigger verbs}, {artifact nouns}, or {situations}. Produces
  {outputs}. {Antitrigger if needed, name the better fit skill}.
license: Apache-2.0
metadata:
  version: "1.0.0"
  category: persona
---

# {Display Name}

## Role

One paragraph. Who this skill is when invoked. What lens it brings. What seniority level. What it cares about more than the average engineer.

## When to invoke

- Trigger situation 1, written as a verb phrase.
- Trigger situation 2.
- Trigger situation 3.
- ...

Also invoke when the user uses any of: {synonyms / phrases}.

Do **not** invoke when: {situation that belongs to another skill}. Hand off to `other-skill`.

## Operating principles

1. **{Principle name}.** One sentence stating it. One sentence on the consequence when it is violated.
2. **{Principle name}.** ...
3. ...

(5 to 10 principles. Sharp. Defensible. Specific to this role.)

## Workflow

When activated, follow this sequence:

1. **{Step verb}.** What to do, what to read, what to ask.
2. **{Step verb}.** ...
3. ...

## Deliverables

This skill produces one or more of:

### {Artifact name}

Shape / template:

```
{concrete template}
```

### {Artifact name}

...

## Quality bar

Before claiming done, verify:

- [ ] {Concrete check 1}
- [ ] {Concrete check 2}
- [ ] {Concrete check 3}
- [ ] ...

## Antipatterns

- **{Antipattern}.** Why it happens. What to do instead.
- ...

## Handoffs

- For {situation}, hand off to `other-skill-name`.
- ...

## Quick reference

| Question | Answer |
|---|---|
| What does this skill produce? | {one liner} |
| What does it explicitly not do? | {one liner} |
| Common partner skills | `skill-a`, `skill-b` |
