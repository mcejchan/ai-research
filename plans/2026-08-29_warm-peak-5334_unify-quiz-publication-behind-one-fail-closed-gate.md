# Plan 2026-08-29: Unify quiz publication behind one fail-closed gate

Define one reusable publication contract that validates all quiz sources, builds the catalog fail-closed, and exercises the static runtime from both local and Pages gates.

*Status: WIP*
*Created: 2026-08-29*

## Progress

- [x] Phase 0: Config + Init
- [x] Phase 1: Research
- [x] Phase 2: Knowledge
- [ ] Phase 3: Synthesis

## Analysis [WIP]

### Codebase Context [DONE]

- `quiz/build-index.js` recursively discovers level JSON, excludes the generated `index.json`, preserves date/path sorting and metadata defaults, but catches read/parse failures per file and writes a partial catalog.
- `quiz/validate-quiz.js` owns the existing structural checks and bias heuristics, combines both into blocking `errors`, reads files internally, and calls `main()` unconditionally, so it is not reusable by the builder.
- `quiz/build-index.test.js` uses temporary directories for builder coverage and also contains the focused static runtime/index integration test through `app.levelUrl`; its fixtures currently characterize metadata defaults rather than complete level structure.
- Root `Makefile:test` runs the quiz test directly alongside unrelated subsystem suites. `.github/workflows/deploy-quiz.yml` independently repeats that test and the tolerant builder before uploading `quiz/`.
- Valid index semantics to preserve are generated JSON formatting, recursive relative paths, generated-index exclusion, newest-date/path sorting, difficulty fallback to `hard`, question count, and summed points.

### Relevant Documentation [DONE]

- `.architecture-reviews/reports/2026-08-29T080000Z-ai-research.md` requires one thin, fail-closed quiz boundary and explicitly rejects coupling Pages to the root-wide gate.
- `README.md` defines `make test` as authoritative and documents the current difficulty fallback; add the named quiz publication contract beside it.
- `docs/proposals/proposal-20260518-yt-knowledge-quiz.md` defines the static, serverless runtime, one-JSON-per-level schema, generated manifest, and current direct builder command; update its content-pipeline command.
- No relevant PlantUML diagram exists under repository docs.

### Knowledge Base [DONE]

- `learnings/tooling/keep-repository-health-orchestration-at-root-boundary.md`: keep Make orchestration thin, propagate non-zero statuses, and allow Pages to run only the dependency-free quiz slice.
- `learnings/architecture/self-contained-quiz-dashboard-without-dependencies.md` and `learnings/tooling/cool-brook-0229-static-quiz-generated-manifest.md`: retain static JSON, recursive manifest generation, generated-index exclusion, relative paths, and Node built-ins only.
- `learnings/test-failures/bold-vale-3575-inject-filesystem-roots-for-deterministic-integration-tests.md`: pass temporary level/index roots into tests rather than touching tracked quiz data.
- `learnings/architecture/quiz-level-difficulty-metadata.md`: preserve source difficulty projection and the documented fallback behavior already covered by builder tests.
- `learnings/tooling/final-note-is-an-acceptance-deliverable.md`: implementation evidence must record exact commands, exit codes, outcomes, changed behavior, and follow-ups.
- Recall used the deterministic local backend because QMD collection `ai-research-learnings` was unavailable; this cache miss is non-blocking.
- Baseline check `node quiz/validate-quiz.js quiz/levels` passes all 20 tracked source levels, so no quiz-data migration is expected.

## Available Skills [DONE]

- `tdd`: implement characterization-first negative tests and retain RED/GREEN proof.
- `validate-implementation`: verify the finished gate against project rules and the publication boundary.
- `save-learning`: mandatory final implementation action after all verification and final-note evidence are complete.

## Solution [TODO]

## Implementation [TODO]

## Files to Modify [TODO]

## TDD [TODO]

## Dependencies [TODO]
