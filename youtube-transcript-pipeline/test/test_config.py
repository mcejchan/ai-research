import os
from pathlib import Path
import subprocess
import sys

import pytest


def test_pipeline_import_does_not_require_drive_folder_id():
    env = os.environ.copy()
    env.pop("DRIVE_FOLDER_ID", None)
    command = (
        "from unittest.mock import patch\n"
        "with patch('dotenv.load_dotenv', return_value=False):\n"
        "    import src.yt_pipeline\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", command],
        cwd=Path(__file__).resolve().parents[1],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr


def test_real_drive_requires_folder_id_at_execution(monkeypatch):
    from src.yt_pipeline import run_for_url

    class RealDrive:
        mock_mode = False

    monkeypatch.delenv("DRIVE_FOLDER_ID", raising=False)

    with pytest.raises(RuntimeError, match="DRIVE_FOLDER_ID"):
        run_for_url("https://youtu.be/example", RealDrive())


PIPELINE_ROOT = Path(__file__).resolve().parents[1]


def _load_pipeline_pytest_config():
    return pytest.Config.fromdictargs(
        {},
        ["-c", str(PIPELINE_ROOT / "pytest.ini")],
    )


def test_pytest_ini_section_is_read_by_pytest():
    cfg = _load_pipeline_pytest_config()
    addopts = cfg.getini("addopts")
    assert "--cov=src" in addopts
    assert cfg.getini("testpaths") == ["test"]


def test_pytest_ini_env_block_present():
    cfg = _load_pipeline_pytest_config()
    env = cfg.getini("env")
    assert "USE_WHISPER_FALLBACK = false" in env
