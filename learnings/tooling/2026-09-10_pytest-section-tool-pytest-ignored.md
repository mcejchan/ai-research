---
title: "pytest.ini [tool:pytest] vs [pytest] — silently ignored config"
date: 2026-09-10
category: tooling
component: tooling
tags: [pytest, pytest-cov, pytest-env, config, test-gate]
file_type: rules
---

# pytest.ini `[tool:pytest]` vs `[pytest]` — silently ignored config

In a `pytest.ini` file the valid section header is `[pytest]`. Using `[tool:pytest]` (the `setup.cfg` form) makes pytest ignore the WHOLE file — `testpaths`, `addopts` (incl. `--cov=...`) and any `env` block (pytest-env) are never applied. The suite still runs because pytest falls back to default discovery, and any env values supplied on the command line / Makefile mask the missing `env` block. Result: a silent, not-a-no-op defect — tests pass but coverage and configured env are dropped.

## Detection
- Inspect `pytest.ini`/`pytest.cfg`/`tox.ini`/`setup.ini` for a `[tool:pytest]` header.
- `pytest -c pytest.ini --collect-only -q` and compare against an explicit `python_files` glob.
- `python3 -c "import pytest; c=pytest.Config.from_path('pytest.ini'); print(c.getini('addopts')); print(c.getini('testpaths')); print(c.getini('env'))"` — if all three return `[]`/empty, the section is being ignored.

## Fix
- Change only the section header `[tool:pytest]` → `[pytest]`. Keep all other lines.

## Why it stayed hidden in ai-research
- The root `Makefile` test target re-supplies the same env values explicitly, so dropping the `env` block changed no runtime behavior.
- The `python_files`/`python_classes`/`python_functions` globs equal pytest defaults, so enabling `testpaths=test` does not change test count (42 → 42).

## Characterization test (proves the fix)
```python
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_pytest_ini_section_is_read_by_pytest():
    cfg = pytest.Config.from_path(ROOT / "pytest.ini")
    addopts = cfg.getini("addopts")
    assert "--cov=src" in addopts        # RED before fix (addopts == []); GREEN after [pytest]
    assert cfg.getini("testpaths") == ["test"]

def test_pytest_ini_env_block_present():
    cfg = pytest.Config.from_path(ROOT / "pytest.ini")
    assert "USE_WHISPER_FALLBACK = false" in cfg.getini("env")
```

## When to use
- Any project where `pytest.ini`/`pytest.cfg`/`tox.ini` looks "configured but not taking effect."
- Auditing coverage reports that come back empty despite `--cov` being declared.
