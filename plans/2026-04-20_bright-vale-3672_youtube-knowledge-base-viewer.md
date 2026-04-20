# Plan 2026-04-20: YouTube Knowledge Base Viewer

Webový viewer pro `local-knowledge-base/youtube/` — Node.js server (zero deps) + single-file SPA s dark mode.

*Status: DRAFT*
*Task ID: bright-vale-3672*

---

## Problem

38 kanálů s desítkami videí v `local-knowledge-base/youtube/{channel}/{date}_{slug}/` nemá žádné UI pro procházení. Potřebujeme lightweight viewer na portu 4001.

## Analysis

### Kontext z codebase
- **38 kanálů** v `local-knowledge-base/youtube/`
- Struktura: `{channel}/{YYYY-MM-DD}_{slug}/` obsahuje `analysis_main.md` a `transcript_clean.txt`
- Žádný existující viewer (`yt-viewer/` neexistuje)
- Reference pattern: task popisuje `ai-education/server.js` inline — použít jako vzor pro HTTP server

### Knowledge base
- Learnings z task description se týkají `llm_client.py` proxy-backed OpenAI — **irelevantní** pro tento task

## Solutions

Jeden přímočarý přístup — přesně dle zadání:
- `yt-viewer/server.js`: Node.js HTTP server, `fs`/`path`/`http` only, ~80 řádků
- `yt-viewer/index.html`: Single-file SPA (HTML + CSS + JS), `marked.js` z CDN

## Implementation

### Krok 1: Vytvořit `yt-viewer/server.js`

```javascript
// Struktura:
const http = require("http");
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..", "local-knowledge-base", "youtube");
const PORT = 4001;
```

**Endpointy:**

| Route | Logika |
|-------|--------|
| `GET /` | Serve `index.html` z `__dirname` |
| `GET /api/channels` | `fs.readdirSync(ROOT)` → filter dirs → map `{name, videoCount}` → sort alpha |
| `GET /api/channel/:name` | Validate name (no `..`, no `/`), readdir, parse `YYYY-MM-DD_slug`, sort newest first |
| `GET /api/video/:channel/:folder/analysis` | Validate params, read `analysis_main.md` |
| `GET /api/video/:channel/:folder/transcript` | Validate params, read `transcript_clean.txt` |

**Security:** Reject params containing `..` or `/` with 400.

**URL parsing:** Use `new URL(req.url, ...)`, match routes via `pathname.match(/^\/api\/.../)`.

### Krok 2: Vytvořit `yt-viewer/index.html`

Single file SPA:

**Layout:**
- CSS Grid: sidebar (250px) + main content (flex)
- Dark mode: `background: #1a1a2e`, `color: #e0e0e0`

**Sidebar:**
- Fetch `/api/channels`, render `<div>` per channel with name + badge count
- Click → fetch `/api/channel/:name`, populate main panel

**Main panel:**
- Video list: cards s datem + title
- Click video → fetch analysis, render via `marked.parse()`
- Toggle button: Analysis ↔ Transcript

**Title parsing:** `"2026-02-08_state-of-ai-in-2026"` → date `2026-02-08`, title `State Of Ai In 2026` (split `_` from first, rest replace `-` with space, capitalize words)

**CDN:** `<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>`

### Krok 3: Verify

```bash
node yt-viewer/server.js &
sleep 1
curl -s http://localhost:4001/api/channels | python3 -m json.tool | head -20
curl -s -o /dev/null -w "%{http_code}" http://localhost:4001/
kill %1
```

## Files to Modify

| Soubor | Změna |
|--------|-------|
| `yt-viewer/server.js` | NEW — Node.js HTTP server |
| `yt-viewer/index.html` | NEW — Single-file SPA |

## TDD: skip

Zero-dep vanilla JS viewer s inline HTML — žádná test infrastruktura, čistě UI/server task. Ověření manuální curl příkazy dle verify sekce.

## Dependencies

- Node.js runtime
- `local-knowledge-base/youtube/` existuje s daty (38 kanálů)
- Síťový přístup k CDN pro `marked.js` (pouze frontend)

---
*Vytvořeno: 2026-04-20*
