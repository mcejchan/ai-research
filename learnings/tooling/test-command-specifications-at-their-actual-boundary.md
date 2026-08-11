---
title: "Test command specifications at their actual boundary"
date: 2026-08-11
category: tooling
component: tooling
tags: [command-contracts, node-test, knowledge-base, root-test-gate]
file_type: rules
---

# Test command specifications at their actual boundary

In this repository, the knowledge commands under `.claude/commands/` are executable specifications rather than wrappers around a shared library. Missing-artifact behavior therefore cannot be characterized by inventing a parallel implementation: dependency-free Node tests should read those command files and assert explicit, command-specific contracts.

For `analysis_main.md`, each consumer needs a different absence rule that preserves its public purpose: skip and report unavailable sources for synthesis commands, retain index entries without broken links, and stop commands that require an existing analysis draft. Register these specification tests in the root `Makefile`; otherwise focused coverage does not become repository health authority.
