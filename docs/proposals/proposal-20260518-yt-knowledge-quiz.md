# YT Knowledge Quiz Dashboard

**Stav:** Draft
**Projekt:** ai-research
**Datum:** 2026-05-18

## Vision <!-- section:vision type:context -->

Herní dashboard pro testování znalostí z YouTube videí. Hráč prochází "levely" — každý level odpovídá jednomu zpracovanému videu. Level má:
- Obrázek nahoře (vizuální téma)
- N otázek s multiple-choice odpověďmi (single nebo multi-select)
- Bodování za správné odpovědi

Obsah generován z existujících transkriptů v `local-knowledge-base/youtube/`.

## Architecture <!-- section:architecture type:context -->

TBD — rozhodnout:
- Standalone HTML/JS app (jako yt-viewer) vs. součást existujícího dashboardu?
- Port?
- Kde žijí data (JSON soubory per level vs. jeden velký JSON)?
- Jak se generují otázky (LLM pipeline krok navíc, nebo separátní skript)?

## Open Questions <!-- section:open-questions type:context -->

1. **Persistence skóre** — ukládáme výsledky hráče? LocalStorage? Nebo jen session-based?
2. **Multiplayer/leaderboard** — jen single-player, nebo chceme scoreboard?
3. **Generování otázek** — automaticky z každého zpracovaného videa (nový krok v pipeline), nebo manuálně/on-demand?
4. **Obtížnost** — všechny otázky stejné, nebo difficulty levels?
5. **Obrázky** — odkud? Thumbnail z YT, nebo generované (DALL-E)?
6. **Cílová skupina** — kdo to bude hrát? Jen my, nebo veřejně?

## Content Pipeline <!-- section:content-pipeline -->

Proces přidání nového levelu:
1. Zpracovat video přes yt-transcript pipeline (transcript + analysis)
2. Vygenerovat otázky z transkriptu/analýzy (LLM)
3. Přidat obrázek
4. Level se objeví v dashboardu

## Quiz UI <!-- section:quiz-ui -->

- Level select screen (grid/list levelů s obrázky)
- Quiz screen (otázka + odpovědi + progress bar)
- Results screen (skóre, správné odpovědi)

## Scoring <!-- section:scoring -->

TBD — bodovací mechanika.

## Data Format <!-- section:data-format -->

TBD — struktura JSON/dat pro otázky a levely.
