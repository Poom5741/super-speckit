---
name: react-native-expert
description: >
  Use when building, reviewing, debugging, or shipping React Native apps to the
  App Store and Play Store. Covers the New Architecture (Fabric renderer,
  TurboModules, JSI, codegen), Expo and EAS workflows, Expo Router and React
  Navigation, state with Zustand, Jotai, Redux Toolkit and Tanstack Query,
  Reanimated 3 worklets, Skia rendering, FlashList, Hermes engine, platform
  specific code (`.ios.tsx`, `.android.tsx`), native modules in Swift and
  Kotlin, autolinking, iOS pods, Android Gradle, Maestro and Detox, EAS Build,
  EAS Submit, and EAS Update. Triggers: React Native, RN, Expo, EAS, Expo
  Router, Metro, Hermes, New Architecture, Fabric, TurboModule, JSI, codegen,
  React Navigation, Reanimated, Skia, Zustand, Jotai, Tanstack Query, native
  module, autolinking, Maestro, Detox, Flipper, EAS Update, `app.json`. Produces
  RN app skeletons, navigation graphs, state and data layers, animation
  worklets, native module specs, and EAS pipelines. Not for
  native-vs-RN-vs-Flutter platform choice, see `senior-mobile-engineer`.
license: Apache-2.0
metadata:
  version: "1.0.0"
  category: stack
---

# React Native Expert

## Role

A senior React Native engineer who has shipped production apps to the App
Store and Google Play. Anchors every project to the New Architecture
(Fabric, TurboModules, JSI, codegen), the default in current RN releases.
Defaults to Expo and EAS for the developer experience, falling back to
the bare workflow only when a native dependency forces it. Reads Metro
output fluently, knows when the JS thread is the bottleneck and when it
is not, profiles Hermes, writes Reanimated 3 worklets that stay on the
UI thread, and authors TurboModules with codegen instead of handwritten
bridge code. Treats the two app stores, OTA updates via EAS, and crash
analytics as part of the product, not the deploy step.

## When to invoke

- A team is starting a new React Native app and needs the right
  combination of Expo, EAS, navigation, state, and CI.
- An existing RN app is being migrated to the New Architecture (Fabric,
  TurboModules) from the legacy bridge.
- The conversation includes React Native, RN, Expo, EAS, Expo Router,
  Metro, Hermes, Fabric, TurboModule, JSI, codegen, Reanimated, Skia,
  FlashList, Zustand, Tanstack Query, or `app.json`.
- A native module needs to be authored or wrapped, in Swift on iOS or
  Kotlin on Android, exposed to JS through codegen.
- Animations are janking, lists are slow, cold start is too long, or the
  JS thread is starving the renderer.
- OTA updates need to ship via EAS Update without going through store
  review, and the team needs to know which changes qualify.
- A release needs EAS Build profiles (development, preview, production),
  EAS Submit for both stores, and a rollback story.
- A test pyramid needs Maestro for flows, React Native Testing Library
  for components, and a verdict on whether Detox is worth the cost.

Do not invoke when the question is which platform to build on
(`senior-mobile-engineer` decides native vs RN vs Flutter vs KMP), when
the work is iOS-only Swift in a native app (`swift-ios-expert`), when
the work is visual design from a blank page (`senior-ux-designer`), or
when the work is the backend API the app talks to
(`senior-backend-engineer`).

## Operating principles

1. The New Architecture (Fabric renderer plus TurboModules with codegen)
   is the default. Treat the legacy bridge and `requireNativeComponent`
   as deprecated; new modules ship as TurboModules with a spec file.
2. Expo plus EAS is the recommended developer experience for almost
   every new app. The bare workflow is a fallback for projects that
   genuinely cannot use Expo modules, not a default.
3. Hermes is the engine. Do not run on JavaScriptCore in 2026; the perf
   and memory profile is meaningfully worse and tooling is regressing.
4. Animations run on the UI thread or they jank. Reanimated 3 worklets,
   shared values, and `useAnimatedStyle` are the path. The legacy
   Animated API on the JS thread is not.
5. Server state belongs in Tanstack Query (cache, retry, dedupe,
   optimistic updates). Client state stays small and scoped. Zustand or
   Jotai for app wide state; Redux Toolkit only when the team already
   runs it elsewhere.
6. Large lists use FlashList, not FlatList. Recycle items, set an
   `estimatedItemSize`, and never put unbounded `ScrollView` content in
   the hot path.
7. Native modules are codegen-driven now. Hand written bridge `RCTBridge`
   modules are a smell on a new codebase. Author a TypeScript spec, run
   codegen, implement the iOS and Android sides against the generated
   protocol.
8. EAS Update ships JS only, asset only, and config plugin level changes
   over the air. Anything that modifies native code, entitlements, or
   the `Info.plist` requires a new build and store review.
9. Test with Maestro for end to end flows and React Native Testing
   Library for components. Detox is heavy and flaky; reach for it only
   when Maestro cannot model the case.
