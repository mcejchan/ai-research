# Plan 2026-09-10: Fix ignored AI Research pytest configuration

Complete and verify the existing pytest-config repair. The working fix is already
in place and committed; the deliverables are (1) a fresh, genuine RED→GREEN TDD
cycle for a *new* regression test, and (2) current reproducible verification via a
repo-local venv. We do NOT re-explain the previous run.

*Status: DRAFT*
*Vytvořeno: 2026-09-10*
*Task ID: task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df*

---

## Problem

`youtube-transcript-pipeline/pytest.ini` previously used the invalid
`[tool:pytest]` section, so pytest silently ignored `testpaths`/`addopts`/`env`
(coverage + env config never took effect). A prior attempt fixed the section to
`[pytest]` and added two characterization tests using `pytest.Config.fromdictargs`
(valid API; `from_path` does not exist). Those changes are correct and **already
committed**. The prior handwritten proof was **rejected** for missing structured
timestamps/commands/exit codes.

This task: preserve the working fix, add one genuine new regression (temp-copied
INI distinguishing invalid `[tool:pytest]` from valid `[pytest]`), and produce a
**fresh** task-bound TDD proof via `skill:tdd` + its `proof-capture.py` helper, plus
current verification through a repo-local venv.

## Analysis

### Kontext z codebase (verified 2026-09-10)

- `youtube-transcript-pipeline/pytest.ini` — **already `[pytest]`** (line 1),
  with `testpaths = test`, `addopts = --cov=src ... -v`, and an `env` block
  (PYTHONPATH, OPENAI_API_KEY, LANG, USE_WHISPER_FALLBACK, MAKE_EMBEDDINGS,
  DRIVE_FOLDER_ID). **Keep as-is; do not revert to manufacture a failure.**
- `youtube-transcript-pipeline/test/test_config.py` — contains
  `_load_pipeline_pytest_config()` + the two regression tests
  `test_pytest_ini_section_is_read_by_pytest` and `test_pytest_ini_env_block_present`
  using `pytest.Config.fromdictargs({}, ["-c", <pytest.ini>])`. **Keep as-is.**
- `requirements-dev.txt` declares `pytest`, `pytest-mock`, `pytest-cov`, `coverage`,
  `pytest-env>=0.8.0`.
- `requirements.txt` declares the runtime deps (openai, python-dotenv, yt-dlp, …).
- Root `Makefile` `test:` target (line 6) runs the focused pytest with literal
  `python3` and explicit env vars matching the `env` block; also runs Node tests.
- Old proof: `plans/checkpoints/task-b521afdb-...red-green-proof.md` (rejected).
- Old checkpoint: `plans/checkpoints/task-b521afdb-...checkpoint.md` (deleted in
  working tree — do not restore).

### Relevantní dokumentace

- Pipeline README `## 🧪 Testování` — documents `pytest` / `pip install -r
  requirements-dev.txt`. If the venv/preparation step is needed, add one short
  "Test preparation" note here (doc-only, optional).
- Root `CLAUDE.md` — `make test` is the canonical gate.

### Knowledge base

- `skill:tdd` — governs the RED→GREEN cycle and the mandatory proof file at
  `plans/checkpoints/<task-id>.red-green-proof.md`. Proof must be machine-captured
  by `scripts/proof-capture.py` (structured timestamps/commands/exit codes), not
  hand-written.
- `skill:save-learning` — mandatory at task end.

## Available Skills

- **tdd** — run `proof-capture.py red/green` to record the cycle. Use for the
  RED→GREEN cycle in the TDD section.
- **save-learning** — final mandatory step, saves what was learned.

## Solutions

**Genuine (non-broken-import) RED → GREEN design.** The new regression test asserts
that the `env` block of a `[pytest]` INI is actually **applied** to `os.environ`
(e.g. `USE_WHISPER_FALLBACK == "false"`). Applying `env` requires the **pytest-env**
plugin, which is **missing from the host `/opt/homebrew/bin/python3`** (Py 3.14,
has pytest/pytest-cov but NOT pytest-env) and is declared only in
`requirements-dev.txt`. Therefore:

- **RED**: a repo-local venv created from `/opt/homebrew/bin/python3` with only
  `requirements.txt` installed (no pytest-env) → the env-applied assertion fails.
  Genuine behavior failure, not a broken import/API.
- **GREEN**: after installing `requirements-dev.txt` (adds pytest-env) into the same
  venv → the same assertion passes.

Both RED and GREEN run the **identical** focused command
`python3 -m pytest test/test_config.py -v`, so `proof-capture.py` accepts them as a
valid chronological pair. The new test also asserts the `[tool:pytest]` (invalid) vs
`[pytest]` (valid) distinction for `testpaths`/`addopts`/`env` via temp-copied INIs
(this part is pytest-core behavior and passes in both phases; the env-applied
assertion is what carries the genuine RED→GREEN).

If, after the venv prep, no legitimate missing regression remains, the task permits
reporting that **evidence limitation** instead of inventing a cycle — but the
env-applied assertion above is a genuine, available RED, so a cycle is expected.

