"""Cross-caller slug parity and offline standalone CLI checks."""

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "helper-scripts"
PIPELINE = ROOT / "youtube-transcript-pipeline"


def test_shared_slug_owner_and_script_aliases():
    sys.path.insert(0, str(SCRIPTS))
    sys.path.insert(0, str(PIPELINE))
    from src.path_slugs import slugify_path_segment, slugify_title
    from src.yt_pipeline import slugify_path_segment as public_path, slugify_title as public_title
    from normalize_kb_paths import slugify_path_segment as helper_path
    from rename_video_folders import slugify_title as helper_title

    for value in ("Příliš/žluťoučký_kůň", "a/b_c", "!!!", " a__//---   b ", "A" * 100):
        assert slugify_path_segment(value) == helper_path(value) == public_path(value)
        assert slugify_title(value) == helper_title(value) == public_title(value)
    assert slugify_path_segment("!!!", fallback="channel") == helper_path("!!!", fallback="channel")
    assert slugify_title("a/b_c") == "ab_c"
    assert len(slugify_title("a" * 100)) == 80


def test_importing_owner_does_not_load_services_or_environment(tmp_path):
    env = os.environ.copy()
    env.pop("DRIVE_FOLDER_ID", None)
    env.pop("OPENAI_API_KEY", None)
    code = (
        "import importlib.util, sys\n"
        "spec = importlib.util.spec_from_file_location('owner', sys.argv[1])\n"
        "owner = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(owner)\n"
        "assert owner.slugify_path_segment('Žluťoučký') == 'zlutoucky'\n"
        "assert not any(name in sys.modules for name in "
        "('dotenv', 'src.yt_pipeline', 'src.drive_client', 'src.llm_client', 'openai', 'youtube_transcript_api'))\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", code, str(PIPELINE / "src" / "path_slugs.py")],
        cwd=tmp_path, env=env, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr


def test_normalize_cli_dry_run_then_apply_updates_references(tmp_path):
    yt_root = tmp_path / "youtube"
    yt_root.mkdir()
    (yt_root / "Český Kanál").mkdir()
    refs = tmp_path / "refs"
    refs.mkdir()
    note = refs / "index.md"
    original = "youtube/Český Kanál/video\n"
    note.write_text(original, encoding="utf-8")
    command = [sys.executable, str(SCRIPTS / "normalize_kb_paths.py"),
               "--root", str(yt_root), "--refs-root", str(refs)]
    dry = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
    assert dry.returncode == 0, dry.stderr
    assert "DRY-RUN: Český Kanál -> cesky-kanal" in dry.stdout
    assert (yt_root / "Český Kanál").exists()
    assert note.read_text(encoding="utf-8") == original
    applied = subprocess.run(command + ["--apply"], cwd=tmp_path, capture_output=True, text=True)
    assert applied.returncode == 0, applied.stderr
    assert (yt_root / "cesky-kanal").is_dir()
    assert note.read_text(encoding="utf-8") == "youtube/cesky-kanal/video\n"


def test_title_script_direct_cli_keeps_underscore_and_slash_rules(tmp_path):
    yt_root = tmp_path / "youtube"
    video = yt_root / "channel" / "2024-01-01_videoid"
    video.mkdir(parents=True)
    (video / "analysis_main.md").write_text("# A/B_C\n", encoding="utf-8")
    command = [sys.executable, str(SCRIPTS / "rename_video_folders.py"),
               "--root", str(yt_root), "--refs-root", str(tmp_path)]
    dry = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
    assert dry.returncode == 0, dry.stderr
    assert "2024-01-01_ab_c" in dry.stdout
    assert video.exists()
