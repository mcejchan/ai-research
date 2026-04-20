# Plan 2026-04-20: Route YT pipeline LLM calls through copilot-bridge

Route `src/llm_client.py` OpenAI client construction through the local OpenAI-compatible proxy while keeping model selection unchanged and limiting code edits to the requested module.

*Status: DRAFT*
*Vytvoreno: 2026-04-20*

---

## Progress

- [x] Faze 0: Config + Init
- [x] Faze 1: Research
- [x] Faze 2: Knowledge
- [x] Faze 3: Synthesis

## Problem

`src/llm_client.py` currently requires a standalone `OPENAI_API_KEY`, but this workspace routes all LLM traffic through `copilot-bridge` on port `18800`. The plan must update client initialization in `analyze_text()` and `embed_text()` to use `OPENAI_BASE_URL` and a dummy default API key, then verify existing tests and a manual pipeline smoke test. Scope is limited to `src/llm_client.py`.

## Analysis

### Kontext z codebase
- `youtube-transcript-pipeline/src/llm_client.py:105-132` instantiates `OpenAI` separately inside `analyze_text()` and `embed_text()` with `api_key=os.getenv("OPENAI_API_KEY")`; those are the only production call sites that need rerouting.
- `youtube-transcript-pipeline/test/test_llm_client.py:41-60` patches `src.llm_client.OpenAI` and asserts the old constructor signature exactly via `assert_called_once_with(api_key=os.getenv("OPENAI_API_KEY"))`.
- `youtube-transcript-pipeline/test/mocks/mock_llm.py:23-35` only accepts `api_key` in `MockOpenAI.__init__`, but the patched class in tests is the mock object from `unittest.mock`, so constructor signature pressure comes from test assertions, not from this helper.
- `youtube-transcript-pipeline/README.md:79-119,142-168` documents `src/llm_client.py`, `OPENAI_API_KEY` setup, and `pytest` as the standard verification path for this package.

### Relevantni dokumentace
- No PlantUML or dedicated architecture docs exist in the workspace for this pipeline.
- `CLAUDE.md` establishes repository-wide verification guidance: run `pytest` before commit and keep secrets out of the repo.
- `youtube-transcript-pipeline/README.md` is the only local doc relevant to this change; it still describes direct OpenAI key usage and may become stale, but the task scope explicitly forbids editing other files.

### Knowledge base
- No project `learnings/` directory or `critical-patterns.md` file exists in this workspace, so there are no local planning constraints to import beyond repo instructions.

## Available Skills

- `compound-plan`: create and maintain this plan file.
- `recall-knowledge`: use only if project learnings appear later; currently no local learnings were found.
- `run-and-debug-app-tests`: useful during implementation if `pytest` or the smoke run fails.
- `validate-implementation`: useful after implementation to confirm the change stayed within `src/llm_client.py` and preserved model names.
- `save-learning`: mandatory last step after implementation per task instructions.
- `tdd`: only applicable if scope is loosened enough to allow a focused test update.

## Solutions

- Update both `OpenAI(...)` call sites in `src/llm_client.py` to pass `base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:18800/v1")` and `api_key=os.getenv("OPENAI_API_KEY", "copilot-bridge")` directly where the client is created.
- Keep all prompt logic, model names, and embedding behavior unchanged so the change is transport-only.
- Treat the current constructor assertion in `test/test_llm_client.py` as a scope mismatch to resolve before implementation: either confirm the user still wants zero non-`src/llm_client.py` edits and accept that the current suite may fail, or confirm the user branch already contains a compatible assertion.

## Implementation

### Pre-implementation checklist
- [ ] Confirm whether the existing `test/test_llm_client.py::test_analyze_text_openai_success` assertion has already been updated outside this session; if not, flag that the written task constraints conflict with the requested constructor change.
- [ ] Work only in `youtube-transcript-pipeline/src/llm_client.py` unless the user explicitly relaxes the scope.
- [ ] Preserve `gpt-4o-mini` and `text-embedding-3-large` exactly.

### Kroky implementace
1. Edit `youtube-transcript-pipeline/src/llm_client.py` and replace the `OpenAI(api_key=os.getenv("OPENAI_API_KEY"))` constructor in `analyze_text()` with the requested `base_url` and default `api_key` arguments.
2. Apply the same constructor change in `embed_text()` and leave the embedding model lookup untouched.
3. Run `pytest` from `youtube-transcript-pipeline/` and inspect whether the pre-existing constructor assertion still matches the new signature.
4. If tests pass, run `python -m src.yt_pipeline --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"` from `youtube-transcript-pipeline/` to verify the proxy-backed runtime path.
5. If the smoke test fails because `copilot-bridge` is unavailable, report that as an environment issue rather than broadening code changes.
6. After implementation and verification, invoke `save-learning` as the final action and record the proxy-routing decision and any test-scope mismatch discovered.

## Files to Modify

| Soubor | Zmena |
|--------|-------|
| `youtube-transcript-pipeline/src/llm_client.py` | Replace both direct OpenAI client initializations with the proxy-aware constructor using `OPENAI_BASE_URL` and dummy default API key. |

## TDD: skip

This task is behavior-testable, but the stated implementation scope forbids editing any file other than `src/llm_client.py`, while the existing test suite currently asserts the old constructor signature and would require a test edit to create or maintain a RED-first targeted test.

## Dependencies

- `youtube-transcript-pipeline` test environment must remain installable enough to run `pytest`.
- `copilot-bridge` must be running at `http://127.0.0.1:18800/v1` for the manual smoke test, or `OPENAI_BASE_URL` must point to an equivalent OpenAI-compatible endpoint.
- Any runtime auth used by `copilot-bridge` is expected to come from existing local GitHub Copilot credentials, not from a checked-in secret.
