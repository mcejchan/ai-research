# Plan 2026-08-11: Make analysis_main.md a truthful success-only artifact

Reserve `analysis_main.md` presence as the existing completion signal while preserving transcript ingestion and explicit failure diagnostics.

## Analysis

### Codebase

- `youtube-transcript-pipeline/src/yt_pipeline.py:226-255` already isolates optional analysis in a `try`; its `except` must log and continue without a second upload.
- `youtube-transcript-pipeline/test/test_yt_pipeline.py:212-279` pins three uploads on failure and lacks filename, content, and local-filesystem assertions.
- `yt-viewer/server.js:64-102` already derives `hasAnalysis` from file presence and maps missing files to `404 Not found`; tests need an isolated KB root rather than mutable repository content.
- `.claude/commands/{mindmap,kb-index,expand-analysis,flashcards}.md` are the actual knowledge-command implementations. Missing-analysis handling is implicit, incomplete, or can emit a broken link.
- Root `Makefile` owns quiz, viewer, and pipeline health but does not run command-contract tests.

### Documentation And Learnings

- `.architecture-reviews/reports/2026-08-11T080000Z-ai-research.md` is authoritative: use absence as the unavailable state; add no manifest, sentinel, database, or retry workflow.
- `CLAUDE.md:86-98` and `youtube-transcript-pipeline/README.md:130-140` should describe analysis output as success-only.
- No relevant PlantUML documentation exists. The only `docs/` proposal concerns the quiz and is out of scope.
- Knowledge recall used the deterministic local fallback because collection `ai-research-learnings` was unavailable. Applicable rules are to anchor integration work in live code/tests, keep dependency-free Node verification, and retain root `make test` as final authority.

## Available Skills

- `tdd`: execute and record characterization-first RED/GREEN evidence.
- `validate-implementation`: verify scope, contracts, and repository rules after GREEN.
- `save-learning`: mandatory final implementation-session action.

## Approach

- Characterize transcript-only folders before production edits: viewer listing and analysis response, producer upload/local storage behavior, and all four command specifications.
- Keep successful analysis unchanged: upload the returned LLM body to the same filename and folder.
- On analysis or analysis-upload exceptions, retain the existing warning output and continue cleanup/optional embeddings without creating fallback content.
- Make command behavior explicit at its current Markdown boundary:
  - `mindmap`: discover only existing `analysis_main.md` sources, report skipped transcript-only folders, and stop without output if no eligible analysis exists.
  - `kb-index`: retain every video and folder-name title fallback, but render analysis as unavailable rather than linking to a missing file.
  - `expand-analysis`: require both transcript and an existing analysis draft; report and stop before confirmation/read/write when analysis is absent.
  - `flashcards`: direct mode reports and stops on missing analysis; search mode skips and reports such folders, and stops without output when no eligible analysis remains.
- Do not edit historical `local-knowledge-base/**` artifacts or refactor storage, retries, viewer UI, or command architecture.

## Implementation

1. Invoke `skill:tdd` and create `plans/checkpoints/bold-vale-3575.red-green-proof.md`.
2. Add the command-contract test, add deterministic transcript-only viewer tests, and reverse/add pipeline failure assertions. Run focused tests before source edits; record which characterization tests already pass and which new contract assertions are RED.
3. Add an environment override for the viewer KB root while preserving its current default. Do not alter route response contracts.
4. Add explicit missing-analysis branches to the four command Markdown files and register their Node contract test in root `Makefile`.
5. Remove placeholder construction/upload from the pipeline exception handler; retain the warning and continuation. Strengthen the successful-analysis assertion for unchanged filename/body.
6. Update output documentation to mark `analysis_main.md` optional and success-only.
7. Run focused GREEN tests, then `make test`; confirm quiz, viewer, and pipeline boundaries all pass and the new command contracts are part of the root gate.
8. Invoke `skill:validate-implementation`, inspect the diff for forbidden state artifacts or historical KB changes, and prepare the final note with exact commands/results and historical-placeholder follow-up.
9. Invoke `skill:save-learning` last and save at least one learning file.

## Files To Modify

