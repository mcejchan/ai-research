# Plan 2026-10-23: Consolidate knowledge-base reference rewriting

Extract the duplicate recursive rewrite loop into a helper-script-local KB-specific module while keeping both callers' pattern generation and CLI behavior intact.

## Analysis

- `helper-scripts/normalize_kb_paths.py` and `helper-scripts/rename_video_folders.py` each define `update_references` with identical extension filtering, UTF-8 IO, unreadable-file tolerance, ordered replacements, changed-only writes, recursive traversal, and touched-path reporting.
- `replacement_patterns` must remain in each script: channel and video paths have distinct shapes. Existing CLI parity tests are in `test/test_path_slug_callers.py` and use temporary directories.
- Project gate: `make test`. No diagram or API documentation applies to this helper-script refactor.
- Relevant learning: `learnings/patterns/2026-10-16_preserve-distinct-title-and-path-slug-semantics.md` — centralize shared mechanics without altering caller-specific contracts.
- Relevant skills: `tdd` for RED/GREEN proof; `recall-knowledge` before implementation; `save-learning` after completion.

## Approach

- Add `helper-scripts/kb_reference_rewriter.py` with a KB/reference-specific public function (for example `rewrite_kb_references(ref_root, patterns)`).
- Move only the common traversal and text replacement mechanics; preserve `.md`, `.txt`, `.json`, `.csv` filtering case-insensitively and all current IO/error/write semantics.
- Import the helper in both scripts and delegate their existing `update_references` call sites to it; remove the duplicate implementations and now-unused imports only.
- Add focused temporary-fixture tests for extension filtering, unchanged files, ordered multiple replacements, returned touched paths, and unreadable-file tolerance where platform permissions permit. Keep current CLI tests and assertions intact.

## Implementation

1. First add `test/test_kb_reference_rewriter.py` with the concrete characterization cases below and run it to capture RED.
2. Implement the shared function in `helper-scripts/kb_reference_rewriter.py`; preserve traversal, return paths, and error tolerance exactly.
3. Update both scripts to import and call the helper; retain each local `replacement_patterns` implementation and existing dry-run/apply gates and messages.
4. Run focused tests, `test/test_path_slug_callers.py`, and the repository `make test` gate. Run the locally supported duplication check against the two scripts if available, recording unavailable tooling as a blocker/result rather than changing thresholds.
5. Review the diff to confirm all test data is temporary and no knowledge-base content or unrelated files changed.

## Testing

- `python3 -m pytest test/test_kb_reference_rewriter.py`
- `python3 -m pytest test/test_path_slug_callers.py`
- `make test`
- Run the repository-supported duplication checker on `helper-scripts/normalize_kb_paths.py` and `helper-scripts/rename_video_folders.py`, if installed; report its exact result.

## TDD

Implementation follows `skill:tdd`; capture focused RED/GREEN evidence before the full regression gate.

**Test file:** `test/test_kb_reference_rewriter.py`  
**Framework:** pytest, matching the Python test gate.  
**Run command:** `python3 -m pytest test/test_kb_reference_rewriter.py`  
**Edit hint:** New file; import `rewrite_kb_references` from `kb_reference_rewriter` after adding `helper-scripts` to `sys.path` or follow the existing caller test import pattern.

```python
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parents[1] / "helper-scripts"
sys.path.insert(0, str(SCRIPTS))
from kb_reference_rewriter import rewrite_kb_references


def test_filters_extensions_and_reports_only_changed_files(tmp_path):
    md = tmp_path / "ref.MD"
    md.write_text("youtube/old", encoding="utf-8")
    unchanged = tmp_path / "same.txt"
    unchanged.write_text("nothing", encoding="utf-8")
    ignored = tmp_path / "data.bin"
    ignored.write_text("youtube/old", encoding="utf-8")

    touched = rewrite_kb_references(tmp_path, [("youtube/old", "youtube/new")])

    assert touched == [md]
    assert md.read_text(encoding="utf-8") == "youtube/new"
    assert unchanged.read_text(encoding="utf-8") == "nothing"
    assert ignored.read_text(encoding="utf-8") == "youtube/old"


def test_applies_replacements_in_order(tmp_path):
    ref = tmp_path / "ref.json"
    ref.write_text("old", encoding="utf-8")

    assert rewrite_kb_references(tmp_path, [("old", "middle"), ("middle", "new")]) == [ref]
    assert ref.read_text(encoding="utf-8") == "new"
```

| Test | RED | GREEN |
|---|---|---|
| Extension filter/touched paths | Import or missing helper fails | Only changed supported file is returned and written; unsupported and unchanged files remain intact |
| Ordered replacements | Import or missing helper fails | Later replacement sees earlier replacement output, and touched path is returned |
| Unreadable file (platform permitting) | Missing helper or unexpected read error | File is skipped without aborting other rewrites |

## Files

| Path | Planned change |
|---|---|
| `helper-scripts/kb_reference_rewriter.py` | New shared KB-specific recursive text-reference rewrite helper |
| `helper-scripts/normalize_kb_paths.py` | Delegate rewrite operation; keep channel replacement construction and CLI gates |
| `helper-scripts/rename_video_folders.py` | Delegate rewrite operation; keep video replacement construction and CLI gates |
| `test/test_kb_reference_rewriter.py` | Add temporary-fixture characterization tests |
| `test/test_path_slug_callers.py` | No weakening or unrelated edits; run as existing CLI regression coverage |

## Progress

- [x] Resolve canonical plan path and inspect relevant callers, tests, project gate, and learning.
- [x] Define extraction boundary and focused TDD cases.
- [ ] Implement the refactor and verify acceptance criteria.
