# Examples: Inbox to Strategy

These examples show how rough inbox notes get synthesized into strategy document updates.

---

## Example 1: Simple feature idea

### Inbox note (`2026-02-10-warc-filtering.md`)

```
We need a way to filter WARC records by content type. Users are drowning in
irrelevant records. HTML-only filtering would save them hours.
```

### Strategy documents updated

**roadmap.md** -- Added to Planned:

```markdown
| WARC content-type filtering | Filter records by content type (e.g. HTML-only) to reduce noise | High | Users waste hours sifting through irrelevant record types |
```

**vision.md** -- Added to Pain Points (if not already captured):

```markdown
- Users spend excessive time sifting through irrelevant WARC records because there is no way to filter by content type before processing.
```

### Change summary presented to user

> **roadmap.md**: Added "WARC content-type filtering" to Planned (High priority). Rationale: reduces time users spend on irrelevant records.
>
> **vision.md**: Added content-type filtering pain point under Pain Points (new).
>
> No contradictions. Archived `2026-02-10-warc-filtering.md`.

---

## Example 2: Strategic direction change

### Inbox note (`2026-02-12-local-first.md`)

```
I've been thinking more about this. We should be local-first. No cloud
dependencies. Users should be able to run everything on their own machine
with no internet connection after the initial download.

This is a shift from earlier thinking where we considered a hosted API.
```

### Strategy documents updated

**principles.md** -- Added to Technical Principles:

```markdown
- **Local-first**: All functionality must work offline after initial setup. No cloud dependencies. Users run everything on their own machine.
```

**decisions.md** -- New entry:

```markdown
## Local-first architecture

- **Date**: 2026-02-12
- **Decision**: Adopt a local-first architecture with no cloud dependencies.
- **Context**: Early discussions considered a hosted API, but the founder determined that offline capability and user autonomy are higher priorities.
- **Options considered**: (1) Hosted API with cloud processing, (2) Hybrid local + cloud, (3) Fully local-first.
- **Rationale**: Users should own their workflow without internet dependency. Reduces operational complexity and aligns with the target user's preference for control.
- **Rejected alternatives**: Hosted API -- adds operational burden, creates internet dependency, conflicts with user autonomy goals.
```

**strategy.md** -- Updated Differentiation:

```markdown
- Fully local-first: unlike cloud-based alternatives, users maintain complete control and can work offline.
```

### Change summary presented to user

> **principles.md**: Added "Local-first" technical principle -- no cloud dependencies, full offline capability.
>
> **decisions.md**: Logged decision to adopt local-first architecture. Noted the shift away from the previously considered hosted API approach.
>
> **strategy.md**: Added local-first as a differentiation point.
>
> **Contradiction resolved**: Earlier discussions considered a hosted API (no formal doc entry existed). This note explicitly supersedes that direction. Logged in decisions.md.
>
> Archived `2026-02-12-local-first.md`.

---

## Example 3: Ambiguous note requiring clarification

### Inbox note (`2026-02-12-pricing.md`)

```
Maybe freemium? Or maybe just open source the whole thing. Not sure yet.
Need to think about this more.
```

### Strategy documents updated

**strategy.md** -- Updated Revenue Model with clarification callout:

```markdown
## Revenue Model

> [!NOTE] Needs clarification: The founder is considering either a freemium model or fully open-sourcing the project. No decision has been made yet. Revisit when the founder has a clearer direction.
```

### Change summary presented to user

> **strategy.md**: Added note under Revenue Model flagging the open question (freemium vs. full open source). No changes made to other documents -- waiting for clearer direction.
>
> Archived `2026-02-12-pricing.md`.
