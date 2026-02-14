![CI Status](https://github.com/richardm/cc_news/actions/workflows/ci.yml/badge.svg)

# Common Crawl News Analyzer

This is a CLI tool that allows anyone to pull a [CC-NEWS](https://commoncrawl.org/news-crawl) dataset and explore it.

## Supported Usage Modes
1. The human analyst can use the Google Colab extension in VS Code / Cursor to download and explore WARC files in a remote Google Colab env. They will open a Jupyter notebook in VS Code -> Select Kernel -> Colab -> create or select a kernel, and then proceed to use the notebook.
2. The human analyst may use the CLI to download and explore CC-NEWS files locally. This repo includes a `.devcontainer`, allowing the user to run `cc-news` in a Docker container. (Open a terminal in the container and run `cc-news --help` to see available commands.)
3. TODO: Eventually, AI agents will use this CLI as a tool to explore CC-NEWS datasets, composing emergent capabilities from tool calls. (See [Agent-native architectures](https://every.to/guides/agent-native))

## CLI Reference

Full CLI documentation is auto-generated on every push and pull request.
Download the latest from the [Actions artifacts](https://github.com/richardm/cc_news/actions).

To generate locally:

```
cc-news-docs
```
