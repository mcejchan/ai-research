# Plan 2026-04-20: [acceptance-fix] Route YT pipeline LLM calls through copilot-bridge: Verify the change with `pytest`

Close the remaining acceptance gaps by finishing verification-only work on top of the already-committed proxy-backed `OpenAI` change.

## Problem

Complete the unmet acceptance goals without reworking `youtube-transcript-pipeline/src/llm_client.py`: add the missing `embed_text()` proxy-constructor assertion, capture RED to GREEN evidence in `plans/checkpoints/fresh-wave-6764.red-green-proof.md`, rerun package verification with `pytest`, and record the successful proxy-backed smoke test in `plans/checkpoints/fresh-wave-6764.checkpoint.md`.

## Available Skills

- `compound-plan`: maintain this plan at the canonical `calm-peak-2174` path.
- `tdd`: drive the required RED to GREEN proof flow for the touched LLM tests.
- `run-and-debug-app-tests`: use if targeted tests, package `pytest`, or the smoke test fail unexpectedly.
- `validate-implementation`: confirm the acceptance-fix stays limited to unmet verification goals.
- `save-learning`: run last after the verification work is complete.

## Analysis

### Kontext z codebase
- `youtube-transcript-pipeline/src/llm_client.py:105-138` already routes both `analyze_text()` and `embed_text()` through `OpenAI(base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:18800/v1"), api_key=os.getenv("OPENAI_API_KEY", "copilot-bridge"))`; the plan must preserve that code and verify it.
- `youtube-transcript-pipeline/test/test_llm_client.py:41-63` already asserts proxy kwargs for `test_analyze_text_openai_success`, so the remaining test gap is not there anymore.
- `youtube-transcript-pipeline/test/test_llm_client.py:132-144` still checks only the embedding result and does not verify `OpenAI` constructor kwargs; that is the concrete missing acceptance item.
- `plans/checkpoints/fresh-wave-6764.checkpoint.md` says verification is complete, but it does not record the explicit smoke-test command, output path, and final acceptance-oriented outcome in the detail required by the retry task.
- `plans/checkpoints/fresh-wave-6764.red-green-proof.md` does not exist, so RED to GREEN evidence for the targeted LLM tests is still missing.
- `plans/2026-04-20_fresh-wave-6764_route-yt-pipeline-llm-calls-through-copilot-bridge-verify.md` is the original task plan; reuse its verified runtime assumptions, but correct file targets and scope for this acceptance-fix follow-up.

### Relevantní dokumentace
- `CLAUDE.md` requires `pytest` before completion and explicitly says external APIs are mocked.
- `youtube-transcript-pipeline/README.md:142-168` documents `pytest` as the package verification command and keeps the test harness mock-based.
- `youtube-transcript-pipeline/README.md:198-205` shows the pipeline entrypoint is `python -m src.yt_pipeline --url ...`, which matches the required manual smoke test form.
- No `docs/` directory or PlantUML diagrams were found for this workspace, so the plan should rely on repository docs plus direct code/test reads.

### Knowledge base
**Pravidla:**
- `learnings/test-failures/proxy-backed-openai-client-constructor-assertions.md` says proxy-routing changes should be verified by inspecting `call_args.kwargs` selectively instead of freezing the old constructor shape.
- `learnings/test-failures/acceptance-verification-proxy-backed-openai-changes.md` says acceptance verification may need `DRIVE_FOLDER_ID=test_folder_id` for `pytest`, and that the remaining unrelated failure was tied to `yt-dlp` availability on `PATH` rather than the proxy change.
- The same learning captures the previously successful smoke-test command with `PATH="/Users/michal/Library/Python/3.9/bin:$PATH"`, `USE_WHISPER_FALLBACK=false`, and `MAKE_EMBEDDINGS=false`; reuse that command pattern rather than inventing a new smoke path.

**Checklisty:**
- Keep the acceptance-fix limited to unmet goals only: missing `embed_text` constructor coverage, RED/GREEN proof, green verification evidence, and checkpoint detail.
- Do not reopen or refactor `src/llm_client.py` unless the focused verification disproves the current runtime behavior.
- Record evidence against `fresh-wave-6764` checkpoint/proof files, because those files are the acceptance artifacts named in the retry task.

## Solutions

- Extend `test_embed_text_success` in `youtube-transcript-pipeline/test/test_llm_client.py` to assert `mock_openai_class.call_args.kwargs["base_url"]` and `...["api_key"]`, matching the already-proven `analyze_text()` behavior without adding new helpers.
- Capture the RED state by running the focused LLM tests before the final test edit is complete, then rerun the same focused tests after the edit and write both outcomes into `plans/checkpoints/fresh-wave-6764.red-green-proof.md`.
- Run package verification from `youtube-transcript-pipeline/` with the minimum environment needed for this repo (`DRIVE_FOLDER_ID=test_folder_id`; prepend the local `yt-dlp` path if required) and record the accepted green command in `plans/checkpoints/fresh-wave-6764.checkpoint.md`.
- Re-run the manual proxy-backed smoke test with the known-good environment and append the exact command, the generated output path, and the success signal to the same checkpoint file.

## Implementation

### Pre-implementation checklist
- [ ] Confirm `youtube-transcript-pipeline/src/llm_client.py` still uses the proxy-backed `OpenAI` constructor in both entrypoints.
- [ ] Confirm `youtube-transcript-pipeline/test/test_llm_client.py` still lacks proxy-constructor assertions in `test_embed_text_success`.
- [ ] Confirm `plans/checkpoints/fresh-wave-6764.red-green-proof.md` is still absent before creating new evidence.
- [ ] Keep edits limited to the test file plus the two `fresh-wave-6764` evidence files unless verification exposes a task-related regression.

