# [acceptance-fix] Quiz Dashboard UI tweaks: Do not change server API, scoring logic, level select screen, or file structure

Auto-created by the monitor because the original task `dark-vale-9814` was accepted as done
but did not fully meet all acceptance goals.

## Primary goals (from original task)

- Do not change server API, scoring logic, level select screen, or file structure
- [P1] Out-of-scope quiz/content files were added and an existing level file was renamed (`quiz/levels/futurecast-technologie-zitrka/*`, `local-knowledge-base/youtube/futurecast-technologie-zitrka/*`) -> Keep the UI changes limited to the relevant quiz frontend files; remove unrelated new KB/quiz content files and avoid renaming existing level files unless explicitly requested.

## Additional cleanup (suite-wide)

- [P2] Missing TDD proof for testable code change (`plans/checkpoints/dark-vale-9814.red-green-proof.md`) -> Add a RED-GREEN proof file for the UI behavior or document an explicit TDD skip reason in the plan.


## Context

- Original task: `dark-vale-9814`
- Reason: `acceptance_incomplete`
- The original task's code changes are preserved. Continue from that state.

## Instructions

Implement the remaining primary goals above first, then handle any listed cleanup items. The original implementation is committed —
build on it, do not revert or redo completed work.

## Important: do not repeat completed work

The previous attempt partially succeeded. Review what is already committed before making changes. Do NOT revert or redo completed work. If the previous approach caused the failure, try a different approach.

## Original plan

Read the original plan at `/Users/michal/Projects/ai-research/plans/2026-05-18-2_quiz-dashboard-ui-tweaks.md` for full context. Focus only on the unmet goals listed above.

## Previous attempt: acceptance context

**Why incomplete:** The three requested UI behaviors appear implemented, including safe escaping for explanation content. Acceptance is blocked because the diff includes unrelated quiz/content additions and a level file rename despite the plan explicitly forbidding file-structure changes.


**Already done (do NOT redo):**
- Show question points before answering
- Use less aggressive red for wrong-answer feedback
- Show `explanation` after answering when present

## Recent learnings from previous attempt


### quiz-feedback-escape-json-content.md

```
---
title: "Quiz UI: escapovat JSON obsah ve feedbacku"
date: 2026-05-18
category: architecture
component: frontend
tags: [quiz, frontend, xss, vanilla-js, feedback]
---

# Quiz UI: zachovat data bezpečně při renderování feedbacku

V quiz dashboardu je feedback po odpovědi skládaný v klientském `app.js`. Pokud se k běžnému textu přidává volitelné HTML pro doplňující vysvětlení, je potřeba dál escapovat obsah z JSON dat.

## Praktický vzor

Text odpovědi i `question.explanation` nejdřív projdou přes existující `escapeHtml()` a teprve potom se vloží do `innerHTML` spolu s malým wrapperem pro sty
```


### cool-cove-5127-repository-wide-test-runs-can-expose-unrelated-environment-coupled-failures.md

```
---
title: "Repository-wide test runs can expose unrelated environment-coupled failures"
date: 2026-05-18
category: test-failures
component: backend
tags: [pytest, openai-client, environment-config, mocking, verification-scope]
---

The task-specific quiz verification passed, but a repository-wide `pytest` run still reported unrelated failures in `test_llm_client.py`. The failures were tied to assumptions about the OpenAI client setup: one test expected the old `OPENAI_BASE_URL` default, while another expected a mock shape that no longer matched the client call path. The reusable lesson is tha
```


### cool-cove-5127-use-a-non-reserved-shell-variable-for-command-exit-capture-in-zsh.md

```
---
title: "Use a non-reserved shell variable for command exit capture in zsh"
date: 2026-05-18
category: tooling
component: tooling
tags: [zsh, shell-script, exit-code, cleanup, verification]
---

A focused verification command failed after successful checks because it assigned to `status`, which is a read-only variable in `zsh`. Renaming the capture variable to something neutral like `rc` fixed the issue. When writing portable verification one-liners with background process cleanup, avoid shell-special names for temporary variables or the cleanup path can fail even after the main assertions 
```

## Implementation session log excerpt (last 50 lines)

```
es:
D tmp/dark-vale-9814-learning.md
Implemented the quiz UI tweaks.

Changed:
- `quiz/app.js`
  - Points chip now shows Czech wording like `1 bod`, `2 body`, `5 bodů` before answering.
  - Feedback now renders optional `question.explanation` after any answered question.
  - Explanation content is HTML-escaped before insertion.

- `quiz/style.css`
  - Wrong-answer red changed to muted `#cc4444`.
  - Incorrect answer border/shadow toned down.
  - Question points chip styled as subtle neon monospace accent.
  - Explanation styled as smaller muted italic text.

Verification:
- `node --check app.js`
- `node --check server.js`

Required learning saved:
- `learnings/architecture/quiz-feedback-escape-json-content.md`

Checkpoint marked complete:
- `plans/checkpoints/dark-vale-9814.checkpoint.md`

```
