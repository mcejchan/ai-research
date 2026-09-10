---
title: Fix ignored AI Research pytest configuration
type: implementation
---

## Goal
Complete and verify the existing pytest configuration repair. Preserve working changes; deliver reproducible current verification and valid chronological TDD evidence, not another account of the previous run.

## Exact files/functions
Within this repository only: `youtube-transcript-pipeline/pytest.ini`, `youtube-transcript-pipeline/test/test_config.py` (`_load_pipeline_pytest_config` and its two regression tests). Read `requirements-dev.txt`, `requirements.txt`, pipeline README testing setup, and root Makefile as needed. Only extend setup documentation if needed; no dependency or application redesign.

## Verified cause/intended change
The previous attempt ALREADY changed `[tool:pytest]` to `[pytest]` and added two tests using `pytest.Config.fromdictargs` (valid API; `from_path` does not exist). Keep them. Historical RED/GREEN exists but its handwritten proof was rejected for missing structured timestamps/commands/exits. Do not backfill those fields or present old evidence as this run.
Implement the TDD cycle using skill:tdd and its discovered proof-capture helper. Preserve the old proof as a clearly labelled previous-attempt artifact before creating fresh task-bound proof. Add a small regression using a temporary copied INI: real pytest loading must distinguish its invalid `[tool:pytest]` section from valid `[pytest]`, including testpaths/addopts/env. Obtain genuine chronological RED then GREEN while developing that regression; a broken API/import is not valid RED. Never revert the working repository configuration merely to manufacture a failure. If no legitimate missing regression remains, report that evidence limitation instead of inventing a cycle.

## Boundaries/non-goals
Bounded single-owner config/test repair; no architecture search, external repositories, credentials, live providers, downloads of video, deployment or application behavior changes. Preserve unrelated files. Existing expected42/44 counts are historical baselines, not fixed assertions. Do not relax acceptance, skip required plugins, or replace the mixed Node/Python gate.

## Verification
Host check now: `/opt/homebrew/bin/python3` is Python3.14 with pytest/pytest-cov but without pytest-env; requirements-dev already declares it. Prepare a repository-local ignored virtualenv from that interpreter using the documented requirements and requirements-dev (ordinary dependency installation only); no global installs. Put its bin directory first in PATH for BOTH focused checks and root `make test`, whose Python command is literal python3. Record interpreter/plugin versions. From pipeline directory run `python3 -m pytest test/test_config.py`; from root run `make test`. Record loaded testpaths/addopts/env, collection changes and actual exit codes; verify a controlled failing temporary test preserves nonzero exit. Keep temporary coverage outputs ignored/disposable. Final checkpoint: changed paths, fresh proof path, exact commands/results, and any unresolved blocker. Current tests and proof—not historical success—determine completion.
