---
title: "Acceptance fixes: keep corrective diffs scoped"
date: 2026-05-18
category: tooling
component: tooling
tags: [acceptance-fix, git-scope, quiz, tdd-proof]
---

# Acceptance fixes: keep corrective diffs scoped

When a follow-up task is created because acceptance failed on out-of-scope files, treat the previous feature implementation as fixed context and make the smallest corrective diff possible.

## Practical pattern

First compare recent commits and current status to separate accepted behavior changes from accidental additions. For this quiz task, the accepted UI edits stayed in `quiz/app.js` and `quiz/style.css`, while the corrective work was only to remove unrelated generated quiz/KB files and restore the original level filename.

## Gotchas

- Do not redo or revert accepted UI behavior just because the same commit also contained unrelated content.
- If a renamed tracked file must be restored, the corrective work can appear as deletions of the accidental new path plus an added file at the original path.
- Existing unrelated modified plan/checkpoint artifacts may be present in the worktree; leave them alone unless the task explicitly requires them.
- A truthful TDD proof cannot be reconstructed after the implementation is already committed. In that case, document the skip reason and verification scope rather than fabricating RED evidence.
