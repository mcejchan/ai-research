# [acceptance-fix] YouTube Knowledge Base Viewer

## Previous learnings (auto-injected)
_Relevant past learnings from this project:_

### test-failures/proxy-backed-openai-client-constructor-assertions.md
---
title: "Pr: Create `yt-viewer/index.html` as a single-file SPA for channel browsing, video s

Auto-created by the monitor because the original task `bright-vale-3672` was accepted as done
but did not fully meet all acceptance goals.

## Unmet goals from acceptance check

- Create `yt-viewer/index.html` as a single-file SPA for channel browsing, video selection, and analysis/transcript viewing
- [P2] Missing frontend SPA file from plan (yt-viewer/index.html) -> Add the planned `yt-viewer/index.html` single-file SPA with channel list, video list, and analysis/transcript toggle.
- [P2] No evidence of the planned dark-mode viewer UI (yt-viewer/index.html) -> Implement the planned UI in `yt-viewer/index.html`, including the dark-mode layout and client-side fetching/rendering flow.

## Context

- Original task: `bright-vale-3672`
- Reason: `acceptance_incomplete`
- The original task's code changes are preserved. Continue from that state.

## Instructions

Implement only the unmet goals above. The original implementation is committed —
build on it, do not revert or redo completed work.

## Important: do not repeat completed work

The previous attempt partially succeeded. Review what is already committed before making changes. Do NOT revert or redo completed work. If the previous approach caused the failure, try a different approach.

## Original plan

Read the original plan at `/Users/michal/Projects/ai-research/plans/2026-04-20_bright-vale-3672_youtube-knowledge-base-viewer.md` for full context. Focus only on the unmet goals listed above.

## Previous attempt: acceptance context

**Why incomplete:** The backend server was implemented and manually verified, but a core planned deliverable, `yt-viewer/index.html`, is missing from the provided diff. Because not all plan goals are met, the task is incomplete.


**Already done (do NOT redo):**
- Create `yt-viewer/server.js` with the planned zero-dependency HTTP endpoints (`/`, `/api/channels`, `/api/channel/:name`, `/api/video/:channel/:folder/{analysis|transcript}`) and path validation
- Verify the viewer by running the planned manual endpoint checks

## Recent learnings from previous attempt


### zero-dep-nodejs-file-viewer.md

```
---
title: "Zero-dep Node.js file viewer pattern"
date: 2026-04-20
category: patterns
component: tooling
tags: [nodejs, zero-dep, file-viewer, spa]
---

# Zero-dep Node.js file viewer pattern

When building a simple file browser/viewer with Node.js (zero dependencies):

## Key patterns
- Use `URL` constructor for parsing request paths, then regex matching for route params
- Path traversal protection: validate segments contain no `..`, `/`, or `\` before joining with `path.join`
- Single-file SPA with `marked.js` from CDN works well for markdown rendering

## Gotchas
- `fs.promises.readdir` wit
```

## Implementation session log excerpt (last 50 lines)

```
.html
[x] Verify with curl tests
[x] Save learnings
[0m
All done. Here's what was implemented:

**`yt-viewer/server.js`** — Zero-dep Node.js HTTP server on port 4001 with 4 endpoints:
- `GET /` — serves the SPA
- `GET /api/channels` — lists channels with video counts
- `GET /api/channel/:name` — lists videos sorted newest-first
- `GET /api/video/:channel/:folder/(analysis|transcript)` — serves file content
- Path traversal protection included

**`yt-viewer/index.html`** — Single-file dark-mode SPA with:
- Left sidebar listing all 38+ channels with video counts
- Video list panel for selected channel
- Markdown rendering via `marked.js` CDN
- Toggle between analysis and raw transcript
- Client-side response caching

Verification passed: `/api/channels` returns valid JSON, `/` returns 200.

```
