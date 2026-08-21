---
title: "Separate evidence failures from implementation defects"
date: 2026-08-21
category: patterns
component: general
tags: [acceptance, diagnosis, verification, minimal-change]
---

A failed acceptance result does not necessarily indicate faulty implementation. Here, inspection of the acceptance manifest and results showed that goals 001 through 004 were satisfied; only verification provenance was missing. Reuse this diagnostic pattern: inspect structured acceptance artifacts first, identify whether the rejection concerns behavior or evidence, and avoid unnecessary code or test changes when the implementation already meets its requirements.