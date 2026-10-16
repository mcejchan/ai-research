# Tech debt: decompose YouTube processing and unify path slug ownership

## Assessment

**Decision: `create`.**

Current source inspection confirms both findings are live. `youtube-transcript-pipeline/src/yt_pipeline.py` has 270 lines and its current AST reports `run_for_url` at lines 185–248 (64 lines), above the function-length warning threshold. The function combines destination construction, transcript fallback, serialization/uploads, best-effort LLM analysis, raw-file cleanup, and optional embeddings.

The reported duplication is also present: `slugify_path_segment` in `youtube-transcript-pipeline/src/yt_pipeline.py:128–135` and `helper-scripts/normalize_kb_paths.py:15–25` implement the same NFKD/ASCII, separator replacement, lowercase, regex cleanup, hyphen collapse, and fallback contract. A third related title-slug implementation exists in `helper-scripts/rename_video_folders.py`, so ownership should be decided deliberately rather than creating another copy.

Current pipeline status shows no unfinished `ai-research`, `yt_pipeline.py`, or YouTube-transcript task to reuse or queue behind. This is a fresh current scope.

## Objective

Make `run_for_url` a short, readable workflow coordinator and establish one repository-local owner for filesystem/path slug normalization used by the pipeline and maintenance helpers, without changing storage paths, Drive behavior, transcript fallback, analysis tolerance, or optional embedding behavior.

## Required approach

Use characterization-first refactoring:

1. Run the focused YouTube pipeline tests before production edits. Add tests first for behavior that existing tests do not pin, especially cleanup ordering, transcript-object serialization, analysis truncation, and embedding gating.
2. Extract cohesive workflow helpers from `run_for_url`, with explicit inputs and side effects. Suitable seams include transcript acquisition with Whisper fallback, conversion/upload of transcript artifacts, best-effort analysis upload, and optional embedding metadata upload. Keep `run_for_url(url, drive)` as the stable public coordinator.
3. Create one import-safe shared slug module at a repository location usable by both the packaged pipeline and standalone helper scripts without executing pipeline environment loading or importing heavy/network dependencies. Rewire the actual callers and remove duplicate implementations in the same slice.
4. Preserve existing public imports from `src.yt_pipeline` if tests or callers depend on `slugify_title` / `slugify_path_segment`; compatibility re-export is acceptable, but implementation ownership must be singular.
5. Decide whether the title-slug helper can safely share the same primitive. Consolidate it only if its distinct slash/underscore and empty-fallback semantics remain explicit and tested; otherwise document why it remains separate. Do not broaden scope into unrelated knowledge-base migration logic.
6. Keep all verification hermetic. Do not call YouTube, Google Drive, Whisper model downloads, OpenAI, or any other external service.

## Behavioral invariants

Preserve with focused regression evidence:

- `DRIVE_FOLDER_ID` is required only outside Drive mock mode;
- video ID and metadata are resolved once, channel paths remain ASCII/kebab-case, title slugs retain their current 80-character bound, and folder naming remains `<current-date>_<title-slug-or-video-id>` under `youtube/<channel>/...`;
- transcript language preference remains Czech then English, with Whisper fallback only when transcript retrieval fails and `USE_WHISPER` is enabled;
- segment objects and dictionaries serialize to the same `transcript_raw.json` shape/default values, and cleaned text remains unchanged;
- `transcript_raw.json` and `transcript_clean.txt` upload names/content remain stable;
- analysis input is capped at 25,000 characters with the same truncation marker, intent, language, metadata context, upload filename, and best-effort failure behavior;
- raw transcript deletion occurs at the same workflow point and retains its current failure behavior;
- embeddings remain controlled by `MAKE_EMBED`, use the full cleaned text, and upload the same minimal `vectors.json` metadata;
- `normalize_kb_paths.py` retains dry-run/apply behavior and produces byte-for-byte equivalent slugs for existing inputs;
- importing the shared slug owner has no environment, network, Drive, LLM, or CLI side effects.

Do not silently change print/output text, exception propagation boundaries, Drive call order, path formats, or configuration semantics merely to simplify the function.

## Acceptance criteria

- `run_for_url` is below the configured function-length warning threshold and reads as a clear workflow coordinator.
- The duplicated path-slug algorithm has one implementation owner; `yt_pipeline.py` and `normalize_kb_paths.py` call it rather than carrying copies.
- The shared owner’s placement/import mechanism is simple and works from both documented execution contexts; no runtime `sys.path` trick tied to the caller’s current directory is introduced.
- Existing import contracts remain compatible or are explicitly migrated with tests.
- Focused tests cover extracted orchestration seams and cross-caller slug equivalence, including Unicode, slash/underscore, punctuation-only fallback, repeated separators, and title length behavior.
- Focused and broader offline test suites pass. The final note records exact commands/results, resulting `run_for_url` line count, the chosen slug owner, rewired callers, and any deliberately retained distinct title behavior.

## Verification

At minimum run the project’s canonical environment equivalents of:

```text
cd youtube-transcript-pipeline && python -m pytest test/test_yt_pipeline.py test/test_config.py -q
cd youtube-transcript-pipeline && python -m pytest -q
```

Add/run focused tests for the standalone normalization helper and the shared slug owner from the repository root. Also run configured lint/type/static checks if present. No live integrations are authorized.
