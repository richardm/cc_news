# Common Crawl News Analyzer

This is a CLI tool that allows anyone to pull a CC-NEWS dataset and explore it.

> Insight: This could potentially be a CLI tool rather than a React tool. Remember the idea: Anything your UI can do should be exposed via tools so agents can do it. Think in terms of tools. Let the agent compose tool calls.
## Supported Usage modes:
1. The human analyst can use the Google Colab extension in VS Code / Cursor to download and explore WARC files in a remote Google Colab env. They will open a Jupyter notebook in VS Code -> Select Kernel -> Colab -> create or select a kernel, and then proceed to use the notebook.
2. The human analyst may use the CLI to download and explore CC-NEWS files locally. This repo includes a `.devcontainer`, allowing the user to run `cc-news` in a Docker container.
3. Eventually, AI agents will use this CLI as a tool to explore CC-NEWS datasets, composing emergent capabilities from tool calls. (See [Agent-native architectures](https://every.to/guides/agent-native))

## Use Cases

As an analyst:
* I want to see how many articles are in the dataset (dataset = WARC file)
* I want to browse articles in the dataset
* I want to see common topics or words and quickly filter down to the subset of articles that match
* I want to be able to see an HTML or Markdown preview of any article I select
* I want to be able to add words and phrases to a list, and I want the preview to indicate all of the exact matches on these words or phrases
* I want to be able to quickly add additional words or phrases, either by double clicking on a word or using the cursor to select multiple words. When I hover on the selected word, I should be able to remove it from the word list.
* I want to also see a list of ignored words or phrases (e.g. stop words, and other low value words or phrases)

Design Questions:
* Is it necessary to extract the data from the WARC file into a database? I’d like to avoid having to maintain a stateful system. It would be easier to work directly with the filesystem.
* Some options: A one-time command to transform a warc file into a JSON file for easier consumption by the UI and tools like jq? Perhaps I can navigate the warc file via the CLI instead of building a react UI.

Perhaps it’s best to expose some CLI tools like:
* `getArticleCount`
* `getArticleContents(warcRecordId)`
* `getArticleCountByDate('MM-DD-YY')`, 
* `getArticle(recordId)`: Extract article’s HTML from WARC file
* `getArticleLede(recordId)`
* `convertHtmlToMarkdown(html)`: Convert HTML to markdown. This markdown should be SIGNIFICANTLY smaller than the HTML because it eliminates SVGs, symbols, scripts, styles, structure, navigation, and other unnecessary data.
* `generateMarkdownForAllArticles(warcFilename, lastRecordIdProcessed = null)`: Generate markdown for all files (This may take 30+ seconds…). Idea: This can track the last WARC-Record-Id extracted (linear, top to bottom) and skip already-extracted articles. For the next article found, continue extracting contents, converting to markdown, and adding the markdown to a JSON file.
* getTitlesFromPage(count, page): Returns the next {count} titles starting at page (0-indexed)
* getTitlesFromRecordId(count, warcRecordId): Returns the next {count} titles starting at a given warcRecordId

Note: Use an existing Python WARC library to read the warc file. The "warc" library seems like a good starting point.

Notes from human analysis of WARC file:
* `WARC-Type: request` and `WARC-Type: response` seem to be what we care about (fetched articles).
* **WarcInfo**:
  * `WARC-Type: warcinfo` appears first and describes the warcfile itself.
  * It provides the WARC date and a unique `WARC-Filename` and a `WARC-Record-ID`
* Articles
  * Each block appears to begin with `WARC/1.0`. Each request consists of a request + a response.
  * Request
    * `WARC-IP-Address`: The IP address where the article was retrieved
    * `WARC-Record-Id`: Unique identifier for the article
    * `Content-Length`: The content-length of the article.
    * `WARC-Date`: The date the article was retrieved?
    * `WARC-Target-URI`: The URI where the article was retrieved from?
  * Note that the `WARC-Record-ID` of the request + response are different, even for the same request.
  * Response:
    * Returns HTML contents, often containing useful data in the title and meta tags


## Formal CLI docs

The CLI is invoked via the `cc-news` command (installed as a console script).

| Command | Description |
|---------|-------------|
| [`count-records`](#cc-news-count-records) | Count WARC records in a local file |
| [`get-index`](#cc-news-get-index) | List available WARC files for a given month |
| [`get-warc`](#cc-news-get-warc) | Download a WARC file by its relative path |

### `cc-news count-records`

Count the number of WARC records with a `WARC-Record-ID` in a local file.

```
cc-news count-records <WARC_FILE>
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `WARC_FILE` | argument | yes | Path to a local `.warc` or `.warc.gz` file. The file must exist. |

**Example:**

```
cc-news count-records .tmp/CC-NEWS-20260204051206-06668.warc.gz
```

### `cc-news get-index`

Download the CC-NEWS WARC index for a given month and list all available WARC files.

```
cc-news get-index [--date MM-YYYY]
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--date` | option | no | current month | Month to fetch in `MM-YYYY` format (e.g. `02-2026`). |

**Examples:**

```
# List WARC files for the current month
cc-news get-index

# List WARC files for February 2026
cc-news get-index --date 02-2026
```

### `cc-news get-warc`

Download a single WARC file from the CC-NEWS dataset by its relative path.

```
cc-news get-warc <WARC_PATH> [--dest DIR]
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `WARC_PATH` | argument | yes | — | Relative path within the Common Crawl dataset, as returned by `get-index` (e.g. `crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz`). |
| `--dest` | option | no | `.tmp` | Destination directory for the downloaded file. Created automatically if it does not exist. |

**Examples:**

```
# Download a WARC file into the default .tmp directory
cc-news get-warc crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz

# Download into a custom directory
cc-news get-warc crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz --dest /data/warcs
```

---

### TODO Later:

Tools:
* Init env
* Clone a common crawl dataset for any given month
* Unzip the files and extract the WARC files
* Ideally, the env will be dockerized so it can run locally or in the cloud.
* The temporary directory (which is currently .tmp) should be specified in a config or env file of some sort. Files should not hardcode this directory name. They should get it from this config file.
* Add some sort of config for keeping track of the file we're currently working with (so user does not have to pass the file name with each command). See features/make-cli-stateful.md for more details.

Note: An Agent should be able to read the README to understand what tools it has and run those CLI commads. Only commands defined in the package.json file should be allowed.
