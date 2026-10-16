# Plan: YouTube workflow and slug ownership

## Progress
- [x] Locate the canonical plan path and inspect current workflow and slug callers.
- [x] Check existing tests, packaging, documentation, and learnings.
- [x] Specify characterization-first changes and offline verification.

## Analysis
- `run_for_url` in `youtube-transcript-pipeline/src/yt_pipeline.py` mixes path creation, transcript fallback, uploads, best-effort analysis, cleanup, and embeddings; preserve the present call order.
- `helper-scripts/normalize_kb_paths.py` duplicates `slugify_path_segment`; `helper-scripts/rename_video_folders.py` duplicates title normalization with distinct slash/underscore behavior.
- `youtube-transcript-pipeline/test/test_yt_pipeline.py` already imports both slugs from `src.yt_pipeline` and patches its external-service functions; `test/test_config.py` asserts Drive-folder validation happens at execution, not import.
- `youtube-transcript-pipeline/README.md` documents `python -m src.yt_pipeline` from the pipeline directory; standalone scripts are executed by file path. There is no project PlantUML diagram relevant to this refactor.
- `learnings/architecture/success-only-optional-analysis-artifact.md`: absence of `analysis_main.md` is a completion signal; retain transcript on analysis failure. Root `Makefile` runs the canonical `make test` gate.

## Approach
- Characterize existing behavior before extracting orchestration helpers; assign slug ownership to a dependency-free module accessible from both execution contexts.
- Keep public `src.yt_pipeline.slugify_title` and `slugify_path_segment` as imported aliases. Implement the unbounded path slug and 80-character title slug in `src/path_slugs.py`, sharing a private normalization primitive but explicitly preserving path slash/underscore conversion and title empty-string fallback.
- In standalone helpers, load the module by a single small `helper-scripts/_slug_owner.py` adapter anchored to `__file__`, not `cwd` or `sys.path` mutation; both helper scripts import its re-exports.
- Keep `run_for_url(url, drive)` as the coordinator: validate folder ID; resolve ID/meta/date/path once; ensure path; acquire transcript (`cs`, `en`, Whisper only on exception and flag); clean text; upload raw JSON then clean text; attempt analysis/upload with the existing catch and prints; delete raw; optionally embed/upload metadata. Pass `drive`, folder ID, text, and metadata explicitly to helpers; leave module-level configuration read semantics intact.

## Implementation
1. Before production edits run `python -m pytest test/test_yt_pipeline.py test/test_config.py -q` from `youtube-transcript-pipeline/`; record baseline. Add characterization tests for object/dict raw serialization (missing object fields default to zero), exact clean-text bytes, path/Drive root, fallback enabled/disabled and empty-success behavior, analysis 25,000-character marker/context/printing and upload failure, delete ordering and propagation, embedding gating/full text/metadata and propagation.
2. Add RED tests for the new transcript-artifact seam and shared module (below), plus root-level parity tests for direct script use with different working directories. Implement `src/path_slugs.py` with a single private NFKD/ASCII/lowercase/punctuation/hyphen-collapse primitive; path-specific slash/underscore replacement and caller fallback; title-specific 80-character slice and empty-string fallback. Re-export via imports in `yt_pipeline.py`; use one file-relative `importlib.util.spec_from_file_location` adapter for the scripts, with no environment/service imports or `sys.path` changes.
3. Extract transcript acquisition, artifact upload, analysis attempt, and embedding upload into small helpers in `src/yt_pipeline.py`. Keep each helper's current exception boundary and printing; ensure raw deletion remains between analysis attempt and embeddings; preserve `run_for_url` patch points for existing tests (`fetch_transcript`, `analyze_text`, `embed_text`).
4. Rewire `normalize_kb_paths.py` and `rename_video_folders.py`; keep their direct CLI invocation and dry-run/apply behavior. Update any documentation only if an actual import or invocation contract changes. Count `run_for_url` AST start/end lines and confirm it is below the configured warning threshold.

