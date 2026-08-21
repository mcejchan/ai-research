---
title: "Keep operator docs stable while runtime owns mutable defaults"
date: 2026-08-21
category: architecture
component: backend
tags: [documentation, runtime-contract, configuration, copilot-bridge, openai]
file_type: rules
---

# Keep operator docs stable while runtime owns mutable defaults

The YouTube pipeline runtime supports two provider modes through one OpenAI-compatible client: a local Copilot Bridge route and a direct OpenAI override. Documentation drifted because it copied a required credential, model name, and test-count snapshot even after runtime routing changed.

For this repository, operator documentation should name stable modes, environment-variable purposes, and precedence. Mutable endpoint, placeholder-key, and model defaults should remain owned by `youtube-transcript-pipeline/src/llm_client.py`, with behavior protected by request-boundary tests in `test/test_llm_client.py`.

Do not add README string tests for endpoint values, model names, or test counts. Such tests create another synchronized copy of volatile facts. Add a documentation contract test only when a stable user-visible invariant is not already protected at the runtime boundary.
