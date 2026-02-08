---
name: write-unit-tests
description: Analyze a Python function or code snippet, identify its behavior and edge cases, then generate comprehensive unit tests using the unittest library. Use when the user asks to write tests, create unit tests, test a function, add test coverage, or mentions unittest.
---

# Write Unit Tests

Generate thorough Python `unittest` test cases for a given function or code snippet.

This skill follows the **TDD workflow** defined in `AGENTS.md`. The standard cycle is:
1. Write a failing test first
2. Implement the minimal code to make it pass
3. Run validation (lint + format + tests)
4. Fix any issues

## Workflow

### Step 0: TDD — Write the test first

If you are implementing new functionality, write the test **before** writing the implementation. The test should fail initially — this confirms it is testing the right thing. Only then proceed to implement the code to make it pass.

If you are adding tests for existing code, skip this step and go to Step 1.

### Step 1: Analyze the Target

Read the function or code snippet. Identify:

1. **Core behavior**: What does it do under normal inputs?
2. **Input boundaries**: Empty collections, zero/negative numbers, None values, max-size inputs
3. **Error paths**: What exceptions should it raise? What invalid inputs exist?
4. **Return types**: All possible return values including edge cases
5. **Side effects**: File I/O, network calls, database access, state mutations
6. **Dependencies**: External modules, services, or functions it calls

### Step 2: Plan Test Cases

Before writing code, list the test cases as a checklist:

```
Test Plan for `function_name`:
- [ ] Happy path with typical input
- [ ] Edge case: empty input
- [ ] Edge case: boundary values
- [ ] Error case: invalid type
- [ ] Error case: expected exception
- [ ] Dependency: mock external call
```

### Step 3: Implement Tests

Place test files in `tests/` at the project root, mirroring the source structure:

```
cc_news_analyzer/
    parser.py          → tests/test_parser.py
    utils/helpers.py   → tests/utils/test_helpers.py
```

Use this structure for each test file:

```python
"""Tests for module_name."""

import unittest
from unittest.mock import patch, MagicMock

from cc_news_analyzer.module_name import function_name


class TestFunctionName(unittest.TestCase):
    """Tests for function_name."""

    def setUp(self):
        """Set up test fixtures."""
        # Common test data used across multiple tests
        pass

    def test_typical_input(self):
        """Should return expected result for standard input."""
        result = function_name(normal_input)
        self.assertEqual(result, expected)

    def test_edge_case_empty(self):
        """Should handle empty input gracefully."""
        result = function_name([])
        self.assertEqual(result, expected_for_empty)

    def test_raises_on_invalid_input(self):
        """Should raise ValueError for invalid input."""
        with self.assertRaises(ValueError):
            function_name(invalid_input)


if __name__ == "__main__":
    unittest.main()
```

### Step 4: Validate

After writing tests, run the full validation pipeline (lint, format, test):

```bash
# Lint and auto-fix
ruff check . --fix

# Format
ruff format .

# Run the tests
pytest tests/ -v
```

Fix any lint errors or test failures before finishing. Repeat until all checks pass.

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Test file | `test_<module>.py` | `test_parser.py` |
| Test class | `Test<ClassName>` or `Test<FunctionName>` | `TestParseWarc` |
| Test method | `test_<scenario>` | `test_returns_empty_list_for_no_records` |

Write test method names that read as behavior descriptions. Prefer `test_returns_none_when_key_missing` over `test_none`.

## Mocking with `unittest.mock`

Mock external dependencies so tests run fast and without side effects.

### Patching functions

```python
@patch("cc_news_analyzer.parser.open_warc_file")
def test_handles_missing_file(self, mock_open):
    mock_open.side_effect = FileNotFoundError("not found")
    with self.assertRaises(FileNotFoundError):
        parse("missing.warc")
```

### Mocking return values

```python
@patch("cc_news_analyzer.fetcher.requests.get")
def test_fetches_data(self, mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {"key": "val"})
    result = fetch_data("http://example.com")
    self.assertEqual(result, {"key": "val"})
```

### Key mocking rules

- Patch where the dependency is **used**, not where it is defined
- Use `MagicMock(spec=ClassName)` to catch attribute errors early
- Keep mock setup close to the assertion for readability

## Edge Case Checklist

Always consider these categories:

| Category | Examples |
|----------|----------|
| Empty/None | `None`, `""`, `[]`, `{}`, `0` |
| Boundaries | First/last element, max int, single-character string |
| Types | Wrong type passed (str instead of int) |
| Duplicates | Repeated values in collections |
| Unicode/encoding | Non-ASCII strings, mixed encodings |
| Concurrency | If applicable, thread safety |
| Large inputs | Performance-sensitive paths |

## Guidelines

- **One assertion per concept** — each test method should verify one logical behavior
- **Tests must be independent** — no test should depend on another test's state; use `setUp`/`tearDown`
- **Use `subTest`** for parameterized variations of the same behavior:

```python
def test_parses_various_formats(self):
    cases = [("a.warc", "warc"), ("b.warc.gz", "warc.gz")]
    for filename, expected_fmt in cases:
        with self.subTest(filename=filename):
            self.assertEqual(detect_format(filename), expected_fmt)
```

- **Avoid testing implementation details** — test what the function returns or raises, not how it works internally
- Create `tests/__init__.py` if it doesn't exist so the test directory is a proper package
