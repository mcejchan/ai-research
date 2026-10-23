# [acceptance-fix] Tech debt: decompose quiz page controllers: goal-001: `initLevelsPage` and `initQuizPage` are each below their configured wa

Auto-created by the monitor because the original task `task-76e9cc6c-1557-4dd4-a93f-2cc49993d0e4` was accepted as done
but did not fully meet all acceptance goals.

## Primary goals (from original task)

- goal-001: `initLevelsPage` and `initQuizPage` are each below their configured warning threshold.
- goal-002: Extracted units have explicit quiz-domain responsibilities and can be tested without reproducing controller internals.
- goal-004: Characterization tests cover the key flows above before/alongside the refactor and existing `quiz/build-index.test.js` remains green without weakened assertions.
- goal-007: Final note records resulting function lengths and exact verification commands/results.

### [BLOCKING] finding-001 - required_implementation_missing / correctness

**Scope:** `goal-001`, `goal-002`  
**Claim:** The required quiz-page controller decomposition was not completed.

**Observed**
The supplied checkpoint states that initQuizPage remains 169 lines and above the goal, while app.js imports and uses only the extracted levels helpers; evaluateAnswer and createQuizSession remain standalone test helpers and are not used by initQuizPage.

**Why this matters**
Leaving initQuizPage above the configured warning threshold fails the explicit size goal, and an unwired extracted session unit does not give the production quiz controller a cohesive independently testable boundary.

**Required action**
Decompose initQuizPage below its configured warning threshold and wire cohesive quiz-domain session/evaluation units into the production controller.

**Evidence**
- artifact: `plans/checkpoints/task-76e9cc6c-1557-4dd4-a93f-2cc49993d0e4.checkpoint.md`
- file: `quiz/app.js:1-3`
- file: `quiz/quiz-page-logic.js:27-66`

### [BLOCKING] finding-002 - required_implementation_missing / correctness

**Scope:** `goal-004`  
**Claim:** The required characterization coverage for the controller flows is incomplete.

**Observed**
quiz/app.test.js contains three pure-helper tests. It does not characterize the levels fetch-failure path, missing or invalid level handling, empty-question handling, incorrect-answer and answer-marking behavior, next-button UI transitions, result rendering, or the public controller wiring boundary; the supplied checkpoint also labels the quiz-page decomposition incomplete.

**Why this matters**
The task explicitly requires representative flow characterization, or pure helpers plus the public wiring boundary when DOM support is unavailable. Testing an unwired createQuizSession helper does not protect the existing initQuizPage browser flows from refactor regressions.

**Required action**
Add focused characterization for the enumerated levels and quiz flows, including the production wiring boundary, without weakening existing assertions.

**Evidence**
- file: `quiz/app.test.js:1-54`
- artifact: `plans/checkpoints/task-76e9cc6c-1557-4dd4-a93f-2cc49993d0e4.checkpoint.md`
- plan: `plans/tasks/2026-10-23_tech-debt-decompose-quiz-page-controllers.md`

### [BLOCKING] finding-003 - verification_evidence_missing / evidence

**Scope:** `goal-007`  
**Claim:** The required completed final note with exact verification records was not supplied.

**Observed**
The supplied checkpoint is an in-progress resume note: it records levels at 28 lines and quiz at 169 lines, says the implementation remains incomplete, and summarizes broader checks as passed without recording each exact command and result. The RED/GREEN proof records only the focused node --test quiz/app.test.js command.

**Why this matters**
Goal-007 explicitly requires resulting function lengths and exact verification commands/results in the final note; partial checkpoint and focused TDD records do not provide that completed evidence.

**Required action**
After completing the implementation, provide the final note with both resulting initializer lengths and every exact verification command and outcome required by the task.

**Evidence**
- artifact: `plans/checkpoints/task-76e9cc6c-1557-4dd4-a93f-2cc49993d0e4.checkpoint.md`
- artifact: `plans/checkpoints/task-76e9cc6c-1557-4dd4-a93f-2cc49993d0e4.red-green-proof.md`


## Context

- Original task: `task-76e9cc6c-1557-4dd4-a93f-2cc49993d0e4`
- Reason: `acceptance_incomplete`
- The original task's code changes are preserved. Continue from that state.

## Instructions

Use the concrete goals and findings above to repair the untrustworthy task outcome. Make the minimum implementation and test changes needed, and verify the repaired behavior.

## Important: do not repeat completed work

The previous attempt partially succeeded. Review what is already committed before making changes. Do NOT revert or redo completed work. If the previous approach caused the failure, try a different approach.

## Original plan

Read the original plan at `/Users/michal/Projects/ai-research/plans/2026-10-23_task-76e9cc6c-1557-4dd4-a93f-2cc49993d0e4_tech-debt-decompose-quiz-page-controllers.md` for full context. Focus only on the unmet goals listed above.

## Previous attempt: acceptance context


**Already done (do NOT redo):**
- goal-003: Existing public `sameSelection` and `levelUrl` CommonJS exports remain compatible; any additional exports are test-focused and minimal.
- goal-005: Browser behavior, localStorage schema, security validation, visible text and CSS/HTML contracts are preserved.
- goal-006: No new generic modules or unrelated source churn are introduced.

## Recent learnings from previous attempt


### testable-logic-for-static-quiz-pages.md

```
---
title: "Testovatelná logika pro statické quiz stránky"
date: 2026-10-23
category: architecture
component: frontend
tags: [quiz, vanilla-javascript, testing, static-hosting]
---

## Vanilla static-page script extraction

When extracting browser logic into a separate file in this dependency-free quiz, preserve the static-host contract by loading the domain script before `app.js` in both HTML entry points. A CommonJS `require` works in Node tests only; browser runtime needs a guarded global export. Keep the browser startup guard intact so requiring `app.js` in Node does not touch `document`.

```

## Implementation session log excerpt (last 50 lines)

```
hodnocení a přechody kvízu. `initLevelsPage` má nyní 28 řádků, ale `initQuizPage` zůstává na 169 řádcích, takže hlavní cíl plánu — dekompozice obou inicializátorů — není splněn. Chybí také DOM-level charakterizace načítání a chybových stavů.

Co je hotové:
- Přidán `quiz/quiz-page-logic.js`, načítaný před `app.js` v obou HTML stránkách.
- Přidán `quiz/app.test.js` s testy logiky vykreslení, výběru odpovědí, skóre a `levelUrl`.
- RED/GREEN důkaz je uložen v požadovaném souboru; GREEN pro `node --test quiz/app.test.js` prošel.
- `make test`, cílené quiz testy a kontroly syntaxe prošly.
- Uložen learning do `learnings/architecture/testable-logic-for-static-quiz-pages.md`.

Průběh a zbývající práce jsou zaznamenány v `plans/checkpoints/task-76e9cc6c-1557-4dd4-a93f-2cc49993d0e4.checkpoint.md`.

```

## TDD proof provenance for this acceptance fix

Do not create or fabricate a fake RED after the original implementation exists. Reuse and link the historical genuine RED from the parent or previous proof when applicable, then capture fresh GREEN verification under this follow-up task.
