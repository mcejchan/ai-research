# Plan 2026-07-22: Complete stale tmp cleanup acceptance evidence

Supply only the missing semantic-learning and canonical Test Gate evidence from the preserved parent implementation.

*Status: DRAFT*
*Created: 2026-07-22*

## Progress

- [x] Phase 0: Config + Init
- [x] Phase 1: Research
- [x] Phase 2: Knowledge
- [x] Phase 3: Synthesis

## Analysis

### Codebase context

- Commit `05316ed2bbac149fc42f3907a37b291f7a154cc1` already contains the six `tmp/*.md` deletions, `.gitignore` rule, checkpoint, and tracked canonical learning; do not redo them.
- `learnings/tooling/verify-deleted-tracked-files-with-worktree-state.md` contains the complete 23-line rule, but the rejected task-scoped diff omitted its content.
- `plans/checkpoints/calm-mist-6511.evidence.md` has no historical command/outcome pairs, and the acceptance result records Test Gate `status:not run`; fresh gate evidence is required.
- The worktree contains unrelated untracked auto-extracted learnings and acceptance artifacts; do not fold them into this follow-up's scoped diff.

### Relevant documentation

- `plans/2026-07-22_calm-mist-6511_remove-stale-tracked-tmp-artifacts.md` is the completed parent plan.
- `plans/checkpoints/acceptance-runs/calm-mist-6511-acceptance-001/{manifest,result}.json` are the authoritative goal and rejection records.
- No architecture document changes are relevant to this evidence-only follow-up.

### Knowledge base

- `learnings/tooling/verify-deleted-tracked-files-with-worktree-state.md`: distinguish index state from worktree state and avoid staging solely for verification; its full text is the semantic evidence target.
- `learnings/patterns/2026-07-22_deployment-workflows-should-invoke-the-tested-project-gate.md` is empty auto-extracted guidance and must not substitute for an actual Test Gate result.
- Recall used deterministic local fallback because collection `ai-research-learnings` was unavailable; the remaining returned quiz and integration learnings are unrelated.
- Historical evidence must remain explicitly unavailable; only fresh `make test` GREEN evidence may satisfy this follow-up.

## Available Skills

- `task-evidence`: preserve the explicit historical-evidence gap; never reconstruct or invent prior command outcomes.
- `validate-implementation`: check the evidence-only scope and goal coverage after artifacts are prepared.
- `save-learning`: mandatory final action; save one non-duplicative lesson about acceptance evidence.

## Solution

- Keep parent commit `05316ed2bbac149fc42f3907a37b291f7a154cc1` unchanged.
- Create one task-local checkpoint that embeds the full tracked learning, its source commit/path, and tracked-repository uniqueness evidence.
- Run `cd ~/Projects/ai-research && make test` through the caller-owned canonical Test Gate and link its returned GREEN reference; checkpoint prose alone is not a substitute.
- Exclude unrelated untracked monitor-generated artifacts from the follow-up diff.

## Implementation

1. Invoke `skill:task-evidence` for `calm-mist-6511`; retain its explicit lack of historical command/outcome evidence and do not reconstruct a historical RED or GREEN.
2. Create `plans/checkpoints/warm-wave-9996.checkpoint.md` with the verbatim output of `git show 05316ed2bbac149fc42f3907a37b291f7a154cc1:learnings/tooling/verify-deleted-tracked-files-with-worktree-state.md`, plus `git grep` results showing its distinctive guidance occurs only in that tracked canonical file.
3. Submit `cd ~/Projects/ai-research && make test` to the canonical Test Gate, require a completed GREEN status, and place only the returned gate reference and exact outcome in the checkpoint.
4. Run `skill:validate-implementation`; confirm the follow-up diff contains only this plan, checkpoint/evidence, and the mandatory learning, with no production, parent-cleanup, or unrelated untracked files.
5. Prepare a concise, non-duplicative lesson about attaching content-bearing evidence when an acceptance baseline hides an already committed artifact; invoke `skill:save-learning` as the final action to write it under `learnings/tooling/`.

## Files to Modify

| Path | Change |
|---|---|
| `plans/checkpoints/warm-wave-9996.checkpoint.md` | Add full parent-learning content, uniqueness evidence, historical-evidence gap, and the canonical Test Gate reference. |
| `learnings/tooling/committed-artifacts-need-content-bearing-acceptance-evidence.md` | Save one distinct session learning via `skill:save-learning`; include its intended content in the checkpoint before the final write. |

## TDD: skip

This follow-up changes evidence and documentation only; do not fabricate RED after the accepted implementation, and capture fresh GREEN through the canonical Test Gate.

## Verification

- `git show 05316ed2bbac149fc42f3907a37b291f7a154cc1:learnings/tooling/verify-deleted-tracked-files-with-worktree-state.md` matches the content embedded in the checkpoint.
- `git grep -n -E 'git ls-files --deleted|preserves index ownership' -- learnings` identifies only the retained tracked learning.
- Canonical Test Gate command `cd ~/Projects/ai-research && make test` returns GREEN and exposes a caller-owned reference recorded in the checkpoint.
- `git diff --check` passes, and the follow-up scoped diff has no runtime, pipeline, parent-cleanup, or unrelated cleanup changes.

## Dependencies

- The caller/task runner must expose the canonical Test Gate result and reference; a local command transcript cannot replace it.
- Parent acceptance run `calm-mist-6511-acceptance-001` and commit `05316ed2bbac149fc42f3907a37b291f7a154cc1` remain immutable provenance.
