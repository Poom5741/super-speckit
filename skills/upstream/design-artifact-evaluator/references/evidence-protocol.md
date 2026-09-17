# Evidence collection protocol

Primary inspiration:

- Vibe Designing Playbook, evidence chain: https://alibaba-cloud-design.github.io/vibe-designing-playbook/#sec-3.3
- Vibe Designing Playbook, delivery gate: https://alibaba-cloud-design.github.io/vibe-designing-playbook/#sec-3.4

Adapt the protocol to the project’s approved `EVAL.md`, platform, and safe test environment.

## 1. Evidence manifest

Record:

- artifact/version;
- environment and account/fixture;
- timestamp;
- viewport/device, theme, locale, zoom, input modality;
- feature flags and authentication state;
- path/state represented;
- collection tool and known limitations.

## 2. DOM, layout, and accessibility facts

Check applicable deterministic facts:

- horizontal or fixed-position overflow;
- clipped, occluded, or unreadable content;
- missing accessible names and invalid semantic relationships;
- keyboard reachability, focus visibility, order, and traps;
- contrast and non-color cues;
- target size and spacing;
- broken images/resources and layout shifts;
- zoom/reflow and responsive breakpoints;
- reduced-motion behavior;
- landmark, heading, label, error, and status semantics.

Automated checks can miss product meaning and dynamic states. Record what was actually inspected.

## 3. Page/content profile

Inventory:

- major regions and reading order;
- headline, primary task, primary CTA, navigation, and exits;
- forms, tables, charts, links, dialogs, overlays, and interactive targets;
- placeholder/dead links and invented data;
- source, timestamp, unit, confidence, and sensitive-data treatment;
- normal and non-ideal states exposed.

## 4. Interaction smoke

Follow the feature spec’s critical path and representative recovery path. Record:

- initial state and action;
- expected system response;
- actual visible feedback;
- console/page/resource errors;
- focus movement and keyboard behavior;
- cancellation, retry, undo, or recovery;
- resulting state and data side effect.

Use safe fixtures. Do not trigger irreversible or externally visible actions without explicit authorization.

## 5. Screenshot/device evidence

Capture enough context to assess:

- text readability;
- visual hierarchy and attention order;
- composition, density, and responsive transformation;
- brand/product fit;
- state and feedback visibility;
- motion purpose where capture supports it.

Name captures by viewport, path, state, and round. Include focused/expanded/error states when they carry essential behavior.

## 6. Evidence conflicts

Resolve according to the claim:

- for what the user can visually perceive, rendered/device evidence has priority over source structure;
- for semantic exposure to assistive technology, accessibility tree/DOM and real assistive testing matter;
- for behavior, actual interaction result and system state matter;
- for business truth, authoritative domain/data evidence matters.

Do not use one evidence type to answer a question it cannot observe.

## 7. Sufficiency

Evidence is insufficient when a required state, path, viewport, permission, or modality was not available or the environment is not representative. Mark the limitation and apply the project’s missing-evidence policy.
