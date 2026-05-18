---
title: "Guard browser startup to make vanilla helpers testable in Node"
date: 2026-05-18
category: patterns
component: frontend
tags: [vanilla-js, node-verification, dom-guard, exported-helper, acceptance-testing]
---

A useful pattern for browser-only apps was to keep the app behavior unchanged in the browser while making core logic directly testable from Node. In this task, `app.js` was updated so DOM startup only runs when a browser environment is present, and the scoring helper (`sameSelection`) is exportable for Node-based checks. That made it possible to verify all-or-nothing multi-select scoring with a fast CLI command instead of needing a full browser harness. Reuse this when a small piece of frontend logic needs acceptance evidence or regression coverage without pulling in a test framework.