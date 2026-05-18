---
title: "Plan acceptance fixes from live worktree evidence"
date: 2026-05-18
category: tooling
component: tooling
tags: [planning, acceptance-fix, tdd, scope-control]
file_type: rules
---

# Plan acceptance fixes from live worktree evidence

When creating an acceptance-fix plan, inspect both the prior plan and the current worktree before prescribing implementation. The failure report may say a feature is missing from the provided diff, while the local workspace can already contain untracked or preserved implementation files.

## Pattern

- Resolve the canonical plan path before writing anything.
- Read the original plan and current files that correspond to the failed acceptance goals.
- Check `git status --short` so the plan can distinguish required scope from unrelated or untracked files.
- If acceptance requires proof outside the feature directory, name that file explicitly and treat it as the only allowed out-of-scope artifact.
- Make TDD skeletons test the missing evidence without adding dependencies; for zero-dependency Node/browser utilities, use `node:test`, `vm`, and small exported seams.

## Why

This keeps the replan actionable and prevents two common retry failures: redoing completed work and accidentally expanding scope while trying to satisfy acceptance cleanup.
