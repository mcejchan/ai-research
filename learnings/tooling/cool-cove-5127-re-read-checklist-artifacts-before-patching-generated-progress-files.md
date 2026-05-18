---
title: "Re-read checklist artifacts before patching generated progress files"
date: 2026-05-18
category: tooling
component: tooling
tags: [apply-patch, checkpoint-files, proof-files, resume-work, artifact-maintenance]
---

Patch updates against progress artifacts like checkpoint and RED/GREEN proof files failed multiple times because the expected lines no longer matched the file contents. The durable lesson is that resumable task artifacts drift quickly, especially after partial runs or manual updates. Before editing them, re-read the current file and patch against the exact live text instead of assuming the previous structure still exists. This avoids brittle patch failures and is especially important for checklist-style files that are updated incrementally during verification.