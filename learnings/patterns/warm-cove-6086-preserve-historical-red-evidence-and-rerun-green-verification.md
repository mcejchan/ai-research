---
title: "Preserve historical RED evidence and rerun GREEN verification"
date: 2026-08-11
category: patterns
component: tooling
tags: [tdd, evidence, verification, acceptance]
---

The original TDD proof contained the genuine failing RED state, while the follow-up repository was already implemented and clean. Recreating a synthetic failure would have produced misleading evidence, so the historical RED was referenced and only fresh GREEN commands were run. For acceptance follow-ups, preserve authentic historical failure evidence and pair it with current reproducible verification rather than manufacturing a new failure.