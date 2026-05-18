# Plan 2026-05-18: Quiz Dashboard Static GitHub Pages Deploy

Prevest quiz dashboard na statickou vanilla app a publikovat ji pres GitHub Pages Actions artifact z `quiz/`.

## Analysis

### Kontext z codebase
- `quiz/app.js`: nahradit `/api/levels` fetch za `levels/index.json`; nahradit `/api/level?path=...` fetch za static JSON fetch pod `levels/`.
- `quiz/server.js`: ponechat API kompatibilitu, ale upravit static server tak, aby lokalne serviroval `levels/*.json`; aktualni `403` pro `levels` by rozbil static dev path.
- `quiz/server.js`: zkopirovat metadata logiku z `getLevels()` do noveho `quiz/build-index.js` bez zmeny formatu level JSON souboru.
- `quiz/levels/**/*.json`: vygenerovat a commitnout `quiz/levels/index.json`; build script musi pri scanu preskocit `levels/index.json`.
- `.github/workflows/`: pridat Pages workflow; neexistuje zadny aktualni workflow.
- `README.md`: root README neexistuje, vytvorit kratky root `README.md` s odkazem na live quiz.

### Relevantni dokumentace
- `docs/proposals/proposal-20260518-yt-knowledge-quiz.md`: zachovat vanilla HTML/JS/CSS, localStorage scoring, jeden JSON per level, chronologicke razeni nejnovejsi nahore, bez UI/scoring redesignu.

### Knowledge base
- `learnings/architecture/quiz-level-difficulty-metadata.md`: metadata index normalizuje `difficulty` na `easy` nebo `hard`; overit parsovani vsech JSON levelu.
- `learnings/architecture/self-contained-quiz-dashboard-without-dependencies.md`: zachovat dependency-free app; pro staticky rezim muze byt `levels/` primo servirovane.
- `learnings/tooling/dark-vale-9814-use-targeted-node-syntax-checks-for-small-script-based-uis-without-package-tooli.md`: pouzit `node --check`, ne neexistujici npm workflow.
- `learnings/patterns/cool-cove-5127-guard-browser-startup-to-make-vanilla-helpers-testable-in-node.md`: Node testy mohou importovat CommonJS helpery bez browser frameworku.

## Available Skills
- `tdd`: implementace zacina RED testem pro `quiz/build-index.js` a uklada RED/GREEN evidence.
- `validate-implementation`: po implementaci zkontrolovat static deploy cestu, DO NOT pravidla a verifikacni prikazy.
- `ci-debug`: pouzit pouze pri selhani GitHub Pages workflow.

## Solutions
- Pouzit GitHub Pages source `GitHub Actions`, ne branch `main` folder `/quiz`; Pages nepodporuje arbitrary `/quiz` folder source.
- Workflow pri pushi na `main` spusti `node quiz/build-index.js`, nahraje obsah `quiz/` jako Pages artifact a deployne ho.
- Commitovat baseline `quiz/levels/index.json`, aby app fungovala i bez Actions artifact buildu a pri primem local/static otevreni.

## Implementation

1. Vytvor `quiz/build-index.test.js` podle TDD sekce a over RED prikazem `cd quiz && node --test build-index.test.js`.
2. Vytvor `quiz/build-index.js` bez dependencies:
   - `walkJsonFiles(levelsDir)` rekurzivne najde `.json` soubory a preskoci `index.json`.
   - `readLevelMetadata(file, levelsDir)` vrati `{ path, title, channel, thumbnail, date, difficulty, questionCount, maxPoints }`.
   - `difficulty` nastav na `easy` jen pro `data.difficulty === 'easy'`, jinak `hard`.
   - `maxPoints` spocitej souctem `Number(question.points || 0)`.
   - Serad `levels.sort((a, b) => (b.date || '').localeCompare(a.date || ''))`.
   - Zapis pretty JSON do `quiz/levels/index.json` s koncovym newline.
   - Exportuj `{ buildLevelsIndex }`; pri `require.main === module` spust build pro `path.join(__dirname, 'levels')`.
3. Uprav `quiz/app.js`:
   - `initLevelsPage()` vola `fetchJson('levels/index.json')`.
   - `initQuizPage()` validuje `levelPath`: musi koncit `.json`, nesmi byt absolute, obsahovat `..` segment ani backslash.
   - Detail levelu nacita `fetchJson('levels/' + levelPath.split('/').map(encodeURIComponent).join('/'))`.
   - Neponechat zadny `/api/` fetch v browser app.
4. Uprav `quiz/server.js` minimalne:
   - Zachovej `/api/levels` a `/api/level` pro zpetnou kompatibilitu.
   - Odstran nebo zjemni `normalized.startsWith('levels')` blok tak, aby static server mohl cist `levels/index.json` a level JSON soubory.
   - Zachovej path traversal ochranu pres `filePath.startsWith(ROOT)`.
5. Pridat `.github/workflows/quiz-pages.yml`:
   - `on: push` pro `main` a `workflow_dispatch`.
   - `permissions: contents: read, pages: write, id-token: write`.
   - `actions/configure-pages`, `actions/upload-pages-artifact` s `path: quiz`, `actions/deploy-pages`.
   - Build krok pred uploadem: `node quiz/build-index.js`.
