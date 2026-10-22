---
description: Open source readiness sweep on the current repo. Multi agent check of LICENSE, README, SECURITY, CI, secrets, attributions, conventions. Returns a go / no go.
argument-hint: "[optional: path to repo, defaults to current directory]"
---

# Open source readiness sweep

Target: $ARGUMENTS (defaults to the current directory if blank).

Run a parallel multi agent sweep to determine whether this repo is ready to flip to public open source. Returns a single go / no go verdict plus a remediation list.

## Agents to dispatch in parallel

1. `tech-writer`, README quality. First time visitor can understand what this is, who it is for, and how to use it within sixty seconds. Quickstart compiles and runs. CONTRIBUTING.md present and useful. CHANGELOG.md present.

2. `security-reviewer`, secrets check across history: scan committed files for hard coded API keys, tokens, private keys, `.env` files. Note: a full git history scan needs `gitleaks` or `trufflehog`; report what can be seen in the current working tree.

3. `compliance-engineer`, LICENSE present and correct, third party license obligations honored, attributions file if needed, copyright headers consistent if your style includes them.

4. `dependency-auditor`, every dependency has a compatible license for the chosen project license, lockfile present, no postinstall scripts that pull from random URLs.

5. `senior-devops-sre` skill, CI configured (at minimum: lint + test on PR), branch protection considered, signed releases considered, semver policy stated.

6. `code-reviewer`, README badges align with reality, links resolve, examples in docs compile, no TODO markers in shipped code that would embarrass the maintainer.

7. `architect`, project structure makes sense to a stranger, no dead folders, no `OLD` / `_archive` dumps, sensible defaults.

8. `senior-product-manager` skill, pitch is clear, audience is named, value prop is concrete, roadmap is honest (no vaporware promises).

9. `senior-ux-designer` skill, README visual hierarchy, badges, screenshots or gifs where useful, hero example, table of contents on long READMEs.

10. `senior-technical-writer` skill (the LudeSkills skill, not the subagent), overall prose tone, plain language, no marketing fluff, no broken links, sentence case headings, code blocks tagged with languages.

## Checklist the synthesis must answer

- [ ] LICENSE file present and matches the headline license.
- [ ] README answers: what is this, who is it for, what problem does it solve, how to install, quickstart, how to contribute.
- [ ] CONTRIBUTING.md present with workflow and commit style.
- [ ] CODE_OF_CONDUCT.md present.
- [ ] SECURITY.md present with disclosure contact.
- [ ] No secrets in current files.
- [ ] No `.env` committed.
- [ ] `.gitignore` covers the obvious (node_modules, .env, .DS_Store, build outputs).
- [ ] Third party licenses honored.
- [ ] CI runs on PR.
- [ ] Issue and PR templates present.
- [ ] Repo description and topics set (caller can confirm on GitHub).
- [ ] First time clone works: `git clone && <install> && <run>` succeeds on a fresh machine.

## Output format

### Verdict
**Ready / Hold / Block** in one sentence.

### Blockers
Each blocker named with severity, the missing file or fix, owning subagent.

### Recommended order of fixes
A numbered list of the next commits to make. Each commit aimed at one blocker.

### Polish (non blocking)
Bulleted suggestions to raise the bar.

### Public release plan
Three steps: pre flip (final checks), flip command (`gh repo edit ... --visibility public`), post flip (announce, pin, star count zero is fine).

Cite the subagent that produced each finding. Keep it terse.
