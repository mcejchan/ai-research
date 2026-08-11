# Make analysis_main.md a truthful success-only artifact

## Objective

Reserve `analysis_main.md` for successfully completed LLM analysis. If optional analysis fails, preserve the successfully captured transcript, leave `analysis_main.md` absent, and keep diagnostics in existing logs/error output rather than writing a success-shaped placeholder or introducing another state manifest.

## Evidence

Use `.architecture-reviews/reports/2026-08-11T080000Z-ai-research.md` as the authoritative finding. It identifies:

- `youtube-transcript-pipeline/src/yt_pipeline.py:226-255` writing a placeholder to `analysis_main.md` after analysis exceptions;
- `test/test_yt_pipeline.py:253-279` pinning that behavior;
- `yt-viewer/server.js:77-81` treating filename existence as `hasAnalysis: true`;
- downstream knowledge commands consuming `analysis_main.md` as structured analysis;
- a real placeholder artifact in the local knowledge base.

The authoritative baseline before this task was green: root `make test` passed quiz 2/2, viewer 1/1, pipeline 41/41.

## Characterization-first guardrail

Before changing production behavior, add focused contract tests proving how every repository-owned consumer behaves when a transcript exists but `analysis_main.md` is missing. Cover at least the viewer listing/status and analysis endpoint, plus each knowledge command that discovers or consumes `analysis_main.md` (`mindmap`, `kb-index`, `expand-analysis`, and `flashcards`, using the actual current command boundaries). Do not weaken structured-content validation or silently treat a missing analysis as successful content.

## Implementation scope

- Change the pipeline failure path so analysis exceptions do not create or upload `analysis_main.md`.
- Preserve transcript success independently from optional analysis failure.
- Keep useful diagnostics in existing logging/error output; do not add `analysis_status.json`, a second manifest, sentinel document, lifecycle database, or retry state machine.
- Update the existing pipeline test that currently expects a placeholder, and add a regression assertion that no local or uploaded `analysis_main.md` is produced after failure.
- Ensure the viewer reports `hasAnalysis: false` and its analysis endpoint returns the existing missing-analysis response when the file is absent.
- Ensure repository-owned knowledge consumers skip, report, or otherwise handle missing analysis explicitly according to their current public contract; they must not crash or manufacture success.
- Do not modify or delete historical knowledge-base artifacts as part of this task. If cleanup/migration is desirable, mention it separately in the final note.
- Avoid unrelated storage-backend, retry, viewer, or command refactors.

## Scope boundary

Work only inside `/Users/michal/Projects/ai-research`. Do not inspect or modify other repositories, global OpenClaw configuration, or external credentials. The architecture review already contains the cross-component evidence needed for this repository-local change.

## Acceptance criteria

- Successful analysis still produces/uploads the same `analysis_main.md` content and location.
- Failed analysis preserves the transcript but produces/uploads no `analysis_main.md`.
- Failure diagnostics remain observable through existing logs/error output.
- Viewer truthfully reports analysis unavailable and serves no placeholder as analysis.
- All named repository-owned consumers have contract tests for a missing analysis and behave explicitly without processing fallback prose as structured content.
- No new product-state manifest or lifecycle authority is introduced.
- Existing successful workflows and public command contracts remain compatible.
- Final note records changed files, exact focused and broad verification results, intentional behavior changes, and any follow-up concerning historical placeholders.

## Verification

Run focused producer, viewer, and consumer contract tests first. Then run the repository's authoritative root gate:

```bash
make test
```

The final gate must pass at least the same component boundaries as the baseline (quiz, viewer, and pipeline). Do not claim success from focused tests alone.
