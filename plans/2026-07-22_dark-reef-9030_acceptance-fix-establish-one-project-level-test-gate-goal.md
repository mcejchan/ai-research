# Plan 2026-07-22: Supply registry test-gate evidence

Preserve the completed registry wiring and make its external commit diff reviewable in this task's evidence bundle.

## Analysis

- Commit `169c092c98` already delivered `ai-research.testCommand: cd ~/Projects/ai-research && make test`; do not redo the registry or root-gate work.
- `plans/checkpoints/dark-vale-6236.checkpoint.md` asserted delivery but omitted the external `projects.yaml` diff, leaving the task-scoped acceptance diff empty.
- `plans/checkpoints/bold-dune-3929.red-green-proof.md` is the genuine historical RED/GREEN proof for the root gate; this YAML/evidence follow-up must record only fresh GREEN results.
- `learnings/tooling/external-registry-changes-need-external-diff-evidence.md` requires evidence from the registry's own Git worktree and execution of the registered command exactly.

## Available Skills

- `task-evidence`: recover and link exact parent proof and verification provenance.
- `validate-implementation`: verify the evidence-only repair against the unmet acceptance goal.
- `save-learning`: save the mandatory session learning as the final action.

## Implementation

1. Use `skill:task-evidence` to confirm the parent proof lineage and exact prior verification outcomes; reference `plans/checkpoints/bold-dune-3929.red-green-proof.md` rather than creating a new RED.
2. Extract the delivered external change with `git -C /Users/michal/.openclaw/workspace show --format= 169c092c98 -- skills/opencode-dev/projects.yaml` and place the verbatim scoped diff in `plans/checkpoints/dark-reef-9030.checkpoint.md` so the acceptance bundle shows the `ai-research.testCommand` value.
3. In that checkpoint, record fresh results for the exact registered command, the YAML value assertion, and external commit/diff validation; explicitly state that no registry implementation was changed by this follow-up.
4. Run `skill:validate-implementation` against goal-001 and confirm the checkpoint contains reviewable external diff evidence, not only an assertion or project-local diff.
5. Run `skill:save-learning` last and save at least one focused learning from this repair session.

## Files to Modify

| File | Change |
|---|---|
| `plans/checkpoints/dark-reef-9030.checkpoint.md` | Add the external commit's scoped registry diff, parent proof link, and fresh GREEN evidence. |
| `learnings/<category>/<generated-name>.md` | Save the required learning from the acceptance-evidence repair. |

`/Users/michal/.openclaw/workspace/skills/opencode-dev/projects.yaml` is verification-only because the required value is already delivered; modify it only if validation disproves the authoritative snapshot.

## TDD: skip

This follow-up supplies evidence for an already implemented YAML change; reuse the historical genuine RED and capture fresh GREEN verification instead of fabricating a new failing test.

## Verification

- Assert the parsed `ai-research` entry equals `testCommand: cd ~/Projects/ai-research && make test`.
- Run the registered command exactly: `cd ~/Projects/ai-research && make test`.
- Run `git -C /Users/michal/.openclaw/workspace show --check 169c092c98 -- skills/opencode-dev/projects.yaml`.
- Confirm the checkpoint embeds the scoped `169c092c98` diff containing the exact command.
- Run `git diff --check -- plans/checkpoints/dark-reef-9030.checkpoint.md learnings`.

*Status: DRAFT*
*Created: 2026-07-22*
