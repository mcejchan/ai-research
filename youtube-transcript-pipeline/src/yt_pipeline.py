import os, re, json, tempfile, subprocess, pathlib, time, unicodedata
from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs
from typing import List, Optional, Dict

import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables FIRST before importing our modules
load_dotenv()

# LLM providers
from src.llm_client import analyze_text, embed_text
# Drive helpers
from src.drive_client import DriveClient
# Transcript
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

LANG = os.getenv("LANG", "en")
USE_WHISPER = os.getenv("USE_WHISPER_FALLBACK", "true").lower() == "true"
MAKE_EMBED = os.getenv("MAKE_EMBEDDINGS", "false").lower() == "true"

@dataclass
class VideoMeta:
    video_id: str
    title: str
    channel: str
    published: Optional[str]
    url: str

# --- utils ---

def extract_video_id(url: str) -> str:
    u = urlparse(url)
    if u.hostname in {"youtu.be"}:
        return u.path.strip("/")
    qs = parse_qs(u.query)
    if "v" in qs:
        return qs["v"][0]
    # fallback: last path segment
    return pathlib.Path(u.path).name


def clean_text_from_segments(segments) -> str:
    chunks = []
    for s in segments:
        if hasattr(s, 'text'):
            chunks.append(s.text.strip())
        elif isinstance(s, dict):
            chunks.append(s.get("text", "").strip())
    
    # Spojíme všechny části a očistíme mezery
    txt = re.sub(r"\s+", " ", " ".join(chunks)).strip()
    
    # Rozdělíme po větách - hledáme tečky následované mezerou a velkým písmenem
    # ale jen pokud není předcházejících písmen zkratka (např. Mr., Dr., U.S.)
    sentences = re.split(r'(?<![A-Z][a-z])\. (?=[A-Z])', txt)
    
    # Pokud se text nerozdělil (jen 1 věta), zkusíme alternativní postupy
    if len(sentences) == 1 and len(txt) > 500:
        # Fallback 1: Rozdělíme podle slov na řádky po ~100-150 znacích
        words = txt.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 pro mezeru
            if current_length + word_length > 150 and current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = word_length
            else:
                current_line.append(word)
                current_length += word_length
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return "\n".join(lines)
    
    # Vyčistíme a spojíme věty s novými řádky
    formatted_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            # Pokud věta nekončí tečkou, přidáme ji (kromě poslední)
            if not sentence.endswith('.') and sentence != sentences[-1]:
                sentence += '.'
            formatted_sentences.append(sentence)
    
    return "\n".join(formatted_sentences)


def fetch_transcript(video_id: str, lang_priorities=("en", "cs")) -> List[Dict]:
    # Try preferred languages first, then auto-generated
    try:
        api = YouTubeTranscriptApi()
        transcripts = api.list(video_id)
        
        # Hledáme preferované jazyky
        for lang in lang_priorities:
            for tr in transcripts:
                if tr.language_code == lang:
                    return tr.fetch()
        
        # Pokud nenajdeme preferované, vezmeme první dostupný
        if transcripts:
            return transcripts[0].fetch()
            
    except Exception as e:
        print(f"Chyba při získávání přepisu: {e}")
        raise


def slugify_title(title: str, max_length: int = 80) -> str:
    """Create a filesystem-friendly slug from a video title."""
    normalized = unicodedata.normalize("NFKD", title or "").encode("ascii", "ignore").decode()
    normalized = normalized.lower().strip()
    # Allow word chars and spaces/hyphens, strip other punctuation
    normalized = re.sub(r"[^\w\s-]", "", normalized)
    normalized = re.sub(r"[\s-]+", "-", normalized).strip("-")
    if not normalized:
        return ""
    return normalized[:max_length]

def slugify_path_segment(text: str, fallback: str = "unknown") -> str:
    """Normalize path segment to ASCII/kebab-case to avoid spaces/diacritics."""
    normalized = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode()
    normalized = normalized.replace("/", " ").replace("_", " ")
    normalized = normalized.lower().strip()
    normalized = re.sub(r"[^\w\s-]", "", normalized)
    normalized = re.sub(r"[\s-]+", "-", normalized).strip("-")
    return normalized or fallback


def whisper_transcribe(video_url: str, lang_hint: str = "auto") -> List[Dict]:
    # Download audio with yt-dlp
    with tempfile.TemporaryDirectory() as td:
        audio_path = os.path.join(td, "audio.m4a")
        cmd = [
            "yt-dlp", "-x", "--audio-format", "m4a",
            "-o", audio_path,
            video_url,
        ]
        subprocess.run(cmd, check=True)
        # faster-whisper
        from faster_whisper import WhisperModel
        model_size = "small"
        model = WhisperModel(model_size)
        segments, info = model.transcribe(audio_path, language=None if lang_hint=="auto" else lang_hint)
        out = []
        for seg in segments:
            out.append({
                "text": seg.text,
                "start": seg.start,
                "duration": seg.end - seg.start,
            })
        return out


