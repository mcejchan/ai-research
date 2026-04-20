---
title: "Test env-driven LLM config directly, and separate tooling failures from product regressions"
date: 2026-04-20
category: test-failures
component: tooling
tags: [llm, openai, pytest, environment, configuration]
---

# Test env-driven LLM config directly, and separate tooling failures from product regressions

For `youtube-transcript-pipeline/src/llm_client.py`, a model switch from a hardcoded value to `os.getenv("LLM_MODEL", "gpt-4o")` should be validated at the request callsite, not indirectly.

## What worked

`test/test_llm_client.py` already patches `src.llm_client.OpenAI`, so the smallest useful regression test is to call `analyze_text()` twice and inspect:

```python
mock_client.chat.completions.create.call_args.kwargs["model"]
```

That keeps the test focused on the changed behavior:

- `LLM_MODEL=gpt-4.1` should be passed through to the completion request
- missing `LLM_MODEL` should fall back to `gpt-4o`

## Why this pattern is useful

- Env-driven runtime behavior is still normal unit-test surface area, even when the production diff is only one line.
- Existing OpenAI mocks can usually absorb the change without helper rewrites when they accept `create(**kwargs)`.
- Assertions should stay on the request kwargs that changed rather than tightening unrelated OpenAI constructor behavior.

## Verification gotcha

When the task asks for `pytest`, keep local tooling failures separate from the code change. In this workspace, verification was blocked because:

- `pytest` was not on `PATH`
- `python3 -m pytest` failed with `No module named pytest`

That is an environment/setup issue, not evidence that the `LLM_MODEL` change regressed product behavior.
