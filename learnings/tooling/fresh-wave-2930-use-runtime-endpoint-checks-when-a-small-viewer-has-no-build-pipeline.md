---
title: "Use runtime endpoint checks when a small viewer has no build pipeline"
date: 2026-04-21
category: tooling
component: frontend
tags: [verification, runtime-checks, server, no-build, inline-script]
---

The `yt-viewer` app had no dedicated build, lint, or test scripts, so verification had to be runtime-based. A useful lightweight sequence was: parse the inline browser script with `new Function(...)`, start `server.js` if the local endpoint is not already serving, then verify `/`, `/api/channels`, and representative analysis/transcript endpoints. This is a good fallback for zero-dependency or single-file frontend tools: validate syntax separately, then confirm the real data flow through HTTP instead of inventing heavier test scaffolding.