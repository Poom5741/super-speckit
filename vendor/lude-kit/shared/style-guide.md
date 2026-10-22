# Skill authoring style guide

The bar for every skill in this repo. Read this before writing or editing one.

A skill is a folder under one of the category dirs (`skills/personas/`, `skills/capabilities/`, `skills/stacks/`). The folder name **must equal** the `name:` field, lowercase kebab, no leading or trailing or consecutive hyphens, 1 to 64 chars. Inside lives one `SKILL.md`.

## The portable frontmatter

```yaml
---
name: my-skill
description: >
  One sentence on what this skill does and when. Lead with trigger phrases, 
  the verbs and nouns that should pull this skill off the shelf. Examples are
  better than adjectives. <=1024 chars total.
license: Apache-2.0
metadata:
  version: "1.0.0"
  category: persona            # persona | capability | stack
---
```

That is the entire required surface for both Claude Code and Codex. Do **not** add Claude only or Codex only keys to `SKILL.md`. If a skill needs platform specific config, put it in a sibling file (`agents/openai.yaml` for Codex, `agents/claude.yaml` for Claude). None of the persona skills in batch 1 should need either.

## The description is the trigger

Both platforms preload only the `description` into context. The body never loads unless the description matches the user's intent. So the description is not a tagline, it is the matcher.

Rules:

1. **Front load the verbs and nouns a user would actually type.** "Use when designing a system, choosing a database, writing an ADR, deciding build vs buy, reviewing an architecture diagram."
2. **List concrete artifacts the skill produces.** "Produces ADRs, system diagrams, RFCs, capacity plans."
3. **Include synonyms.** Architect ↔ design ↔ system ↔ topology. PM ↔ product ↔ PRD ↔ spec.
4. **State antitriggers when overlap is likely.** "Not for code review of a single file, see `senior-code-reviewer`."
5. **Stay under 1024 chars** including the `description:` key. Strip every adjective that does not add a trigger word.
6. **No marketing prose.** "Expert in" and "best in class" cost tokens and match nothing.

A good description reads like a search query the user might type. A bad one reads like a LinkedIn headline.

## The body

Hard ceilings:
- Under 500 lines.
- Under ~5,000 tokens.
- Single file. No `references/` or `examples/` subdirs in the base 10, keep it self contained per user preference. (Capability and stack skills in later batches may use sibling files for deep references.)

Canonical section order (every skill in this repo follows it so an orchestrator can scan many skills consistently):

1. **Role**, one paragraph. Who this skill is when invoked.
2. **When to invoke**, bullet list of trigger situations, explicit and verbose. This is the body-side complement to the frontmatter description.
3. **Operating principles**, 5, 10 numbered principles this role lives by. Sharp, opinionated, defensible.
4. **Workflow**, the concrete steps the skill follows when it activates. Numbered. Each step has a verb.
5. **Deliverables**, the artifacts this skill produces, with a short template or shape for each.
6. **Quality bar**, a checklist the skill uses to self verify before claiming done.
7. **Antipatterns**, what this skill does NOT do, and the kinds of mistakes a naive impersonation would make.
8. **Handoffs**, when and how to defer to another skill in the library. Reference by skill name in backticks.
9. **Quick reference**, a compressed cheat sheet at the bottom for fast scanning on reactivation.

## Style rules

- **Imperative voice.** "Write the PRD." not "The PRD should be written."
- **Concrete over abstract.** Numbers, names, examples. No "leverage synergies."
- **No first person.** The skill is not a character with feelings; it is a role with a job.
- **No reassurance, no apology.** Skip "Great question!" and "I'll do my best."
- **No emojis** unless the deliverable template demands one (e.g., a changelog convention).
- **Headings ATX style** (`##`), not underline. Sentence case headings.
- **Code fences with language tags.** ` ```ts `, ` ```bash `, ` ```yaml `.

## Composability

Skills in this repo are designed to be summoned together by an orchestrator agent. A `staff-software-architect` does not implement; it produces a design that a `senior-backend-engineer` and `senior-frontend-engineer` execute. The Handoffs section in each skill names the partners.

Two consequences:

- A skill should describe **what it produces** more than how the orchestrator consumes it.
- A skill should refuse to do work that belongs to another role and name the right one.

## Verification

Before merging a skill, run this check:

1. Read only the frontmatter `description`. Could a user looking for this role find it from the description alone? Could a sibling skill be falsely triggered by overlap?
2. Read only the body. Does every section pull its weight? Cut anything that would not change the skill's output.
3. Hand the skill to a teammate cold. Within 60 seconds of skimming, can they describe what artifact this skill produces and when not to use it?

If any of the three fails, the skill is not done.
