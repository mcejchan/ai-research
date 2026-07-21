---
title: "Static quiz apps need generated JSON manifests"
date: 2026-05-18
category: tooling
component: frontend
tags: [github-pages, static-deploy, vanilla-js, json-manifest]
file_type: rules
---

# Static quiz apps need a generated manifest and static access to JSON

For a vanilla app deployed as static files, use a committed/generated manifest such as `levels/index.json` instead of runtime discovery.

Key implementation details:
- Generate the manifest from source JSON files with a Node script that uses `__dirname`, so it works from both repository root (`node quiz/build-index.js`) and the app directory (`node build-index.js`).
- Exclude the generated `levels/index.json` from the recursive scan to avoid indexing the manifest itself on later runs.
- Store level paths relative to the `levels/` directory, then fetch details with `levels/${path}` from the browser.
- If local development needs HTTP, use a generic static-file server rooted at `quiz/` so it matches GitHub Pages file access.

This keeps source JSON, generated manifest metadata, and static browser reads as the only runtime data path.
