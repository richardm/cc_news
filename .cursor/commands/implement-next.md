# Implement Next

1. Review the roadmap (`product/strategy-vision/roadmap.md`), pick the highest-priority
   item with no unmet dependencies.
2. Create a plan. Use a sub-agent to review the codebase and create a plan.
3. For each change, follow TDD:
   a. Write a failing test.
   b. Run: `pytest tests/ -v` (confirm it fails).
   c. Write the implementation.
   d. Run: `ruff check . --fix && ruff format . && pytest tests/ -v`
      ALL must pass (exit code 0).
   e. If exit code is non-zero, fix the issue and repeat (d).
4. When all changes are complete, run the full validation one final time:
   `ruff check . --fix && ruff format . && pytest tests/ -v`
   Do NOT proceed if exit code is non-zero.
5. Stage, commit (Conventional Commits), and push.
6. Confirm the push succeeded and report the branch name.

CRITICAL REMINDERS:
- NEVER use `cd <dir> &&` to prefix commands. Use the `working_directory` parameter.
- NEVER run `echo`, `python -c`, or other ad-hoc terminal commands.
- NEVER ignore a non-zero exit code from the validation pipeline.
