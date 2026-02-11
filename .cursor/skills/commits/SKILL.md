---
name: commit-changes
description: Commit changes to the repository following Conventional Commits.
---

# Commit Changes

Commit changes to the repository following Conventional Commits.

## Creating Git commits

1. Ensure all validations are complete (linting, formatting, tests pass).
2. Review the staged diff and the context of the task (user request, GitHub Issue, etc.) to determine the appropriate commit type.
3. Refer to `.cursor/skills/commits/conventional-commits.md` for the Conventional Commits format and available types.
4. Use your best judgment when choosing the commit type (`feat`, `fix`, `docs`, `refactor`, `test`, `chore`, etc.) — pick the type that most accurately describes the **intent** of the change.
5. Write a concise subject line in imperative mood (e.g., "add parser for WARC records", not "added parser").
6. Include a body only when the subject line alone is not sufficient to explain **why** the change was made.

