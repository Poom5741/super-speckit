---
description: Deep multi agent review of a website or web app for perf, a11y, security, SEO, UX, framework idioms, and open source readiness.
argument-hint: "[optional: path to repo, defaults to current directory]"
---

# Website / web app deep review

Target: $ARGUMENTS (defaults to the current directory if blank).

Run a parallel multi agent review of the web app at the target path. Detect the framework first (Next.js, Remix, SvelteKit, Nuxt, Astro, plain React, plain Vue). Dispatch the matching stack expert plus the generalist agents below in parallel via the Agent tool. After all return, synthesize a single verdict.

## Detect first

1. Read `package.json` and the root files to detect the framework.
2. Note the package manager (npm, pnpm, yarn, bun) and the lockfile.
3. Note the deploy target (Vercel, Netlify, Cloudflare, self hosted).

## Agents to dispatch in parallel

1. `code-reviewer` plus the matched stack expert (`nextjs-expert`, `tailwind-expert`, `typescript-expert`, etc.), code quality review with severity labels.

2. `security-reviewer`, OWASP top 10 walk over the codebase: auth, session, XSS, SSRF, CSRF, secrets handling, CSP, security headers, SameSite cookies, prompt injection if any AI features.

3. `senior-frontend-engineer` skill, component design, state placement, a11y at the markup level, hydration cost, bundle hygiene.

4. `perf-investigator`, Core Web Vitals (LCP, INP, CLS), bundle size, code split boundaries, image strategy, font loading, network waterfalls.

5. `a11y` perspective via `senior-ux-designer` skill, WCAG 2.1 AA pass: keyboard navigation, focus management, color contrast, alt text, ARIA only when justified, motion preferences.

6. `test-engineer`, Playwright / Cypress coverage, RTL component tests, contract tests, CI gates.

7. `tech-writer`, README, contributing, in product copy (microcopy quality), changelog.

8. `dependency-auditor`, npm audit, lockfile diff trail, postinstall scripts, license obligations.

9. `senior-ux-designer` skill, UX heuristics, mobile responsive review, error states, empty states, loading states, microcopy.

10. `architect`, overall architecture: server vs client split, data fetching pattern, caching strategy, env var hygiene, monorepo or polyrepo decisions.

## Output format

### Verdict
**Ship / Hold / Block** in one sentence.

### Top 5 blockers
Ranked, with severity, file:line, owning subagent, recommended action.

### Strong suggestions
Grouped by area: perf, a11y, security, code quality, UX, docs.

### Core Web Vitals snapshot
Estimated p75 LCP, INP, CLS based on code review (caveat: real numbers come from Lighthouse / RUM, but flag obvious cost centers).

### What was done well
Brief praise.

### Open source readiness
LICENSE, README, SECURITY, .env example, secrets check, contribution path.

### Next 5 commits
Ranked by impact, each with owning subagent.

Cite the subagent that produced each finding. Keep it terse.
