# Google DESIGN.md format summary

Last checked against the official repository on 2026-07-17.

- Repository: https://github.com/google-labs-code/design.md
- Specification: https://github.com/google-labs-code/design.md/blob/main/docs/spec.md
- Status at last check: `alpha`

Verify the upstream specification when possible. This bundled file is a working summary, not a replacement for the official source.

## Purpose

`DESIGN.md` is a plain-text representation of visual identity for humans and coding agents. It combines:

1. optional YAML front matter containing normative machine-readable tokens;
2. Markdown sections containing human-readable rationale and usage guidance.

## Core YAML shape

```yaml
---
version: alpha
name: Example system
description: Optional description
colors:
  primary: "#000000"
typography:
  body-md:
    fontFamily: Example Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
rounded:
  sm: 4px
spacing:
  sm: 8px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 12px
---
```

Token references use `{path.to.token}` syntax.

## Canonical Markdown section order

1. `## Overview` or `## Brand & Style`
2. `## Colors`
3. `## Typography`
4. `## Layout` or `## Layout & Spacing`
5. `## Elevation & Depth` or `## Elevation`
6. `## Shapes`
7. `## Components`
8. `## Do's and Don'ts`

Sections may be omitted if irrelevant. Unknown headings are preserved by the format, but the team should prefer companion documents for product, domain, behavior and evaluation rules to keep `DESIGN.md` portable.

## Current component-token properties

- `backgroundColor`
- `textColor`
- `typography`
- `rounded`
- `padding`
- `size`
- `height`
- `width`

Component semantics, complex behavior and business meaning require companion documentation.

## Official CLI

```bash
npx @google/design.md lint DESIGN.md
npx @google/design.md diff DESIGN-old.md DESIGN.md
npx @google/design.md export --format dtcg DESIGN.md
npx @google/design.md export --format css-tailwind DESIGN.md
npx @google/design.md spec
```

The official linter covers structural findings such as broken references, missing primary/typography values, contrast, orphaned tokens, section order and likely unknown-key typos. Passing lint does not prove that the design direction is coherent or appropriate for users.
