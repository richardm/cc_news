## High-Level Concept

### Use Cases

As an analyst:
* I want to see how many articles are in the dataset (dataset = WARC file)
* I want to browse articles in the dataset
* I want to see common topics or words and quickly filter down to the subset of articles that match
* I want to be able to see an HTML or Markdown preview of any article I select
* I want to be able to add words and phrases to a list, and I want the preview to indicate all of the exact matches on these words or phrases
* I want to be able to quickly add additional words or phrases, either by double clicking on a word or using the cursor to select multiple words. When I hover on the selected word, I should be able to remove it from the word list.
* I want to also see a list of ignored words or phrases (e.g. stop words, and other low value words or phrases)
* Might be useful to have a one-time command to transform a warc file into a JSONL file for easier consumption by the UI and tools like jq, grep / ripgrep?

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
