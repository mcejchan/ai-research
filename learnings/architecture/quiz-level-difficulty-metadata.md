---
title: "Quiz levels: difficulty as API metadata"
date: 2026-05-18
category: architecture
component: frontend
tags: [quiz, api, metadata, difficulty]
file_type: checklist
---

# Quiz levels: difficulty as API metadata

The quiz dashboard keeps level data in JSON files and renders the level select screen from `/api/levels`. If the UI needs a new card attribute such as difficulty, add it in two places: the level JSON schema and the metadata object returned by `getLevels()` in `quiz/server.js`.

## Pattern used

- Store `difficulty` directly in each level JSON as `easy` or `hard`.
- In `/api/levels`, normalize the metadata value so missing or unexpected values default to `hard`.
- Render badges from the API metadata on the level select cards only; do not touch quiz scoring or answer flow.

## Verification

- `node --check server.js` and `node --check app.js` cover syntax because this quiz app has no npm build step.
- Parse all files under `quiz/levels/` with `JSON.parse` after metadata edits.
- Start `quiz/server.js` and validate that every item from `http://localhost:4002/api/levels` includes `difficulty` with either `easy` or `hard`.

## Gotcha

When using a temporary local server for API verification, make sure the background Node process is killed after the curl/fetch check. A hanging helper process can leave port `4002` occupied even when the verification itself succeeded.
