# Route YT pipeline LLM calls through copilot-bridge

## Problem
`src/llm_client.py` requires `OPENAI_API_KEY` env var. We don't have a standalone OpenAI key on this workspace — all LLM access goes through `copilot-bridge` (port 18800), which is an OpenAI-compatible proxy using GitHub Copilot auth.

## Changes

### `src/llm_client.py`
In both `analyze_text()` and `embed_text()`, change the OpenAI client init:

```python
# OLD:
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# NEW:
client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:18800/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "copilot-bridge"),
)
```

The `api_key` default is a dummy value — copilot-bridge ignores it and uses its own auth from opencode's `auth.json`.

### Verify
```bash
cd ~/Projects/ai-research/youtube-transcript-pipeline
pytest
```

All existing tests should pass (they mock the OpenAI client). Then do a manual smoke test:
```bash
python -m src.yt_pipeline --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

## DO NOT
- Change any other files
- Change the model names (gpt-4o-mini, text-embedding-3-large)
- Add new dependencies
- Change test mocks
