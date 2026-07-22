---
title: "Verify tracked-file deletion without changing the index"
date: 2026-07-22
category: tooling
component: tooling
tags: [git, cleanup, verification, index, worktree]
file_type: rules
---

# Verify tracked-file deletion without changing the index

During an implementation task, `git ls-files 'path/**'` reads the Git index, so it continues to list tracked files that have been deleted only in the worktree. That does not mean the proposed deletion failed, and staging solely to make this command empty would unexpectedly alter the user's index.

Before commit, verify the intended state with both views:

```bash
git ls-files --deleted 'path/**'
for path in $(git ls-files 'path/**'); do test ! -e "$path" || exit 1; done
```

The first command confirms Git recognizes the removals; the second confirms no indexed path remains present in the worktree. `git status --short` and the scoped diff should show only the expected deletions. After the deletion is staged or committed, plain `git ls-files 'path/**'` becomes empty.

This preserves index ownership while still providing exact cleanup evidence.
