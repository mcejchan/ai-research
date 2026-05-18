# RED-GREEN Proof: cool-cove-5127

## RED Phase

Created before production-code changes for this acceptance-fix session.

Acceptance gaps to prove/fix:
- Required quiz app files must exist under `quiz/`: `server.js`, `index.html`, `quiz.html`, `style.css`, `app.js`, and `levels/.gitkeep`.
- `GET /api/levels` must return a JSON array from `quiz/levels`.
- `GET /api/level?path=<channel/slug.json>` must return the selected level JSON and reject invalid paths.
- Browser logic must include `quiz_scores` localStorage scoring with all-or-nothing multi-select behavior.

Initial RED expectation: prior acceptance evidence did not contain these artifacts/behaviors in the submitted diff, so focused verification must fail or remain unproven until implemented and tested in this session.
