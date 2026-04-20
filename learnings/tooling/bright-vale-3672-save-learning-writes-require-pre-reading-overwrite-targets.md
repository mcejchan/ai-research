---
title: "Save-learning writes require pre-reading overwrite targets"
date: 2026-04-20
category: tooling
component: tooling
tags: [save-learning, read-before-write, overwrite-guard, workflow]
---

The `save-learning` flow failed with `You must read file .../tmp/content.md before overwriting it` because the tooling enforces a read-before-overwrite safeguard. Reuse: if a learning pipeline writes to an existing temp or content file, read that file first or choose a fresh path. Avoid direct overwrites without a preceding read, because the guard will block the write even for intermediary content files.