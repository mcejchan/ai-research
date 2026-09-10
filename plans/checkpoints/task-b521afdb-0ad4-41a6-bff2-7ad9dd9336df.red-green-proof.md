# RED-GREEN Proof: fix ignored pytest.ini section (ai-research)

Task: task-b521afdb-0ad4-41a6-bff2-7ad9dd9336df
Target: youtube-transcript-pipeline/pytest.ini  `[tool:pytest]` -> `[pytest]`
Test file: youtube-transcript-pipeline/test/test_config.py (append 2 characterization tests)

This file is created BEFORE any production change. The RED Phase records the
failing characterization tests as written against the still-broken `[tool:pytest]`
pytest.ini. The GREEN Phase is appended after the section fix and a passing run.

## RED Phase

**Goal before fix:** prove `pytest.ini`'s `[tool:pytest]` section is silently
ignored (testpaths/addopts/env all come back empty), so the declared coverage
and env config never take effect.

**Note on API vs plan:** the plan's skeleton used `pytest.Config.from_path`,
which does NOT exist in pytest 8.4.2 (`AttributeError: type object 'Config' has
no attribute 'from_path'`). The task description itself names `fromdictargs`,
which is the correct public API. The two appended tests use
`pytest.Config.fromdictargs({}, ["-c", <path to pytest.ini>])` to genuinely
load the ini file through pytest's own config machinery.

**Test file edited:** `youtube-transcript-pipeline/test/test_config.py`
(2 tests appended: `test_pytest_ini_section_is_read_by_pytest`,
`test_pytest_ini_env_block_present`). `pytest.ini` NOT touched yet.

**Command (run from youtube-transcript-pipeline/):**
```
python3 -m pytest test/test_config.py -v
```

**Result (RED) — 2 failed, 2 passed, 4 warnings in 1.29s:**
```
test/test_config.py::test_pipeline_import_does_not_require_drive_folder_id PASSED [ 25%]
test/test_config.py::test_real_drive_requires_folder_id_at_execution PASSED [ 50%]
test/test_config.py::test_pytest_ini_section_is_read_by_pytest FAILED     [ 75%]
test/test_config.py::test_pytest_ini_env_block_present FAILED     [100%]

    def test_pytest_ini_section_is_read_by_pytest():
        cfg = _load_pipeline_pytest_config()
        addopts = cfg.getini("addopts")
>       assert "--cov=src" in addopts
E       AssertionError: assert '--cov=src' in []

    def test_pytest_ini_env_block_present():
        cfg = _load_pipeline_pytest_config()
        env = cfg.getini("env")
>       assert "USE_WHISPER_FALLBACK = false" in env
E       AssertionError: assert 'USE_WHISPER_FALLBACK = false' in []

=========================== short test summary info ============================
FAILED test/test_config.py::test_pytest_ini_section_is_read_by_pytest - Asser...
FAILED test/test_config.py::test_pytest_ini_env_block_present - AssertionErro...
=================== 2 failed, 2 passed, 4 warnings in 1.29s ====================
```

**Independent cross-check (`python3 -c ...` with fromdictargs, before fix):**
```
rootpath: /Users/michal/Projects/ai-research/youtube-transcript-pipeline
inipath:  /Users/michal/Projects/ai-research/youtube-transcript-pipeline/pytest.ini
addopts:  []
testpaths:[]
env:      []
```
The file is located (inipath points at pytest.ini) but every value is empty —
proving `[tool:pytest]` is the wrong section for a `pytest.ini` file and pytest
ignores the whole file. This is a silent defect (suite still runs via default
discovery), not a no-op.

## GREEN Phase

**Fix applied:** `youtube-transcript-pipeline/pytest.ini` line 1 only:
`[tool:pytest]` -> `[pytest]`. No other line changed (verified by re-reading the
file: lines 2-13 identical to before).

**Command (run from youtube-transcript-pipeline/):**
```
python3 -m pytest test/test_config.py -v
```

**Result (GREEN) — 4 passed, 4 warnings in 1.72s:**
```
test/test_config.py::test_pipeline_import_does_not_require_drive_folder_id PASSED [ 25%]
test/test_config.py::test_real_drive_requires_folder_id_at_execution PASSED [ 50%]
test/test_config.py::test_pytest_ini_section_is_read_by_pytest PASSED      [ 75%]
test/test_config.py::test_pytest_ini_env_block_present PASSED      [100%]
======================== 4 passed, 4 warnings in 1.72s =========================
```

**Independent cross-check (`python3 -c ...` with fromdictargs, after fix):**
```
addopts:   ['--cov=src', '--cov-report=term-missing', '--cov-report=html', '-v']
testpaths: ['test']
env:       ['PYTHONPATH = src', 'OPENAI_API_KEY = test_openai_key', 'LANG = cs',
            'USE_WHISPER_FALLBACK = false', 'MAKE_EMBEDDINGS = false',
            'DRIVE_FOLDER_ID = test_folder_id']
python_files: ['test_*.py']
```
All three previously-empty values (addopts, testpaths, env) are now non-empty,
proving the `[pytest]` section is genuinely read by pytest. `python_files` matches
the pytest default, so test count is unaffected.

## Regression (full suite + root mixed gate)

**Full pipeline suite** (`cd youtube-transcript-pipeline && python3 -m pytest -q`):
```
44 passed, 4 warnings in 21.53s
================================ tests coverage ================================
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/__init__.py           0      0   100%
src/drive_client.py      93     32    66%
src/llm_client.py        16      0   100%
src/yt_pipeline.py      169     52    69%
---------------------------------------------------
TOTAL                   278     84    70%
Coverage HTML written to dir htmlcov
```
44 = 42 baseline + 2 new characterization tests. Count rose by exactly the 2
tests I appended (no pre-existing test was dropped/added); the declared globs
(`python_files`/`python_classes`/`python_functions`) equal pytest defaults, so
`testpaths=test` did not change discovery. Coverage table + HTML now emitted
because `addopts=--cov=src ...` is finally honored.

**Root mixed Node/Python gate** (`cd ~/Projects/ai-research && make test`, exit 0):
- quiz-publication-check: node --test (6 pass, 0 fail) + `node quiz/build-index.js`
  (wrote quiz/levels/index.json, 20 levels).
- yt-viewer/server.test.js: 2 pass, 0 fail.
- test/knowledge-command-contracts.test.js: 4 pass, 0 fail.
- python3 -m pytest (with explicit env matching the now-active `env` block):
  **44 passed, 4 warnings**, coverage table emitted.
- `make test` exit code: 0.
Enabling the previously-ignored `env` block did NOT change runtime behavior for
`make test` because that target already supplies the same 5 env values on the
command line; this is expected and confirmed (no regression).

**No new tracked artifacts** (`git status --porcelain` after run):
```
M youtube-transcript-pipeline/pytest.ini
 M youtube-transcript-pipeline/test/test_config.py
?? learnings/tooling/2026-09-10_pytest-section-tool-pytest-ignored.md   (pre-existing, untouched)
?? plans/checkpoints/task-b521afdb-...checkpoint.md                      (this task)
?? plans/checkpoints/task-b521afdb-...red-green-proof.md               (this task)
```
`git status --porcelain --ignored` confirms `youtube-transcript-pipeline/htmlcov/`,
`.coverage`, `.pytest_cache/` are all ignored (`!!`), not tracked — so enabling
coverage created no new tracked artifacts. The only tracked changes are the 2
intended files. `learnings/tooling/...` is a pre-existing untracked artifact that
was already present (not created by this task) and is left untouched.
