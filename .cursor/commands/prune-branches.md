# Prune Local Git Branches

Clean up local branches that have already been merged or pushed to `main`. This is safe — it will never delete `main` or the currently checked-out branch, and only removes branches whose work is already on `main`.

## Steps

1. **Fetch the latest remote state** so merge checks are accurate:

```bash
git fetch origin main --prune
```

2. **List candidates for deletion.** Run the following to identify local branches (excluding `main` and the current branch) that are fully merged into `origin/main`:

```bash
git branch --merged origin/main | grep -v -E '^\*|^\s*main$'
```

3. **Show the list to the user** before deleting anything. If the list is empty, report "No branches to prune" and stop.

4. **Delete the merged branches** using `git branch -d` (lowercase `-d`, which is the safe delete that refuses to delete unmerged work):

```bash
git branch -d <branch1> <branch2> ...
```

5. **Report results.** Summarize which branches were deleted and confirm the cleanup is complete.

## Safety rules

- **Never** delete `main`.
- **Never** delete the currently checked-out branch (the one marked with `*`).
- **Only** use `git branch -d` (safe delete). Never use `-D` (force delete).
- If a branch fails to delete, report the error but continue with the remaining branches.
