# Extract mode: reconstruct from existing designs

Use when a product has meaningful design evidence but no trustworthy visual source of truth.

## Process

1. Inventory sources and record their authority, date and scope.
2. Extract visual values from design tools, code and representative screenshots.
3. Group values by role, not only by literal similarity.
4. Identify repeated patterns, deliberate exceptions, conflicts and isolated legacy values.
5. Compare design-tool values with production implementation.
6. Propose a normalized system with migration impact.
7. Ask the design owner to approve material choices.
8. Draft and validate `DESIGN.md`.

## Required audit categories

- visual intent and brand expression;
- color values and semantic roles;
- typography families, roles and scale;
- spacing, grid, density and breakpoints;
- radii, surfaces, borders and elevation;
- component visual variants and states;
- iconography, imagery, charts and motion where evidenced;
- accessibility and contrast;
- differences between source design and production.

## Classification

For each extracted pattern classify it as:

- `candidate standard`;
- `deliberate exception`;
- `needs normalization`;
- `legacy/deprecated`;
- `unresolved`.

Do not average conflicting values or select the most frequent value without explaining its role and consequences.
