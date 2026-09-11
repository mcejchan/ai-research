# Plan 2026-09-11: Fix ignored AI Research pytest.ini section (verification only)

Verification of the **already-applied** repair. No production change is made. The repair
(`youtube-transcript-pipeline/pytest.ini` line 1 `[tool:pytest]` → `[pytest]`) and the two
regression tests in `test/test_config.py` (`test_pytest_ini_section_is_read_by_pytest`,
`test_pytest_ini_env_block_present`) already exist and are preserved. This plan produces
trustworthy current verification plus a fresh, explicitly-labelled isolated RED/GREEN reproduction
of the original defect.

## Problem

- `pytest.ini` must use `[pytest]` (not `[tool:pytest]`) for pytest to read `addopts`,
  `testpaths`, and `env`. The repair is in place; it only needs trustworthy verification and
  task-bound proof.
- The tdd `proof-capture.py` helper (`/Users/michal/.config/opencode/skills/tdd/scripts/proof-capture.py`)
  writes to a **fixed** canonical path `plans/checkpoints/<TASK_ID>.red-green-proof.md`, requires a
  `TASK_ID` env var, **refuses to overwrite** an existing proof, and **validates that RED and GREEN use
  the identical command**. A hand-crafted, rejected proof already occupies that canonical path.

## Analysis

### Kontext z codebase [DONE]
- `youtube-transcript-pipeline/pytest.ini`:1 = `[pytest]` (already fixed). Lines 2-13: `testpaths`,
  `python_*`, `addopts = --cov=src ...`, `env =` block (6 vars). All intact.
- `youtube-transcript-pipeline/test/test_config.py`:44-61 — two regression tests load the ini via
  `pytest.Config.fromdictargs({}, ["-c", str(PIPELINE_ROOT / "pytest.ini")])` and assert
  `--cov=src in addopts`, `testpaths == ["test"]`, and `USE_WHISPER_FALLBACK = false in env`.
- `src/yt_pipeline.py`:149 — `from faster_whisper import WhisperModel` (lazy import inside
  `whisper_transcribe`); top-level imports are `pandas`, `dotenv`, `tqdm`. Both requirements files
  must be installed for the declared environment.
- Root `Makefile`:3-6 `test` runs node tests + `cd youtube-transcript-pipeline && ... python3 -m pytest`
  with the 5 env vars already supplied inline (so enabling the previously-ignored `env` block changes
  nothing for `make test` — no regression).
- `.gitignore` ignores `.venv/`, `__pycache__/`, `.pytest_cache/`, `htmlcov/`, `.coverage`, `tmp/`.

### Knowledge base [DONE]
- Prior proof for this task id existed at `plans/checkpoints/task-b521afdb-...red-green-proof.md`
  (hand-crafted, from the rejected plan) — it is the artifact to **preserve** as a previous-attempt
  file, not to overwrite.

## Solutions

1. Current verification only: install both requirements into one ignored venv, run the focused
   `test/test_config.py`, then root `make test`. Do not touch production config.
2. Isolated RED/GREEN reproduction (explicitly labelled, NOT the original development TDD):
   copy the pipeline into an ignored disposable dir, revert only the copied `pytest.ini` header to
   `[tool:pytest]`, run the two existing regression tests via the proof-capture helper (RED = genuine
   non-zero failure), revert the copied header back to `[pytest]`, rerun the **identical command**
   in the **identical venv** (GREEN = pass). Tests, plugins, assertions, and dependencies are unchanged
   between phases.
3. proof-capture canonical path is occupied by the rejected proof → preserve it as a clearly named
   previous-attempt file first so the free canonical path exists for the helper to write fresh RED/GREEN.

## Implementation

### Pre-implementation checklist
- [ ] Confirm production `pytest.ini:1` is `[pytest]` and the 2 regression tests exist (read-only, no edit).
- [ ] Confirm `.venv/` and `tmp/` are git-ignored (they are) so no tracked artifacts are created.

