# Plan: Complete goal-006 verification evidence and final note

## Progress

- [x] Resolve canonical plan path.
- [x] Inspect original plan, preserved code, and verification artifacts.
- [x] Identify caller-owned canonical Test Gate requirement and final-note content.
- [x] Specify evidence-only acceptance repair.

## Analysis

- `plans/checkpoints/task-4b4c2668-1c7b-4098-8cc3-c1d143a53ac0.red-green-proof.md` contains genuine RED and GREEN for the six-test refactor suite; parent checkpoint reports other passes without canonical Test Gate provenance.
- `Makefile` aggregates quiz, viewer, command-contract, and pipeline suites under `make test`; the registered command is `cd ~/Projects/ai-research && make test`. The previous plan lacked this top-level plan heading, causing `invalid_header`.
- `youtube-transcript-pipeline/src/yt_pipeline.py:215-238` spans 24 lines. `youtube-transcript-pipeline/src/path_slugs.py` owns both slug functions; `helper-scripts/_slug_owner.py` loads it relative to its file.
- Use `skill:task-evidence` to extract historical command provenance and `skill:save-learning` after the acceptance repair; use the caller-owned Test Gate for canonical proof. Follow `learnings/tooling/evidence-only-followups-rerun-the-exact-root-gate.md` and `learnings/architecture/slug-boundary-and-title-semantics.md`.

## Approach

- Preserve parent implementation and RED proof; verify current code through a fresh caller-owned canonical Test Gate rather than treating checkpoint prose or local shell output as canonical evidence.
- Supply a follow-up final note with exact commands and actual outcomes, slug ownership/callers, and distinct title semantics; link the new plan and gate reference in follow-up state.

## Implementation

1. Inspect committed parent diff and task artifacts; use `skill:task-evidence` for historical command/results; do not synthesize a new RED or attribute fresh results to the parent run.
2. Request the caller/orchestrator's canonical Test Gate to run the focused pipeline command, focused root slug command, broader pipeline command, and registered root `make test` command below from their specified working directories. Record returned gate run ID, status, exact argv, cwd, exit codes, and suite counts; if the facility cannot record multiple commands, request separate canonical runs/references. Do not substitute local shell output for this record.
3. If any gate fails, diagnose that concrete failure and make only the minimum necessary tested correction before rerunning the affected gate; otherwise leave production and tests untouched.
4. Write the follow-up final note in `plans/checkpoints/task-ab931892-697e-4c5e-8c59-e74e624be651.checkpoint.md` and include it in the final task response: actual command/result pairs and gate references; AST start/end and 24-line `run_for_url` count; owner `youtube-transcript-pipeline/src/path_slugs.py`; rewired callers `youtube-transcript-pipeline/src/yt_pipeline.py`, `helper-scripts/normalize_kb_paths.py`, and `helper-scripts/rename_video_folders.py` (last two through `helper-scripts/_slug_owner.py`). Explicitly state path slugs split `/` and `_` and use caller fallback; title slugs drop `/`, retain `_`, return empty for punctuation-only input, and cap at 80 characters.
5. Link canonical gate result and plan from the follow-up state/checkpoint, read back both artifacts, then run `skill:save-learning` and save at least one relevant learning file as the last task action.

## Testing

- From repository root: `python3 -m pytest youtube-transcript-pipeline/test/test_refactor_contracts.py -q -c youtube-transcript-pipeline/pytest.ini` (historical GREEN: 6 passed); `python3 -m pytest test/test_path_slug_callers.py -q` (historical summary: 4 passed).
- From `youtube-transcript-pipeline/`: `python3 -m pytest test/test_yt_pipeline.py test/test_config.py -q` (historical summary: 22 passed); `python3 -m pytest -q` (historical summary: 50 passed).
- From repository root, canonical registered gate: `cd ~/Projects/ai-research && make test`; require fresh caller-owned gate evidence for successful completion, not the parent checkpoint's claimed pass. Report fresh observed counts/status, not assumed historical numbers.
- Recount by AST or source span after verification; check `git diff --check` and confirm scope before reporting.

## TDD

- Skip a new RED/GREEN cycle: this is evidence-only verification of existing implementation, not a behavior change. Link the genuine parent RED/GREEN proof and capture fresh GREEN in the canonical Test Gate; never fabricate RED after implementation.

## Files

- `plans/checkpoints/task-ab931892-697e-4c5e-8c59-e74e624be651.checkpoint.md`: final note and canonical gate reference/results.
- Follow-up task state: link this dedicated plan and new checkpoint without overwriting the task file or parent evidence.
- Caller-owned Test Gate record: authoritative fresh execution evidence, created through the orchestrator facility.
- `learnings/`: save one applicable learning via `skill:save-learning` after completing the repair.
