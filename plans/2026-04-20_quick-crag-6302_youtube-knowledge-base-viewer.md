# Plan 2026-04-20: [acceptance-fix] YouTube Knowledge Base Viewer

Fix acceptance check for missing `yt-viewer/index.html` — file already exists and is committed.

*Status: DRAFT*
*Task ID: quick-crag-6302*

---

## Problem

Acceptance check flagged `yt-viewer/index.html` as missing, but the file exists at `yt-viewer/index.html` (committed in `7620f85`). All three unmet goals are already satisfied:

1. **Single-file SPA** — 112-line HTML file with channel browsing, video selection, analysis/transcript viewing
2. **Dark-mode UI** — `background: #1a1a2e`, `color: #e0e0e0`, accent `#e94560`
3. **Client-side fetching/rendering** — `fetch()` to API endpoints, `marked.parse()` for markdown, response caching via `cache` object

## Analysis

### Already committed (do NOT redo)
- `yt-viewer/server.js` — zero-dep Node.js server with 4 API endpoints
- `yt-viewer/index.html` — single-file dark-mode SPA with all planned features

### Verification of unmet goals

| Goal | Status | Evidence |
|------|--------|----------|
| Create `yt-viewer/index.html` as SPA | DONE | File exists, 112 lines, committed `7620f85` |
| Channel list + video list + analysis/transcript | DONE | `loadChannels()`, `selectChannel()`, `selectVideo()`, `showTab()` |
| Dark-mode layout | DONE | CSS: `#1a1a2e` bg, `#e0e0e0` text, `#e94560` accents |
| Client-side fetching/rendering | DONE | `fetch('/api/...')`, `marked.parse()`, `cache` object |

## Implementation

### Krok 1: Verify file is served correctly

The acceptance failure may have been a diff-detection issue. Verify the server serves the SPA:

```bash
node yt-viewer/server.js &
sleep 1
curl -s -o /dev/null -w "%{http_code}" http://localhost:4001/
curl -s http://localhost:4001/ | head -5
kill %1
```

If `GET /` returns 200 with HTML content, no further changes needed.

### Krok 2: (conditional) If file somehow not served

Check `server.js` route for `/` serves `index.html` from `__dirname`. Fix if needed.

## Files to Modify

| Soubor | Změna |
|--------|-------|
| (none expected) | All goals already met |

## TDD: skip

No code changes expected — acceptance verification only.

## Dependencies

- Node.js runtime for verification
- Committed files in `yt-viewer/`

---
*Vytvořeno: 2026-04-20*
