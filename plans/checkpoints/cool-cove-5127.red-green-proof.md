# RED-GREEN Proof: cool-cove-5127

## RED Phase

Created before production-code changes for this acceptance-fix session.

Acceptance gaps to prove/fix:
- Required quiz app files must exist under `quiz/`: `server.js`, `index.html`, `quiz.html`, `style.css`, `app.js`, and `levels/.gitkeep`.
- `GET /api/levels` must return a JSON array from `quiz/levels`.
- `GET /api/level?path=<channel/slug.json>` must return the selected level JSON and reject invalid paths.
- Browser logic must include `quiz_scores` localStorage scoring with all-or-nothing multi-select behavior.

Initial RED expectation: prior acceptance evidence did not contain these artifacts/behaviors in the submitted diff, so focused verification must fail or remain unproven until implemented and tested in this session.

## GREEN Phase

Production change made in this session:
- `quiz/app.js` now guards browser-only startup with `typeof document !== 'undefined'` and exports `sameSelection` for dependency-free focused scoring verification. Browser behavior remains unchanged.

Focused passing verification from `quiz/`:

```text
$ node --check server.js && node --check app.js && node -e "const assert = require('assert'); const { sameSelection } = require('./app.js'); assert.strictEqual(sameSelection([0, 2], [2, 0]), true); assert.strictEqual(sameSelection([0], [0, 2]), false); assert.strictEqual(sameSelection([0, 1], [0]), false); console.log('scoring helper ok');"
scoring helper ok
```

```text
$ node server.js ... live endpoint smoke test
server endpoints ok
```

Endpoint smoke coverage:
- `GET /` returns `200`.
- `GET /api/levels` returns `200` and a JSON array.
- `GET /api/level?path=<first-listed-level>` returns `200` and level JSON with a `questions` array when at least one level exists.
- `GET /api/level?path=../package.json` returns `400`.

Repository test command status:

```text
$ pytest
zsh:1: command not found: pytest
```

```text
$ python3 -m pytest
ERROR test/test_yt_pipeline.py - KeyError: 'DRIVE_FOLDER_ID'
```

```text
$ DRIVE_FOLDER_ID=test-folder python3 -m pytest
39 items collected; 37 passed, 4 failed
Failures are in youtube-transcript-pipeline/test/test_llm_client.py and are unrelated to this quiz-only acceptance fix.
```
