# Plan 2026-05-18: Acceptance Fix YT Knowledge Quiz Dashboard

Implement and prove the missing quiz acceptance goals without changing unrelated repository files.

## Problem

Acceptance evidence must show the self-contained `quiz/` app, `/api/level`, quiz scoring/localStorage behavior, and a RED-GREEN proof; out-of-scope `docs/proposals/...` changes must be absent.

## Analysis

### Kontext z codebase
- `quiz/server.js` already contains a dependency-free Node `http` static server on port `4002`, `/api/levels`, `/api/level?path=...`, recursive JSON discovery, and path normalization.
- `quiz/app.js` already contains level loading, quiz rendering, all-or-nothing selection checks, score persistence under `quiz_scores`, and page dispatch by `body[data-page]`.
- `quiz/index.html`, `quiz/quiz.html`, `quiz/style.css`, and `quiz/levels/.gitkeep` already match the required app shape in the current worktree.
- `git status --short` shows `quiz/` is untracked and several unrelated files are untracked; implementation must stage/touch only the accepted scope.
- `plans/checkpoints/calm-vale-5131.checkpoint.md` exists; `plans/checkpoints/calm-vale-5131.red-green-proof.md` is missing.

### Relevantní dokumentace
- `plans/2026-05-18_build-yt-knowledge-quiz-dashboard.md`: original contract for files, endpoints, UI, scoring, dark responsive design, and no dependencies.
- No `docs/**/*.puml` diagrams found for this feature.

### Knowledge base
- `learnings/architecture/self-contained-quiz-dashboard-without-dependencies.md`: keep JSON levels under `quiz/levels/`, expose list/detail endpoints, use `localStorage` for browser-only progress, validate paths before joining, and use `node --check` for no-build verification.
- `learnings/patterns/zero-dep-nodejs-file-viewer.md`: use `URL`, precise route handling, `fs.promises.readdir(..., { withFileTypes: true })`, and traversal protection.
- `learnings/tooling/yt-viewer-stale-dev-server-can-invalidate-localhost-verification.md`: verify port `4002` is not serving stale code before trusting curl smoke checks.

## Available Skills
- `tdd`: use first during implementation; create RED tests, implement, then record GREEN evidence.
- `save-learning`: run after implementation, as required by the task instructions.
- `validate-implementation`: optional after GREEN to confirm scope and acceptance evidence.

## Solutions

Use the existing `quiz/` implementation as the base, then add testability seams only where needed:
- Refactor `quiz/server.js` to export `createServer`, `getLevels`, and `safeLevelPath`, and start listening only under `if (require.main === module)`.
- Refactor `quiz/app.js` to export pure helpers for Node tests and guard browser bootstrapping with `typeof document !== 'undefined'`.
- Add `quiz/test/quiz.test.js` using built-in `node:test`; no npm dependencies, no framework, no build step.
- Add the mandated proof at `plans/checkpoints/calm-vale-5131.red-green-proof.md`; treat this as the only allowed non-`quiz/` implementation artifact besides this plan.
- Confirm there is no diff under `docs/proposals/`; if present, exclude it from the final changes rather than editing it.

## Implementation

### Pre-implementation checklist
- [ ] Run `git status --short` and note unrelated files; do not edit or stage them.
- [ ] Keep all app changes under `quiz/`; only the RED-GREEN proof may be written outside `quiz/`.
- [ ] Do not add npm dependencies, TypeScript, bundlers, or frameworks.
- [ ] Verify no `docs/proposals/...` changes remain in the final diff.

### Kroky implementace
1. Create `quiz/test/quiz.test.js` from the TDD skeleton below.
2. Run `cd quiz && node --test test/quiz.test.js` and record RED failures in `plans/checkpoints/calm-vale-5131.red-green-proof.md`.
3. Update `quiz/server.js` minimally: `createServer({ rootDir, levelsDir })`, exported helpers, `require.main` listener guard, unchanged runtime port `4002`.
4. Update `quiz/app.js` minimally: export `sameSelection`, `getScores`, `saveScore`; guard browser dispatch; keep `quiz_scores` payload shape unchanged.
5. Ensure `quiz/index.html`, `quiz/quiz.html`, `quiz/style.css`, and `quiz/levels/.gitkeep` remain present and aligned with the original contract.
6. Run `cd quiz && node --test test/quiz.test.js`, `node --check server.js`, and `node --check app.js`; append GREEN evidence to the proof file.
7. Start a fresh server on port `4002`, smoke test `/`, `/quiz.html`, `/api/levels`, and `/api/level?path=<fixture>` if a temporary fixture is added during tests; stop the server after verification.
8. Run `git status --short` and `git diff -- docs/proposals` to prove scope cleanup.
9. Run `save-learning` and save at least one concise learning from the acceptance-fix session.

## Files to Modify

| Soubor | Změna |
|--------|-------|
| `quiz/server.js` | Export testable server factory/helpers; keep dependency-free runtime behavior and `/api/level`. |
| `quiz/app.js` | Export scoring helpers; guard browser-only bootstrapping; keep UI behavior and `quiz_scores`. |
| `quiz/test/quiz.test.js` | New built-in Node tests for endpoint behavior and scoring/localStorage helpers. |
| `quiz/index.html` | Only adjust if current level cards miss metadata, played indicator, or click-through. |
| `quiz/quiz.html` | Only adjust if current quiz screen misses progress, thumbnail, feedback, results, or back button. |
| `quiz/style.css` | Only adjust if current dark responsive tech design fails acceptance. |
| `quiz/levels/.gitkeep` | Ensure the empty level directory is tracked. |
| `plans/checkpoints/calm-vale-5131.red-green-proof.md` | Required RED-GREEN proof for original accepted task. |

