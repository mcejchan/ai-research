# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

AI Research workspace focused on YouTube video transcript processing, analysis, and knowledge extraction.

### Workspace Structure

```
ai-research/
├── youtube-transcript-pipeline/    # YouTube transcript processing pipeline
│   ├── src/                        # Core modules (yt_pipeline, llm_client, drive_client)
│   ├── test/                       # Tests with mocks and fixtures
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pytest.ini
│   ├── Makefile
│   └── README.md
├── local-knowledge-base/           # Processed content
│   ├── youtube/                    # ~65 videos organized by channel/date
│   └── mindmap/                    # Generated mindmaps from YT content
├── helper-scripts/                 # Utility scripts
├── .claude/commands/               # Slash commands for knowledge work
├── CLAUDE.md                       # This file
└── .env                            # Environment config (create manually)
```

## YouTube Transcript Pipeline

Downloads, transcribes, analyzes, and organizes YouTube video content.

### Architecture

1. **Video Processing**: Extracts metadata via `yt-dlp`
2. **Transcript Extraction**: YouTube Transcript API with Whisper fallback
3. **Content Analysis**: OpenAI GPT-4o-mini for analysis
4. **Storage**: Google Drive or local mock storage (`local-knowledge-base/youtube/`)

### Core Modules

- **`src/yt_pipeline.py`**: Main orchestration pipeline with CLI
- **`src/llm_client.py`**: OpenAI API integration (analysis + embeddings)
- **`src/drive_client.py`**: Google Drive API with local fallback

## Common Commands

All pipeline commands run from `youtube-transcript-pipeline/`:

```bash
cd youtube-transcript-pipeline

# Process single video
python -m src.yt_pipeline --url "https://youtube.com/watch?v=VIDEO_ID"

# Process batch from Google Sheets
python -m src.yt_pipeline --from-sheet

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests (ALWAYS before commits)
pytest

# Coverage report
pytest --cov=src --cov-report=html
```

## Environment Configuration

Required in `.env` at workspace root:

```bash
OPENAI_API_KEY=your_openai_key
OPENAI_EMBEDDING_MODEL=text-embedding-3-large
DRIVE_FOLDER_ID=your_google_drive_folder_id
LANG=cs
USE_WHISPER_FALLBACK=true
MAKE_EMBEDDINGS=false
```

Without Drive credentials, pipeline falls back to local storage in `local-knowledge-base/`.

## Output Structure

Each video: `local-knowledge-base/youtube/{channel}/{date}_{slug}/`
- `transcript_clean.txt` - Cleaned transcript
- `analysis_main.md` - LLM analysis

## Slash Commands

- **`/mindmap <topic>`** - Create Markmap mind map from KB content
- **`/expand-analysis`** - Expand existing video analysis
- **`/flashcards <topic|path>`** - Generate flashcards from content
- **`/recall-knowledge`** - Search across knowledge base
- **`/kb-index`** - Regenerate KB index

## Testing

All external APIs are mocked. Run `pytest` before every commit.

## Key Dependencies

- `yt-dlp`, `youtube-transcript-api` - Video/transcript extraction
- `openai` - GPT-4o-mini analysis, text-embedding-3-large embeddings
- `google-api-python-client` - Drive integration
- `faster-whisper` - Whisper fallback
- `pytest` - Testing

## Git Workflow

```bash
git commit -m "Description of changes

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Security

- Never commit `.env`, `client_secret.json`, `token.json`, or API keys
- Use mock mode for development without credentials
