# Plan 2026-04-20: Make LLM model configurable via env var, default to gpt-4o

Switch the chat-completions model selection from a hardcoded value to `LLM_MODEL`, while keeping the existing OpenAI client wiring intact and leaving embeddings alone.

*Status: DRAFT*
*Vytvoreno: 2026-04-20*

---

## Progress

- [x] Faze 0: Config + Init
- [x] Faze 1: Research
- [x] Faze 2: Knowledge
- [x] Faze 3: Synthesis

## Problem

The pipeline hardcodes `gpt-4o-mini` in `src/llm_client.py`, so operators cannot switch chat models through environment configuration. The requested change is limited to the chat model default and must not alter embeddings, base URL, API key behavior, or dependencies.

## Analysis

### Kontext z codebase
- `youtube-transcript-pipeline/src/llm_client.py:105-127` builds the chat request inside `analyze_text()` and hardcodes `model="gpt-4o-mini"` in `client.chat.completions.create(...)`.
- `youtube-transcript-pipeline/src/llm_client.py:130-137` already makes embeddings configurable through `OPENAI_EMBEDDING_MODEL`; the requested change should mirror that pattern only for chat completions.
- `youtube-transcript-pipeline/test/test_llm_client.py:41-62` already patches `src.llm_client.OpenAI` and inspects constructor kwargs via `mock_openai_class.call_args.kwargs`; the same style can verify the completion `model` kwarg without tightening unrelated behavior.
- `youtube-transcript-pipeline/test/mocks/mock_llm.py:37-53` accepts arbitrary `create(**kwargs)`, so a focused test on the `model` kwarg can run without changing the mock helpers.

### Relevantni dokumentace
- `youtube-transcript-pipeline/README.md:79-93` documents `src/llm_client.py` and still describes the analysis model as `GPT-4o-mini`; after implementation, this doc should be checked for drift even if the task scope stays code-only.
- `youtube-transcript-pipeline/README.md:142-158` names `pytest` as the standard verification path for this package.
- No PlantUML or other architecture docs were found in this workspace for the pipeline.

### Knowledge base
**Rules**
- `learnings/test-failures/proxy-backed-openai-client-constructor-assertions.md`: avoid over-constraining OpenAI client tests; inspect only the kwargs that are part of the behavior under change.
- `learnings/test-failures/acceptance-verification-proxy-backed-llm-tests.md`: verify each LLM entrypoint that creates a client or request object instead of relying on indirect coverage.

**Gotchas**
- `learnings/test-failures/acceptance-verification-proxy-backed-llm-tests.md`: full-suite `pytest` in this repo can need environment setup such as `DRIVE_FOLDER_ID` and a usable `yt-dlp` on `PATH`; that is an environment risk, not a reason to widen the code change.
- `learnings/test-failures/acceptance-verification-proxy-backed-openai-changes.md`: when the requested code change is narrow, keep verification failures separated into product changes vs pre-existing test-environment issues.

## Available Skills

- `compound-plan`: create and maintain this plan file.
- `recall-knowledge`: already relevant for pulling local learnings about this pipeline's LLM tests.
- `tdd`: use during implementation if the agent follows the RED/GREEN workflow below.
- `run-and-debug-app-tests`: use if the requested `pytest` verification fails and root-cause isolation is needed.
- `validate-implementation`: use after implementation to confirm only the requested behavior changed.
- `save-learning`: mandatory final step after implementation per task instructions.

## Solutions

- Replace the hardcoded chat-completions model in `analyze_text()` with `os.getenv("LLM_MODEL", "gpt-4o")`.
- Leave `embed_text()` unchanged so `OPENAI_EMBEDDING_MODEL` remains the only embedding-model control.
- Add a focused unit test that proves `analyze_text()` uses the env override and falls back to `gpt-4o`; keep assertions on the request kwargs, not on unrelated OpenAI client details.

## Implementation

### Pre-implementation checklist
- [ ] Edit only `youtube-transcript-pipeline/src/llm_client.py` and `youtube-transcript-pipeline/test/test_llm_client.py`.
- [ ] Preserve existing `OPENAI_BASE_URL`, `OPENAI_API_KEY`, and `OPENAI_EMBEDDING_MODEL` behavior.
- [ ] Keep the default chat model at `gpt-4o` when `LLM_MODEL` is unset.

