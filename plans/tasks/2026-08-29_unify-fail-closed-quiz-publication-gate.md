# Unify quiz publication behind one fail-closed gate

## Type

Implementation

## Context

Architecture review `/Users/michal/Projects/ai-research/.architecture-reviews/reports/2026-08-29T080000Z-ai-research.md` found three divergent acceptance mechanisms in the quiz publication path:

- `quiz/build-index.test.js` checks only index metadata behavior.
- `quiz/build-index.js` catches malformed level reads/JSON and silently omits them from the generated catalog.
- `quiz/validate-quiz.js` contains schema/quality validation but is invoked by neither the root gate nor Pages.

The root `make test` and `.github/workflows/deploy-quiz.yml` therefore do not prove that every tracked quiz level is structurally valid and included. A malformed level can yield a green deployment with a partial catalog.

## Objective

Create one repository-owned, fail-closed quiz publication check and make both the authoritative root gate and GitHub Pages use it. Preserve the useful separation between blocking structural integrity and advisory content-quality/bias heuristics.

## Requirements

1. Add one explicit quiz publication command or Make target that is the sole maintained publication contract.
2. The contract must:
   - parse and structurally validate every tracked source level;
   - fail non-zero on unreadable files, malformed JSON, schema errors, or any level that cannot be included;
   - build the index without swallowing or silently skipping invalid inputs;
   - verify the static quiz runtime/index integration with the focused runtime test.
3. Reuse or consolidate the existing builder, builder tests, and validator rather than introducing a fourth independent validation implementation.
4. Separate blocking structural/schema validation from advisory quality/bias heuristics. Advisory findings may warn, but must not accidentally become deployment blockers unless already part of the documented publication contract.
5. Make root `make test` invoke the shared quiz publication check.
6. Make `.github/workflows/deploy-quiz.yml` invoke that same shared command/target rather than spelling out its own builder/test sequence.
7. Keep Pages scoped to quiz publication. Do not make it depend on unrelated Python pipeline or viewer tests.
8. Preserve current generated index semantics for valid levels.

## Characterization-first guardrail

Before changing production behavior, add focused characterization/negative tests proving the current risk and desired contract, including at least:

- malformed JSON causes the publication check to fail;
- structurally invalid level data causes it to fail;
- no invalid level is silently omitted while the command succeeds;
- valid levels still produce the expected index and static runtime behavior;
- advisory-only quality/bias findings do not fail publication.

Use temporary fixtures or isolated test directories; tests must not mutate tracked quiz data or leave generated artifacts behind.

## Acceptance criteria

- There is one named quiz publication gate used by both root `make test` and Pages.
- A malformed or schema-invalid tracked level makes that gate and the Pages build step fail non-zero.
- Index generation cannot report success after silently excluding an invalid source level.
- The existing static runtime/index behavior remains covered and passing for valid input.
- Structural failures and advisory quality warnings have an explicit, tested distinction.
- Duplicate validation logic and dead/uninvoked validator paths are removed or reduced to thin shared components; no parallel source of truth remains.
- Workflow and repository documentation name the shared command as the publication contract where appropriate.
- Changes remain repository-local to `/Users/michal/Projects/ai-research`; do not inspect or modify other repositories or external OpenClaw configuration. Record any genuinely external dependency as a follow-up instead of crossing this boundary.

## Verification

Run from the ai-research repository root:

- focused quiz publication tests, including the new fail-closed cases;
- the shared quiz publication command directly;
- `make test`;
- a static inspection/test demonstrating that `.github/workflows/deploy-quiz.yml` calls the shared command and no longer duplicates the tolerant sequence.

Record exact commands, exit codes, and results in the final note. Do not add git, push, PR, or deployment operations to the implementation workflow.
