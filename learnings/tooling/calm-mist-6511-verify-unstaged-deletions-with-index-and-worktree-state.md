---
title: "Verify unstaged deletions with index and worktree state"
date: 2026-07-22
category: tooling
component: tooling
tags: [git, cleanup, index, worktree, verification]
---

After deleting tracked files without staging, `git ls-files 'tmp/**'` still lists them because it reports index entries, not filesystem existence. Verify cleanup with both `git ls-files --deleted 'tmp/**'` and an explicit existence check over tracked paths. This proves the files are absent from the worktree without mutating the index or staging unrelated changes.