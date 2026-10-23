---
title: "Testovatelná logika pro statické quiz stránky"
date: 2026-10-23
category: architecture
component: frontend
tags: [quiz, vanilla-javascript, testing, static-hosting]
---

## Vanilla static-page script extraction

When extracting browser logic into a separate file in this dependency-free quiz, preserve the static-host contract by loading the domain script before `app.js` in both HTML entry points. A CommonJS `require` works in Node tests only; browser runtime needs a guarded global export. Keep the browser startup guard intact so requiring `app.js` in Node does not touch `document`.

Focused behavior tests can directly exercise pure filter/render/session logic with Node's built-in test runner, but those tests do not substitute for wiring DOM interactions into the controller. Keep separate controller-level characterization coverage for fetch failures and click-driven transitions.
