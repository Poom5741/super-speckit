---
description: Deep multi agent review of a macOS app for bugs, security, perf, UX, and open source readiness. Dispatches ten subagents in parallel and synthesizes a single verdict.
argument-hint: "[optional: path to repo, defaults to current directory]"
---

# macOS app deep review

Target: $ARGUMENTS (defaults to the current directory if blank).

Run a parallel multi agent review of the macOS app at the target path. Dispatch the following subagents simultaneously via the Agent tool. Each returns a structured report. After all return, synthesize the findings into a single verdict.

## Agents to dispatch in parallel

1. `code-reviewer` plus the `swift-ios-expert` skill loaded, full code quality review across the Swift / SwiftUI / AppKit codebase. Severity labels (blocking, strong, nit) on every comment. Focus on: force unwraps, retain cycles, `@MainActor` boundary violations, `@State` / `@Observable` / `ObservableObject` correctness, deprecated API usage, swift concurrency hygiene.

2. `security-reviewer`, STRIDE threat model focused on macOS specifics: sandbox entitlements (which ones, why), app group sharing, Keychain usage, code signing identity, notarization status, hardened runtime, network client permissions, raw user input paths, URL schemes, helper tools, XPC services.

3. `debugger`, read the code adversarially and surface likely bug clusters. Concurrency bugs (data races, actor reentrancy, Task cancellation), lifecycle bugs (window controllers, NSDocument, App lifecycle phases), memory leaks (closure capture, observer dangling), KVO misuse, NSCoder fragility.

4. `perf-investigator`, Instruments worthy hotspots in the code. Main thread work, image decode on the UI thread, layout thrash in updates, expensive operations in hot draws, memory growth patterns, animation cost.

5. `test-engineer`, test coverage assessment, missing regression cases, balance of unit tests vs XCTestPlan integration vs XCUITest, CI gates, fixture hygiene.

6. `tech-writer`, README quality, CONTRIBUTING, in app help, App Store description draft (if shipping to MAS), changelog discipline.

7. `dependency-auditor`, package manifests (SPM, Carthage, CocoaPods), supply chain risk, license obligations, third party attributions for the Acknowledgments screen.

8. With `senior-ux-designer` skill triggered, focus on Apple HIG for macOS (NOT iOS): menu bar discipline, window restoration, keyboard shortcuts, dark mode, dynamic type, VoiceOver, localization readiness, status bar conventions, drag and drop.

9. `compliance-engineer`, Mac App Store eligibility if applicable, sandboxing review, privacy nutrition label readiness, third party SDK transparency.

10. `architect`, overall architecture review: separation between view, model, services; concurrency model choice; data flow; testability of seams.

## Context to gather first

Before dispatching, gather:
- Project layout: `git ls-files | head -50` then a one paragraph summary of the structure.
- Build tooling: SPM, Xcode project, both.
- Deployment target and Swift version from `Package.swift` or `.xcodeproj`.
- Whether the app is signed and notarized.
- Whether it ships to the Mac App Store or via Sparkle / direct download.

## Output format

After all ten agents return, produce a single synthesis with these sections.

### Verdict
**Ship / Hold / Block** in one sentence, with the dominant reason.

### Top 5 blockers
Ranked. Each row: severity, file:line if any, description, owning subagent, recommended action.

### Strong suggestions
Bulleted. Not blocking, but worth doing before launch. Group by area (code quality, security, perf, UX, docs).

### What was done well
Brief praise where deserved. No fluff.

### Open source readiness
Separate verdict on whether the codebase is ready to be opened. Check: LICENSE present and correct, README sufficient for a first time visitor, SECURITY policy present, no hard coded secrets or API keys, third party licenses attributed, sensitive files in .gitignore, contribution path clear.

### Next 5 commits
A concrete short list of the next five commits to make, ranked by impact, each with the subagent that recommended it.

Cite the subagent that produced each finding and the file:line where applicable. Keep the synthesis terse and structured.