### Kroky implementace
1. Re-read `youtube-transcript-pipeline/test/test_llm_client.py` and preserve the already-fixed `analyze_text()` assertion; only extend `test_embed_text_success` with selective `call_args.kwargs` checks for `base_url` and `api_key`.
2. Use the focused LLM test command to capture RED evidence in `plans/checkpoints/fresh-wave-6764.red-green-proof.md`; if the current branch is already green because part of the edit exists, create RED by applying the missing assertion first in a failing form and record that targeted failure before the final correction.
3. Finish the minimal `embed_text()` assertion update and rerun the same focused LLM tests to capture GREEN evidence in the same proof file.
4. Run package-level `pytest` from `youtube-transcript-pipeline/` with `DRIVE_FOLDER_ID=test_folder_id`; if `yt-dlp` is still not on the default shell `PATH`, rerun with `PATH="/Users/michal/Library/Python/3.9/bin:$PATH"` and treat that as the accepted verification command.
5. Re-run the manual smoke test from `youtube-transcript-pipeline/`: `PATH="/Users/michal/Library/Python/3.9/bin:$PATH" DRIVE_FOLDER_ID=test_folder_id USE_WHISPER_FALLBACK=false MAKE_EMBEDDINGS=false python3 -m src.yt_pipeline --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"`.
6. Update `plans/checkpoints/fresh-wave-6764.checkpoint.md` with the final targeted-test result, package `pytest` command and outcome, smoke-test command, generated output location, and the statement that acceptance-fix scope stayed on verification artifacts.
7. Run `save-learning` last and save at least one learning about acceptance retries, proxy-constructor assertions, or environment-dependent verification evidence.

## Files to Modify

| Soubor | Změna |
|--------|-------|
| `youtube-transcript-pipeline/test/test_llm_client.py` | Add the missing `embed_text()` proxy-constructor assertions while leaving the existing `analyze_text()` coverage intact. |
| `plans/checkpoints/fresh-wave-6764.red-green-proof.md` | Record explicit RED and GREEN evidence for the focused LLM tests. |
| `plans/checkpoints/fresh-wave-6764.checkpoint.md` | Record final verification commands, smoke-test output path, and acceptance-oriented completion notes. |

## TDD

**Workflow pro implementujícího agenta:**
1. Touch only `youtube-transcript-pipeline/test/test_llm_client.py` first.
2. Run the focused LLM tests and capture the failing state in `plans/checkpoints/fresh-wave-6764.red-green-proof.md`.
3. Complete the `embed_text()` constructor assertion update.
4. Rerun the same focused tests and capture the passing state in the same proof file.
5. Run package `pytest` and the manual smoke test after the focused tests are green.

> Implementace TDD cyklu dle skill:tdd — RED/GREEN evidence se zapisuje do `plans/checkpoints/fresh-wave-6764.red-green-proof.md`.

### Targeted Tests

**Test file:** `youtube-transcript-pipeline/test/test_llm_client.py`
**Framework:** `pytest` running the existing `unittest` suite so the current harness stays unchanged.
**Run command:** `pytest test/test_llm_client.py::TestLLMClient::test_analyze_text_openai_success test/test_llm_client.py::TestLLMClient::test_embed_text_success`
**Edit hint:** Keep `test_analyze_text_openai_success` as-is and extend `test_embed_text_success` near line 133.

```python
import os
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
        self.assertEqual(kwargs["base_url"], os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:18800/v1"))
        self.assertEqual(kwargs["api_key"], os.getenv("OPENAI_API_KEY", "copilot-bridge"))

    @patch("src.llm_client.OpenAI")
    def test_embed_text_success(self, mock_openai_class):
        mock_openai_class.return_value = MockOpenAI(embedding_data=[0.1, 0.2, 0.3])

        result = embed_text("Test text for embedding")

        self.assertEqual(result, [0.1, 0.2, 0.3])
        kwargs = mock_openai_class.call_args.kwargs
        self.assertEqual(kwargs["base_url"], os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:18800/v1"))  # RED until embedding path verifies proxy kwargs
        self.assertEqual(kwargs["api_key"], os.getenv("OPENAI_API_KEY", "copilot-bridge"))  # RED until embedding path verifies proxy kwargs
```

| Test | RED (před implementací) | GREEN (po implementaci) |
|------|------|-------|
| `TestLLMClient::test_analyze_text_openai_success` | Should stay green; any failure here means the committed proxy constructor regressed and the task is no longer verification-only. | Confirms `analyze_text()` still constructs `OpenAI` with proxy kwargs. |
| `TestLLMClient::test_embed_text_success` | Fails until the test asserts and proves `base_url` and `api_key` on the embedding client path. | Confirms `embed_text()` uses the same proxy-backed constructor contract. |

### Regression

- [ ] `DRIVE_FOLDER_ID=test_folder_id pytest` passes from `youtube-transcript-pipeline/`, or the accepted rerun with the local `yt-dlp` path prepended is recorded.
- [ ] The manual smoke test succeeds and the resulting local output path is recorded in `plans/checkpoints/fresh-wave-6764.checkpoint.md`.

## Dependencies

- `yt-dlp` may need to be available via `PATH="/Users/michal/Library/Python/3.9/bin:$PATH"` for package verification and the manual smoke test.
- `DRIVE_FOLDER_ID=test_folder_id` may be required when running `pytest` because pipeline imports read that environment at import time.
- The proxy endpoint must remain reachable at `OPENAI_BASE_URL` or the default `http://127.0.0.1:18800/v1` during the smoke test.

---
*Vytvořeno: 2026-04-20*
*Status: DRAFT*
