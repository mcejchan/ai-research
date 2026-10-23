# Plan 2026-10-23: Complete aggregate quiz-validator threshold characterization

Extend the existing threshold test to pin omitted aggregate cutoff equality and crossing behavior, reusing historical TDD provenance rather than manufacturing a RED against existing code.

## Analysis

- `quiz/validate-quiz.test.js:133-174` currently covers position bias at 9/20 and 10/20 and longest-answer aggregate crossing at 7/10, but lacks equality for longest-answer and equality/crossing for much-longer ratios.
- `quiz/validate-quiz.js` is the behavior authority; preserve current advisory strings, `ok`, and stats. Do not modify production code unless tests demonstrate a real contract mismatch.
- The original plan and `learnings/architecture/quiz-validator-threshold-characterization.md` establish strict `>` aggregate comparisons and warn to distinguish per-question advisories from aggregate `BIAS:` messages.
- Genuine parent RED/GREEN provenance is in `plans/checkpoints/task-b364dbad-44ba-4188-ab44-a38d38ee7433.red-green-proof.md`; its observed RED was caused by incorrect expectations, so link it as historical context only and capture fresh GREEN for this follow-up.

## Approach

- Add focused cases for exact equality and immediately across the longest-answer cutoff, and equality/crossing for the much-longer cutoff.
- Construct denominators and correct-answer marks deliberately; filter aggregate `BIAS:` advisories separately from question-level length advisories.
- Assert exact advisory arrays (or exact aggregate subsets), structural errors, stats, and `ok` for each boundary fixture.
- Preserve existing position-boundary and structural-error suppression assertions.

## Implementation

1. Inspect `quiz/validate-quiz.js` to confirm the established aggregate cutoffs and advisory text before choosing fixtures.
2. Extend the existing aggregate test in `quiz/validate-quiz.test.js` with equality and one-mark crossing fixtures for the longest-answer and much-longer ratios.
3. Run focused characterization and correct fixture construction/expectations only when they disagree with the existing contract; make no production change absent a demonstrated mismatch.
4. Capture fresh GREEN under this task. Link the parent proof as historical provenance; do not claim its invalid RED as valid requirement-driven evidence.
5. Run `node --test quiz/validate-quiz.test.js` and the project gate `make test`; record exact outcomes in task evidence.
6. Invoke `save-learning` after completing the implementation/verification task as required by the acceptance instructions.

## Testing

- Focused: `node --test quiz/validate-quiz.test.js`.
- Full project: `make test`.
- Confirm exact cutoff equality produces no corresponding aggregate advisory and the first representable ratio across the cutoff produces the existing exact advisory; confirm `ok` and stats remain unchanged in meaning.

## TDD

The production refactor already exists. Do not create a synthetic RED. Reuse/link historical parent proof only as provenance and capture fresh GREEN for the completed boundary characterization.

**Test file:** `quiz/validate-quiz.test.js`  
**Framework:** Node built-in `node:test` and `node:assert/strict`.  
**Run command:** `node --test quiz/validate-quiz.test.js`  
**Edit hint:** Extend the existing aggregate bias characterization test.

| Test case | Historical RED | Fresh GREEN |
|---|---|---|
| Longest-answer aggregate equality and crossing | Not applicable; do not manufacture against current behavior | Equality omits that aggregate advisory; crossing emits its exact existing text |
| Much-longer aggregate equality and crossing | Not applicable; do not manufacture against current behavior | Equality omits that aggregate advisory; crossing emits its exact existing text |

Use historical parent proof `plans/checkpoints/task-b364dbad-44ba-4188-ab44-a38d38ee7433.red-green-proof.md` for provenance, and capture follow-up GREEN; if an implementation mismatch is found, use `tdd` for a genuine new correction cycle.

## Files

| File | Change |
|---|---|
| `quiz/validate-quiz.test.js` | Add missing exact aggregate equality/crossing characterization cases. |
| `quiz/validate-quiz.js` | Change only if characterization reveals a real mismatch with the established validator contract. |
| `plans/checkpoints/task-b364dbad-44ba-4188-ab44-a38d38ee7433.red-green-proof.md` | Link as historical provenance; do not rewrite. |

## Progress

- [x] Resolve canonical plan path and inspect original plan, current focused test, historical proof, and relevant learning.
- [x] Define omitted cutoff coverage and evidence approach.
- [ ] Add aggregate equality/crossing characterization, capture fresh GREEN, and run verification.
