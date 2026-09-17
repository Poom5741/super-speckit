---
version: alpha
name: "[Design system name]"
description: "[What product and platforms this visual system covers]"
colors:
  primary: "[CSS color]"
typography:
  body-md:
    fontFamily: "[Font family]"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
rounded:
  sm: 4px
spacing:
  sm: 8px
components: {}
---

# [Design system name]

## Overview

Describe the visual thesis, audience, emotional response, density and category posture. Reference `design/PRODUCT.md` rather than duplicating the full product definition.

## Colors

Describe semantic color roles, hierarchy, contrast, themes and deliberate limits. Every normative value must match the YAML tokens.

## Typography

Describe font roles, language priorities, hierarchy, numeric behavior, fallback strategy and readability requirements.

## Layout

Describe grid, content widths, density, spacing rhythm, responsive posture and touch-target expectations. Keep exact spacing values aligned with YAML tokens.

## Elevation & Depth

Describe how hierarchy is expressed through surfaces, borders, tonal layers or shadows.

## Shapes

Describe corner-radius roles, container relationships, control shapes and when full rounding is appropriate.

## Components

Describe visual properties for key components. Keep semantic meaning and behavioral rules in `design/COMPONENTS.md`.

## Do's and Don'ts

- Do [observable, actionable rule].
- Don't [observable anti-pattern and why].
