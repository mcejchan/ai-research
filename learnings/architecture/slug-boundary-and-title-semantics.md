---
title: "Share path slugs without changing title semantics"
date: 2026-10-16
category: architecture
component: shared
tags: [youtube-pipeline, slug, standalone-scripts, refactor]
file_type: rules
---

The pipeline is invoked as `python -m src.yt_pipeline` from `youtube-transcript-pipeline/`, but maintenance scripts are invoked directly from `helper-scripts/`. A common import cannot assume the repository root is on sys.path. Keep a pure slug owner in `youtube-transcript-pipeline/src/path_slugs.py` and load it in standalone helpers through one adapter anchored to `__file__`, without importing `yt_pipeline` (which loads environment and service dependencies) or mutating sys.path based on cwd.

The two slug contracts differ: path slugs replace slash and underscore with separators and return a caller-specified fallback; title slugs drop slash, retain underscore, return an empty string for punctuation-only input, and truncate to 80 characters. Share the NFKD/ASCII, lowercase, punctuation, and hyphen-collapse primitive while testing the distinct rules across both callers. Preserve `src.yt_pipeline` public slug imports as aliases when extracting implementation ownership.