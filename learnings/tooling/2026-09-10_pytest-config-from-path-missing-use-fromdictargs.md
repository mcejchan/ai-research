---
title: "pytest Config: from_path does not exist; use fromdictargs"
date: 2026-09-10
category: tooling
component: tooling
tags: [pytest, pytest-cov, pytest-env, config, characterization-test]
file_type: rules
---

# pytest: `Config.from_path` does not exist; use `fromdictargs`

When a plan/skeleton suggests `pytest.Config.from_path("pytest.ini")` to load an
ini file programmatically, it will crash in pytest 8.4.2:

```
AttributeError: type object 'Config' has no attribute 'from_path'
```

`from_path` is not a public API. The real ways to build a `Config` from a
config file / ini are:

```python
# Load a specific config file the way a test program would (the only public
# entry points that exist in pytest 8.4.2):
cfg = pytest.Config.fromdictargs({}, ["-c", str(path / "pytest.ini")])
addopts  = cfg.getini("addopts")     # list, honors [pytest] only
testpaths = cfg.getini("testpaths")  # list
env       = cfg.getini("env")        # pytest-env: list of "K = V" strings

# Or go through the real CLI parse path:
cfg = pytest.pytest_cmdline_main([...])   # side-effecting; returns exit code
```

## Why this matters

A characterization test that *proves* a `pytest.ini` section is honored must read
the file through pytest's own config machinery. `fromdictargs({}, ["-c", f])`
does exactly that: it locates the file (so `inipath` points at it) but, if the
section header is wrong (e.g. `[tool:pytest]` instead of `[pytest]`), returns
empty values for every key. That is precisely the signal you want for a RED
test — non-trivial, but not an `AttributeError` masking the real assertion.

## Detection / verification

- `python3 -c "import pytest; c=pytest.Config.fromdictargs({}, ['-c','pytest.ini']); print(c.getini('addopts')); print(c.getini('testpaths')); print(c.getini('env'))"`
  - All three `[]`/empty  => section is being ignored (wrong header or wrong file type).
  - Non-empty  => section is honored.
- `pytest -c pytest.ini --collect-only -q` to confirm a test count and that
  `testpaths` is applied.

## When to use

- Writing characterization tests that load a project's pytest config in-process.
- Auditing whether a `pytest.ini`/`pytest.cfg`/`tox.ini` config is actually taking
  effect (especially after noticing coverage/env "silently dropped").
- Any time a documented/plan API name looks right but throws `AttributeError` on
  `pytest.Config` — prefer `fromdictargs` over the non-existent `from_path` /
  `from_fileargs`.
