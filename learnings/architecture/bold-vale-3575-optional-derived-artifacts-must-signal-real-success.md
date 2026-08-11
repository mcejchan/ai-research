---
title: "Optional derived artifacts must signal real success"
date: 2026-08-11
category: architecture
component: backend
tags: [success-artifacts, graceful-degradation, pipeline, failure-semantics]
---

When LLM analysis failed, the pipeline still created and uploaded a placeholder `analysis_main.md`. Downstream consumers therefore could not distinguish successful analysis from graceful degradation.

Treat the existence of an optional derived artifact as a success contract: preserve durable upstream outputs such as transcripts, log the analysis failure, but do not create the derived file. Reuse this rule whenever downstream code uses file presence as a readiness or success signal.