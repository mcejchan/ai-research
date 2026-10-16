# [acceptance-fix] [acceptance-fix] Tech debt: decompose YouTube processing and unify path slug ownership: goal-006: Focused and broader of: goal-001: [acceptance-fix] Tech debt: decompose YouTube processing and unify pat

Auto-created by the monitor because the original task `task-ab931892-697e-4c5e-8c59-e74e624be651` was accepted as done
but did not fully meet all acceptance goals.

## Primary goals (from original task)

- goal-001: [acceptance-fix] Tech debt: decompose YouTube processing and unify path slug ownership: goal-006: Focused and broader of

### [BLOCKING] finding-001 - verification_evidence_missing / evidence

**Scope:** `goal-001`  
**Claim:** Canonical evidence that the required focused and broader offline suites pass is missing.

**Observed**
The supplied Test Gate status is not run and explicitly states that no canonical Test Gate evidence exists. The checkpoint reports fresh local command results, but also states that those runs cannot replace the requested canonical Test Gate record.

**Why this matters**
Goal 001 carries forward goal-006, which explicitly requires focused and broader offline suites to pass. The caller restricts assessment of this test-artifact goal to supplied artifacts and the canonical Test Gate reference, so local checkpoint summaries do not establish the required canonical verification.

**Required action**
Provide caller-owned canonical Test Gate evidence for the required focused and broader offline verification commands and their successful results.

**Evidence**
- test-gate: `status:not-run`
- artifact: `plans/checkpoints/task-ab931892-697e-4c5e-8c59-e74e624be651.checkpoint.md:Current verification`


## Context

- Original task: `task-ab931892-697e-4c5e-8c59-e74e624be651`
- Reason: `acceptance_incomplete`
- The original task's code changes are preserved. Continue from that state.

## Instructions

Treat this as an evidence-only follow-up. Production-code changes are forbidden by default. You must inspect the parent implementation and evidence first, then supply only the missing acceptance evidence. Escalate only if that inspection lets you document a real implementation defect; in that case, make only the minimal fix with tests.

## Important: do not repeat completed work

The previous attempt partially succeeded. Review what is already committed before making changes. Do NOT revert or redo completed work. If the previous approach caused the failure, try a different approach.

## Original plan

Read the original plan at `/Users/michal/Projects/ai-research/plans/2026-10-16_task-ab931892-697e-4c5e-8c59-e74e624be651_tech-debt-decompose-youtube-processing-and-unify-path-slug.md` for full context. Focus only on the unmet goals listed above.

## Recent learnings from previous attempt


### followup-note-proof-does-not-substitute-for-test-gate.md

```
---
title: "Důkaz následného artefaktu nezastupuje kanonickou Test Gate"
date: 2026-10-16
category: tooling
component: tooling
tags: [acceptance, tdd, test-gate, provenance]
file_type: checklist
---

Při evidence-only follow-upu k již implementovanému refaktoru zachovej historický genuine RED pro produkční změnu. Pokud následný úkol vyžaduje nový RED/GREEN, otestuj skutečně chybějící následný artefakt před jeho vytvořením a výslovně odděl tento důkaz od původního refaktoru. Proof-capture.py potvrzuje pouze identitu cíleného příkazu a jeho RED/GREEN výsledek, nikoli širší suite. Lokálně úspěšný
```

## Implementation session log excerpt (last 50 lines)

```
tract **4**, and pipeline **50** tests. The follow-up proof captures a genuine failing test for the missing note, followed by **1 passing** test after the note was added; the original refactor’s historical RED/GREEN proof is linked separately.

`run_for_url` spans lines **215–238 (24 lines)**. `youtube-transcript-pipeline/src/path_slugs.py` owns the slug rules; the checkpoint names all three rewired callers and the deliberately distinct path/title behavior. No production code was changed. A learning was saved at `learnings/tooling/followup-note-proof-does-not-substitute-for-test-gate.md`.

**Remaining action:** the caller/orchestrator must run its canonical Test Gate for the specified offline commands and attach its reference. The local results cannot be presented as that gate’s evidence.

```

## TDD proof provenance for this acceptance fix

Do not create or fabricate a fake RED after the original implementation exists. Reuse and link the historical genuine RED from the parent or previous proof when applicable, then capture fresh GREEN verification under this follow-up task.
