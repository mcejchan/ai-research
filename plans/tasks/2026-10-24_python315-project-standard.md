# ai-research: Python 3.15 — canonical Make test and YouTube pipeline children

## Outcome
The Python portion of canonical `make test` must run on the project's explicit exact CPython 3.15.0, not whichever `python3` appears first on PATH. Keep `.python-version=3.15.0`. Preserve the Node quiz/viewer/publication checks and the existing offline pytest environment; do not turn the Node app into a Python package or create another interpreter manager.

## Concrete scope and changes
- `Makefile`, `test` recipe: the command currently changes into `youtube-transcript-pipeline` and runs bare `python3 -m pytest`. Select and validate the root project runtime before executing Python tests, fail clearly for missing/mismatched interpreter, preserve cwd, test discovery, environment values and failure propagation. Keep `quiz-publication-check`, both existing Node test invocations and quiz build-index behavior intact.
- `youtube-transcript-pipeline/test/test_config.py`: preserve the deliberate `sys.executable` child; test observed identity, not merely argv. Inspect real pipeline CLI/child callsites only to classify same-runtime vs external tools and remove demonstrated ambient Python selections. Do not change model/download/Drive behavior as part of version work.
- Dependency sources are `youtube-transcript-pipeline/requirements.txt` and `requirements-dev.txt`. Verify them on real 3.15, change only concrete incompatibilities and record why. No unbounded upgrades, global pip or artificial root package.
- Add a focused launcher regression in the existing Python test tree, e.g. `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py`. First check the domain-qualified basename is unique. Reuse Make/existing bootstrap conventions, no generic utils/helpers/state/common modules.
- Handoff must enumerate each Make/CLI Python execution surface, owning runtime, selected path, changed/unchanged disposition and corresponding test selector. Historical snippets/vendor files are not runtime targets.

## Acceptance and verification
- Genuine task-scoped RED/GREEN must exercise the real Make test recipe in a synthetic checkout fixture: run with hostile ambient python3 and unrelated cwd (`make -C`), observe real CPython 3.15.0 executable/implementation/full version and sentinel pytest-child result. Stub Node/quiz/external actions in this focused fixture only, not the actual full gate. Argument and exit propagation remain intact.
- Missing/stale project interpreter fixtures fail actionably, with no fallback. Preserve intentionally foreign interpreter tests; do not rewrite all subprocesses to root Python regardless of ownership.
- Run focused runtime regression and `test/test_config.py` under real selected3.15; record module origins. Mock all LLM, Drive, network/download/embedding effects. Existing fake/offline environment values are not real credentials.
- Unchanged registered project gate is `make test` from root: retain Node tests, publication check and the entire pipeline pytest suite. Record actual interpreter for its Python branch, collection/results and Node outcomes. No narrower replacement or green claim from a mocked launcher test alone.
- A project pin or pytest pass under older Python is not compatibility. If required3.15 dependencies/project environment are unavailable, report exact host prerequisite and partial source results without claiming registered success or weakening metadata/tests.

## Host boundary and evidence
Host provisions a dependency-complete real3.15 candidate before registered compatibility verification and owns canonical `.venv` creation/cutover. Worker may use an already provisioned disposable3.15 environment for local tests, never replace the active venv or bootstrap global tools.
Write `plans/checkpoints/python315-host-handoff.md` with source identity, entrypoint matrix, focused/full commands and actual identities/results, exact requirements install recipe and dependency provenance, remaining host setup. Separate source implementation, source compatibility and runtime activation. Wider library support is not automatically removed by the development pin.
No transcripts/private content, credentials, live provider/model/network/replay, recording download, cloud data access, services/restart/deploy/schedulers, instruction/registry/lifecycle or sibling edits. Preserve all normal planning/review/acceptance/TestGate requirements and existing Node/quiz behavior.