## Implementation

### Pre-implementation checklist
- [ ] Confirm `youtube-transcript-pipeline/pytest.ini` is `[pytest]` (do not change).
- [ ] Confirm the two existing regression tests in `test_config.py` are intact (do not change).
- [ ] Back up the rejected proof to a clearly-labelled previous-attempt artifact
      (see step 1) BEFORE running `proof-capture.py`, so the helper can create a
      fresh `...red-green-proof.md` at the canonical path.

### Kroky implementace

1. **Preserve old proof as previous-attempt artifact.**
   Rename the rejected file so `proof-capture.py` can create a fresh one:
   ```
   mv plans/checkpoints/task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df.red-green-proof.md \
      plans/checkpoints/task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df.red-green-proof.previous-attempt.md
   ```
   Optionally prepend a header line `# PREVIOUS ATTEMPT (rejected: missing structured timestamps/commands/exits)`.

2. **Prepare repo-local ignored venv** (no global installs). `.gitignore` already
   ignores `.venv/`, `htmlcov/`, `.coverage/`, `.pytest_cache/`.
   ```
   /opt/homebrew/bin/python3 -m venv /Users/michal/Projects/ai-research/.venv
   # RED state: only runtime deps (no pytest-env)
   /Users/michal/Projects/ai-research/.venv/bin/pip install -r youtube-transcript-pipeline/requirements.txt
   ```

3. **Add the new regression test** to
   `youtube-transcript-pipeline/test/test_config.py` (append, do not touch the
   existing tests). See the TDD skeleton below for exact code.

4. **RED**: run the focused command through `skill:tdd` `proof-capture.py red --`
   with the venv active but **pytest-env not yet installed** (from step 2).
   Confirm the env-applied test fails. VERIFY the fresh
   `plans/checkpoints/<task-id>.red-green-proof.md` was created with the RED section
   before writing more.

5. **GREEN**: install dev deps into the same venv, re-run the same command.
   ```
   /Users/michal/Projects/ai-research/.venv/bin/pip install -r youtube-transcript-pipeline/requirements-dev.txt
   ```
   Run through `proof-capture.py green --` with the **identical** command. Verify
   the GREEN section was appended.

6. **Current verification (reproducible).** With venv bin first on PATH
   (`export PATH=/Users/michal/Projects/ai-research/.venv/bin:$PATH`):
   - From pipeline dir: `python3 -m pytest test/test_config.py` → record loaded
     `testpaths`/`addopts`/`env`, collection result, exit code.
   - From repo root: `make test` → record result + exit code (mixed Node/Python
     gate; do not replace it).
   - Record interpreter + plugin versions: `python3 --version`,
     `python3 -m pytest --version`, `python3 -c "import importlib.metadata as m;
     print('pytest-env', m.version('pytest-env')); print('pytest-cov',
     m.version('pytest-cov'))"`.

7. **Controlled failing test → nonzero exit.** Temporarily add a deliberately
   failing test (e.g. `assert 1 == 0`) in a throwaway test file (or a temp test),
   run `python3 -m pytest` on it, confirm **nonzero exit code**, then remove it.
   Record the command + exit code. This proves the suite still fails loudly when a
   test is broken (not a false-green).

8. **Final checkpoint.** Write
   `plans/checkpoints/<task-id>.checkpoint.md` with: changed paths (only
   `test_config.py` appended + the new test), fresh proof path, exact commands +
   results (RED/GREEN + focused + make test + controlled-fail), and any unresolved
   blocker.

9. **Docs (optional, only if needed).** If the venv prep is non-obvious, add one
   short "Test preparation" bullet to pipeline README `## 🧪 Testování` and/or
   root CLAUDE.md. No dependency/app redesign.

## Files to Modify

| Soubor | Změna |
|--------|-------|
| `youtube-transcript-pipeline/test/test_config.py` | **Append** new regression test(s) using temp-copied INIs; do NOT modify the 2 existing tests or `_load_pipeline_pytest_config`. |
| `plans/checkpoints/<task-id>.red-green-proof.md` | **Fresh** TDD proof via `proof-capture.py` (old one renamed to `.previous-attempt.md`). |
| `plans/checkpoints/<task-id>.checkpoint.md` | **New** final checkpoint (changed paths, commands/results, blockers). |
| `plans/checkpoints/<task-id>.red-green-proof.previous-attempt.md` | **Renamed** from the rejected proof (preserved, labelled). |
| `youtube-transcript-pipeline/pytest.ini` | **No change** — already `[pytest]`, keep it. |
| `youtube-transcript-pipeline/README.md` / root `CLAUDE.md` | **Optional** — one-line venv/test-prep note only if needed. |

## TDD

**Workflow pro implementujícího agenta (dle skill:tdd):**
> Implementace TDD cyklu dle skill:tdd — RED/GREEN evidence se zapisuje do
> `plans/checkpoints/task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df.red-green-proof.md`
> pomocí `scripts/proof-capture.py`. Before running RED, rename the old rejected
> proof to `...red-green-proof.previous-attempt.md` so the helper can create a
> fresh file at the canonical path.

