---
title: "Static quiz controller session boundary"
date: 2026-10-23
category: architecture
component: frontend
tags: [quiz, vanilla-javascript, testing, static-hosting]
---

For static browser quiz pages, keep the initializer as an orchestration boundary and route answer state through the domain session module. That makes answer evaluation, progress, and score persistence part of the same production path exercised by pure unit tests. Keep presentation helpers responsible for DOM rendering and preserve HTML escaping at every interpolated text boundary.
