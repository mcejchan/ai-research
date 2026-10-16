"""Dependency-free filesystem slug rules shared by the pipeline and helpers."""

import re
import unicodedata


def _normalize(text: str, *, path_segment: bool) -> str:
    normalized = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode()
    if path_segment:
        normalized = normalized.replace("/", " ").replace("_", " ")
    normalized = normalized.lower().strip()
    normalized = re.sub(r"[^\w\s-]", "", normalized)
    return re.sub(r"[\s-]+", "-", normalized).strip("-")


def slugify_path_segment(text: str, fallback: str = "unknown") -> str:
    """Normalize a channel/path segment; separators become word boundaries."""
    return _normalize(text, path_segment=True) or fallback


def slugify_title(title: str, max_length: int = 80) -> str:
    """Keep title underscores, discard slashes, and return empty for empty slugs."""
    return _normalize(title, path_segment=False)[:max_length]
