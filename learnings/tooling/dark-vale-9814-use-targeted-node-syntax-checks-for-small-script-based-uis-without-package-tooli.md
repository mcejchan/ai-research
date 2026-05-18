---
title: "Use targeted Node syntax checks for small script-based UIs without package tooling"
date: 2026-05-18
category: tooling
component: frontend
tags: [verification, node-check, lightweight-app, no-package-json, syntax-check]
---

This quiz app had no `package.json` and no repo-local JS task runner, so broad build or test assumptions were wrong. The practical verification path was to inspect what tooling actually existed and then run `node --check` directly on the affected JavaScript entry points (`app.js`, `server.js`). Reuse this when working in minimal or static apps: verify available commands first, then choose the smallest syntax/build check that matches the real project setup instead of inventing missing npm workflows.