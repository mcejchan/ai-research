# Plan 2026-08-21: README YouTube pipeline runtime contract

Align operator documentation with the runtime-owned provider contract while keeping mutable defaults and test snapshots out of prose.

## Analysis

- `youtube-transcript-pipeline/src/llm_client.py:105-138` is the runtime authority: both LLM paths use an OpenAI-compatible client, route through the local Copilot Bridge by default, and support direct-provider overrides through `OPENAI_BASE_URL` and `OPENAI_API_KEY`; `LLM_MODEL` controls chat model selection.
- `youtube-transcript-pipeline/test/test_llm_client.py:41-88,158-172` already protects bridge routing, environment overrides, and model selection at the request boundary.
- `youtube-transcript-pipeline/README.md:79-119,144-170,178-198` currently requires direct OpenAI, names a stale model, freezes coverage/test counts, and gives provider-specific troubleshooting for the wrong default mode.
- `CLAUDE.md:31-44,71-84` repeats the stale model and required direct-key setup; it must stop acting as a second operator contract.
- `README.md:7-15` already describes the stable root `make test` gate without counts and needs no change.
- `.architecture-reviews/reports/2026-08-21T080000Z-ai-research.md:24-51` is the background evidence; no PlantUML diagram applies to this documentation-only correction.

## Knowledge Applied

- `learnings/patterns/calm-brook-6860-test-env-configurable-llm-selection-at-the-request-boundary.md`: keep deploy-specific values environment-driven and test them at the outbound request boundary.
- `learnings/patterns/bold-dune-3929-defer-environment-validation-to-execution-boundaries.md`: distinguish optional integration configuration from configuration required only when a mode executes.
- Recall used the local fallback because QMD collection `ai-research-learnings` was unavailable; this does not block planning.

## Available Skills

- `recall-knowledge`: applied before synthesis to ground configuration and test-boundary decisions.
- `save-learning`: run after the plan is complete as the mandatory final action.

## Implementation

1. Edit `youtube-transcript-pipeline/README.md` so the LLM setup names two supported modes: local Copilot Bridge as the default path, and direct OpenAI as an explicit override using `OPENAI_BASE_URL` plus a real `OPENAI_API_KEY`.
2. List stable environment-variable purposes and precedence only; point readers to `src/llm_client.py` for mutable endpoint, placeholder-key, and model defaults instead of copying their values into prose.
3. Remove GPT-4o-mini/default-model claims, the `100% (37/37 tests pass)` snapshot, and direct-OpenAI-only credit/key troubleshooting; replace them with mode-aware connectivity/auth guidance.
4. Keep stable commands, storage modes, output semantics, and test categories; direct repository-wide verification to root `make test` without asserting counts or coverage percentages.
5. Edit `CLAUDE.md` to remove its GPT-4o-mini and required direct-key claims, summarize bridge-default/direct-override modes, and refer to the pipeline README plus `src/llm_client.py` rather than duplicating mutable defaults.
6. Review both documents for remaining claims that make a specific model, provider credential, test count, or coverage percentage authoritative.
7. In the implementation final note, list both changed files, summarize `make test` output, and state that no documentation contract test was added because existing request-boundary tests protect behavior while a prose-string test would reintroduce duplicated volatile facts.

## Files to Modify

| File | Change |
|---|---|
| `youtube-transcript-pipeline/README.md` | Document bridge-default and direct-OpenAI override modes; remove copied runtime defaults and test snapshots. |
| `CLAUDE.md` | Remove stale provider/model setup and defer mutable details to the pipeline README and runtime source. |

## TDD: skip

This is a documentation-only correction, and existing request-boundary tests already cover the runtime facts; a README text test would couple tests to wording or duplicate mutable defaults.

## Verification

1. Run `make test` from `/Users/michal/Projects/ai-research`.
2. Confirm the gate passes all Node suites and the pipeline pytest suite without recording their current counts as documentation.
3. Search `youtube-transcript-pipeline/README.md` and `CLAUDE.md` for `GPT-4o-mini`, `37/37`, `100%`, and direct-key-as-required wording; expect no stale runtime-contract claims.

---
*Created: 2026-08-21*
*Status: DRAFT*
