---
title: "Characterization-first quiz validator decomposition"
date: 2026-10-23
category: architecture
component: frontend
tags: [quiz, validator, refactoring, testing]
file_type: rules
---

# Characterization-first plan for validator decomposition

When decomposing a public validator whose output includes ordered diagnostics, advisory-only findings, and statistics, pin representative complete results before extracting helpers. Keep public API result construction and early returns under direct tests; test threshold boundaries and malformed-input exclusions explicitly. Existing integration tests may verify publication behavior, but a focused validator test file gives more precise regression signals for diagnostic and counter semantics.

For the quiz pipeline, Node's built-in `node:test` is already used, and `build-index.js` is a direct consumer of `validateLevelData`. Therefore, characterization belongs beside the quiz source and should preserve the distinction between structural errors that block indexing and advisories that only warn.
