# Canonical offline verification evidence follow-up

## Progress
- [x] Resolve canonical plan path.
- [x] Inspect parent implementation, plan, proof, checkpoint, and acceptance record.
- [x] Specify evidence-only completion and verification.

## Analysis
- `youtube-transcript-pipeline/src/yt_pipeline.py:215-238` already delegates the workflow; `youtube-transcript-pipeline/src/path_slugs.py` owns the path/title rules. The committed refactor has historical RED/GREEN at `plans/checkpoints/task-4b4c2668-1c7b-4098-8cc3-c1d143a53ac0.red-green-proof.md`.
- `plans/checkpoints/task-ab931892-697e-4c5e-8c59-e74e624be651.checkpoint.md` records local focused (6, 4, 22) and broader (50, root `make test`) passing suites; the acceptance finding still records Test Gate `not-run`. The parent evidence extraction has truncated outcomes, so neither artifact supplies canonical gate provenance.
- Root `Makefile` aggregates quiz, viewer, command-contract, and pipeline suites. Follow `learnings/tooling/evidence-only-followups-rerun-the-exact-root-gate.md` and `learnings/tooling/followup-note-proof-does-not-substitute-for-test-gate.md`.

## Approach
- Use the caller/orchestrator's canonical Test Gate to run the existing focused tests and broader offline suites, including the registered root command. Do not label local shell output or the parent's proof as gate evidence.

## Implementation
1. Preserve the committed implementation and historical proof; use `skill:task-evidence` only if the gate needs exact historical command lineage.
2. Request caller-owned Test Gate runs from repository root for `python3 -m pytest youtube-transcript-pipeline/test/test_refactor_contracts.py -q -c youtube-transcript-pipeline/pytest.ini`, `python3 -m pytest test/test_path_slug_callers.py -q`, and `cd ~/Projects/ai-research && make test`; from `youtube-transcript-pipeline/` run `python3 -m pytest test/test_yt_pipeline.py test/test_config.py -q` and `python3 -m pytest -q`. Use separate canonical run IDs if the gate accepts only one command per run.
3. Collect gate reference(s), exact argv, cwd, status, exit code, and test counts for each command. If any command fails, investigate that concrete failure; only plan a minimal tested code correction if it proves an implementation defect.
4. Link the successful canonical gate reference(s) to this follow-up's checkpoint/final note and have the caller link this dedicated plan in task state through its supported mechanism; do not overwrite `plans/tasks/` or edit acceptance manifests manually. If no gate facility is exposed, report the blocker explicitly rather than claiming acceptance.
5. Read back gate and note; invoke `skill:save-learning` and save at least one learning as the final action of implementation.

## Testing
- Require fresh successful canonical Test Gate results for all five commands in Implementation step 2, with the registered `cd ~/Projects/ai-research && make test` as the project-wide gate. Check the gate record against recorded cwd, exit 0, and suite summaries; do not infer counts from prior runs.
- Read back checkpoint and state links; run `git diff --check` and verify no production/test files changed when gates pass.

## TDD: skip
- This is an evidence-only operation on an already implemented refactor; preserve the historical genuine RED and capture fresh canonical GREEN without inventing another RED.

## Files
- Follow-up checkpoint under `plans/checkpoints/`: gate IDs, command/results, and historical proof link.
- Caller-owned Test Gate record and follow-up task state: canonical result and plan/checkpoint links, managed by the caller.
- `learnings/`: at least one learning via `skill:save-learning` at implementation completion.
