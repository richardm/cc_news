# validate

Run the full validation pipeline: lint, format, and test.

```bash
ruff check . --fix && ruff format . && pytest tests/ -v
```

Fix any errors before considering the change complete.
