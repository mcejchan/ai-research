# Plan 2026-05-18: wild-vale-3770 Proof Artifact Fix

Create the missing task-specific RED/GREEN proof document for the already accepted quiz UI work and keep all product code untouched.

## Problem

Acceptance is blocked because `plans/checkpoints/wild-crag-7582.red-green-proof.md` is missing/incorrect while the prior cleanup and quiz UI changes are already complete.

## Analysis

### Kontext z codebase
- `plans/2026-05-18_wild-crag-7582_quiz-dashboard-ui-tweaks-do-not-change-server-api-scoring.md` names the completed UI cleanup and the earlier wrong proof target `dark-vale-9814`.
- `plans/checkpoints/wild-crag-7582.checkpoint.md` says the implementation is complete but only references verification and learning, not the required `wild-crag-7582.red-green-proof.md` artifact.
- `plans/checkpoints/wild-crag-7582.red-green-proof.md` is the only primary file to create/update for this acceptance fix.
- `youtube-transcript-pipeline/test/test_llm_client.py` failures are suite-wide cleanup only; record separately if investigated, do not block the proof artifact.

### Relevantní dokumentace
- Original plan: `plans/2026-05-18_wild-crag-7582_quiz-dashboard-ui-tweaks-do-not-change-server-api-scoring.md`.
- Checkpoint: `plans/checkpoints/wild-crag-7582.checkpoint.md`.

### Knowledge base
- `learnings/tooling/acceptance-fix-proof-artifacts.md`: create `plans/checkpoints/<task-id>.red-green-proof.md`, include exactly one `## RED Phase` and one `## GREEN Phase`, and verify those headings before marking complete.
- `learnings/tooling/wild-crag-7582-acceptance-fixes-keep-corrective-diffs-scoped.md`: do not redo accepted UI behavior; make the smallest corrective diff; do not fabricate RED evidence after the fact.

## Available Skills
- `tdd`: use only as workflow guidance for proof-file structure if the implementer needs the RED/GREEN evidence format.
- `save-learning`: mandatory final implementation action after the proof artifact is written and verified.

## Solutions

- Create/update `plans/checkpoints/wild-crag-7582.red-green-proof.md` for the original task ID, not `dark-vale-9814` or `wild-vale-3770`.
- Make the RED phase truthful for this acceptance-fix state: required `wild-crag-7582` proof artifact missing/incorrect and acceptance monitor reported P1.
- Make the GREEN phase truthful after the fix: artifact exists, has exactly one `## RED Phase` and one `## GREEN Phase`, and no app/API/scoring/level file changes were needed.

## Implementation

1. Inspect `git status --short` and `plans/checkpoints/` only to confirm current proof/checkpoint state; do not modify product files.
2. Read any existing `plans/checkpoints/wild-crag-7582.red-green-proof.md`; if it exists, preserve truthful useful evidence and consolidate to exactly one RED section and one GREEN section.
3. Write `plans/checkpoints/wild-crag-7582.red-green-proof.md` with:
   - `# RED-GREEN Proof: wild-crag-7582`
   - `## RED Phase` documenting the failed acceptance condition: missing/wrong task proof artifact and lack of RED/GREEN phases for `wild-crag-7582`.
   - `## GREEN Phase` documenting the fixed condition: correct file path, correct task ID, exactly one RED heading, exactly one GREEN heading, and no quiz/server/scoring/level-select changes.
4. Verify headings with a targeted search for `^## (RED|GREEN) Phase$` in `plans/checkpoints/wild-crag-7582.red-green-proof.md`.
5. Verify scope with `git status --short`; expected primary change is the proof artifact plus any mandatory learning file generated at the end.
6. Run focused syntax checks only if product files changed unexpectedly; otherwise record that no product verification was needed because this is documentation-only.
7. For P2 cleanup, optionally run `DRIVE_FOLDER_ID=test-folder python3 -m pytest youtube-transcript-pipeline/test/test_llm_client.py` and record results separately without changing this acceptance fix.
8. Run `save-learning` as the final action and save one concise learning about task-specific proof artifacts when acceptance fixes are documentation-only.

## Files to Modify

| Soubor | Změna |
|--------|-------|
| `plans/checkpoints/wild-crag-7582.red-green-proof.md` | Create/update truthful RED/GREEN proof for original task `wild-crag-7582`. |
| `learnings/tooling/<new-learning>.md` | Add mandatory learning from the implementation session via `save-learning`. |

## TDD: skip

Skip automated TDD because the remaining primary output is a proof document; the required verification is the RED/GREEN artifact itself plus heading/scope checks.

## Dependencies

- Do not edit `quiz/app.js`, `quiz/style.css`, `quiz/server.js`, quiz level JSON, scoring logic, server API, level select screen, or file structure.
- Do not rewrite the completed original implementation or previous cleanup commits.
- Do not treat existing `test_llm_client.py` failures as blocking this proof-artifact acceptance fix.

---
*Vytvořeno: 2026-05-18*
*Status: DRAFT*
