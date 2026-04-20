---
name: flashcards
description: Vygeneruj Obsidian Spaced Repetition flashcards z KB obsahu pro dané téma nebo konkrétní video
argument-hint: "<téma> NEBO <cesta/k/videu>"
allowed-tools: [AskUserQuestion, Bash, Read, Write]
---

<objective>
Generovat flashcards z knowledge base obsahu ve formátu kompatibilním s Obsidian Spaced Repetition pluginem. Podporuje dva módy:
1. **Search mód**: Prohledá KB podle tématu a vytvoří karty z relevantních zdrojů
2. **Direct mód**: Vytvoří karty z konkrétního videa/složky

Výstup uložit do `./local-knowledge-base/flashcards/YYYY-MM-DD-<slug>.md`.
</objective>

<context>
- Data jsou v `./local-knowledge-base/youtube/channel={CHANNEL}/{DATE}_{VIDEO_ID}/`
- Každé video má strukturovaný `analysis_main.md` se sekcemi:
  - Key Takeaways (s "Why it matters")
  - Practical Tips & Procedures (s kroky)
  - Tools & Technologies Mentioned
  - Important Warnings/Risks
- Výstupy patří do `./local-knowledge-base/flashcards/`
- Jazyk karet = jazyk zdroje (anglické video = anglické karty)
</context>

<process>
<step_1_intake>
Zpracuj $ARGUMENTS:

1. Pokud chybí, použij AskUserQuestion:
   - "Chceš vytvořit flashcards podle tématu (prohledám KB) nebo z konkrétního videa?"
   - Možnosti: "Podle tématu", "Z konkrétního videa"
   - Pak se zeptej na téma nebo cestu

2. Urči mód:
   - Pokud $ARGUMENTS obsahuje "youtube/" nebo "channel=" nebo existuje jako cesta → DIRECT mód
   - Jinak → SEARCH mód

3. Připrav výstup:
   - slug = téma/název složky převedené na lowercase-hyphenated
   - today = `date +%Y-%m-%d`
   - output_dir = `./local-knowledge-base/flashcards`; pokud neexistuje, `mkdir -p`
   - output_file = `$output_dir/$today-$slug.md`; pokud existuje, přidej `-v2`, `-v3`...
</step_1_intake>

<step_2_discovery>
**DIRECT mód:**
1. Ověř, že cesta existuje a obsahuje `analysis_main.md`
2. Přečti celý `analysis_main.md`
3. Extrahuj metadata (titul, kanál, URL) z hlavičky

**SEARCH mód:**
1. Prohledej KB pomocí `rg`:
   ```bash
   rg -i "<téma>" ./local-knowledge-base/youtube --glob '*.md' -l
   ```
2. Hledej i anglický/český ekvivalent tématu
3. Přečti relevantní `analysis_main.md` soubory (max 5-7 pro rozumnou velikost)
4. Zaznamenej zdroje pro citace
</step_2_discovery>

<step_3_extract_and_generate>
Z každého `analysis_main.md` extrahuj a transformuj:

**Z "Key Takeaways":**
```
Why is {takeaway title} significant?
?
{Why it matters text}
*Source: [{Channel}]({relative-path})*
```

**Z "Practical Tips & Procedures":**
```
How do you {procedure name}?
?
{Steps as numbered list}
*When to use: {context if available}*
```

**Z "Tools & Technologies":**
```
What is {tool name} and when to use it?
::
{Description}. {Use case if mentioned}.
```

**Z "Important Warnings":**
```
What risk is associated with {topic}?
?
{Warning explanation}
*Source: [{Channel}]({relative-path})*
```

**Cloze karty z citátů:**
```
"{First part of quote} =={key insight}== {rest of quote}"
```

Zachovej jazyk zdroje - pokud je analysis_main.md v angličtině, piš anglické otázky. Pokud česky, české.
</step_3_extract_and_generate>

<step_4_format>
Vytvoř výstupní soubor:

```markdown
---
tags:
  - flashcards
  - {topic-slug}
created: {YYYY-MM-DD}
sources: {count}
---

# {TOPIC} - Flashcards

## Key Concepts
#flashcards/{topic-slug}/concepts

{Karty z Key Takeaways oddělené ---}

---

## Procedures
#flashcards/{topic-slug}/procedures

{Karty z Practical Tips oddělené ---}

---

## Tools & Technologies
#flashcards/{topic-slug}/tools

{Karty z Tools oddělené ---}

---

## Warnings & Risks
#flashcards/{topic-slug}/warnings

{Karty z Warnings oddělené ---}

---

## Quick Facts (Cloze)
#flashcards/{topic-slug}/facts

{Cloze karty z citátů}

---

*Generated: {YYYY-MM-DD}*
*Total cards: {count}*
*Sources:*
{seznam zdrojů jako odrážky s relativními cestami}
```

Každou kartu odděl `---` na samostatném řádku.
</step_4_format>

<step_5_save>
1. Ulož do output_file pomocí Write
2. Vypiš potvrzení:
   - Cesta k souboru
   - Počet vygenerovaných karet
   - Seznam zdrojů
   - Tip: "Otevři v Obsidian s nainstalovaným Spaced Repetition pluginem pro review"
</step_5_save>
</process>

<card_format_reference>
Obsidian Spaced Repetition plugin podporuje:

| Typ | Syntaxe | Příklad |
|-----|---------|---------|
| Jednořádková | `Q::A` | `Capital of France::Paris` |
| Oboustranná | `Q:::A` | `Paris:::Capital of France` |
| Víceřádková | Q + newline + `?` + newline + A | viz výše |
| Oboustranná víceřádková | Q + newline + `??` + newline + A | vytvoří 2 karty |
| Cloze | `==skrytý text==` | `The year is ==2025==` |

Tagy jako `#flashcards/topic` vytváří decky v pluginu.
</card_format_reference>

<success_criteria>
- Flashcards uloženy v `./local-knowledge-base/flashcards/YYYY-MM-DD-<slug>.md`
- Karty správně naformátované pro Obsidian SR plugin
- Každá karta má zdroj/citaci
- Jazyk karet odpovídá jazyku zdroje
- Metadata v YAML frontmatter
</success_criteria>
