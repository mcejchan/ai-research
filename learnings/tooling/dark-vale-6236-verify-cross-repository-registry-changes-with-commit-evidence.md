---
title: "Verify cross-repository registry changes with commit evidence"
date: 2026-07-22
category: tooling
component: ci-cd
tags: [registry, test-gate, git, acceptance, cross-repository]
---

The project-level test command lived in an external workspace registry rather than the project repository. Although the project worktree did not show the expected edit, inspecting the registry's file history proved that commit `169c092c98` had already changed the command from pipeline-only `pytest` to `cd ~/Projects/ai-research && make test`. Rewriting the already-correct file would have created unnecessary churn. For cross-repository acceptance work, inspect the owning repository's status, diff, and file history; validate the parsed configuration value exactly; then run the configured command from its intended context. Here, the root gate successfully covered all three suites: quiz, viewer, and transcript pipeline.