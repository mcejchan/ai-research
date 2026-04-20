---
title: "Acceptance checks: verify before re-implementing"
date: 2026-04-20
category: tooling
component: general
tags: [acceptance, monitor, workflow]
---

# Acceptance fix: already-committed files detected by monitor

When a monitor marks a task as incomplete due to "missing" files, the files may actually exist and be committed — the monitor may have checked the diff rather than the actual repo state. Always verify the actual file system and git log before re-implementing.

## Pattern
1. Check if the "missing" file exists on disk
2. Check `git log -- <file>` to confirm it's committed
3. Verify functionality (e.g., curl the server)
4. If everything is present and working, the task is already complete
