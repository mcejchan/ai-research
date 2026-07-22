# Plan 2026-07-22: Wire the registry to the root test gate

Persist the canonical registry command and expose the external-file change as reviewable acceptance evidence.

## Context

- Keep the accepted root `Makefile`, README, subsystem tests, and deployment workflow unchanged.
- Use the injected canonical value `cd ~/Projects/ai-research && make test` for `ai-research.testCommand`; the rejected parent artifact omitted the external registry change.
- Follow `learnings/tooling/root-test-gates-expose-hidden-suite-failures.md`: the registry owns the complete gate, while subsystem preflights remain scoped.

## Available Skills

- `task-evidence`: link the parent RED/GREEN proof without recreating historical failures.
- `validate-implementation`: check the registry-only repair against goal-002.
- `save-learning`: persist the required implementation-session learning as the final action.

## Implementation

1. In `/Users/michal/.openclaw/workspace/skills/opencode-dev/projects.yaml`, change only the `ai-research` `testCommand` to `cd ~/Projects/ai-research && make test`; preserve every other project field and registry entry.
2. Capture `git -C /Users/michal/.openclaw/workspace diff -- skills/opencode-dev/projects.yaml` in the task delivery evidence so acceptance reviews the external registry change rather than only the `ai-research` repository diff.
3. Create `plans/checkpoints/dark-vale-6236.red-green-proof.md` that links `plans/checkpoints/bold-dune-3929.red-green-proof.md` as historical RED/GREEN provenance and records only the fresh GREEN commands below; do not claim a new RED for the config edit.
4. Run `skill:validate-implementation`, confirm no completed parent-task files changed, then run `skill:save-learning` last and save at least one focused learning.

## Files to Modify

| File | Change |
|---|---|
| `/Users/michal/.openclaw/workspace/skills/opencode-dev/projects.yaml` | Point only `ai-research.testCommand` at the root `make test` gate. |
| `plans/checkpoints/dark-vale-6236.red-green-proof.md` | Link parent proof and record fresh registry/root-gate GREEN evidence. |
| `learnings/<category>/<generated-name>.md` | Save the required learning about delivering external registry diffs with acceptance artifacts. |

## TDD: skip

This is a registry-only YAML change with no suitable unit-test boundary; reuse the genuine parent proof and capture fresh GREEN verification instead of fabricating RED.

## Verification

- Parse `/Users/michal/.openclaw/workspace/skills/opencode-dev/projects.yaml` and assert the `ai-research` entry has exactly `testCommand: cd ~/Projects/ai-research && make test`.
- Run the registered command exactly: `cd ~/Projects/ai-research && make test`.
- Run `git -C /Users/michal/.openclaw/workspace diff --check -- skills/opencode-dev/projects.yaml`.
- Review `git -C /Users/michal/.openclaw/workspace diff -- skills/opencode-dev/projects.yaml` and confirm it contains only the intended `ai-research.testCommand` replacement.
- Run `git diff --check -- plans/checkpoints/dark-vale-6236.red-green-proof.md learnings` from the project root.

*Status: DRAFT*
*Created: 2026-07-22*
