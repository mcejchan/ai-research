---
title: Fix ignored AI Research pytest configuration
type: implementation
---

# Fix ignored pytest.ini section in AI Research

## Confirmed defect
In /Users/michal/Projects/ai-research/youtube-transcript-pipeline/pytest.ini the section is [tool:pytest], which pytest expects in setup.cfg, not pytest.ini. Host tested pytest.Config.fromdictargs with this file: effective testpaths=[] and addopts=[]. Therefore declared testpaths, coverage and environment configuration are silently ignored. Root make test does run actual Python tests using default discovery and supplies several environment values explicitly, so do NOT describe this as zero tests or a passing no-op. Host Python suite on2026-09-10:42 passed,12 subtests passed,25.88s.

## Scope
Only registered ai-research repository. Characterization-first fix of this pytest config and minimal regression/dependency documentation as necessary. Do not change pipeline behavior, provider credentials, environment values, report publishing or unrelated tests. No live APIs/providers/downloads; use synthetic tests. No external repo inspection, deployment.

## Acceptance
Prove currently ignored config with local test before correction. Correct section to [pytest], verify that pytest/pytest-cov/pytest-env requirements are declared and available via documented existing setup rather than silent fallbacks. Verify actual loaded testpaths/addopts/env, expected42-test collection (explain any changes), offline suite success, and nonzero failures preserved. Ensure enabling previously ignored options does not unexpectedly create tracked artifacts; use disposable coverage outputs as necessary. Preserve make test mixed Node/Python coverage; do not weaken assertions. Record command/effective config evidence and scope.

## Authorization and scope refresh
User authorized registration and repair on 2026-09-10. Recheck named local owners before changes; preserve any equivalent concurrent fix instead of overwriting it. Earlier test counts are audit baselines, not a requirement to freeze the suite. Explain genuine changes in collection. Only edit within the registered project and explicitly named ownership boundary. Record focused verification and remaining host-only checks.
