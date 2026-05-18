# Fix copilot-bridge URL prefix in yt_pipeline LLM client

Since copilot-bridge v2.1.0, auto-routing was removed. The pipeline's `src/llm_client.py` uses `OPENAI_BASE_URL` defaulting to `http://127.0.0.1:18800/v1` but bridge now requires explicit prefix `/v1/copilot/chat/completions`.

## Fix

Update default `OPENAI_BASE_URL` in `src/llm_client.py` to `http://127.0.0.1:18800/v1/copilot` (or append the prefix in the client code). Ensure `yt_pipeline --url` works without manual env override.

## Acceptance

- `DRIVE_FOLDER_ID=mock python3 -m src.yt_pipeline --url "<any-yt-url>"` completes analysis without 404 error
