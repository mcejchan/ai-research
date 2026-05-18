# Build YT Knowledge Quiz Dashboard

Postav kompletní quiz dashboard jako self-contained web app v `~/Projects/ai-research/quiz/`.

## Specifikace

### Architektura

```
quiz/
├── server.js          # Node.js static file server, port 4002, + API endpoint GET /api/levels (čte ./levels/ dynamicky)
├── index.html         # Level select screen
├── quiz.html          # Quiz + results screen
├── style.css          # Dark tech theme
├── app.js             # Quiz logic, scoring, localStorage
└── levels/            # JSON soubory per level (bude prázdný, struktura hotová)
    └── .gitkeep
```

### Server (server.js)

- Port 4002
- Servíruje statické soubory (index.html, quiz.html, style.css, app.js)
- `GET /api/levels` — prochází `./levels/` rekurzivně, z každého JSON přečte metadata (title, channel, thumbnail, date, počet otázek, max bodů), vrátí pole seřazené chronologicky (nejnovější první)
- `GET /api/level?path=<channel/slug.json>` — vrátí obsah konkrétního level JSON

### Level Select (index.html)

- Grid karet s YT thumbnaily
- Každá karta: thumbnail, název videa, kanál, počet otázek, max body
- Indikátor "už hráno" + nejlepší skóre (z localStorage)
- Klik → quiz.html?level=<path>

### Quiz Screen (quiz.html)

- Progress bar nahoře (otázka X z N)
- Thumbnail videa nahoře (menší)
- Text otázky + bodová hodnota
- Odpovědi: radio buttony (single) nebo checkboxy (multi) podle `type`
- Tlačítko "Odpovědět"
- Po odpovědi: okamžitý feedback — zelená pro správné, červená pro špatné, zobrazit správnou odpověď
- Tlačítko "Další otázka"
- Na konci: results screen (celkové skóre / max, přehled otázek)
- Tlačítko "Zpět na levely"

### Design (style.css)

- **Dark tech theme** — tmavé pozadí (#0a0a0f nebo podobné near-black)
- **Neon akcenty** — cyan (#00f0ff), electric blue, amber pro highlights
- **Glow efekty** — subtle box-shadow/text-shadow na aktivních elementech
- **Typografie** — monospace font pro headings a skóre, sans-serif pro body
- **Karty** — glassmorphism nebo subtle border-glow
- **Celkový vibe** — sci-fi/hacking terminal, láká hrát, ne školní test
- **Responsive** — funguje na desktopu i tabletu

### Scoring + localStorage

- Každá otázka: body podle `points` (1–4)
- Single-select: správná = plné body, špatná = 0
- Multi-select: all-or-nothing (všechny správné zaškrtnuté, žádná navíc = plné body; jinak 0)
- localStorage key: `quiz_scores` — objekt `{ "channel/slug.json": { best: N, max: M, date: "ISO" } }`

### Data format (level JSON)

```json
{
  "title": "Název videa",
  "channel": "Název kanálu",
  "url": "https://youtube.com/watch?v=...",
  "thumbnail": "https://i.ytimg.com/vi/ID/maxresdefault.jpg",
  "date": "2026-05-18",
  "questions": [
    {
      "question": "Text otázky?",
      "type": "single",
      "points": 2,
      "options": ["Odpověď A", "Odpověď B", "Odpověď C", "Odpověď D"],
      "correct": [2]
    },
    {
      "question": "Vyber všechny správné:",
      "type": "multi",
      "points": 3,
      "options": ["X", "Y", "Z"],
      "correct": [0, 2]
    }
  ]
}
```

## DO NOT

- Nepoužívej žádný framework (React, Vue, etc.) — čistý vanilla JS
- Nepřidávej npm dependencies — jen Node.js built-in moduly (http, fs, path)
- Neměň nic mimo `quiz/` adresář
- Nepřidávej TypeScript, bundler, ani build step

## Ověření

```bash
cd ~/Projects/ai-research/quiz && node server.js &
# Server běží na http://localhost:4002
# GET http://localhost:4002/ → index.html
# GET http://localhost:4002/api/levels → []  (prázdné levels/)
curl -s http://localhost:4002/api/levels | python3 -c "import json,sys; d=json.load(sys.stdin); assert isinstance(d, list)"
```