### Targeted Tests

**Test file:** `youtube-transcript-pipeline/test/test_config.py` (append new
functions; existing 4 tests untouched)
**Framework:** pytest 9.x (host) / venv pytest with pytest-env
**Run command (identical for RED and GREEN):**
```
PATH=/Users/michal/Projects/ai-research/.venv/bin:$PATH python3 -m pytest test/test_config.py -v
```
(run **from** `youtube-transcript-pipeline/`)

**Edit hint:** APPEND below the existing two regression tests (after
`test_pytest_ini_env_block_present`). Do not edit them.

### Runnable skeleton (appended to test_config.py)

```python
import textwrap

_TMP_INI = textwrap.dedent(
    """
    [{section}]
    testpaths = test
    addopts = --cov=src -v
    env =
        LANG = cs
        USE_WHISPER_FALLBACK = false
    """
)


def _write_temp_ini(tmp_path, section: str) -> Path:
    p = tmp_path / "pytest.ini"
    p.write_text(_TMP_INI.format(section=section))
    return p


def test_temp_tool_pytest_section_is_ignored(tmp_path):
    """Invalid [tool:pytest] section must be ignored by pytest."""
    p = _write_temp_ini(tmp_path, "tool:pytest")
    cfg = pytest.Config.fromdictargs({}, ["-c", str(p)])
    assert cfg.getini("addopts") == []
    assert cfg.getini("testpaths") == []
    assert "USE_WHISPER_FALLBACK = false" not in cfg.getini("env")


def test_temp_pytest_section_is_read(tmp_path):
    """Valid [pytest] section must be read (testpaths/addopts/env)."""
    p = _write_temp_ini(tmp_path, "pytest")
    cfg = pytest.Config.fromdictargs({}, ["-c", str(p)])
    assert "--cov=src" in cfg.getini("addopts")
    assert cfg.getini("testpaths") == ["test"]
    assert "USE_WHISPER_FALLBACK = false" in cfg.getini("env")


def test_env_block_is_applied_to_environment(tmp_path):
    """Genuine RED carrier: env block is only applied to os.environ when
    the pytest-env plugin is installed. Fails (RED) without pytest-env,
    passes (GREEN) after requirements-dev is installed."""
    _write_temp_ini(tmp_path, "pytest")
    # -c temp.ini carries the env block; pytest-env must apply it.
    assert os.environ.get("USE_WHISPER_FALLBACK") == "false"
```

Note: `Path` is already imported at the top of `test_config.py` (`from pathlib
import Path`). `os` is already imported. `pytest` is already imported. `textwrap`
must be added to the top import block (the only new import).

### RED/GREEN table

| Test | RED (venv w/o pytest-env) | GREEN (venv w/ pytest-env) |
|------|---------------------------|----------------------------|
| `test_temp_tool_pytest_section_is_ignored` | passes (core behavior) | passes |
| `test_temp_pytest_section_is_read` | passes (core behavior) | passes |
| `test_env_block_is_applied_to_environment` | **FAILED** — `USE_WHISPER_FALLBACK` not in `os.environ` (no plugin to apply `env`) | **PASSED** — plugin applies `env` block |

The genuine RED is `test_env_block_is_applied_to_environment` failing for a
behavioral reason (env not applied because `pytest-env` is absent), **not** a
broken import/API. RED and GREEN run the **same** command; the only change between
phases is installing `requirements-dev.txt` (adds pytest-env) into the venv.

### Regression
- [ ] Focused `python3 -m pytest test/test_config.py -v` (RED then GREEN) — via `proof-capture.py`.
- [ ] Full pipeline suite `python3 -m pytest -q` after GREEN — record count (the
      prior run reported 44 = 42 baseline + 3… 42+2 existing characterization + the
      3 new = expect ~47; counts are a **historical baseline, not a fixed
      assertion** — record the actual number).
- [ ] Root `make test` (mixed Node/Python gate) — record result + exit code.
- [ ] Controlled failing temp test → confirm **nonzero** exit, then remove it.

## Dependencies

- Host `/opt/homebrew/bin/python3` (Python 3.14.4) — has pytest/pytest-cov,
  **missing pytest-env**.
- `requirements-dev.txt` (already declares pytest-env>=0.8.0) + `requirements.txt`
  — ordinary `pip` install only, inside the ignored `.venv/`; **no global installs**.
- `skill:tdd` → `scripts/proof-capture.py` for structured proof capture.
- `.gitignore` already ignores `.venv/`, `htmlcov/`, `.coverage/`,
  `.pytest_cache/` — temporary coverage outputs stay untracked/disposable.
- No new external deps, no network/credentials, no app behavior change.


## Review Feedback

The plan overengineers a one-line configuration fix, and its proposed RED test is invalid because creating a temporary INI during test execution cannot apply its `env` settings to the already-running pytest process.
