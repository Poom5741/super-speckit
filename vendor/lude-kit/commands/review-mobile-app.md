---
description: Deep multi agent review of an iOS / Android / cross platform mobile app. Native, React Native, Flutter, or KMP.
argument-hint: "[optional: path to repo, defaults to current directory]"
---

# Mobile app deep review

Target: $ARGUMENTS (defaults to the current directory if blank).

Detect the mobile stack first (native iOS Swift, native Android Kotlin, React Native, Flutter, Kotlin Multiplatform, Capacitor, Expo). Dispatch the matching stack expert plus the generalists below.

## Detect first

- Look for `ios/`, `android/`, `package.json` with `react-native`, `pubspec.yaml`, `shared/build.gradle.kts` (KMP), `Podfile`, etc.
- Note the deployment target (App Store, Play Store, internal distribution, MDM).

## Agents to dispatch in parallel

1. `code-reviewer` plus matched stack expert (`swift-ios-expert`, `flutter-expert`, `react-native-expert`), code quality with severity labels.

2. `senior-mobile-engineer` skill, cross platform decisions, offline strategy, push notification design, deep links, store mechanics.

3. `security-reviewer`, Keychain / Keystore usage, biometric auth flow, ATS / Network Security Config, deep link validation, cert pinning, secrets in the binary, plist / manifest entitlements.

4. `debugger`, lifecycle bugs (foreground / background transitions), memory pressure on low end devices, threading bugs, push token handling edge cases.

5. `perf-investigator`, startup time, frame budget (60 / 120 fps), main thread work, image decode, list virtualization, animation cost, energy use.

6. `senior-ux-designer` skill, Apple HIG vs Material Design 3 conformance, accessibility (Dynamic Type, VoiceOver / TalkBack), localization readiness, dark mode.

7. `test-engineer`, unit, snapshot, UI test coverage; balance and CI cost.

8. `tech-writer`, README, App Store / Play Store metadata, in app help.

9. `dependency-auditor`, Pods, gradle deps, npm deps, supply chain.

10. `compliance-engineer`, App Store and Play Store policy fit, privacy nutrition label, data safety form, third party SDK transparency, age gating if applicable.

## Output format

### Verdict
**Ship / Hold / Block** in one sentence.

### Top 5 blockers
Ranked, with severity, file:line, owning subagent, recommended action.

### Store submission readiness
Quick rating per store (App Store / Play Store): signing, metadata, screenshots, privacy form, third party SDKs declared, age gate, in app purchases if any.

### Strong suggestions
Grouped by area.

### Open source readiness
LICENSE, README, SECURITY, secrets check, attributions, contribution path.

### Next 5 commits
Ranked by impact.

Cite the subagent that produced each finding. Keep it terse.
