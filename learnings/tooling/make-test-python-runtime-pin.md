---
title: "Make test gate: pin Python runtime explicitly"
date: 2026-10-25
category: tooling
component: tooling
tags: [makefile, python, pytest, runtime]
---

# Pin Make's Python test branch to the project interpreter

The repository test gate must not invoke ambient `python3`: PATH ordering can select an unrelated interpreter. Resolve the checkout's canonical `.venv/bin/python`, verify both CPython implementation and the exact full version before running pytest, and fail with an actionable diagnostic if it is absent or stale. Keeping the pytest command in the same shell recipe preserves cwd and environment assignments.

For Python child processes, preserve ownership explicitly: same-runtime checks should use `sys.executable` and assert the child's observed identity; external tools such as `yt-dlp` remain external executables. A synthetic checkout can test the real Make recipe against hostile PATH stubs without changing the actual Node/quiz gate.

Host-managed virtualenv activation is separate from source implementation. Do not claim runtime compatibility based only on source tests under an older interpreter; record exact interpreter and dependency provenance after host provisioning.
