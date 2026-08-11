---
title: "Transcript-only records are a valid intermediate state"
date: 2026-08-11
category: patterns
component: shared
tags: [partial-state, consumer-contracts, missing-analysis, knowledge-base]
---

Removing the placeholder exposed assumptions across the viewer and knowledge-base commands that every video directory contains `analysis_main.md`. Transcript-only folders must instead be treated as valid partial records.

Define missing-analysis behavior at every consumer boundary: viewers should report `hasAnalysis: false` and return a clear not-found response; generators should skip or report unavailable analysis; indexes should include the record without creating broken analysis links; mutating commands should stop before confirmation or file access. Contract tests over command specifications worked well for keeping these behaviors explicit.