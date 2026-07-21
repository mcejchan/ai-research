# Establish one project-level test gate

## Context
The registered test command currently runs only `youtube-transcript-pipeline && pytest`, although maintained executable tests also exist in `quiz/build-index.test.js` and `yt-viewer/server.test.js`. GitHub Pages deployment builds and uploads the quiz without running its tests.

Current verified baseline:
- `yt-viewer/server.test.js` passes.
- `quiz/build-index.test.js` fails because production preserves `data.difficulty || 'hard'` (including `extra-easy`) while the test expects unknown `weird` to normalize to `hard`.
- Plain `pytest` is absent from PATH in the review environment.
- `python3 -m pytest` reaches collection but fails because `DRIVE_FOLDER_ID` is read unconditionally during module import.

The repository needs one authoritative health entrypoint that delegates to the existing subsystem suites. This task must resolve the exposed test-contract/configuration defects rather than papering over them.

## Required change
- Add one small root-level test entrypoint (prefer an existing project convention such as a Make target or script; do not introduce a framework) that runs:
  1. quiz tests,
  2. yt-viewer tests,
  3. YouTube transcript pipeline pytest.
- Make the Python suite collect and run under explicit test-safe configuration without requiring operator production secrets at import time.
- Resolve the quiz difficulty contract explicitly: preserve supported `extra-easy`, `easy`, and `hard`; unknown values must follow one documented/default behavior, and implementation plus tests must agree.
- Update `skills/opencode-dev/projects.yaml` registry `testCommand` for `ai-research` to call the single root gate.
- Update `.github/workflows/deploy-quiz.yml` to run at least the quiz slice before upload; prefer the root gate only if the workflow environment can satisfy all subsystem dependencies without unrelated credentials.

## Constraints
- Keep the three subsystem test suites separate beneath the root orchestration.
- Do not merge quiz and yt-viewer architectures.
- Do not weaken assertions, skip suites, swallow failures, or rely on locally installed global `pytest`.
- Do not embed real Drive IDs or production secrets in tests or workflows.
- Do not address obsolete quiz API deletion or `tmp/` cleanup here.

## Acceptance criteria
- A single documented root command represents repository health and returns non-zero when any delegated suite fails.
- The registry invokes that command rather than only pipeline pytest.
- Quiz deployment cannot proceed when its maintained test fails.
- Quiz tests cover `extra-easy` and unknown difficulty consistently with the chosen contract.
- Python tests collect without a production `DRIVE_FOLDER_ID` dependency at module import.
- All delegated suites pass in their supported local/test environment.
- No duplicate test orchestration path is introduced beyond the root delegator and deployment's justified quiz preflight.

## TDD stance
First encode/fix the two observed failing contracts: quiz difficulty handling and Python import-time configuration. Then add the root orchestration and workflow/registry wiring. Keep failure propagation observable.

## Verify
- Run the new root-level test command from repository root.
- Run each delegated suite independently to show the root gate is a faithful composition.
- Validate the workflow syntax and inspect the registry command.
- Run `git diff --check`.

## Previous Plan (rejected - attempt 1)
Plan file: /Users/michal/Projects/ai-research/plans/2026-07-21_bold-dune-3929_establish-one-project-level-test-gate.md
Review feedback: The plan is only a WIP skeleton with TODO sections, so it silently omits how the root health command, suite composition, contract fixes, files, TDD, and verification will be handled.
Read the previous plan, understand what was wrong, and produce a corrected plan.
