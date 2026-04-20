# Plan 2026-04-20: [acceptance-fix] Route YT pipeline LLM calls through copilot-bridge: Verify the change with `pytest`

Finish the acceptance evidence around the already-committed proxy-backed `OpenAI` client change without reworking `src/llm_client.py`.

## Problem

Close the remaining acceptance gaps by proving the committed `llm_client.py` behavior with `pytest`, proving the runtime path with a manual pipeline smoke test, and writing RED→GREEN evidence to `plans/checkpoints/bright-brook-9068.red-green-proof.md`.

## Available Skills

- `compound-plan`: maintain this plan.
- `tdd`: drive the RED→GREEN test update and proof capture.
- `run-and-debug-app-tests`: use if `pytest` or the smoke run fails.
- `validate-implementation`: use after evidence is captured to confirm no scope creep beyond verification work.
- `save-learning`: run last after the acceptance fix is complete.

## Analysis

### Kontext z codebase
- `youtube-transcript-pipeline/src/llm_client.py:105-138` already routes both `analyze_text()` and `embed_text()` through `OpenAI(base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:18800/v1"), api_key=os.getenv("OPENAI_API_KEY", "copilot-bridge"))`; production code should stay unchanged unless a verification step proves otherwise.
- `youtube-transcript-pipeline/test/test_llm_client.py:41-60` still asserts the old constructor shape with `assert_called_once_with(api_key=os.getenv("OPENAI_API_KEY"))`; this is the direct mismatch against the committed behavior.
- `youtube-transcript-pipeline/test/test_llm_client.py:129-140` checks only the embedding result and does not verify proxy kwargs; add parity coverage there instead of introducing a new helper.
- `youtube-transcript-pipeline/test/test_yt_pipeline.py:302-308` can fail with `FileNotFoundError` when `yt-dlp` is missing on `PATH`; the previous session already showed this is an environment issue, not a required product change.
- `plans/checkpoints/bright-brook-9068.checkpoint.md` already records that implementation is complete and that pytest/smoke evidence is what remains; extend this file with the final commands and outcomes.

### Relevantní dokumentace
- `CLAUDE.md` requires `pytest` verification for this package before completion.
- `youtube-transcript-pipeline/README.md:142-168` documents `pytest` as the project verification command and `python -m src.yt_pipeline --url ...` as the manual pipeline entrypoint.
- No PlantUML or additional architecture docs were found for this pipeline area.

### Knowledge base
**Pravidla:**
- `learnings/test-failures/proxy-backed-openai-client-constructor-assertions.md` says proxy-routing tests must assert constructor kwargs selectively instead of freezing the old `OpenAI(api_key=...)` signature.
- The same learning records the working smoke-test command and the `yt-dlp` PATH requirement: `PATH="$HOME/Library/Python/3.9/bin:$PATH"`.

**Checklisty:**
- Keep acceptance-fix scope on unmet goals only: test coverage alignment, pytest evidence, smoke-test evidence, proof/checkpoint updates.
- Do not reopen the already-accepted `src/llm_client.py` transport change unless verification exposes a real regression.

## Solutions

- Update `test/test_llm_client.py` to verify proxy kwargs through `mock_openai_class.call_args.kwargs` in both `analyze_text` and `embed_text`, while keeping the existing mock-based structure.
- Use focused RED→GREEN runs on the touched llm tests to populate `plans/checkpoints/bright-brook-9068.red-green-proof.md`.
- Run package-level `pytest` from `youtube-transcript-pipeline/`; if `yt-dlp` is not discoverable, rerun with `PATH="$HOME/Library/Python/3.9/bin:$PATH"` and record that environment requirement as part of the verification evidence instead of changing unrelated pipeline code.
- Re-run the previously successful manual smoke test with the proxy-backed environment and record the command, output location, and success signal in `plans/checkpoints/bright-brook-9068.checkpoint.md`.

## Implementation

### Pre-implementation checklist
- [ ] Confirm the current branch still contains the proxy-backed `OpenAI` constructor in `youtube-transcript-pipeline/src/llm_client.py`.
- [ ] Confirm `plans/checkpoints/bright-brook-9068.red-green-proof.md` does not already contain completed RED→GREEN evidence.
- [ ] Keep code edits limited to verification artifacts and test coverage unless a verification step proves the committed runtime behavior is wrong.

### Kroky implementace
1. Edit `youtube-transcript-pipeline/test/test_llm_client.py` first: replace the strict `assert_called_once_with(...)` constructor assertion with selective `call_args.kwargs` checks for `base_url` and `api_key`, and add the same proxy assertion coverage to `test_embed_text_success`.
2. Run only the touched llm tests before any further edits and capture the RED state in `plans/checkpoints/bright-brook-9068.red-green-proof.md`; use the existing failing constructor assertion as the initial RED if it is still present.
3. Complete the minimal test edit, rerun the same focused llm tests, and capture the GREEN result in the same proof file.
4. Run `pytest` from `youtube-transcript-pipeline/`; if the suite stops on missing `yt-dlp`, rerun with `PATH="$HOME/Library/Python/3.9/bin:$PATH" pytest` and record which command produced the accepted verification result.
5. Run the manual smoke test from `youtube-transcript-pipeline/` with the previously proven environment: `PATH="$HOME/Library/Python/3.9/bin:$PATH" DRIVE_FOLDER_ID=test_folder_id USE_WHISPER_FALLBACK=false MAKE_EMBEDDINGS=false python3 -m src.yt_pipeline --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"`.
6. Update `plans/checkpoints/bright-brook-9068.checkpoint.md` with the final pytest command(s), the smoke-test command, and the observed success evidence, including the generated local output path.
7. Run `save-learning` last and store at least one learning about acceptance evidence or proxy-routing verification gotchas discovered during this follow-up.

