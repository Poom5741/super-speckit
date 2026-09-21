# Premium UI skill stack

Super-SpecKit now ships a deliberately layered UI stack. More skills do not mean more simultaneous instructions: `design-first` picks only the smallest set needed for the specific feature, records the decision, and leaves rendered approval to an independent checker.

| Layer | Skills | Use for |
| --- | --- | --- |
| Product and feature foundation | `product-design-context`, `vibe-design-bootstrap`, `feature-design-spec`, `vibe-design-execute` | The product context, user flow, and design decision before implementation. |
| Premium visual direction | `ui-ux-pro-max`, Anthropic `frontend-design`, `ui-visual-composition` | One differentiated visual thesis; type, color, density, token, motion, and composition choices. |
| Interaction and information | `interaction-patterns-components`, `information-architecture-navigation`, `forms-inputs-checkout`, `ux-usability-foundations` | Components, navigation, task flows, forms, feedback, and recovery. |
| Inclusion and content | `accessibility-inclusive-design`, `ux-writing-content-design` | Keyboard/semantic/reduced-motion behavior and meaningful labels, errors, empty states, and CTAs. |
| Reusable systems | `design-system`, `design-systems-frontend-architecture`, `design-system-foundation`, `design-template-and-variants` | Tokens, component contracts, responsive rules, and reusable page patterns. |
| Evidence and independent review | PaulRBerg `frontend-design`, `design-artifact-evaluator`, `design-system-review` | Rendered desktop/mobile/state inspection by a checker independent of the UI maker. |
| Discovery, only when uncertainty matters | `ux-research-discovery-testing` | Lightweight research or usability-test planning before a UI decision that would otherwise be guesswork. |

## The premium rule

For a net-new UI surface, generate one UI/UX Pro Max design-system recommendation and turn it into a one-sentence visual thesis. Then use at most the specialist skills relevant to the feature. A dashboard may combine composition, interaction, information architecture, and accessibility; a checkout may combine forms, content, interaction, and accessibility. Neither should mix arbitrary catalog styles or discard the project’s established design system.

## Non-negotiable release rule

Premium is a claim about observed quality, not source code aesthetics. The independent checker must still inspect the running UI at relevant viewport sizes, states, keyboard paths, and changed interactions; capture evidence; and mark unverified items honestly.
