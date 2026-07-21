# Plan 2026-07-21: Remove obsolete quiz API server

*Status: WIP*
*Created: 2026-07-21*

## Progress

- [x] Phase 0: Config + init
- [x] Phase 1: Research
- [x] Phase 2: Knowledge
- [x] Phase 3: Synthesis

## Analysis

### Codebase context [DONE]

- `quiz/app.js:121` reads `levels/index.json`; `quiz/app.js:269-277` validates a manifest path and reads `levels/<encoded path>`.
- `quiz/build-index.js` recursively projects source level JSON into `quiz/levels/index.json`, explicitly excluding the generated index.
- `.github/workflows/deploy-quiz.yml:29-38` runs the index builder and uploads only `quiz/` as a Pages artifact.
- `quiz/server.js` is a duplicate runtime path: it exposes both API routes, includes `index.json` in discovery, and collapses every non-`easy` difficulty to `hard`.
- `quiz/build-index.test.js` characterizes generated-path ordering and index exclusion, but does not prove the browser is API-independent or that `server.js` is absent.
- Commit `8b90375` changed both browser API reads to static files while retaining `quiz/server.js`.

### Relevant documentation [DONE]

- `README.md` already documents GitHub Pages deployment and needs no server-related edit.
- `docs/proposals/proposal-20260518-yt-knowledge-quiz.md:24-25,41,83` still specifies a standalone server, port, server file, and dynamic directory discovery; revise only those stale architecture statements to the generated-manifest path.
- Historical files under `plans/`, `plans/tasks/`, and `tmp/` contain old API references but are records or separately scoped artifacts, not maintained runtime documentation; leave them unchanged.

### Knowledge base [TODO]

- `learnings/tooling/cool-brook-0229-static-quiz-generated-manifest.md`: keep source JSON -> generated manifest -> static detail reads as the sole data path; exclude `index.json` from generation.
- `learnings/tooling/quick-brook-2964-static-quiz-acceptance-fixes.md`: cover both generator output and browser path construction with dependency-free Node tests.
- `learnings/tooling/cool-brook-0229-github-pages-subdirectory-apps-need-actions-artifact-deploy.md`: preserve Actions artifact deployment because Pages cannot publish directly from `main:/quiz`.
- `learnings/tooling/wild-crag-7582-acceptance-fixes-keep-corrective-diffs-scoped.md`: leave unrelated dirty files, historical plans, and tracked `tmp/` findings untouched; do not fabricate RED evidence.
- QMD collection `ai-research-learnings` is unavailable; fallback search identified several durable learnings that still actively prescribe the removed quiz server and must be corrected with the deletion.

## Available Skills [DONE]

- `tdd`: record RED/GREEN evidence for the focused static-runtime characterization before deleting the server.
- `validate-implementation`: check scope, architecture, and acceptance criteria after edits.
- `save-learning`: mandatory final action after implementation and verification.

## Implementation

1. Run one bounded pre-deletion caller check over maintained paths: `git grep -nE 'quiz/server\.js|/api/levels|/api/level|node( +quiz)?/server\.js|node +server\.js' -- quiz docs learnings README.md .github helper-scripts`; classify only `quiz/server.js` and stale documentation as matches, and stop if a real caller appears.
2. Apply `skill:tdd`: append the focused characterization below to `quiz/build-index.test.js`, run its name-filtered command, and record RED from the still-present `quiz/server.js`.
3. Delete `quiz/server.js`; do not add an application server, compatibility route, or local-server wrapper.
4. Update current quiz architecture documentation to name `quiz/build-index.js`, `quiz/levels/index.json`, and browser static reads; remove obsolete port/server/API instructions. Do not edit historical `plans/**`, task records, or `tmp/**`.
5. Update reusable learnings that actively invoke the quiz server: convert quiz-specific guidance to the static manifest path, remove server syntax/smoke commands, and retain generic server guidance only where it no longer claims to be the quiz runtime.
6. Run the focused GREEN test, full quiz suite, syntax checks, index regeneration/equality check, and maintained-path reference search. Preserve exact evidence for the known difficulty assertion failure and inspect the final diff for only planned files.
7. Run `skill:validate-implementation`, then invoke `skill:save-learning` and save at least one learning file as the final action.

