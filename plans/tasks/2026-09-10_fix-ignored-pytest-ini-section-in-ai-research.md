---
title: Fix ignored AI Research pytest configuration
type: implementation
---

## Goal and current state
Finish verification of the EXISTING repair, not a second implementation. `youtube-transcript-pipeline/pytest.ini` already uses `[pytest]`; `test/test_config.py` already has two regression tests using `pytest.Config.fromdictargs`. Preserve both. The remaining obligation is trustworthy current verification and task-bound evidence. This brief replaces the previous rejected recovery instructions.

## Scope
Repository `/Users/michal/Projects/ai-research` only. Read the two files above, pipeline requirements/requirements-dev and root Makefile. No new permanent regression test is required; no application changes, refactor, new dependencies, setup documentation project, or unrelated repair. A short verification plan is sufficient. Do not follow the previous plan's dependency-driven RED/GREEN approach.

## Minimal verification and evidence
1. Use one repository-local ignored virtualenv with BOTH declared requirements files installed before measuring any test result. Use its absolute Python path, and prepend its absolute bin directory to PATH for root `make test`. Record interpreter/plugin versions once. Missing dependencies are setup blockers, NEVER the RED for this repair.
2. Run existing `test/test_config.py` from the pipeline directory, then root `make test`. Record actual commands, working directories and exits. Do not assume historical test counts. Successful current verification does not establish historical TDD chronology.
3. The task still requires structured RED/GREEN evidence. The authorized minimal approach is a CURRENT isolated reproduction of the original defect, using the existing tests, not an invented new regression: create a disposable copy of the pipeline inside an ignored repository-local directory (exclude environments, caches and generated artifacts). In that copy only, change `[pytest]` to `[tool:pytest]`. With the fully prepared environment, run the two existing pytest-config regression tests and verify assertion failures caused by ignored config. Change only the copied header back to `[pytest]`, rerun the identical command in the identical environment, and require success. Do not change plugins, assertions or dependencies between phases. Never revert the working repository configuration.
4. Use the installed `tdd` skill's proof-capture helper for real timestamps, commands and exits. Keep proof task-bound at the repository's canonical checkpoint location; label it explicitly as a fresh isolated reproduction of an already implemented repair, NOT the original development sequence. Preserve the rejected historical proof unchanged in a clearly named previous-attempt artifact if the helper requires a free canonical path; do not overwrite an existing archive. No hand-filled historical timestamps. This reproduction already supplies the relevant nonzero-exit check; do not add a separate controlled failing test.

## Acceptance and stop conditions
- Working repair and existing tests preserved; current focused check and mixed Node/Python `make test` pass in the same declared environment.
- Fresh evidence distinguishes the bad versus good HEADER, with unchanged tests/environment, and records the copied scope transparently. Never claim it proves pre-implementation history.
- Do not weaken/disable TDD or acceptance, invent a waiver, or treat proof formatting alone as semantic acceptance. If the existing evidence contract cannot accept this explicitly labelled reproduction, report that exact limitation and current verification results; do not manufacture another cycle or add tests to evade it.
- Final note: changed paths (including none for production), commands/results, proof location and any blocker. Reuse required pipeline artifacts rather than inventing extra reports. Do not operate task/batch lifecycle yourself.
