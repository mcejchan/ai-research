---
title: "Keep config-only LLM plans anchored in code and tests"
date: 2026-04-20
category: tooling
component: tooling
tags: [planning, llm, pytest, env-config]
file_type: rules
---

# Keep config-only LLM plans anchored in code and tests

When a task looks like a one-line configuration change in `src/llm_client.py`, the plan still needs to read the adjacent tests before deciding scope.

## Why it mattered

This task only changes:

```python
model=os.getenv("LLM_MODEL", "gpt-4o")
```

But `test/test_llm_client.py` already patches `OpenAI` and is the natural place to prove both behaviors:

- env override via `LLM_MODEL`
- default fallback to `gpt-4o`

## Practical takeaway

- Treat env-driven runtime behavior as testable, even if the production diff is tiny.
- Reuse the existing mock pattern and assert request kwargs with `call_args.kwargs` instead of coupling tests to unrelated constructor details.
- Keep verification failures from `pytest` environment setup separate from the product change itself.
