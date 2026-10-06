---
name: hackathon
description: Discover and validate tech or blockchain hackathon ideas using event rules, user problems, comparable prize winners, and a feasible demo scope.
---

# Hackathon idea discovery

Use this internal skill through `ask-super-speckit` when choosing a hackathon idea, comparing candidates, or validating an existing idea. Produce an evidence-backed recommendation and a buildable demo brief. Discovery alone does not create delivery state. If the user also requests implementation, carry the selected brief into the normal Super-SpecKit delivery workflow.

Read [sources and evidence](references/sources-and-evidence.md) when researching winner methods or labeling prize claims. These are winner-informed methods; this skill has no documented prize-winning deployment.

## Establish the event constraints

Read the current official event rules, judging criteria, prize tracks, deadlines with timezone, required technologies, team restrictions, prior-work policy, AI disclosure rules, and submission requirements. Cite the actual pages and record the retrieval date. Separate overall finalists, overall winners, and sponsor prize winners.

Use the event and team information already available. Ask only for missing constraints that change the recommendation, such as the event, available time, or team capabilities. Continue independent research while waiting. If no event is named, label the recommendation provisional and do not invent prize eligibility.

## Discover problems and alternatives

Start with a specific person, their costly or frustrating task, and evidence of the problem. Use customer conversations, issue reports, workflow observations, or authoritative domain sources. Distinguish observed needs from assumptions. Generate several materially different solutions when the user has not already chosen one, then narrow them against the event criteria and available build time.

For blockchain ideas, explain which requirement needs shared settlement, verifiable ownership, permissionless coordination, or another concrete blockchain property. Compare a conventional implementation. Sponsor technologies must support the user flow; do not add integrations only to accumulate bounty names.

## Study relevant projects

Search official ETHGlobal project and prize pages for blockchain events, and official organizer results or Devpost project pages for other tech events. Expand search terms into adjacent concepts and alternative vocabulary. Study projects that overlap in user, problem, or mechanism, including relevant non-winners. A close non-winner may reveal a useful gap, but its loss does not prove the idea is poor.

For each useful comparable, record the project/event, overlap, differentiated behavior, implementation or demo evidence, exact award category, and direct source links. Verify awards from organizer results or official award badges. A finalist label, repository claim, or impressive demo alone does not establish a prize win. If search or page access fails, report the coverage limitation; do not conclude no competitors exist.

Use qualitative comparisons rather than presenting invented scores as win probabilities. Explain whether a candidate has a substantiated need, a distinct contribution, natural track fit, feasible implementation, and an observable demo. Cite the evidence behind each judgment. Prior winners show what judges rewarded in that event, not a guarantee of future success.

## Recommend and scope

Recommend go, differentiate, pivot, or insufficient evidence. Explain the decisive tradeoff and the largest unresolved assumption. When choosing among ideas, include a compact comparison and why the selected idea fits this team and event.

Write a discovery brief in an existing project artifact location, or `hackathon/<event-slug>/discovery.md` when no convention exists. Include:

- Event constraints and linked judging/prize requirements, or explicit unknowns.
- Target user, problem evidence, candidate comparison, and chosen thesis.
- Relevant project comparison with verified award labels and source links.
- A single end-to-end demo journey, minimum necessary capabilities, and cut list.
- Required integrations, technical unknowns, and a time-boxed feasibility check for the riskiest dependency.
- Observable acceptance criteria mapped to the judging requirements and a submission checklist derived from the official rules.
- Recommendation, assumptions, source retrieval dates, and next action.

Scale detail to the time budget. A demo should show the claimed user outcome, with live behavior distinguished from mocked or planned behavior. Preserve event restrictions on work completed before the start. Discovery authorization does not authorize entering the competition, contacting organizers, spending money, or submitting externally.

For requested implementation, pass the brief and unresolved assumptions to `skills/ask-super-speckit/SKILL.md`. Use native specification, design, and verification stages without weakening their evidence requirements for a hackathon deadline. Mark incomplete requirements truthfully and scope the demo accordingly.