### Kroky implementace
1. **Create one repository-local ignored venv with BOTH requirements files.**
   ```
   python3 -m venv /Users/michal/Projects/ai-research/.venv
   /Users/michal/Projects/ai-research/.venv/bin/pip install \
     -r youtube-transcript-pipeline/requirements.txt \
     -r youtube-transcript-pipeline/requirements-dev.txt
   ```
2. **Record interpreter/plugin versions once** (missing deps are setup blockers, NEVER the RED):
   ```
   /Users/michal/Projects/ai-research/.venv/bin/python - \
     -c "import sys,pytest,pytest_cov,pytest_env,pytest_mock;print(sys.executable);print('pytest',pytest.__version__);print('pytest-cov',pytest_cov.__version__);print('pytest-env',pytest_env.__version__)"
   ```
3. **Current focused verification** from the pipeline dir (venv python, real absolute path):
   ```
   cd youtube-transcript-pipeline && /Users/michal/Projects/ai-research/.venv/bin/python -m pytest test/test_config.py -v
   ```
   Record command, cwd (`.../youtube-transcript-pipeline`), and exit. Do not assume historical counts.
4. **Root mixed Node/Python gate** (prepend venv bin to PATH so `python3` resolves to venv):
   ```
   cd /Users/michal/Projects/ai-research && PATH="/Users/michal/Projects/ai-research/.venv/bin:$PATH" make test
   ```
   Record command and exit.
5. **Preserve the rejected proof** so the helper's canonical path is free:
   ```
   mv plans/checkpoints/task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df.red-green-proof.md \
      plans/checkpoints/task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df.red-green-proof.rejected-v1.md
   ```
6. **Create the disposable isolated copy** (exclude environments, caches, generated artifacts):
   ```
   rsync -a --exclude='.venv' --exclude='__pycache__' --exclude='.pytest_cache' \
     --exclude='htmlcov' --exclude='.coverage' --exclude='*/__pycache__' \
     youtube-transcript-pipeline/ tmp/isolated-pytest-repro/youtube-transcript-pipeline/
   ```
7. **RED — revert ONLY the copied header** `tmp/isolated-pytest-repro/.../pytest.ini` line 1
   `[pytest]` → `[tool:pytest]`, then run via the helper from repo root (proof path resolves there):
   ```
   cd /Users/michal/Projects/ai-research && TASK_ID=task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df \
     python3 /Users/michal/.config/opencode/skills/tdd/scripts/proof-capture.py red -- \
     bash -c "cd /Users/michal/Projects/ai-research/tmp/isolated-pytest-repro/youtube-transcript-pipeline \
       && /Users/michal/Projects/ai-research/.venv/bin/python -m pytest test/test_config.py -v"
   ```
   Expect: genuine non-zero exit (the 2 config regression tests fail because the `[tool:pytest]`
   section is ignored). Record real timestamp/command/exit from the helper.
8. **GREEN — revert the copied header back to `[pytest]`** and rerun the **identical command** in the
   **identical venv**:
   ```
   cd /Users/michal/Projects/ai-research && TASK_ID=task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df \
     python3 /Users/michal/.config/opencode/skills/tdd/scripts/proof-capture.py green -- \
     bash -c "cd /Users/michal/Projects/ai-research/tmp/isolated-pytest-repro/youtube-transcript-pipeline \
       && /Users/michal/Projects/ai-research/.venv/bin/python -m pytest test/test_config.py -v"
   ```
   Expect: exit 0. The inner command string is byte-identical to step 7 (only the on-disk copied
   header differs), satisfying `validate_red_proof`'s identical-command check.

## Files to Modify

| Soubor | Změna |
|--------|-------|
| (none — production) | No permanent change; working repair + existing tests preserved as-is |
| `tmp/isolated-pytest-repro/.../pytest.ini` | Disposable copy only: header toggled `[pytest]`→`[tool:pytest]` (RED) then back to `[pytest]` (GREEN) |
| `plans/checkpoints/...red-green-proof.md` | Fresh canonical proof written by proof-capture (RED+GREEN) |
| `plans/checkpoints/...red-green-proof.rejected-v1.md` | Preserved prior/rejected hand-crafted proof, untouched |

## TDD

