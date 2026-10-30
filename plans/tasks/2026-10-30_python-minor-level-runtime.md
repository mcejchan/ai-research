---
title: "ai-research make test: accept CPython 3.15.x instead of exact 3.15.0"
type: implementation
---

# ai-research make test: accept CPython 3.15.x instead of exact 3.15.0

## Goal
The `test` target in `Makefile` accepts the project `.venv` when it is CPython 3.15.x, not only 3.15.0.

## Files
- Tests above in `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py`.
- `Makefile` lines ~6–13 (identity string compare `'CPython 3.15.0'`), `.python-version` (`3.15.0` → `3.15`), `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py`.

## Change
Accept identity `CPython 3.15.<any>`; messages "CPython 3.15.x".

## Also fix
`test_make_test_uses_real_python_315_and_runs_pytest_child` and `test_make_test_propagates_pytest_arguments_and_failure_status` compare `Path(sys.executable).resolve()` with the interpreter path printed by `make test`. They fail when `.venv` was created from the stable Homebrew link `/opt/homebrew/opt/python@3.15/...` (the canonical way, survives patch upgrades) because resolve() yields the versioned Cellar path. Compare both sides after `os.path.realpath`, or compare implementation+version instead of the path.

## Boundaries
Keep refusal for missing `.venv`, 3.14 and non-CPython; no other targets or dependencies.

## Verification
Implement the TDD cycle using skill:tdd: 3.15.7 accepted, 3.14.4/PyPy rejected. Registered gate green.
