# GenUI and A2UI principles

Primary source:

- Vibe Designing Playbook, From UX to AX: https://alibaba-cloud-design.github.io/vibe-designing-playbook/#sec-2.1
- Vibe Designing Playbook, GenUI: https://alibaba-cloud-design.github.io/vibe-designing-playbook/#sec-2.2
- Vibe Designing Playbook, A2UI: https://alibaba-cloud-design.github.io/vibe-designing-playbook/#sec-2.3
- Vibe Designing Playbook, runtime interaction examples: https://alibaba-cloud-design.github.io/vibe-designing-playbook/#sec-2.4

## Transferable principles

1. Agentic products reduce the effort required to execute steps, but they can increase the effort required to judge whether the result is correct.
2. Dynamic UI is justified by changing intent, context, task state, evidence, or decision needs—not by novelty alone.
3. The Agent declares what needs to be communicated and what actions are semantically available.
4. The client controls how that declaration is validated and rendered through approved components, tokens, interaction rules, accessibility, and fallbacks.
5. Users need visible opportunities to understand, authorize, verify, correct, stop, and recover.
6. Generated results should preserve evidence and offer appropriate next actions rather than presenting unsupported certainty.

## Freedom versus control

Higher expressive freedom can cover more contexts, but it increases validation, security, performance, accessibility, brand, and predictability risk. Prefer fixed or parameterized surfaces for stable tasks; use controlled composition when runtime variation materially improves comprehension or action.

## Common failure modes

- adding a chat box without redesigning delegation and evaluation;
- allowing generated content to imply authorization;
- hiding tool progress or presenting waiting as failure;
- presenting model confidence as factual probability without calibration;
- letting arbitrary UI code bypass component and security boundaries;
- losing task context after a user decision;
- making cancellation visible but ineffective;
- generating a report without evidence provenance or follow-up actions.
