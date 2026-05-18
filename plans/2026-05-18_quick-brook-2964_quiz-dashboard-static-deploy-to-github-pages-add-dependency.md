# Plan 2026-05-18: Quiz Dashboard Static Deploy Acceptance Fix

Close the remaining acceptance gaps from `cool-brook-0229` without redoing the already committed static quiz work.

## Analysis

### Kontext z codebase
- `quiz/build-index.js`: already generates `levels/index.json`, but exports `{ buildIndex, levelFromJson }`; change to export `{ buildLevelsIndex }` and accept explicit `levelsDir` plus optional `indexPath`.
- `quiz/build-index.js`: `walkJsonFiles()` currently skips only the repo default `INDEX_PATH`; make skip relative to the explicit `levelsDir` so temp-dir tests cannot index their own `index.json`.
- `quiz/app.js`: already uses `levels/index.json` and `levelUrl(levelPath)`, but `levelUrl()` only strips leading slashes; add validation before fetch: require `.json`, reject absolute paths, reject `..` segments, reject backslashes.
- `.github/workflows/deploy-quiz.yml`: already deploys `quiz/` artifact and runs `node quiz/build-index.js`; add `workflow_dispatch` under `on`.
- `README.md`: missing at repo root; create it with `https://mcejchan.github.io/ai-research/` and note the site is deployed from the `quiz/` Pages artifact.
- `quiz/build-index.test.js`: missing; add dependency-free Node built-in test file.

### Relevantní dokumentace
- `plans/2026-05-18_cool-brook-0229_quiz-dashboard-static-deploy-to-github-pages.md`: original accepted plan; reuse only incomplete steps, especially TDD proof and static path validation.
- `docs/proposals/proposal-20260518-yt-knowledge-quiz.md`: keep vanilla HTML/JS/CSS, localStorage scoring, one JSON per level, chronological level ordering, no UI/scoring redesign.

### Knowledge base
- `learnings/tooling/cool-brook-0229-static-quiz-generated-manifest.md`: use `__dirname`, support `node quiz/build-index.js` and `cd quiz && node build-index.js`, skip generated `levels/index.json`, keep static access to `levels/*.json`.
- `learnings/tooling/cool-brook-0229-github-pages-subdirectory-apps-need-actions-artifact-deploy.md`: deploy `quiz/` as Pages artifact root; URL is `https://mcejchan.github.io/ai-research/`, not `/quiz/`.
- `learnings/tooling/acceptance-fix-proof-artifacts.md`: create RED/GREEN proof before production edits; keep focused quiz verification separate from broader unrelated failures.
- `learnings/test-failures/cool-cove-5127-repository-wide-test-runs-can-expose-unrelated-environment-coupled-failures.md`: treat existing `youtube-transcript-pipeline/test/test_llm_client.py` failures as out of scope unless changed.
- `learnings/tooling/dark-vale-9814-use-targeted-node-syntax-checks-for-small-script-based-uis-without-package-tooli.md`: use `node --check` and targeted Node commands; do not invent npm tooling.

## Available Skills
- `tdd`: use first during implementation for `quiz/build-index.test.js` and `plans/checkpoints/quick-brook-2964.red-green-proof.md`.
- `validate-implementation`: use after implementation to check acceptance coverage and static deploy path assumptions.
- `save-learning`: mandatory final implementation action after all verification.

## Solutions
- Keep current static manifest approach; patch only export shape, explicit directory support, path validation, workflow trigger, README, and missing tests.
- Do not modify quiz UI, scoring, level JSON schema, existing static deploy artifact path, or local API compatibility.
- Do not fix unrelated Python suite failures; rerun or document them only as separate cleanup evidence.

## Implementation

1. Start TDD via `skill:tdd`; create `plans/checkpoints/quick-brook-2964.red-green-proof.md` with `## RED Phase` before production edits.
2. Add `quiz/build-index.test.js` from the TDD skeleton and run `cd quiz && node --test build-index.test.js`; record RED failure.
3. Patch `quiz/build-index.js`:
   - Rename public function to `buildLevelsIndex(levelsDir = LEVELS_DIR, indexPath = path.join(levelsDir, 'index.json'))`.
   - Pass `levelsDir` and `indexPath` into helper logic instead of relying on global `LEVELS_DIR`/`INDEX_PATH` for relative paths and index skipping.
   - Preserve metadata shape, date desc sort with path tie-breaker, `easy` else `hard`, `questionCount`, `maxPoints`, pretty JSON plus newline.
   - Export exactly `{ buildLevelsIndex }`; CLI calls `buildLevelsIndex()` and logs the written default index path.
4. Patch `quiz/app.js`:
   - Add pure `validateLevelPath(levelPath)` or make `levelUrl()` perform strict validation.
   - Reject missing/non-string values, absolute URL/path values (`/x`, `http://`, protocol-relative `//x`), non-`.json`, any `..` path segment, and backslash characters (`\\`).
   - Keep valid nested paths encoded as `levels/<encoded segments>`.
   - Export validation helper with `levelUrl` for focused Node assertions.
