# Plan 2026-10-23: Finish quiz page controller decomposition

Complete the existing partial refactor by wiring the quiz session unit into production, characterizing controller flows, and recording exact verification evidence.

## Analysis

- Existing work in `quiz/quiz-page-logic.js` already extracts levels helpers plus `evaluateAnswer` and `createQuizSession`; preserve it rather than redo it.
- `quiz/app.js:initQuizPage` remains 157 source lines (lines 107–263), with session logic, DOM rendering and async setup intertwined. `initLevelsPage` is already 28 lines.
- `quiz/app.test.js` currently tests pure helpers only; missing levels fetch failure, invalid/missing level, empty questions, answer marking, UI transitions, result rendering and production wiring.
- Preserve guarded browser startup, static script ordering in both HTML pages, CommonJS `sameSelection`/`levelUrl`, storage schema, text, escaping, and path validation.
- Relevant learning: `learnings/architecture/testable-logic-for-static-quiz-pages.md` requires browser global export and loading domain script before `app.js`.

## Approach

Extend the existing quiz-domain module into the production session/evaluation boundary, with DOM operations injected or handled by cohesive quiz-page functions. Keep `initQuizPage` as short orchestration and route actual submit/advance/results behavior through the session unit. Add focused DOM-capable characterization where existing dependencies permit; otherwise test extracted pure units and an explicit production wiring seam.

## Implementation

1. Inspect current diff, configured initializer warning threshold, HTML script contracts and available test dependencies; preserve already completed levels extraction and existing assertions.
2. Add missing characterization for levels fetch failure; missing/invalid level and empty questions; incorrect/correct answer marking and disabled inputs; submit/next visibility; final result and best-score rendering; and proof that production initialization uses the extracted session/evaluation unit.
3. Refactor quiz initialization into orchestration and named quiz-domain units; ensure `createQuizSession` and `evaluateAnswer` are used by the production path, not only exported for tests.
4. Keep browser and Node entry behavior compatible; update HTML only if a new browser-loaded script is required, loading it before `app.js` on both pages.
5. Measure both initializer lengths against the repository threshold and record exact commands, outcomes, and lengths in the implementation final note. Reuse historical genuine RED evidence; capture fresh GREEN evidence without fabricating a new RED.

## Testing

- Focused: `node --test quiz/app.test.js`.
- Existing quiz regressions: `node --test quiz/build-index.test.js quiz/publication-check.test.js`.
- Repository gate: `make test`.
- Syntax-check each changed JavaScript file with `node --check`.
- Retain all existing assertions; report measured `initLevelsPage` and `initQuizPage` line counts and exact verification results.

## TDD

Use `skill:tdd` for fresh characterization additions and GREEN verification. Link the genuine historical RED in `plans/checkpoints/task-76e9cc6c-1557-4dd4-a93f-2cc49993d0e4.red-green-proof.md`; do not claim that the current already-passing helper tests are fresh RED evidence.

**Target test file:** `quiz/app.test.js`  
**Framework:** Node built-in `node:test` and `node:assert/strict`.  
**Run command:** `node --test quiz/app.test.js`.

```js
const assert = require('node:assert/strict');
const test = require('node:test');
const { createQuizSession } = require('./quiz-page-logic');
const { initQuizPage } = require('./app');

test('production quiz initialization delegates answer evaluation to session logic', () => {
  assert.equal(typeof initQuizPage, 'function');
  // RED: initializer is currently private; expose only the smallest test seam or verify via injected session factory.
});

test('session rejects empty answers without marking question answered', () => {
  const session = createQuizSession({ levelPath: 'x.json', questions: [{ points: 1, correct: [0], options: ['yes'] }], saveScore: () => ({ best: 0, max: 1 }) });
  assert.equal(session.submit([]).message, 'Vyber alespoň jednu odpověď.');
  assert.equal(session.submit([0]).correct, true);
});
```

| Test | RED | GREEN |
|---|---|---|
| Public production wiring seam | Current initializer is not independently inspectable/delegation boundary is unverified | Test demonstrates initializer reaches the extracted session/evaluation behavior through a minimal seam or DOM harness |
| Expanded page-flow characterization | Listed async and DOM transitions are not covered | Error, marking, visibility, result, and persistence contracts pass |

## Files

| File | Planned change |
|---|---|
| `quiz/app.js` | Reduce initializer to orchestration; wire extracted quiz session/evaluation units into real page flow; preserve compatibility exports and startup guard. |
| `quiz/quiz-page-logic.js` | Refine cohesive session/domain API only as needed by production wiring. |
| `quiz/app.test.js` | Add focused characterization for uncovered levels/quiz flows and production wiring. |
| `quiz/quiz.html`, `quiz/index.html` | Touch only if browser loading order needs adjustment for a new domain script. |

## Progress

- [x] Canonical plan path resolved; parent plan and partial checkpoint reviewed.
- [x] Existing implementation and tests inspected; completed levels extraction identified for preservation.
- [ ] Implement missing characterization and wire quiz session into production.
- [ ] Verify configured lengths and all exact commands; record final evidence.
