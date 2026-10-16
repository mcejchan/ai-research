"""Contract for the goal-006 follow-up's required final note."""

from pathlib import Path


def test_followup_records_slug_boundary_and_run_size():
    root = Path(__file__).resolve().parents[1]
    note = (root / "plans/checkpoints/task-ab931892-697e-4c5e-8c59-e74e624be651.checkpoint.md").read_text()

    for required in (
        "## Final note",
        "24 lines",
        "youtube-transcript-pipeline/src/path_slugs.py",
        "youtube-transcript-pipeline/src/yt_pipeline.py",
        "helper-scripts/normalize_kb_paths.py",
        "helper-scripts/rename_video_folders.py",
        "helper-scripts/_slug_owner.py",
        "slash and underscore",
        "80 characters",
    ):
        assert required in note
