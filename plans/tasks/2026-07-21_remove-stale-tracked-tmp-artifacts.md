# Remove stale tracked tmp artifacts

## Context
Five committed files under `tmp/` are agent/task staging artifacts rather than maintained project inputs or outputs. Maintained-code searches found no reader, and their history ends in May 2026. `tmp/content.md` still claims the quiz browser renders from `/api/levels`, contradicting the static architecture introduced by commit `8b90375`. Durable learning material already has a canonical home under `learnings/`; Git history preserves deleted staging files.

## Required change
- Remove the tracked files under `tmp/` after confirming they have no maintained caller.
- Add the repository-appropriate ignore rule so disposable `tmp/` staging content is not committed again.
- If any genuinely durable, unique knowledge exists only in `tmp/`, move only that unique information into the existing canonical `learnings/` structure; do not copy stale task prose or duplicate existing material.
- Remove maintained references that incorrectly treat `tmp/` as project-owned documentation.

## Constraints
- Do not create a replacement archive or new staging system.
- Do not rewrite historical commits.
- Do not edit unrelated quiz runtime, test-gate, or pipeline behavior.
- Do not preserve stale architecture claims merely as documentation history; Git already serves that purpose.

## Acceptance criteria
- No tracked files remain under `tmp/`.
- Disposable `tmp/` content is ignored according to existing repository conventions.
- Maintained code and documentation have no dependency on removed files.
- Any retained learning is unique, accurate, and located under the existing canonical `learnings/` hierarchy.
- Existing relevant tests pass and final diff contains no unrelated cleanup.

## TDD stance
This is repository hygiene, not new behavior. No new test is required unless a maintained consumer is discovered; if one exists, stop and reassess rather than deleting its input blindly.

## Verify
- Search maintained source/config/docs for references to each removed file and to `tmp/` as a required path.
- Confirm with Git that no files under `tmp/` remain tracked.
- Run the project's current available test suites or the root gate if established by an earlier batch task.
- Run `git diff --check`.
