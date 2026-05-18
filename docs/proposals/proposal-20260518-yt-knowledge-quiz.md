# YT Knowledge Quiz Dashboard

**Stav:** Draft — decisions locked
**Projekt:** ai-research
**Datum:** 2026-05-18

## Vision <!-- section:vision type:context -->

Herní dashboard pro testování znalostí z YouTube videí. Hráč prochází "levely" — každý level odpovídá jednomu zpracovanému videu. Level má:
- Obrázek nahoře (YT thumbnail)
- N otázek s multiple-choice odpověďmi (single nebo multi-select, variabilní počet odpovědí)
- Bodování za správné odpovědi podle obtížnosti (1–4 body)

Obsah generován z existujících transkriptů v `local-knowledge-base/youtube/`.

## Decisions <!-- section:decisions type:context -->

| # | Rozhodnutí | Hodnota |
|---|-----------|---------|
| D1 | Cílová skupina | Lokální (my), ne veřejné |
| D2 | Persistence skóre | LocalStorage (žádný server) |
| D3 | Generování otázek | Manuální — Jackie vygeneruje level na požádání z konkrétního videa |
| D4 | Obrázky levelů | YT thumbnail |
| D5 | Stack | Vanilla HTML + JS + CSS, standalone server |
| D6 | Port | 4002 |
| D7 | Formát otázek | Mix single-select (radio) a multi-select (checkbox) |
| D8 | Počet odpovědí | Variabilní — od 2 (ano/ne) po N, podle kontextu |
| D9 | Feedback | Ihned po každé otázce (správně/špatně + správná odpověď) |
| D10 | Obtížnost/bodování | Každá otázka má rating 1–4 body podle obtížnosti |
| D11 | Data struktura | Jeden JSON per level |
| D12 | Umístění dat | `quiz/levels/<channel>/<video-slug>.json` (vše v `ai-research/quiz/`) |
| D13 | Řazení levelů | Chronologicky, nejnovější nahoře |
| D14 | Design | Dark tech theme — sci-fi/neon vibe, láká hrát |
| D15 | Adresář projektu | `~/Projects/ai-research/quiz/` (self-contained podprojekt) |

## Architecture <!-- section:architecture type:context -->

```
~/Projects/ai-research/
├── quiz/
│   ├── server.js          # Static file server, port 4002, serves levels from ./levels/
│   ├── index.html         # Level select (grid s thumbnaily, chronologicky)
│   ├── quiz.html          # Quiz screen
│   ├── style.css          # Dark tech theme
│   └── app.js             # Quiz logic, scoring, localStorage
│   └── levels/            # Quiz JSON soubory (per level)
│       └── <channel>/
│           └── <video-slug>.json
```

### Data format (level JSON)

Uložení: `quiz/levels/<channel>/<video-slug>.json`

```json
{
  "title": "Název videa",
  "channel": "Název kanálu",
  "url": "https://youtube.com/watch?v=...",
  "thumbnail": "https://i.ytimg.com/vi/<id>/maxresdefault.jpg",
  "date": "2026-05-18",
  "questions": [
    {
      "question": "Text otázky",
      "type": "single | multi",
      "points": 1-4,
      "options": ["A", "B", "C", "D"],
      "correct": [0] 
    }
  ]
}
```

`correct` = pole indexů správných odpovědí (i pro single-select, kvůli uniformitě).
`date` = pro chronologické řazení v level select.

## Content Pipeline <!-- section:content-pipeline -->

Proces přidání nového levelu (manuální trigger):
1. Video musí být zpracované přes yt-transcript pipeline (transcript + analysis existuje)
2. Jackie na požádání vygeneruje quiz otázky z transkriptu/analýzy (LLM)
3. Uloží JSON do `quiz/levels/<channel>/<slug>.json`
4. Level se automaticky objeví v dashboardu (server čte složku dynamicky)

## Quiz UI <!-- section:quiz-ui -->

### Level Select
- Grid karet s thumbnaily
- Název videa + kanál
- Počet otázek + max bodů
- Indikátor "už hráno" (z localStorage)

### Quiz Screen
- Progress bar (otázka X z N)
- Text otázky
- Odpovědi (radio/checkbox podle `type`)
- Po odpovědi: okamžitý feedback (zelená/červená + správná odpověď)
- Tlačítko "Další"

### Results Screen
- Celkové skóre (získané / max body)
- Přehled otázek (správně/špatně)
- Tlačítko "Zpět na levely"

## Scoring <!-- section:scoring -->

- Každá otázka: 1–4 body podle obtížnosti
- Single-select: plný počet bodů za správnou, 0 za špatnou
- Multi-select: plný počet bodů jen při všech správných zaškrtnutých (žádný navíc, žádný chybějící); jinak 0
- LocalStorage: uložit per-level nejlepší skóre + datum

## Design <!-- section:design type:context -->

- **Theme:** Dark, technologický look — evokuje sci-fi/hacking/tech vibe
- **Paleta:** Tmavé pozadí (near-black), neonové akcenty (cyan/electric blue/amber), jemné glow efekty
- **Typografie:** Monospace pro headings/scores, sans-serif pro body text
- **Cíl:** Má to vypadat jako hra, ne jako školní test — lákat k dalšímu levelu
- **Řazení levelů:** Chronologicky, nejnovější nahoře

## Open Questions <!-- section:open-questions type:context -->

- Animace přechodů mezi otázkami (fade/slide) — later
- Sound effects — later
