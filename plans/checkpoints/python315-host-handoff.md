# Python 3.15 host handoff

## Source implementation

- Source pin: repository `.python-version` is exactly `3.15.0`.
- Root `Makefile` now selects only `<checkout>/.venv/bin/python`, validates `platform.python_implementation()` and `platform.python_version()` as `CPython 3.15.0`, then executes pytest. Missing, non-executable, or mismatched runtime fails before pytest; no ambient `python3` fallback.
- Pipeline subprocess audit: the only `subprocess.run` callsites are the two `yt-dlp` invocations in `src/yt_pipeline.py` (`whisper_transcribe`, `get_basic_meta`), external CLI tools, unchanged. `test/test_config.py` intentionally uses `sys.executable` for its same-runtime import child and now asserts observed executable, implementation, and full version. No other Python child selection found.
- Surface matrix:

| Surface | Owner/selected path | Disposition | Test selector |
|---|---|---|---|
| Canonical Make pytest branch | Root-owned `.venv/bin/python`, exact CPython 3.15.0 | Implemented, host activation pending | `make test` |
| `test_config.py` import subprocess | Current test interpreter via `sys.executable` | Preserved same-runtime child; identity asserted | `test/test_config.py::test_pipeline_import_does_not_require_drive_folder_id` |
| `yt-dlp` calls in whisper/meta | External `yt-dlp` executable via PATH | Unchanged external-tool ownership | `test/test_research_python_runtime_contract.py` protects Make selection; pipeline tests cover behavior |
| Focused synthetic Make regression | Fixture `.venv/bin/python` fake CPython; Node/external actions stubbed only in fixture | Exercises real copied Make recipe, hostile PATH, missing runtime, and pytest failure propagation | `test/test_research_python_runtime_contract.py` |

## Source compatibility

- Requirements sources remain unchanged: `requirements.txt`, `requirements-dev.txt`. No concrete incompatibility was established.
- Candidate interpreter: `/opt/homebrew/opt/python@3.15/bin/python3.15`, observed `CPython 3.15.0`; `python3.15 -m pytest --version` reports `No module named pytest`.
- Exact declared-requirements dry-run attempted: `python3.15 -m pip install --dry-run -r requirements.txt -r requirements-dev.txt`; blocked by Homebrew PEP 668 externally-managed-environment policy before dependency resolution. Do not add `--break-system-packages` or install globally.
- On a host-provisioned disposable 3.15 environment, run `python -m pip install -r requirements.txt -r requirements-dev.txt`, then `python -m pytest -q test/test_research_python_runtime_contract.py test/test_config.py`. Record `python -c 'import sys,platform; print(sys.executable,platform.python_implementation(),platform.python_version())'` and module origins for pytest, pandas, dotenv, tqdm, youtube_transcript_api, openai, googleapiclient, and coverage. Existing tests use fake credentials; no live integrations are needed.
- Current source test environment was CPython 3.9.6. Focused launcher regression: 3 passed; config suite was not run in this old runtime as a substitute for 3.15.

## Runtime activation and verification

- Canonical root `.venv` is absent; creating/cutting it over is host-owned and intentionally not performed.
- Focused TDD proof: `plans/checkpoints/task-a45bce59-6f99-4d3f-98fd-35bb161d44c8.red-green-proof.md` records accepted RED and GREEN for `python3 -m pytest -q test/test_research_python_runtime_contract.py`. Synthetic checkout validates actual recipe behavior, not dependency compatibility.
- Canonical unchanged gate attempted exactly: `make test` from repository root. Publication check passed (6/6); quiz index generated with 20 levels; viewer tests passed (2/2); knowledge contract tests passed (4/4). Python branch stopped with actionable missing `/Users/michal/Projects/ai-research/.venv/bin/python` error; no pytest collection/results or registered-gate success claim.
- Host prerequisite: provision dependency-complete project `.venv` using exact CPython 3.15.0, install both requirements files with the recipe above, then rerun focused tests and unmodified root `make test`. Record full interpreter identity, module origins, Python collection/results, and all Node outcomes. Do not weaken the version guard or alter Node/quiz behavior.
