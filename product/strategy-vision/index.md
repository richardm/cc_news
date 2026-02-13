# Product Strategy

This directory is the source of truth for product direction. It aligns everyone -- humans and agents -- on what we're building and why.

## Documents

| Document | Purpose | When to consult |
|----------|---------|-----------------|
| [vision.md](vision.md) | North Star: who we serve, what we're building, why it matters | Before starting any new feature or making architectural decisions |
| [strategy.md](strategy.md) | How we win: market positioning, competitive landscape, revenue | When evaluating trade-offs, prioritizing features, or assessing competitors |
| [roadmap.md](roadmap.md) | What's built, in progress, and planned | When planning work, checking priorities, or understanding current state |
| [principles.md](principles.md) | Operating guardrails and decision-making framework | When making technical or organizational decisions |
| [decisions.md](decisions.md) | Key decisions, rejected approaches, and rationale | Before proposing something that may have been previously considered and rejected |

## For agents

- Read `vision.md` and `principles.md` first to understand context and constraints.
- Check `decisions.md` before proposing architectural changes -- the rationale for past decisions prevents re-litigating settled questions.
- Update `roadmap.md` when features ship or priorities change.

## For the founder

- Drop rough ideas into `product/idea-inbox/` and ask an agent to process them using the `refine-product-strategy` skill.
- Review changes via `git diff` after processing.
- All documents here are living documents -- they evolve as the product evolves.
