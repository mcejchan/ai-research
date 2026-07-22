---
title: "Verify unstaged deletions using both index and worktree state"
date: 2026-07-23
category: tooling
component: tooling
tags: [git, deletions, index, worktree, verification]
---

`git ls-files 'path/**'` reads the index, so it still lists tracked files deleted only from the worktree. This does not mean deletion failed, and staging files merely to make the command return nothing improperly changes the user's index. Before commit, combine `git ls-files --deleted 'path/**'` with checks that each indexed path is absent from the worktree. Use `git status --short` and a scoped diff to confirm that only the intended deletions remain.