6. Vygeneruj baseline index prikazem `node quiz/build-index.js` a zahrn `quiz/levels/index.json` do commitu.
7. Vytvor nebo uprav `README.md` s odkazem `https://mcejchan.github.io/ai-research/` a poznamkou, ze quiz je Pages app z `quiz/` artifactu.
8. Po mergi/pushi v GitHub repo settings nastav Pages source na `GitHub Actions`; nenastavuj branch source `/quiz`.

## Files to Modify

| Soubor | Zmena |
|--------|-------|
| `quiz/build-index.test.js` | Node built-in testy pro metadata index generator. |
| `quiz/build-index.js` | Novy dependency-free generator `levels/index.json`. |
| `quiz/app.js` | Static fetch z `levels/index.json` a `levels/<path>.json`, zadne `/api/`. |
| `quiz/server.js` | Ponechat API, povolit static servirovani `levels/*.json`. |
| `quiz/levels/index.json` | Generated baseline index commitnuty s appkou. |
| `.github/workflows/quiz-pages.yml` | Pages deploy pres Actions artifact z `quiz/`. |
| `README.md` | Live link a kratka poznamka ke static quiz app. |

## TDD

**Workflow pro implementujiciho agenta:**
1. Vytvor/uprav test soubor podle skeletonu nize.
2. Spust targeted test a over RED.
3. Implementuj `quiz/build-index.js`.
4. Spust targeted test a over GREEN.
5. Spust verifikace v sekci Regression.

Implementace TDD cyklu dle skill:tdd. RED/GREEN evidence zapsat do `plans/checkpoints/cool-brook-0229.red-green-proof.md`.

### Targeted Tests

**Test file:** `quiz/build-index.test.js`  
**Framework:** Node built-in `node:test`, bez npm dependencies.  
**Run command:** `cd quiz && node --test build-index.test.js`  
**Edit hint:** NEW FILE

```js
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const { buildLevelsIndex } = require('./build-index');

test('buildLevelsIndex writes sorted static metadata and skips existing index', async () => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'quiz-levels-'));
  const channelDir = path.join(root, 'futurecast');
  await fs.mkdir(channelDir, { recursive: true });
  await fs.writeFile(path.join(root, 'index.json'), JSON.stringify([{ path: 'stale.json' }]));
  await fs.writeFile(path.join(channelDir, 'old.json'), JSON.stringify({
    title: 'Old', channel: 'FutureCast', thumbnail: 'old.jpg', date: '2024-01-01', difficulty: 'easy',
    questions: [{ points: 1 }, { points: 2 }]
  }));
  await fs.writeFile(path.join(channelDir, 'new.json'), JSON.stringify({
    title: 'New', channel: 'FutureCast', thumbnail: 'new.jpg', date: '2026-05-18', difficulty: 'weird',
    questions: [{ points: 4 }]
  }));

  const levels = await buildLevelsIndex(root, path.join(root, 'index.json'));
  const written = JSON.parse(await fs.readFile(path.join(root, 'index.json'), 'utf8'));

  assert.deepEqual(levels.map((level) => level.path), ['futurecast/new.json', 'futurecast/old.json']);
  assert.deepEqual(written, levels);
  assert.equal(levels[0].difficulty, 'hard');
  assert.equal(levels[0].questionCount, 1);
  assert.equal(levels[0].maxPoints, 4);
  assert.equal(levels[1].difficulty, 'easy');
  assert.equal(levels[1].maxPoints, 3);
});
```

| Test | RED pred impl | GREEN po impl |
|------|---------------|---------------|
| `buildLevelsIndex writes sorted static metadata and skips existing index` | `Cannot find module './build-index'` nebo chybi `buildLevelsIndex` | Vraci metadata nejnovejsi prvni, preskoci stale `index.json`, zapise stejny obsah na disk. |

### Regression
- [ ] `cd quiz && node --test build-index.test.js`
- [ ] `node --check quiz/build-index.js`
- [ ] `node --check quiz/app.js`
- [ ] `node --check quiz/server.js`
- [ ] `node quiz/build-index.js`
- [ ] `node -e "const fs=require('fs'); const levels=JSON.parse(fs.readFileSync('quiz/levels/index.json','utf8')); if (levels.length !== 6) throw new Error('Expected 6 levels'); if (levels.some(l => l.path === 'index.json' || !l.path.endsWith('.json'))) throw new Error('Bad paths');"`
- [ ] `! rg "/api/" quiz/app.js`
- [ ] `cd quiz && node server.js`, potom otevrit `http://localhost:4002/` a overit Network bez `/api/` requestu.
- [ ] Po pushi overit Pages URL `https://mcejchan.github.io/ai-research/`.

## Dependencies
- GitHub repo setting musi byt `Pages -> Source: GitHub Actions`; branch source `/quiz` nepouzivat.
- GitHub Pages URL pro artifact z `quiz/` bude root `https://mcejchan.github.io/ai-research/`; ne `/quiz/`, pokud artifact root je `quiz/`.
- Nepridavat npm dependencies ani package manager soubory do `quiz/`.
- Nemazat `quiz/server.js`, nemenit scoring, UI design ani format existujicich level JSON souboru.

---
*Status: DRAFT*
*Vytvoreno: 2026-05-18*
