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
- Create the required proof file before production edits and include `## RED Phase` immediately.
- After focused verification, append one `## GREEN Phase` with the exact commands or summarized output that proves the fixed behavior.
- Verify the proof file by searching for `^## (RED|GREEN) Phase$` before marking the checkpoint step complete.

## Gotcha

Concurrent or resumed sessions can duplicate `## GREEN Phase` sections if each session appends blindly. Before finalizing, read or grep the proof file and consolidate to exactly one RED section and one GREEN section when the checkpoint claims that invariant.

## Verification split

For dependency-free browser utilities, focused checks can cover most acceptance risk without a bundler:

```bash
node --check quiz/build-index.js
node --check quiz/app.js
node --test quiz/build-index.test.js
```

Pair that with exact equality between source level paths and generated manifest paths, plus browser assertions for manifest and selected JSON loading. Broader repository tests should still be run, but unrelated failures should be recorded rather than fixed during a quiz-only acceptance patch.
