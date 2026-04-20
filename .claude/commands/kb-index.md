---
name: kb-index
description: Vygeneruj nebo aktualizuj centrální index všech zdrojů v knowledge base
argument-hint: "[--update]"
allowed-tools: [Bash, Read, Write]
---

<objective>
Proskenovat celý `./local-knowledge-base/` adresář, extrahovat metadata ze všech zdrojů (YouTube videa, články, theme guides, mindmapy, flashcards) a vygenerovat přehledný centrální index. Výstup uložit do `./local-knowledge-base/INDEX.md`.
</objective>

<context>
- Hlavní data jsou v `./local-knowledge-base/youtube/channel={CHANNEL}/{DATE}_{VIDEO_ID}/`
- Každé video má `analysis_main.md` (první řádek = titul) a `transcript_clean.txt`
- Další obsah: `filosofie/`, `theme/`, `mindmap/`, `flashcards/`
- Index slouží jako rozcestník pro rychlou orientaci a jako podklad pro ostatní KB nástroje
</context>

<process>
<step_1_scan>
Proskenuj strukturu `./local-knowledge-base/`:

1. Najdi všechny YouTube video složky:
   ```bash
   find ./local-knowledge-base/youtube -type d -name "*_*" 2>/dev/null | sort
   ```

2. Najdi všechny ostatní soubory:
   ```bash
   find ./local-knowledge-base -name "*.md" -not -path "*/youtube/*" 2>/dev/null | sort
   ```

3. Spočítej statistiky podle typu obsahu.
</step_1_scan>

<step_2_extract_metadata>
Pro každou YouTube video složku:
1. Extrahuj kanál z cesty (mezi `channel=` a `/`)
2. Extrahuj datum z názvu složky (YYYY-MM-DD prefix)
3. Přečti první řádek z `analysis_main.md` pro titul (odstraň `# ` prefix)
4. Pokud `analysis_main.md` neexistuje, použij název složky jako fallback

Pro ostatní soubory:
1. Přečti první heading jako titul
2. Urči typ podle cesty (filosofie, theme, mindmap, flashcards)
</step_2_extract_metadata>

<step_3_generate_index>
Vytvoř strukturovaný index s těmito sekcemi:

```markdown
# Knowledge Base Index

*Vygenerováno: {YYYY-MM-DD HH:MM}*

## Statistiky

| Typ | Počet |
|-----|-------|
| YouTube videa | {count} |
| Kanály | {count} |
| Filosofie | {count} |
| Theme guides | {count} |
| Mind mapy | {count} |
| Flashcard decky | {count} |

## Rychlá navigace

- [YouTube podle kanálu](#youtube-videa-podle-kanálu)
- [Chronologicky](#chronologicky)
- [Filosofie](#filosofie)
- [Theme guides](#theme-guides)
- [Mind mapy](#mind-mapy)
- [Flashcards](#flashcards)

---

## YouTube videa podle kanálu

### {Kanál} ({count} videí)

| Datum | Titul | Link |
|-------|-------|------|
| {YYYY-MM-DD} | {Titul} | [Analýza]({relativní-cesta}) |

... (seřazeno abecedně podle kanálu, videa chronologicky sestupně)

---

## Chronologicky (posledních 20)

| Datum | Titul | Kanál | Link |
|-------|-------|-------|------|
| {YYYY-MM-DD} | {Titul} | {Kanál} | [Analýza]({cesta}) |

---

## Filosofie

| Titul | Link |
|-------|------|
| {Titul} | [Číst]({cesta}) |

---

## Theme guides

| Datum | Téma | Link |
|-------|------|------|
| {YYYY-MM-DD} | {Téma} | [Číst]({cesta}) |

---

## Mind mapy

*Zatím žádné mind mapy. Použij `/mindmap <téma>` pro vytvoření.*

---

## Flashcards

*Zatím žádné flashcard decky. Použij `/flashcards <téma>` pro vytvoření.*

---

*Tento index je automaticky generovaný. Spusť `/kb-index` pro aktualizaci.*
```

Všechny cesty musí být relativní k `./local-knowledge-base/` pro funkční odkazy.
</step_3_generate_index>

<step_4_save>
1. Ulož obsah do `./local-knowledge-base/INDEX.md` pomocí Write
2. Vypiš potvrzení:
   - Cesta k souboru
   - Počet indexovaných položek podle typu
   - Datum generování
</step_4_save>
</process>

<success_criteria>
- Index uložen v `./local-knowledge-base/INDEX.md`
- Všechny YouTube videa zahrnuty s kanálem, datem a titulem
- Všechny ostatní sekce KB zahrnuty
- Relativní cesty fungují pro navigaci
- Statistiky odpovídají skutečnému obsahu
</success_criteria>
