# Plan 2026-05-18: Quiz Dashboard Acceptance Fix

Restore task scope boundaries for the accepted quiz UI tweak and add the missing proof artifact.

## Problem

Acceptance is blocked by unrelated quiz/KB content additions, one deleted original level JSON, and missing RED-GREEN proof for the already completed UI behavior.

## Analysis

### Kontext z codebase
- Keep existing accepted UI edits in `quiz/app.js`: `formatPoints()`, pre-answer `#question-points`, escaped `question.explanation` feedback, guarded browser startup, and existing `sameSelection` export.
- Keep existing accepted CSS edits in `quiz/style.css`: muted `--red`, toned-down `.answer-option.incorrect`, `#question-points`, and `.feedback-explanation`.
- Restore tracked deleted file `quiz/levels/futurecast-technologie-zitrka/ziskala-ai-vedomi-novy-model-desi-i-samotne-vedce.json` so there is no level rename.
- Remove untracked unrelated quiz content files under `quiz/levels/futurecast-technologie-zitrka/` that split or add levels for another video.
- Remove untracked unrelated KB directory `local-knowledge-base/youtube/futurecast-technologie-zitrka/2026-05-18_fotonicke-cipy-prichazi-konec-klasickych-procesoru/`.

### Relevantní dokumentace
- `plans/2026-05-18-2_quiz-dashboard-ui-tweaks.md`: original scope allows only quiz screen UI tweaks and explicitly forbids server API, scoring logic, level select, and file-structure changes.
- `docs/proposals/proposal-20260518-yt-knowledge-quiz.md`: quiz app is standalone vanilla HTML/JS/CSS; one JSON file per level; scoring stays localStorage/client-side.
- No PlantUML diagrams found for this area.

### Knowledge base
- `learnings/tooling/plan-acceptance-fixes-from-live-worktree-evidence.md`: plan acceptance fixes from the original plan plus live `git status`; name proof artifacts explicitly as the only allowed out-of-scope files.
- `learnings/tooling/acceptance-fix-proof-artifacts.md`: create `plans/checkpoints/<task-id>.red-green-proof.md` with one RED phase and one GREEN phase; keep production edits inside requested scope.
- `learnings/architecture/quiz-feedback-escape-json-content.md`: keep JSON-backed feedback text escaped before inserting explanation markup via `innerHTML`.
- `learnings/architecture/self-contained-quiz-dashboard-without-dependencies.md`: use lightweight `node --check` verification for the dependency-free quiz app.

## Available Skills
- `tdd`: use only for the proof-file workflow if implementation chooses to produce RED/GREEN evidence before cleanup.
- `save-learning`: run after implementation and verification as the last action required by the task prompt.

## Solutions
- Preserve completed UI changes; do not touch `quiz/server.js`, level select rendering, scoring functions, or API routes.
- Treat `plans/checkpoints/dark-vale-9814.red-green-proof.md` as the only new out-of-scope artifact allowed by acceptance cleanup.
- Use targeted file cleanup instead of broad resets so unrelated user/agent work is not reverted.

## Implementation

1. Inspect `git status --short` and confirm the current unrelated paths still match this plan before editing.
2. Restore the deleted original level file from `HEAD`: `quiz/levels/futurecast-technologie-zitrka/ziskala-ai-vedomi-novy-model-desi-i-samotne-vedce.json`.
3. Delete only `quiz/levels/futurecast-technologie-zitrka/fotonicke-cipy-prichazi-konec-klasickych-procesoru-easy.json`.
4. Delete only `quiz/levels/futurecast-technologie-zitrka/fotonicke-cipy-prichazi-konec-klasickych-procesoru-hard.json`.
5. Delete only `quiz/levels/futurecast-technologie-zitrka/ziskala-ai-vedomi-novy-model-desi-i-samotne-vedce-easy.json`.
6. Delete only `quiz/levels/futurecast-technologie-zitrka/ziskala-ai-vedomi-novy-model-desi-i-samotne-vedce-hard.json`.
7. Delete only `local-knowledge-base/youtube/futurecast-technologie-zitrka/2026-05-18_fotonicke-cipy-prichazi-konec-klasickych-procesoru/`.
8. Create `plans/checkpoints/dark-vale-9814.red-green-proof.md` with `## RED Phase` recording acceptance failure state before cleanup: unrelated quiz/KB files present, original level file deleted, proof file absent.
9. Add `## GREEN Phase` to `plans/checkpoints/dark-vale-9814.red-green-proof.md` recording focused verification after cleanup: no unrelated quiz/KB additions in `git status --short`, original level file present, `node --check app.js`, `node --check server.js` pass from `quiz/`.
10. Re-run `git status --short`; verify remaining product changes are limited to `quiz/app.js`, `quiz/style.css`, restored level file status cleared, and the proof/learning artifacts required by workflow.
11. Run `node --check app.js` and `node --check server.js` from `quiz/`.
12. Run `save-learning` as the final implementation action and save at least one learning if the cleanup reveals a reusable gotcha.

## Files to Modify

| Soubor | Změna |
|--------|-------|
| `quiz/levels/futurecast-technologie-zitrka/ziskala-ai-vedomi-novy-model-desi-i-samotne-vedce.json` | Restore original tracked level file so no rename remains. |
| `quiz/levels/futurecast-technologie-zitrka/*-easy.json` | Delete unrelated new split level files listed above. |
| `quiz/levels/futurecast-technologie-zitrka/*-hard.json` | Delete unrelated new split level files listed above. |
| `local-knowledge-base/youtube/futurecast-technologie-zitrka/2026-05-18_fotonicke-cipy-prichazi-konec-klasickych-procesoru/` | Delete unrelated new KB content directory. |
| `plans/checkpoints/dark-vale-9814.red-green-proof.md` | Add RED/GREEN evidence for accepted UI behavior and scope cleanup. |

## TDD: skip

Skip adding a new automated test file because the remaining product work is scope cleanup/restoring file structure, and the prompt allows satisfying the missing TDD item by adding `plans/checkpoints/dark-vale-9814.red-green-proof.md` evidence without changing quiz app file structure.

## Dependencies

- Do not edit `quiz/server.js`, `quiz/index.html`, API endpoint behavior, scoring logic, or level select UI.
- Do not remove or rewrite accepted changes in `quiz/app.js` and `quiz/style.css` unless verification shows they were accidentally altered.
- Treat unrelated repository-wide test failures as out of scope; record them only if encountered during optional broader checks.

---
*Vytvořeno: 2026-05-18*
*Status: DRAFT*
