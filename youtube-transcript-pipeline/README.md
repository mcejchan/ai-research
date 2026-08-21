# YouTube Transcription & Analysis Pipeline

Automatizovaný nástroj pro stahování, přepis a analýzu YouTube videí pomocí AI. Projekt extrahuje přepisy videí, analyzuje obsah přes OpenAI-kompatibilní LLM rozhraní a ukládá výsledky do Google Drive s možností lokálního mock módu.

## 🚀 Rychlý start

```bash
# Z rootu repozitáře
cd youtube-transcript-pipeline

# Instalace závislostí
pip install -r requirements.txt

# Spuštění testů
pytest

# Zpracování jednoho videa
python -m src.yt_pipeline --url "https://youtube.com/watch?v=VIDEO_ID"

# Zpracování batch z Google Sheets
python -m src.yt_pipeline --from-sheet
```

## 📁 Struktura projektu

```
youtube-transcript-pipeline/
├── README.md                    # Tato dokumentace
├── CLAUDE.md                    # Instrukce pro Claude Code (AI asistent)
├── requirements.txt             # Produkční závislosti
├── requirements-dev.txt         # Vývojářské závislosti
├── pytest.ini                  # Konfigurace testů
├── .env                        # Volitelné lokální environment proměnné
│
├── src/                        # 📦 Zdrojové kódy
│   ├── __init__.py
│   ├── yt_pipeline.py          # 🎯 Hlavní pipeline logika
│   ├── llm_client.py           # 🤖 OpenAI-kompatibilní LLM integrace
│   └── drive_client.py         # ☁️ Google Drive/lokální storage
│
└── test/                       # 🧪 Test suite
    ├── __init__.py
    ├── fixtures/               # Test data
    │   ├── sample_llm_response.md
    │   ├── sample_metadata.json
    │   └── sample_transcript.json
    ├── mocks/                  # Mock objekty
    │   ├── mock_drive.py       # Google Drive API mock
    │   ├── mock_llm.py         # LLM API mocks
    │   └── mock_youtube.py     # YouTube API mock
    ├── test_yt_pipeline.py     # Tests pro hlavní pipeline
    ├── test_llm_client.py      # Tests pro LLM funkcionalitu
    └── test_drive_client.py    # Tests pro storage
```

## 🎯 Klíčové moduly

### `src/yt_pipeline.py` - Hlavní pipeline

**Co dělá:** Orchestruje celý proces od URL k finálnímu výstupu

**Klíčové funkce:**
- `extract_video_id(url)` - Extrakce video ID z YouTube URL
- `get_basic_meta(url)` - Získání metadat pomocí yt-dlp
- `fetch_transcript(video_id)` - Stažení přepisu (YouTube API + Whisper fallback)
- `clean_text_from_segments()` - Čištění a formátování přepisu
- `run_for_url(url, drive_client)` - Kompletní zpracování jednoho videa

**Workflow:**
1. Extrakce video ID z URL
2. Získání metadat (název, kanál, datum)
3. Stažení přepisu (YouTube Transcript API → Whisper fallback)
4. Čištění a formátování textu
5. LLM analýza obsahu
6. Uložení všech výstupů (raw JSON, clean text, analýza)
7. Aktualizace master indexu

### `src/llm_client.py` - LLM integrace

**Co dělá:** Zpracovává přepisy pomocí OpenAI-kompatibilního API

**Klíčové funkce:**
- `analyze_text(transcript, intent, lang, extra_context)` - Hlavní analýza
- `embed_text(text)` - Generování embeddings
- `analyze_text()` - Analýza přepisu pomocí zvoleného LLM modelu

**Templaty:**
- `TEMPLATE_GENERAL` - Obecná analýza videí
- `TEMPLATE_CLAUDE_CODE_HACKS` - Specializovaná extrakce tipů pro Claude Code

Konkrétní modely se vybírají pomocí `LLM_MODEL` a `OPENAI_EMBEDDING_MODEL`. Výchozí runtime hodnoty vlastní `src/llm_client.py`, aby se nekopírovaly do dokumentace.

### `src/drive_client.py` - Storage management

**Co dělá:** Ukládá výsledky do Google Drive nebo lokálně (mock mode)

**Klíčové funkce:**
- `upload_string(data, name, parent_id)` - Upload souboru
- `ensure_path(parts, root_id)` - Vytvoření folder struktury

**Módy:**
- **Google Drive mode**: Skutečný upload do Google Drive
- **Mock mode**: Lokální uložení (když chybí credentials)

## 🔧 Konfigurace

### LLM provider

Pipeline podporuje dva provozní módy přes stejné OpenAI-kompatibilní rozhraní:

- **Výchozí mód - lokální Copilot Bridge:** `OPENAI_BASE_URL` ani `OPENAI_API_KEY` není nutné nastavovat. Před spuštěním musí být lokální bridge dostupný; přesný výchozí endpoint a interní placeholder credential vlastní `src/llm_client.py`.
- **Direct OpenAI override:** nastavte současně `OPENAI_BASE_URL=https://api.openai.com/v1` a skutečný `OPENAI_API_KEY`. Tím má přímé OpenAI připojení přednost před výchozí bridge cestou.

