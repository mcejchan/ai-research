# Plan 2026-09-11: Fix ignored pytest.ini section (verification only, corrected)

Verification of the **already-applied** repair. **No production change.** The repair
(`youtube-transcript-pipeline/pytest.ini:1` `[tool:pytest]` → `[pytest]`) and the two regression
tests (`test/test_config.py:51` `test_pytest_ini_section_is_read_by_pytest`, `:58`
`test_pytest_ini_env_block_present`) already exist and are preserved untouched.

This is a replan of attempt 1, which was overengineered (venv recreation, proof-file relocation,
disposable copy, synthetic RED/GREEN). Corrected approach: **direct verification first**; the
isolated reproduction is a secondary, explicitly-labelled supplement required by the brief.

## Problem
`pytest.ini` must use `[pytest]` (not `[tool:pytest]`) for pytest to read `addopts`/`testpaths`/`env`.
The fix is in place; only trustworthy current verification + task-bound evidence remain.

## Analysis
- `pytest.ini:1` = `[pytest]`; lines 2-13 `testpaths=test`, `addopts = --cov=src ...`, `env `= 6 vars. Intact.
- `test/test_config.py:44-61`: `_load_pipeline_pytest_config()` uses `pytest.Config.fromdictargs({}, ["-c", str(PIPELINE_ROOT / "pytest.ini")])` (correct public API; `from_path` does not exist in pytest 8.x); assert `--cov=src in addopts`, `testpaths == ["test"]`, `USE_WHISPER_FALLBACK = false in env`.
- `Makefile:3-6` `test` runs node tests then `cd youtube-transcript-pipeline && ... python3 -m pytest` with the 5 env vars supplied **inline** → enabling the previously-ignored `env` block changes nothing for `make test` (no regression).
- `test/test_config.py:29-38` imports `run_for_url` from `src.yt_pipeline`; `requirements.txt` needs to be installed (incl. `faster-whisper` import is lazy at `src/yt_pipeline.py:149`, but pandas/dotenv/tqdm are top-level).
- Checkpoints: `plans/checkpoints/task-b521afdb-...red-green-proof.md` already occupied by a handed-crafted **rejected** proof (7159 bytes) — preserve, do not overwrite.
- All disposable artifacts (`.venv/`, `tmp/`, `__pycache__/`, `.pytest_cache/`, `htmlcov/`, `.coverage`) are git-ignored.

## Implementation (direct verification first)

### Step 0 — Pre-check (read-only)
Confirm `pytest.ini:1 == [pytest]` and the 2 regression tests exist. No edits to working repo.

### Step 1 — One ignored venv, both requirements
```
python3 -m venv /Users/michal/Projects/ai-research/.venv
/Users/michal/Projects/ai-research/.venv/bin/pip install \
  -r youtube-transcript-pipeline/requirements.txt \
  -r youtube-transcript-pipeline/requirements-dev.txt
```
Record interpreter + plugin versions once (missing deps are setup blockers, **not** the RED):
```
/Users/michal/Projects/ai-research/.venv/bin/python -c "import sys,pytest,pytest_cov,pytest_env,pytest_mock;print(sys.executable,pytest.__version__,pytest_cov.__version__,pytest_env.__version__)"
```

### Step 2 — Direct verification (primary action)
Focused config tests from the pipeline dir (venv python, absolute path):
```
cd youtube-transcript-pipeline && /Users/michal/Projects/ai-research/.venv/bin/python -m pytest test/test_config.py -v
```
Mixed Node/Python gate (prepend venv bin so `python3` resolves to venv):
```
cd /Users/michal/Projects/ai-research && PATH="/Users/michal/Projects/ai-research/.venv/bin:$PATH" make test
```
Record exact command, cwd, and exit for each. Do not assume historical counts.

### Step 3 — Isolated RED/GREEN reproduction (secondary, explicitly labelled)
Required structured evidence: a **fresh, current** reproduction of the defect using the **existing**
tests — NOT original development history, NOT a new invented test.

