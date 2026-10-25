# Plan 2026-10-25: Repair Python 3.15 runtime contract fixtures

Correct unsafe runtime fixture setup and capture fresh CPython 3.15.0 GREEN evidence for the existing four-test regression, reusing the parent task's authentic RED.

## Analysis

- `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py` creates `.venv/bin/python` as a symlink, then `_write_executable` follows that symlink in the propagation and stale-runtime tests. Unlink before each replacement script write.
- Preserve current test coverage for exact pytest arguments/status and stale-runtime rejection, and leave the Make runtime implementation unchanged.
- Historical genuine RED is `plans/checkpoints/task-a45bce59-6f99-4d3f-98fd-35bb161d44c8.red-green-proof.md`; link it in fresh follow-up proof rather than generating a new RED.
- Relevant learning: acceptance-fix proof artifacts must contain exact fresh GREEN evidence; retain separation between implementation regressions and proof requirements.

## Approach

- Apply the smallest fixture correction: unlink the symlink before writing each synthetic executable.
- Run the repaired four-test module with the actual CPython 3.15.0 interpreter, record exact command and result in this task's proof artifact, and reference historical RED.
- Run the root registered gate `make test` and record its outcome.

## Implementation

1. In both script-replacement cases, unlink `.venv/bin/python` before `_write_executable`; keep the missing-runtime case and all existing assertions intact.
2. Confirm the synthetic replacement is a regular executable fixture and does not alter the resolved host interpreter.
3. Capture focused GREEN under CPython 3.15.0 for all four tests in `plans/checkpoints/task-9576667c-4cac-4e0c-92dc-0ef1a8644178.red-green-proof.md`; include a direct link to the historical RED artifact.
4. Run `make test` from the workspace root and record the result.

## Testing

- Focused: from `youtube-transcript-pipeline`, run `python3.15 -m pytest -q test/test_research_python_runtime_contract.py` using the real CPython 3.15.0 executable. Confirm four tests pass, exact `-m pytest` arguments and exit status propagate, stale runtime is rejected, and host interpreter target remains intact.
- Full registered gate: `make test` from the workspace root.
- Proof must identify interpreter version/executable and link the original genuine RED; do not fabricate a new RED.

## TDD

This acceptance fix repairs an existing regression test after implementation already exists. Reuse the historical genuine RED and capture a fresh GREEN only after repairing fixtures, following `skill:tdd` evidence requirements.

**Test file:** `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py`  
**Framework:** pytest.  
**Run command:** `python3.15 -m pytest -q test/test_research_python_runtime_contract.py` from `youtube-transcript-pipeline`, with CPython 3.15.0.  
**Edit hint:** Update the two `_write_executable` call sites that replace the symlink runtime.

```python
def test_make_test_propagates_pytest_arguments_and_failure_status(tmp_path):
    root, hostile = _synthetic_checkout(tmp_path, Path(sys.executable))
    runtime = root / ".venv" / "bin" / "python"
    runtime.unlink()  # Ensure replacement script does not overwrite real_python.
    _write_executable(runtime, """#!/bin/sh
        if [ "$1" = "-c" ]; then
          exec "REAL_PYTHON" -c "$2"
        fi
        printf 'PYTEST_ARGS:' >&2
        printf ' <%s>' "$@" >&2
        printf '\\n' >&2
        exit 23
    """)
    result = _run(root, hostile, tmp_path)
    assert result.returncode == 23
    assert "PYTEST_ARGS: <-m> <pytest>" in result.stderr
```

| Test | Historical RED / expected failure | GREEN |
|---|---|---|
| Pytest args/status propagation | Link authentic parent RED; no synthetic new RED | Four-test CPython 3.15.0 run passes; exact args and status observed |
| Stale runtime rejection | Link authentic parent RED | Mismatched runtime rejected; no fallback or pytest sentinel |
| Safe fixture replacement | Historical source is unsafe because write follows symlink | Host interpreter remains unmodified; replacement is a regular executable |

## Files

| File | Change |
|---|---|
| `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py` | Unlink runtime symlink before each script replacement. |
| `plans/checkpoints/task-9576667c-4cac-4e0c-92dc-0ef1a8644178.red-green-proof.md` | Record fresh CPython 3.15.0 GREEN and link the parent's genuine RED. |

## Progress

- [x] Read original plan and inspect current regression fixtures and Makefile.
- [x] Identify symlink-following defect and proof requirements.
- [ ] Unlink symlink in both replacement fixtures.
- [ ] Capture fresh focused GREEN and run root `make test`.
