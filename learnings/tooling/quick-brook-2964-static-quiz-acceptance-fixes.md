---
title: "Static quiz acceptance fixes need generated-artifact tests"
date: 2026-05-18
category: tooling
component: frontend
tags: [github-pages, static-deploy, node-test, path-validation, json-manifest]
file_type: rules
---

# Static quiz acceptance fixes need tests around generated artifacts and path guards

When a static GitHub Pages quiz app replaces API discovery with committed JSON artifacts, acceptance checks should cover both the artifact generator and the browser path construction.

## Pattern

- Keep the generator dependency-free and export the planned entry point, for example `buildLevelsIndex(levelsDir, indexPath)`, so Node built-in tests can run against a temporary fixture directory.
- Test that the generator skips an existing `index.json`, sorts newest-first, normalizes metadata, writes the same JSON it returns, and supports explicit directories instead of relying only on repository paths.
- In the browser app, validate any query-derived `levelPath` before static `fetch`: require `.json`, reject leading `/`, URL schemes, `..` segments, and backslashes, then encode each safe path segment.
- If `node quiz/build-index.js` is run in a dirty workspace, regenerated `quiz/levels/index.json` can legitimately reflect unrelated user edits to source level JSON files. Do not revert those source edits; call out the generated-artifact effect instead.

## Verification

Useful focused commands for this repository:

```bash
cd quiz && node --test build-index.test.js
node --check quiz/build-index.js
node --check quiz/app.js
node quiz/build-index.js
```
