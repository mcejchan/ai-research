# Plan 2026-04-20: Route YT pipeline LLM calls through copilot-bridge

Route `src/llm_client.py` OpenAI client construction through the local OpenAI-compatible proxy without changing models, mocks, or other files.

*Status: WIP*
*Vytvoreno: 2026-04-20*

---

## Progress

- [x] Faze 0: Config + Init
- [ ] Faze 1: Research
- [ ] Faze 2: Knowledge
- [ ] Faze 3: Synthesis

## Problem

`src/llm_client.py` currently requires a standalone `OPENAI_API_KEY`, but this workspace routes all LLM traffic through `copilot-bridge` on port `18800`. The plan must update client initialization in `analyze_text()` and `embed_text()` to use `OPENAI_BASE_URL` and a dummy default API key, then verify existing tests and a manual pipeline smoke test. Scope is limited to `src/llm_client.py`.

## Analysis [WIP]

### Kontext z codebase [TODO]

### Relevantni dokumentace [TODO]

### Knowledge base [TODO]

## Available Skills [TODO]

## Solutions [TODO]

## Implementation [TODO]

## Files to Modify [TODO]

## TDD [TODO]

## Dependencies [TODO]
