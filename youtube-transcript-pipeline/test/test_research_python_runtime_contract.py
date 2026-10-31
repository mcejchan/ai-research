import os
from pathlib import Path
import shlex
import subprocess
import sys
import textwrap

import pytest


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
        "print('PYTEST_EXECUTABLE:' + sys.executable)\n"
        "print('PYTEST_IMPLEMENTATION:' + platform.python_implementation())\n"
        "print('PYTEST_VERSION:' + '.'.join(map(str, sys.version_info[:2])))\n"
        "print('PYTEST_SENTINEL')\n"
    )
    (root / ".python-version").write_text("3.15\n")
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
    stable_link = tmp_path / "stable-python"
    stable_link.symlink_to(Path(sys.executable))
    runtime = root / ".venv" / "bin" / "python"
    runtime.unlink()
    runtime.symlink_to(stable_link)
    result = _run(root, hostile, tmp_path)
    observed = next(
        line.removeprefix("PYTEST_EXECUTABLE:")
        for line in result.stdout.splitlines()
        if line.startswith("PYTEST_EXECUTABLE:")
    )
    assert os.path.realpath(observed) == os.path.realpath(sys.executable)
    assert "PYTEST_IMPLEMENTATION:CPython" in result.stdout
    assert "PYTEST_VERSION:3.15" in result.stdout
    assert "PYTEST_SENTINEL" in result.stdout
    assert "HOSTILE_PYTHON_SELECTED" not in result.stdout + result.stderr
    assert result.returncode == 0


def test_make_test_fails_actionably_when_project_runtime_is_missing(tmp_path):
    root, hostile = _synthetic_checkout(tmp_path, Path(sys.executable))
    (root / ".venv" / "bin" / "python").unlink()
    result = _run(root, hostile, tmp_path)
    assert result.returncode != 0
    assert "CPython 3.15.x" in result.stderr
    assert "HOSTILE_PYTHON_SELECTED" not in result.stdout + result.stderr


def test_make_test_propagates_pytest_arguments_and_failure_status(tmp_path):
    root, hostile = _synthetic_checkout(tmp_path, Path(sys.executable))
    runtime = root / ".venv" / "bin" / "python"
    runtime.unlink()
    _write_executable(runtime, f"""#!/bin/sh
        if [ "$1" = "-c" ]; then
          exec {shlex.quote(sys.executable)} -c "$2"
        fi
        printf 'PYTEST_ARGS:' >&2
        printf ' <%s>' "$@" >&2
        printf '\\n' >&2
        exit 23
    """)
    result = _run(root, hostile, tmp_path)
    assert result.returncode != 0
    assert "Error 23" in result.stderr
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
    assert "expected CPython 3.15.x, got PyPy 3.15.0" in result.stderr
    assert "HOSTILE_PYTHON_SELECTED" not in result.stdout + result.stderr
    assert "PYTEST_SENTINEL" not in result.stdout + result.stderr


def test_repository_python_pin_selects_minor_series():
    assert (REPOSITORY_ROOT / ".python-version").read_text().strip() == "3.15"


@pytest.mark.parametrize("identity, accepted", [
    ("CPython 3.15.0", True),
    ("CPython 3.15.7", True),
    ("CPython 3.14.4", False),
    ("PyPy 3.15.7", False),
    ("CPython 3.15.", False),
    ("CPython 3.15.7rc1", False),
    ("CPython 3.15.7.1", False),
])
def test_make_test_runtime_patch_contract(tmp_path, identity, accepted):
    root, hostile = _synthetic_checkout(tmp_path, Path(sys.executable))
    runtime = root / ".venv" / "bin" / "python"
    runtime.unlink()  # Never write through a host-interpreter symlink.
    _write_executable(runtime, f'''#!/bin/sh
        if [ "$1" = "-c" ]; then
          printf '%s\\n' '{identity}'
          exit 0
        fi
        printf 'PYTEST_SENTINEL\\n'
        exit 0
    ''')
    result = _run(root, hostile, tmp_path)
    output = result.stdout + result.stderr
    assert (result.returncode == 0) is accepted
    assert ("PYTEST_SENTINEL" in output) is accepted
    assert "HOSTILE_PYTHON_SELECTED" not in output
    if not accepted:
        assert f"expected CPython 3.15.x, got {identity}" in result.stderr