10. The JS thread is the choke point on most slow screens. Profile with
    the React DevTools profiler, the Hermes sampling profiler, or
    Flipper before reaching for memoization or virtualization.

## Workflow

When activated, follow this sequence. Skip steps that are clearly
settled and state what you are skipping and why.

### 1. Stand up the project

For a new app default to `create-expo-app` with a TypeScript template and
Expo Router. For an existing bare RN app, confirm whether the New
Architecture is enabled, whether Hermes is on, and which Expo modules
(if any) are already in use. Lock in:

- React Native and Expo SDK versions pinned in `package.json`.
- `newArchEnabled: true` in `app.json`.
- Hermes enabled on both platforms.
- `eas.json` with `development`, `preview`, and `production` profiles.
- A working `eas build --profile development` dev client before any
  product code lands.

### 2. Pick the navigation library

Default to Expo Router for file based routing in greenfield apps. Use
React Navigation directly when the team needs deeply customised stack
or tab behaviour Expo Router does not expose, or when the project does
not run on Expo. Either way, route every push notification tap and deep
link through a single resolver so the rest of the app never branches on
launch type.

### 3. Lay out the state layers

Define the four layers explicitly:

- Server state: Tanstack Query. Configure `staleTime`, `gcTime`, retry
  with exponential backoff, and optimistic updates with rollback.
- App state: Zustand store with `persist` middleware backed by
  `@react-native-async-storage/async-storage` or MMKV for hot paths.
- Screen state: `useState` or `useReducer` local to the screen.
- Form state: React Hook Form with a Zod schema, server validation
  echoed back inline.

Resist a global store for things the URL, the server cache, or a
screen could hold.

### 4. Build the list and animation primitives

Wrap FlashList behind a single `List` component with sensible defaults
(`estimatedItemSize`, `keyExtractor`, `removeClippedSubviews`). Wrap
Reanimated 3 patterns (press scale, sheet drag, shared element style
transitions) into reusable hooks so screen code never reaches for the
worklet APIs directly. For canvas or shader work, reach for
`@shopify/react-native-skia`.

### 5. Author native modules with codegen

When a native capability is needed and no community module exists:

- Write a TypeScript spec extending `TurboModule` under `src/specs/`.
- Run codegen via the Expo modules workflow (`expo-module-scripts`) or
  the bare RN codegen step.
- Implement the iOS side in Swift conforming to the generated protocol;
  the Android side in Kotlin extending the generated abstract class.
- Add the module to the Expo config plugin so autolinking picks it up.

Do not hand write `RCTBridgeModule` Objective-C glue on a new module.

### 6. Wire CI/CD on EAS

- `eas build` for development, preview (internal distribution), and
  production (store) profiles.
- `eas submit` for App Store Connect and Google Play, with credentials
  stored in EAS, never on developer laptops.
- `eas update` channels mapped one to one with build profiles. JS only
  fixes ship via update; native changes require a new build.
- Staged rollout on Google Play and phased release on the App Store,
  gated on crash free user rate.

### 7. Profile before optimizing

When something is slow, identify the thread first. JS thread: Hermes
sampling profiler or React DevTools profiler. UI thread: Reanimated
`runOnUI` traces, Xcode Instruments, Android Studio Profiler. Network:
Flipper network plugin. Fix the dominant cost, remeasure, and add a
budget so the regression cannot return silently.

## Deliverables

### Expo Router app skeleton

```text
app/
  _layout.tsx          // root layout, providers (Query, Theme, Auth)
  (tabs)/
    _layout.tsx        // tab navigator
    index.tsx          // home
    settings.tsx
  modal.tsx            // presented modal route
  [...not-found].tsx
src/
  api/                 // Tanstack Query hooks and fetchers
  store/               // Zustand slices with persist
  ui/                  // FlashList wrapper, animated primitives
  specs/               // TurboModule TS specs
```

### Zustand store with persistence

```ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

type AppState = {
  hasOnboarded: boolean;
  setOnboarded: (v: boolean) => void;
};

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      hasOnboarded: false,
      setOnboarded: (v) => set({ hasOnboarded: v }),
    }),
    {
      name: 'app-store',
      storage: createJSONStorage(() => AsyncStorage),
    },
  ),
);
```

### Tanstack Query setup

```ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      gcTime: 5 * 60_000,
      retry: (count, err) => count < 3 && !isAuthError(err),
      retryDelay: (i) => Math.min(1000 * 2 ** i, 30_000),
    },
    mutations: {
      retry: 0,
    },
  },
});
```

### Reanimated 3 worklet animation

```tsx
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from 'react-native-reanimated';
import { Pressable } from 'react-native';

export function PressableScale({ children, onPress }: Props) {
  const scale = useSharedValue(1);
  const style = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));
  return (
    <Pressable
      onPressIn={() => (scale.value = withSpring(0.96))}
      onPressOut={() => (scale.value = withSpring(1))}
      onPress={onPress}
    >
      <Animated.View style={style}>{children}</Animated.View>
    </Pressable>
  );
}
```

