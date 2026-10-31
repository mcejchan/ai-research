---
tdd:
  decision: required
  reason: Changing the executable runtime gate requires regression tests for accepted patch versions and rejected implementations and minor versions.
---
# Plan
## Analysis
- Preserve `Makefile:6–14` project-local interpreter selection, inspection failure handling, pytest environment/argv, and hostile-PATH protection; replace only the exact-version check and diagnostics.
- Reuse `_synthetic_checkout`, `_write_executable`, and `_run` in `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py`; update its synthetic `.python-version` and exact-version expectations.
- Follow `README.md:7–15`: root `make test` is the repository-wide gate; leave subsystem targets and dependencies intact.
- Apply `learnings/tooling/safe-synthetic-python-runtime-fixtures.md`: unlink synthetic interpreter symlinks before writing wrappers; run real-child tests under CPython 3.15 with pytest available.
- Apply `learnings/tooling/2026-10-25_pin-make-test-execution-to-the-project-interpreter.md` for interpreter provenance, superseding only its historical exact-patch requirement.
- Retain pytest.ini-provided test environment via `python -m pytest`; knowledge search used backend `local`, collection `ai-research-learnings`, diagnostic `Collection not found`.
## Approach
- Keep full implementation/version identity for diagnostics. Accept only prefix `CPython 3.15.` followed by a nonempty numeric patch; use POSIX shell `case`/parameter expansion in the existing recipe, preserving Makefile dollar escaping.
- Compare the observed child executable and expected interpreter with `os.path.realpath` on both sides; assert CPython plus major/minor 3.15 independently of patch.
## Implementation
1. Load `skill:tdd`; add the parameterized regression below first and capture genuine RED for CPython 3.15.7 before editing Makefile or `.python-version`.
2. Extend rejection coverage for CPython 3.14.4 and PyPy 3.15.7; retain missing-runtime refusal, no ambient-python fallback, and no pytest child on rejection. Update missing/invalid diagnostics expectations to `CPython 3.15.x`.
3. Change root `.python-version` from `3.15.0` to `3.15`; update the synthetic fixture to mirror it and assert the repository pin is `3.15`.
4. Replace Makefile's exact identity comparison with the bounded numeric-patch check; change both expected-runtime messages to `CPython 3.15.x`. Leave identity-inspection errors and all execution wiring intact.
5. In the real-child fixture, print an unambiguous executable marker; parse it and compare `os.path.realpath(observed)` to `os.path.realpath(sys.executable)`. Replace the hardcoded `CPython 3.15.0` assertion with implementation and major/minor assertions. Exercise a synthetic intermediate symlink representing Homebrew's stable-link layout using the actual interpreter; keep a genuine Python child rather than substituting identity output for that test.
6. Preserve `test_make_test_propagates_pytest_arguments_and_failure_status` argv and exit-23 assertions. It currently embeds a resolved interpreter path but has no observed-path assertion: use the selected executable safely in its wrapper and normalize both sides if adding a printed-path assertion; do not assert raw link spelling.
7. Capture focused GREEN, run the registered gate, and inspect the final diff for exactly the three authorized implementation files plus task evidence required by skill:tdd. Record precise commands, working directories, exits, and any prerequisite blocker.
## Files
- `Makefile`: CPython 3.15 numeric-patch acceptance and `CPython 3.15.x` diagnostics only.
- `.python-version`: minor-series selector `3.15`.
- `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py`: runtime matrix, stable-link provenance checks, patch-independent real-child assertions, and updated pin/messages.
## Testing
- From `youtube-transcript-pipeline/`, run `../.venv/bin/python -m pytest -q test/test_research_python_runtime_contract.py` for both RED and GREEN; use the identical command/cwd for proof capture.
- Verify acceptance of CPython 3.15.0 and 3.15.7, rejection of CPython 3.14.4 and PyPy, missing `.venv` refusal, real pytest-child execution, hostile-PATH exclusion, exact `-m pytest` argv, and failure status propagation.
- Run `make test` with working directory `/Users/michal/Projects/ai-research`, equivalent to registered `cd ~/Projects/ai-research && make test`; require the aggregate Node/Python gate to pass. Record any missing CPython 3.15/pytest prerequisite without substituting ambient Python or claiming GREEN.
- Inspect `git diff` and `git status --short`; preserve other targets/dependencies and do not create a separate learning file.
## TDD
- Implement the TDD cycle using `skill:tdd`; store its canonical task-scoped RED/GREEN proof. Append this runnable skeleton to `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py` using existing helpers/imports plus `pytest`:

```python
import pytest


@pytest.mark.parametrize("identity, accepted", [
    ("CPython 3.15.0", True),
    ("CPython 3.15.7", True),
    ("CPython 3.14.4", False),
    ("PyPy 3.15.7", False),
])
def test_make_test_runtime_patch_contract(tmp_path, identity, accepted):
    root, hostile = _synthetic_checkout(tmp_path, Path(sys.executable))
    runtime = root / ".venv" / "bin" / "python"
    runtime.unlink()  # Never write through a host-interpreter symlink.
    _write_executable(runtime, f'''#!/bin/sh
        if [ "$1" = "-c" ]; then
          printf '%s\\n' '{identity}'
          exit 0
        fi
        printf 'PYTEST_SENTINEL\\n'
        exit 0
    ''')
    result = _run(root, hostile, tmp_path)
    output = result.stdout + result.stderr
    assert (result.returncode == 0) is accepted
    assert ("PYTEST_SENTINEL" in output) is accepted
    assert "HOSTILE_PYTHON_SELECTED" not in output
    if not accepted:
        assert f"expected CPython 3.15.x, got {identity}" in result.stderr
```

| Characterization | RED before repair | GREEN after repair |
| --- | --- | --- |
| CPython 3.15.7 | Acceptance assertion fails; child absent | Exit 0 and child marker present |
| CPython 3.15.0 | Existing behavior passes | Continues to pass |
| CPython 3.14.4 / PyPy 3.15.7 | Rejected, but new diagnostic assertion fails | Rejected with 3.15.x diagnostic and no child |
| Missing runtime | Existing refusal; updated diagnostic assertion fails | Actionable 3.15.x refusal without fallback |
| Real child via intermediate symlink | Raw-path comparison may fail depending on host layout | Both executable paths normalize identically; CPython 3.15 asserted |

- Keep the matrix wrapper limited to gate characterization; retain the real interpreter/pytest-child test as independent execution-provenance coverage.
