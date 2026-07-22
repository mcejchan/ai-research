import os
from pathlib import Path
import subprocess
import sys


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
