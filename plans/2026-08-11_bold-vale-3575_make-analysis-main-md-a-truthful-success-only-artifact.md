# Plan 2026-08-11: Make analysis_main.md a truthful success-only artifact

*Status: WIP*
*Created: 2026-08-11*

## Progress

- [x] Phase 0: Config + init
- [x] Phase 1: Research
- [x] Phase 2: Knowledge
- [ ] Phase 3: Synthesis

## Analysis [WIP]

### Codebase context [DONE]

- `youtube-transcript-pipeline/src/yt_pipeline.py:226-255` already isolates optional analysis in a `try`, but its `except` uploads fallback prose as `analysis_main.md`; removing that upload preserves transcript completion and existing diagnostics.
- `youtube-transcript-pipeline/test/test_yt_pipeline.py:212-279` covers success and LLM failure but pins three uploads in both cases; it needs filename/content assertions plus a real local-storage absence check.
- `yt-viewer/server.js:64-102` already maps absent analysis to `hasAnalysis: false` and `404 Not found`; `yt-viewer/server.test.js` needs a deterministic transcript-only fixture, requiring only an injectable KB root with the current root as default.
- `.claude/commands/{mindmap,kb-index,expand-analysis,flashcards}.md` are the executable command boundaries. Their missing-analysis behavior is implicit or incomplete, and no command-contract test exists.
- Root `Makefile` runs quiz, viewer, and pipeline tests; a command-contract test must be added there so the repository gate owns the new boundary.

### Relevant documentation [DONE]

- `.architecture-reviews/reports/2026-08-11T080000Z-ai-research.md` is authoritative: artifact presence is the sole completion signal; absence is sufficient and no manifest/state machine should be added.
- `CLAUDE.md:86-98` and `youtube-transcript-pipeline/README.md:130-140` describe `analysis_main.md` as universal output and should state that it exists only after successful analysis.
- No relevant PlantUML architecture documentation exists under `docs/`; `docs/proposals/proposal-20260518-yt-knowledge-quiz.md` is unrelated.

### Knowledge base [DONE]

- Recall used local fallback (`ai-research-learnings` QMD collection absent). Relevant rule: anchor integration plans in live code and tests, and verify dependency-free Node utilities with built-in Node tests.
- Preserve root `make test` as the authoritative repository-health gate; focused tests are evidence, not a substitute.
- Keep integration configuration import-safe and injectable at execution boundaries; apply this by defaulting viewer `ROOT` while allowing tests to override it.

## Available Skills

- `compound-plan`: build and persist this implementation plan.
- `recall-knowledge`: identify repository learnings that constrain the change.
- `tdd`: execute the characterization-first RED/GREEN implementation cycle.
- `validate-implementation`: check the completed change against repository rules and acceptance criteria.
- `save-learning`: record implementation-session findings before completion.

## Solution [TODO]

## Implementation [TODO]

## Files to Modify [TODO]

## TDD [TODO]

## Dependencies [TODO]
