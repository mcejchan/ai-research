---
title: "Centralize KB reference rewriting without merging path contracts"
date: 2026-10-23
category: architecture
component: shared
tags: [knowledge-base, refactoring, python, testing]
---

# Centralize KB reference rewriting without merging path contracts

When multiple scripts recursively update references in knowledge-base files, move only the shared traversal and IO loop into a KB-specific helper. Keep each caller's replacement-pattern construction local when their path shapes differ. Preserve case-insensitive extension filtering, ordered replacements, UTF-8 IO, unreadable-file tolerance, changed-only writes, and touched-path results. A focused test can emulate unreadability by patching `Path.read_text`; patching `builtins.open` does not intercept `Path.read_text` on this platform.
