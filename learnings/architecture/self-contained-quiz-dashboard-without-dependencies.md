---
title: "Self-contained quiz dashboard without dependencies"
date: 2026-05-18
category: architecture
component: frontend
tags: [vanilla-js, nodejs, static-server, localstorage]
file_type: decisions
---

# Self-contained quiz dashboard without dependencies

For small knowledge-base utilities in this repository, a complete browser app can stay dependency-free by pairing a tiny Node.js `http` server with vanilla DOM code.

## Pattern used

- Keep dynamic content in plain JSON files under a data directory such as `quiz/levels/`.
- Expose a listing endpoint that recursively scans JSON files and returns only metadata needed by the index screen.
- Expose a detail endpoint that returns one JSON file by a normalized relative path.
- Keep scoring and user progress client-side with `localStorage` when persistence only needs to be per-browser.

## Important gotchas

- Normalize and validate API file paths before joining them with the data directory; reject absolute paths, `..`, backslashes, and non-JSON paths.
- Static serving should not expose the raw data directory if the API is intended to be the access layer.
- With no npm build step, `node --check` is a useful lightweight verification for server and browser JS syntax.

## Verification

For an empty levels directory, `/api/levels` should still return a valid JSON list (`[]`) so the UI can render an empty state cleanly.
