---
title: "Repository-wide test runs can expose unrelated environment-coupled failures"
date: 2026-05-18
category: test-failures
component: backend
tags: [pytest, openai-client, environment-config, mocking, verification-scope]
---

The task-specific quiz verification passed, but a repository-wide `pytest` run still reported unrelated failures in `test_llm_client.py`. The failures were tied to assumptions about the OpenAI client setup: one test expected the old `OPENAI_BASE_URL` default, while another expected a mock shape that no longer matched the client call path. The reusable lesson is that broad verification can surface pre-existing integration-test coupling to environment defaults and mock internals. Treat those as separate failures unless the task actually changes that area, and keep task acceptance evidence focused on the component under work.