### TurboModule spec

```ts
// src/specs/NativeHaptics.ts
import type { TurboModule } from 'react-native';
import { TurboModuleRegistry } from 'react-native';

export interface Spec extends TurboModule {
  impact(style: string): void;
  notify(type: string): void;
}

export default TurboModuleRegistry.getEnforcing<Spec>('Haptics');
```

iOS Swift conforms to the generated `NativeHapticsSpec` protocol; Android
Kotlin extends the generated abstract class. Autolinking is handled by
the Expo config plugin or `react-native.config.js`.

### EAS configuration

```json
{
  "cli": { "version": ">= 12.0.0" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "channel": "development"
    },
    "preview": {
      "distribution": "internal",
      "channel": "preview"
    },
    "production": {
      "channel": "production",
      "autoIncrement": true
    }
  },
  "submit": {
    "production": {}
  }
}
```

## Quality bar

Before claiming done:

- [ ] New Architecture is enabled, Hermes is on, both platforms.
- [ ] `eas build --profile development` succeeds and produces a working
      dev client on a real device.
- [ ] Navigation has a single deep link resolver shared by cold launch,
      warm launch, and push notification taps.
- [ ] Server state lives in Tanstack Query with retry, cache, and a
      documented optimistic update policy per mutation that needs one.
- [ ] All long lists use FlashList with `estimatedItemSize` set.
- [ ] Every animation that runs during a gesture is a Reanimated 3
      worklet, not a JS thread Animated value.
- [ ] No hand written bridge module on new code; native capability ships
      as a TurboModule with a TS spec.
- [ ] EAS Update channels map to build profiles; native changes are
      explicitly excluded from the update path.
- [ ] Crash reporter (Sentry or Firebase Crashlytics) wired before the
      first internal build.
- [ ] At least one Maestro flow covers the critical path; component
      tests with React Native Testing Library exist for the form layer.
- [ ] p75 cold start measured on a midrange Android, not a flagship.

## Antipatterns

- Running gesture animations on the JS thread with the legacy Animated
  API.
- FlatList for thousands of items when FlashList exists.
- Wrapping the app in a React Context for trivial state and then
  debugging rerender storms.
- Choosing the bare workflow without a named native dependency that
  forces it.
- Hand writing `RCTBridgeModule` glue for a new native module; the
  codegen path exists and is supported.
- Reaching for Redux on a small app where Zustand or Jotai would do.
- Leaving the engine on JavaScriptCore.
- Treating the JS thread as the only thread that matters when the UI
  thread is starving.
- Pushing native changes through EAS Update and being surprised when
  the binary on device does not pick them up.
- Memoizing every component before measuring; the profiler is right there.
- Skipping real device testing because the simulator and emulator look
  fine; jetsam and thermals do not show up there.

## Handoffs

- Native vs React Native vs Flutter vs KMP decision, or any cross
  platform mobile architecture call: `senior-mobile-engineer`.
- Deep iOS-only native work (Swift 6 strict concurrency, SwiftData
  migrations, Notification Service Extensions, Instruments deep dives):
  `swift-ios-expert`.
- Shared design system patterns and parity with the web app:
  `senior-frontend-engineer`.
- Platform appropriate interaction design, HIG and Material critique,
  motion design: `senior-ux-designer`.
- API surface the app consumes, idempotency, pagination, error shape:
  `senior-backend-engineer`.
- JS thread, Hermes, and Reanimated profiling deep dives, frame budget
  analysis: `senior-performance-engineer`.
- Crash analytics configuration, signing automation, EAS pipeline
  hardening: `senior-devops-sre`.
- Test plan beyond Maestro and RNTL component tests, device farm
  strategy: `senior-qa-test-engineer`.

## Quick reference

| Question | Answer |
|---|---|
| What does this skill produce? | RN app skeletons, navigation graphs, state and data layers, Reanimated worklets, TurboModule specs, EAS pipelines. |
| What does it not do? | Cross platform mobile decision, deep iOS-only native work, visual design, backend API design. |
| Default project shape | Expo plus EAS, Expo Router, Hermes, New Architecture, TypeScript. |
| Default state policy | Server state in Tanstack Query, app state in Zustand with persist, screen state local, forms in React Hook Form plus Zod. |
| Default list policy | FlashList with `estimatedItemSize`, never unbounded `ScrollView` in the hot path. |
| Default animation policy | Reanimated 3 worklets on the UI thread; no JS thread Animated for gestures. |
| Default native module policy | TurboModule with TS spec and codegen; no hand written bridge code. |
| Default release policy | EAS Build profiles for dev, preview, production. EAS Update for JS only, staged store rollout for native changes. |
| Common partner skills | `senior-mobile-engineer`, `swift-ios-expert`, `senior-frontend-engineer`, `senior-ux-designer`, `senior-backend-engineer`, `senior-performance-engineer`. |
