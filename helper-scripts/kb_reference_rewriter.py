"""Shared recursive rewriting of references in knowledge-base text files."""

from pathlib import Path
from typing import List, Tuple


def rewrite_kb_references(ref_root: Path, patterns: List[Tuple[str, str]]) -> List[Path]:
    """Apply ordered replacements to supported KB files and return changed paths."""
    touched: List[Path] = []
    extensions = {".md", ".txt", ".json", ".csv"}
    for file in ref_root.rglob("*"):
        if not file.is_file() or file.suffix.lower() not in extensions:
            continue
        try:
            text = file.read_text(encoding="utf-8")
        except Exception:
            continue
        new_text = text
        for old, new in patterns:
            new_text = new_text.replace(old, new)
        if new_text != text:
            file.write_text(new_text, encoding="utf-8")
            touched.append(file)
    return touched
