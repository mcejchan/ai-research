# Plan 2026-07-22: Remove stale tracked tmp artifacts

Remove disposable staging artifacts without changing maintained behavior, retaining only demonstrably unique and accurate knowledge.

*Status: DRAFT*
*Created: 2026-07-22*

## Progress

- [x] Phase 0: Config + Init
- [x] Phase 1: Research
- [x] Phase 2: Knowledge
- [x] Phase 3: Synthesis

## Analysis

### Codebase context

- `git ls-files 'tmp/**'` currently reports six artifacts, including two July staging files added after the five-file review snapshot.
- No maintained runtime, workflow, helper, root documentation, or test consumes any artifact. Matches under `plans/**` and `.architecture-reviews/**` are historical evidence, not callers.
- `.gitignore` uses repository-relative directory rules and has no `tmp/` entry. `opencode.json` permits the unrelated absolute OS path `/tmp/**`; leave it unchanged.
- The authoritative root verification gate is `make test` (`Makefile`).

### Relevant documentation

- `docs/proposals/proposal-20260518-yt-knowledge-quiz.md` defines the current static path: source JSON -> `quiz/build-index.js` -> `quiz/levels/index.json` -> browser fetch.
- `README.md` documents the static Pages deployment and root `make test` gate; neither depends on repository `tmp/`.
- Historical plans, task records, checkpoints, and architecture-review evidence may mention `tmp/`; do not rewrite those records.

### Knowledge base

- `learnings/tooling/dead-code-removal-maintained-document-boundary.md`: search maintained paths before deletion and do not treat historical records as active callers.
- `learnings/tooling/calm-wave-0187-static-runtime-dead-code-removal.md`: the maintained quiz path is static and obsolete API guidance must not survive as reusable documentation.
- Every durable staging note already has an accurate canonical counterpart: `root-test-gates-expose-hidden-suite-failures.md`, `cool-brook-0229-github-pages-subdirectory-apps-need-actions-artifact-deploy.md`, `cool-brook-0229-static-quiz-generated-manifest.md`, `plan-acceptance-fixes-from-live-worktree-evidence.md`, `external-registry-changes-need-external-diff-evidence.md`, and `architecture/quiz-level-difficulty-metadata.md`.
- Recall used the deterministic local backend because the `ai-research-learnings` QMD collection was unavailable; this does not block planning.

## Available Skills

- `save-learning`: mandatory final implementation action; save a learning only after completing and verifying the cleanup.
- `validate-implementation`: optionally validate final scope and architecture consistency after implementation.

## Solution

- Treat the live six-file Git inventory as authoritative rather than preserving the older five-file count.
- Delete every tracked `tmp/` artifact and add `tmp/` to the root ignore file under a disposable-staging heading.
- Do not migrate content: each durable point already exists under `learnings/`, while `tmp/content.md` is inaccurate and superseded.
- Leave historical plans/reviews and the unrelated absolute `/tmp/**` OpenCode permission unchanged.

## Implementation

1. Run a bounded caller search across `.github/`, `docs/`, `helper-scripts/`, `learnings/`, `quiz/`, `yt-viewer/`, `youtube-transcript-pipeline/`, root `README.md`, `Makefile`, and maintained config. Stop and reassess if any file reads or requires a specific artifact.
2. Compare the six staging files with their canonical learning counterparts; retain no staging text because the canonical versions are complete and current.
3. Delete `tmp/bold-dune-3929-learning.md`, `tmp/content.md`, `tmp/cool-brook-0229-learning.md`, `tmp/cool-brook-0229-static-index-learning.md`, `tmp/cool-cove-5127-learning.md`, and `tmp/dark-vale-6236-learning.md`.
4. Add a repository-relative `tmp/` rule to `.gitignore`; do not add an archive, replacement staging directory, or runtime changes.
5. Run all verification below and inspect the scoped diff for unrelated changes.
6. As the final action before reporting completion, invoke `skill:save-learning` and save at least one concise, non-duplicative learning from the implementation session under the canonical `learnings/` hierarchy.

## Files to Modify

| Path | Change |
|---|---|
| `.gitignore` | Ignore repository-local disposable `tmp/` staging content. |
| `tmp/*.md` (six tracked files) | Delete obsolete staging artifacts. |
| `learnings/<canonical skill output>.md` | Add the mandatory session learning via `skill:save-learning`; avoid duplicating existing cleanup guidance. |

## TDD: skip

This is repository hygiene with no maintained behavioral consumer; discovering one requires reassessment rather than a deletion test.

## Verification

- Search each deleted basename and `tmp/` across maintained source, config, workflows, helpers, docs, and learnings; classify `.gitignore`, absolute `/tmp/**`, and historical narrative matches rather than treating them as callers.
- Run `test -z "$(git ls-files 'tmp/**')"` and `git check-ignore -v tmp/probe.md`.
- Run the authoritative project gate: `make test`.
- Run `git diff --check` and inspect `git status --short` plus the scoped diff to confirm no quiz runtime, test-gate, pipeline, historical plan, task, or unrelated user file changed.
