---
title: "Anchor viewer follow-up plans in the live file and exact style source"
date: 2026-04-20
category: tooling
component: frontend
tags: [planning, frontend, viewer, css, source-of-truth]
---

# Plan viewer follow-up tasks by anchoring in the live file and external style source

For a UI follow-up on an existing single-file viewer, the fastest useful plan came from reading the current target file and the external reference file before proposing any steps.

## What worked
- Read the actual viewer file first to anchor the plan in the current DOM, CSS, and client state instead of the request wording.
- Read the external style source (`~/Projects/ai-education/index.html`) early so the plan can call for verbatim CSS copying instead of a vague visual match.
- Keep the plan scoped to the existing single-file architecture when the viewer already has the needed fetch/cache behavior.

## Reusable rule
If a task says "match X exactly" and only one file is allowed to change, the plan should name the exact source file to copy from, the exact target file to edit, and the minimal state/layout changes needed around that copied block.

## Why it matters
This prevents drifting into a redesign, avoids unnecessary dependencies, and makes the later implementation/review check straightforward: one target file, one style source of truth, and a short manual verification path.
