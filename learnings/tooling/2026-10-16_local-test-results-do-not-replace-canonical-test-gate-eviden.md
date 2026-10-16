---
title: "Local test results do not replace canonical Test Gate evidence"
date: 2026-10-16
category: tooling
component: tooling
tags: [acceptance, tdd, test-gate, provenance]
file_type: rules
---

# Local test results do not replace canonical Test Gate evidence

An evidence-only follow-up passed its focused and broader offline tests, but the acceptance goal remained open because the session had no caller-owned Test Gate facility or run ID. The follow-up captured a genuine RED/GREEN test for its missing checkpoint note and linked the refactor’s earlier RED/GREEN proof separately. Reuse this separation: record exact local commands and results, identify which artifact each proof covers, and leave the canonical gate requirement open until its own run record is available.

## Context
Extracted from task: [acceptance-fix] Tech debt: decompose YouTube processing and unify path slug ownership: goal-006: Fo