def get_basic_meta(video_url: str) -> Dict:
    # Minimální metadata: název/kanál/publish z yt-dlp (bez YouTube API klíče)
    cmd = [
        "yt-dlp", "--ignore-config", "--dump-single-json", "--no-warnings", video_url
    ]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, check=True)
        js = json.loads(p.stdout)
        return {
            "title": js.get("title"),
            "channel": js.get("uploader"),
            "published": js.get("upload_date"),  # YYYYMMDD
            "duration": js.get("duration"),
            "thumbnail": js.get("thumbnail"),
        }
    except subprocess.CalledProcessError as e:
        print(f"yt-dlp error: {e}")
        print(f"stderr: {e.stderr}")
        print(f"stdout: {e.stdout}")
        raise


def run_for_url(url: str, drive: DriveClient):
    drive_folder_id = os.getenv("DRIVE_FOLDER_ID")
    if not drive_folder_id and not drive.mock_mode:
        raise RuntimeError("DRIVE_FOLDER_ID is required when using Google Drive")

    vid = extract_video_id(url)
    meta = get_basic_meta(url)
    channel = slugify_path_segment(meta.get("channel", "unknown"), fallback="unknown-channel")
    title_slug = slugify_title(meta.get("title", ""))
    folder_label = title_slug or vid
    folder_name = f"{time.strftime('%Y-%m-%d')}_{folder_label}"

    # Create channel/vid folder on Drive
    base_folder_id = drive.ensure_path(["youtube", channel, folder_name], root_id=drive_folder_id)

    # 1) transcript
    try:
        segments = fetch_transcript(vid, lang_priorities=("cs", "en"))
    except Exception:
        if not USE_WHISPER:
            raise
        segments = whisper_transcribe(url)

    # 2) clean text
    clean_txt = clean_text_from_segments(segments)

    # 3) save raw + txt - konvertujeme objekty na dictionary
    segments_dict = []
    for s in segments:
        if hasattr(s, 'text'):
            segments_dict.append({
                "text": s.text,
                "start": getattr(s, 'start', 0),
                "duration": getattr(s, 'duration', 0)
            })
        else:
            segments_dict.append(s)
    
    drive.upload_string(json.dumps(segments_dict, ensure_ascii=False, indent=2), "transcript_raw.json", base_folder_id)
    drive.upload_string(clean_txt, "transcript_clean.txt", base_folder_id)

    # 4) LLM analyses - přeskočíme pokud nemáme kredity
    try:
        # Zkrátíme text pokud je příliš dlouhý (max ~25k znaků pro spolehlivost)
        max_chars = 25000
        analysis_text = clean_txt if len(clean_txt) <= max_chars else clean_txt[:max_chars] + "\n\n[PŘEPIS ZKRÁCEN PRO ANALÝZU]"
        
        print(f"🧠 Spouštím LLM analýzu (délka: {len(analysis_text):,} znaků)...")
        analysis = analyze_text(analysis_text, intent="video_general", lang=LANG, extra_context={
            "title": meta.get("title"), "channel": meta.get("channel"), "url": url
        })
        drive.upload_string(analysis, "analysis_main.md", base_folder_id)
        print("✅ LLM analýza úspěšně vytvořena")
    except Exception as e:
        print(f"⚠️ LLM analýza přeskočena ({str(e)})")
        # Vytvoříme placeholder analýzu
        placeholder_analysis = f"""# Analýza videa: {meta.get("title", "Neznámý název")}

**Kanál:** {meta.get("channel", "Neznámý kanál")}
**URL:** {url}

## Přepis byl úspěšně stažen

Přepis videa je k dispozici v souboru `transcript_clean.txt`.
Pro automatickou analýzu obsahu je potřeba přidat kredity do LLM API.

**Statistiky:**
- Počet znaků: {len(clean_txt):,}
- Odhadovaná délka: {len(clean_txt.split())} slov
"""
        drive.upload_string(placeholder_analysis, "analysis_main.md", base_folder_id)

    # 5) cleanup - smazat raw transcript (už je duplicitní)
    drive.delete_file("transcript_raw.json", base_folder_id)

    # 6) embeddings (volitelně)
    if MAKE_EMBED:
        vec = embed_text(clean_txt)
        # persist minimal NPZ next to transcript
        drive.upload_string(json.dumps({"model": "openai", "dim": len(vec), "note": "store vectors locally if big"}), "vectors.json", base_folder_id)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="YouTube URL")
    parser.add_argument("--from-sheet", action="store_true", help="Process all URLs from Google Sheet queue")
    args = parser.parse_args()

    drive = DriveClient()

    if args.url:
        run_for_url(args.url, drive)
    elif args.from_sheet:
        from sheet_queue import pop_all_urls
        for u in tqdm(pop_all_urls()):
            try:
                run_for_url(u, drive)
            except Exception as e:
                print("Failed:", u, e)
    else:
        parser.print_help()
