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
    api_key=os.getenv("OPENAI_API_KEY", "copilot-bridge"),
)
```

The production behavior stayed compatible, and the manual smoke test succeeded, but one unit test still asserted the old constructor shape exactly:

```python
mock_openai_class.assert_called_once_with(api_key=os.getenv("OPENAI_API_KEY"))
```

That assertion fails even though the mocked client still works, because the new transport configuration adds `base_url`.

## Practical takeaway

For OpenAI-compatible proxy routing changes, tests should avoid over-constraining client construction unless the exact kwargs are part of the contract.

Better options are:

- assert only the kwargs that matter to the behavior under test
- inspect `call_args.kwargs` selectively
- move client construction behind a small helper if multiple tests need a shared contract

## Related environment gotcha

This repo's smoke test also needed a real executable on `PATH` for `yt-dlp`. Installing the package was not enough for subprocess-based tests unless `~/Library/Python/3.9/bin` was added to `PATH` in the shell running the command.
