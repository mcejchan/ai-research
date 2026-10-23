# Tech debt: decompose quiz page controllers

## Assessment

**Decision: create**

Current source inspection confirms both findings remain present in `quiz/app.js`: `initLevelsPage` starts at line 69 and spans 62 lines, while `initQuizPage` starts at line 138 and spans 157 lines. These controllers mix DOM discovery, mutable page state, HTML rendering, event binding, fetch/error handling, score calculation/persistence, answer evaluation, progress transitions, and result rendering.

Existing automated coverage is narrow: `quiz/build-index.test.js` imports `levelUrl`, while no repository test directly characterizes the levels-page or quiz-page controller flows. The HTML contracts live in `quiz/index.html` and `quiz/quiz.html`. Because behavior drift would be easy in this UI code, characterization-first protection is required before decomposition.

Current task state was inspected before registration. There is no unfinished `ai-research` owner, including no queued work touching `quiz/app.js`, so there is no exact task to reuse and no current collision.

Finding evidence: primary `f0005` fingerprint `8f336ec63c4ef363f61592fa25a1d18d87b3b15ec381d4f378a44d399645bf6e` (`initLevelsPage`, 62 lines) with related critical `f0006` fingerprint `3db3b8e7d08fe59efd24a030b57263d9b059ad48338ab6d63ad1825257a8348e` (`initQuizPage`, 157 lines), both first seen 2026-09-26.

## Goal

Reduce both page initializers below the configured function-length thresholds by extracting cohesive rendering, state-transition, and event-wiring helpers while preserving the existing browser UX, persistence, security checks, and HTML contracts.

## Characterization-first guardrail

Before production refactoring, add focused DOM-level characterization for representative flows using the project's existing JavaScript test approach and no new heavy browser framework unless already available:

- levels index success, difficulty filtering, count/empty state, cards, badges and fetch failure;
- missing/invalid level path and empty-question failures;
- single- and multi-select answer evaluation, no-selection feedback, score/progress transitions, next/final transitions and persisted best score;
- escaping of externally supplied level/question/option/explanation fields and continued enforcement of `levelUrl` traversal/scheme rejection.

If the current test environment cannot support a DOM flow without a substantial new dependency, extract pure render/state helpers first and characterize those plus the public wiring boundary; record the remaining limitation explicitly rather than weakening acceptance.

## Implementation scope

- Keep current automatic page initialization based on `document.body.dataset.page`.
- Extract cohesive, domain-specific helpers or controller factories. New filenames, if any, must be quiz-domain qualified (for example `quiz-levels-page.js` or `quiz-session-controller.js`), not `state.js`, `ui.js`, `helpers.js`, `utils.js`, or `common.js`.
- Preserve all element IDs/classes and HTML structure relied on by `quiz/index.html`, `quiz/quiz.html`, and `quiz/style.css`.
- Preserve score storage key/schema and best-score-only update behavior.
- Preserve Czech user-facing messages, point formatting, difficulty labels, card URLs, thumbnail behavior, answer-option marking, result rows, and progress/status text.
- Preserve `levelUrl` validation and HTML escaping; do not introduce `innerHTML` use with unescaped external values.
- Preserve fetch paths and dry static-host compatibility; do not add a bundler or server dependency.
- Avoid unrelated visual redesign or quiz-content changes.

## Acceptance criteria

- `initLevelsPage` and `initQuizPage` are each below their configured warning threshold.
- Extracted units have explicit quiz-domain responsibilities and can be tested without reproducing controller internals.
- Existing public `sameSelection` and `levelUrl` CommonJS exports remain compatible; any additional exports are test-focused and minimal.
- Characterization tests cover the key flows above before/alongside the refactor and existing `quiz/build-index.test.js` remains green without weakened assertions.
- Browser behavior, localStorage schema, security validation, visible text and CSS/HTML contracts are preserved.
- No new generic modules or unrelated source churn are introduced.
- Final note records resulting function lengths and exact verification commands/results.

## Verification

- Run the new focused quiz controller/render/state tests.
- Run `quiz/build-index.test.js` and `quiz/publication-check.test.js`.
- Run the repository's configured JavaScript/Python test gate relevant to the quiz artifacts.
- Perform the smallest supported static-browser smoke if the repository already provides one; do not add deployment or live publication steps.

## Scope boundary

Work only within `/Users/michal/Projects/ai-research`. Do not edit generated knowledge content, other repositories, OpenClaw configuration, runtime services, task state, or deployment/publication hooks. Use local test fixtures only; record a blocker instead of crossing this boundary.
