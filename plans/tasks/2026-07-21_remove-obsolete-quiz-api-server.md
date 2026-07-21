# Remove obsolete quiz API server

## Context
The deployed quiz is fully static. `quiz/app.js` reads `levels/index.json` and `levels/<path>`, while `.github/workflows/deploy-quiz.yml` builds the manifest and publishes `quiz/` to GitHub Pages. Commit `8b90375` migrated the browser away from `/api/levels` and `/api/level`, but left `quiz/server.js` behind.

Repository inspection found no maintained caller of `/api/levels`, `/api/level`, or `quiz/server.js`. The retained server has drifted: it scans `index.json` as a level, projects 21 rows for 20 source levels, and maps all four `extra-easy` levels to `hard`. The generated static manifest has exactly 20 paths and preserves all four `extra-easy` values.

## Required change
- Remove `quiz/server.js` and references that specifically document or invoke this obsolete API server.
- Keep source level JSON → `quiz/build-index.js` → static browser reads as the only quiz runtime path.
- If maintained local-development instructions need an HTTP server, use/document a generic static-file server rather than introducing another quiz API.
- Before deletion, perform one bounded repository caller check; do not preserve dead code merely because external use cannot be disproved absolutely.

## Constraints
- Do not change quiz level content, manifest schema, difficulty semantics, or Pages deployment architecture.
- Do not add a replacement application server or compatibility endpoint.
- Do not address the broader project test-gate or tracked `tmp/` findings in this task.

## Acceptance criteria
- `quiz/server.js` is absent.
- Maintained code and documentation contain no active references to `/api/levels`, `/api/level`, or the removed server.
- `quiz/app.js` continues to load the static manifest and level JSON files.
- `quiz/build-index.test.js` and relevant existing quiz tests pass, except any already-observed unrelated baseline failure must be explicitly evidenced rather than hidden or weakened.
- Final diff contains no unrelated cleanup.

## TDD stance
This is dead-code removal protected by characterization. Preserve existing static-path assertions; add a focused test only if current tests do not prove that the browser and build output remain independent of the removed API.

## Verify
- Run the quiz Node test suite.
- Search maintained source/docs for `quiz/server.js`, `/api/levels`, and `/api/level`.
- Build/regenerate the index and verify exact equality between source level paths and `levels/index.json` paths.
