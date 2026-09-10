# Plan 2026-09-10: Fix ignored AI Research pytest configuration

Corrections to a rejected plan (attempt 1). The one-line config fix
(`[tool:pytest]` → `[pytest]`) and the two existing characterization tests are
already committed and **correct** — keep them. This run only (1) adds **one**
small regression, and (2) produces a **fresh** task-bound TDD proof + current
verification via a repo-local venv. We do NOT re-narrate the previous run.

*Status: DRAFT*
*Vytvořeno: 2026-09-10*
*Task ID: task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df*

## Why attempt 1 was rejected (and the fix)
- **Overengineered**: attempt 1 added *three* temp-INI tests. Reduced to **one**
  new regression (below) that already covers the section distinction *and* the env
  carrier.
- **Invalid RED test**: attempt 1 asserted `os.environ.get("USE_WHISPER_FALLBACK")
  == "false"` after writing a temp INI *during* test execution. A temp `-c` INI
  **cannot** apply its `env` block to the already-running pytest process, so that
  assertion is unsound. **Dropped.** The corrected env check reads the config via
  `getini("env")` (pytest's own machinery + the `pytest-env` plugin registering
  the `env` option) — a genuine, reproducible failure point.

## Analysis (verified 2026-09-10)
- `youtube-transcript-pipeline/pytest.ini` — already `[pytest]` (line 1);
  `testpaths = test`, `addopts = --cov=src ... -v`, full `env` block. **Keep as-is;
  never revert to manufacture a failure.**
- `test/test_config.py` — `_load_pipeline_pytest_config()` + the 2 characterization
  tests (`test_pytest_ini_section_is_read_by_pytest`,
  `test_pytest_ini_env_block_present`) already use `pytest.Config.fromdictargs`
  (valid API; `from_path` does not exist). **Keep as-is.**
  - On host `/opt/homebrew/bin/python3` (Py 3.14.4, pytest 9.0.3, pytest-cov 7.0.0,
    **no pytest-env**), the focused run currently shows **1 failed**
    (`test_pytest_ini_env_block_present` → `ValueError: unknown config value: 'env'`).
    That is the genuine behavioral RED (missing declared dev dep), not a broken
    import/API.
- `requirements-dev.txt` declares `pytest-env>=0.8.0`; `requirements.txt` is runtime
  only. Root `Makefile` `test:` runs Node tests then `python3 -m pytest` with
  literal `python3` and explicit env vars. `make test` is the canonical gate.
- `plans/checkpoints/<task-id>.red-green-proof.md` exists (the **rejected handwritten
  proof**); `proof-capture.py` **refuses to overwrite** an existing proof, so it must
  be renamed to `.previous-attempt.md` first.
- `.gitignore` already ignores `.venv/`, `htmlcov/`, `.coverage`, `.pytest_cache/`.

## Solution (minimal)
- Keep the working `pytest.ini` + the 2 existing tests untouched.
- Add **one** new regression that (a) proves a temp `[tool:pytest]` INI is ignored
  (testpaths/addopts come back empty — pure pytest-core behavior) and (b) proves a
  temp `[pytest]` INI is read (testpaths/addopts), with the `env` block read via
  `getini("env")`. Part (b)'s `env` assertion is the **genuine RED→GREEN carrier**:
  it fails (`ValueError`) when the `pytest-env` plugin is absent and passes when
  present — without ever applying env to a running process.
- Drive a real RED→GREEN in an ignored repo-local venv: **RED** = venv with
  `requirements.txt` only (no pytest-env) → the new test + the existing env test
  fail; **GREEN** = add `requirements-dev.txt` (installs pytest-env) into the **same**
  venv, re-run the **identical** command → all pass.
- Then run current, reproducible verification (focused pytest + `make test`) in that
  venv, record versions/exit codes, and confirm a controlled failing test yields a
  nonzero exit.

## Implementation

### Pre-implementation checklist
- [ ] Confirm `pytest.ini` is `[pytest]` and the 2 existing tests are intact — do NOT change them.
- [ ] Rename the rejected proof to a labelled previous-attempt artifact (step 1) BEFORE running `proof-capture.py red`.

### Steps
1. **Preserve the old proof as a previous-attempt artifact** (so the helper can create a fresh proof at the canonical path):
   ```
   mv plans/checkpoints/task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df.red-green-proof.md \
      plans/checkpoints/task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df.red-green-proof.previous-attempt.md
   ```
   Optionally prepend a header: `# PREVIOUS ATTEMPT (rejected: missing structured timestamps/commands/exits)`.

