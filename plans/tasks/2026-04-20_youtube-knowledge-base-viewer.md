# YouTube Knowledge Base Viewer

## Problem
Máme desítky analyzovaných YT videí v `~/Projects/ai-research/local-knowledge-base/youtube/` organizovaných po kanálech a datech. Potřebujeme webový viewer podobný ai-education Markdown Vieweru (port 4000), ale s navigací přizpůsobenou YT struktuře.

## Struktura dat
```
local-knowledge-base/youtube/
├── lex-fridman/
│   ├── 2026-02-08_state-of-ai-in-2026/
│   │   ├── analysis_main.md
│   │   └── transcript_clean.txt
│   └── 2025-12-14_michael-levin/
│       ├── analysis_main.md
│       └── transcript_clean.txt
├── every/
│   ├── 2026-02-02_claude-turned-todos/
│   ...
└── (36 kanálů celkem)
```

## Požadavky

### Server
- Node.js HTTP server (stejný pattern jako `ai-education/server.js` — 75 řádků, zero deps)
- Port 4001 (aby nekolidoval s ai-education na 4000)
- ROOT = `~/Projects/ai-research/local-knowledge-base/youtube/`
- Endpointy:
  - `GET /` → index.html (SPA)
  - `GET /api/channels` → seznam kanálů (adresářů 1. úrovně) s počtem videí
  - `GET /api/channel/:name` → seznam videí v kanálu (adresáře 2. úrovně, seřazené od nejnovějšího)
  - `GET /api/video/:channel/:folder/analysis` → obsah `analysis_main.md`
  - `GET /api/video/:channel/:folder/transcript` → obsah `transcript_clean.txt`

### Frontend (index.html — single file SPA)
- Levý sidebar: seznam kanálů (kliknutelné, zobrazí videa)
- Hlavní panel: seznam videí vybraného kanálu, klik → zobrazení analysis_main.md
- Tlačítko pro přepnutí mezi analýzou a raw transkriptem
- Markdown rendering: použít `marked.js` z CDN (stejně jako ai-education viewer)
- Responsivní layout (CSS grid/flexbox)
- Datum extrahovat z názvu složky (prefix `YYYY-MM-DD_`)
- Název videa: zbytek po datu, nahradit `-` za mezery, capitalize

### Design
- Minimalistický, tmavý theme (dark mode)
- Inspirace ai-education viewerem ale vlastní identita
- Počet videí u každého kanálu v sidebar

## Reference
- Existující viewer: `~/Projects/ai-education/server.js` + `~/Projects/ai-education/index.html`
- Data: `~/Projects/ai-research/local-knowledge-base/youtube/`

## Soubory k vytvořit
- `~/Projects/ai-research/yt-viewer/server.js`
- `~/Projects/ai-research/yt-viewer/index.html`

## Verify
```bash
node ~/Projects/ai-research/yt-viewer/server.js &
sleep 1
curl -s http://localhost:4001/api/channels | python3 -m json.tool | head -20
curl -s -o /dev/null -w "%{http_code}" http://localhost:4001/
```

## DO NOT
- Add any npm dependencies — zero-dep Node.js only
- Modify anything in ai-education project
- Modify the knowledge-base data files
- Use frameworks (React, Vue etc.) — vanilla JS only

## Previous Plan (rejected - attempt 1)
Plan file: /Users/michal/Projects/ai-research/plans/2026-04-20_bright-vale-3672_youtube-knowledge-base-viewer.md
Review feedback: The plan content is missing—without any implementation details it cannot be judged for simplicity or alignment, and key requirements are silently omitted.
Read the previous plan, understand what was wrong, and produce a corrected plan.
