# [acceptance-fix] [acceptance-fix] AI Research Python 3.15: Make test and pipeline child provenance: goal-001: AI Research Python 3.15: Ma: goal-001: [acceptance-fix] AI Research Python 3.15: Make test and pipeline child

Auto-created by the monitor because the original task `task-91da195f-e8e0-4807-86c1-3ecda9071d25` was accepted as done
but did not fully meet all acceptance goals.

## Primary goals (from original task)

- goal-001: [acceptance-fix] AI Research Python 3.15: Make test and pipeline child provenance: goal-001: AI Research Python 3.15: Ma

### [BLOCKING] finding-001 - implemented_behavior_incorrect / correctness

**Scope:** `goal-001`  
**Claim:** The propagation and stale-runtime fixtures must replace the synthetic project runtime without modifying the real CPython executable to which it initially points.

**Observed**
_synthetic_checkout creates .venv/bin/python as a symlink to real_python, but both later fixtures call _write_executable on that symlink. Path.write_text follows the symlink, so these cases truncate and rewrite the real interpreter target instead of replacing the synthetic checkout entry; they therefore cannot safely or reliably exercise the intended pytest-propagation and stale-runtime branches.

**Why this matters**
The required regression is itself incorrect and can damage the selected host interpreter, while leaving the synthetic runtime as a symlink rather than the intended fixture script.

**Required action**
Unlink the synthetic .venv/bin/python symlink before writing each replacement script, or create isolated non-symlink fixture runtimes, then retain assertions for exact pytest arguments/status and stale-runtime rejection.

**Evidence**
- file: `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py:11-13`
- file: `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py:34-35`
- file: `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py:75-82`
- file: `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py:91-97`

### [BLOCKING] finding-002 - required_tdd_proof_missing / evidence

**Scope:** `goal-001`  
**Claim:** Caller-required TDD evidence must include a credible fresh GREEN for the final repaired four-test regression under the required CPython 3.15.0 runtime, linked to the historical genuine RED.

**Observed**
The supplied proof is the parent task artifact: its GREEN ran under Python 3.9.6, collected three tests, and predates the delivered four-test source. No follow-up task proof artifact supplies the planned fresh GREEN under CPython 3.15.0, and the follow-up checkpoint still marks repair and fresh GREEN capture incomplete.

**Why this matters**
The parent proof cannot demonstrate that the final corrected source passes or that it observes the required real CPython 3.15.0 child provenance; tddRequired is true for this run.

**Required action**
After correcting the final fixture source, capture the follow-up task's genuine GREEN with the real CPython 3.15.0 command and four repaired tests, while linking the authentic parent RED rather than fabricating a new RED.

**Evidence**
- artifact: `plans/checkpoints/task-a45bce59-6f99-4d3f-98fd-35bb161d44c8.red-green-proof.md:GREEN-Phase`
- artifact: `plans/checkpoints/task-91da195f-e8e0-4807-86c1-3ecda9071d25.checkpoint.md:Steps`
- plan: `plans/2026-10-25_task-91da195f-e8e0-4807-86c1-3ecda9071d25_ai-research-python-3-15-make-test-and-pipeline-child.md:TDD`


## Context

- Original task: `task-91da195f-e8e0-4807-86c1-3ecda9071d25`
- Reason: `acceptance_incomplete`
- The original task's code changes are preserved. Continue from that state.

## Instructions

Use the concrete goals and findings above to repair the untrustworthy task outcome. Make the minimum implementation and test changes needed, and verify the repaired behavior.

## Important: do not repeat completed work

The previous attempt partially succeeded. Review what is already committed before making changes. Do NOT revert or redo completed work. If the previous approach caused the failure, try a different approach.

## Original plan

Read the original plan at `/Users/michal/Projects/ai-research/plans/2026-10-25_task-91da195f-e8e0-4807-86c1-3ecda9071d25_ai-research-python-3-15-make-test-and-pipeline-child.md` for full context. Focus only on the unmet goals listed above.

## Recent learnings from previous attempt


### make-test-real-child-provenance.md

```
---
title: "Make test provenance requires observing the real pytest child"
date: 2026-10-25
category: tooling
component: tooling
tags: [makefile, python, pytest, runtime]
---

# Prove Make test runtime provenance through the real child

When a runtime guard validates a project interpreter before launching a test child, report provenance from the real interpreter itself rather than synthesizing identity in a shell stub. A minimal child module can print `sys.executable`, `platform.python_implementation()`, and `sys.version` while emitting a sentinel. For failure propagation, let the fixture dele
```

## Implementation session log excerpt (last 50 lines)

```
-real-child-provenance.md
[0m
**The regression fixtures are updated, but the required proof and verification are incomplete.**

`youtube-transcript-pipeline/test/test_research_python_runtime_contract.py` now uses a real CPython executable for the nominal fixture, checks the pytest child’s arguments and exit status, and adds a stale-runtime rejection case.

I couldn’t capture GREEN: the TDD helper requires a helper-captured RED for this task, while the plan explicitly says to reuse the parent’s historical RED rather than create a new one after the implementation exists. The helper rejected GREEN before running the tests. As a result, the required task proof file is absent, and I haven’t run broader verification. I saved a learning at `learnings/tooling/make-test-real-child-provenance.md`.

```

## TDD proof provenance for this acceptance fix

Do not create or fabricate a fake RED after the original implementation exists. Reuse and link the historical genuine RED from the parent or previous proof when applicable, then capture fresh GREEN verification under this follow-up task.
