#!/usr/bin/env python3
"""
Rename video folders under local-knowledge-base/youtube from date_VIDEOID
to date_title-slug (ASCII kebab-case) and update references in KB files.
"""

import argparse
import re
import unicodedata
import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


def slugify_title(title: str, max_length: int = 80) -> str:
    normalized = unicodedata.normalize("NFKD", title or "").encode("ascii", "ignore").decode()
    normalized = normalized.lower().strip()
    normalized = re.sub(r"[^\w\s-]", "", normalized)
    normalized = re.sub(r"[\s-]+", "-", normalized).strip("-")
    return normalized[:max_length] if normalized else ""


def get_video_title(folder: Path) -> str:
    """Read first markdown heading in analysis_main.md."""
    analysis = folder / "analysis_main.md"
    if not analysis.exists():
        return ""
    for line in analysis.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def load_index_titles(index_path: Path) -> Dict[str, str]:
    """Parse INDEX.md table rows to map 'channel/folder' -> title."""
    if not index_path.exists():
        return {}
    titles: Dict[str, str] = {}
    row_re = re.compile(
        r"^\|\s*\d{4}-\d{2}-\d{2}\s*\|\s*(?P<title>.+?)\s*\|.*?\[Analýza\]\(youtube/(?P<rel>[^)]+?)/analysis_main\.md\)",
        re.UNICODE,
    )
    for line in index_path.read_text(encoding="utf-8").splitlines():
        m = row_re.match(line)
        if not m:
            continue
        rel = m.group("rel").strip()
        # rel already contains channel/folder
        titles[rel] = m.group("title").strip()
    return titles


def replacement_patterns(channel: str, old: str, new: str) -> List[Tuple[str, str]]:
    bases = [
        f"youtube/{channel}/",
        f"../youtube/{channel}/",
        f"local-knowledge-base/youtube/{channel}/",
    ]
    return [(f"{base}{old}", f"{base}{new}") for base in bases]


def update_references(ref_root: Path, patterns: List[Tuple[str, str]]) -> List[Path]:
    touched: List[Path] = []
    exts = {".md", ".txt", ".json", ".csv"}
    for file in ref_root.rglob("*"):
        if not file.is_file() or file.suffix.lower() not in exts:
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


def rename_videos(
    yt_root: Path,
    allowed_channels: Iterable[str],
    apply: bool,
    index_titles: Dict[str, str],
) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for channel_dir in yt_root.iterdir():
        if not channel_dir.is_dir():
            continue
        if allowed_channels and channel_dir.name not in allowed_channels:
            continue
        for vid_dir in channel_dir.iterdir():
            if not vid_dir.is_dir():
                continue
            parts = vid_dir.name.split("_", 1)
            if len(parts) != 2:
                continue
            date_prefix, suffix = parts
            rel = f"{channel_dir.name}/{vid_dir.name}"
            title = get_video_title(vid_dir)
            if not title:
                title = index_titles.get(rel, "")
            slug = slugify_title(title) or suffix
            new_name = f"{date_prefix}_{slug}"
            if new_name == vid_dir.name:
                continue
            target = vid_dir.parent / new_name
            if target.exists() and not target.samefile(vid_dir):
                print(f"⚠️ target exists, skip: {vid_dir} -> {target}")
                continue
            print(f"{'RENAME' if apply else 'DRY-RUN'}: {vid_dir} -> {target}")
            if apply:
                # case-insensitive hop
                if target.exists() and target.samefile(vid_dir):
                    temp = vid_dir.parent / f"{new_name}__tmpcase__"
                    vid_dir.rename(temp)
                    temp.rename(target)
                else:
                    vid_dir.rename(target)
            mapping[str(vid_dir.relative_to(yt_root))] = str(target.relative_to(yt_root))
    return mapping


def main():
    parser = argparse.ArgumentParser(description="Rename video folders to use title slug instead of video ID.")
    parser.add_argument("--root", default="local-knowledge-base/youtube", help="Path to youtube root")
    parser.add_argument("--refs-root", default="local-knowledge-base", help="Root for reference updates")
    parser.add_argument("--index", default="local-knowledge-base/INDEX.md", help="Path to INDEX.md for title lookup")
    parser.add_argument("--only-channels", nargs="*", help="Limit to specific channel directories")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default dry-run)")
    args = parser.parse_args()

    yt_root = Path(args.root).resolve()
    ref_root = Path(args.refs_root).resolve()
    if not yt_root.exists():
        raise SystemExit(f"Youtube root not found: {yt_root}")

    index_titles = load_index_titles(Path(args.index))
    mapping = rename_videos(yt_root, args.only_channels or [], apply=args.apply, index_titles=index_titles)
    if not mapping:
        print("No renames needed.")
        return

    if not args.apply:
        print("Dry-run; references not updated.")
        return

    patterns: List[Tuple[str, str]] = []
    for old_rel, new_rel in mapping.items():
        channel = old_rel.split("/")[0]
        old_leaf = "/".join(old_rel.split("/")[1:])
        new_leaf = "/".join(new_rel.split("/")[1:])
        patterns.extend(replacement_patterns(channel, old_leaf, new_leaf))

    touched = update_references(ref_root, patterns)
    print(f"Updated references in {len(touched)} files.")


if __name__ == "__main__":
    main()
