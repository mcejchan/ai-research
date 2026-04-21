# Plan 2026-04-21: YT Viewer: Sort channels by latest video, show relative time

Sort the channel sidebar from newest activity to oldest by extending `/api/channels` with `latestDate`, then render a client-side relative timestamp without changing existing video ordering.

*Status: WIP*
*Vytvoreno: 2026-04-21*

---

## Progress

- [x] Faze 0: Config + Init
- [ ] Faze 1: Research
- [ ] Faze 2: Knowledge
- [ ] Faze 3: Synthesis

## Problem

Channel list currently sorts alphabetically. The API should expose each channel's newest video date from the `YYYY-MM-DD_` folder prefix, sort channels by that date descending, and the sidebar should show a relative label such as `today` or `2 days ago` next to each channel.

## Available Skills [WIP]

- `recall-knowledge`: pull repo learnings before finalizing implementation steps.
- `save-learning`: run after task completion to persist new learnings.

## Analysis [WIP]

### Kontext z codebase [TODO]

### Relevantni dokumentace [TODO]

### Knowledge base [TODO]

## Solutions [TODO]

## Implementation [TODO]

## Files to Modify [TODO]

## TDD [TODO]

## Dependencies [TODO]
