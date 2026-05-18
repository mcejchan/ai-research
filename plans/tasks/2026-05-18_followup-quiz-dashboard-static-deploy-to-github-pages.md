# [acceptance-fix] Quiz Dashboard: Static deploy to GitHub Pages: Add dependency-free `quiz/build-index.js` to generate `quiz/levels/index.json`

Auto-created by the monitor because the original task `cool-brook-0229` was accepted as done
but did not fully meet all acceptance goals.

## Primary goals (from original task)

- Add dependency-free `quiz/build-index.js` to generate `quiz/levels/index.json`
- Add TDD coverage for `quiz/build-index.js`
- Update browser app to use static JSON instead of `/api/*`
- Add GitHub Pages workflow deploying `quiz/` artifact
- Create or update root `README.md` with live quiz link and Pages artifact note
- [P1] Missing static level path validation (`quiz/app.js`) -> Validate `levelPath` before fetch: require `.json`, reject absolute paths, reject `..` path segments, and reject backslashes.
- [P1] Missing planned build-index test file (`quiz/build-index.test.js`) -> Add `quiz/build-index.test.js` using Node built-in tests and include RED/GREEN proof for `node --test build-index.test.js`.
- [P1] Build-index export does not match plan (`quiz/build-index.js`) -> Export `{ buildLevelsIndex }` and support building from an explicit `levelsDir` as planned.
- [P1] Pages workflow lacks manual dispatch (`.github/workflows/deploy-quiz.yml`) -> Add `workflow_dispatch` to the workflow triggers.
- [P1] Root README update missing (`README.md`) -> Create or update root `README.md` with `https://mcejchan.github.io/ai-research/` and note that quiz is deployed from the `quiz/` Pages artifact.

## Additional cleanup (suite-wide)

- [P2] Broader Python test suite has unrelated failures (`youtube-transcript-pipeline/test/test_llm_client.py`) -> Investigate separately; failures are outside the quiz static deploy task.


## Context

- Original task: `cool-brook-0229`
- Reason: `acceptance_incomplete`
- The original task's code changes are preserved. Continue from that state.

## Instructions

Implement the remaining primary goals above first, then handle any listed cleanup items. The original implementation is committed —
build on it, do not revert or redo completed work.

## Important: do not repeat completed work

The previous attempt partially succeeded. Review what is already committed before making changes. Do NOT revert or redo completed work. If the previous approach caused the failure, try a different approach.

## Original plan

Read the original plan at `/Users/michal/Projects/ai-research/plans/2026-05-18_cool-brook-0229_quiz-dashboard-static-deploy-to-github-pages.md` for full context. Focus only on the unmet goals listed above.

## Previous attempt: acceptance context

**Why incomplete:** Core static fetch and Pages artifact deployment are partially implemented, but several explicit plan goals are missing: path validation, test file/TDD execution, expected export shape, manual workflow dispatch, and README update.


**Already done (do NOT redo):**
- Generate and commit baseline `quiz/levels/index.json`
- Keep local server API compatibility while allowing static `levels/*.json`
- Save implementation learning

## Recent learnings from previous attempt


### cool-brook-0229-static-quiz-generated-manifest.md

```
---
title: "Static quiz apps need generated JSON manifests"
date: 2026-05-18
category: tooling
component: frontend
tags: [github-pages, static-deploy, vanilla-js, json-manifest]
file_type: rules
---

# Static quiz apps need a generated manifest and static access to JSON

For a vanilla app deployed as static files, replace dynamic discovery endpoints like `/api/levels` with a committed/generated manifest such as `levels/index.json`.

Key implementation details:
- Generate the manifest from source JSON files with a Node script that uses `__dirname`, so it works from both repository root (`node q
```


### cool-brook-0229-github-pages-subdirectory-apps-need-actions-artifact-deploy.md

```
---
title: "GitHub Pages subdirectory apps need Actions artifact deploy"
date: 2026-05-18
category: tooling
component: ci-cd
tags: [github-pages, github-actions, static-deploy, planning]
file_type: rules
---

# GitHub Pages for subdirectory apps needs Actions artifact, not branch subfolder

When planning a static deploy for a project kept in a repository subdirectory such as `quiz/`, do not assume GitHub Pages can publish directly from `main:/quiz`. Branch-based Pages sources only support the repository root or `/docs`.

Use Pages source `GitHub Actions` instead:

```yaml
- run: node quiz/buil
```

## Implementation session log excerpt (last 50 lines)

```
cal dev.
- Created required proof file: `plans/checkpoints/cool-brook-0229.red-green-proof.md` with both `## RED Phase` and `## GREEN Phase`.
- Updated checkpoint: `plans/checkpoints/cool-brook-0229.checkpoint.md`.
- Saved learning: `learnings/tooling/cool-brook-0229-static-quiz-generated-manifest.md`.

Verification:
- `node build-index.js` passed.
- `node -c app.js && node -c server.js && node -c build-index.js` passed.
- Generated index validation passed: `levels/index.json OK: 6 levels`.
- Confirmed `quiz/app.js` has no `/api/` references.

Broader tests:
- `pytest` failed because command is unavailable.
- `python -m pytest` failed because `python` is unavailable.
- `DRIVE_FOLDER_ID=test python3 -m pytest` ran, with unrelated existing `test_llm_client.py` failures: 37 passed, 4 failed.

```
