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

## CLI-first architecture (web UI indefinitely deferred)

- **Date**: Pre-v0.1 (refined 2026-02-13)
- **Decision**: Build a CLI tool as the primary interface. A React UI is indefinitely deferred but not permanently ruled out.
- **Context**: Early design considered a React UI for browsing articles in WARC files. The question was whether a visual interface was needed for exploration.
- **Options considered**: (1) React web UI, (2) CLI with Jupyter notebooks for interactive use, (3) TUI (terminal UI).
- **Rationale**: A CLI is simpler to build and maintain, works natively for AI agents, and pairs well with Jupyter notebooks for interactive exploration. The analyst target user is comfortable with a terminal and with Jupyter. Core principle: **anything a UI can do must first be doable via CLI** -- this ensures agent compatibility and keeps the CLI as the source of truth for all capabilities.
- **Deferred alternatives**: React UI -- indefinitely deferred. May revisit in the future, but only after CLI capabilities are comprehensive. The CLI-first principle means a UI would be a layer on top of existing CLI/library functionality, never a replacement.

---

## Filesystem over database

- **Date**: Pre-v0.1
- **Decision**: Work directly with WARC files on the filesystem rather than extracting data into a database.
- **Context**: The README asked: "Is it necessary to extract the data from the WARC file into a database?" The concern was avoiding a stateful system.
- **Options considered**: (1) Extract to SQLite or similar, (2) Transform WARC to JSON for easier consumption, (3) Work directly with WARC files.
- **Rationale**: A database adds setup, migration, and maintenance burden. Working directly with files keeps the tool portable and stateless. JSON transformation remains a possibility for specific use cases (e.g., batch Markdown generation) without requiring a full database.
- **Rejected alternatives**: Database extraction -- unnecessary statefulness for an exploration tool. The founder strongly prefers ephemeral environments with no managed infrastructure. May revisit if query performance becomes a bottleneck at scale.

---

## JSONL as intermediate format for keyword search

- **Date**: 2026-02-13
- **Decision**: Use JSONL (one JSON article per line) as an intermediate format for keyword search and filtering, rather than a database or in-memory search.
- **Context**: The core use case of finding articles related to a topic requires some way to search article content. Vector search over embeddings is the ideal long-term solution but has infrastructure cost. Needed a zero-infrastructure short-term approach.
- **Options considered**: (1) Vector search with embeddings, (2) Full-text search via SQLite FTS, (3) JSONL transformation + line-level keyword grep, (4) Search WARC files directly.
- **Rationale**: JSONL files are simple, portable, and can be filtered with standard Unix tools or Python line-by-line. An agent can generate a keyword list, grep JSONL lines for matches, and extract matching record IDs -- all without a database. This aligns with the ephemeral-environment and filesystem-over-database principles.
- **Deferred alternatives**: Vector search -- deferred due to infrastructure cost (embedding storage, similarity search). Will revisit when the use case justifies the complexity. SQLite FTS -- viable but introduces a database dependency that conflicts with the ephemeral-environment principle.

---

## Repo scope: CLI tools first, extensions TBD

- **Date**: 2026-02-13
- **Decision**: Short-term priority is building CLI tools. Whether this repo also provides an MCP server, agent skills, or other extensions is undecided.
- **Context**: The founder is considering whether this repo should be only a CLI or also provide an MCP server (for agent-native tool access) and skills (instructions that teach agents to use the tools). The question is whether these belong in the same repo or separate projects.
- **Options considered**: (1) Everything in one self-contained repo, (2) CLI in this repo + separate repos for MCP server and skills, (3) Decide later.
- **Rationale**: The CLI tools are the foundation -- everything else depends on them. Building the tools first keeps focus. The scope question for MCP server and skills can be answered once the CLI is more mature and the trade-offs (repo complexity vs. cross-project coordination) are clearer.
- **Deferred alternatives**: No alternatives rejected -- this is a "decide later" decision. Tracked in the backlog.

---

## Custom CLI docs generation (no external tools)

- **Date**: Pre-v0.1
- **Decision**: Build a custom Click introspection script (`generate_docs.py`) rather than using an existing documentation tool.
- **Context**: Needed auto-generated CLI reference docs. Evaluated several existing tools.
- **Options considered**: (1) click-man (man pages), (2) sphinx-click, (3) mkdocs-click, (4) Custom script.
- **Rationale**: Existing tools either produced the wrong format (man pages), required heavy dependencies (Sphinx, MkDocs), or didn't support the exact Markdown output we wanted. A custom script using Click's introspection API is ~50 lines and gives us full control.
- **Rejected alternatives**: click-man (man pages, not Markdown), sphinx-click (requires Sphinx ecosystem), mkdocs-click (requires MkDocs ecosystem). All add dependency weight for a simple need.

---

## Click for CLI framework

- **Date**: Pre-v0.1
- **Decision**: Use Click as the CLI framework.
- **Context**: Needed a Python CLI framework that supports commands, arguments, options, and help text generation.
- **Options considered**: (1) Click, (2) argparse (stdlib), (3) Typer, (4) Fire.
- **Rationale**: Click is mature, well-documented, and widely used. It supports command groups, has good introspection for docs generation, and integrates well with testing via `CliRunner`.
- **Rejected alternatives**: argparse (verbose, less ergonomic), Typer (adds a dependency layer on top of Click), Fire (too magic, less control over help text and validation).

---

## warcio as WARC parsing library

- **Date**: Pre-v0.1
- **Decision**: Use `warcio` as the Python WARC file parsing library.
- **Context**: A WARC parsing library is needed to read and iterate over CC-NEWS archive files. The founder's initial concept notes suggested the `warc` Python library as a starting point.
- **Options considered**: (1) `warc` (older Python WARC library), (2) `warcio` (modern, actively maintained).
- **Rationale**: `warcio` is actively maintained, provides a clean `ArchiveIterator` API for streaming through WARC records, and is the de facto standard for WARC processing in Python. It handles both `.warc` and `.warc.gz` files transparently.
- **Rejected alternatives**: `warc` — older, less actively maintained, and lacks the streaming iterator API that `warcio` provides.

---

## Google Colab for notebooks (not local Jupyter)

- **Date**: Pre-v0.1
- **Decision**: Use Google Colab as the primary notebook environment, accessed via the VS Code Colab extension.
- **Context**: Jupyter notebooks are used for interactive exploration during development. Needed to decide where they run.
- **Options considered**: (1) Local JupyterLab in devcontainer, (2) Google Colab via VS Code extension, (3) Both.
- **Rationale**: Colab provides ephemeral, zero-setup environments with free compute. The VS Code Colab extension allows editing in the IDE while executing on Colab. This avoids burdening the local devcontainer with heavy computation.
- **Rejected alternatives**: Local-only Jupyter -- viable but puts compute load on the developer's machine. Colab is preferred for exploration; local remains available via `jupyterlab` dependency.
