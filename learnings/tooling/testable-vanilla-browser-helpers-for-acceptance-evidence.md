---
title: "Testable vanilla browser helpers for acceptance evidence"
date: 2026-05-18
category: tooling
component: frontend
tags: [vanilla-js, testing, acceptance, nodejs]
file_type: rules
---

# Testable vanilla browser helpers for acceptance evidence

When a task is constrained to a dependency-free browser app, focused acceptance evidence can still be produced without adding a test framework or build step.

## Pattern

Keep browser runtime behavior unchanged, but isolate small pure helpers and guard DOM startup:

```js
if (typeof document !== 'undefined') {
  // browser initialization
}

if (typeof module !== 'undefined') {
  module.exports = { sameSelection };
}
```

This makes all-or-nothing quiz scoring logic testable through `node -e` while preserving the same static `app.js` file for the browser.

## Why it helped

The acceptance fix required proof for both server endpoints and quiz scoring behavior, but the app intentionally has no dependencies, no bundler, and no formal test runner. Exporting a pure helper allowed a direct Node assertion for multi-select scoring without introducing framework code or changing the UI.

## Verification split

- Use `node --check` for syntax validation of `server.js` and `app.js`.
- Use `node -e` with `assert` for pure scoring helpers.
- Start `server.js` in a short-lived process and use Node's built-in `http` module for endpoint smoke tests.
- Document broader unrelated suite failures separately instead of fixing outside the task scope.
