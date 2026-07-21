---
title: "Self-contained quiz dashboard without dependencies"
date: 2026-05-18
category: architecture
component: frontend
tags: [vanilla-js, nodejs, static-files, localstorage]
file_type: decisions
---

# Self-contained quiz dashboard without dependencies

For small knowledge-base utilities in this repository, a complete browser app can stay dependency-free with vanilla DOM code, static JSON files, and a generated manifest.

## Pattern used

- Keep dynamic content in plain JSON files under a data directory such as `quiz/levels/`.
- Generate a manifest that recursively scans source JSON and contains only metadata needed by the index screen.
- Fetch selected level JSON directly from a validated relative path in that manifest.
- Keep scoring and user progress client-side with `localStorage` when persistence only needs to be per-browser.

## Important gotchas

- Exclude the generated manifest from recursive source discovery so it cannot index itself.
- Validate manifest paths before fetching them; reject absolute paths, URL schemes, `..`, backslashes, and non-JSON paths.
- With no npm build step, `node --check` is a useful lightweight verification for browser and generator JavaScript syntax.

## Verification

Generate `quiz/levels/index.json`, verify it contains exactly the source-level paths, and run the browser and generator tests with Node's built-in test runner.
