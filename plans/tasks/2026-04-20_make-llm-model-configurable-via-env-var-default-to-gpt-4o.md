# Make LLM model configurable via env var, default to gpt-4o

## Problem
`src/llm_client.py` line 122 has `model="gpt-4o-mini"` hardcoded. No way to switch models without editing code.

## Changes

### `src/llm_client.py`
Line 122 — change:
```python
# OLD:
model="gpt-4o-mini",

# NEW:
model=os.getenv("LLM_MODEL", "gpt-4o"),
```

Note: `os` is already imported at the top of the file.

Default changes from `gpt-4o-mini` to `gpt-4o` (better quality, still free via copilot-bridge).

## Verify
```bash
cd ~/Projects/ai-research/youtube-transcript-pipeline && pytest
```

## DO NOT
- Change the embedding model (already configurable via `OPENAI_EMBEDDING_MODEL`)
- Change base_url or api_key logic
- Add new dependencies
