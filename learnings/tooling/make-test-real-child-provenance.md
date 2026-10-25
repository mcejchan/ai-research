---
title: "Make test provenance requires observing the real pytest child"
date: 2026-10-25
category: tooling
component: tooling
tags: [makefile, python, pytest, runtime]
---

# Prove Make test runtime provenance through the real child

When a runtime guard validates a project interpreter before launching a test child, report provenance from the real interpreter itself rather than synthesizing identity in a shell stub. A minimal child module can print `sys.executable`, `platform.python_implementation()`, and `sys.version` while emitting a sentinel. For failure propagation, let the fixture delegate the `-c` identity probe to CPython, then record and fail only the subsequent `-m pytest` invocation.

Keep stale runtime coverage distinct from missing executable coverage: assert expected and observed identities, no ambient fallback, and no test child execution.
