---
title: "Pin Make test execution to the project interpreter"
date: 2026-10-25
category: tooling
component: tooling
tags: [makefile, python, pytest, runtime, subprocess]
file_type: rules
---

# Pin Make test execution to the project interpreter

The Makefile’s Python test branch now uses only the project `.venv/bin/python` and validates that it is exactly CPython 3.15.0 before running pytest. A focused synthetic-checkout regression covers hostile `PATH`, a missing interpreter, child `sys.executable` identity, and failure propagation. Reuse this approach when tests or child processes require a specific runtime: resolve and validate the project interpreter explicitly rather than allowing `PATH` to select another Python. Keep external tools such as `yt-dlp` separate when they are not Python dependencies. The focused regression and Node checks passed, but canonical `make test` remains unverified because the host-owned root `.venv` was absent; available CPython 3.15 lacked pytest, and Homebrew blocked the requirements dry run.

## Context
Extracted from task: AI Research Python 3.15: Make test and pipeline child provenance
