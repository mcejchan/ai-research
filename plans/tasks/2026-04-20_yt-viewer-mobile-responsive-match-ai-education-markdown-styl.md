# YT Viewer: Mobile responsive + match ai-education markdown styles

## Problem
YT Viewer (`yt-viewer/index.html`) is desktop-only — no responsive layout for mobile. Markdown content styles differ from ai-education viewer.

## Requirements

### Mobile responsive layout
- Sidebar collapses to a hamburger menu or top bar on screens < 768px
- Video list and content take full width on mobile
- Touch-friendly tap targets (min 44px)
- Smooth transitions between sidebar/list/content views on mobile (back navigation)

### Markdown styles — match ai-education viewer exactly
Copy the markdown/content CSS from `~/Projects/ai-education/index.html` (the `.markdown-body` or equivalent styles). The rendered markdown should look identical between both viewers.

## Reference: ai-education index.html CSS

Agent: read `~/Projects/ai-education/index.html` and extract all CSS related to markdown rendering, typography, code blocks, headings, lists, tables, blockquotes. Copy those styles verbatim into `yt-viewer/index.html`.

## Files to modify
- `yt-viewer/index.html` — add responsive CSS + markdown styles

## Verify
1. Open `http://localhost:4001` on desktop — should still look good
2. Open in Chrome DevTools mobile view (iPhone SE, Pixel 7) — sidebar should be collapsible, content readable
3. Compare markdown rendering with `http://localhost:4000` — should look identical

## DO NOT
- Change server.js
- Add npm dependencies
- Break existing desktop layout
- Modify ai-education files