## Files to Modify

| File | Change |
|---|---|
| `quiz/server.js` | Delete the obsolete API/static application server. |
| `quiz/build-index.test.js` | Add one static-runtime characterization that is RED while the server file exists. |
| `docs/proposals/proposal-20260518-yt-knowledge-quiz.md` | Replace standalone-server, port, file-tree, and dynamic-discovery statements with the generated manifest and Pages-compatible static flow. |
| `learnings/architecture/self-contained-quiz-dashboard-without-dependencies.md` | Replace active endpoint/server guidance with the dependency-free static quiz architecture. |
| `learnings/architecture/quiz-level-difficulty-metadata.md` | Point difficulty metadata guidance and verification at source JSON and the generated manifest without changing semantics. |
| `learnings/patterns/calm-vale-5131-use-a-dependency-free-node-static-server-for-isolated-feature-drops.md` | Remove the obsolete quiz/API example while retaining only reusable generic-server guidance. |
| `learnings/tooling/cool-brook-0229-static-quiz-generated-manifest.md` | Remove API-compatibility wording and document generic static serving when local HTTP is needed. |
| `learnings/tooling/quick-brook-2964-static-quiz-acceptance-fixes.md` | Remove the deleted server's syntax-check command. |
| `learnings/tooling/testable-vanilla-browser-helpers-for-acceptance-evidence.md` | Replace obsolete endpoint/server smoke guidance with static browser and manifest checks. |
| `learnings/tooling/acceptance-fix-proof-artifacts.md` | Make its quiz verification example use the actual static runtime rather than a live application server. |

## TDD

Implement the cycle with `skill:tdd` and write RED/GREEN evidence to `plans/checkpoints/calm-wave-0187.red-green-proof.md`.

**Test file:** `quiz/build-index.test.js`  
**Framework:** Node built-in `node:test`  
**Run command:** `node --test --test-name-pattern='quiz runtime is static and has no application server' quiz/build-index.test.js`  
**Edit:** add the `app.js` import beside the existing build import and append this test.

```js
const { levelUrl } = require('./app');

test('quiz runtime is static and has no application server', async () => {
  const appSource = await fs.readFile(path.join(__dirname, 'app.js'), 'utf8');

  await assert.rejects(
    fs.access(path.join(__dirname, 'server.js')),
    { code: 'ENOENT' }, // RED: server.js still exists before deletion.
  );
  assert.match(appSource, /fetchJson\('levels\/index\.json'\)/);
  assert.doesNotMatch(appSource, /\/api\/levels?\b/);
  assert.equal(levelUrl('channel/level.json'), 'levels/channel/level.json');
});
```

| Test | RED | GREEN |
|---|---|---|
| `quiz runtime is static and has no application server` | `assert.rejects` fails because `fs.access(quiz/server.js)` resolves. | The file is absent; manifest fetch, static level URL, and no-API assertions pass. |

The existing generator test remains unchanged. Its current unrelated baseline is `quiz/build-index.test.js:36`, where actual difficulty `weird` does not equal expected `hard`; record this full-suite failure without changing level content, difficulty projection, or the assertion.

## Verification

- `node --test --test-name-pattern='quiz runtime is static and has no application server' quiz/build-index.test.js`
- `node --test quiz/*.test.js` and explicitly capture the known `build-index.test.js:36` baseline if it remains the only failure.
- `node --check quiz/app.js && node --check quiz/build-index.js`
- `node quiz/build-index.js`, then compare the sorted recursive source JSON paths (excluding `levels/index.json`) with every `path` in `quiz/levels/index.json`; require exact equality and 20 entries without editing level content or schema.
- `git grep -nE 'quiz/server\.js|/api/levels|/api/level|node( +quiz)?/server\.js|node +server\.js' -- quiz docs learnings README.md .github helper-scripts` must return no maintained matches.
- `git diff --check` and `git diff -- quiz docs learnings .github README.md` must show only the deletion, characterization, and directly stale documentation edits; inspect any regenerated index diff rather than reverting unrelated source-level changes.

*Status: DRAFT*
