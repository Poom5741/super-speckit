---
description: Accessibility audit on the current repo (any UI surface). WCAG 2.1 AA pass, assistive technology walk, microcopy review.
argument-hint: "[optional: path or area to focus, defaults to whole repo]"
---

# Accessibility audit

Target: $ARGUMENTS (defaults to the whole repo).

Run a WCAG 2.1 AA accessibility audit on the UI surface. Works for web, mobile, and native macOS / iOS / Android.

## Detect first

- Surface type: web (HTML / React / Vue / Svelte), iOS (SwiftUI / UIKit), Android (Compose / Views), macOS (AppKit / SwiftUI), Flutter, RN.
- Whether the project has an accessibility test setup already.

## Agents to dispatch in parallel

1. `senior-ux-designer` skill, primary lead. Walk Nielsen heuristics plus WCAG 2.1 AA. Findings with severity (cosmetic / minor / major / catastrophic).

2. `senior-frontend-engineer` skill (for web) OR matched stack expert (for native), semantic HTML / native control usage, focus management, ARIA only when justified, keyboard navigation, screen reader names, target sizes (44 by 44 on touch), color contrast, motion reduced variants, dark mode.

3. `code-reviewer`, code level a11y issues: divs with onClick, placeholder as label, alt text missing, color only signaling, focus traps in modals, missing language attributes, dynamic content without aria-live.

4. `test-engineer`, a11y test coverage: axe-core / Pa11y integration for web, accessibility inspector use for native, keyboard only test passes.

5. `senior-technical-writer` skill, microcopy review: button labels are verbs, error messages plain language and actionable, empty states explain what goes here.

## What to walk (WCAG 2.1 AA quick list)

### Perceivable
- Text alternatives for non text content.
- Captions and transcripts for audio / video.
- Content presentable in different ways (responsive, zoom).
- Color contrast at least 4.5:1 for normal text, 3:1 for large text and UI components.

### Operable
- Keyboard accessible without traps.
- Enough time for any timed responses; offer extensions.
- No content that flashes more than three times per second.
- Skip links, page titles, focus order, link purpose clear.
- Target size at least 44 by 44 for touch.

### Understandable
- Language of page or component declared.
- Predictable navigation; consistent identification of components.
- Error identification with suggestion; labels and instructions for inputs.

### Robust
- Markup parses; name, role, value programmatically determinable.

## Output format

### Verdict
**Pass / Fail / Pass with caveats** in one sentence.

### Findings
Numbered, each with:
- WCAG criterion (e.g., 1.4.3 Contrast Minimum).
- Severity.
- Location (file:line or component name).
- Affected users (keyboard only, screen reader, low vision, etc.).
- Reproduction (how to see it).
- Recommended fix.

### Quick wins
The top three fixes that take less than an hour each.

### Structural changes
Larger fixes that need a sprint or two.

### Testing recommendations
Specific tests (axe rules to enable, manual keyboard runs, screen reader scripts).

### Next 5 commits
Ranked by user impact.

Cite the subagent. Keep it terse.
