# [acceptance-fix] AI Research Python 3.15: Make test and pipeline child provenance: goal-001: AI Research Python 3.15: Make test and pipeline child provenance

Auto-created by the monitor because the original task `task-a45bce59-6f99-4d3f-98fd-35bb161d44c8` was accepted as done
but did not fully meet all acceptance goals.

## Primary goals (from original task)

- goal-001: AI Research Python 3.15: Make test and pipeline child provenance

### [BLOCKING] finding-001 - implemented_behavior_incorrect / correctness

**Scope:** `goal-001`  
**Claim:** The focused launcher regression must observe the selected real CPython 3.15.0 executable, implementation, and full version while exercising the real Make test recipe.

**Observed**
The synthetic checkout creates .venv/bin/python as a /bin/sh script that prints a hard-coded identity whenever its first argument is -c. It neither runs nor observes a real CPython executable, and its success output does not include an observed executable path.

**Why this matters**
A shell stub with a hard-coded version can pass even if the Make identity probe is incomplete or semantically wrong, so it does not establish the explicitly required real-interpreter provenance.

**Required action**
Use a real CPython 3.15.0 executable in the synthetic checkout fixture and assert its observed executable path, CPython implementation, full 3.15.0 version, and pytest-child sentinel while retaining hostile ambient python3.

**Evidence**
- file: `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py:35-44`
- plan: `plans/tasks/2026-10-24_python315-project-standard.md:acceptance-and-verification`

### [BLOCKING] finding-002 - implemented_behavior_incorrect / correctness

**Scope:** `goal-001`  
**Claim:** The focused regression must exercise the pytest child invocation and verify its arguments and exit-status propagation.

**Observed**
In the propagation test, the replacement runtime prints PYTEST_ARGS and exits 23 for every invocation. Make first invokes it with -c for identity inspection, so the recipe fails in the inspection error branch and never invokes -m pytest; the test therefore cannot observe pytest arguments or pytest's status.

**Why this matters**
Failing the interpreter probe is a different behavior from propagating the downstream pytest command's arguments and exit status, leaving the required child-propagation contract untested.

**Required action**
Make the fake return a valid CPython 3.15.0 identity for the -c probe, then capture the subsequent -m pytest invocation and exit nonzero there; assert the exact arguments and propagated status.

**Evidence**
- file: `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py:73-95`
- plan: `plans/tasks/2026-10-24_python315-project-standard.md:acceptance-and-verification`

### [BLOCKING] finding-003 - required_implementation_missing / correctness

**Scope:** `goal-001`  
**Claim:** The launcher regression must include a stale or mismatched project-interpreter fixture that fails actionably without ambient fallback.

**Observed**
The delivered test file covers a nominal hard-coded identity, a missing executable, and an inspection failure. It contains no fixture where an executable project runtime reports a non-CPython or non-3.15.0 identity and verifies the actionable mismatch diagnostic and lack of fallback.

**Why this matters**
The missing-runtime branch does not exercise the distinct stale/mismatched-runtime guard required by the task contract.

**Required action**
Add a stale/mismatched executable fixture and assert rejection identifies the expected and observed identities and never invokes ambient python3 or pytest.

**Evidence**
- file: `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py:47-95`
- plan: `plans/tasks/2026-10-24_python315-project-standard.md:acceptance-and-verification`

### [BLOCKING] finding-004 - required_tdd_proof_missing / evidence

**Scope:** `goal-001`  
**Claim:** Caller-required TDD proof must provide credible RED/GREEN evidence for the delivered focused regression.

**Observed**
The GREEN artifact reports all three delivered tests passing, but the delivered propagation fake exits 23 on Make's initial -c identity probe, preventing the later -m pytest invocation; its assertion requires -m and pytest in stderr even though that branch emits only the inspection command/output. The reported GREEN result therefore does not credibly correspond to the supplied final test source.

**Why this matters**
Because tddRequired is true and the supplied GREEN outcome is incompatible with the delivered test's control flow, the mandatory RED/GREEN proof is invalid for the reviewed implementation.

**Required action**
Capture a genuine GREEN proof from the final corrected focused test source after the propagation fixture reaches the pytest child; retain the authentic behavioral RED evidence.

**Evidence**
- artifact: `plans/checkpoints/task-a45bce59-6f99-4d3f-98fd-35bb161d44c8.red-green-proof.md:GREEN-Phase`
- file: `youtube-transcript-pipeline/test/test_research_python_runtime_contract.py:73-95`


## Context

- Original task: `task-a45bce59-6f99-4d3f-98fd-35bb161d44c8`
- Reason: `acceptance_incomplete`
- The original task's code changes are preserved. Continue from that state.

## Instructions

Use the concrete goals and findings above to repair the untrustworthy task outcome. Make the minimum implementation and test changes needed, and verify the repaired behavior.

## Important: do not repeat completed work

The previous attempt partially succeeded. Review what is already committed before making changes. Do NOT revert or redo completed work. If the previous approach caused the failure, try a different approach.

## Original plan

Read the original plan at `/Users/michal/Projects/ai-research/plans/2026-10-25_task-a45bce59-6f99-4d3f-98fd-35bb161d44c8_ai-research-python-3-15-make-test-and-pipeline-child.md` for full context. Focus only on the unmet goals listed above.

## Recent learnings from previous attempt


### make-test-python-runtime-pin.md

```
---
title: "Make test gate: pin Python runtime explicitly"
date: 2026-10-25
category: tooling
component: tooling
tags: [makefile, python, pytest, runtime]
---

# Pin Make's Python test branch to the project interpreter

The repository test gate must not invoke ambient `python3`: PATH ordering can select an unrelated interpreter. Resolve the checkout's canonical `.venv/bin/python`, verify both CPython implementation and the exact full version before running pytest, and fail with an actionable diagnostic if it is absent or stale. Keeping the pytest command in the same shell recipe preserves cwd 
```

## Implementation session log excerpt (last 50 lines)

```
evidence in `plans/checkpoints/task-a45bce59-6f99-4d3f-98fd-35bb161d44c8.red-green-proof.md`. In `make test`, the publication check passed (6/6), the quiz index was generated, and both Node test invocations passed (2/2 and 4/4). The Python branch could not run because the host-owned root `.venv` is absent, so canonical `make test` is **not yet fully verified**. The available CPython 3.15.0 has no pytest installed, and Homebrew’s externally-managed-environment policy blocked the requirements dry run.

The handoff and checkpoint document the exact host prerequisite and follow-up verification in `plans/checkpoints/python315-host-handoff.md` and `plans/checkpoints/task-a45bce59-6f99-4d3f-98fd-35bb161d44c8.checkpoint.md`. Saved a learning at `learnings/tooling/make-test-python-runtime-pin.md`.

```

## TDD proof provenance for this acceptance fix

Do not create or fabricate a fake RED after the original implementation exists. Reuse and link the historical genuine RED from the parent or previous proof when applicable, then capture fresh GREEN verification under this follow-up task.
