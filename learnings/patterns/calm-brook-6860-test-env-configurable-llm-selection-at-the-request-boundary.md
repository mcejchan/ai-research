---
title: "Test env-configurable LLM selection at the request boundary"
date: 2026-04-20
category: patterns
component: backend
tags: [llm, environment, configuration, openai, unit-test]
---

A hardcoded OpenAI model in `youtube-transcript-pipeline/src/llm_client.py` was replaced with `os.getenv("LLM_MODEL", "gpt-4o")`. The implementation worked best when the accompanying test stayed narrow: it asserted only the `model` argument passed into the client call, covering both the env override and the default fallback. Reuse this pattern for SDK wrappers and integration clients: make deploy-specific values environment-driven, keep a safe default in code, and test the exact outbound parameter instead of broader mocked behavior.