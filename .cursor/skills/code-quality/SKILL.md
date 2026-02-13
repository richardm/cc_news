---
name: review-code-quality
description: Improve code quality. Use this skill when asked to review, assess, or improve code quality. Use this when considering architecture and design tradeoffs.
---

# Code Quality Review

Review code quality by running complexity tooling, then spawning parallel sub-agents per module. If the user specifies a scope (e.g., "review `warc.py`"), constrain to that scope.

## Step 0: Run complexity tooling

Run these commands and capture their output:

- `radon cc cc_news_analyzer/ -s -a` -- per-function complexity grades (A-F)
- `ruff check . --select C901` -- any functions exceeding the max-complexity threshold

## Step 1: Discover and group modules

List the source files under the main package. Pair each with its corresponding test file:

```
cc_news_analyzer/warc.py       + tests/test_warc.py
cc_news_analyzer/index.py      + tests/test_index.py
cc_news_analyzer/cli.py        + tests/test_cli.py
```

Group into review units. If sub-packages exist, group by sub-package instead of individual file.

## Step 2: Spawn review sub-agents

Launch one `explore` sub-agent per module group (max 4 concurrent, `readonly: true`). Pass each sub-agent:

1. The source and test file paths for its module
2. The radon/ruff output for that module (from Step 0)
3. The **Review Checklist** below (embed in the prompt)
4. Instructions to return structured findings per the **Output Format** below

## Step 3: Consolidate and report

Collect results from all sub-agents. Add any cross-cutting concerns (circular dependencies, inconsistent patterns across modules). Present a unified report.

---

## Review Checklist

### Complexity

- Review the radon grades: any function at grade C (11-20) or worse needs attention.
- Functions longer than ~40 lines or with deep nesting (3+ levels) -- flag for extraction.
- Prefer smaller, composable functions.

### Composability

- Prefer stateless, pure functions. Flag functions that mix I/O with business logic.
- Flag god functions that do too many things (Single Responsibility Principle).
- Simple functions should compose into powerful higher-level capabilities.

### Naming and Readability

- Clear, descriptive names. No ambiguous abbreviations.
- Consistent conventions across the module.

### Error Handling

- Explicit error paths with meaningful error messages.
- No bare `except:`.

### Algorithmic Choices and Scale Readiness

Target worst-case O(n log n). Domain context: ~50k WARC records/file, ~1 GB compressed (4-5 GB uncompressed), dozens of files/month.

- Flag anything that loads full files into memory unnecessarily.
- Flag O(n^2) or worse patterns.
- Assess whether binary search O(log n) is viable where data has monotonic ordering.
- **Document algorithmic choices in code**: e.g., `# linear scan: no known monotonic ordering in WARC records` or `# binary search: records ordered chronologically`. Flag undocumented choices.

### Test Quality

Prefer **behavioral / functional tests** (black-box: test inputs and outputs).

- **No change-detection tests.** Tests validate behavior, not that code changed.
- **Minimize mocks.** Use mocks only where legitimately needed (external I/O, network calls). Prefer real data or fixtures.
- Each test should test a single behavior.
- **Parameterized tests:** Where multiple tests differ only in input/expected output, consolidate into a single test iterating over a test-data array.
- Assess whether the module has adequate edge-case and error-path coverage.
- Flag modules needing more robust test coverage.

---

## Output Format

Each sub-agent should return findings in this structure:

```
### [Module Name] (source.py + test_source.py)
- **Findings**: bullet list, tagged (info / warning / action-needed)
- **Algorithmic notes**: undocumented algorithmic choices found
- **Test gaps**: areas needing better coverage
- **Suggestions**: concrete refactoring recommendations
```

The parent agent consolidates into the final report:

```
## Code Quality Review: [scope]

### Complexity Summary
(radon grades + ruff C901 violations)

### [Module findings from sub-agents]

### Cross-Cutting Concerns
(items spanning multiple modules)

### Summary
- Total findings by severity
- Top 3 priority actions
```
