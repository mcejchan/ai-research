# YouTube Knowledge Base Viewer

## Problem
Máme desítky analyzovaných YT videí v `local-knowledge-base/youtube/` organizovaných po kanálech a datech. Potřebujeme webový viewer s navigací přizpůsobenou YT struktuře.

## Struktura dat
```
local-knowledge-base/youtube/
├── lex-fridman/
│   ├── 2026-02-08_state-of-ai-in-2026/
│   │   ├── analysis_main.md
│   │   └── transcript_clean.txt
│   └── 2025-12-14_michael-levin/
│       └── ...
├── every/
│   └── ...
└── (38 kanálů celkem)
```

## Požadavky

### Server (`yt-viewer/server.js`)
- Node.js HTTP server, zero deps, ~80 řádků
- Port 4001
- ROOT = `path.join(__dirname, '..', 'local-knowledge-base', 'youtube')`
- Endpointy:
  - `GET /` → serve `index.html` from `yt-viewer/`
  - `GET /api/channels` → JSON array of `{name, videoCount}` (1st-level dirs, sorted alpha)
  - `GET /api/channel/:name` → JSON array of `{folder, date, title, hasAnalysis, hasTranscript}` (2nd-level dirs, sorted newest first)
  - `GET /api/video/:channel/:folder/analysis` → text content of `analysis_main.md`
  - `GET /api/video/:channel/:folder/transcript` → text content of `transcript_clean.txt`
- Path traversal protection: validate channel/folder contain no `..` or `/`

### Frontend (`yt-viewer/index.html` — single file SPA)
- Levý sidebar: seznam kanálů s počtem videí, kliknutelné
- Hlavní panel: seznam videí vybraného kanálu, klik → zobrazení `analysis_main.md`
- Tlačítko pro přepnutí mezi analýzou a raw transkriptem
- Markdown rendering: `marked.js` z CDN (`https://cdn.jsdelivr.net/npm/marked/marked.min.js`)
- Datum extrahovat z názvu složky (prefix `YYYY-MM-DD_`)
- Název videa: zbytek po datu, nahradit `-` za mezery, capitalize first letters
- Dark mode, minimalistický design

## Reference: ai-education server.js (DO NOT access this file — reference is inline below)

```javascript
const http = require("http");
const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const PORT = Number(process.env.PORT) || 4000;

const send = (res, status, body, type = "text/plain; charset=utf-8") => {
  res.writeHead(status, { "Content-Type": type });
  res.end(body);
};

http
  .createServer(async (req, res) => {
    try {
      const url = new URL(req.url, `http://${req.headers.host || "localhost"}`);
      if (req.method !== "GET") return send(res, 405, "Method not allowed");
      if (url.pathname === "/" || url.pathname === "/index.html") {
        const html = await fs.promises.readFile(path.join(ROOT, "index.html"), "utf8");
        return send(res, 200, html, "text/html; charset=utf-8");
      }
      if (url.pathname === "/api/files") {
        const files = await walk(ROOT);
        return send(res, 200, JSON.stringify(files), "application/json; charset=utf-8");
      }
      if (url.pathname === "/api/file") {
        const content = await fs.promises.readFile(safe.abs, "utf8");
        return send(res, 200, content, "text/plain; charset=utf-8");
      }
      return send(res, 404, "Not found");
    } catch (error) {
      if (error && error.code === "ENOENT") return send(res, 404, "Not found");
      return send(res, 500, "Internal server error");
    }
  })
  .listen(PORT, () => console.log(`Running on http://localhost:${PORT}`));
```

Use this pattern but adapt endpoints for the channel/video structure described above.

## Soubory k vytvořit
- `yt-viewer/server.js`
- `yt-viewer/index.html`

## Verify
```bash
node yt-viewer/server.js &
sleep 1
curl -s http://localhost:4001/api/channels | python3 -m json.tool | head -20
curl -s -o /dev/null -w "%{http_code}" http://localhost:4001/
kill %1
```

## DO NOT
- Add any npm dependencies — zero-dep Node.js only
- Access files outside this project (ai-education etc.)
- Modify the knowledge-base data files
- Use frameworks (React, Vue etc.) — vanilla JS only
