# [acceptance-fix] Architektonické review — ai-research: README YouTube pipeline runtime contract: goal-005: `make test` passes from `/Users/michal/Projects/ai-research`.

Auto-created by the monitor because the original task `warm-reef-4253` was accepted as done
but did not fully meet all acceptance goals.

## Primary goals (from original task)

- goal-005: `make test` passes from `/Users/michal/Projects/ai-research`.

### [BLOCKING] finding-001 - verification_evidence_missing / evidence

**Scope:** `goal-005`  
**Claim:** The required root make test gate has passing canonical evidence.

**Observed**
The caller-supplied canonical Test Gate status is not run, and no Test Gate evidence exists; the checkpoint only asserts that make test passed without canonical gate provenance or output.

**Why this matters**
Goal-005 explicitly requires make test to pass from the project root, so task-authored checkpoint prose cannot establish the required caller-owned verification result when the canonical Test Gate reference has no run.

**Required action**
Provide a caller-owned canonical Test Gate result showing make test passed from /Users/michal/Projects/ai-research.

**Evidence**
- test-gate: `caller-supplied canonical Test Gate status: not run`
- artifact: `plans/checkpoints/warm-reef-4253.checkpoint.md:7`


## Context

- Original task: `warm-reef-4253`
- Reason: `acceptance_incomplete`
- The original task's code changes are preserved. Continue from that state.

## Instructions

Treat this as an evidence-only follow-up. Production-code changes are forbidden by default. You must inspect the parent implementation and evidence first, then supply only the missing acceptance evidence. Escalate only if that inspection lets you document a real implementation defect; in that case, make only the minimal fix with tests.

## Important: do not repeat completed work

The previous attempt partially succeeded. Review what is already committed before making changes. Do NOT revert or redo completed work. If the previous approach caused the failure, try a different approach.

## Original plan

Read the original plan at `/Users/michal/Projects/ai-research/plans/2026-08-21_warm-reef-4253_architektonick-review-ai-research-readme-youtube-pipeline.md` for full context. Focus only on the unmet goals listed above.

## Previous attempt: acceptance context


**Already done (do NOT redo):**
- goal-001: README/operator docs no longer require direct OpenAI as the default path when runtime defaults to Copilot Bridge.
- goal-002: README/operator docs no longer claim stale GPT-4o-mini defaults or static “100% / 37 tests” style snapshots.
- goal-003: Supported modes are clear: bridge default, direct OpenAI override if still supported.
- goal-004: Any added test is narrow, stable, and justified in the final note; if no test is added, final note explains why documentation-only is safer.

## Recent learnings from previous attempt


### operator-docs-stable-modes-runtime-defaults.md

```
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

For this r
```

## Implementation session log excerpt (last 50 lines)

```
-transcript-pipeline/README.md`
- `CLAUDE.md`
- `plans/checkpoints/warm-reef-4253.checkpoint.md`

The docs now:
- Identify local Copilot Bridge as the default provider path.
- Explain direct OpenAI configuration as an explicit override.
- Delegate mutable model and endpoint defaults to `src/llm_client.py`.
- Remove stale GPT-4o-mini and `100% (37/37)` claims.
- Improve provider-specific troubleshooting.

No documentation test was added because existing runtime tests already protect configuration behavior; README string assertions would duplicate volatile defaults.

**Verification**
- `make test` passed.
- All three Node test suites passed.
- Pytest: `42 passed in 24.76s`.
- `git diff --check` passed.

Saved learning: `learnings/architecture/operator-docs-stable-modes-runtime-defaults.md`.

```

## TDD proof provenance for this acceptance fix

Do not create or fabricate a fake RED after the original implementation exists. Reuse and link the historical genuine RED from the parent or previous proof when applicable, then capture fresh GREEN verification under this follow-up task.
