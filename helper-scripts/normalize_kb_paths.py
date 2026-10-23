#!/usr/bin/env python3
"""
Normalize local-knowledge-base/youtube channel paths to ASCII/kebab-case
and update references in text files. Designed to be run locally (mock mode).
"""

import argparse
import urllib.parse
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from _slug_owner import slugify_path_segment
from kb_reference_rewriter import rewrite_kb_references


def find_channels(root: Path) -> List[Path]:
    return [p for p in root.iterdir() if p.is_dir()]


def replacement_patterns(old: str, new: str) -> List[Tuple[str, str]]:
    """Generate common string replacements for old->new path segments."""
    quoted_old = urllib.parse.quote(old)
    patterns = []
    bases = [
        "youtube/",
        "../youtube/",
        "local-knowledge-base/youtube/",
    ]
    for base in bases:
        patterns.append((f"{base}{old}", f"{base}{new}"))
        patterns.append((f"{base}{quoted_old}", f"{base}{new}"))
    return patterns


def rename_channels(root: Path, allowed: Iterable[str], dry_run: bool) -> Dict[str, str]:
    """Rename channel directories; return mapping old->new for changes applied."""
    applied: Dict[str, str] = {}
    allowed_set = set(allowed) if allowed else None
    for chan_dir in find_channels(root):
        if allowed_set and chan_dir.name not in allowed_set:
            continue
        slug = slugify_path_segment(chan_dir.name)
        if slug == chan_dir.name:
            continue
        target = chan_dir.parent / slug
        if target.exists() and not target.samefile(chan_dir):
            print(f"⚠️ Target already exists, skipping: {chan_dir} -> {target}")
            continue
        print(f"{'DRY-RUN' if dry_run else 'RENAME'}: {chan_dir.name} -> {slug}")
        if not dry_run:
            # Handle case-only renames on case-insensitive FS by using a temp hop
            if target.exists() and target.samefile(chan_dir):
                temp = chan_dir.parent / f"{slug}__tmpcase__"
                chan_dir.rename(temp)
                temp.rename(target)
            else:
                chan_dir.rename(target)
        applied[chan_dir.name] = slug
    return applied


def main():
    parser = argparse.ArgumentParser(description="Normalize channel folder names and update references.")
    parser.add_argument("--root", default="local-knowledge-base/youtube", help="Path to youtube root")
    parser.add_argument("--refs-root", default="local-knowledge-base", help="Root for reference updates")
    parser.add_argument("--only", nargs="*", help="Channel names to process (defaults to all)")
    parser.add_argument("--apply", action="store_true", help="Actually rename; otherwise dry-run")
    parser.add_argument("--no-update-refs", action="store_true", help="Skip reference updates")
    args = parser.parse_args()

    yt_root = Path(args.root).resolve()
    ref_root = Path(args.refs_root).resolve()

    if not yt_root.exists():
        raise SystemExit(f"Youtube root not found: {yt_root}")

    mapping = rename_channels(yt_root, args.only or [], dry_run=not args.apply)
    if not mapping:
        print("No channel names needed normalization.")
        return

    if not args.apply:
        print("Dry-run only; skipping reference updates.")
        return

    if args.no_update_refs:
        return

    patterns = []
    for old, new in mapping.items():
        patterns.extend(replacement_patterns(old, new))

    touched = rewrite_kb_references(ref_root, patterns)
    print(f"Updated references in {len(touched)} files.")


if __name__ == "__main__":
    main()
