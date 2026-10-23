---
title: "Keep shared file mechanics separate from caller path semantics"
date: 2026-10-23
category: patterns
component: shared
tags: [refactoring, knowledge-base, testing]
---

# Keep shared file mechanics separate from caller path semantics

When two scripts share a recursive text-file replacement loop but construct different path patterns, extract only the traversal, IO, and ordered-replacement mechanics. Keep replacement-pattern generation with each caller so channel and video path shapes remain independently compatible. Characterize changed-only writes, supported extensions, replacement order, touched paths, and unreadable-file tolerance using temporary fixtures before refactoring.
