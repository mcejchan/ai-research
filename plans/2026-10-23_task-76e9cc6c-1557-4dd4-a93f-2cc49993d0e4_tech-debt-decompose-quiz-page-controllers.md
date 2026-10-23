# Plan 2026-10-23: Decompose quiz page controllers

Characterize existing browser behavior, then split the quiz page controllers into cohesive, testable quiz-domain units without changing the static browser contract.

## Analysis

### Codebase
- `quiz/app.js` owns score persistence, escaping, URL validation, levels rendering/filtering, quiz state, answer evaluation and result rendering; the two page initializers exceed the configured length thresholds.
- `quiz/index.html`, `quiz/quiz.html`, and `quiz/style.css` define existing IDs, classes and presentation contracts to preserve.
- `quiz/build-index.test.js` and `quiz/publication-check.test.js` use Node's built-in test runner. `Makefile` defines `make test` and a quiz publication gate; there is no quiz DOM flow test yet.
- Keep browser auto-start selected by `document.body.dataset.page`, existing CommonJS exports `sameSelection` and `levelUrl`, relative static fetch paths, and no new runtime/build dependency.

### Relevant docs
- No quiz PlantUML diagram or API specification was found. HTML contracts are in `quiz/index.html` and `quiz/quiz.html`.

### Knowledge base
- Keep the static quiz dependency-free; guarded DOM startup and minimal CommonJS exports permit Node tests (`learnings/architecture/self-contained-quiz-dashboard-without-dependencies.md`, `learnings/tooling/testable-vanilla-browser-helpers-for-acceptance-evidence.md`, `learnings/patterns/cool-cove-5127-guard-browser-startup-to-make-vanilla-helpers-testable-in-node.md`).
- Continue rejecting unsafe level paths and HTML-escape all JSON-backed values inserted through `innerHTML` (`learnings/architecture/dark-vale-9814-escape-json-backed-quiz-feedback-before-using-innerhtml.md`).

## Approach

Add characterization coverage before production changes. Use a lightweight DOM harness only if supported by existing dependencies; otherwise extract pure rendering/state units and test those plus the public wiring boundary, explicitly documenting any uncovered browser-flow limitation. Decompose into quiz-domain-qualified modules or factories; retain the single static script-compatible runtime and avoid generic module names or bundlers.

## Implementation

1. Inspect existing Node test/dependency support and establish focused baseline behavior for levels and quiz flows before refactoring.
2. Cover index success, filtering, count/empty states, cards/badges, fetch failure; missing/invalid paths and empty questions; single/multi-select, no-selection, scoring/progress, next/final flow and best-score persistence.
3. Cover escaping of external level/question/option/explanation values and `levelUrl` traversal/scheme rejection; retain existing assertions in build-index and publication checks.
4. Extract cohesive level rendering/filter/event wiring and quiz session state/evaluation/rendering/event wiring units. Keep initializers as short orchestration boundaries and preserve all existing text, DOM contracts, storage key/schema, fetch paths, answer marking and security behavior.
5. Verify both initializer lengths are below configured warning thresholds; record measured lengths and exact commands/results in the implementation final note.

## Testing

- Run the focused new quiz controller/render/state tests.
- Run `node --test quiz/build-index.test.js quiz/publication-check.test.js`.
- Run `make test` as the configured repository gate, including the quiz publication check.
- Run `node --check` on changed quiz JavaScript. Perform a static-browser smoke only if existing repository tooling supports it; add no deployment/publication step.

## TDD

**Target test file:** `quiz/app.test.js` (or the existing test convention if inspection establishes a better location).
**Framework:** `node:test` and `node:assert/strict`, matching existing quiz tests; use only an already-present DOM facility.
**Focused command:** `node --test quiz/app.test.js`.
**First RED:** Add tests that fail against the current unexported/controller-bound flows, then expose minimal testable boundaries or fixtures while preserving browser startup. Use the agreed DOM harness when available; if not, test extracted pure render/state functions and public wiring and document DOM-flow limitations.

| Characterization | RED expectation | GREEN expectation |
|---|---|---|
| Levels render/filter/error | Controller behavior is not independently exercisable through current exports | Counts, empty state, cards/badges/filter and offline state match current contracts |
| Quiz evaluation and transitions | Session behavior is not independently exercisable through current exports | Single/multi-select, no-selection, progress, next/final results and best-score-only persistence match current behavior |
| Escaping and URL validation | External values/path edge cases lack controller-level assertions | Rendered values are escaped and invalid traversal/scheme paths are rejected |

Implement genuine RED/GREEN cycles using `skill:tdd`; retain baseline evidence and do not weaken existing assertions.

## Files

| File | Planned change |
|---|---|
| `quiz/app.js` | Keep page auto-init and compatibility exports; delegate to extracted domain units. |
| `quiz/quiz-levels-page.js` (candidate) | Levels page render, filtering, fetch/error behavior and event wiring, if extraction needs a separate file. |
| `quiz/quiz-session-controller.js` (candidate) | Quiz session state, evaluation, transitions, persistence/render delegation, if extraction needs a separate file. |
| `quiz/app.test.js` (candidate) | Focused characterization for levels and quiz flows with Node built-ins and existing test facilities. |

## Progress

- [x] Read task, inspected source/tests/HTML and relevant repository learnings.
- [x] Resolved the required canonical plan path and saved this plan there.
- [ ] Implement characterization tests and decomposition (future implementation task).
- [ ] Run verification and record resulting initializer lengths (future implementation task).
