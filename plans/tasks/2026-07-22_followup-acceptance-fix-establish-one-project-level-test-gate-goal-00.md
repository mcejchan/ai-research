# [acceptance-fix] [acceptance-fix] Establish one project-level test gate: goal-002: The registry invokes that command rather than only pip: goal-001: [acceptance-fix] Establish one project-level test gate: goal-002: The 

Auto-created by the monitor because the original task `dark-vale-6236` was accepted as done
but did not fully meet all acceptance goals.

## Primary goals (from original task)

- goal-001: [acceptance-fix] Establish one project-level test gate: goal-002: The registry invokes that command rather than only pip

### [BLOCKING] finding-001 - required_implementation_missing / correctness

**Scope:** `goal-001`  
**Claim:** The caller-supplied material does not deliver the ai-research registry testCommand wiring for semantic review.

**Observed**
The task-scoped diff is empty. The only additional artifact is a checkpoint that asserts the registry goal was delivered in commit 169c092c98, but it does not include the projects.yaml content or the required external registry diff showing testCommand: cd ~/Projects/ai-research && make test.

**Why this matters**
Goal goal-001 requires the registry itself to invoke the root test gate, and the canonical task requires the delivered registry change to be supplied for review. An unsupported checkpoint assertion cannot establish that required configuration behavior from the caller-supplied material.

**Required action**
Supply the delivered ai-research entry from skills/opencode-dev/projects.yaml, or its scoped external diff, showing testCommand set to cd ~/Projects/ai-research && make test.

**Evidence**
- artifact: `caller-supplied-task-scoped-diff`
- artifact: `/Users/michal/Projects/ai-research/plans/checkpoints/dark-vale-6236.checkpoint.md`
- plan: `/Users/michal/Projects/ai-research/plans/2026-07-22_dark-vale-6236_establish-one-project-level-test-gate-goal-002-the-registry.md`


## Context

- Original task: `dark-vale-6236`
- Reason: `acceptance_incomplete`
- The original task's code changes are preserved. Continue from that state.

## Instructions

Use the concrete goals and findings above to repair the untrustworthy task outcome. Make the minimum implementation and test changes needed, and verify the repaired behavior.

## Important: do not repeat completed work

The previous attempt partially succeeded. Review what is already committed before making changes. Do NOT revert or redo completed work. If the previous approach caused the failure, try a different approach.

## Original plan

Read the original plan at `/Users/michal/Projects/ai-research/plans/2026-07-22_dark-vale-6236_establish-one-project-level-test-gate-goal-002-the-registry.md` for full context. Focus only on the unmet goals listed above.

## Recent learnings from previous attempt


### external-registry-changes-need-external-diff-evidence.md

```
---
title: "External registry changes need external diff evidence"
date: 2026-07-22
category: tooling
component: ci-cd
tags: [acceptance, registry, test-gate, evidence, git]
file_type: rules
---

# External registry changes need external diff evidence

When a project task changes configuration stored outside the project repository, a project-scoped diff cannot prove that the change was delivered. Acceptance may reject correct runtime state if its evidence bundle contains only repository-local files.

For `ai-research`, the root `make test` gate lives in the project repository, but its authorit
```

## Implementation session log excerpt (last 50 lines)

```
-learning/add-frontmatter.py" --title "External registry changes need external diff evidence" --category "tooling" --component "ci-cd" --tags "acceptance,registry,test-gate,evidence,git" --file-type "rules" --content-file tmp/dark-vale-6236-learning.md --output learnings/tooling/external-registry-changes-need-external-diff-evidence.md
✓ Learning saved to learnings/tooling/external-registry-changes-need-external-diff-evidence.md
[0m
Implemented and verified goal-002.

- Registry command: `cd ~/Projects/ai-research && make test`
- Delivered in external workspace commit `169c092c98`
- Root gate passed: quiz 2, yt-viewer 1, pipeline 41 tests
- Registry YAML assertion passed
- Checkpoint completed
- Learning saved to `learnings/tooling/external-registry-changes-need-external-diff-evidence.md`

```

## TDD proof provenance for this acceptance fix

Do not create or fabricate a fake RED after the original implementation exists. Reuse and link the historical genuine RED from the parent or previous proof when applicable, then capture fresh GREEN verification under this follow-up task.
