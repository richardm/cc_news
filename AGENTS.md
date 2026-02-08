This is a Python-based CLI library that allows users to analyze Common Crawl News datasets via the CLI.

## Dev Mode
For development purposes, this codebase should be dockerized and run in a VS Code devcontainer.

The user should be able to mount a local directory containing various warc files.

Create Jupyter notebooks for analyzing the WARC files using the tools that will be exposed by this library.

It is ok to hardcode functionality in Jupyter cells during development, but any functionality that should be exposed as tools should live in a Python file which is imported by the Jupyter notebook. Functions should be stateless and accept input and return output. Python cells should simply call the functions with the appropriate params and render the output.
