# Plan 2026-08-21: Acceptance evidence for root test gate

Capture the missing caller-owned verification for the existing documentation change without repeating implementation work.

*Status: DRAFT*
*Created: 2026-08-21*

## Progress

- [x] Phase 0: Config + init
- [x] Phase 1: Research
- [x] Phase 2: Knowledge
- [x] Phase 3: Synthesis

## Analysis

### Codebase context

- Commit `dc2ef34` contains the completed README, `CLAUDE.md`, and parent checkpoint changes; do not modify or repeat them.
- Root `Makefile:3-7` is the executable gate authority: three Node suites followed by pipeline pytest.
- `plans/checkpoints/warm-reef-4253.evidence.md` has no verification evidence for either parent session.
- Acceptance repair `warm-reef-4253-acceptance-001-evidence-repair-001` escalated with `exact_command_outcome_evidence_unavailable` and no command/outcome pairs.

### Relevant documentation

- The parent plan marks `make test` from the project root as required verification.
- The acceptance result marks only `goal-005` unmet because the canonical caller-owned Test Gate was not run; goals 001-004 are complete.
- The parent checkpoint's prose claim is not canonical evidence and must not be reused as proof.

### Knowledge base

- `learnings/architecture/operator-docs-stable-modes-runtime-defaults.md`: runtime tests, not README string assertions, protect mutable behavior.
- Recall used deterministic local fallback because QMD collection `ai-research-learnings` was unavailable; unrelated returned learnings do not alter this evidence-only scope.
- Historical evidence gaps must be reported, not reconstructed or fabricated; fresh GREEN verification is required for this follow-up.

## Available Skills

- `acceptance`: finalize the caller-supplied acceptance run against the fresh canonical gate result.
- `task-evidence`: retain the existing historical no-evidence finding; do not rerun tests to invent parent provenance.
- `save-learning`: capture the evidence-provenance rule after the follow-up is complete.

## Implementation

1. Leave commit `dc2ef34` and all completed documentation/runtime work unchanged; preserve the historical evidence artifact's explicit absence of command/outcome pairs.
2. Use the caller-owned canonical Test Gate to run the registered command `cd ~/Projects/ai-research && make test`, with `/Users/michal/Projects/ai-research` as the effective working directory. An ordinary checkpoint assertion is not a substitute.
3. Require the canonical result to retain the command, working directory, exit status `0`, and passing outcomes for all three Node suites plus pipeline pytest.
4. Link the canonical gate run identifier and status from the `bold-reef-7057` follow-up state/checkpoint; report the parent provenance gap separately rather than attributing the fresh run to `warm-reef-4253`.
5. If the gate fails, document the concrete failure before changing anything; make only the smallest defect fix and its targeted test. Do not edit production files for evidence plumbing alone.
6. Invoke `save-learning` after evidence capture and save the provenance rule as the final task action.

## Files to Modify

| File or state | Change |
|---|---|
| Caller-owned canonical Test Gate record | Store the fresh root command, working directory, complete outcome, and passing status. |
| `bold-reef-7057` follow-up checkpoint/state | Reference the canonical gate record and this plan; do not duplicate it as self-authored proof. |
| Production code and operator docs | No change unless the canonical gate exposes a documented implementation defect. |

## TDD: skip

This is an evidence-only follow-up with no planned behavior change; do not fabricate a post-implementation RED, and use the fresh canonical `make test` result as GREEN regression evidence.

## Acceptance

- [ ] Canonical Test Gate ran `cd ~/Projects/ai-research && make test` from the registered project root.
- [ ] Caller-owned result records exit status `0` and passing Node and pytest outcomes.
- [ ] Follow-up state references the canonical result instead of relying on checkpoint prose.
- [ ] Parent evidence remains truthfully marked unavailable.
- [ ] No production files changed unless a real failing test justified a minimal fix.

## Dependencies

- The caller/orchestrator must expose a canonical Test Gate facility; a local shell transcript alone cannot satisfy `finding-001`.
- The preserved parent implementation at commit `dc2ef34` is the baseline under test.