### Kroky implementace
1. In `youtube-transcript-pipeline/test/test_llm_client.py`, add a targeted test around `analyze_text()` that patches `src.llm_client.OpenAI`, sets `LLM_MODEL`, calls `analyze_text()`, and asserts `mock_client.chat.completions.create` received the expected `model` kwarg.
2. Extend the same test area with a default-path assertion for `gpt-4o` when `LLM_MODEL` is absent, or fold both checks into one test using `patch.dict(os.environ, ..., clear=False)` in two sub-scenarios.
3. In `youtube-transcript-pipeline/src/llm_client.py`, change only the `model=` argument in `client.chat.completions.create(...)` to `os.getenv("LLM_MODEL", "gpt-4o")`.
4. Run the targeted test first, then run `pytest` from `~/Projects/ai-research/youtube-transcript-pipeline` as requested.
5. If full-suite verification fails for environment reasons (`pytest` missing from PATH, `DRIVE_FOLDER_ID`, or `yt-dlp`), record that separately from the code change and, if needed, confirm with `python3 -m pytest` for local validation.
6. After implementation and verification, invoke `save-learning` as the last action and capture the env-configurable-model pattern plus any verification gotchas.

## Files to Modify

| Soubor | Zmena |
|--------|-------|
| `youtube-transcript-pipeline/src/llm_client.py` | Replace the hardcoded chat model with `os.getenv("LLM_MODEL", "gpt-4o")`. |
| `youtube-transcript-pipeline/test/test_llm_client.py` | Add/extend a focused unit test that asserts the completion request uses the env-selected model and the new default. |

## TDD

**Workflow pro implementujiciho agenta:**
1. Vytvor/uprav test soubor podle skeletonu nize.
2. Spust testy a over RED.
3. Implementuj zmenu v `src/llm_client.py`.
4. Spust stejny test znovu a over GREEN.
5. Spust cely `pytest` suite.

> Implementace TDD cyklu dle skill:tdd. RED/GREEN evidence patri do `plans/checkpoints/calm-brook-6860.red-green-proof.md`.

### Targeted Tests

**Test file:** `youtube-transcript-pipeline/test/test_llm_client.py`
**Framework:** `unittest` with `unittest.mock`, because the existing LLM client tests already use it.
**Run command:** `python3 -m pytest test/test_llm_client.py -k llm_model`
**Edit hint:** Append a new `test_analyze_text_uses_llm_model_env_and_default` method inside `TestLLMClient`.

```python
from unittest.mock import patch
import os

@patch('src.llm_client.OpenAI')
def test_analyze_text_uses_llm_model_env_and_default(self, mock_openai_class):
    mock_client = MockOpenAI(response_content="Model-aware analysis")
    mock_openai_class.return_value = mock_client

    with patch.dict(os.environ, {"LLM_MODEL": "gpt-4.1"}, clear=False):
        analyze_text(
            transcript=self.test_text,
            intent="video_general",
            lang="cs",
            extra_context=self.test_extra_context,
        )

    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    self.assertEqual(call_kwargs["model"], "gpt-4.1")  # RED: current code sends gpt-4o-mini
```

| Test (odpovida skeletonu) | RED (pred impl) | GREEN (po impl) |
|------|------|-------|
| `test_analyze_text_uses_llm_model_env_and_default` env override branch | `AssertionError: 'gpt-4o-mini' != 'gpt-4.1'` | completion call uses `model='gpt-4.1'` |
| `test_analyze_text_uses_llm_model_env_and_default` default branch | `AssertionError: 'gpt-4o-mini' != 'gpt-4o'` | completion call uses `model='gpt-4o'` when env var is absent |

### Regression
- [ ] `pytest` from `youtube-transcript-pipeline/`

## Dependencies

- Existing Python test dependencies from `youtube-transcript-pipeline/requirements-dev.txt` must already be installed.
- Local shell may need `python3 -m pytest` instead of bare `pytest` if `pytest` is not on `PATH`.
- Full-suite collection may require local environment values already used elsewhere in the repo, especially `DRIVE_FOLDER_ID` and a reachable `yt-dlp` binary.
