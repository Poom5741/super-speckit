---
name: agentic-interface-foundation
description: Define the product-level experience and rendering contract for AI assistants, agents, copilots, generative UI, adaptive workflows, human-in-the-loop decisions, and structured Agent-to-UI messages. Use this skill whenever a product includes conversational or autonomous actions, dynamically generated interface regions, agent progress, uncertainty, authorization, generated reports, or requests mentioning AX, GenUI, A2UI, chat UI, copilot, or agentic experience. Do not use it to make stable settings, navigation, or dashboards generative without a contextual need.
---

# Agentic Interface Foundation

Define how an Agent participates in the experience without giving it uncontrolled authority over product UI, user decisions, security, or brand expression.

Read:

- `references/genui-a2ui-principles.md`;
- `assets/AGENTIC-INTERFACE.template.md`;
- `assets/a2ui-envelope.schema.json` when a machine-readable message envelope is useful.

## Inputs

Prefer approved:

- `PRODUCT.md`, `DOMAIN.md`, and relevant feature `SPEC.md`;
- `DESIGN.md`, `CRAFT.md`, `COMPONENTS.md`, `PATTERNS.md`, and `TEMPLATES.md`;
- Agent capabilities, tool/action boundaries, permission model, data policy, and audit requirements;
- latency, streaming, failure, cancellation, retry, and rollback behavior;
- content provenance, model confidence, and human-approval policies;
- client renderer capabilities and platform constraints.

Do not design an interaction around a capability the Agent or renderer does not actually have.

## Outputs

Default outputs:

- `design/AGENTIC-INTERFACE.draft.md`;
- an adapted `design/a2ui-envelope.schema.json` when structured runtime UI is in scope;
- updates to `COMPONENTS.md`, `PATTERNS.md`, `TEMPLATES.md`, and `GAPS.md` as proposals;
- feature-level contract references inside the relevant `SPEC.md`.

The bundled schema is a neutral starting envelope, not a production protocol. Adapt, version, secure, and approve it before implementation.

## Workflow

### 1. Decide whether runtime-generated UI is justified

Use stable UI when tasks, information architecture, and decision structure are predictable. Consider GenUI when one or more of these materially vary with context:

- task path or next action;
- evidence or result structure;
- user decision and clarification needs;
- tool progress, partial results, or interruption;
- risk, authorization, uncertainty, or recovery;
- composition of heterogeneous but approved content.

Dynamic generation is not inherently more advanced. Choose the lowest freedom that still supports the user task.

### 2. Define the Agent Experience loop

For each agentic task define how the user can:

- express or refine intent;
- understand what the Agent will do;
- inspect scope, data, tools, cost, risk, and expected effects;
- authorize sensitive actions at the right moment;
- follow progress and distinguish waiting from failure;
- verify evidence, provenance, and uncertainty;
- correct assumptions or provide missing information;
- pause, cancel, retry, resume, undo, or recover where feasible;
- retain, share, or continue from the resulting artifact.

Compressing user effort must not remove their ability to evaluate and control outcomes.

### 3. Set the generation freedom

Select and justify one or a combination:

- `fixed`: known screen and components, Agent supplies content only;
- `parameterized`: known template with bounded slots and variants;
- `composed`: Agent selects from an allowlisted component/pattern catalog;
- `generated artifact`: Agent organizes a richer result under an approved schema;
- `open generation`: exceptional and separately governed.

Document why the chosen freedom is safe, testable, performant, accessible, and maintainable.

### 4. Separate declaration from rendering

The Agent may declare:

- intent and task state;
- content and data references;
- provenance, freshness, confidence, and uncertainty;
- available user actions and their semantic effect;
- whether a decision blocks further execution;
- progress, cancellation, retry, expiry, and fallback needs.

The client renderer owns:

- schema validation and version compatibility;
- mapping to allowlisted components and patterns;
- visual tokens, layout, responsive behavior, and accessibility;
- input validation, authorization binding, and action dispatch;
- safe rendering of untrusted/generated content;
- loading, error, empty, stale, unsupported, and fallback states;
- telemetry and audit records.

The Agent must not send arbitrary executable UI code as a substitute for this contract.

### 5. Define interaction surfaces

Use product-appropriate versions of:

- intent-entry surface;
- clarification or missing-context surface;
- authorization and risk-confirmation surface;
- progress and interruption surface;
- intermediate decision surface;
- result artifact with evidence and follow-up actions;
- failure, fallback, and human-escalation surface.

These are semantic roles, not mandatory branded components or page layouts.

### 6. Specify message and action safety

Define:

- protocol/schema version;
- message and task correlation;
- trusted and untrusted fields;
- content sanitization;
- action identifiers and allowlists;
- authorization scope and expiry;
- idempotency and duplicate-action handling;
- stale message and optimistic-concurrency behavior;
- audit, retention, and sensitive-data redaction;
- unknown component, schema mismatch, and client downgrade behavior.

Never treat a visible button from generated content as proof that the underlying action is authorized.

### 7. Cover lifecycle states

Map the product's domain states to interface treatment for:

- awaiting input or clarification;
- awaiting authorization;
- queued, running, streaming, or long-running;
- partial, degraded, stale, or uncertain result;
- completed;
- failed with retry or alternative;
- cancelled, expired, superseded, or rolled back.

Use the product's canonical terminology. Do not impose generic state labels if they conflict with the domain.

### 8. Validate with scenarios

Test at least:

- a routine low-risk success;
- missing context requiring clarification;
- a sensitive action requiring authorization;
- a long-running or partial result;
- failure, retry, cancellation, and stale response;
- unsupported schema/component fallback;
- keyboard, screen-reader, reduced-motion, narrow viewport, and localization behavior;
- malicious or malformed generated content.

Connect these scenarios to `EVAL.md` and the feature acceptance contract.

## Human approval gate

Require product, design, engineering, and relevant security/privacy approval for:

- generation freedom and renderer boundary;
- sensitive actions and authorization timing;
- cancellation, undo, and fallback promises;
- data exposure, provenance, and confidence representation;
- schema and action-dispatch policy;
- open-generation exceptions.

## Boundaries

- Do not turn every screen into chat or GenUI.
- Do not let the Agent choose arbitrary components, CSS, HTML, scripts, or network actions.
- Do not hide uncertainty, tool use, irreversible effects, or missing evidence.
- Do not claim undo or rollback where the system cannot provide it.
- Do not treat an A2UI envelope as a complete security protocol or implementation.
