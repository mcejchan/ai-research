---
title: "Test doubles must preserve assertion interfaces"
date: 2026-07-22
category: test-failures
component: backend
tags: [mocking, unittest, call-args, fixtures, openai]
---

The OpenAI fixture returned correct fake responses, but implemented `chat.completions.create` as a plain function. Tests that inspected `.call_args` therefore failed with `AttributeError`. If tests assert invocation details, expose the mocked endpoint as `Mock` or `MagicMock` with a configured side effect or return value rather than as an ordinary function. A useful test double must reproduce both the runtime response and the observation interface used by assertions.