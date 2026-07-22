---
title: "Prove external configuration with task-local evidence"
date: 2026-07-22
category: tooling
component: ci-cd
tags: [acceptance, evidence, external-config, git, test-gate]
---

When an implementation is committed in a different Git workspace, a repository-scoped review cannot see the clean external worktree and may incorrectly conclude that acceptance evidence is missing.

For an already-committed external change, create a bounded task-local evidence artifact containing the external repository path, full commit SHA, path-scoped `git show` diff, current parsed configuration value, and fresh behavioral verification. Link genuine historical RED/GREEN evidence and explicitly document gaps such as truncated command output.

Do not rewrite correct external configuration merely to create a fresh diff, and do not fabricate a new RED after implementation. The committed scoped diff proves delivery, while fresh tests and configuration assertions prove current behavior.