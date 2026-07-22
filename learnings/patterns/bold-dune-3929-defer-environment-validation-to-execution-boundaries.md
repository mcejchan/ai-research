---
title: "Defer environment validation to execution boundaries"
date: 2026-07-22
category: patterns
component: backend
tags: [environment, imports, pytest, configuration]
---

The pipeline accessed `DRIVE_FOLDER_ID` with `os.environ[...]` at module import time. When the variable was absent, importing `src.yt_pipeline` raised `KeyError`, preventing unrelated tests from collecting and hiding additional failures. Keep optional integration configuration import-safe and validate it only when the Drive-dependent operation actually executes. Add a subprocess import test with the variable removed so `.env` loading or ambient shell state cannot mask the contract.