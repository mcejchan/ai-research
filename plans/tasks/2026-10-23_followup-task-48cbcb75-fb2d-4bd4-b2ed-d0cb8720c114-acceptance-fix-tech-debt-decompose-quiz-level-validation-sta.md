# [acceptance-fix] [acceptance-fix] Tech debt: decompose quiz level validation stages: goal-004: Focused characterization covers the cases : goal-001: [acceptance-fix] Tech debt: decompose quiz level validation stages: go

Auto-created by the monitor because the original task `task-b364dbad-44ba-4188-ab44-a38d38ee7433` was accepted as done
but did not fully meet all acceptance goals.

## Primary goals (from original task)

- goal-001: [acceptance-fix] Tech debt: decompose quiz level validation stages: goal-004: Focused characterization covers the cases

### [BLOCKING] finding-001 - required_implementation_missing / correctness

**Scope:** `goal-001`  
**Claim:** The focused characterization still does not cover every required aggregate threshold at and across its boundary.

**Observed**
The added aggregate test checks the position-bias boundary at 9/20 versus 10/20 and checks a longest-answer crossing case at 7/10, but it does not characterize equality for the longest-answer aggregate cutoff or equality/crossing for the much-longer aggregate cutoff.

**Why this matters**
The repair contract explicitly requires focused characterization at and across the aggregate threshold boundaries; leaving aggregate cutoffs unpinned does not fully establish compatibility for the validator contract.

**Required action**
Add exact focused cases at equality and immediately across each established aggregate advisory cutoff, including longest-answer and much-longer ratios, while preserving exact advisory and result semantics.

**Evidence**
- file: `quiz/validate-quiz.test.js:133-174`
- plan: `plans/tasks/2026-10-23_followup-task-b364dbad-44ba-4188-ab44-a38d38ee7433-tech-debt-decompose-quiz-level-validation-stages.md`

### [BLOCKING] finding-002 - required_tdd_proof_missing / evidence

**Scope:** `goal-001`  
**Claim:** The caller-required TDD proof is invalid for the delivered characterization repair.

**Observed**
The RED phase failed because it expected correctIsLongest to be 0 instead of the established value 1 and expected no per-question length advisories where the validator produced them; the GREEN phase followed after those test expectations were corrected, with no production implementation change.

**Why this matters**
A RED produced by mistaken characterization expectations and resolved by changing those expectations to match pre-existing behavior is not a requirement-driven failing test that demonstrates the delivered repair through RED/GREEN evidence.

**Required action**
Provide valid task-scoped TDD provenance as required by the task instructions, using applicable genuine historical RED/GREEN evidence rather than treating corrected mistaken expectations as a fresh RED.

**Evidence**
- artifact: `plans/checkpoints/task-b364dbad-44ba-4188-ab44-a38d38ee7433.red-green-proof.md`
- artifact: `plans/checkpoints/task-b364dbad-44ba-4188-ab44-a38d38ee7433.checkpoint.md`


## Context

- Original task: `task-b364dbad-44ba-4188-ab44-a38d38ee7433`
- Reason: `acceptance_incomplete`
- The original task's code changes are preserved. Continue from that state.

## Instructions

Use the concrete goals and findings above to repair the untrustworthy task outcome. Make the minimum implementation and test changes needed, and verify the repaired behavior.

## Important: do not repeat completed work

The previous attempt partially succeeded. Review what is already committed before making changes. Do NOT revert or redo completed work. If the previous approach caused the failure, try a different approach.

## Original plan

Read the original plan at `/Users/michal/Projects/ai-research/plans/2026-10-23_task-b364dbad-44ba-4188-ab44-a38d38ee7433_tech-debt-decompose-quiz-level-validation-stages-goal-004.md` for full context. Focus only on the unmet goals listed above.

## Recent learnings from previous attempt


### quiz-validator-threshold-characterization.md

```
---
title: "Quiz validator: characterizing strict aggregate thresholds"
date: 2026-10-23
category: architecture
component: general
tags: [quiz, validation, statistics, testing]
---

# Quiz validator threshold characterization

Validator aggregate ratios are strict (`>`), so characterization fixtures should calculate the denominator across all correct-answer marks, not assume one answer per question creates every desired percentage. A position ratio of exactly 45% requires 20 correct marks (for example, 9 of 20); 4/10 is 40%, while 5/10 crosses the threshold. Also assert per-question advisories
```

## Implementation session log excerpt (last 50 lines)

```
sed suite passes **10/10**; the build-index/publication tests pass **6/6**; and `make test` passes, including all **50 Python tests**. The valid CLI fixture exited 0, and the invalid fixture exited 1 with the expected missing-questions diagnostic.

Evidence caveats: the task proof file contains RED and GREEN sections, but the helper rejected a later GREEN capture after I refined the threshold fixture; the final focused run passed directly. I also had no independent Test Gate interface available, so `make test` and the direct Node checks are recorded, but not as separate Test Gate evidence. Details are in `plans/checkpoints/task-b364dbad-44ba-4188-ab44-a38d38ee7433.checkpoint.md`. Saved a validator-threshold learning at `learnings/architecture/quiz-validator-threshold-characterization.md`.

```

## TDD proof provenance for this acceptance fix

Do not create or fabricate a fake RED after the original implementation exists. Reuse and link the historical genuine RED from the parent or previous proof when applicable, then capture fresh GREEN verification under this follow-up task.
