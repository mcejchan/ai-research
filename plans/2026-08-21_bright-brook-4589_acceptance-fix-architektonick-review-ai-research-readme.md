# Plan 2026-08-21: Canonical `make test` evidence

Capture the missing caller-owned root test-gate evidence without changing production code.

*Status: DRAFT*
*Vytvořeno: 2026-08-21*

## Progress

- [x] Fáze 0: Config + Init
- [x] Fáze 1: Research
- [x] Fáze 2: Knowledge
- [x] Fáze 3: Synthesis

## Analysis

### Kontext z codebase

- Commit `dc2ef34` already contains the accepted README and `CLAUDE.md` changes; no production edit is indicated.
- Root `Makefile:3-7` defines the registered aggregate gate: three Node test commands and pipeline pytest.
- `plans/checkpoints/bold-reef-7057.checkpoint.md` is locally modified with a self-authored pass claim, but it does not identify a caller-owned gate record.

### Relevantní dokumentace

- `plans/checkpoints/acceptance-runs/bold-reef-7057-acceptance-001/result.json` requires a caller-owned canonical Test Gate, not checkpoint prose.
- `plans/checkpoints/bold-reef-7057.evidence.md` and the repair audit contain no historical command/outcome pair; preserve that gap.
- The parent plan requires the registered root command and forbids production changes unless that gate exposes a real defect.

### Knowledge base

- `learnings/tooling/evidence-only-followups-rerun-the-exact-root-gate.md`: preserve command, root working directory, exit status, and all suite outcomes; a narrower test is insufficient.
- `learnings/architecture/operator-docs-stable-modes-runtime-defaults.md`: protect runtime behavior at executable boundaries instead of adding README string tests.
- Recall backend was local because collection `ai-research-learnings` was unavailable; no critical-pattern file was returned.

## Available Skills

- `task-evidence`: retain exact historical evidence and explicit gaps; never reconstruct provenance by rerunning history.
- `acceptance`: consume the caller-supplied canonical gate reference when reevaluating `goal-001`; it does not execute tests itself.
- `save-learning`: mandatory final implementation-session action after canonical evidence is attached.

## Implementation

1. Keep commit `dc2ef34`, production code, operator docs, and the historical no-evidence artifact unchanged.
2. Ask the caller/orchestrator's canonical Test Gate to execute the registered command `cd ~/Projects/ai-research && make test`, with effective working directory `/Users/michal/Projects/ai-research`; do not substitute a task-authored Bash transcript.
3. Require the gate record to identify caller ownership/run ID, exact command, working directory, exit status `0`, and passing outcomes for all three Node suites plus pipeline pytest.
4. Link that canonical gate record and this plan from the `bright-brook-4589` follow-up state/checkpoint; keep the unavailable parent-session evidence explicitly separate.
5. If the canonical gate fails, record the failure before editing anything and escalate only a concrete implementation defect to a minimal tested fix.
6. Invoke `save-learning` after the evidence and state link are complete, and save at least one session learning as the final action.

## Files to Modify

| File or state | Change |
|---|---|
| Caller-owned canonical Test Gate record | Create the authoritative command/outcome record through the caller/orchestrator facility. |
| `bright-brook-4589` follow-up state/checkpoint | Link this plan and the canonical gate run ID/status without copying prose as substitute evidence. |
| `learnings/**/*.md` | Add the mandatory session learning via `save-learning` last. |
| Production code and existing parent artifacts | No change unless the canonical gate reveals a real defect. |

## TDD: skip

This evidence-only task has no planned behavior change; do not fabricate RED evidence after the implementation already exists. The canonical `make test` result is fresh GREEN regression evidence.

## Acceptance

- [ ] Caller-owned canonical Test Gate ran the registered command from `/Users/michal/Projects/ai-research`.
- [ ] The canonical record includes its run ID/owner, exact command, working directory, exit status `0`, and all aggregate suite outcomes.
- [ ] Follow-up state references both this plan and the canonical record; checkpoint prose is not treated as the record.
- [ ] Historical parent evidence remains truthfully unavailable and no completed implementation work is repeated.
- [ ] `save-learning` created at least one learning as the implementation session's final action.

## Dependencies

- The caller/orchestrator must expose the canonical Test Gate; repository-authored artifacts alone cannot satisfy `finding-001`.
- The preserved implementation at `dc2ef34` remains the baseline unless the canonical gate proves a defect.
