# Plan 2026-09-10: Fix ignored AI Research pytest configuration

Correct the pytest section in `youtube-transcript-pipeline/pytest.ini` so the declared `testpaths`, `addopts`, and `env` are actually loaded, and prove the fix with a characterization test.

*Status: DRAFT*
*Created: 2026-09-10*

## Problem

`youtube-transcript-pipeline/pytest.ini:1` declares the section as `[tool:pytest]`. That is the `setup.cfg` form; pytest reads `[pytest]` from a `pytest.ini` file. With the wrong section, pytest ignores the whole file: `testpaths`, `addopts` (`--cov=src`, `--cov-report=...`, `-v`) and the `env` block are never applied. The suite still runs because pytest falls back to default discovery and the root `Makefile` supplies the env values explicitly — so the defect is silent, not a no-op.

## Analysis

### Codebase context
- `youtube-transcript-pipeline/pytest.ini` — the only place declaring `testpaths=test`, coverage `addopts`, and the 6 `env` vars. Section `[tool:pytest]` (wrong for a `.ini` file).
- Root `Makefile:6` — `make test` runs `cd youtube-transcript-pipeline && OPENAI_API_KEY=test_openai_key LANG=cs USE_WHISPER_FALLBACK=false MAKE_EMBEDDINGS=false DRIVE_FOLDER_ID=test_folder_id python3 -m pytest`. These 5 env values exactly match the `pytest.ini` `env` block (plus `PYTHONPATH=src`, which the `cd`/`-m` invocation already provides). So enabling the section changes **no runtime behavior** for `make test`.
- `youtube-transcript-pipeline/Makefile:14` — `make test` in the pipeline just runs bare `pytest` (no env, no testpaths). This is where the config fix has a real effect: bare `pytest` gains `testpaths=test` + coverage + env.
- `test/test_config.py` — existing config tests (subprocess import checks). Appended test lives here.
- 42 tests currently collected (`grep "def test_" test/*.py` = 42; `pytest --collect-only` = 42). The declared `python_files`/`python_classes`/`python_functions` globs equal pytest defaults, so enabling `testpaths=test` keeps collection at 42.

### Relevant documentation
- `CLAUDE.md` — "Run tests (ALWAYS before commits): pytest" and notes the pipeline runs from `youtube-transcript-pipeline/`.
- `youtube-transcript-pipeline/README.md` — documents test/requirements setup.

### Knowledge base
- Host baseline 2026-09-10: `42 passed, 12 subtests passed, 25.88s`. Audit baseline only, not a freeze target.
- Verified locally: `pytest-cov 7.0.0`, `pytest-env` import OK; `pytest 8.4.2`.

### Available Skills
- `tdd` — drive the RED→GREEN cycle for the characterization test and record evidence to `plans/checkpoints/task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df.red-green-proof.md`.
- `save-learning` — **mandatory final action** after implementation (record the section-mismatch gotcha).
- `recall-knowledge` — load any pytest/coverage learnings before implementing.

## Solution

1. Change only the section header in `pytest.ini`: `[tool:pytest]` → `[pytest]`. No other line changes; the already-declared `testpaths`, `addopts`, `env`, and `python_*` globs then take effect.
2. Add a characterization test to `test/test_config.py` proving the section is read (it fails on the current file, passes after the fix).
3. No dependency change: `requirements-dev.txt` already lists `pytest`, `pytest-mock`, `pytest-cov`, `coverage`, `pytest-env`. Only **verify** they are declared and installed (they are).

## Implementation

### Pre-implementation checklist
- [ ] `git status` clean and no concurrent fix for `pytest.ini` (verified: only initial commit, no uncommitted changes).
- [ ] Confirm `requirements-dev.txt` declares `pytest-cov`, `pytest-env`, `pytest-mock`, `coverage`, `pytest` (already does).
- [ ] Confirm root `Makefile` env values still match after the fix (they will — unchanged).

### Steps
1. `pytest.ini`: line 1 `[tool:pytest]` → `[pytest]`.
2. Append two tests to `test/test_config.py` (skeleton in TDD below) — write first, run → RED.
3. Apply the section fix, re-run the two tests → GREEN.
4. Run the full pipeline suite: `cd youtube-transcript-pipeline && python3 -m pytest -q` → expect 42 passed, coverage emitted.
5. Run the root gate: `cd ~/Projects/ai-research && make test` → Node gate + Python suite, no regressions.

