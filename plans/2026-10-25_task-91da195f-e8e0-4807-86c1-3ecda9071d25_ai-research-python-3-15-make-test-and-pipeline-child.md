# Plan 2026-10-25: Repair Python 3.15 Make test provenance regression

Correct the focused launcher regression so it proves real interpreter selection, pytest-child invocation/status propagation, and actionable rejection of stale runtimes. Preserve the already-implemented Make runtime guard.

## Analysis

- `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py` currently uses a shell script that fabricates identity and does not exercise pytest in the failure-propagation case.
- The project Makefile validates `.venv/bin/python`; regression cases must exercise its actual recipe with hostile ambient `python3` still first on `PATH`.
- The previous task's historical RED is at `plans/checkpoints/task-a45bce59-6f99-4d3f-98fd-35bb161d44c8.red-green-proof.md`; reuse/link that authentic evidence rather than manufacturing a new RED.
- `learnings/tooling/make-test-python-runtime-pin.md`: keep pytest under the project interpreter; record observed executable, implementation, and full version; distinguish owned Python children from external tools.
- Recall search found no critical patterns; no task-specific architecture/docs changes are needed.

## Approach

- Keep scope to repairing the existing test fixtures and capturing fresh GREEN evidence; do not redo the existing runtime-selection implementation.
- For the nominal synthetic checkout, use a real CPython 3.15.0 executable (symlink the active selected executable) and a minimal pytest child that prints a unique sentinel. Assert observed `sys.executable`, `platform.python_implementation()`, full `sys.version`, sentinel, and that hostile ambient Python was not used.
- For exit propagation, make the runtime answer the Make identity `-c` probe correctly, then record the exact subsequent `-m pytest` argv and exit with a nonzero status only for that child. Assert arguments and Make's propagated status.
- Add a distinct executable stale/mismatched-runtime case; assert diagnostic expected and observed identities, and no ambient Python or pytest invocation.

## Implementation

1. Confirm a real CPython 3.15.0 executable is available to the focused test run; use it directly for the synthetic checkout runtime rather than an identity-printing shell stub.
2. Repair the nominal and child-failure fixtures so identity inspection succeeds and the actual pytest branch is observed.
3. Add the stale/mismatched identity fixture and assert actionable rejection without fallback or child execution.
4. Run the focused regression under CPython 3.15.0 and capture fresh GREEN proof; link the parent task's historical RED proof.
5. Run the registered `make test` if host prerequisites permit; report the existing host-owned `.venv` limitation accurately if unavailable.

## Testing

- Focused: from `youtube-transcript-pipeline`, `python3.15 -m pytest -q test/test_research_python_runtime_contract.py` (use the exact selected CPython 3.15.0 executable path if `python3.15` is unavailable).
- Assert selected runtime's executable path, `CPython`, full version `3.15.0`, pytest sentinel, exact pytest argv/status, mismatch diagnostics, and absence of hostile fallback.
- Full registered gate: `make test` from workspace root, subject to host-owned `.venv` provisioning.
- Save fresh GREEN command/output under `plans/checkpoints/task-91da195f-e8e0-4807-86c1-3ecda9071d25.red-green-proof.md`; reference the historical RED proof above.

## TDD

**Test file:** `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py`  
**Framework:** pytest.  
**Run command:** `python3.15 -m pytest -q test/test_research_python_runtime_contract.py` from `youtube-transcript-pipeline`, using the real CPython 3.15.0 executable.  
**Edit hint:** Repair existing tests and add mismatch test; do not create a synthetic RED after the implementation exists.

```python
from pathlib import Path
import subprocess
import sys


def test_make_test_reports_real_python_315_and_runs_pytest_child(tmp_path):
    # RED history: plans/checkpoints/task-a45bce59-6f99-4d3f-98fd-35bb161d44c8.red-green-proof.md
    root, hostile = _synthetic_checkout(tmp_path, real_python=Path(sys.executable))
    result = _run_make_test(root, hostile)
    assert str(Path(sys.executable).resolve()) in result.stdout
    assert "CPython" in result.stdout and "3.15.0" in result.stdout
    assert "PYTEST_SENTINEL" in result.stdout
    assert "HOSTILE_PYTHON_SELECTED" not in result.stdout
    assert result.returncode == 0
```

| Test | Historical RED / expected failure | GREEN |
|---|---|---|
| Real interpreter and pytest sentinel | Historical RED demonstrates ambient Python was selected; retain its provenance | Observed actual executable, CPython 3.15.0, and pytest sentinel |
| Pytest argv/status propagation | Existing faulty case never passes identity inspection | Identity probe succeeds; exact `-m pytest` args are observed and child exit status propagates |
| Stale/mismatched project runtime | Not previously covered | Expected/observed identity diagnostic; no ambient fallback and no pytest child |

Follow `skill:tdd` evidence rules: reuse the authentic parent RED and capture new GREEN only after correcting the final source.

## Files

| File | Planned change |
|---|---|
| `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py` | Replace hard-coded runtime identity with real CPython fixture; repair child-propagation path; cover mismatched runtime and no-fallback diagnostics. |
| `plans/checkpoints/task-91da195f-e8e0-4807-86c1-3ecda9071d25.red-green-proof.md` | Record fresh focused GREEN and link historical genuine RED. |

## Progress

- [x] Inspect the original plan, current Make recipe, regression source, and historical proof.
- [x] Identify the unmet acceptance cases and relevant runtime provenance learning.
- [ ] Repair focused fixtures and add mismatch coverage.
- [ ] Capture fresh GREEN and run available verification.
