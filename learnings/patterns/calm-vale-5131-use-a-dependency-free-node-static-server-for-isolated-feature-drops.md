---
title: "Use a dependency-free Node static server for isolated feature drops"
date: 2026-05-18
category: patterns
component: frontend
tags: [vanilla-js, nodejs, static-server, localstorage, prototype]
---

A complete quiz dashboard was delivered under `quiz/` using only Node built-ins plus static HTML/CSS/JS, with `/api/levels` and `/api/level` served from the same minimal server. This made the feature self-contained, easy to verify with `curl`, and independent from the rest of the app stack.

Reuse this pattern for small standalone tools, demos, or dashboards that need to live inside a repo without adding package/dependency overhead. It works especially well when the UI only needs simple browser state such as `localStorage` and file-backed JSON endpoints. Verify the pattern with two checks: syntax validation via `node --check` and an end-to-end smoke test hitting both `/` and the JSON API.