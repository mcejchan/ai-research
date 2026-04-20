---
name: mindmap
description: Vygeneruj Markmap-kompatibilní mind mapu z KB obsahu pro dané téma
argument-hint: "<téma nebo fráze>"
allowed-tools: [AskUserQuestion, Bash, Read, Write]
---

<objective>
Prohledat knowledge base podle zadaného tématu, extrahovat klíčové koncepty, jejich propojení a zdroje, a vygenerovat hierarchickou mind mapu ve formátu kompatibilním s Markmap. Výstup uložit do `./local-knowledge-base/mindmap/<slug>.mindmap.md` (bez datového prefixu).
</objective>

<context>
- Data jsou v `./local-knowledge-base/` (YouTube analýzy, filosofie, theme guides)
- Každé video má `analysis_main.md` se strukturovanými sekcemi
- Markmap používá markdown headings pro hierarchii (# → ## → ### = strom)
- Výstupy patří do `./local-knowledge-base/mindmap/`
- Jazyk mapy = jazyk převažujících zdrojů
</context>

<process>
<step_1_intake>
1. Pokud $ARGUMENTS chybí, použij AskUserQuestion:
   - "Jaké téma chceš vizualizovat jako mind mapu?"
   - Volný text pro odpověď

2. TOPIC = $ARGUMENTS (ořízni mezery)

3. Připrav výstup:
   - slug = `echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//;s/-\{2,\}/-/g'`
   - output_dir = `./local-knowledge-base/mindmap`; pokud neexistuje, `mkdir -p`
   - output_file = `$output_dir/$slug.mindmap.md`; verze `-v2`, `-v3` pokud existuje
</step_1_intake>

<step_2_discovery>
1. Prohledej KB (ignoruj mindmap/ a theme/):
   ```bash
   rg -i "<téma>" ./local-knowledge-base --glob '!mindmap/*' --glob '!theme/*' --glob '*.md' -l
   ```

2. Odvoď anglický/český ekvivalent a hledej obojí

3. Pro obecná témata odvoď související klíčová slova:
   - AI → "model", "agent", "prompt", "LLM"
   - flashcards → "spaced repetition", "Anki", "memory"

4. Přečti relevantní `analysis_main.md` soubory (zaměř se na:)
   - Key Takeaways - hlavní koncepty
   - Practical Tips - aplikace
   - Tools & Technologies - konkrétní nástroje
   - Quotes - klíčové myšlenky

5. Zaznamenej pro každý zdroj:
   - Koncepty a jejich definice
   - Vztahy mezi koncepty
   - Zdroje (kanál, datum, cesta)
   - Citáty

6. **Mapuj koncepty ↔ zdroje (M:N vztah):**
   - Jeden zdroj může pokrývat více konceptů
   - Jeden koncept může mít více zdrojů
   - Příklad: video o "AI agenteck" může být relevantní pro koncepty "Prompt Engineering", "LangChain", "Autonomní systémy"
</step_2_discovery>

<step_3_synthesize>
Analyzuj nalezený obsah a identifikuj:

1. **Hlavní koncepty** - opakující se témata napříč zdroji
2. **Podkoncepty** - specifické aspekty hlavních témat
3. **Propojení** - jak spolu koncepty souvisí
4. **Praktické aplikace** - konkrétní tipy a postupy
5. **Nástroje** - zmíněné technologie a nástroje
6. **Otevřené otázky** - co stojí za další prozkoumání

Seskup podle logických kategorií, ne podle zdrojů.

**Důležité - multi-výskyt zdrojů:**
- Každý koncept/list může mít **více zdrojů**
- Každý zdroj se může objevit u **více konceptů** v různých větvích stromu
- Pokud video pokrývá témata A, B i C, přidej odkaz na něj ke všem třem
- Cíl: uživatel najde relevantní zdroj ať klikne na kteroukoliv větev, která ho zajímá
</step_3_synthesize>

<step_4_generate_markmap>
Vytvoř hierarchický markdown pro Markmap:

```markdown
---
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

# {TOPIC}

## Key Concepts
### {Concept 1}
- {Definition or explanation}
- **Quote:** "{relevant quote}"
- *Source:* [{Channel A}]({path-a})
- *Source:* [{Channel B}]({path-b})  ← více zdrojů pokud relevantní

### {Concept 2}
- {Explanation}
- Related to: {Concept 1}
- *Source:* [{Channel A}]({path-a})  ← stejný zdroj jako u Concept 1

### {Concept 3}
- {Explanation}
- *Source:* [{Channel C}]({path-c})

## Practical Applications
### {Application 1}
- {Step or tip}
- When to use: {context}
- *Source:* [{Channel}]({path})

### {Application 2}
- {Details}
- *Source:* [{Channel A}]({path-a})  ← zdroj se může opakovat i zde

## Tools & Technologies
### {Tool 1}
- {What it does}
- {How to use}
- *Source:* [{Channel}]({path})

### {Tool 2}
- {Description}
- *Source:* [{Channel}]({path})

## Sources
### {Channel 1}
- [{Video Title}]({path}) - {key contribution}

### {Channel 2}
- [{Video Title}]({path}) - {key contribution}

## Connections
### {Concept A} ↔ {Concept B}
- {How they relate}
- {Synergies or tensions}

## Questions for Exploration
- {Open question 1}
- {Open question 2}
- {Follow-up idea}

---
*Generated: {YYYY-MM-DD}*
*Sources: {count} files from {channel_count} channels*
```

Hierarchie:
- `#` = kořen (téma)
- `##` = hlavní větve (kategorie)
- `###` = podvětve (koncepty)
- `-` = listy (detaily)
- Formátování (`**bold**`, `*italic*`) se zachová v uzlech
</step_4_generate_markmap>

<step_5_save>
1. Ulož do output_file pomocí Write

2. Vypiš potvrzení:
   - Cesta k souboru
   - Počet zdrojů a kanálů
   - Počet identifikovaných konceptů
   - Tip: "Pro vizualizaci:"
     - "VS Code: nainstaluj 'Markdown Preview Markmap' extension"
     - "Web: zkopíruj obsah do markmap.js.org/repl"
     - "Obsidian: použij markmap community plugin"
</step_5_save>
</process>

<markmap_format_reference>
Markmap transformuje markdown headings na stromovou strukturu:

```
# Root           →  Kořenový uzel
## Branch 1      →  Větev 1. úrovně
### Leaf 1.1     →  Větev 2. úrovně
- Detail         →  List (potomek Leaf 1.1)
- **Bold**       →  Formátování zachováno
## Branch 2      →  Další větev 1. úrovně
```

YAML frontmatter `markmap:` konfiguruje:
- `colorFreezeLevel: 2` - barvy se mění od 2. úrovně
- `maxWidth: 300` - max šířka uzlu v px
- `initialExpandLevel: 2` - rozbalené úrovně na začátku

Podporované formátování v uzlech:
- `**bold**`, `*italic*`, `~~strikethrough~~`
- `[link](url)` - klikatelné odkazy
- `` `code` `` - inline kód
- `==highlight==` (s některými viewery)
</markmap_format_reference>

<success_criteria>
- Mind mapa uložena v `./local-knowledge-base/mindmap/<slug>.mindmap.md`
- Validní Markmap struktura (správná hierarchie headings)
- Koncepty logicky seskupené, ne jen seznam zdrojů
- Propojení mezi koncepty identifikována
- Všechny odkazy relativní a funkční
- Jazyk odpovídá převažujícímu jazyku zdrojů
</success_criteria>
