---
name: refine-product-strategy
description: Process product idea notes from the inbox and update strategy documents. Use when the user asks to process product ideas, refine strategy, update product vision, review the idea inbox, or mentions product direction.
---

# Refine Product Strategy

Process the founder's rough notes from `product/idea-inbox/` and synthesize them into the structured strategy documents in `product/strategy-vision/`.

## When to use this skill

- The user asks to "process my ideas", "refine strategy", or "update product vision"
- The user mentions the idea inbox or strategy documents
- The user drops notes into `product/idea-inbox/` and wants them incorporated

## Workflow

### Step 1: Read the inbox

1. List all `.md` files in `product/idea-inbox/` (exclude the `processed/` subdirectory and `.gitkeep`).
2. Sort by file modification time, **oldest first**. More recent notes reflect the founder's latest thinking and take precedence on conflicts.
3. If the inbox is empty, inform the user and stop.

### Step 2: Check strategy documents

Read all documents in `product/strategy-vision/`.

If the directory does not exist or is missing documents, **bootstrap** before proceeding:

1. Read project context: `README.md`, `AGENTS.md`, `pyproject.toml`, and any existing code or notebooks.
2. Read the templates in `templates.md` (in this skill's directory) for the expected document structure.
3. Create each missing document using the template, populated with content inferred from the codebase.
4. For sections where no information can be inferred, use the placeholder: `> [!NOTE] To be defined.`

### Step 3: Analyze notes and draft updates

For each inbox note:

1. Identify which strategy documents are affected (a single note may touch multiple documents).
2. **Feature and API inventory** (critical for notes containing feature proposals):
   - Extract every distinct feature, CLI command, function name, API signature, and use case from the note into a flat list.
   - For each item, find its closest match in the existing roadmap (Shipped, In Progress, Planned, or Backlog).
   - If an item has no 1:1 match, it must be added to the roadmap. Do not assume an existing entry covers it unless the match is exact.
   - If an item matches an existing entry but the note provides additional detail (parameter signatures, behavioral specifics, output formats, performance expectations), enrich the existing entry with that detail.
   - Present this mapping as part of your analysis before drafting updates, so gaps are visible.
3. Draft the updates. Follow the **update principles** below.
4. When a note contradicts existing strategy content, the **note wins** -- it reflects newer thinking.

### Step 4: Apply updates and present summary

1. Apply the drafted changes directly to the strategy documents in `product/strategy-vision/`.
2. Present a concise change summary to the user, organized by document:
   - Which documents were updated
   - What changed and why (1-2 sentences per document)
   - Any contradictions that were resolved (noting what was replaced)
   - Any ambiguities flagged with `[!NOTE]` callouts

This is a CEO-level review -- keep it concise and decision-oriented.

### Step 5: Archive processed notes

Move each processed note from `product/idea-inbox/` to `product/idea-inbox/processed/`, preserving the original filename. Use `git mv` (shell) or equivalent.

The founder can always reference archived notes there or via git history.

## Update Principles

Apply these principles when modifying strategy documents:

- **Additive by default**: New ideas extend existing strategy. Do not remove or replace existing content unless the note explicitly says to.
- **Recency wins**: When notes conflict with existing docs, the more recent note takes precedence. Note the change in the summary.
- **Preserve voice**: Keep the founder's framing and language where possible. Do not over-corporatize or add unnecessary jargon.
- **Preserve specificity**: When a note provides specific API names, function signatures, parameter details, output formats, or behavioral expectations, carry those through to the strategy docs verbatim. Do not abstract away concrete details into vague summaries. If the founder wrote `generateMarkdownForAllArticles(warcFilename, lastRecordIdProcessed=None)`, the roadmap entry should include that signature -- not just "batch Markdown generation." The founder's specificity is signal, not noise.
- **One note item = one roadmap entry**: Do not merge distinct features into a single roadmap row, even if they are related. If the founder lists `getTitlesFromPage(count, page)` and `getTitlesFromRecordId(count, warcRecordId)` separately, they get separate roadmap entries. Lumping them together loses the founder's intent about distinct capabilities.
- **Flag ambiguity**: If a note is unclear or could be interpreted multiple ways, add a callout in the relevant strategy doc rather than guessing:
  ```markdown
  > [!NOTE] Needs clarification: [describe the ambiguity]
  ```
- **Atomic sections**: Each section in a strategy doc should stand alone. A reader should not need to read the entire document to understand one section.
- **Maintain structure**: Follow the section structure defined in `templates.md`. Add new sections only when existing ones genuinely do not fit.

## Document Reference

See `product/strategy-vision/index.md` for the full guide. Quick reference:

| Document | Covers | Update frequency |
|----------|--------|-----------------|
| `vision.md` | Who, what, why, beliefs about the future, non-goals | Rarely |
| `strategy.md` | How we win: positioning, landscape, differentiation, revenue | Occasionally |
| `roadmap.md` | Features: shipped, in progress, planned, priorities | Frequently |
| `principles.md` | Operating guardrails: technical and organizational values | Rarely |
| `decisions.md` | Key decisions, rejected approaches, rationale | As decisions are made |

## Examples

See `examples.md` in this skill's directory for concrete examples of inbox notes being transformed into strategy document updates.
