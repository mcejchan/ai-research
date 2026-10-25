# Plan 2026-10-25: AI Research Python 3.15 Make test and pipeline child provenance

Pin the Python branch of the root test gate to the validated project CPython 3.15.0 while preserving Node checks, offline pytest settings, and child-process ownership.

## Analysis

- `.python-version` already pins `3.15.0`; root `Makefile` currently invokes bare `python3` after changing into `youtube-transcript-pipeline`.
- `test_config.py` deliberately invokes `[sys.executable, ...]`; change its assertion to establish observed executable, implementation, and full version in the child, retaining same-runtime ownership.
- `src/yt_pipeline.py` uses subprocess only for `yt-dlp` commands, external tools rather than Python children; preserve those calls and their behavior. Audit all other pipeline CLI/child surfaces before disposition.
- Dependency sources are `requirements.txt` and `requirements-dev.txt`; validate/install against real 3.15 before editing. Do not broaden or remove runtime support based only on the development pin.
- `test_research_python_runtime_contract.py` basename is currently unique. No project PlantUML diagrams found. Relevant learning: canonical root gate evidence is separate from focused test evidence; retain authentic RED and rerun GREEN.

## Approach

- Resolve the project-root runtime explicitly from the Makefile location, validate existence and exact CPython implementation/version, and fail with actionable diagnostics without falling back to ambient `python3`.
- Preserve Make recipe cwd, test discovery, offline environment values, Node commands, quiz publication/build-index behavior, and failure propagation.
- Keep Python children bound to their owning runtime; document external `yt-dlp` as external and preserve foreign-interpreter cases.
- Separate source implementation, 3.15 source compatibility, and host-owned `.venv` activation evidence in the handoff.

## Implementation

1. Add the focused runtime contract test and synthetic checkout fixture that exercises the actual `make test` recipe using hostile ambient `python3` and unrelated `make -C` cwd; stub Node/quiz/external actions only inside that fixture.
2. Capture genuine RED, then update Make runtime selection/validation and `test_config.py` child identity assertions; retain real interpreter and sentinel pytest-child evidence.
3. Test missing/stale interpreter failures, argv and exit propagation, cwd/environment retention, and untouched foreign-interpreter ownership.
4. Audit Makefile and pipeline CLI/subprocess callsites; record every execution surface, owner, selected path, disposition, and test selector in `plans/checkpoints/python315-host-handoff.md`.
5. On a provisioned disposable real 3.15 environment, run requirements install/compatibility checks, focused tests and `test/test_config.py`; record module origins and mock LLM, Drive, network/download/embedding effects. Change dependency metadata only for demonstrated incompatibilities with rationale.
6. Run the registered root gate exactly as `make test`; record actual Python identity, collection/results, publication check, both Node tests and quiz index outcome. If host prerequisites are unavailable, report exact prerequisite and partial source results without claiming gate success.
7. Leave canonical `.venv` creation/cutover to host; never replace the active environment or bootstrap global tools.

## Testing

- RED/GREEN launcher regression: `cd youtube-transcript-pipeline && <selected-3.15-python> -m pytest -q test/test_research_python_runtime_contract.py` (fixture itself invokes real Make test recipe).
- Selected-runtime focused tests: `<selected-3.15-python> -m pytest -q test/test_research_python_runtime_contract.py test/test_config.py` from pipeline root; record executable, implementation, full version and imported module origins.
- Compatibility: install exact declared requirements into disposable host-provisioned 3.15 environment, then run focused tests; record exact recipe and provenance in handoff.
- Canonical verification: `make test` from repository root, retaining all Node, quiz/publication and full pipeline pytest branches; no mocked launcher test substitutes for this gate.
- Negative fixtures: absent and stale/mismatched runtime must fail actionably with no fallback; verify child argument and status propagation.

## TDD

**Test file:** `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py`  
**Framework:** pytest; existing Python test suite.  
**Run command:** `<selected-3.15-python> -m pytest -q test/test_research_python_runtime_contract.py` from `youtube-transcript-pipeline`.  
**Edit hint:** NEW FILE; first assert the current Make recipe selects the wrong interpreter under hostile PATH.

```python
from pathlib import Path
import subprocess


def test_make_test_uses_project_cpython_and_propagates_pytest_sentinel(tmp_path):
    # Build an isolated synthetic checkout and hostile python3/Node stubs.
    # RED: invoking the real root Makefile must not execute hostile python3.
    result = subprocess.run(
        ["make", "-C", str(tmp_path), "test"],
        cwd=tmp_path.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    assert "CPython 3.15.0" in result.stdout
    assert "PYTEST_SENTINEL" in result.stdout
    assert result.returncode == 0
```

| Test | RED | GREEN |
|---|---|---|
| hostile PATH real-Make fixture | ambient interpreter is selected or identity/sentinel is absent | project CPython identity and pytest sentinel observed |
| absent/stale interpreter fixture | — | actionable failure, no ambient fallback |
| child argument/status fixture | — | arguments and pytest exit status propagate |

Implement the genuine RED/GREEN cycle using `skill:tdd`; retain its evidence and do not substitute mocked-launcher evidence for `make test`.

## Files

| File | Planned change |
|---|---|
| `Makefile` | Select and validate project CPython before pytest; preserve gate structure/settings. |
| `youtube-transcript-pipeline/test/test_config.py` | Assert observed deliberate child runtime identity. |
| `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py` | Add real-Make synthetic checkout regression and failure/propagation cases. |
| `youtube-transcript-pipeline/requirements.txt` | Only evidence-backed 3.15 compatibility changes, if required. |
| `youtube-transcript-pipeline/requirements-dev.txt` | Only evidence-backed 3.15 compatibility changes, if required. |
| `plans/checkpoints/python315-host-handoff.md` | Record execution surface matrix, identities, exact commands/results, dependency provenance, and remaining host setup. |

## Progress

- [x] Resolve canonical plan path and inspect core Make/Python/dependency context.
- [x] Identify current child ownership and verify proposed test basename is unique.
- [ ] Implement genuine RED/GREEN and runtime selection.
- [ ] Verify with provisioned real CPython 3.15 and canonical `make test`; write host handoff evidence.
