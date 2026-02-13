# Vision

## Target User

The primary user is a **human analyst** exploring news datasets. They are technically comfortable (can use a CLI, run Docker, work in Jupyter) but are not necessarily software engineers. They want to answer questions about news coverage -- what was published, when, by whom, about what topics -- without building a custom pipeline from scratch.

A key secondary user is the **aspiring founder** building products on top of CC-NEWS data. This person needs reliable, composable tools for data retrieval and exploration so they can focus on their product logic rather than wrestling with WARC files. This CLI is the foundation layer that makes CC-NEWS usable inside other products.

The tertiary user (growing in importance) is an **AI agent** that uses the CLI as a composable toolset to autonomously explore CC-NEWS datasets. The founder anticipates delegating increasing amounts of analysis work to agents. The agent composes individual commands to build emergent analytical capabilities that the tool authors never explicitly designed.

## Example Use Cases

- **Find articles on a topic.** An analyst (or agent) searches CC-NEWS for articles related to a given topic -- e.g., "find recent news articles about X." This may involve downloading WARC files for a specific date or date range, then searching and filtering articles by keyword.
- **Source claims from news coverage.** A founder building a product needs to attribute claims to specific reporters and publications. The CLI provides the raw article retrieval; the consuming product handles attribution logic.
- **Build a breaking-news timeline.** A product builder wants to construct a historical timeline of events related to a breaking story, sourcing and attributing claims from multiple news articles as they emerge -- correcting early misinformation as additional reporting comes in. We are not building that product here, but we are building the tools that make it possible.
- **Keyword expansion and entity discovery.** A data analyst retrieves articles matching initial keywords, then identifies additional keywords, entities, or tags from those articles to broaden the search. The CLI provides article retrieval and text extraction; entity recognition may live in consuming projects.

## Pain Points

- **CC-NEWS is powerful but inaccessible.** Common Crawl publishes one of the largest open news archives on the planet, but there is no purpose-built tool for exploring it. Users must cobble together generic WARC libraries, custom scripts, and manual HTTP requests.
- **WARC files are opaque.** The WARC format is complex -- records have multiple types, headers are inconsistent, and there is no built-in way to browse, count, or filter content without writing code.
- **No quick path from "I have a WARC file" to "I see the articles."** Analysts want to go from download to insight quickly. Today, that requires significant setup and boilerplate.
- **Existing WARC tools are generic.** Tools like `warcio` provide low-level primitives but no CC-NEWS-specific workflows (index discovery, monthly archives, article extraction).
- **Finding relevant articles in large datasets is hard.** WARC files contain thousands of articles. There is no built-in way to filter by date, topic, or keyword without processing the entire file manually.

## Product Purpose

Provide composable CLI tools and library functions that make Common Crawl News datasets accessible for analysis, exploration, and use as a data source inside other products. This is a toolkit for builders -- not an end-user application.

## What Success Looks Like

An analyst can go from zero to exploring a month's worth of global news coverage in under five minutes: discover the index, download a WARC file, count records, browse articles, extract content, and filter by topic -- all from the CLI or a Jupyter notebook, with no infrastructure to manage.

A founder building a product on CC-NEWS data can use this CLI as their data layer -- retrieving articles by date, filtering by keyword, extracting clean text -- and focus entirely on their product logic. For example, a founder building a breaking-news timeline product could use the CLI to retrieve articles matching a topic, extract their text, and feed that into their own attribution and timeline logic.

AI agents can use the same commands as building blocks, composing them into autonomous analytical workflows that the tool authors never explicitly programmed. An agent might download WARC files for a date range, search for articles matching a keyword list, extract the text, identify additional keywords, and iterate -- all by composing CLI commands.

## Beliefs About the Future

- **Agents will compose tools to create emergent behavior.** The founder strongly anticipates a future where AI agents compose CLI tool calls to perform novel tasks that were never explicitly designed. Rather than hardcoding specific workflows, we build an extensive toolkit and let agents discover how to use it. This is a core architectural bet.
- **Telemetry will drive tool improvement.** By adding telemetry to observe which tool calls succeed vs. fail, the founder can identify friction points and improve tools based on real agent usage patterns. Skills (instructions that teach agents to use tools proficiently) can further improve agent success rates.
- **Demand for news media analysis is growing.** Journalists, researchers, and analysts increasingly need to study media coverage at scale. CC-NEWS is an underutilized resource because the tooling gap is too wide.
- **Open data tooling is underdeveloped.** Common Crawl publishes incredible data for free, but the tooling to actually use it lags far behind. Making open data accessible creates outsized value relative to the effort.
- **AI agents will need composable CLI tools.** As AI agents become capable of autonomously using tools, a well-designed CLI becomes an API for agents. Building agent-friendly commands now positions the project to be valuable in the agentic future.

## Non-Goals

- **We are not building end-user products.** We build the tools that enable others to build products (e.g., a breaking-news timeline, a claim-attribution system). The CLI is a foundation layer.
- **We are not building a hosted service.** The tool runs locally -- no cloud infrastructure, no accounts, no SaaS.
- **We are not building or requiring managed databases.** We work directly with the filesystem and WARC files. No stateful system to maintain. Environments should be ephemeral -- load data, analyze, store output, tear down.
- **We are not building a general-purpose WARC tool.** We are purpose-built for CC-NEWS. Supporting arbitrary WARC sources is not a goal.
- **We are not doing entity extraction or NLP in this repo (for now).** Features like TF-IDF keyword extraction or named entity recognition may belong in consuming projects. This repo provides raw text retrieval; downstream projects handle analysis. However, we will provide example notebooks showing how to combine this CLI with NLP tools.
- **We are not hardcoding workflows.** We build individual tools, not opinionated pipelines. Agents and users compose the tools as they see fit. However, we will provide some Jupyter notebooks showing how to construct example workflows from these tools.

## Failed or Rejected Approaches

- **React UI for browsing articles.** Early thinking considered building a web-based UI for browsing WARC contents. Indefinitely deferred in favor of a CLI-first approach -- simpler to build, easier for agents to use, and avoids front-end complexity. The CLI + Jupyter notebooks cover the interactive exploration use case. A React UI remains possible in the future, but the core principle is that anything a UI can do must first be doable via CLI.
- **Extracting WARC data into a database.** Considered but rejected. A stateful system adds complexity and maintenance burden. Working directly with the filesystem keeps the tool simple and portable. The founder strongly prefers ephemeral environments with no managed infrastructure.
