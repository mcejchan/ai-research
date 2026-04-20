---
title: "Verify test tooling exists before running unrelated suite"
date: 2026-04-20
category: tooling
component: tooling
tags: [pytest, environment, verification, venv]
---

Attempting to run `pytest` in `youtube-transcript-pipeline` failed with `zsh:1: command not found: pytest` because the Python test environment was not available in the current shell. Reuse: before invoking repo tests from an implementation task, confirm the required runtime or virtualenv exists and that the suite is relevant to the change. Avoid treating missing test tooling as a product failure when the task only added a separate Node-based utility.