## TDD

**Workflow pro implementujícího agenta:**
1. Implementace TDD cyklu dle skill:tdd.
2. Create the test file below before changing app code.
3. Run the targeted test and record RED.
4. Implement only the minimal code needed for GREEN.
5. Record GREEN and smoke-check evidence in `plans/checkpoints/calm-vale-5131.red-green-proof.md`.

### Targeted Tests

**Test file:** `quiz/test/quiz.test.js`  
**Framework:** Node built-in `node:test` and `assert`; dependency-free repo utility.  
**Run command:** `cd quiz && node --test test/quiz.test.js`  
**Edit hint:** NEW FILE.

```js
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const quizRoot = path.resolve(__dirname, '..');

function loadAppModule(localStorage) {
  const source = fs.readFileSync(path.join(quizRoot, 'app.js'), 'utf8');
  const sandbox = {
    console,
    fetch: async () => { throw new Error('fetch should not run in helper tests'); },
    localStorage,
    module: { exports: {} },
    exports: {},
  };
  vm.runInNewContext(source, sandbox, { filename: 'app.js' });
  return sandbox.module.exports;
}

function memoryStorage(initial = {}) {
  const data = { ...initial };
  return {
    getItem(key) { return Object.prototype.hasOwnProperty.call(data, key) ? data[key] : null; },
    setItem(key, value) { data[key] = String(value); },
  };
}

test('GET /api/level returns a requested nested level JSON', async (t) => {
  const { createServer } = require('../server.js');
  assert.equal(typeof createServer, 'function'); // RED: current server starts immediately and exports nothing.

  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'quiz-levels-'));
  const channelDir = path.join(temp, 'channel');
  fs.mkdirSync(channelDir);
  fs.writeFileSync(path.join(channelDir, 'slug.json'), JSON.stringify({
    title: 'Fixture Level',
    channel: 'Fixture Channel',
    thumbnail: 'https://example.test/thumb.jpg',
    date: '2026-05-18',
    questions: [{ question: 'Pick one', type: 'single', points: 2, options: ['A', 'B'], correct: [1] }],
  }));

  const server = createServer({ rootDir: quizRoot, levelsDir: temp });
  t.after(() => server.close());
  await new Promise((resolve) => server.listen(0, resolve));
  const { port } = server.address();

  const response = await fetch(`http://127.0.0.1:${port}/api/level?path=channel%2Fslug.json`);
  assert.equal(response.status, 200);
  const body = await response.json();
  assert.equal(body.title, 'Fixture Level');
  assert.equal(body.questions[0].points, 2);
});

test('GET /api/level rejects traversal paths', async (t) => {
  const { createServer } = require('../server.js');
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'quiz-levels-'));
  const server = createServer({ rootDir: quizRoot, levelsDir: temp });
  t.after(() => server.close());
  await new Promise((resolve) => server.listen(0, resolve));

  const response = await fetch(`http://127.0.0.1:${server.address().port}/api/level?path=..%2Fsecret.json`);
  assert.equal(response.status, 400);
});

test('sameSelection scores single and multi answers all-or-nothing', () => {
  const helpers = loadAppModule(memoryStorage());
  assert.equal(typeof helpers.sameSelection, 'function'); // RED: helper is not exported yet.
  assert.equal(helpers.sameSelection([2], [2]), true);
  assert.equal(helpers.sameSelection([0, 2], [0, 2]), true);
  assert.equal(helpers.sameSelection([0, 1, 2], [0, 2]), false);
  assert.equal(helpers.sameSelection([2, 0], [0, 2]), true);
});

test('saveScore stores quiz_scores best score without lowering it', () => {
  const storage = memoryStorage();
  const helpers = loadAppModule(storage);
  assert.equal(typeof helpers.saveScore, 'function');

  helpers.saveScore('channel/slug.json', 3, 5);
  helpers.saveScore('channel/slug.json', 2, 5);
  helpers.saveScore('channel/slug.json', 4, 5);

  const saved = JSON.parse(storage.getItem('quiz_scores'));
  assert.equal(saved['channel/slug.json'].best, 4);
  assert.equal(saved['channel/slug.json'].max, 5);
  assert.match(saved['channel/slug.json'].date, /^\d{4}-\d{2}-\d{2}T/);
});
```

| Test | RED (před impl) | GREEN (po impl) |
|------|------|-------|
| `GET /api/level returns a requested nested level JSON` | `createServer` missing or `server.js` starts a listener on import. | Returns fixture JSON with status `200`. |
| `GET /api/level rejects traversal paths` | No exported factory or traversal handling not testable. | Returns status `400` for `../secret.json`. |
| `sameSelection scores single and multi answers all-or-nothing` | `app.js` helper not exported or browser bootstrap touches `document`. | Single/multi selections compare exactly as required. |
| `saveScore stores quiz_scores best score without lowering it` | `saveScore` not exported or `localStorage` helper not testable. | Best score is retained and then improved under `quiz_scores`. |

### Regression
- [ ] `cd quiz && node --test test/quiz.test.js`
- [ ] `cd quiz && node --check server.js && node --check app.js`
- [ ] `cd quiz && node server.js` then smoke `http://localhost:4002/`, `/quiz.html`, `/api/levels`, and `/api/level?path=...`
- [ ] `git diff -- docs/proposals` returns no changes.

## Dependencies

- Node.js version must provide built-in `node:test` and global `fetch`.
- No npm install is required.
- `quiz/levels/` may remain empty for normal app acceptance; tests create temporary level data outside the repo.

---
*Vytvořeno: 2026-05-18*
*Status: DRAFT*
