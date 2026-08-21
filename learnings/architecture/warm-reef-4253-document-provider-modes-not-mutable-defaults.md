---
title: "Document provider modes, not mutable defaults"
date: 2026-08-21
category: architecture
component: backend
tags: [documentation, configuration, openai-compatible, provider-precedence, runtime-contract]
---

The pipeline supports two modes through one OpenAI-compatible client: a local Copilot Bridge is selected when provider overrides are absent, while direct OpenAI requires both `OPENAI_BASE_URL` and `OPENAI_API_KEY`. Operator documentation had become misleading by presenting a direct key and specific models as fixed requirements.

Document stable behavior such as supported modes, override precedence, and which variables operators must set. Keep volatile endpoint placeholders, model fallbacks, and credentials authoritative in executable code such as `src/llm_client.py`. Avoid README assertions for copied defaults or test counts because they duplicate mutable implementation details and quickly become stale; protect configuration behavior with runtime tests instead.