Preserve the rejected proof so the canonical path is free for the helper:
```
mv plans/checkpoints/task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df.red-green-proof.md \
   plans/checkpoints/task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df.red-green-proof.rejected-v1.md
```
Disposable copy (exclude envs/caches/generata):
```
rsync -a --exclude='.venv' --exclude='__pycache__' --exclude='.pytest_cache' \
  --exclude='htmlcov' --exclude='.coverage' \
  youtube-transcript-pipeline/ tmp/isolated-pytest-repro/youtube-transcript-pipeline/
```
In the **copy only**: toggle `pytest.ini:1` `[pytest]` → `[tool:pytest]`, then run the two existing
pytest-config regression tests via the tdd proof-capture helper (RED = genuine non-zero exit).
```
cd /Users/michal/Projects/ai-research && TASK_ID=task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df \
  python3 /Users/michal/.config/opencode/skills/tdd/scripts/proof-capture.py red -- \
  bash -c "cd /Users/michal/Projects/ai-research/tmp/isolated-pytest-repro/youtube-transcript-pipeline && /Users/michal/Projects/ai-research/.venv/bin/python -m pytest test/test_config.py::test_pytest_ini_section_is_read_by_pytest test/test_config.py::test_pytest_ini_env_block_present -v"
```
Then revert the **copied** header back to `[pytest]` and rerun the **identical command** in the
**identical venv** (GREEN = exit 0). Plugins, assertions, and dependencies unchanged between phases.
```
cd /Users/michal/Projects/ai-research && TASK_ID=task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df \
  python3 /Users/michal/.config/opencode/skills/tdd/scripts/proof-capture.py green -- \
  bash -c "cd /Users/michal/Projects/ai-research/tmp/isolated-pytest-repro/youtube-transcript-pipeline && /Users/michal/Projects/ai-research/.venv/bin/python -m pytest test/test_config.py::test_pytest_ini_section_is_read_by_pytest test/test_config.py::test_pytest_ini_env_block_present -v"
```
Helper supplies real timestamps/commands/exits; no separate controlled failing test. The working repo's
config is never reverted.

## TDD
**Workflow:**
1. Do NOT edit working `pytest.ini` or `test_config.py` — repair + tests already exist.
2. Setup venv (Step 1); missing deps are setup blockers, not RED.
3. Direct verification (Step 2) — primary.
4. Isolated reproduction (Step 3) via `proof-capture.py` — secondary, labelled.

**Target file (existing, unchanged):** `youtube-transcript-pipeline/test/test_config.py`
**Tests:** `test_pytest_ini_section_is_read_by_pytest`, `test_pytest_ini_env_block_present`
**Framework:** pytest, run inside the disposable copy at `tmp/isolated-pytest-repro/`.
**Proof location (helper-managed, canonical):** `plans/checkpoints/task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df.red-green-proof.md` — label explicitly as a **fresh isolated reproduction of an already-implemented repair, NOT the original development sequence**.
**Rejected proof preserved at:** `...red-green-proof.rejected-v1.md`.

| Test (both phases) | RED (copied header `[tool:pytest]`) | GREEN (copied header `[pytest]`) |
|---|---|---|
| `test_pytest_ini_section_is_read_by_pytest` | FAILS: `assert '--cov=src' in []` (addopts/testpaths empty) | PASSES: `--cov=src in addopts`, `testpaths == ["test"]` |
| `test_pytest_ini_env_block_present` | FAILS: `assert 'USE_WHISPER_FALLBACK = false' in []` | PASSES: env block contains it |

> Success of current verification does **not** establish historical TDD chronology; the reproduction is a
> freshness check of bad-vs-good header with unchanged tests/environment.

## Files to Modify
| File | Change |
|---|---|
| (none — production) | Working repair + existing tests preserved as-is |
| `tmp/isolated-pytest-repro/.../pytest.ini` | Disposable copy only: header toggled `[pytest]`↔`[tool:pytest]` |
| `plans/checkpoints/...red-green-proof.md` | Fresh canonical proof (RED+GREEN) via helper |
| `plans/checkpoints/...red-green-proof.rejected-v1.md` | Preserved prior/rejected proof, untouched |

## Acceptance / stop
- Working repair + existing tests preserved; focused check + mixed Node/Python `make test` pass in the same declared venv.
- Fresh evidence distinguishes bad vs good header (unchanged tests/env); copied scope recorded transparently; never claims pre-implementation history.
- Do NOT weaken/disable TDD or acceptance, invent a waiver, or treat proof formatting alone as semantic acceptance. If the evidence contract cannot accept this labelled reproduction, report that exact limitation + the current verification results — do not manufacture another cycle or add tests.

## Final note (fill after execution)
- Changed paths: **none for production**; disposable copy `tmp/isolated-pytest-repro/`, venv `.venv/`, fresh proof + preserved `...rejected-v1.md`.
- Commands/results: venv install, `test_config.py -v` (expected exit 0), `make test` (expected exit 0), isolated RED (non-zero, 2 config tests fail) + GREEN (exit 0) captured by helper.
- Proof location: `plans/checkpoints/task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df.red-green-proof.md`.
- Blockers: any missing venv dependency is a setup blocker, not RED.

---
*Vytvořeno: 2026-09-11*
*Status: DRAFT*
