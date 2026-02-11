# Project Instructions

This is a Python-based CLI library that allows users to analyze Common Crawl News datasets via the CLI.

## Tech Stack
- Python 3.12
- [Click](https://click.palletsprojects.com/en/stable/) Python package for creating CLI apps
- VS Code / Docker: Refer to `.devcontainer` directory if necessary.
- Jupyter notebooks: Use ephemeral environments in Google Colab via the VS Code Google Colab extension
- Linter/formatter: [ruff](https://docs.astral.sh/ruff/) (configured in `pyproject.toml`)
- Tests: [pytest](https://docs.pytest.org/) with tests in the `tests/` directory

## Dev Mode
For development purposes, this codebase should be dockerized and run in a VS Code devcontainer.

The user should be able to mount a local directory containing various WARC files.

Create Jupyter notebooks for analyzing the WARC files using the tools that will be exposed by this library.

It is ok to hardcode functionality in Jupyter cells during development, but any functionality that should be exposed as tools should live in a Python file which is imported by the Jupyter notebook. Functions should be stateless and accept input and return output. Python cells should simply call the functions with the appropriate params and render the output.

## Dev Workflow

Follow a **test-driven development (TDD)** cycle for all code changes:

### 1. Write a failing test

Before writing any implementation code, write a test that describes the expected behavior. Place test files in `tests/` mirroring the source structure:

```
cc_news_analyzer/warc.py       →  tests/test_warc.py
cc_news_analyzer/index.py      →  tests/test_index.py
cc_news_analyzer/cli.py        →  tests/test_cli.py
```

Run the test to confirm it fails:

```bash
pytest tests/ -v
```

### 2. Implement the code

Write the minimal implementation to make the failing test pass. Keep functions stateless — accept input, return output.

### 3. Run validation

After making any change, run the full validation pipeline:

```bash
# Lint and auto-fix
ruff check . --fix

# Format
ruff format .

# Run tests
pytest tests/ -v
```

### 4. Fix any issues

If the linter or tests report failures, fix them before considering the change complete. Repeat step 3 until everything passes.

### When to run what

| Trigger | Commands to run |
|---------|----------------|
| Any Python file changed | `ruff check . --fix && ruff format .` |
| Any logic changed | `pytest tests/ -v` |
| Before committing | `ruff check . --fix && ruff format . && pytest tests/ -v` |

### Test conventions

- Test files: `test_<module>.py` (e.g. `test_warc.py`)
- Test classes: `Test<FunctionName>` (e.g. `TestCountRecords`)
- Test methods: `test_<scenario>` — descriptive names like `test_raises_on_missing_file`
- Use `unittest.mock` to mock external dependencies (file I/O, network calls)
- Each test should be independent — no shared mutable state between tests

### Command conventions

- Always run `pytest` directly — never use `python -m pytest`
- Do not prefix commands with `cd <dir> &&`. Use the shell's `working_directory` parameter instead.

### Git workflow

All code changes must go through a pull request. Never commit directly to `main`.

1. **Create a feature branch** before making any changes:
   - Use a descriptive branch name (e.g. `feat/add-count-command`, `fix/index-url-parsing`, `ci/add-test-workflow`)
2. **Work on the branch** following the TDD cycle above.
3. **Validate before committing** — run the full validation pipeline (`ruff check . --fix && ruff format . && pytest tests/ -v`) and ensure everything passes.
4. **Commit and push** the branch to `origin` when it is ready for human review.
   - Do not push until all tests pass and the change is complete.
   - Do not consider the task finished until the commit is created and the branch is pushed.
5. The human will open a PR and merge after review.
