# Quiz Dashboard: Static deploy to GitHub Pages

Převést quiz dashboard na statickou app deployovatelnou přes GitHub Pages.

## Kontext

Aktuálně app používá Node.js server s dynamickým API (`GET /api/levels` čte `./levels/` složku). Pro GitHub Pages potřebujeme čistě statickou verzi bez serveru.

## Změny

### 1. Build skript: `quiz/build-index.js`

Node.js skript, který:
- Projde rekurzivně `quiz/levels/` 
- Z každého JSON přečte metadata (title, channel, thumbnail, date, difficulty, počet otázek, max bodů, relativní path)
- Zapíše `quiz/levels/index.json` — pole levelů seřazené chronologicky (nejnovější první)

Spuštění: `node quiz/build-index.js`

### 2. Upravit `app.js` — číst `levels/index.json` místo `/api/levels`

- Level select: fetchne `levels/index.json` (relativní URL)
- Detail levelu: fetchne přímo `levels/<channel>/<slug>.json` (relativní URL)
- Žádné volání `/api/` endpointů

### 3. `server.js` zachovat pro lokální dev

Server zůstane funkční pro lokální vývoj (servíruje statické soubory). Může zůstat i dynamický API endpoint pro zpětnou kompatibilitu, ale app ho nepoužívá.

### 4. Autocommit zahrnuje `levels/index.json`

Build skript se musí volat před commitem NEBO bude součást pre-push hooku. Nejjednodušší: přidat do autocommit cronu krok `node ~/Projects/ai-research/quiz/build-index.js` před git add.

**Alternativa (lepší):** GitHub Action, která po pushi spustí build-index a commitne výsledek. Tím se nemusí měnit lokální autocommit.

## DO NOT

- Nemazat `server.js` — zůstává pro lokální dev
- Neměnit formát level JSON souborů
- Neměnit quiz logiku, scoring, UI design
- Nepřidávat npm dependencies do quiz/ (čistý vanilla zůstává)

## Ověření

```bash
cd ~/Projects/ai-research/quiz
node build-index.js
cat levels/index.json  # ověřit že obsahuje všechny levely
# Otevřít index.html přímo v browseru (file:// nebo přes server) — musí fungovat bez /api/ volání
```


## Review Feedback

The static conversion is simple, but the GitHub Pages step contradicts the deploy requirement because Pages cannot publish directly from arbitrary `/quiz` folder source on `main`; it needs root/docs or an Actions deploy path.
