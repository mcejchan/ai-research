# Quiz Dashboard: Difficulty labels (Easy/Hard)

Doplnit zobrazení obtížnosti levelu na dashboardu a do datové struktury.

## Změny

### 1. Data format — přidat `difficulty` pole do level JSON

Každý level JSON bude mít nové pole `"difficulty": "easy" | "hard"`. Server ho čte a vrací v API.

Aktuální soubory k úpravě:
- `quiz/levels/futurecast-technologie-zitrka/*-easy.json` → přidat `"difficulty": "easy"`
- `quiz/levels/futurecast-technologie-zitrka/*-hard.json` → přidat `"difficulty": "hard"`

### 2. Server — vracet `difficulty` v `/api/levels`

`server.js` — při čtení level JSON zahrnout `difficulty` pole do metadat vracených v API odpovědi. Pokud pole chybí, defaultovat na `"hard"`.

### 3. Level Select UI — zobrazit difficulty badge

Na kartě levelu v `index.html` zobrazit vizuální label/badge:
- Easy → zelený badge "Easy"
- Hard → červený/oranžový badge "Hard"

Badge by měl být viditelný na kartě (roh nebo pod titulem), styl konzistentní s tech theme (neon glow).

### 4. Možnost filtrovat/řadit podle obtížnosti (nice-to-have)

Pokud jednoduché — přidat toggle/filter nahoře: "Všechny / Easy / Hard". Pokud to komplikuje kód příliš, vynechat.

## DO NOT

- Neměň quiz screen logiku ani scoring
- Neměň obsah otázek v JSON souborech (jen přidej `difficulty` pole)
- Neměň server port ani API endpointy

## Ověření

- Na level select screenu u každého levelu vidět badge Easy/Hard
- `curl http://localhost:4002/api/levels` vrací `difficulty` u každého levelu
