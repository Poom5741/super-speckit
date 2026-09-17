# Update mode: revise an approved system

Use when an approved `DESIGN.md` exists and a product, platform, theme, component or brand change requires revision.

## Process

1. Preserve the current approved file.
2. Identify the change request and its evidence.
3. Determine whether the change is a system rule, project exception or implementation bug.
4. Trace affected tokens, components, patterns and representative screens.
5. Draft the smallest coherent system change.
6. Run lint and diff when the official CLI is available.
7. Show visual and migration impact.
8. Require approval before replacement.

## Regression questions

- Does the change break token references?
- Does it reduce contrast or accessibility?
- Does it create a second value for an existing semantic role?
- Does it invalidate component or pattern documentation?
- Does it require code/Figma migration?
- Does it affect light/dark, density or responsive variants?
- Does it make prior approved examples misleading?

Record the decision, migration owner and effective version.