`LLM_MODEL` a `OPENAI_EMBEDDING_MODEL` jsou volitelné override hodnoty. Aktuální fallbacky jsou definované v `src/llm_client.py`.

### Ostatní environment proměnné (`.env`)

```bash
DRIVE_FOLDER_ID=your_google_drive_folder_id

# === VOLITELNÉ ===
LANG=cs                          # Jazyk analýzy (cs/en)
USE_WHISPER_FALLBACK=true        # Whisper fallback když YouTube transcript nedostupný
MAKE_EMBEDDINGS=false            # Generovat embeddings
```

### Google Drive setup

1. Vytvořte Google Cloud projekt
2. Povolte Drive API
3. Stáhněte `client_secret.json` credentials
4. Při prvním spuštění proběhne OAuth flow → vytvoří se `token.json`

**Bez credentials:** Automaticky fallback na lokální mock mode

## 🏗️ Výstupní struktura

Pro každé video se vytvoří složka:
```
youtube/
└── {CHANNEL_NAME}/
    └── {YYYY-MM-DD}_{VIDEO_TITLE_SLUG}/
        ├── transcript_clean.txt     # Vyčištěný text (vždy po úspěšném přepisu)
        ├── analysis_main.md         # LLM analýza (jen po úspěšné analýze)
        └── vectors.json            # Embedding metadata (pokud enabled)
```

Pokud volitelná LLM analýza selže, přepis zůstane uložený a chyba se vypíše do logu. `analysis_main.md` se v takovém případě nevytvoří.

## 🧪 Testování

### Spuštění testů

```bash
# Všechny testy
pytest

# S coverage reportem
pytest --cov=src --cov-report=html

# Konkrétní test soubor
pytest test/test_yt_pipeline.py

# Konkrétní test
pytest test/test_yt_pipeline.py::TestYTPipeline::test_extract_video_id_youtube_com
```

### Test architektura

**Mock-based testing:** Všechny externí APIs jsou mockované
- ✅ YouTube Transcript API
- ✅ LLM API
- ✅ Google Drive API
- ✅ Subprocess calls (yt-dlp)

**Test kategorie:**
- **Unit tests**: Jednotlivé funkce
- **Integration tests**: Celý pipeline
- **Mock tests**: Externí API chování
- **Error handling**: Failure scénáře

## 🚨 Troubleshooting

### Časté problémy

**1. YouTube HTTP 403 Forbidden**
```bash
# Aktualizace yt-dlp na nejnovější verzi
pip install --upgrade yt-dlp
# nebo
yt-dlp --rm-cache-dir  # vyčistit cache
```

**2. Google Drive API chyby**
- Zkontrolujte `client_secret.json`
- Ověřte Drive API permissions
- Smazat `token.json` a znovu autorizovat

**3. LLM API chyby**
- Ve výchozím módu ověřte, že běží lokální Copilot Bridge
- V direct OpenAI módu ověřte `OPENAI_BASE_URL`, API klíč a kredity/limity
- Ověřte, že hodnoty `LLM_MODEL` a `OPENAI_EMBEDDING_MODEL` podporuje zvolený provider

**4. Import chyby**
```bash
# Spustit z root directory
python -m src.yt_pipeline --url "..."

# Ne takto:
cd src && python yt_pipeline.py  # ❌
```

## 🔄 Workflow pro vývojáře

### Přidání nové funkcionality

1. **Vytvoř testy první** (TDD approach)
2. **Implementuj funcionalitu** v příslušném modulu
3. **Spusť testy**: `pytest`
4. **Zkontroluj coverage**: `pytest --cov=src`
5. **Commit**: Následuj pattern "feat: description"

### Coding konvence

- **Python 3.12+** required
- **Type hints** pro všechny funkce
- **Docstrings** pro komplexní funkce
- **Mock external APIs** v testech
- **Environment variables** pro konfiguraci

### Git workflow

```bash
git checkout -b feature/new-functionality
# ... develop & test ...
git add .
git commit -m "feat: add new functionality

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin feature/new-functionality
# Create PR on GitHub
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `pytest`
5. Update documentation if needed
6. Create Pull Request

## 📚 Užitečné příkazy

```bash
# Development setup
pip install -r requirements-dev.txt

# Lint & format
black src/ test/
flake8 src/ test/

# Test jednotlivých komponent
pytest test/test_yt_pipeline.py -v
pytest test/test_llm_client.py -v  
pytest test/test_drive_client.py -v

# Zpracování konkrétního videa (debug)
python -c "
from src.yt_pipeline import run_for_url
from src.drive_client import DriveClient
run_for_url('https://youtu.be/VIDEO_ID', DriveClient())
"
```

## 📄 License

MIT License - viz LICENSE soubor

---

💡 **Pro otázky nebo problémy vytvořte GitHub Issue**
