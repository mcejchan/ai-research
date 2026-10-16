"""Load the pure pipeline slug owner relative to this script, regardless of cwd."""

import importlib.util
from pathlib import Path


_owner_path = Path(__file__).resolve().parents[1] / "youtube-transcript-pipeline" / "src" / "path_slugs.py"
_spec = importlib.util.spec_from_file_location("_kb_path_slugs", _owner_path)
_owner = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_owner)

slugify_path_segment = _owner.slugify_path_segment
slugify_title = _owner.slugify_title
