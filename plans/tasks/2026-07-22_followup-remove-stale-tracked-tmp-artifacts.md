# [acceptance-fix] Remove stale tracked tmp artifacts: goal-004: Any retained learning is unique, accurate, and located under the exist

Auto-created by the monitor because the original task `calm-mist-6511` was accepted as done
but did not fully meet all acceptance goals.

## Primary goals (from original task)

- goal-004: Any retained learning is unique, accurate, and located under the existing canonical `learnings/` hierarchy.
- goal-005: Existing relevant tests pass and final diff contains no unrelated cleanup.

### [BLOCKING] finding-001 - verification_evidence_missing / evidence

**Scope:** `goal-004`  
**Claim:** The retained canonical learning must be reviewable as unique and accurate.

**Observed**
The task-scoped diff names learnings/tooling/verify-deleted-tracked-files-with-worktree-state.md but supplies no content hunk or separate artifact containing its text; the checkpoint only asserts what the learning explains.

**Why this matters**
Without the retained learning content, semantic review cannot verify the explicit uniqueness and accuracy requirement from caller-supplied material.

**Required action**
Supply the content-bearing diff or artifact for the retained learning so its uniqueness, accuracy, and canonical placement can be evaluated.

**Evidence**
- artifact: `task-scoped diff:learnings/tooling/verify-deleted-tracked-files-with-worktree-state.md`
- artifact: `plans/checkpoints/calm-mist-6511.checkpoint.md`

### [BLOCKING] finding-002 - verification_evidence_missing / evidence

**Scope:** `goal-005`  
**Claim:** The explicit acceptance requirement that existing relevant tests pass needs canonical Test Gate evidence.

**Observed**
The caller-supplied canonical Test Gate status is not run and states that no Test Gate evidence exists; checkpoint prose claims verification but is not the canonical Test Gate reference.

**Why this matters**
Acceptance cannot establish the test-pass portion of goal-005 from task-local prose when the caller-owned canonical Test Gate has supplied no result.

**Required action**
Provide a completed canonical Test Gate reference establishing the relevant test outcome for this run.

**Evidence**
- test-gate: `status:not run`
- artifact: `plans/checkpoints/calm-mist-6511.checkpoint.md`


## Context

- Original task: `calm-mist-6511`
- Reason: `acceptance_incomplete`
- The original task's code changes are preserved. Continue from that state.

## Instructions

Treat this as an evidence-only follow-up. Production-code changes are forbidden by default. You must inspect the parent implementation and evidence first, then supply only the missing acceptance evidence. Escalate only if that inspection lets you document a real implementation defect; in that case, make only the minimal fix with tests.

## Important: do not repeat completed work

The previous attempt partially succeeded. Review what is already committed before making changes. Do NOT revert or redo completed work. If the previous approach caused the failure, try a different approach.

## Original plan

Read the original plan at `/Users/michal/Projects/ai-research/plans/2026-07-22_calm-mist-6511_remove-stale-tracked-tmp-artifacts.md` for full context. Focus only on the unmet goals listed above.

## Previous attempt: acceptance context


**Already done (do NOT redo):**
- goal-001: No tracked files remain under `tmp/`.
- goal-002: Disposable `tmp/` content is ignored according to existing repository conventions.
- goal-003: Maintained code and documentation have no dependency on removed files.

## Recent learnings from previous attempt


### verify-deleted-tracked-files-with-worktree-state.md

```
---
title: "Verify tracked-file deletion without changing the index"
date: 2026-07-22
category: tooling
component: tooling
tags: [git, cleanup, verification, index, worktree]
file_type: rules
---

# Verify tracked-file deletion without changing the index

During an implementation task, `git ls-files 'path/**'` reads the Git index, so it continues to list tracked files that have been deleted only in the worktree. That does not mean the proposed deletion failed, and staging solely to make this command empty would unexpectedly alter the user's index.

Before commit, verify the intended state with
```

## Implementation session log excerpt (last 50 lines)

```
us maintained references
[✓] Remove stale tmp files and add repository-convention ignore rule
[✓] Verify references, tracked files, tests, and diff integrity
[✓] Run save-learning skill and save at least one learning
[0m
Implemented the stale `tmp/` cleanup:

- Deleted all six tracked `tmp/*.md` artifacts.
- Added `tmp/` to `.gitignore`.
- Confirmed no maintained callers or required references.
- Preserved historical references and unrelated `/tmp/**` configuration.
- Added learning: `learnings/tooling/verify-deleted-tracked-files-with-worktree-state.md`.
- Updated the mandatory checkpoint.

Verification passed:

- Root `make test`: 44 tests passed.
- `git check-ignore -v tmp/probe.md`: ignored correctly.
- `git diff --check`: clean.
- Scoped diff contains no runtime or pipeline changes.

```

## TDD proof provenance for this acceptance fix

Do not create or fabricate a fake RED after the original implementation exists. Reuse and link the historical genuine RED from the parent or previous proof when applicable, then capture fresh GREEN verification under this follow-up task.
