---
title: "YT Viewer: stale dev server can invalidate localhost verification"
date: 2026-04-21
category: tooling
component: tooling
tags: [yt-viewer, node, verification, ports, dev-server]
---

# YT viewer verification should account for stale long-running dev servers

For `yt-viewer`, a targeted `node:test` regression is the most reliable proof that endpoint behavior changed, because the app is often run as a long-lived local server on `localhost:4001`.

## What happened

The new `/api/channels` test went GREEN after the server code change, but the runtime `curl http://localhost:4001/api/channels` check still returned the old payload shape.

The cause was not the implementation. Port `4001` was already occupied by an older `node yt-viewer/server.js` process, so a fresh verification server could not start and the curl request hit stale code.

## Practical rule

- Keep a focused `node:test` coverage for the zero-dependency HTTP routes.
- When a runtime check disagrees with the test result, verify whether the dev port is already in use before assuming the code change failed.
- For `yt-viewer`, restarting the existing dev server is required before trusting the `localhost:4001` payload after backend edits.
