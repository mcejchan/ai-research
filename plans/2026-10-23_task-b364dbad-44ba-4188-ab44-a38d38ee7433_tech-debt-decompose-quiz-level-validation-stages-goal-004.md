# Plan 2026-10-23: Characterize quiz validator compatibility gaps

Extend focused tests around the existing validator contract, then capture canonical verification and exact CLI evidence for the acceptance follow-up.

## Analysis

- `quiz/validate-quiz.js` already contains the decomposition; this follow-up should preserve it and add coverage only for omitted cases.
- `quiz/validate-quiz.test.js` currently has five tests and uses Node's built-in `node:test`.
- Validation details to pin: ordered structural diagnostics, advisory-only consistency findings, option statistics, aggregate thresholds, and aggregate bias suppression when any structural error exists.
- Existing integration tests in `quiz/build-index.test.js` and `quiz/publication-check.test.js` cover publication rejection and advisory-vs-failure behavior; preserve their assertions.
- Relevant learning `learnings/architecture/2026-10-23_characterization-first-quiz-validator-decomposition.md`: pin complete results, early returns, malformed-input behavior, threshold boundaries, and the distinction between structural errors and advisories.
- Relevant learning `learnings/architecture/quiz-validator-structural-errors-and-option-statistics.md`: duplicate in-range correct indices still contribute individually to statistics; structural errors suppress aggregate bias advisories only.
- No validator-specific diagram is needed for test-only characterization.

## Approach

- Append focused tests to the existing validator suite using fixture builders and exact result assertions where diagnostics or stats are contractual.
- Include independent invalid type, invalid points variants, invalid options, non-integer/out-of-range correct indices, single/multi consistency, and threshold tests at and across the established aggregate cutoffs.
- Pin structural-error gating of aggregate advisories while confirming per-question diagnostics/statistics still behave as before.
- Preserve duplicate-index statistics semantics; do not recreate or claim a fabricated RED against already-refactored production code. Link the genuine historical RED/GREEN proof from the parent task and capture fresh GREEN for this follow-up.
- Keep `build-index` and validator CLI checks unweakened; obtain canonical Test Gate evidence for the prescribed checks and record each exact command/result, fixture invocation, and `validateLevelData` line count in the final task note.

## Implementation

1. Add focused cases in `quiz/validate-quiz.test.js`, asserting exact diagnostics, advisories, stats, `ok`, and boundary outcomes.
2. Run the new focused tests. For each newly specified case, compare against the established validator behavior before altering expectations; do not change production behavior absent a demonstrated mismatch.
3. Run unchanged build-index and publication/validator CLI checks through the canonical Test Gate and preserve its raw evidence.
4. Run the project verification gate and capture command plus result for each run; exercise valid and invalid temporary CLI fixtures with exact invocations and exit/output results.
5. Record the final `validateLevelData` line count and link the parent genuine TDD artifact in the follow-up evidence; do not fabricate a post-implementation RED.

## Testing

- Focused: `node --test quiz/validate-quiz.test.js`
- Integration: `node --test quiz/build-index.test.js quiz/publication-check.test.js`
- CLI: `node quiz/validate-quiz.js <temporary-valid-fixture>` and `node quiz/validate-quiz.js <temporary-invalid-fixture>`; capture exact output and exit codes.
- Canonical project gate: `make test`.
- Obtain caller-owned Test Gate evidence specifically covering build-index and validator CLI checks, without changing or weakening assertions.
- Record the exact command/result for every verification in the final task note.

## TDD

This follow-up adds testable characterization. Add tests before any production change and capture fresh GREEN. Since the refactor already exists, reuse historical genuine RED/GREEN evidence from `plans/checkpoints/task-5da65213-e708-4892-a7c1-6f3a89105dc4.red-green-proof.md`; do not manufacture a failing RED against current production code.

**Test file:** `quiz/validate-quiz.test.js`  
**Framework:** Node built-in `node:test` and `node:assert/strict`.  
**Run command:** `node --test quiz/validate-quiz.test.js`  
**Edit hint:** Append focused test cases alongside existing validator contract tests.

```js
const assert = require('node:assert/strict');
const test = require('node:test');
const { validateLevelData } = require('./validate-quiz');

test('invalid type and points produce ordered structural diagnostics', () => {
  const result = validateLevelData({ title: 'Fixture', questions: [{
    question: 'Q?', type: 'unknown', points: 0, options: ['A', 'B'], correct: [0], explanation: 'why',
  }] });
  assert.deepEqual(result.structuralErrors, [
    'Q1: "type" must be "single" or "multi"',
    'Q1: "points" must be a finite number from 1 to 4',
  ]);
});

test('aggregate advisories are absent at the strict ratio boundaries', () => {
  // Construct fixtures at the established strict thresholds and pin exact advisories.
  assert.deepEqual(validateLevelData(levelAtAggregateBoundaries()).advisories, []);
});
```

| Characterization | Expected current-contract result |
|---|---|
| Invalid type and points | Exact ordered structural diagnostics; `ok` false |
| Invalid options and correct indices | Exact diagnostics; invalid/non-analyzable inputs do not corrupt option statistics |
| Single/multi consistency | Single cardinality is structural; multi with one correct answer is advisory and increments `typeMismatch` |
| Aggregate strict boundaries | No advisory at equality; crossing the relevant threshold emits the exact existing diagnostic |
| Structural-error gating | Any structural error suppresses aggregate bias advisories; retains per-question advisories/statistics allowed by current contract |

Implement any production correction only if a characterization test proves a contract mismatch; use `tdd` skill for such a correction, otherwise retain characterization-only scope and historical proof provenance.

## Files

- `quiz/validate-quiz.test.js` — add omitted structural, advisory, statistics, aggregate-boundary, and structural-gating characterization.
- `quiz/build-index.test.js` and `quiz/publication-check.test.js` — verify existing assertions remain unchanged and green; modify only if a narrowly necessary compatibility assertion is missing.
- `plans/checkpoints/task-5da65213-e708-4892-a7c1-6f3a89105dc4.red-green-proof.md` — historical evidence to link, not rewrite or fabricate.
- Final task note — exact verification commands/results, CLI fixture outcomes, function length, and canonical Test Gate evidence.

## Progress

- [x] Resolve the required canonical plan path.
- [x] Inspect original plan, validator implementation, current focused/integration tests, and relevant learnings.
- [x] Define acceptance-focused coverage and evidence requirements.
- [ ] Implement characterization and obtain fresh GREEN plus canonical Test Gate evidence.
