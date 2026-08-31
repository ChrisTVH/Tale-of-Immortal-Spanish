# Repository Safety Rules

## Workshop cache files

- Never delete, modify, stage, commit, publish, copy, or expose `ModProject/ModData.cache` or `ModProject/ModProject.cache`.
- These untracked cache files contain Workshop keys and other sensitive project data.
- Preserve them during validation, cleanup, and tooling runs.
- Never print or include their contents in logs, diffs, documentation, or responses.
