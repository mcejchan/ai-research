# Plan 2026-10-23: Decompose quiz level validation stages

Characterize the public validator contract, then extract validation stages while preserving exact output semantics.

## Analysis

- `quiz/validate-quiz.js` exports `validateLevelData`, `validateLevel`, `formatResult`, and `main`; its 132-line target accumulates diagnostics, statistics, and bias advisories.
- `quiz/build-index.js` consumes `validateLevelData` and relies on structural errors and advisory separation. Existing integration coverage is in `quiz/build-index.test.js` and `quiz/publication-check.test.js`.
- Quiz tests use Node's built-in `node:test`; `Makefile` defines `make quiz-publication-check` and the project gate `make test`.
- Relevant learning: `learnings/architecture/2026-10-23_expose-quiz-page-logic-for-testing-without-a-browser.md` recommends keeping pure logic directly testable with Node's runner.
- No relevant PlantUML diagrams or validator-specific test file are present.

## Approach

- First add focused characterization in `quiz/validate-quiz.test.js`; retain exact current message text, diagnostic ordering, full stats shape, early returns, and thresholds.
- Then extract cohesive helpers in `quiz/validate-quiz.js` for result construction/top-level checks, per-question structural validation, per-question statistical analysis, and aggregate bias advisories. Pass a narrowly scoped validation context explicitly; avoid hidden mutable state and a generic module.
- Keep `validateLevelData(data, file = '<level>')` as the orchestrator and preserve all exports, callers, CLI behavior, and publication semantics.

## Implementation

1. Add characterization tests for invalid level inputs and early returns; question structure, duplicate/out-of-range correct indices, single/multi consistency, explanations, and invalid questions excluded from stats.
2. Add boundary tests for correct-answer length, positional frequency, minimum question count, aggregate bias ratios, and zero-structural-error gating; assert exact advisories, ordered structural errors, `file`, `ok`, and complete stats.
3. Add a `build-index.js` compatibility assertion for valid result consumption and advisory-vs-failure behavior without weakening existing tests.
4. Extract helpers by responsibility, preserving all threshold values, operators, denominators, counter updates, and diagnostic ordering; reduce `validateLevelData` below the configured warning threshold.
5. Run temporary-fixture CLI checks for valid and invalid levels, followed by focused and repository gates.

## Testing

- `node --test quiz/validate-quiz.test.js`
- `node --test quiz/build-index.test.js quiz/publication-check.test.js`
- Exercise `node quiz/validate-quiz.js <temporary-valid-or-invalid-fixture>`; create fixtures under OS temp storage and remove them afterward.
- `make test` (includes quiz publication checks and the project's configured broader test gate).
- Record `validateLevelData`'s resulting line count and exact verification commands/results in the implementation task's final note.

## TDD

Implement the characterization tests first and establish RED against current unpinned outcomes, then preserve GREEN through extraction using the `tdd` skill's RED/GREEN evidence workflow.

**Test file:** `quiz/validate-quiz.test.js` (new)
**Framework:** Node built-in `node:test` and `node:assert/strict`, matching existing quiz tests.
**Run command:** `node --test quiz/validate-quiz.test.js`
**Edit hint:** NEW FILE; import `validateLevelData` from `./validate-quiz`.

```js
const assert = require('node:assert/strict');
const test = require('node:test');
const { validateLevelData } = require('./validate-quiz');

test('invalid level object returns the stable complete result', () => {
  assert.deepEqual(validateLevelData(null, 'fixture.json'), {
    file: 'fixture.json',
    ok: false,
    structuralErrors: ['Level must be a JSON object'],
    advisories: [],
    stats: {
      total: 0,
      correctIsLongest: 0,
      correctIndexCounts: {},
      correctMuchLongerThanDistractors: 0,
      typeMismatch: 0,
      missingExplanation: 0,
    },
  });
});

test('a malformed question is excluded from option statistics', () => {
  const result = validateLevelData({ title: 'Fixture', questions: [null] });
  assert.equal(result.stats.total, 1);
  assert.equal(result.stats.correctIsLongest, 0);
  assert.deepEqual(result.stats.correctIndexCounts, {});
  assert.deepEqual(result.structuralErrors, ['Q1: question must be an object']);
});
```

| Test | RED | GREEN |
|---|---|---|
| Invalid level result | Fails if any result field, diagnostic, or stats key/value differs | Exact public result remains stable |
| Malformed question stats | Fails if malformed question contributes option-derived counters | `total` increments while option statistics remain empty |

Implement the RED/GREEN cycle using the `tdd` skill.

## Files

- `quiz/validate-quiz.test.js` — add focused contract and threshold-boundary characterization.
- `quiz/validate-quiz.js` — decompose validation stages without changing public API or semantics.
- `quiz/build-index.test.js` — only add a narrowly scoped compatibility assertion if existing publication coverage does not already pin the needed validator result contract.

## Progress

- [x] Resolve canonical plan path and inspect task-relevant code, tests, project gate, and learning.
- [x] Define characterization-first sequence, helper boundaries, and verification commands.
- [ ] Implementation and verification remain for the implementation task.