## TDD
- Implement the RED/GREEN cycle per skill:tdd; create tests and capture a genuine failing focused run before any production refactor. Use the identical focused command for RED and GREEN, then run broader suites.
- Target: `youtube-transcript-pipeline/test/test_refactor_contracts.py` (new; pytest). Run from `youtube-transcript-pipeline/`: `python -m pytest test/test_refactor_contracts.py -q`.

```python
import json
from types import SimpleNamespace
from unittest.mock import Mock, call


def test_transcript_artifacts_preserve_object_defaults_and_dict_values():
    from src.yt_pipeline import upload_transcript_artifacts

    drive = Mock()
    segments = [SimpleNamespace(text="Ahoj", start=1.5),
                {"text": "Svět", "start": 2, "duration": 1}]
    upload_transcript_artifacts(segments, "Ahoj Svět", drive, "folder")
    raw = [{"text": "Ahoj", "start": 1.5, "duration": 0},
           {"text": "Svět", "start": 2, "duration": 1}]
    assert drive.upload_string.call_args_list == [
        call(json.dumps(raw, ensure_ascii=False, indent=2), "transcript_raw.json", "folder"),
        call("Ahoj Svět", "transcript_clean.txt", "folder"),
    ]


def test_shared_slug_owner_preserves_distinct_title_and_path_rules():
    from src.path_slugs import slugify_path_segment, slugify_title

    assert slugify_path_segment("Příliš/žluťoučký_kůň") == "prilis-zlutoucky-kun"
    assert slugify_title("a/b_c") == "ab_c"
    assert slugify_title("!!!") == ""
    assert slugify_path_segment("!!!", fallback="channel") == "channel"
    assert len(slugify_title("A" * 100)) == 80
```

| Test | RED before production edits | GREEN after implementation |
| --- | --- | --- |
| `test_transcript_artifacts_preserve_object_defaults_and_dict_values` | `ImportError: cannot import name 'upload_transcript_artifacts'` | Exact JSON bytes and ordered upload calls match. |
| `test_shared_slug_owner_preserves_distinct_title_and_path_rules` | `ModuleNotFoundError: src.path_slugs` | Unicode, separator, empty fallback, and title bound match. |

## Files
| Path | Planned change |
| --- | --- |
| `youtube-transcript-pipeline/src/yt_pipeline.py` | Extract workflow helpers; import public slug names from sole owner. |
| `youtube-transcript-pipeline/src/path_slugs.py` | Pure path/title normalization owner. |
| `helper-scripts/_slug_owner.py` | File-relative import adapter for standalone scripts. |
| `helper-scripts/normalize_kb_paths.py` | Replace duplicate path slug with shared import. |
| `helper-scripts/rename_video_folders.py` | Replace duplicate title slug with shared import while retaining its title semantics. |
| `youtube-transcript-pipeline/test/test_yt_pipeline.py`, `youtube-transcript-pipeline/test/test_config.py` | Extend mock-based characterization and import/config contracts as needed. |
| `youtube-transcript-pipeline/test/test_refactor_contracts.py`, `test/test_path_slug_callers.py` | Focused seam and root-level cross-caller/CLI tests. |

## Testing
- From `youtube-transcript-pipeline/`: `python -m pytest test/test_yt_pipeline.py test/test_config.py -q` before edits and after; `python -m pytest test/test_refactor_contracts.py -q` for RED/GREEN; `python -m pytest -q` for broader offline suite.
- From repository root: `python3 -m pytest test/test_path_slug_callers.py -q`; compare public pipeline imports against both standalone scripts on Unicode, slash/underscore, punctuation-only, repeated separators, and long titles; subprocess import shared module with poisoned/missing env and no external module imports; subprocess dry-run/apply normalization against temporary directories/refs and direct script invocation from outside repository root.
- Run `make test` from repository root as registered gate; run configured static checks if available (`black --check`/`flake8` for touched Python files if installed/configured), otherwise record absence. Report exact commands/results, AST `run_for_url` line count, owner/callers, and preserved distinct title semantics. All external calls remain mocked; never execute a live video/Drive/LLM/Whisper request.
