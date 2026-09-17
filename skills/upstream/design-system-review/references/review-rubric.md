# Vibe Design foundation review rubric

## 1. Scope and provenance

- Candidate version and reviewer separation are explicit.
- Review authority is distinguished from advisory recommendation.
- Every document declares status, owner, scope and review date.
- Material rules have evidence, rationale or explicit approval.
- Inferences and unresolved gaps are labeled.
- Existing designs were treated as evidence rather than automatically canonized.
- External formats and review methods are not presented as target-product
  evidence or owner approval.

## 2. Product and domain readiness

- Target users, jobs, outcomes and non-goals are explicit.
- Canonical terminology and state meanings are stable.
- Risk, permissions, sensitive data and destructive actions are covered where relevant.
- Visual rules do not redefine business meaning.

## 3. DESIGN.md integrity

- YAML is parseable and uses the current compatible format.
- Token references resolve.
- Prose and normative tokens agree.
- Color and typography roles are defined rather than presented as raw palettes.
- Layout, depth, shapes, components and do/don't guidance are actionable.
- Contrast and accessible use are addressed.
- Unsupported Google-schema areas are handled intentionally in prose or companion documents.

## 4. Craft readiness

- The craft thesis traces to product intent, domain trust and brand direction.
- Vague adjectives are translated into observable consequences.
- Hierarchy, composition, density, content, motion, feedback, accessibility and anti-default risks are covered where relevant.
- Rules identify applicability, exceptions, evidence and evaluation destinations.
- Personal preference is not presented as a universal blocker.

## 5. Component, pattern and template readiness

- Component entries define semantics and selection boundaries.
- Required states, behavior, recovery and accessibility are documented.
- Common semantic collisions have explicit rules.
- Patterns describe adaptable task structures rather than screenshots to copy.
- Empty, loading, error, permission and responsive behavior are covered where relevant.
- Templates define shells, regions, slots, constraints, extension points and responsive transformations.
- Template provenance and maturity prevent one-off screens from becoming accidental standards.

## 6. Agentic Interface readiness when applicable

- GenUI is limited to tasks whose structure, evidence or decisions materially vary at runtime.
- The Agent declaration and client rendering responsibilities are separated.
- Authorization, provenance, uncertainty, waiting, cancellation, retry, fallback and audit are explicit.
- Components/actions are allowlisted and generated content cannot bypass validation or security boundaries.
- Stable product surfaces are not made generative for novelty alone.

## 7. Evaluation readiness

- Evidence requirements are explicit.
- Dimensions trace to foundation documents.
- Approved blockers protect critical failures from average scores; proposed
  blockers remain visibly provisional.
- Review modes distinguish maturity without changing evidence meaning.
- Failed reviews return concrete work.
- Calibration status and limitations are honest.
- Numerical scoring defines calculation, rounding, policy version and best-round comparison.

## 8. Cross-document integrity

- Product goals connect to patterns and evaluation.
- Domain meanings connect to components and content.
- Component visual roles connect to DESIGN.md.
- Craft rules connect to templates, representative artifacts and evaluation.
- Template regions connect to approved components and patterns.
- Agentic actions connect to domain authorization and renderer behavior.
- Evaluation checks return to the correct source document.
- Duplicated rules have a single authoritative source.

## 9. Visual and migration evidence

- At least two different representative artifacts exercise the proposed system when possible.
- Visual output matches declared intent and tokens.
- Update mode includes diff and downstream impact.
- Legacy values have classification and migration treatment.
- Unvalidated platforms/themes are named as limitations.
- Observed viewports and states are not promoted into support or release gates
  without an authoritative scope decision.

## Typical governed gate blockers

Use these only when an approved review contract makes them blockers. Otherwise
report them as advisory readiness limitations.

- final standards based on insufficient or unapproved evidence;
- unresolved token references or invalid document structure;
- contradictory business, component or visual rules;
- missing risk/permission treatment in a high-risk product;
- no human approval for material normalization or greenfield direction;
- hidden agent defaults presented as team decisions;
- no representative visual validation while claiming production readiness;
- evaluation contract lacks blockers or return path.
- material craft rules remain vague or untestable;
- a canonical template contradicts the primary task or responsive order;
- Agentic UI permits arbitrary rendering/actions or lacks authorization and fallback boundaries;

Reviewer separation failure is not solved by self-scoring. Leave the independent
gate pending and commission a separate reviewer.