**Workflow for the implementing agent:**
1. Do NOT modify the working repository's `pytest.ini` or `test/test_config.py` — the repair and
   regression tests already exist; preserve both.
2. Set up the ignored venv with both requirements (steps 1-2). Missing deps are setup blockers, not RED.
3. Produce current verification (steps 3-4) and record real commands/cwd/exits.
4. Run the isolated reproduction (steps 5-8) using the tdd skill's `proof-capture.py` helper for
   genuine timestamps/commands/exits.
5. Label the proof file explicitly as a **fresh isolated reproduction of an already-implemented repair,
   NOT the original development sequence** — never claim it proves pre-implementation history.

### Isolated Reproduction (fresh, task-bound — not original TDD)

**Test file (existing, unchanged):** `youtube-transcript-pipeline/test/test_config.py`
**Target tests:** `test_pytest_ini_section_is_read_by_pytest`, `test_pytest_ini_env_block_present`
**Framework:** pytest (run inside disposable copy under `tmp/isolated-pytest-repro/`)
**Run command (RED and GREEN identical — only copied `pytest.ini` header differs on disk):**
```
bash -c "cd /Users/michal/Projects/ai-research/tmp/isolated-pytest-repro/youtube-transcript-pipeline && /Users/michal/Projects/ai-research/.venv/bin/python -m pytest test/test_config.py -v"
```
**Proof location (canonical, helper-managed):** `plans/checkpoints/task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df.red-green-proof.md`

| Test (both phases) | RED (copied header `[tool:pytest]`) | GREEN (copied header `[pytest]`) |
|------|------|------|
| `test_pytest_ini_section_is_read_by_pytest` | FAILS: `assert '--cov=src' in []` (addopts/testpaths empty) | PASSES: `--cov=src in addopts`, `testpaths == ["test"]` |
| `test_pytest_ini_env_block_present` | FAILS: `assert 'USE_WHISPER_FALLBACK = false' in []` (env block empty) | PASSES: env block contains `USE_WHISPER_FALLBACK = false` |

> Implement the RED/GREEN capture via `proof-capture.py` (steps 7-8). The helper supplies the
> nonzero-exit (RED) and zero-exit (GREEN) checks; do NOT add a separate controlled failing test.

### Regression
- [ ] Current `python3 -m pytest test/test_config.py -v` from `youtube-transcript-pipeline/` (step 3)
- [ ] Root `make test` mix of Node + Python in the same venv (step 4)

*Note: successful current verification does NOT establish historical TDD chronology; the isolated
reproduction is an explicitly labelled freshness check of the bad-vs-good header with unchanged tests/environment.*

## Dependencies

- `youtube-transcript-pipeline/requirements.txt` (incl. `faster-whisper`, `pandas`, `yt-dlp`,
  `youtube-transcript-api`, dotenv, tqdm) and `requirements-dev.txt` (pytest, pytest-cov, pytest-env,
  pytest-mock, coverage) — both installed into the single ignored venv.
- tdd skill `proof-capture.py` at `/Users/michal/.config/opencode/skills/tdd/scripts/proof-capture.py`
  (requires `TASK_ID=task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df` and a free canonical proof path).
- `node` (present at `/opt/homebrew/bin/node`) for the root `make test` Node checks.
- `rsync` for the disposable copy.

## Final note (record after execution)

- Changed paths: **none for production** (working repair + existing tests preserved); disposable copy under
  `tmp/isolated-pytest-repro/`, ignored venv `.venv/`, fresh proof + preserved `...rejected-v1.md`.
- Commands/results: venv install, focused `test/test_config.py` run (exit 0), root `make test` (exit 0),
  isolated RED (non-zero, 2 config tests fail) + GREEN (exit 0) as captured by the helper.
- Proof location: `plans/checkpoints/task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df.red-green-proof.md`
  (fresh, explicitly labelled as an isolated reproduction, not original development).
- Blockers: any missing dependency in the venv is a setup blocker, not RED. If the evidence contract
  cannot accept this explicitly labelled reproduction, report that exact limitation + the current
  verification results — do not manufacture another cycle or add tests to evade it.

---
*Vytvořeno: 2026-09-11*
*Status: DRAFT*
