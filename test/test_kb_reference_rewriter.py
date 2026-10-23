from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parents[1] / "helper-scripts"
sys.path.insert(0, str(SCRIPTS))
from kb_reference_rewriter import rewrite_kb_references


def test_filters_extensions_and_reports_only_changed_files(tmp_path):
    md = tmp_path / "ref.MD"
    md.write_text("youtube/old", encoding="utf-8")
    unchanged = tmp_path / "same.txt"
    unchanged.write_text("nothing", encoding="utf-8")
    ignored = tmp_path / "data.bin"
    ignored.write_text("youtube/old", encoding="utf-8")

    touched = rewrite_kb_references(tmp_path, [("youtube/old", "youtube/new")])

    assert touched == [md]
    assert md.read_text(encoding="utf-8") == "youtube/new"
    assert unchanged.read_text(encoding="utf-8") == "nothing"
    assert ignored.read_text(encoding="utf-8") == "youtube/old"


def test_applies_replacements_in_order(tmp_path):
    ref = tmp_path / "ref.json"
    ref.write_text("old", encoding="utf-8")

    assert rewrite_kb_references(tmp_path, [("old", "middle"), ("middle", "new")]) == [ref]
    assert ref.read_text(encoding="utf-8") == "new"


def test_skips_unreadable_files_and_continues(tmp_path, monkeypatch):
    unreadable = tmp_path / "unreadable.csv"
    unreadable.write_text("old", encoding="utf-8")
    readable = tmp_path / "readable.txt"
    readable.write_text("old", encoding="utf-8")
    original_read_text = Path.read_text

    def selective_read_text(file, *args, **kwargs):
        if file == unreadable:
            raise PermissionError("denied")
        return original_read_text(file, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", selective_read_text)
    assert rewrite_kb_references(tmp_path, [("old", "new")]) == [readable]
    assert readable.read_text(encoding="utf-8") == "new"