5. Patch `.github/workflows/deploy-quiz.yml` with `workflow_dispatch:` while keeping push trigger and `path: quiz` artifact upload.
6. Create root `README.md` with the live link `https://mcejchan.github.io/ai-research/` and a one-line note that GitHub Pages deploys the `quiz/` directory as the Pages artifact root.
7. Run `node quiz/build-index.js`; include any deterministic `quiz/levels/index.json` update only if output changes.
8. Record GREEN proof with exact commands and outcomes; run `save-learning` as the last implementation action.

## Files to Modify

| Soubor | Změna |
|--------|-------|
| `quiz/build-index.test.js` | New Node built-in tests for explicit `levelsDir`, sorted metadata, generated `index.json`, and skip behavior. |
| `quiz/build-index.js` | Export `{ buildLevelsIndex }`; support explicit dirs; keep dependency-free CLI. |
| `quiz/app.js` | Add strict level path validation before static JSON fetch. |
| `.github/workflows/deploy-quiz.yml` | Add `workflow_dispatch`. |
| `README.md` | Add live Pages link and `quiz/` artifact note. |
| `quiz/levels/index.json` | Regenerate only if `node quiz/build-index.js` changes deterministic output. |
| `plans/checkpoints/quick-brook-2964.red-green-proof.md` | RED/GREEN evidence for this acceptance fix. |

## TDD

**Workflow pro implementujícího agenta:**
1. Implementace TDD cyklu dle skill:tdd.
2. Create `quiz/build-index.test.js` exactly before production edits.
3. Run targeted test and record RED in `plans/checkpoints/quick-brook-2964.red-green-proof.md`.
4. Implement production changes.
5. Run targeted test and record GREEN.

### Targeted Tests

**Test file:** `quiz/build-index.test.js`  
**Framework:** Node built-in `node:test`, no dependencies.  
**Run command:** `cd quiz && node --test build-index.test.js`  
**Edit hint:** NEW FILE

```js
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const { buildLevelsIndex } = require('./build-index');

test('buildLevelsIndex writes sorted static metadata and skips existing index', async () => {
  const levelsDir = await fs.mkdtemp(path.join(os.tmpdir(), 'quiz-levels-'));
  const channelDir = path.join(levelsDir, 'futurecast');
  const indexPath = path.join(levelsDir, 'index.json');
  await fs.mkdir(channelDir, { recursive: true });
  await fs.writeFile(indexPath, JSON.stringify([{ path: 'stale.json' }]));
  await fs.writeFile(path.join(channelDir, 'old.json'), JSON.stringify({
    title: 'Old', channel: 'FutureCast', thumbnail: 'old.jpg', date: '2024-01-01', difficulty: 'easy',
    questions: [{ points: 1 }, { points: 2 }]
  }));
  await fs.writeFile(path.join(channelDir, 'new.json'), JSON.stringify({
    title: 'New', channel: 'FutureCast', thumbnail: 'new.jpg', date: '2026-05-18', difficulty: 'weird',
    questions: [{ points: 4 }]
  }));

  const levels = await buildLevelsIndex(levelsDir, indexPath);
  const written = JSON.parse(await fs.readFile(indexPath, 'utf8'));

  assert.deepEqual(levels.map((level) => level.path), ['futurecast/new.json', 'futurecast/old.json']);
  assert.deepEqual(written, levels);
  assert.equal(levels[0].difficulty, 'hard');
  assert.equal(levels[0].questionCount, 1);
  assert.equal(levels[0].maxPoints, 4);
  assert.equal(levels[1].difficulty, 'easy');
  assert.equal(levels[1].maxPoints, 3);
});
```

| Test | RED | GREEN |
|------|-----|-------|
| `buildLevelsIndex writes sorted static metadata and skips existing index` | `buildLevelsIndex is not a function` or temp `index.json` is incorrectly included | Returns two sorted level entries, writes same JSON to explicit `indexPath`, skips stale manifest, normalizes metadata. |

### Regression
- [ ] `cd quiz && node --test build-index.test.js`
- [ ] `node --check quiz/build-index.js`
- [ ] `node --check quiz/app.js`
- [ ] `node --check quiz/server.js`
- [ ] `node quiz/build-index.js`
- [ ] `node -e "const { levelUrl } = require('./quiz/app.js'); const assert = require('node:assert/strict'); assert.equal(levelUrl('channel/video.json'), 'levels/channel/video.json'); for (const bad of ['http://x/y.json','//x/y.json','/x.json','../x.json','x/../y.json','x\\y.json','x.txt']) assert.throws(() => levelUrl(bad));"`
- [ ] `python3 -m pytest` or `DRIVE_FOLDER_ID=test python3 -m pytest`; if `test_llm_client.py` still fails, document as unrelated cleanup and do not fix in this task.

## Dependencies
- GitHub Pages repository setting must use `GitHub Actions` source.
- Keep artifact root as `quiz/`; live URL remains `https://mcejchan.github.io/ai-research/`.
- Keep app dependency-free; no `package.json`, npm packages, bundler, or test runner dependency.
- Mandatory final implementation action: run `save-learning` and save at least one learning file.

---
*Status: DRAFT*
*Vytvořeno: 2026-05-18*
