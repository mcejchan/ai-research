import os
from pathlib import Path
import subprocess
import sys
import textwrap


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def _write_executable(path: Path, contents: str) -> None:
    path.write_text(textwrap.dedent(contents))
    path.chmod(0o755)


def _synthetic_checkout(tmp_path: Path, real_python: Path) -> tuple[Path, Path]:
    root = tmp_path / "checkout"
    (root / "youtube-transcript-pipeline").mkdir(parents=True)
    (root / "Makefile").write_bytes((REPOSITORY_ROOT / "Makefile").read_bytes())
    hostile = tmp_path / "hostile-bin"
    hostile.mkdir()
    _write_executable(hostile / "python3", """
        #!/bin/sh
        echo HOSTILE_PYTHON_SELECTED
        exit 97
    """)
    for command in ("node", "quiz-stub"):
        _write_executable(hostile / command, "#!/bin/sh\nexit 0\n")
    runtime = root / ".venv" / "bin" / "python"
    runtime.parent.mkdir(parents=True)
    runtime.symlink_to(real_python.resolve())
    (root / "youtube-transcript-pipeline" / "pytest.py").write_text(
        "import platform, sys\n"
        "print(sys.executable)\n"
        "print(platform.python_implementation(), sys.version)\n"
        "print('PYTEST_SENTINEL')\n"
    )
    (root / ".python-version").write_text("3.15.0\n")
    return root, hostile


def _run(root: Path, hostile: Path, cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PATH"] = f"{hostile}{os.pathsep}{env['PATH']}"
    return subprocess.run(
        ["make", "-C", str(root), "test"], cwd=cwd, env=env,
        capture_output=True, text=True, check=False,
    )


def test_make_test_uses_real_python_315_and_runs_pytest_child(tmp_path):
    root, hostile = _synthetic_checkout(tmp_path, Path(sys.executable))
    result = _run(root, hostile, tmp_path)
    assert str(Path(sys.executable).resolve()) in result.stdout
    assert "CPython 3.15.0" in result.stdout
    assert "PYTEST_SENTINEL" in result.stdout
    assert "HOSTILE_PYTHON_SELECTED" not in result.stdout + result.stderr
    assert result.returncode == 0


def test_make_test_fails_actionably_when_project_runtime_is_missing(tmp_path):
    root, hostile = _synthetic_checkout(tmp_path, Path(sys.executable))
    (root / ".venv" / "bin" / "python").unlink()
    result = _run(root, hostile, tmp_path)
    assert result.returncode != 0
    assert "3.15.0" in result.stderr
    assert "HOSTILE_PYTHON_SELECTED" not in result.stdout + result.stderr


def test_make_test_propagates_pytest_arguments_and_failure_status(tmp_path):
    root, hostile = _synthetic_checkout(tmp_path, Path(sys.executable))
    runtime = root / ".venv" / "bin" / "python"
    runtime.unlink()
    _write_executable(runtime, f"""#!/bin/sh
        if [ "$1" = "-c" ]; then
          exec "{Path(sys.executable).resolve()}" -c "$2"
        fi
        printf 'PYTEST_ARGS:' >&2
        printf ' <%s>' "$@" >&2
        printf '\\n' >&2
        exit 23
    """)
    result = _run(root, hostile, tmp_path)
    assert result.returncode == 23
    assert "PYTEST_ARGS: <-m> <pytest>" in result.stderr
    assert "HOSTILE_PYTHON_SELECTED" not in result.stdout + result.stderr


def test_make_test_rejects_stale_project_runtime_without_fallback(tmp_path):
    root, hostile = _synthetic_checkout(tmp_path, Path(sys.executable))
    runtime = root / ".venv" / "bin" / "python"
    runtime.unlink()
    _write_executable(runtime, """
        #!/bin/sh
        echo 'PyPy 3.15.0'
        exit 0
    """)
    result = _run(root, hostile, tmp_path)
    assert result.returncode != 0
    assert "expected CPython 3.15.0, got PyPy 3.15.0" in result.stderr
    assert "HOSTILE_PYTHON_SELECTED" not in result.stdout + result.stderr
    assert "PYTEST_SENTINEL" not in result.stdout + result.stderr
