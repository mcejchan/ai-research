# [acceptance-fix] Route YT pipeline LLM calls through copilot-bridge: Verify the change with `pytest`

Auto-created by the monitor because the original task `bright-brook-9068` was accepted as done
but did not fully meet all acceptance goals.

## Unmet goals from acceptance check

- Verify the change with `pytest`
- Verify the change with a manual pipeline smoke test
- [P2] Missing TDD proof for testable code change (`plans/checkpoints/bright-brook-9068.red-green-proof.md`) -> Provide RED→GREEN evidence in the requested proof file, or explicitly mark TDD as skipped in the plan.

## Context

- Original task: `bright-brook-9068`
- Reason: `acceptance_incomplete`
- The original task's code changes are preserved. Continue from that state.

## Instructions

Implement only the unmet goals above. The original implementation is committed —
build on it, do not revert or redo completed work.

## Important: do not repeat completed work

The previous attempt partially succeeded. Review what is already committed before making changes. Do NOT revert or redo completed work. If the previous approach caused the failure, try a different approach.

## Original plan

Read the original plan at `/Users/michal/Projects/ai-research/plans/2026-04-20_bright-brook-9068_route-yt-pipeline-llm-calls-through-copilot-bridge.md` for full context. Focus only on the unmet goals listed above.

## Previous attempt: acceptance context

**Why incomplete:** The core implementation matches the plan and stays in scope, but required verification evidence is incomplete: there is no completed `pytest` result and no manual pipeline smoke test result in the provided evidence.


**Already done (do NOT redo):**
- Update `analyze_text()` to construct `OpenAI` through the local proxy using `OPENAI_BASE_URL` and a dummy default API key, without changing model selection
- Update `embed_text()` with the same proxy-backed `OpenAI` construction and preserve the embedding model
- Keep code edits limited to `youtube-transcript-pipeline/src/llm_client.py`

## Recent learnings from previous attempt


### proxy-backed-openai-client-constructor-assertions.md

```
---
title: "Proxy-backed OpenAI clients require looser constructor assertions"
date: 2026-04-20
category: test-failures
component: tooling
tags: [openai, copilot-bridge, pytest, mocks, yt-dlp]
---

# Proxy-backed OpenAI clients require looser constructor assertions

When `youtube-transcript-pipeline/src/llm_client.py` was updated to route through `copilot-bridge`, the runtime change was limited to adding `base_url` and a dummy default API key:

```python
client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:18800/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "copilot-bri
```

## Implementation session log excerpt (last 50 lines)

```
LLMClient::test_analyze_text_openai_success`
      - still asserts the old `OpenAI(api_key=...)` signature
    - `test/test_yt_pipeline.py::TestYTPipeline::test_run_for_url_invalid_url`
      - expects `CalledProcessError` but gets `FileNotFoundError` when `yt-dlp` is not on `PATH`
- Manual smoke test succeeded:
  - `PATH="$HOME/Library/Python/3.9/bin:$PATH" DRIVE_FOLDER_ID=test_folder_id USE_WHISPER_FALLBACK=false MAKE_EMBEDDINGS=false python3 -m src.yt_pipeline --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"`
  - Pipeline completed and produced local output including `analysis_main.md`

Task protocol completed:
- Checkpoint updated at `plans/checkpoints/bright-brook-9068.checkpoint.md`
- Learning saved to `learnings/test-failures/proxy-backed-openai-client-constructor-assertions.md`

```