2. **Create the repo-local ignored venv** (no global installs), starting at the RED state (runtime deps only, **no pytest-env**):
   ```
   /opt/homebrew/bin/python3 -m venv .venv
   .venv/bin/pip install -r youtube-transcript-pipeline/requirements.txt
   ```

3. **Add the one new regression** to `test/test_config.py` (append; do not touch the existing tests or `_load_pipeline_pytest_config`). See TDD skeleton. `tmp_path` is a built-in pytest fixture — no new import needed.

4. **RED** — run the focused command via `skill:tdd` `proof-capture.py red --` with the venv active (pytest-env **not** yet installed):
   ```
   TASK_ID=task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df python3 "$SKILL_DIR/scripts/proof-capture.py" red -- \
     .venv/bin/python3 -m pytest test/test_config.py -v
   ```
   (run **from** `youtube-transcript-pipeline/`). Confirm the new regression **and**
   `test_pytest_ini_env_block_present` **FAIL** for the `env`-option reason, then
   **verify** a fresh `plans/checkpoints/<task-id>.red-green-proof.md` was created
   with the RED section before any further work.

5. **GREEN** — install the declared dev deps into the **same** venv, then re-run the **identical** command via `proof-capture.py green --`:
   ```
   .venv/bin/pip install -r youtube-transcript-pipeline/requirements-dev.txt
   TASK_ID=task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df python3 "$SKILL_DIR/scripts/proof-capture.py" green -- \
     .venv/bin/python3 -m pytest test/test_config.py -v
   ```
   Confirm **0 failures**, then verify the GREEN section was appended.

6. **Current reproducible verification** — with the venv bin first on PATH
   (`export PATH="$(pwd)/.venv/bin:$PATH"`, so the literal `python3` in `make test`
   resolves to the venv):
   - From pipeline dir: `python3 -m pytest test/test_config.py -v` → record loaded
     `testpaths`/`addopts`/`env`, collection result, exit code.
   - From repo root: `make test` → record result + exit code (mixed Node/Python
     gate — do not replace it).
   - Record versions: `python3 --version`, `python3 -m pytest --version`, and
     `python3 -c "import importlib.metadata as m; print('pytest-cov', m.version('pytest-cov')); print('pytest-env', m.version('pytest-env'))"`.

7. **Controlled failing test → nonzero exit** — add a throwaway test (e.g. a temp
   file with `def test_x(): assert 1 == 0`), run `python3 -m pytest` on it, confirm
   a **nonzero** exit code, then delete it. Record command + exit code (proves the
   suite still fails loudly; no false-green).

8. **Final checkpoint** — write `plans/checkpoints/<task-id>.checkpoint.md` with:
   changed paths (only `test_config.py` appended + the new test), the fresh proof
   path, exact commands/results (RED, GREEN, focused, `make test`, controlled-fail),
   and any unresolved blocker. **Current** tests + proof — not historical success —
   determine completion.

9. **Docs (optional, only if non-obvious)** — one short "Test preparation" bullet
   (venv from `/opt/homebrew/bin/python3` + `requirements.txt` then
   `requirements-dev.txt`) in pipeline README `## 🧪 Testování`. No dependency/app redesign.

10. **save-learning** (mandatory, last action).

## Files to modify

| File | Change |
|------|--------|
| `youtube-transcript-pipeline/test/test_config.py` | **Append** one new regression (temp-copied INI, section distinction + `getini("env")`). Do NOT modify the 2 existing tests or `_load_pipeline_pytest_config`. |
| `plans/checkpoints/<task-id>.red-green-proof.md` | **Fresh** proof via `proof-capture.py` (old one renamed to `.previous-attempt.md`). |
| `plans/checkpoints/<task-id>.red-green-proof.previous-attempt.md` | **Renamed** from the rejected proof (preserved, labelled). |
| `plans/checkpoints/<task-id>.checkpoint.md` | **New** final checkpoint. |
| `youtube-transcript-pipeline/pytest.ini` | **No change** — already `[pytest]`. |
| `youtube-transcript-pipeline/README.md` | **Optional** — one-line venv/test-prep note only if needed. |

## TDD

