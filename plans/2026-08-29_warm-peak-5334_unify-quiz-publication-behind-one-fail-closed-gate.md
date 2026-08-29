# Plan 2026-08-29: Unify quiz publication behind one fail-closed gate

Define one reusable publication contract that validates all quiz sources, builds the catalog fail-closed, and exercises the static runtime from both local and Pages gates.

*Status: DRAFT*
*Created: 2026-08-29*

## Progress

- [x] Phase 0: Config + Init
- [x] Phase 1: Research
- [x] Phase 2: Knowledge
- [x] Phase 3: Synthesis

## Analysis

### Codebase Context

- `quiz/build-index.js` recursively discovers level JSON, excludes the generated `index.json`, preserves date/path sorting and metadata defaults, but catches read/parse failures per file and writes a partial catalog.
- `quiz/validate-quiz.js` owns the existing structural checks and bias heuristics, combines both into blocking `errors`, reads files internally, and calls `main()` unconditionally, so it is not reusable by the builder.
- `quiz/build-index.test.js` uses temporary directories for builder coverage and also contains the focused static runtime/index integration test through `app.levelUrl`; its fixtures currently characterize metadata defaults rather than complete level structure.
- Root `Makefile:test` runs the quiz test directly alongside unrelated subsystem suites. `.github/workflows/deploy-quiz.yml` independently repeats that test and the tolerant builder before uploading `quiz/`.
- Valid index semantics to preserve are generated JSON formatting, recursive relative paths, generated-index exclusion, newest-date/path sorting, difficulty fallback to `hard`, question count, and summed points.

### Relevant Documentation

- `.architecture-reviews/reports/2026-08-29T080000Z-ai-research.md` requires one thin, fail-closed quiz boundary and explicitly rejects coupling Pages to the root-wide gate.
- `README.md` defines `make test` as authoritative and documents the current difficulty fallback; add the named quiz publication contract beside it.
- `docs/proposals/proposal-20260518-yt-knowledge-quiz.md` defines the static, serverless runtime, one-JSON-per-level schema, generated manifest, and current direct builder command; update its content-pipeline command.
- No relevant PlantUML diagram exists under repository docs.

### Knowledge Base

- `learnings/tooling/keep-repository-health-orchestration-at-root-boundary.md`: keep Make orchestration thin, propagate non-zero statuses, and allow Pages to run only the dependency-free quiz slice.
- `learnings/architecture/self-contained-quiz-dashboard-without-dependencies.md` and `learnings/tooling/cool-brook-0229-static-quiz-generated-manifest.md`: retain static JSON, recursive manifest generation, generated-index exclusion, relative paths, and Node built-ins only.
- `learnings/test-failures/bold-vale-3575-inject-filesystem-roots-for-deterministic-integration-tests.md`: pass temporary level/index roots into tests rather than touching tracked quiz data.
- `learnings/architecture/quiz-level-difficulty-metadata.md`: preserve source difficulty projection and the documented fallback behavior already covered by builder tests.
- `learnings/tooling/final-note-is-an-acceptance-deliverable.md`: implementation evidence must record exact commands, exit codes, outcomes, changed behavior, and follow-ups.
- Recall used the deterministic local backend because QMD collection `ai-research-learnings` was unavailable; this cache miss is non-blocking.
- Baseline check `node quiz/validate-quiz.js quiz/levels` passes all 20 tracked source levels, so no quiz-data migration is expected.

## Available Skills

- `tdd`: implement characterization-first negative tests and retain RED/GREEN proof.
- `validate-implementation`: verify the finished gate against project rules and the publication boundary.
- `save-learning`: mandatory final implementation action after all verification and final-note evidence are complete.

## Solution

