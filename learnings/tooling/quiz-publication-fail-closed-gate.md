---
title: "Jedna fail-closed hranice pro publikaci kvizu"
date: 2026-08-29
category: tooling
component: ci-cd
tags: [quiz, publication, validation, makefile, github-pages]
file_type: decisions
---

# One fail-closed boundary for static quiz publication

The quiz catalog must not treat source discovery, validation, and index generation as separate best-effort steps. `make quiz-publication-check` is the repository-owned boundary: it runs focused runtime/index tests and then builds the catalog from every discovered source level.

## Practical pattern

- Keep structural validation in an importable data-level function so both the CLI and builder use one schema definition.
- Separate blocking `structuralErrors` from non-blocking `advisories`; bias and answer-quality heuristics should be visible without changing deployment status.
- Accumulate path-specific read, parse, and schema failures and throw before writing the generated index. Per-file catches that continue are unsafe because they turn malformed input into a successful partial deployment.
- Test with temporary level roots and assert that mixed valid/invalid input rejects and leaves no generated index.
- Let root `make test` depend on the focused target, while Pages invokes only the focused target so static publication is not coupled to unrelated Python or viewer suites.

This preserves generated index formatting, sorting, metadata defaults, and static runtime behavior for valid inputs while making omission impossible on a successful publication run.
