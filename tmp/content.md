# Acceptance verification for proxy-backed LLM tests

When an acceptance follow-up is limited to verification, the missing artifact can still be a real product gap if it leaves one runtime path unproved.

## What mattered here

- `youtube-transcript-pipeline/src/llm_client.py` already routed both `analyze_text()` and `embed_text()` through the proxy-backed `OpenAI(...)` constructor.
- Acceptance still failed because `test_embed_text_success()` only verified the embedding payload and never asserted the constructor kwargs.
- The correct minimal fix was to keep production code untouched and add constructor assertions in the embedding test, while aligning the analysis test to inspect `mock_openai_class.call_args.kwargs` directly.

## Verification pattern

For this pipeline, the dependable end-to-end verification sequence was:

```bash
python3 -m pytest test/test_llm_client.py::TestLLMClient::test_analyze_text_openai_success test/test_llm_client.py::TestLLMClient::test_embed_text_success
PATH="$HOME/Library/Python/3.9/bin:$PATH" DRIVE_FOLDER_ID=test_folder_id python3 -m pytest
PATH="$HOME/Library/Python/3.9/bin:$PATH" DRIVE_FOLDER_ID=test_folder_id USE_WHISPER_FALLBACK=false MAKE_EMBEDDINGS=false python3 -m src.yt_pipeline --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

## Environment gotchas

- `python3 -m pytest` is more reliable than bare `pytest` in this workspace because `pytest` is not guaranteed to be on the shell PATH.
- The full suite needs `DRIVE_FOLDER_ID` during test collection.
- The suite and smoke test need `yt-dlp` on `PATH`; in this environment that meant `PATH="$HOME/Library/Python/3.9/bin:$PATH"`.

## Why save this

Acceptance can stay red even after the production behavior is correct if one code path is only indirectly tested. For proxy-backed clients, verify constructor kwargs on every entrypoint that instantiates the client, not just the most common one.
