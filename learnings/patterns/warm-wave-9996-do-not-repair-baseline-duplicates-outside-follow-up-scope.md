---
title: "Do not repair baseline duplicates outside follow-up scope"
date: 2026-07-23
category: patterns
component: general
tags: [scope, follow-up, baseline, provenance]
---

A repository-wide search may reveal later-generated artifacts that duplicate a canonical learning, but that does not automatically make them part of an evidence-only follow-up. Compare commit provenance and the task's scoped baseline first. When the parent artifact is immutable and the duplicates were introduced later outside the follow-up scope, leave them untouched and prove the canonical artifact's uniqueness at the relevant parent commit instead of introducing unrelated cleanup.