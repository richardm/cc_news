# Common Crawl News Analyzer

This is a CLI tool that allows anyone to pull a CC-NEWS dataset and explore it.

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

---

### TODO Later:

Tools:
* Init env
* Clone a common crawl dataset for any given month
* Unzip the files and extract the WARC files
* Ideally, the env will be dockerized so it can run locally or in the cloud.
* The temporary directory (which is currently .tmp) should be specified in a config or env file of some sort. Files should not hardcode this directory name. They should get it from this config file.

Note: An Agent should be able to read the README to understand what tools it has and run those CLI commads. Only commands defined in the package.json file should be allowed.
