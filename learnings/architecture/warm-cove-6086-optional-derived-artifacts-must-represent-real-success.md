---
title: "Optional derived artifacts must represent real success"
date: 2026-08-11
category: architecture
component: backend
tags: [artifacts, failure-semantics, partial-state, pipeline]
---

The transcript pipeline previously risked representing failed analysis with a placeholder `analysis_main.md`. The successful pattern is to create that derived artifact only after analysis succeeds; on failure, preserve transcripts and diagnostics while leaving analysis absent. Consumers must treat transcript-only records as a valid intermediate state and explicitly report analysis as unavailable instead of interpreting file existence as success.