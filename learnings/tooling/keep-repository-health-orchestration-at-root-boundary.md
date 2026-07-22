---
title: "Keep repository health orchestration at the root boundary"
date: 2026-07-22
category: tooling
component: ci-cd
tags: [test-gate, makefile, pytest, nodejs, github-actions, configuration]
file_type: rules
---

# Keep repository health orchestration at the root boundary

A mixed repository can have one authoritative health command without merging subsystem test frameworks. Use a small root Make target that invokes each maintained suite with its native runner and lets every non-zero status propagate.

## Project-specific pattern

- Run dependency-free quiz and viewer suites with `node --test`.
- Run the transcript pipeline with `python3 -m pytest`; a bare `pytest` executable is not guaranteed on PATH.
- Pass explicit non-secret test configuration from the delegator, but also move production-secret reads such as `DRIVE_FOLDER_ID` out of module import and into the execution boundary. Test configuration must not conceal an import-time product defect.
- A component-only deployment may run only its own maintained slice when installing every repository dependency would add unrelated credentials or setup. The root command remains the sole repository-wide authority.

## Planning gotcha

`plan-path.py --touch` can return a file that is already seeded. Read or replace that seed rather than applying a context-free append, otherwise the final plan can contain duplicate WIP headers and stale TODO sections.