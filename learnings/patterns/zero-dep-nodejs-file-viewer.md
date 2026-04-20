---
title: "Zero-dep Node.js file viewer pattern"
date: 2026-04-20
category: patterns
component: tooling
tags: [nodejs, zero-dep, file-viewer, spa]
---

# Zero-dep Node.js file viewer pattern

When building a simple file browser/viewer with Node.js (zero dependencies):

## Key patterns
- Use `URL` constructor for parsing request paths, then regex matching for route params
- Path traversal protection: validate segments contain no `..`, `/`, or `\` before joining with `path.join`
- Single-file SPA with `marked.js` from CDN works well for markdown rendering

## Gotchas
- `fs.promises.readdir` with `{ withFileTypes: true }` avoids extra `stat` calls
- Route regex must be precise — e.g. `([^/]+)` to capture path segments without slashes
- Cache API responses on the client side to avoid redundant fetches when switching tabs
