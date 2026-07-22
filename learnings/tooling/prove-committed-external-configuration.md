---
title: "Prove committed external configuration in task-local evidence"
date: 2026-07-22
category: tooling
component: ci-cd
tags: [acceptance, evidence, git, external-config, test-gate]
file_type: rules
---

# Acceptance Evidence for External Configuration

When a required implementation lives in another Git workspace, confirming its
runtime state is not sufficient for task acceptance. A repository-scoped review
cannot see either a clean external worktree or an assertion in a checkpoint.

For an already-committed external change, add a bounded in-repository evidence
artifact containing:

- the external repository path and full commit SHA;
- the exact path-scoped `git show` command and diff;
- the current delivered configuration entry;
- fresh behavioral verification results;
- links to genuine historical RED/GREEN evidence, including any evidence gaps.

Do not rewrite a correct external configuration merely to produce a fresh diff,
and do not fabricate a new RED after implementation. The committed scoped diff
proves delivery while fresh tests prove current behavior.