- Make `make quiz-publication-check` the only public publication contract: run the focused quiz tests, then regenerate `quiz/levels/index.json`; let either command's non-zero status stop publication.
- Refactor `quiz/validate-quiz.js` into importable parsing/validation functions guarded by `require.main === module`; return structural errors separately from advisory quality/bias findings.
- Make `buildLevelsIndex` fail before writing when discovery, reading, JSON parsing, or structural validation fails; emit advisories without rejecting, then preserve the existing metadata projection and sort for valid sources.
- Keep optional metadata defaults, including unknown difficulty to `hard`; enforce runtime-required question shape as structural: object/title, non-empty questions, question text, `single|multi` type, 1-4 finite points, at least two string options, valid unique integer `correct` indexes, and exactly one correct index for `single`.
- Keep missing explanations, one-answer `multi` questions, and answer-length/position heuristics advisory-only.

## Implementation

1. Apply `skill:tdd`: add `quiz/publication-check.test.js` with temporary directories for malformed JSON, invalid schema, mixed valid/invalid no-omission, and advisory-only fixtures; update `quiz/build-index.test.js` fixtures to satisfy the structural contract while retaining metadata and static runtime assertions; capture RED evidence.
2. Split `quiz/validate-quiz.js` into reusable data validation and file/CLI formatting layers. Preserve explicit parse/not-found exit failures, make only structural errors set a failing result/exit code, and export the shared validator for the builder.
3. Remove the per-file catch and missing-directory tolerance from `quiz/build-index.js`. Parse each discovered source, reject aggregated/path-specific structural failures before `writeFile`, print advisory findings, and retain generated-index exclusion, recursive paths, JSON formatting, sorting, defaults, and metadata calculations.
4. Add `.PHONY: quiz-publication-check` to `Makefile`; have it run `node --test quiz/build-index.test.js quiz/publication-check.test.js` followed by `node quiz/build-index.js`, and make root `test` invoke/depend on that target before unrelated suites.
5. Replace the direct test/build commands in `.github/workflows/deploy-quiz.yml` with `make quiz-publication-check`; keep checkout, Pages setup/upload/deploy, and quiz-only path scope unchanged.
6. Document `make quiz-publication-check` in `README.md` and replace the proposal's direct builder instruction with the shared publication contract.
7. Run focused, publication, root, and workflow-contract verification; run `skill:validate-implementation`; record exact commands, exit codes, and results for the final note.
8. After all implementation and verification work, invoke `skill:save-learning`, save at least one repository learning, and perform no further tool action before the final response.

## Files to Modify

| File | Change |
|---|---|
| `quiz/publication-check.test.js` | Add isolated fail-closed, advisory, and Make/Pages contract tests. |
| `quiz/build-index.test.js` | Keep index/runtime coverage but make source fixtures structurally valid. |
| `quiz/validate-quiz.js` | Expose one structural/advisory validator and keep a thin CLI. |
| `quiz/build-index.js` | Validate every source and reject instead of skipping before index output. |
| `Makefile` | Define and compose `quiz-publication-check`. |
| `.github/workflows/deploy-quiz.yml` | Invoke the shared quiz-only gate. |
| `README.md` | Name the publication command and its blocking/advisory policy. |
| `docs/proposals/proposal-20260518-yt-knowledge-quiz.md` | Point content publication at the shared command. |

## TDD

**Test file:** `quiz/publication-check.test.js`  
**Framework:** Node built-in `node:test`; matches the dependency-free quiz suite.  
**Run command:** `node --test quiz/publication-check.test.js quiz/build-index.test.js`  
**Edit hint:** Create the new file first; separately replace empty questions in `quiz/build-index.test.js` fixtures with valid question objects.

> Implement the TDD cycle with `skill:tdd`; save RED/GREEN evidence to `plans/checkpoints/warm-peak-5334.red-green-proof.md`.

