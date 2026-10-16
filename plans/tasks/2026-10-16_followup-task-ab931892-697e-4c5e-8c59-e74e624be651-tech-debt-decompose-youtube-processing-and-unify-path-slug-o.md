# [acceptance-fix] Tech debt: decompose YouTube processing and unify path slug ownership: goal-006: Focused and broader offline test suites pass. The final note records e

Auto-created by the monitor because the original task `task-4b4c2668-1c7b-4098-8cc3-c1d143a53ac0` was accepted as done
but did not fully meet all acceptance goals.

## Primary goals (from original task)

- goal-006: Focused and broader offline test suites pass. The final note records exact commands/results, resulting `run_for_url` line count, the chosen slug owner, rewired callers, and any deliberately retained distinct title behavior.

### [BLOCKING] finding-001 - verification_evidence_missing / evidence

**Scope:** `goal-006`  
**Claim:** Canonical evidence that the focused and broader offline suites pass is missing.

**Observed**
The caller states that Test Gate was not run and no canonical Test Gate evidence exists; the supplied checkpoint only summarizes pass counts, while the detailed proof covers the six-test focused RED/GREEN command.

**Why this matters**
Goal 006 explicitly requires focused and broader offline suites to pass, and acceptance may establish that test-artifact goal only from supplied artifacts and the canonical Test Gate reference. The canonical reference provides no execution evidence for the broader commands.

**Required action**
Provide canonical Test Gate evidence for the required focused and broader offline verification commands and their results.

**Evidence**
- test-gate: `status:not-run`
- artifact: `plans/checkpoints/task-4b4c2668-1c7b-4098-8cc3-c1d143a53ac0.checkpoint.md:6`
- artifact: `plans/checkpoints/task-4b4c2668-1c7b-4098-8cc3-c1d143a53ac0.red-green-proof.md`

### [BLOCKING] finding-002 - required_artifact_missing / correctness

**Scope:** `goal-006`  
**Claim:** The required final note is absent from the supplied task artifacts.

**Observed**
The supplied checkpoint is a brief completion summary and does not record the exact verification commands/results, identify  as the chosen owner, enumerate the rewired callers, or state the deliberately retained title behavior; the other supplied artifact is only RED/GREEN proof.

**Why this matters**
Goal 006 makes that detailed final note an explicit task deliverable, not merely optional verification commentary.

**Required action**
Supply a final note recording exact commands and results, the 24-line  result, the chosen slug owner, all rewired callers, and the retained slash/underscore, empty-fallback, and 80-character title behavior.

**Evidence**
- artifact: `plans/checkpoints/task-4b4c2668-1c7b-4098-8cc3-c1d143a53ac0.checkpoint.md:6`
- artifact: `plans/checkpoints/task-4b4c2668-1c7b-4098-8cc3-c1d143a53ac0.red-green-proof.md`
- plan: `plans/tasks/2026-10-16_tech-debt-decompose-youtube-run-and-unify-slugs.md:acceptance-criteria`


## Context

- Original task: `task-4b4c2668-1c7b-4098-8cc3-c1d143a53ac0`
- Reason: `acceptance_incomplete`
- The original task's code changes are preserved. Continue from that state.

## Instructions

Use the concrete goals and findings above to repair the untrustworthy task outcome. Make the minimum implementation and test changes needed, and verify the repaired behavior.

## Important: do not repeat completed work

The previous attempt partially succeeded. Review what is already committed before making changes. Do NOT revert or redo completed work. If the previous approach caused the failure, try a different approach.

## Original plan

Read the original plan at `/Users/michal/Projects/ai-research/plans/2026-10-16_task-4b4c2668-1c7b-4098-8cc3-c1d143a53ac0_tech-debt-decompose-youtube-processing-and-unify-path-slug.md` for full context. Focus only on the unmet goals listed above.

## Previous attempt: acceptance context


**Already done (do NOT redo):**
- goal-001: `run_for_url` is below the configured function-length warning threshold and reads as a clear workflow coordinator.
- goal-002: The duplicated path-slug algorithm has one implementation owner; `yt_pipeline.py` and `normalize_kb_paths.py` call it rather than carrying copies.
- goal-003: The shared owner’s placement/import mechanism is simple and works from both documented execution contexts; no runtime `sys.path` trick tied to the caller’s current directory is introduced.
- goal-004: Existing import contracts remain compatible or are explicitly migrated with tests.
- goal-005: Focused tests cover extracted orchestration seams and cross-caller slug equivalence, including Unicode, slash/underscore, punctuation-only fallback, repeated separators, and title length behavior.

## Recent learnings from previous attempt


### tdd-proof-root-for-nested-pipeline.md

```
---
title: "TDD důkaz v podprojektu: pracovní adresář určuje umístění"
date: 2026-10-16
category: tooling
component: tooling
tags: [tdd, pytest, proof-capture, monorepo]
file_type: checklist
---

# TDD proof helper: pracovní adresář určuje cestu kanonického důkazu

V repozitáři `ai-research` je Python projekt v `youtube-transcript-pipeline/`, ale úkolový důkaz musí vzniknout v kořenovém `plans/checkpoints/`. Pomocník `proof-capture.py` ukládá důkaz relativně k adresáři, ze kterého se spouští. Spuštění z adresáře pipeline by vytvořilo nesprávně umístěný artefakt.

Spouštěj pomocníka z kořene re
```

## Implementation session log excerpt (last 50 lines)

```
gs treat slashes and underscores as separators.

**Offline verification passed:**
- Focused RED/GREEN command: `python3 -m pytest youtube-transcript-pipeline/test/test_refactor_contracts.py -q -c youtube-transcript-pipeline/pytest.ini` — accepted RED, then 6 passed on GREEN.
- From `youtube-transcript-pipeline/`: `python3 -m pytest test/test_yt_pipeline.py test/test_config.py -q` — 22 passed; `python3 -m pytest -q` — 50 passed.
- From the repository root: `python3 -m pytest test/test_path_slug_callers.py -q` — 4 passed; `make test` — passed; `git diff --check` — passed.

The required proof is at `plans/checkpoints/task-4b4c2668-1c7b-4098-8cc3-c1d143a53ac0.red-green-proof.md`. The checkpoint is complete, and a learning was saved at `learnings/tooling/tdd-proof-root-for-nested-pipeline.md`.

```

## TDD proof provenance for this acceptance fix

Do not create or fabricate a fake RED after the original implementation exists. Reuse and link the historical genuine RED from the parent or previous proof when applicable, then capture fresh GREEN verification under this follow-up task.
