# Roadmap

## Shipped

Features and capabilities that are live and usable today.

| Feature | Description | Date shipped |
|---------|-------------|-------------|
| Monthly index discovery | `get-index` downloads the CC-NEWS WARC index for a given month and lists available WARC paths | Pre-v0.1 |
| WARC file download | `get-warc` downloads a WARC file from CC-NEWS by its relative path | Pre-v0.1 |
| Record counting | `count-records` counts WARC records in a file | Pre-v0.1 |
| List WARC files (library) | `list_warc_files()` scans a directory for `.warc`/`.warc.gz` files and returns metadata | Pre-v0.1 |
| CLI docs generation | `cc-news-docs` auto-generates CLI reference documentation from Click commands | Pre-v0.1 |
| Jupyter exploration notebook | `notebooks/explore.ipynb` demonstrates index discovery, WARC download, and record counting via Google Colab | Pre-v0.1 |
| Devcontainer setup | Dockerized development environment with data volume mount and pre-installed dependencies | Pre-v0.1 |

## In Progress

Features currently being built.

| Feature | Description | Status |
|---------|-------------|--------|
| (none) | | |

## Planned

Features we intend to build, roughly in priority order.

| Feature | Description | Priority | Rationale |
|---------|-------------|----------|-----------|
| Article extraction | Extract article HTML from a WARC file by record ID (`getArticle`) | High | Core capability needed before any content analysis is possible |
| HTML to Markdown conversion | Convert extracted HTML to clean Markdown, stripping navigation, scripts, styles, SVGs (`convertHtmlToMarkdown`) | High | Markdown is dramatically smaller than HTML and far more useful for analysis and agent consumption |
| Batch Markdown generation | Generate Markdown for all articles in a WARC file, with resume support (`generateMarkdownForAllArticles`) | High | Enables bulk analysis workflows; resume support handles the 30+ second processing time |
| WARC to JSONL transformation | Transform a WARC file into a JSONL file with one JSON article per line. Enables keyword filtering via line-level grep and extraction of matching record IDs | High | Key enabler for keyword search workflows; avoids needing a database while making articles individually addressable |
| Keyword search and filtering | Search articles in a WARC (or JSONL) file by keyword/phrase list. Return matching record IDs or full article data | High | Core use case: find articles related to a topic. Short-term alternative to vector search with zero infrastructure cost |
| Date-based WARC download | Download WARC files for a specific date or date range, not just by path | High | Analysts need to target specific time periods when investigating a topic or event |
| Article browsing | Get titles by page or by record ID (`getTitlesFromPage`, `getTitlesFromRecordId`) | Medium | Analysts need to browse and select articles before deep-diving |
| Article lede extraction | Extract the lede/summary of an article (`getArticleLede`) | Medium | Quick triage without reading the full article |
| Topic and word analysis | Identify common topics/words and filter articles by keyword matches | Medium | Core analyst use case: find patterns in news coverage |
| Keyword search + entity extraction POC notebook | Google Colab notebook demonstrating end-to-end workflow: load a WARC file, extract articles matching a search term, then extract related keywords/tags/entities from those articles | Medium | Demonstrates the value of the CLI to product builders; serves as both tutorial and marketing |
| Keyword highlighting | Maintain a word/phrase list and highlight matches in article previews | Low | Quality-of-life feature for deeper analysis sessions |
| Stop word management | Maintain a list of ignored words/phrases to reduce noise in analysis | Low | Supports the keyword/topic analysis workflow |

## Backlog

Ideas that are worth tracking but not yet prioritized.

- Vector search against embeddings: Support semantic search over article content using vector embeddings. Deferred due to infrastructure cost; keyword search is the short-term approach
- MCP server: Expose CLI tools as an MCP server so agents can use them natively without shell access. Under consideration -- may live in this repo or a separate project
- Agent skills: Provide skill files that teach agents how to use the CLI tools proficiently. Under consideration -- may live in this repo or a separate project
- Telemetry: Add observability to CLI tool calls so the founder can observe which calls succeed vs. fail and improve tools based on real usage patterns
- Agent-native CLI patterns: Design commands specifically for AI agent composition (structured output, machine-readable formats)
- Config file for temporary directory: Replace hardcoded `.tmp` with a configurable path via config or env file
- WARC file init/setup tooling: Commands to clone a CC-NEWS dataset for a given month, unzip, and extract WARC files
- Article count by date: `getArticleCountByDate('MM-DD-YY')` for temporal analysis
- `list-warc-files` CLI command: Expose the existing `list_warc_files()` library function as a CLI command
- React frontend: A web UI for visual exploration. Indefinitely deferred -- core principle is CLI-first, and anything a UI does must be doable via CLI. May revisit in the future
