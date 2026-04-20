# Plan 2026-04-20: YT Viewer: Mobile responsive + match ai-education markdown styles

Align `yt-viewer/index.html` with the existing single-file viewer pattern while making the UI usable on small screens and copying the ai-education markdown presentation exactly.

*Status: DRAFT*
*Vytvoreno: 2026-04-20*

---

## Progress

- [x] Faze 0: Config + Init
- [x] Faze 1: Research
- [x] Faze 2: Knowledge
- [x] Faze 3: Synthesis

## Problem

`yt-viewer/index.html` currently uses a fixed desktop split layout and custom markdown styling. The plan needs to preserve the existing desktop SPA, add a mobile navigation flow for sidebar/video/content panels, and replace markdown presentation with the ai-education CSS rules copied verbatim from `~/Projects/ai-education/index.html`.

## Analysis

### Available Skills
- `recall-knowledge`: pull any project learnings relevant to a single-file viewer change before implementation.
- `save-learning`: capture viewer-specific lessons after the implementation task is completed.

### Kontext z codebase
- `yt-viewer/index.html`: single-file SPA with fixed `body` flex layout, `#sidebar` fixed at `280px`, `#video-list` capped at `200px`, hidden `#toolbar`, cached fetches, and markdown rendered into `#content-area` via `marked.parse(...)`.
- Existing DOM shape is minimal: `#sidebar` for channels, `#video-list` for cards, `#toolbar` for analysis/transcript toggle, `#content-area` for rendered markdown or transcript `<pre>`.
- Current viewer behavior already has the state needed for mobile drill-down (`current.channel`, `current.folder`, `current.tab`); responsive work can stay inside the same file without changing `server.js`.
- `plans/2026-04-20_bright-vale-3672_youtube-knowledge-base-viewer.md`: original viewer plan established the zero-dependency single-file SPA approach; the follow-up should stay in that architecture instead of introducing frameworks or build steps.

### Relevantni dokumentace
- `~/Projects/ai-education/index.html`: source of truth for markdown rendering CSS, especially `.markdown-content` typography, headings, links, code, blockquotes, tables, list spacing, and responsive behavior around the viewer shell.
- `CLAUDE.md`: repository guidance favors minimal changes, no new dependencies, and verification after changes.
- No project PlantUML docs were found under `docs/**/*.puml`.

### Knowledge base
**Pravidla a patterns:**
- `learnings/patterns/zero-dep-nodejs-file-viewer.md`: keep the viewer as a zero-dependency single-file SPA using `marked.js`; do not expand scope beyond `yt-viewer/index.html` for this UI pass.
- `learnings/patterns/bright-vale-3672-zero-dependency-node-file-viewer-can-stay-simple-and-safe.md`: preserve the existing client cache and lightweight browser-only flow; the mobile work should adjust layout/state only.

**Tooling learnings:**
- `learnings/tooling/bright-vale-3672-use-the-globally-installed-save-learning-helper-path.md`: post-task learning capture should use the globally installed `save-learning` skill path, not a repo-local assumption.
- `learnings/tooling/bright-vale-3672-save-learning-writes-require-pre-reading-overwrite-targets.md`: if `save-learning` writes through temp files, respect any read-before-overwrite guard.

**Search note:**
- QMD lookup for `ai-research-learnings` was unavailable (`Collection not found`), so the knowledge pass relied on direct learning-file reads and grep matches.

## Solutions
- Rework the page shell into a responsive layout that keeps the desktop two-pane view at `>=768px` and switches to a mobile panel flow at `<768px`.
- Add a compact mobile top bar with a menu toggle and contextual back controls; use class-based state on the root or body to switch between `channels`, `videos`, and `content` views without reloading data.
- Increase `.channel`, `.video-card`, toolbar buttons, and any new nav buttons to at least `44px` touch height.
- Replace the current `#content-area` markdown presentation rules with the ai-education markdown CSS copied verbatim from `~/Projects/ai-education/index.html`; keep transcript-specific `<pre>` rendering isolated so transcript mode remains readable.
- Preserve existing fetch endpoints, caching, and tab switching logic; only extend the DOM/state handling needed for mobile navigation.

## Implementation
### Pre-implementation checklist
- [ ] Read `yt-viewer/index.html` and `~/Projects/ai-education/index.html` side-by-side before editing so the markdown CSS is copied exactly.
- [ ] Keep changes confined to `yt-viewer/index.html`.
- [ ] Preserve desktop behavior for channel selection, video selection, analysis/transcript toggling, and cached fetches.

### Kroky implementace
1. Refactor the static shell CSS in `yt-viewer/index.html` so desktop keeps the current sidebar + main split while mobile switches to a stacked app shell with a top navigation row.
2. Add mobile-only controls and state classes for `menu open`, `video list open`, and `content open`, so selecting a channel moves the user to the video list and selecting a video moves the user to content with a back path.
3. Update interactive element sizing and spacing so channel rows, video cards, and toolbar buttons meet the 44px touch-target requirement without breaking desktop density.
4. Copy the ai-education markdown CSS rules for typography, headings, links, inline code, code blocks, blockquotes, tables, lists, and spacing into `yt-viewer/index.html`, replacing the current custom `#content-area` markdown styles.
5. Keep transcript rendering readable by scoping copied markdown CSS to markdown output and preserving a transcript-specific `pre`/plain-text style when `current.tab === 'transcript'`.
6. Adjust the existing `selectChannel`, `selectVideo`, `showTab`, and initial render flow so mobile state transitions feel continuous and desktop behavior stays unchanged.
7. Verify on desktop (`http://localhost:4001`), then in DevTools mobile emulation (iPhone SE and Pixel 7), then compare rendered markdown against `http://localhost:4000`.
8. After implementation is complete, run the `save-learning` skill and store at least one learning about the viewer/mobile/CSS-copy workflow.

## Files to Modify

| Soubor | Zmena |
|--------|-------|
| `yt-viewer/index.html` | Add responsive layout CSS, mobile navigation controls/state, touch-target sizing, and ai-education markdown CSS copied verbatim |

## TDD: skip

This task is a single-file responsive/CSS behavior change with manual browser verification requirements and no existing UI test harness in scope.

## Dependencies
- `yt-viewer/server.js` must remain unchanged and continue serving `yt-viewer/index.html` at `http://localhost:4001`.
- `~/Projects/ai-education/index.html` must remain readable during implementation because it is the exact markdown-style source.
- Verification depends on browser/device emulation rather than automated tests.
