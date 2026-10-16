"""Offline characterization of transcript workflow and shared slug ownership."""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, call, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import yt_pipeline as pipeline


URL = "https://youtu.be/video_id"
META = {"title": "Příliš dlouhý název", "channel": "Český/Kanál_Name"}


def test_transcript_artifacts_preserve_object_defaults_and_dict_values():
    from src.yt_pipeline import upload_transcript_artifacts

    drive = Mock()
    segments = [SimpleNamespace(text="Ahoj", start=1.5),
                {"text": "Svět", "start": 2, "duration": 1}]
    upload_transcript_artifacts(segments, "Ahoj Svět", drive, "folder")
    raw = [{"text": "Ahoj", "start": 1.5, "duration": 0},
           {"text": "Svět", "start": 2, "duration": 1}]
    assert drive.upload_string.call_args_list == [
        call(json.dumps(raw, ensure_ascii=False, indent=2), "transcript_raw.json", "folder"),
        call("Ahoj Svět", "transcript_clean.txt", "folder"),
    ]


def test_shared_slug_owner_preserves_distinct_title_and_path_rules():
    from src.path_slugs import slugify_path_segment, slugify_title

    assert slugify_path_segment("Příliš/žluťoučký_kůň") == "prilis-zlutoucky-kun"
    assert slugify_title("a/b_c") == "ab_c"
    assert slugify_title("!!!") == ""
    assert slugify_path_segment("!!!", fallback="channel") == "channel"
    assert slugify_path_segment("a___ // -- b") == "a-b"
    assert len(slugify_title("A" * 100)) == 80
    assert pipeline.slugify_title is slugify_title
    assert pipeline.slugify_path_segment is slugify_path_segment


def run_mocked(monkeypatch, segments, *, analysis="analysis", embedding=False):
    monkeypatch.setattr(pipeline, "extract_video_id", Mock(return_value="video_id"))
    monkeypatch.setattr(pipeline, "get_basic_meta", Mock(return_value=META))
    monkeypatch.setattr(pipeline, "fetch_transcript", Mock(return_value=segments))
    monkeypatch.setattr(pipeline, "analyze_text", Mock(return_value=analysis))
    monkeypatch.setattr(pipeline, "embed_text", Mock(return_value=[0.1, 0.2]))
    monkeypatch.setattr(pipeline.time, "strftime", Mock(return_value="2026-10-16"))
    monkeypatch.setattr(pipeline, "MAKE_EMBED", embedding)
    monkeypatch.setenv("DRIVE_FOLDER_ID", "root")
    drive = Mock(mock_mode=False)
    drive.ensure_path.return_value = "folder"
    pipeline.run_for_url(URL, drive)
    return drive


def test_workflow_path_text_serialization_and_order(monkeypatch):
    segments = [SimpleNamespace(text="Ahoj.  Svět", start=1.5),
                {"text": " Druhá věta", "start": 2}]
    drive = run_mocked(monkeypatch, segments)
    pipeline.extract_video_id.assert_called_once_with(URL)
    pipeline.get_basic_meta.assert_called_once_with(URL)
    pipeline.fetch_transcript.assert_called_once_with("video_id", lang_priorities=("cs", "en"))
    drive.ensure_path.assert_called_once_with(
        ["youtube", "cesky-kanal-name", "2026-10-16_prilis-dlouhy-nazev"], root_id="root"
    )
    clean = pipeline.clean_text_from_segments(segments)
    assert clean == "Ahoj.\nSvět Druhá věta"
    assert drive.method_calls == [
        call.ensure_path(["youtube", "cesky-kanal-name", "2026-10-16_prilis-dlouhy-nazev"], root_id="root"),
        call.upload_string(json.dumps([
            {"text": "Ahoj.  Svět", "start": 1.5, "duration": 0},
            {"text": " Druhá věta", "start": 2},
        ], ensure_ascii=False, indent=2), "transcript_raw.json", "folder"),
        call.upload_string(clean, "transcript_clean.txt", "folder"),
        call.upload_string("analysis", "analysis_main.md", "folder"),
        call.delete_file("transcript_raw.json", "folder"),
    ]


def test_transcript_fallback_only_on_exception(monkeypatch):
    monkeypatch.setattr(pipeline, "fetch_transcript", Mock(side_effect=ValueError("missing")))
    monkeypatch.setattr(pipeline, "whisper_transcribe", Mock(return_value=[]))
    monkeypatch.setattr(pipeline, "USE_WHISPER", False)
    with pytest.raises(ValueError, match="missing"):
        pipeline.acquire_transcript("id", URL)
    pipeline.whisper_transcribe.assert_not_called()
    monkeypatch.setattr(pipeline, "USE_WHISPER", True)
    assert pipeline.acquire_transcript("id", URL) == []
    pipeline.whisper_transcribe.assert_called_once_with(URL)
    pipeline.fetch_transcript.side_effect = None
    pipeline.fetch_transcript.return_value = []
    assert pipeline.acquire_transcript("id", URL) == []
    pipeline.whisper_transcribe.assert_called_once_with(URL)


def test_analysis_truncation_context_and_embedding_full_text(monkeypatch, capsys):
    text = "x" * 25001
    drive = run_mocked(monkeypatch, [{"text": text}], embedding=True)
    analysis = text[:25000] + "\n\n[PŘEPIS ZKRÁCEN PRO ANALÝZU]"
    pipeline.analyze_text.assert_called_once_with(
        analysis, intent="video_general", lang=pipeline.LANG,
        extra_context={"title": META["title"], "channel": META["channel"], "url": URL},
    )
    pipeline.embed_text.assert_called_once_with(text)
    assert drive.method_calls[-2:] == [
        call.delete_file("transcript_raw.json", "folder"),
        call.upload_string(json.dumps({"model": "openai", "dim": 2, "note": "store vectors locally if big"}),
                           "vectors.json", "folder"),
    ]
    assert f"🧠 Spouštím LLM analýzu (délka: {len(analysis):,} znaků)..." in capsys.readouterr().out


def test_analysis_upload_failure_is_best_effort_but_delete_failure_propagates(monkeypatch, capsys):
    drive = run_mocked(monkeypatch, [{"text": "hello"}])
    drive.reset_mock()
    def upload(content, name, folder):
        if name == "analysis_main.md":
            raise ValueError("offline")
    drive.upload_string.side_effect = upload
    pipeline.run_for_url(URL, drive)
    assert [c.args[1] for c in drive.upload_string.call_args_list] == [
        "transcript_raw.json", "transcript_clean.txt", "analysis_main.md"
    ]
    assert "⚠️ LLM analýza přeskočena (offline)" in capsys.readouterr().out
    drive.delete_file.side_effect = RuntimeError("delete failed")
    with pytest.raises(RuntimeError, match="delete failed"):
        pipeline.run_for_url(URL, drive)
    pipeline.embed_text.assert_not_called()
