---
title: "Keep copied reference CSS isolated from responsive shell rules"
date: 2026-04-21
category: tooling
component: frontend
tags: [viewer, css, responsive, markdown, source-of-truth]
---

# Keep copied reference CSS isolated from responsive shell rules

When a task says a viewer must match another viewer's markdown rendering exactly, the most reliable implementation is to copy the reference selectors verbatim and render markdown inside an inner wrapper that owns those classes.

## What worked

- Read the live target file and the external reference file side by side before editing.
- Copy the markdown selector block exactly instead of approximating colors, spacing, or typography.
- Keep responsive layout CSS on outer shell containers and render markdown inside a child wrapper like `<div class="markdown-content">...</div>`.

## Gotcha

Applying mobile padding or font-size overrides directly to the same element that carries the copied markdown class breaks the "match exactly" requirement even if the copied CSS text is present.

## Reusable rule

If a single-page viewer needs both responsive shell changes and exact markdown parity with another app, separate them into:

1. Outer container/layout state for navigation and sizing.
2. Inner markdown wrapper for verbatim copied presentation rules.

That keeps the shell flexible without drifting from the style source of truth.
