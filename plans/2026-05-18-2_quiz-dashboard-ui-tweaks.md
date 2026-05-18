# Quiz Dashboard UI tweaks

Dva drobné UX vylepšení v `~/Projects/ai-research/quiz/`.

## Změny

### 1. Zobrazit obtížnost (body) PŘED odpovědí

Na quiz screen u každé otázky zobrazit bodovou hodnotu ještě před tím, než hráč odpoví. Např. badge/chip vedle otázky: "2 body", "4 body". Styl: monospace, neon accent, subtle — ne dominantní ale viditelné.

### 2. Méně agresivní červená pro špatnou odpověď

Aktuální feedback pro špatnou odpověď je příliš výrazně červená. Změnit na tlumenější variantu — např. `#cc4444` nebo `rgba(255, 80, 80, 0.7)` místo plného `#ff0000` / `red`. Cíl: hráč vidí že je špatně, ale není to "řev do obličeje".

### 3. Podpora `explanation` pole

Po zodpovězení otázky (ať správně nebo špatně) zobrazit krátké vysvětlení z `explanation` pole v JSON. Styl: menší text, italika nebo muted color, pod feedbackem.

## DO NOT

- Neměň strukturu souborů ani server.js API
- Neměň scoring logiku
- Neměň level select screen

## Ověření

- Otevřít quiz, u každé otázky vidět body PŘED odpovědí
- Po odpovědi: špatná = tlumená červená/oranžová (ne agresivní red)
- Po odpovědi: zobrazí se explanation text (pokud existuje v JSON)
