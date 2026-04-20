---
title: "Acceptance verification for proxy-backed OpenAI changes"
date: 2026-04-20
category: test-failures
component: tooling
tags: [openai, pytest, copilot-bridge, yt-dlp, verification]
---

# Acceptance verification for proxy-backed OpenAI changes

When `youtube-transcript-pipeline/src/llm_client.py` routes `OpenAI(...)` through the local proxy, the direct effect on tests is the constructor signature.

## What changed

The production code now initializes the client like this:

```python
OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:18800/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "copilot-bridge"),
)
```

Any unit test that still asserts `OpenAI(api_key=os.getenv("OPENAI_API_KEY"))` will fail even though runtime behavior is correct.

## Verification notes

- `pytest` may also need a minimal `DRIVE_FOLDER_ID` in the environment because `src.yt_pipeline` reads it at import time.
- After aligning the LLM constructor assertion, the remaining failing test in this workspace was unrelated to the proxy change: `test_run_for_url_invalid_url` assumes `yt-dlp` is available on the default `PATH`, but the actual failure is `FileNotFoundError` when that binary is absent.
- A manual smoke test can still pass by prepending the local user install path for `yt-dlp`:

```bash
PATH="/Users/michal/Library/Python/3.9/bin:$PATH" \
DRIVE_FOLDER_ID=test_folder_id \
USE_WHISPER_FALLBACK=false \
MAKE_EMBEDDINGS=false \
python3 -m src.yt_pipeline --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

That run succeeded and produced local output including `analysis_main.md`.
