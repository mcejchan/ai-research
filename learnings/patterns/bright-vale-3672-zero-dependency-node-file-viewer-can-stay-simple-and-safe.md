---
title: "Zero-dependency Node file viewer can stay simple and safe"
date: 2026-04-20
category: patterns
component: tooling
tags: [nodejs, zero-dep, file-viewer, path-traversal, spa]
---

A lightweight file viewer worked well as a zero-dependency Node HTTP server plus a single HTML page. The durable parts were: parsing routes with the `URL` constructor and precise regexes like `([^/]+)`, using `fs.promises.readdir(..., { withFileTypes: true })` to avoid extra `stat` calls, validating path segments against `..`, `/`, and `\\` before `path.join`, and caching API responses on the client to reduce repeated fetches while switching tabs. Reuse this pattern for small internal viewers where a framework would be unnecessary.