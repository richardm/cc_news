## Common Crawl News Analyzer

## Purpose
This is a tool that allows anyone to pull a CC-NEWS dataset and explore it.

> Insight: This could potentially be a CLI tool rather than a React tool. Remember the idea: Anything your UI can do should be exposed via tools so agents can do it. Think in terms of tools. Let the agent compose tool calls.

## Use Cases

As an analyst:
* I want to see how many articles are in the dataset
* I want to browse articles in the dataset
* I want to see common topics or words and quickly filter down to the subset of articles that match
* I want to be able to see an HTML or Markdown preview of any article I select
* I want to be able to add words and phrases to a list, and I want the preview to indicate all of the exact matches on these words or phrases
* I want to be able to quickly add additional words or phrases, either by double clicking on a word or using the cursor to select multiple words. When I hover on the selected word, I should be able to remove it from the word list.
* I want to also see a list of ignored words or phrases (e.g. stop words, and other low value words or phrases)

Questions:
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

Note: Use an existing Python WARC library to read the warc file. The "warc" library seems like a good starting point.

Human analysis of WARC file:
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


### TODO Later:

Tools:
* Init env
* Clone a common crawl dataset for any given month
* Unzip the files and extract the WARC files

Note: An Agent should be able to read the README to undrestand what tools it has and run those CLI commads. Only commands defined in the package.json file should be allowed.

Ideally, the env will be dockerized so it can run locally or in the cloud.
