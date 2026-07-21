---
title: "Quiz levels: difficulty as manifest metadata"
date: 2026-05-18
category: architecture
component: frontend
tags: [quiz, json-manifest, metadata, difficulty]
file_type: checklist
---

# Quiz levels: difficulty as manifest metadata

The quiz dashboard keeps level data in JSON files and renders the level select screen from `quiz/levels/index.json`. If the UI needs a new card attribute such as difficulty, add it to the level JSON schema and to the metadata projected by `quiz/build-index.js`.

## Pattern used

- Store the intended `difficulty` directly in each level JSON; values such as `extra-easy` must remain distinct from `hard`.
- Preserve the source value when projecting metadata into the generated manifest.
- Render badges from manifest metadata on the level select cards only; do not touch quiz scoring or answer flow.

## Verification

- `node --check quiz/build-index.js` and `node --check quiz/app.js` cover syntax because this quiz app has no npm build step.
- Parse all files under `quiz/levels/` with `JSON.parse` after metadata edits.
- Run `node quiz/build-index.js` and verify each manifest item preserves the corresponding source level's `difficulty`.

## Gotcha

Do not infer difficulty from a path or collapse unknown values during manifest generation; the manifest is a projection of source metadata, not a normalization layer.
