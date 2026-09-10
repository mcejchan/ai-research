---
title: "Genuine RED for already-fixed config: use a missing declared plugin as the behavioral RED"
date: 2026-09-10
category: tooling
component: tooling
tags: [pytest, tdd, red-green, pytest-env, venv, proof-capture]
file_type: rules
---

# Genuine RED→GREEN for an already-fixed config task: use a missing declared plugin as the behavioral RED

When a TDD task asks to re-prove evidence for a fix that is **already in place**
(e.g. `pytest.ini` `[tool:pytest]` → `[pytest]` was already corrected and
committed), you cannot legitimately "revert the working repo" to manufacture a
failure. The task explicitly forbids reverting config merely to create RED.

## The problem

- Prior handwritten proof was **rejected** for missing structured
  timestamps/commands/exit codes.
- The two regression tests using `pytest.Config.fromdictargs` already pass.
- A broken import/API is **not valid RED** (tdd skill rule 3 + failure_handling).

## The solution

Find a *genuine behavioral* RED that the fix legitimately depends on but that is
absent in the host environment:

1. Check the **host interpreter** vs the **declared dev requirements**.
   Here: `/opt/homebrew/bin/python3` (Py 3.14) has `pytest` + `pytest-cov` but
   **NOT `pytest-env`**, while `requirements-dev.txt` declares `pytest-env>=0.8.0`.
2. Build a **repo-local virtualenv** (ignored by `.gitignore`) from that host
   interpreter, installing only `requirements.txt` first (no pytest-env).
3. Write a regression test whose assertion **depends on the missing plugin**:
   e.g. assert that a `pytest.ini` `env` block is actually applied to `os.environ`
    (`os.environ.get("USE_WHISPER_FALLBACK") == "false"`). Without `pytest-env`,
   the `env` block is silently ignored → assertion **FAILED** (genuine RED).
   With `pytest-env` installed (after `pip install -r requirements-dev.txt`) →
   assertion **PASSED** (GREEN).
4. RED and GREEN run the **identical** focused command
   (`python3 -m pytest test/test_config.py -v`); the only change between phases is
   installing the declared dev deps. This keeps the command stable so
   `proof-capture.py` accepts the pair.
5. The temp-copied-INI part (invalid `[tool:pytest]` vs valid `[pytest]` for
   testpaths/addopts/env) is plain pytest-core behavior and passes in both
   phases — it documents the fix; the **env-applied** assertion is the RED carrier.

## Provenance / how discovered

- Confirmed host plugin gap: `python3 -c "import importlib.util as u;
  print(u.find_spec('pytest_env') is not None)"` → `False`.
- `requirements-dev.txt` already lists `pytest-env` — so installing it is "ordinary
  dependency installation only", not a redesign.
- `.gitignore` already ignores `.venv/`, `htmlcov/`, `.coverage/` → venv + coverage
  outputs stay untracked/disposable.
- The env block in `pytest.ini` and the `make test` target supply the same env
  values, so enabling `env` did not change runtime behavior of `make test`
  (no regression) — worth noting in the proof.

## When to use

- Any "complete/verify an already-applied fix" task demanding fresh, structured
  TDD evidence.
- Whenever the host is missing a plugin that the project's dev requirements
  declare. Use that gap as the legitimate, behavioral RED carrier instead of
  inverting a working config.

## Pitfalls

- Do NOT use a broken import/API as RED — `proof-capture.py` and the tdd skill
  reject it ("RED failures must be about missing implementation, not broken test
  syntax").
- Do NOT revert the working `pytest.ini` to fake RED.
- If no legitimate missing regression exists, **report the evidence limitation**
  rather than inventing a cycle (the task explicitly allows this).
- Keep the focused command byte-identical between RED and GREEN, or
  `proof-capture.py` refuses the pair (command-change rejection).
- Rename the old rejected proof to a `.previous-attempt` artifact BEFORE running
  `proof-capture.py red`, so the helper can create a fresh file at the canonical
  path `plans/checkpoints/<task-id>.red-green-proof.md`.

## Related learnings

- `2026-09-10_pytest-section-tool-pytest-ignored.md` — the original silent-ignore
  defect.
- `2026-09-10_pytest-config-from-path-missing-use-fromdictargs.md` —
  `fromdictargs` is the valid API; `from_path` does not exist.
