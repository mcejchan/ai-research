# Architektonické review — ai-research: README YouTube pipeline runtime contract

## Context

Architecture review report: `/Users/michal/Projects/ai-research/.architecture-reviews/reports/2026-08-21T080000Z-ai-research.md`

Problem: the YouTube pipeline README is a stale second authority for the runtime contract.

Evidence from the review:
- README requires a direct OpenAI key, describes GPT-4o-mini, and claims 100% / 37 tests.
- Runtime code actually defaults to the local Copilot Bridge, placeholder bridge key, and `LLM_MODEL=gpt-4o`.
- The current gate found 42 Python tests.
- `make test` passed fully: all Node suites and 42/42 pytest tests.

Impact: setup and troubleshooting guide operators toward a different provider boundary than runtime, while static test-count snapshots drift immediately.

## Scope boundary

Work only inside `/Users/michal/Projects/ai-research`. Do not inspect other repositories or external OpenClaw config. Use the architecture review report above as the external/background evidence source.

## Goal

Update the repository documentation and, only if genuinely useful, add a small public-contract test so the README no longer competes with runtime configuration as a second source of truth.

## Requirements

1. Keep stable setup and supported operating modes in the README.
2. Remove copied runtime defaults and static test-count/snapshot claims that drift.
3. Explicitly document that the local Copilot Bridge is the default provider path.
4. Document direct OpenAI as an override mode if the code still supports it.
5. Do not introduce another configuration generator or broad doc-sync mechanism.
6. If adding a test, keep it small and focused only on genuinely public facts that should remain documented; do not test ephemeral counts or model snapshots.

## Acceptance criteria

- README/operator docs no longer require direct OpenAI as the default path when runtime defaults to Copilot Bridge.
- README/operator docs no longer claim stale GPT-4o-mini defaults or static “100% / 37 tests” style snapshots.
- Supported modes are clear: bridge default, direct OpenAI override if still supported.
- Any added test is narrow, stable, and justified in the final note; if no test is added, final note explains why documentation-only is safer.
- `make test` passes from `/Users/michal/Projects/ai-research`.

## Verification

Run:

```bash
cd /Users/michal/Projects/ai-research
make test
```

Final note must include changed files and verification output summary.
