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
| Article count | `count-articles` CLI command and `count_articles()` library function to count only articles (HTML response records) in a WARC file | Ready for review |

## Planned

Features we intend to build, roughly in priority order.

| Feature | Description | Priority | Rationale |
|---------|-------------|----------|-----------|
| Article count | `getArticleCount`: Count only articles in a WARC file (response records containing HTML), as distinct from `count-records` which counts all WARC record types including requests and warcinfo | High | Analysts care about article count, not raw WARC record count; this is the first question an analyst asks about a dataset |
| Article content retrieval | `getArticleContents(warcRecordId)`: Retrieve the full raw contents of a specific WARC record by its record ID | High | Core retrieval primitive needed to access individual articles in a WARC file; lower-level than `getArticle` which extracts only the HTML |
| Article extraction | `getArticle(recordId)`: Extract the article's HTML from a WARC file by record ID | High | Core capability needed before any content analysis is possible |
| HTML to Markdown conversion | `convertHtmlToMarkdown(html)`: Convert extracted article HTML to clean Markdown, stripping SVGs, symbols, scripts, styles, structure, navigation, and other unnecessary data. The resulting Markdown should be significantly smaller than the source HTML | High | Markdown is dramatically smaller than HTML and far more useful for analysis and agent consumption |
| Batch Markdown generation | `generateMarkdownForAllArticles(warcFilename, lastRecordIdProcessed=None)`: Generate Markdown for all articles in a WARC file, outputting to a JSON file. Supports resume by tracking the last `WARC-Record-Id` processed (linear, top to bottom) and skipping already-extracted articles. Processing may take 30+ seconds for large files | High | Enables bulk analysis workflows; resume support handles long processing times gracefully |
| WARC to JSONL transformation | One-time command to transform a WARC file into a JSONL file (one JSON article per line) for easier consumption by tools like `jq`, `grep`/`ripgrep`. Enables keyword filtering via line-level grep and extraction of matching record IDs | High | Key enabler for keyword search workflows; avoids needing a database while making articles individually addressable |
| Keyword search and filtering | Search articles in a WARC (or JSONL) file by keyword/phrase list. Return matching record IDs or full article data | High | Core use case: find articles related to a topic. Short-term alternative to vector search with zero infrastructure cost |
| Date-based WARC download | Download WARC files for a specific date or date range, not just by path | High | Analysts need to target specific time periods when investigating a topic or event |
| Article browsing (by page) | `getTitlesFromPage(count, page)`: Return the next `count` article titles starting at `page` (0-indexed) | Medium | Analysts need to browse and select articles before deep-diving; page-based pagination for sequential browsing |
| Article browsing (by record ID) | `getTitlesFromRecordId(count, warcRecordId)`: Return the next `count` article titles starting at the given `warcRecordId` | Medium | Enables resumable browsing from a known position in the WARC file |
| Article lede extraction | `getArticleLede(recordId)`: Extract the lede/summary of an article | Medium | Quick triage without reading the full article |
| Topic and word analysis | Identify common topics/words across articles in a dataset and filter down to the subset of articles that match | Medium | Core analyst use case: find patterns in news coverage |
| Keyword search + entity extraction POC notebook | Google Colab notebook demonstrating end-to-end workflow: load a WARC file, extract articles matching a search term, then extract related keywords/tags/entities from those articles | Medium | Demonstrates the value of the CLI to product builders; serves as both tutorial and marketing |
| Keyword highlighting | Maintain a word/phrase list and highlight all exact matches in article previews. Support quickly adding words (e.g. double-click a word or select a phrase) and removing words from the list | Low | Quality-of-life feature for deeper analysis sessions; enables iterative keyword refinement |
| Stop word management | Maintain a list of ignored words or phrases (e.g. stop words, low-value terms) to reduce noise in topic and keyword analysis | Low | Supports the keyword/topic analysis workflow by filtering out noise |

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
