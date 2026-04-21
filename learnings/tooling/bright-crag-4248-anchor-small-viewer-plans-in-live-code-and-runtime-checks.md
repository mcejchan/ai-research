---
title: "Anchor small viewer feature plans in live routes, inline render points, and runtime checks"
date: 2026-04-21
category: tooling
component: tooling
tags: [planning, yt-viewer, zero-dep, runtime-verification]
---

# Anchor small viewer feature plans in live routes, inline render points, and runtime checks

For `yt-viewer` tasks, the most reliable plan came from reading the exact live route and the exact inline rendering callsite instead of extrapolating from the wider repo. The app is a zero-dependency Node server plus one HTML file, so the actionable planning pattern was:

1. Read `yt-viewer/server.js` to locate the route that owns the behavior change.
2. Read `yt-viewer/index.html` to find the single render path that consumes that API.
3. Confirm the real data shape under `local-knowledge-base/youtube/` so the plan follows existing folder conventions.
4. Prefer runtime verification (`curl`, live endpoint checks, browser/manual confirmation) over assuming there is a build or test harness.

This keeps the plan small and concrete. It also avoids over-planning extra modules or dependencies for a viewer that is intentionally simple.
