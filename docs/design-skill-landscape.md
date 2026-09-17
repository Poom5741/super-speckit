# Frontend-design skill landscape

Research date: 2026-09-18. This is a discovery list, not an endorsement or permission to install every entry. Skills are executable instructions; inspect the source, exact revision, and license before use in a sensitive project.

| # | Skill / repository | Primary strength | License signal | Super-SpecKit fit |
| --- | --- | --- | --- | --- |
| 1 | [Anthropic `frontend-design`](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design) | Opinionated art direction and non-generic implementation | Skill points to `LICENSE.txt`; upstream terms must travel with copied source | Best baseline visual craft skill |
| 2 | [PaulRBerg `frontend-design`](https://github.com/PaulRBerg/agent-skills/tree/main/skills/frontend-design) | Existing-system-first, accessibility, rendered-browser verification | Repository MIT; verify exact source before vendoring | Strong build/review complement |
| 3 | [nick3 `vibe-design-skills`](https://github.com/nick3/vibe-design-skills) | 12-skill governed product/design workflow with independent evaluator | MIT | Best design-first/design-governance suite |
| 4 | [JezWeb `design-loop`](https://github.com/jezweb/claude-skills/tree/main/plugins/frontend/skills/design-loop) | Persistent `DESIGN.md`, site memory, and baton handoffs | Inspect before installation | Useful long-running website loop |
| 5 | [Firzus `frontend-design`](https://github.com/Firzus/agent-skills/tree/main/skills/web/frontend-design) | Three-phase system → greybox → real-content artifact pipeline | Inspect before installation | Very close to HTML-first workflow |
| 6 | [JuliusBrussee `interface-kit`](https://github.com/JuliusBrussee/skills/tree/main/skills/interface-kit) | Accessible, performant UI implementation after a `DESIGN.md` | Inspect before installation | Implementation/craft companion |
| 7 | [osmontero `designing-frontend-interfaces`](https://github.com/osmontero/opencode-skills/tree/main/skills/designing-frontend-interfaces) | Choose a locked visual system before components | Skill references `LICENSE.txt` | Art-direction alternative |
| 8 | [KilimiaoSix `frontend-design-codex`](https://github.com/KilimiaoSix/frontend-design-codex-skill) | Codex-specific design brief, image concepting, browser verification | Inspect before installation | Codex-targeted implementation option |
| 9 | [dachent `frontend-design-codex`](https://github.com/dachent/skills/tree/main/frontend-design-codex) | Rendered behavior/screenshot evidence, responsive/accessibility review | Inspect before installation | Strong QA bridge |
| 10 | [PracticalSwan `frontend-design`](https://github.com/PracticalSwan/agent-skills/tree/main/frontend-design) | Context-fit UI, complete states, accessibility as hard gates | MIT AND Apache-2.0 | Broad production alternative |
| 11 | [AnswerZhao `frontend-design`](https://github.com/AnswerZhao/agent-skills/tree/main/glm-skills/frontend-design) | Formal token system and reusable code/templates | MIT | Design-system oriented option |
| 12 | [Firstp1ck `pi-skill-frontend-design`](https://github.com/Firstp1ck/pi-coding-agent-forge/tree/main/pi-skill-frontend-design/skills/frontend-design) | Portable frontend-design package | Apache-2.0 | Lightweight portable option |
| 13 | [hueyexe `frontend-agent-skills`](https://github.com/hueyexe/frontend-agent-skills) | Specialized visual-composition and UX/UI skills | Inspect before installation | Potential specialist source |
| 14 | [sapsapshen `ui-ux-design`](https://github.com/sapsapshen/ui-ux-design) | Multi-artifact UI/UX agent package | Inspect before installation | Broader UI/UX alternative |
| 15 | [Krishna-Modi12 `frontend-design-pro`](https://github.com/Krishna-Modi12/frontend-design-pro) | Router/catalog for components, a11y, data tables, 3D, and design systems | Inspect before installation | Large toolkit; avoid wholesale install initially |

## Recommended non-conflicting stack

Do **not** install every skill above: many share the same `frontend-design` name and give contradictory aesthetic instructions. The practical stack is:

1. **Foundation/design workflow:** nick3 `vibe-design-skills`—use its design foundation, feature spec, and independent evaluator capabilities.
2. **Visual craft:** Anthropic `frontend-design`—the already copied upstream skill; pinned source metadata belongs beside it.
3. **Rendered evaluation:** PaulRBerg `frontend-design` *or* dachent `frontend-design-codex`, evaluated in a distinct checker context. Choose one after checking exact licenses and repository health.
4. **Super-SpecKit-owned code:** only the HTML-first bridge, state/evidence binding, and policy routing. It should call upstream skills rather than reimplement their design doctrine.

This separates designer, maker, and evaluator while avoiding three artistic directors issuing instructions to the same maker.

## Verification before adoption

- Pin repository URL, commit SHA, skill path, and license in a source manifest.
- Inspect every bundled script/reference, not merely `SKILL.md`.
- Install into a disposable fixture first; run the source’s stated validations if available.
- Test a representative UI brief against a real local design system and inspect desktop/mobile screenshots.
- Record whether the skill is a generator, a design-system author, or evaluator. A skill should not certify its own generated design.