**Workflow for the implementing agent (per `skill:tdd`):**
> Implement the TDD cycle per `skill:tdd` — RED/GREEN evidence is captured into
> `plans/checkpoints/task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df.red-green-proof.md`
> using `scripts/proof-capture.py`. Before RED, rename the old rejected proof to
> `...red-green-proof.previous-attempt.md` so the helper can create a fresh file.
> Derive `SKILL_DIR` from the loaded `skill:tdd` `SKILL.md`; never use
> `~/.openclaw/workspace`.

### Targeted tests
- **Test file:** `youtube-transcript-pipeline/test/test_config.py` (append; existing 4 tests + 2 new characterization tests untouched).
- **Framework:** pytest 9.x in an ignored `.venv/` (RED without pytest-env, GREEN with it).
- **Run command (identical for RED and GREEN), from `youtube-transcript-pipeline/`:**
  ```
  .venv/bin/python3 -m pytest test/test_config.py -v
  ```
- **Edit hint:** APPEND a new `def test_...` after `test_pytest_ini_env_block_present`.

### Runnable skeleton (append to `test_config.py`)
```python
def test_temp_ini_distinguishes_invalid_tool_pytest_section(tmp_path):
    bad = tmp_path / "bad.ini"
    bad.write_text("[tool:pytest]\ntestpaths = test\naddopts = --cov=src -v\n")
    cfg_bad = pytest.Config.fromdictargs({}, ["-c", str(bad)])
    assert cfg_bad.getini("testpaths") == []
    assert cfg_bad.getini("addopts") == []

    good = tmp_path / "good.ini"
    good.write_text(
        "[pytest]\ntestpaths = test\naddopts = --cov=src -v\n"
        "env =\n    USE_WHISPER_FALLBACK = false\n"
    )
    cfg_good = pytest.Config.fromdictargs({}, ["-c", str(good)])
    assert cfg_good.getini("testpaths") == ["test"]
    assert "--cov=src" in cfg_good.getini("addopts")
    assert "USE_WHISPER_FALLBACK = false" in cfg_good.getini("env")
```
`tmp_path` is a built-in pytest fixture; `pytest` is already imported. No new import.

The last assertion (`getini("env")`) is the **genuine RED→GREEN carrier**: it raises
`ValueError: unknown config value: 'env'` when the `pytest-env` plugin is absent and
returns the list once `pytest-env` is installed. It checks the *config* (read via
pytest's machinery) and never applies env to a running process — avoiding attempt 1's
invalid `os.environ` approach.

### RED/GREEN table
| Test | RED (venv, no pytest-env) | GREEN (venv, + requirements-dev) |
|------|----------------------------|----------------------------------|
| `test_temp_ini_distinguishes_invalid_tool_pytest_section` | **FAILED** — `getini("env")` → `ValueError: unknown config value: 'env'` | **PASSED** |
| `test_pytest_ini_env_block_present` (existing) | **FAILED** — same `ValueError` on the real `pytest.ini` | **PASSED** |
| `test_pytest_ini_section_is_read_by_pytest` (existing) | passed | passed |

Note: the `[tool:pytest]` portion of the new test (testpaths/addopts) is core
pytest behavior and passes in both phases; the `env` assertion is what carries the
genuine RED. If, after venv prep, no legitimate missing regression remains, report
that **evidence limitation** rather than inventing a cycle — but the `env`-option
gap above is a genuine, available RED, so a cycle is expected.

### Regression
- [ ] Focused `python3 -m pytest test/test_config.py -v` (RED then GREEN) via `proof-capture.py`.
- [ ] Full pipeline suite `python3 -m pytest -q` after GREEN — record the **actual** count (42–44 are historical baselines, **not** a fixed assertion).
- [ ] Root `make test` (mixed Node/Python gate) — record result + exit code.
- [ ] Controlled failing temp test → confirm **nonzero** exit, then remove it.

## Dependencies
- Host `/opt/homebrew/bin/python3` (Py 3.14.4): pytest 9.0.3, pytest-cov 7.0.0, **no pytest-env**.
- `requirements.txt` (runtime) + `requirements-dev.txt` (declares `pytest-env>=0.8.0`) — ordinary `pip` install **inside the ignored `.venv/` only; no global installs**.
- `skill:tdd` → `scripts/proof-capture.py` for structured proof capture.
- `.gitignore` already ignores `.venv/`, `htmlcov/`, `.coverage`, `.pytest_cache/` — temp coverage outputs stay untracked/disposable.
- No new external deps, no network/credentials, no app behavior change.
