# Plan 2026-07-22: Establish one project-level test gate

Create a root `make test` gate that composes the unchanged subsystem runners after fixing the quiz enum and lazy Drive configuration contracts.

*Status: DRAFT*

## Analysis

### Codebase context

- `quiz/build-index.js:27-42` accepts every truthy difficulty, while `quiz/app.js:94-99` and source manifests recognize only `extra-easy`, `easy`, and `hard`.
- `quiz/build-index.test.js:10-42` expects unknown `weird` to become `hard` but lacks an `extra-easy` fixture.
- `youtube-transcript-pipeline/src/yt_pipeline.py:20-23,186-196` reads `DRIVE_FOLDER_ID` at import even though it is used only when work starts.
- `.github/workflows/deploy-quiz.yml:27-38` builds and uploads without testing and does not install pipeline Python dependencies.
- The repository has no root test entrypoint; its existing command convention is Make.

### Documentation and learnings

- `README.md` is the appropriate location for the root health command and concise difficulty default.
- `docs/proposals/proposal-20260518-yt-knowledge-quiz.md` keeps the quiz dependency-free and separate from `yt-viewer`; no PlantUML diagram applies.
- `learnings/architecture/quiz-level-difficulty-metadata.md` requires preserving `extra-easy`; this task defines `hard` as the missing/unknown default.
- `learnings/architecture/self-contained-quiz-dashboard-without-dependencies.md` requires Node's built-in test runner.
- `learnings/test-failures/acceptance-verification-proxy-backed-llm-tests.md` favors `python3 -m pytest` over a global executable and records the Drive import coupling.
- Knowledge search used local fallback because collection `ai-research-learnings` was unavailable.

## Available Skills

- `tdd`: record RED/GREEN evidence for the quiz and Python contracts.
- `validate-implementation`: check completed wiring against project rules and acceptance criteria.

## Implementation

1. Follow `skill:tdd`: extend `quiz/build-index.test.js` with all three supported values plus unknown `weird`, and add `youtube-transcript-pipeline/test/test_config.py` proving `src.yt_pipeline` imports with both the process variable and dotenv loading disabled. Capture both RED failures before production edits.
2. In `quiz/build-index.js`, replace the truthy fallback with a closed check for `extra-easy`, `easy`, and `hard`; preserve those values and map missing or unknown values to `hard`.
3. In `youtube-transcript-pipeline/src/yt_pipeline.py`, remove the module-level `os.environ["DRIVE_FOLDER_ID"]` read. Resolve it when `run_for_url` begins: use the configured ID for Drive, allow the existing local/mock storage path without one, and raise a clear runtime error only for a real Drive client lacking the ID.
4. Add a root `Makefile` with one `.PHONY` `test` recipe that runs, in order, `node --test quiz/build-index.test.js`, `node --test yt-viewer/server.test.js`, then pipeline pytest from its directory with explicit non-secret test values and `python3 -m pytest`. Leave commands unguarded so Make stops and returns non-zero on failure.
5. Update `README.md` with `make test` as the repository health command, its three slices, and the quiz difficulty enum plus `hard` fallback.
6. Change `/Users/michal/.openclaw/workspace/skills/opencode-dev/projects.yaml` so `ai-research.testCommand` is `cd ~/Projects/ai-research && make test`; do not add another repository-wide command.
7. Add `node --test quiz/build-index.test.js` immediately after checkout in `.github/workflows/deploy-quiz.yml`. Keep this quiz-only preflight because the workflow does not install pipeline dependencies; build/upload/deploy remain downstream.
8. Run `skill:validate-implementation`, then execute the verification commands below.

## Files to Modify

| File | Change |
|---|---|
| `quiz/build-index.test.js` | Cover `extra-easy`, `easy`, `hard`, and unknown fallback. |
| `quiz/build-index.js` | Enforce the documented enum and default. |
| `youtube-transcript-pipeline/test/test_config.py` | Regress import without `DRIVE_FOLDER_ID`. |
| `youtube-transcript-pipeline/src/yt_pipeline.py` | Resolve Drive configuration lazily at execution. |
| `Makefile` | Add the sole root repository-health delegator. |
| `README.md` | Document the root command and difficulty contract. |
| `.github/workflows/deploy-quiz.yml` | Gate quiz build/upload on its maintained test. |
| `/Users/michal/.openclaw/workspace/skills/opencode-dev/projects.yaml` | Point `ai-research.testCommand` at root `make test`. |

## TDD

Implement the RED/GREEN cycle with `skill:tdd`; record evidence in `plans/checkpoints/bold-dune-3929.red-green-proof.md`.

### Quiz contract

**Test file:** `quiz/build-index.test.js`  
**Run command:** `node --test quiz/build-index.test.js`

Amend the existing metadata test to use these inputs and assertion:

```js
await fs.writeFile(path.join(channelDir, 'hard.json'), JSON.stringify({
  title: 'Hard', date: '2026-01-03', difficulty: 'hard', questions: [],
}));
await fs.writeFile(path.join(channelDir, 'extra-easy.json'), JSON.stringify({
  title: 'Extra Easy', date: '2026-01-02', difficulty: 'extra-easy', questions: [],
}));
await fs.writeFile(path.join(channelDir, 'easy.json'), JSON.stringify({
  title: 'Easy', date: '2026-01-01', difficulty: 'easy', questions: [],
}));
await fs.writeFile(path.join(channelDir, 'unknown.json'), JSON.stringify({
  title: 'Unknown', date: '2025-01-01', difficulty: 'weird', questions: [],
}));

const levels = await buildLevelsIndex(root, path.join(root, 'index.json'));
assert.deepEqual(
  Object.fromEntries(levels.map(({ title, difficulty }) => [title, difficulty])),
  { Hard: 'hard', 'Extra Easy': 'extra-easy', Easy: 'easy', Unknown: 'hard' },
); // RED: Unknown is currently "weird".
```

### Python configuration

**Test file:** `youtube-transcript-pipeline/test/test_config.py` (new)  
**Run command:** `cd youtube-transcript-pipeline && python3 -m pytest test/test_config.py`

```python
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
    assert result.returncode == 0, result.stderr  # RED: import raises KeyError.
```

| Test | RED | GREEN |
|---|---|---|
| Quiz supported/unknown matrix | Unknown remains `weird`. | Supported values survive; unknown becomes `hard`. |
| Import without Drive ID | Subprocess exits on `KeyError`. | Import exits zero; validation is deferred to execution. |

## Verification

- `node --test quiz/build-index.test.js`
- `node --test yt-viewer/server.test.js`
- `cd youtube-transcript-pipeline && OPENAI_API_KEY=test_openai_key LANG=cs USE_WHISPER_FALLBACK=false MAKE_EMBEDDINGS=false DRIVE_FOLDER_ID=test_folder_id python3 -m pytest`
- `make test` from repository root; confirm all three commands run and a non-zero child status is propagated.
- `ruby -e 'require "yaml"; YAML.parse_file(".github/workflows/deploy-quiz.yml")'`
- `rg -n -A 3 -B 3 'ai-research|testCommand' /Users/michal/.openclaw/workspace/skills/opencode-dev/projects.yaml` and confirm only the root gate is registered.
- `git diff --check`

Do not modify obsolete quiz API files or `tmp/`, and do not regenerate unrelated quiz content.
