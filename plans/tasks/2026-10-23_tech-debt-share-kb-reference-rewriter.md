# Tech debt: consolidate knowledge-base reference rewriting

## Assessment

**Decision: create**

Current inspection confirms the high-severity duplication remains present. `helper-scripts/normalize_kb_paths.py:34-53` and `helper-scripts/rename_video_folders.py:55-74` independently implement the same recursive text-file rewrite loop: scan `.md`, `.txt`, `.json`, and `.csv` files, tolerate unreadable files, apply an ordered list of string replacements, write changed UTF-8 content, and return touched paths. The reported 190-token duplicate is therefore current rather than stale.

The two scripts intentionally build different replacement patterns, so only the shared file-rewrite mechanism should be consolidated. Existing repository tests exercise both CLI callers in `test/test_path_slug_callers.py`; there is no dedicated characterization of unreadable/irrelevant/unchanged files or replacement ordering.

Current task state was inspected before registration. There is no unfinished `ai-research` task or batch owner, so no current overlap exists and there is nothing exact to reuse.

Finding identity: `ai-research:code_duplication_jscpd:helper-scripts/normalize_kb_paths.py:36-54|helper-scripts/rename_video_folders.py:56-74`, first detected 2026-10-19.

## Goal

Replace the duplicated knowledge-base text-reference update loop with one domain-qualified shared helper while preserving both scripts' CLI behavior and their intentionally distinct replacement-pattern construction.

## Implementation scope

- Add one helper-scripts-local module with a domain-qualified basename such as `kb_reference_rewriter.py`. Do not add generic modules named `common.py`, `utils.py`, `helpers.py`, `files.py`, or `rewrite.py`.
- Move the shared recursive text-file rewriting behavior into that module and import it from both scripts.
- Preserve the supported extension set exactly: `.md`, `.txt`, `.json`, and `.csv`, case-insensitively.
- Preserve UTF-8 reads/writes, unreadable-file tolerance, replacement application order, write-only-when-changed behavior, traversal behavior, and returned touched paths.
- Keep each script's existing `replacement_patterns` logic local because the channel-folder and video-folder path shapes differ.
- Preserve dry-run/apply gates, output messages, rename behavior, argument parsing, and all other script semantics.
- Do not operate on the real `local-knowledge-base`; tests must use temporary fixtures.

## Acceptance criteria

- The duplicated reference-update implementation exists in one source location and both scripts delegate to it.
- The shared module's filename and public helper name are knowledge-base/reference-rewrite specific.
- Both CLI workflows remain behaviorally compatible, including no reference writes during dry runs.
- Focused tests characterize extension filtering, unchanged files, multiple ordered replacements, touched-path reporting, and unreadable-file tolerance where practical on the test platform.
- Existing `test/test_path_slug_callers.py` remains green without weakened assertions.
- A duplication check no longer reports the cited clone between these two ranges.
- No unrelated cleanup or knowledge-base content changes are included.
- Final note records files changed and exact verification commands/results.

## Verification

- Run the focused tests for the shared reference rewriter.
- Run `test/test_path_slug_callers.py`.
- Run the repository's configured Python test/lint gate applicable to helper scripts.
- Run the supported duplication check, if locally available, against the two helper scripts and report the result without weakening thresholds.

## Scope boundary

Work only within `/Users/michal/Projects/ai-research`. Do not inspect or edit other repositories, the real user knowledge base outside repository-controlled temporary fixtures, OpenClaw configuration, runtime services, task state, or deployment hooks. Record a blocker instead of crossing this boundary.