| File | Change |
|---|---|
| `youtube-transcript-pipeline/src/yt_pipeline.py` | Stop producing placeholder analysis after exceptions. |
| `youtube-transcript-pipeline/test/test_yt_pipeline.py` | Prove success content, transcript preservation, no analysis upload, no local analysis file, and visible diagnostics. |
| `yt-viewer/server.js` | Allow a test-only KB-root override with the current default unchanged. |
| `yt-viewer/server.test.js` | Characterize transcript-only listing status and existing missing-analysis 404 response. |
| `.claude/commands/mindmap.md` | Explicitly skip/report transcript-only sources. |
| `.claude/commands/kb-index.md` | Include transcript-only videos without broken analysis links. |
| `.claude/commands/expand-analysis.md` | Explicitly stop when the analysis draft is absent. |
| `.claude/commands/flashcards.md` | Explicitly handle missing analysis in direct and search modes. |
| `test/knowledge-command-contracts.test.js` | Add dependency-free tests over the actual command specification boundaries. |
| `Makefile` | Add command contracts to the authoritative root gate. |
| `youtube-transcript-pipeline/README.md` | Document success-only analysis output. |
| `CLAUDE.md` | Document success-only analysis output for repository agents. |

## TDD

**Workflow:** Implement the TDD cycle with `skill:tdd`; record RED/GREEN evidence in `plans/checkpoints/bold-vale-3575.red-green-proof.md`.

### Initial Contract Skeleton

**Test file:** `test/knowledge-command-contracts.test.js` (new)

**Framework:** Node built-in `node:test`

**Run:** `node --test test/knowledge-command-contracts.test.js`

```js
import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const commands = {
  mindmap: ".claude/commands/mindmap.md",
  "kb-index": ".claude/commands/kb-index.md",
  "expand-analysis": ".claude/commands/expand-analysis.md",
  flashcards: ".claude/commands/flashcards.md",
};

for (const [name, file] of Object.entries(commands)) {
  test(`${name} defines missing-analysis behavior`, async () => {
    const source = await readFile(file, "utf8");
    assert.match(source, /<missing_analysis>/); // RED: no command defines this contract yet
    assert.match(source, /analysis_main\.md/);
    assert.match(source, /report/i);
  });
}
```

Use command-specific assertions in the committed test: skip-and-report for `mindmap`; include-without-link for `kb-index`; stop-before-read/write for `expand-analysis`; direct-stop and search-skip/report for `flashcards`. The shared tag is specification structure, not product state.

### Focused Tests

| Boundary | RED before implementation | GREEN after implementation |
|---|---|---|
| Pipeline mock upload | Failure path still uploads `analysis_main.md` | Upload names are only raw and clean; warning remains observable. |
| Pipeline local storage | Failure leaves local placeholder | Transcript exists and `analysis_main.md` does not. |
| Viewer listing | Characterization should already pass | Transcript-only item has `hasTranscript: true`, `hasAnalysis: false`. |
| Viewer analysis endpoint | Characterization should already pass | Response remains `404` with `Not found`. |
| Four command specs | Explicit contract assertions fail | Each command handles absence according to its public contract. |

Run producer tests:

```bash
cd youtube-transcript-pipeline && OPENAI_API_KEY=test_openai_key LANG=cs USE_WHISPER_FALLBACK=false MAKE_EMBEDDINGS=false DRIVE_FOLDER_ID=test_folder_id python3 -m pytest test/test_yt_pipeline.py::TestYTPipeline::test_run_for_url_success test/test_yt_pipeline.py::TestYTPipeline::test_run_for_url_llm_failure test/test_yt_pipeline.py::TestYTPipeline::test_run_for_url_llm_failure_local_storage
```

Run viewer and consumer tests:

```bash
node --test yt-viewer/server.test.js test/knowledge-command-contracts.test.js
```

Run the authoritative gate:

```bash
make test
```

## Dependencies

- Use only existing Python and Node test infrastructure; add no package dependency.
- Preserve current API status/body, output locations, and successful command workflows.
- Leave the known historical placeholder untouched; mention separate cleanup/migration only in the final note.

*Status: DRAFT*
*Created: 2026-08-11*
