---
title: "Safe synthetic Python runtime fixtures"
date: 2026-10-25
category: tooling
component: tooling
tags: [python, pytest, makefile, tdd]
---

# Safe synthetic Python runtime fixtures

When a fixture creates a runtime path as a symlink to a real interpreter, calling `Path.write_text()` at that path follows the symlink and overwrites the host interpreter. Unlink the synthetic path before writing a script replacement, then retain assertions for the expected child arguments and status. If acceptance proof tooling requires a task-scoped RED while the plan explicitly requires reusing a parent RED, report that workflow mismatch; do not fabricate proof or execute a dangerous pre-fix fixture.

Verification environments also matter: CPython 3.15 may be installed without pytest, while the repository's existing global pytest can be an older Python version that triggers runtime-contract test failures. Use an isolated environment with test dependencies for accurate interpreter-specific verification.