## Files to Modify

| File | Change |
|------|--------|
| `youtube-transcript-pipeline/pytest.ini` | Line 1: `[tool:pytest]` → `[pytest]` (only change) |
| `youtube-transcript-pipeline/test/test_config.py` | Append 2 characterization tests (RED→GREEN) |

No change to `requirements-dev.txt`, `Makefile`, `CLAUDE.md`, or any `src/` pipeline code.

## TDD

**Workflow for the implementing agent:**
1. Append the test skeleton below to `youtube-transcript-pipeline/test/test_config.py`.
2. Run the run command → confirm the new tests FAIL (RED).
3. Apply the `pytest.ini` section fix.
4. Re-run → confirm the new tests PASS (GREEN).
5. Run full suite → no regressions.

> TDD cycle per `skill:tdd` — RED/GREEN evidence recorded to `plans/checkpoints/task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df.red-green-proof.md`.

### Targeted Tests

**Test file:** `youtube-transcript-pipeline/test/test_config.py` (append)
**Framework:** pytest (project's existing runner)
**Run command:** `cd youtube-transcript-pipeline && python3 -m pytest test/test_config.py -v`
**Edit hint:** Append at end of `test/test_config.py`

```python
import pytest
from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parents[1]


def test_pytest_ini_section_is_read_by_pytest():
    # RED: with [tool:pytest], pytest ignores the file; addopts/testpaths come back empty.
    cfg = pytest.Config.from_path(PIPELINE_ROOT / "pytest.ini")
    addopts = cfg.getini("addopts")
    assert "--cov=src" in addopts  # RED before fix (addopts == []); GREEN after [pytest]
    assert cfg.getini("testpaths") == ["test"]  # RED before fix (testpaths == [])


def test_pytest_ini_env_block_present():
    # RED: env block only honored under the [pytest] section.
    cfg = pytest.Config.from_path(PIPELINE_ROOT / "pytest.ini")
    env = cfg.getini("env")
    assert "USE_WHISPER_FALLBACK = false" in env  # RED before fix; GREEN after [pytest]
```

| Test (maps to skeleton) | RED (before fix) | GREEN (after fix) |
|------|------|-------|
| `test_pytest_ini_section_is_read_by_pytest` | `assert "--cov=src" in addopts` fails — `addopts == []` because `[tool:pytest]` is ignored | `addopts` contains `--cov=src`, `testpaths == ["test"]` |
| `test_pytest_ini_env_block_present` | `assert "USE_WHISPER_FALLBACK = false" in env` fails — `env == []` | `env` contains all 6 declared entries |

### Regression
- [ ] Before fix: full suite `python3 -m pytest -q` (baseline, no coverage output).
- [ ] After fix: full suite → **42 passed** (collection unchanged; globs equal defaults) + `term-missing`/`html` coverage emitted.
- [ ] Root gate: `make test` (Node + Python) passes, env values still match.

## Verification (evidence to record)
- `pytest -c pytest.ini --collect-only -q` → 42 tests, `testpaths=test` honored.
- `python3 -c "import pytest; c=pytest.Config.from_path('pytest.ini'); print(c.getini('addopts')); print(c.getini('testpaths')); print(c.getini('env'))"` → non-empty on all three after fix.
- `python3 -m pytest -q` → 42 passed + coverage table.
- `make test` from repo root → mixed Node/Python gate passes.
- `git status --porcelain` after run → only `pytest.ini` + `test_config.py` tracked; `htmlcov/`, `.coverage`, `.pytest_cache/` stay untracked (root `.gitignore` already covers them recursively), so no new tracked artifacts.

## Remaining host-only checks
- `make test` end-to-run timing against the `25.88s` host baseline (note any drift; not a freeze target).
- Confirm `make test` Python step still exits 0 with the now-active `addopts`.

## Scope guardrails
- Only the registered `ai-research` repo; only the two files above.
- No changes to pipeline behavior, provider credentials, env values, report publishing, or unrelated tests.
- Offline / synthetic only — no live API, provider, or download calls.

## Dependencies
- Local interpreter has `pytest 8.4.2`, `pytest-cov 7.0.0`, `pytest-env` (verified importable). `pytest.Config.from_path` requires these plugins for `--cov`/`env` to be recognized — they are present.

---
*Created: 2026-09-10*
*Status: DRAFT*
