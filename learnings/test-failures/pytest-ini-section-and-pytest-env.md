---
title: "pytest.ini: correct section + pytest-env plugin for env/testpaths/addopts"
date: 2026-09-10
category: test-failures
component: tooling
tags: [pytest, pytest-env, config, tdd, regression]
file_type: rules
---

# pytest.ini `env`/`testpaths`/`addopts` need the right section AND the pytest-env plugin

When writing regression tests that assert on pytest's config (via
`pytest.Config.fromdictargs({}, ["-c", <ini>])`), two independent gotchas bite:

## 1. Section name
`[pytest]` is the correct section for a `pytest.ini` file. `[tool:pytest]` is the
section for `pyproject.toml`. With the wrong section, pytest **silently ignores the
whole file** — `getini("testpaths")`, `getini("addopts")`, etc. all come back empty,
yet the suite still runs via default discovery (a silent defect, not a no-op).

## 2. `env` is a plugin-registered ini option
`getini("env")` raises `ValueError: unknown configuration value: 'env'` (and emits a
`PytestConfigWarning: Unknown config option: env`) **unless the `pytest-env` plugin is
installed**. `pytest-env` is what registers the `env` ini key. So a test asserting on
`cfg.getini("env")` is a genuine RED when `pytest-env` is absent and GREEN once it is
installed — a clean behavioral RED/GREEN without touching a running process.

## 3. A temp `-c` INI cannot apply `env` to a running pytest process
A proposed test that wrote a temp INI during execution and then asserted
`os.environ.get("USE_WHISPER_FALLBACK") == "false"` was **rejected**: a temp `-c` config
loaded mid-test cannot retroactively apply its `env` block to the already-running
process. Assert on the **config object** (`getini("env")`), never on `os.environ`, when
the point is to verify the ini is read.

## Valid vs invalid RED
- Valid RED: a behavioral gap (missing declared dev dep `pytest-env`) → the assertion
  genuinely fails for the expected reason.
- Invalid RED: a broken import / wrong API (e.g. `pytest.Config.from_path`, which does
  not exist) — this is a test bug, not real evidence. Use `fromdictargs`, the real API.

## Practical
- To prove a config fix without breaking anything, run focused pytest in an ignored
  repo-local venv: RED = `requirements.txt` only (no `pytest-env`), GREEN = add
  `requirements-dev.txt` (declares `pytest-env>=0.8.0`). Same venv, same command for both.
- `proof-capture.py` refuses to record false RED (exit 0) / false GREEN (nonzero), and
  refuses to overwrite an existing proof — rename the old (rejected) proof to
  `.previous-attempt.md` first so the helper can create a fresh one.
- Counts like 42/44 are historical baselines, not fixed assertions — record the actual number.
