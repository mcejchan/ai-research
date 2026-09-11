---
title: "tdd proof-capture.py: fixed canonical path, no overwrite, RED/GREEN identical command"
date: 2026-09-11
category: tooling
component: tooling
tags: [tdd, proof-capture, red-green, pytest, verification]
file_type: rules
---

# tdd `proof-capture.py`: fixed canonical path, no overwrite, RED/GREEN must use identical command

The tdd skill helper `proof-capture.py` (at `~/.config/opencode/skills/tdd/scripts/proof-capture.py`)
is the source of truth for RED/GREEN evidence but has hard constraints that shape any plan that
must use it.

## Constraints (read the script, do not assume)

- **Fixed output path:** it ALWAYS writes to
  `plans/checkpoints/<TASK_ID>.red-green-proof.md` relative to **CWD**. There is no `--output`
  flag. To get a fresh proof for a task whose canonical path is already occupied, you must first
  `mv`/rename the existing file (e.g. to `...rejected-v1.md`) — the helper refuses to overwrite.
- **`TASK_ID` env var required:** `parse_arguments`/`main` read `os.environ["TASK_ID"]`; it must
  match `^[A-Za-z0-9][A-Za-z0-9._-]*$`. Always pass `TASK_ID=<id>` when invoking.
- **No overwrite on RED:** running `red` when the proof file already exists fails with
  `proof already exists; refusing to replace`. So a second RED run for the same task id is impossible
  without first moving the old proof aside.
- **GREEN validates the previous RED with an IDENTICAL command:** `validate_red_proof` requires the
  recorded RED command (`shlex.join(command)`) and its `command_sha256`/metadata to match the GREEN
  command exactly. Therefore RED and GREEN must run the **byte-identical command string**; only the
  on-disk state (e.g. a copied `pytest.ini` header) may differ between phases.
- **Genuine exit codes enforced:** RED must exit non-zero (a passing RED is refused); GREEN must exit
  zero (a failing GREEN is refused). It records real `datetime.now(timezone.utc)` timestamps — never
  hand-fill historical timestamps.

## Practical recipe for a "fresh reproduction of an already-fixed defect"

When the repair + its regression tests already exist and you only need trustworthy proof that the
old header was the problem:
1. Preserve the occupied canonical proof: `mv ...red-green-proof.md ...red-green-proof.rejected-v1.md`.
2. Copy the target into an ignored disposable dir (`tmp/` or `.venv/`-adjacent), excluding
   `.venv`, `__pycache__`, `.pytest_cache`, `htmlcov`, `.coverage`.
3. In the COPY only, revert the header to the broken form; run `proof-capture.py red -- <cmd>` from
   the repo root so the proof lands at the repo's canonical checkpoint path.
4. Revert the copied header back; rerun `proof-capture.py green -- <same-cmd>` (inner command string
   identical) in the same venv.
5. Label the proof explicitly as a **fresh isolated reproduction, NOT the original development TDD** —
   successful current verification does not establish historical chronology.

## Why
The fixed path + no-overwrite + identical-command validation are the three properties that, taken
together, force a "preserve-old-proof → copy → mutate-copy-only → identical rerun" flow. Ignoring any
of them (e.g. trying to run RED twice, or varying the command between phases) makes the helper refuse.