```js
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const { buildLevelsIndex } = require('./build-index');

function validLevel() {
  return {
    title: 'Fixture',
    questions: Array.from({ length: 5 }, (_, index) => ({
      question: `Question ${index}`,
      type: 'single',
      points: 1,
      options: ['The deliberately longest correct answer', 'No'],
      correct: [0],
      explanation: 'Fixture explanation',
    })),
  };
}

async function fixtureRoot() {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'quiz-publication-'));
  const sourceDir = path.join(root, 'levels');
  const indexPath = path.join(sourceDir, 'index.json');
  await fs.mkdir(sourceDir);
  return { root, sourceDir, indexPath };
}

test('malformed source fails without writing a partial index', async (t) => {
  const { root, sourceDir, indexPath } = await fixtureRoot();
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  await fs.writeFile(path.join(sourceDir, 'valid.json'), JSON.stringify(validLevel()));
  await fs.writeFile(path.join(sourceDir, 'broken.json'), '{');

  await assert.rejects(buildLevelsIndex(sourceDir, indexPath), /broken\.json/); // RED: currently resolves after skipping.
  await assert.rejects(fs.access(indexPath), { code: 'ENOENT' });
});

test('schema-invalid source fails publication', async (t) => {
  const { root, sourceDir, indexPath } = await fixtureRoot();
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  await fs.writeFile(path.join(sourceDir, 'invalid.json'), JSON.stringify({ title: 'Invalid', questions: 'no' }));

  await assert.rejects(buildLevelsIndex(sourceDir, indexPath), /questions/); // RED: currently indexes it with zero questions.
});

test('bias findings warn but do not block publication', async (t) => {
  const { root, sourceDir, indexPath } = await fixtureRoot();
  const warnings = [];
  const originalWarn = console.warn;
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  t.after(() => { console.warn = originalWarn; });
  console.warn = (message) => warnings.push(String(message));
  await fs.writeFile(path.join(sourceDir, 'biased.json'), JSON.stringify(validLevel()));

  await assert.doesNotReject(buildLevelsIndex(sourceDir, indexPath));
  assert.ok(warnings.some((warning) => warning.includes('BIAS'))); // RED: builder does not invoke advisory analysis.
});

test('Make and Pages use one quiz publication gate', async () => {
  const makefile = await fs.readFile(path.join(__dirname, '..', 'Makefile'), 'utf8');
  const workflow = await fs.readFile(path.join(__dirname, '..', '.github', 'workflows', 'deploy-quiz.yml'), 'utf8');

  assert.match(makefile, /^quiz-publication-check:/m); // RED: target does not exist.
  assert.match(workflow, /run: make quiz-publication-check/);
  assert.doesNotMatch(workflow, /node --test quiz\/build-index\.test\.js|node quiz\/build-index\.js/);
});
```

| Test | RED | GREEN |
|---|---|---|
| malformed/mixed sources | Builder resolves and writes a catalog without the bad file. | Builder rejects with the source path and writes no index. |
| invalid `questions` schema | Builder creates zero-question metadata. | Shared structural validator rejects before output. |
| advisory-only bias | No advisory is emitted by the builder. | Bias is reported while index generation succeeds. |
| Make/Pages contract | Named target and workflow call are absent. | Root and Pages both reference `quiz-publication-check`; workflow has no duplicate Node sequence. |
| existing valid metadata/runtime tests | Updated strict fixtures may fail until validator/builder integration is complete. | Sorting, projection, fallback, generated-index exclusion, and static `levels/index.json` runtime behavior pass. |

## Verification

- `node --test quiz/publication-check.test.js quiz/build-index.test.js`
- `make quiz-publication-check`
- `make test`
- Use the focused `Make and Pages use one quiz publication gate` test as static proof that `.github/workflows/deploy-quiz.yml` delegates and no longer duplicates the tolerant sequence.
- Record every command's exit code and result in the final note; do not run git, push, PR, or deployment commands.

## Dependencies

- Use only Node built-ins and Make; add no package or external service dependency.
- Treat every source `.json` discovered under `quiz/levels/`, except generated `index.json`, as publication input; CI's checkout supplies the tracked set.
- Keep all work and learning output inside `/Users/michal/Projects/ai-research`.