## Files to Modify

| Soubor | Změna |
|--------|-------|
| `youtube-transcript-pipeline/test/test_llm_client.py` | Align mocked `OpenAI` assertions with the committed proxy-backed constructor and cover both analysis and embedding client creation. |
| `plans/checkpoints/bright-brook-9068.red-green-proof.md` | Record focused llm-test RED→GREEN evidence for the verification fix. |
| `plans/checkpoints/bright-brook-9068.checkpoint.md` | Record final `pytest` and manual smoke-test commands plus outcomes for acceptance evidence. |

## TDD

**Workflow pro implementujícího agenta:**
1. Edit `youtube-transcript-pipeline/test/test_llm_client.py` before any verification rerun.
2. Run the focused llm tests and capture the failing assertion in `plans/checkpoints/bright-brook-9068.red-green-proof.md`.
3. Finish the minimal assertion update.
4. Rerun the same tests and capture the passing result in the same proof file.
5. Run package-level `pytest` and the manual smoke test to prove no regression outside the focused tests.

> Implementace TDD cyklu dle skill:tdd — RED/GREEN evidence se zapisuje do `plans/checkpoints/bright-brook-9068.red-green-proof.md`.

### Targeted Tests

**Test file:** `youtube-transcript-pipeline/test/test_llm_client.py`
**Framework:** `pytest` running existing `unittest` tests; keeps the current test harness unchanged.
**Run command:** `pytest test/test_llm_client.py::TestLLMClient::test_analyze_text_openai_success test/test_llm_client.py::TestLLMClient::test_embed_text_success`
**Edit hint:** Replace the constructor assertion at line ~59 and extend the embedding test near line ~140.

```python
import os
import unittest
from unittest.mock import patch

from src.llm_client import analyze_text, embed_text
from test.mocks.mock_llm import MockOpenAI


class TestLLMClient(unittest.TestCase):
    @patch("src.llm_client.OpenAI")
    def test_analyze_text_openai_success(self, mock_openai_class):
        mock_openai_class.return_value = MockOpenAI(response_content="Mock analysis result")

        analyze_text(
            transcript="This is a test transcript.",
            intent="video_general",
            lang="cs",
            extra_context={"title": "Test", "channel": "Test", "url": "https://example.com"},
        )

        kwargs = mock_openai_class.call_args.kwargs
        self.assertEqual(kwargs["base_url"], os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:18800/v1"))  # RED if old constructor is still asserted or used
        self.assertEqual(kwargs["api_key"], os.getenv("OPENAI_API_KEY", "copilot-bridge"))  # RED if dummy default proxy key is not wired

    @patch("src.llm_client.OpenAI")
    def test_embed_text_success(self, mock_openai_class):
        mock_openai_class.return_value = MockOpenAI(embedding_data=[0.1, 0.2, 0.3])

        embed_text("Test text for embedding")

        kwargs = mock_openai_class.call_args.kwargs
        self.assertEqual(kwargs["base_url"], os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:18800/v1"))  # RED if embedding path bypasses proxy
        self.assertEqual(kwargs["api_key"], os.getenv("OPENAI_API_KEY", "copilot-bridge"))  # RED if embedding path uses no proxy key default
```

| Test | RED (před úpravou testu) | GREEN (po úpravě testu) |
|------|------|-------|
| `TestLLMClient::test_analyze_text_openai_success` | Existing assertion fails because the mock is called with `base_url` and a defaulted `api_key`, not only `api_key=os.getenv("OPENAI_API_KEY")`. | Selective kwargs assertions match the committed proxy-backed constructor. |
| `TestLLMClient::test_embed_text_success` | No proxy-constructor coverage exists yet, so the verification gap remains unproven. | Test proves `embed_text()` constructs `OpenAI` with the same proxy kwargs as `analyze_text()`. |

### Regression

- [ ] `pytest` from `youtube-transcript-pipeline/` succeeds, or the accepted rerun with `PATH="$HOME/Library/Python/3.9/bin:$PATH" pytest` is recorded with rationale.
- [ ] Manual smoke test succeeds and writes local pipeline output including `analysis_main.md`.

## Dependencies

- `yt-dlp` must be executable from the shell that runs `pytest` and the smoke test; use `PATH="$HOME/Library/Python/3.9/bin:$PATH"` if needed.
- `copilot-bridge` must be reachable at `OPENAI_BASE_URL` or the default `http://127.0.0.1:18800/v1`.
- The smoke test needs a non-empty `DRIVE_FOLDER_ID`; local fallback output should remain available under `local-knowledge-base/youtube/`.

---
*Vytvořeno: 2026-04-20*
*Status: DRAFT*
