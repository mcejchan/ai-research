# Tech debt: decompose quiz level validation stages

## Assessment

**Decision: create**

Current source inspection confirms finding `f0008` remains present: `validateLevelData` starts at `quiz/validate-quiz.js:13` and spans 132 lines. It combines top-level schema checks, per-question structural validation, correct-answer/type consistency, explanation advisories, answer-length and positional statistics, aggregate bias thresholds, and final result construction.

The validator is a public repository-local contract: `quiz/build-index.js:59` calls `validateLevelData`, and `quiz/validate-quiz.js` exports it alongside the CLI functions. Current search found no focused validator tests, so its exact errors, advisories, statistics and early-return behavior need characterization before decomposition.

Current pipeline state was inspected before registration. The only unfinished `ai-research` owner is the quiz page-controller refactor for `quiz/app.js`. It does not own `quiz/validate-quiz.js` or `quiz/build-index.js`. The scopes are related by feature but not overlapping in source or behavior; supported sequential registration in the current project lane is appropriate, and there is no exact owner to reuse.

Finding evidence: fingerprint `8832795b0450dd09bcf303b2cb1394058fbfe9e4e5f039431acafccd5fef4c80`, `function_lines=132` at line 13, critical, first seen 2026-09-26.

## Goal

Reduce `validateLevelData` below the critical and warning function-length thresholds by separating top-level validation, per-question structural analysis, per-question statistical analysis, and aggregate bias advisory generation while preserving its public API and exact validation semantics.

## Characterization-first guardrail

Before changing production structure, add focused tests that pin representative outcomes and exact diagnostics for:

- non-object input, missing title, and missing/empty/invalid questions;
- invalid question object/text/type/points/options/correct indices;
- duplicate and out-of-range correct indices plus single/multi type consistency;
- missing explanations and type-mismatch advisories/stat counters;
- correct-answer length, positional frequency, and aggregate bias thresholds at and across boundaries;
- malformed questions that must not enter statistical analysis;
- returned `file`, `ok`, `structuralErrors`, `advisories`, and complete `stats` shape;
- `build-index.js` compatibility with the validator result.

Do not rewrite expected messages merely to make extraction easier.

## Implementation scope

- Keep `validateLevelData(data, file = '<level>')` exported with the same signature and result shape.
- Extract cohesive quiz-validation helpers within `quiz/validate-quiz.js` unless a separate domain-qualified module provides a clear boundary. Do not introduce generic filenames such as `validation.js`, `schema.js`, `helpers.js`, `utils.js`, or `common.js`.
- Preserve the order and exact text of structural errors and advisories.
- Preserve early-return behavior for invalid level objects and invalid/empty question arrays.
- Preserve all `THRESHOLDS`, comparison operators, ratios, denominator choices, counters, and the condition that aggregate bias analysis runs only with enough questions and zero structural errors.
- Preserve permissive/advisory distinctions; do not turn advisories into failures or relax structural failures.
- Preserve CLI, `validateLevel`, `formatResult`, `levelFiles`, `main`, and `build-index.js` behavior.
- Avoid unrelated quiz UI, content, formatting, or publication changes.

## Acceptance criteria

- `validateLevelData` is below the configured function-length warning threshold.
- Extracted helpers have explicit quiz-validation responsibilities and avoid hidden shared mutable state beyond a clearly scoped validation context.
- Existing exports, caller contracts, result shape, diagnostic ordering/text, statistics and thresholds remain compatible.
- Focused characterization covers the cases above and remains green after refactoring.
- `quiz/build-index.js` and validator CLI tests remain green without weakened assertions.
- No generic module names or unrelated source churn are introduced.
- Final note records the resulting function length and exact verification commands/results.

## Verification

- Run the new focused `validateLevelData` tests.
- Run `quiz/build-index.test.js` and any validator/publication tests.
- Run the repository's configured JavaScript test/lint gate applicable to quiz tooling.
- Exercise the CLI against temporary valid and invalid level fixtures; do not modify real level content.

## Scope boundary

Work only within `/Users/michal/Projects/ai-research`. Do not edit real quiz level content, other repositories, OpenClaw configuration, runtime services, task state, or deployment/publication hooks. Use temporary or checked-in test fixtures only; record a blocker instead of crossing this boundary.
