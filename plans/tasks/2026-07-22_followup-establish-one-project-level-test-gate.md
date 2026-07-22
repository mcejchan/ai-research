# [acceptance-fix] Establish one project-level test gate: goal-002: The registry invokes that command rather than only pipeline pytest.

Auto-created by the monitor because the original task `bold-dune-3929` was accepted as done
but did not fully meet all acceptance goals.

## Primary goals (from original task)

- goal-002: The registry invokes that command rather than only pipeline pytest.

### [BLOCKING] finding-001 - required_implementation_missing / correctness

**Scope:** `goal-002`  
**Claim:** The ai-research registry testCommand was not updated to invoke the new root repository-health gate.

**Observed**
The supplied task-scoped diff adds Makefile test orchestration and documents make test, but contains no change to /Users/michal/.openclaw/workspace/skills/opencode-dev/projects.yaml; the additional artifacts also provide no registry content showing the command was wired.

**Why this matters**
Goal goal-002 explicitly requires the registry to invoke the single root command rather than pipeline pytest, so the root gate is not authoritative for registered project testing without this wiring.

**Required action**
Update the ai-research testCommand in skills/opencode-dev/projects.yaml to run the repository root gate, and supply that delivered change for review.

**Evidence**
- plan: `/Users/michal/Projects/ai-research/plans/2026-07-22_bold-dune-3929_establish-one-project-level-test-gate.md:55`
- artifact: `caller-supplied-task-scoped-diff`


## Context

- Original task: `bold-dune-3929`
- Reason: `acceptance_incomplete`
- The original task's code changes are preserved. Continue from that state.

## Instructions

Use the concrete goals and findings above to repair the untrustworthy task outcome. Make the minimum implementation and test changes needed, and verify the repaired behavior.

## Important: do not repeat completed work

The previous attempt partially succeeded. Review what is already committed before making changes. Do NOT revert or redo completed work. If the previous approach caused the failure, try a different approach.

## Original plan

Read the original plan at `/Users/michal/Projects/ai-research/plans/2026-07-22_bold-dune-3929_establish-one-project-level-test-gate.md` for full context. Focus only on the unmet goals listed above.

## Previous attempt: acceptance context


**Already done (do NOT redo):**
- goal-001: A single documented root command represents repository health and returns non-zero when any delegated suite fails.
- goal-003: Quiz deployment cannot proceed when its maintained test fails.
- goal-004: Quiz tests cover `extra-easy` and unknown difficulty consistently with the chosen contract.
- goal-005: Python tests collect without a production `DRIVE_FOLDER_ID` dependency at module import.
- goal-006: All delegated suites pass in their supported local/test environment.
- goal-007: No duplicate test orchestration path is introduced beyond the root delegator and deployment's justified quiz preflight.

## Recent learnings from previous attempt


### root-test-gates-expose-hidden-suite-failures.md

```
---
title: "Root test gates expose hidden suite failures"
date: 2026-07-22
category: tooling
component: ci-cd
tags: [make, test-gate, pytest, node, configuration, ci]
file_type: rules
---

# Root test gates should expose configuration and latent suite failures

A repository-level test gate should remain a thin delegator: invoke each maintained subsystem runner unchanged, in a deterministic order, and let the first non-zero status stop the gate. For this repository, `make test` composes the quiz Node test, yt-viewer Node test, and pipeline `python3 -m pytest` without merging subsystem architect
```

## Implementation session log excerpt (last 50 lines)

```
 test gate via `make test`.

Key changes:
- Composes quiz, yt-viewer, and Python pytest suites.
- Normalizes unknown quiz difficulties to `hard`; preserves `extra-easy`, `easy`, and `hard`.
- Defers `DRIVE_FOLDER_ID` validation until real Drive execution.
- Gates quiz deployment on its test suite.
- Updated project registry to use `make test`.
- Repaired latent Python test-fixture issues exposed after collection succeeded.
- Documented the root command in `README.md`.

Verification:
- Quiz: 2 passed
- yt-viewer: 1 passed
- Pipeline: 41 passed
- Root `make test`: passed
- Workflow YAML: valid
- `git diff --check`: passed
- RED/GREEN proof verified at `plans/checkpoints/bold-dune-3929.red-green-proof.md`
- Learning saved at `learnings/tooling/root-test-gates-expose-hidden-suite-failures.md`

```

## TDD proof provenance for this acceptance fix

Do not create or fabricate a fake RED after the original implementation exists. Reuse and link the historical genuine RED from the parent or previous proof when applicable, then capture fresh GREEN verification under this follow-up task.
