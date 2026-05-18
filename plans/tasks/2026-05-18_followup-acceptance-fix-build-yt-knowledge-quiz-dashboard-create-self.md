# [acceptance-fix] [acceptance-fix] Build YT Knowledge Quiz Dashboard: Create self-contained `quiz/` app with `server.js`, `index.html`, `quiz.html`, `: Export planned pure helpers from `quiz/app.js`

Auto-created by the monitor because the original task `cool-cove-5127` was accepted as done
but did not fully meet all acceptance goals.

## Primary goals (from original task)

- Export planned pure helpers from `quiz/app.js`
- Provide RED-GREEN proof for the task ID
- [P1] Planned scoring persistence helpers were not exported (`quiz/app.js`) -> Export `getScores` and `saveScore` alongside `sameSelection`, or update the proof with concrete evidence that localStorage persistence behavior is otherwise directly verified per the plan.
- [P1] RED phase does not show an actual failing test (`plans/checkpoints/cool-cove-5127.red-green-proof.md`) -> Add concrete RED evidence from a failing focused test/check created before the implementation, then the corresponding GREEN passing evidence.

## Additional cleanup (suite-wide)

- [P2] Repository pytest has unrelated failures (`youtube-transcript-pipeline/test/test_llm_client.py`) -> Investigate separately; these failures are outside the quiz-only acceptance fix scope.


## Context

- Original task: `cool-cove-5127`
- Reason: `acceptance_incomplete`
- The original task's code changes are preserved. Continue from that state.

## Instructions

Implement the remaining primary goals above first, then handle any listed cleanup items. The original implementation is committed —
build on it, do not revert or redo completed work.

## Important: do not repeat completed work

The previous attempt partially succeeded. Review what is already committed before making changes. Do NOT revert or redo completed work. If the previous approach caused the failure, try a different approach.

## Original plan

Read the original plan at `/Users/michal/Projects/ai-research/plans/2026-05-18_cool-cove-5127_build-yt-knowledge-quiz-dashboard-create-self-contained.md` for full context. Focus only on the unmet goals listed above.

## Previous attempt: acceptance context

**Why incomplete:** Core endpoint and scoring smoke evidence is present, and the diff stays within accepted scope. Acceptance is blocked because planned `getScores`/`saveScore` exports are not shown and the TDD proof does not demonstrate a concrete RED failing test before GREEN.


**Already done (do NOT redo):**
- Keep implementation within project scope and avoid `docs/proposals/...` changes
- Preserve self-contained `quiz/` app shape with dependency-free runtime
- Provide `/api/levels` and `/api/level?path=...` behavior with invalid path rejection
- Prove quiz scoring/all-or-nothing behavior
- Guard browser-only app bootstrapping for Node testability
- Run focused verification and broader repository tests

## Recent learnings from previous attempt


### acceptance-fix-proof-artifacts.md

```
---
title: "Acceptance fixes need proof artifacts independent from app scope"
date: 2026-05-18
category: tooling
component: tooling
tags: [acceptance-fix, tdd, checkpoint, verification]
file_type: checklist
---

# Acceptance fixes need proof artifacts independent from app scope

When an acceptance-fix task requires a self-contained app scope, mandatory workflow artifacts such as checkpoint and RED-GREEN proof files still need to be maintained even if the product changes must stay under the app directory.

## Pattern

- Keep production changes inside the requested scope, for example `quiz/`.
- 
```


### testable-vanilla-browser-helpers-for-acceptance-evidence.md

```
---
title: "Testable vanilla browser helpers for acceptance evidence"
date: 2026-05-18
category: tooling
component: frontend
tags: [vanilla-js, testing, acceptance, nodejs]
file_type: rules
---

# Testable vanilla browser helpers for acceptance evidence

When a task is constrained to a dependency-free browser app, focused acceptance evidence can still be produced without adding a test framework or build step.

## Pattern

Keep browser runtime behavior unchanged, but isolate small pure helpers and guard DOM startup:

```js
if (typeof document !== 'undefined') {
  // browser initialization
}

if
```

## Implementation session log excerpt (last 50 lines)

```
facts.md
?? learnings/tooling/testable-vanilla-browser-helpers-for-acceptance-evidence.md
?? plans/2026-05-18-2_quiz-dashboard-ui-tweaks.md
?? plans/tasks/2026-05-18_quiz-dashboard-ui-tweaks.md
[0m
Implemented/verified `cool-cove-5127`.

- Required proof exists: `plans/checkpoints/cool-cove-5127.red-green-proof.md`
- Proof contains both `## RED Phase` and `## GREEN Phase`
- Checkpoint is marked complete
- Save-learning skill was run and saved `learnings/tooling/acceptance-fix-proof-artifacts.md`

Verification:
- Focused quiz checks passed: `server.js`, `app.js`, scoring helper, `/`, `/api/levels`, `/api/level`, invalid path rejection
- Repository pytest run: `37 passed, 4 failed`
- The 4 failures are unrelated existing `test_llm_client.py` issues around OpenAI base URL/mock expectations.

```
