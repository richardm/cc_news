# Strategy Document Templates

These templates define the expected structure for each document in `product/strategy-vision/`. Use them when bootstrapping new documents or when adding new sections.

Each template shows the section headers and a brief description of what belongs in each section.

---

## index.md

```markdown
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
```

---

## vision.md

```markdown
# Vision

## Target User

Who is the primary user? What is their role, context, and level of technical sophistication?

## Pain Points

What specific problems does the user face today? Why are existing solutions insufficient?

## Product Purpose

Why does this product exist? What is the core value proposition in one sentence?

## What Success Looks Like

What does the world look like when this product succeeds? Describe the end state.

## Beliefs About the Future

What do we believe about the future that makes this the right product to build now? What trends or shifts are we betting on?

## Non-Goals

What are we explicitly not trying to do? What adjacent problems will we intentionally ignore?

## Failed or Rejected Approaches

What approaches have we tried or considered and abandoned? Why didn't they work?
```

---

## strategy.md

```markdown
# Strategy

## Mission

What is our mission in one sentence?

## Market Positioning

Where do we sit in the market? Who are we compared to alternatives?

## Competitive Landscape

Who else is solving similar problems? What are their strengths and weaknesses? How do we differentiate?

## Differentiation

What is our unique advantage? Why would users choose us over alternatives?

## Revenue Model

How do we plan to make money (if applicable)? What is the business model?

## Go-to-Market

How do we reach our target users? What channels, partnerships, or strategies will we use?
```

---

## roadmap.md

```markdown
# Roadmap

## Shipped

Features and capabilities that are live and usable today.

| Feature | Description | Date shipped |
|---------|-------------|-------------|

## In Progress

Features currently being built.

| Feature | Description | Status |
|---------|-------------|--------|

## Planned

Features we intend to build, roughly in priority order.

| Feature | Description | Priority | Rationale |
|---------|-------------|----------|-----------|

## Backlog

Ideas that are worth tracking but not yet prioritized.

- (none yet)
```

---

## principles.md

```markdown
# Operating Principles

These principles guide decision-making across the project. When in doubt, consult these before making trade-offs.

## Technical Principles

- (To be defined based on founder input)

## Organizational Principles

- (To be defined based on founder input)

## Decision-Making Framework

When facing a trade-off, apply these principles in order of priority:

1. (To be defined)
```

---

## decisions.md

```markdown
# Decisions Log

A record of key decisions, what was considered, and why we chose the path we did. This is institutional memory -- consult it before proposing changes to settled questions.

## How to read this log

Each entry follows this format:

- **Date**: When the decision was made
- **Decision**: What we decided
- **Context**: What problem or question prompted this
- **Options considered**: What alternatives were evaluated
- **Rationale**: Why we chose this option
- **Rejected alternatives**: What we didn't choose and why

---

(No decisions logged yet.)
```
