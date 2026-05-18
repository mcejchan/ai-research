---
title: "Escape JSON-backed quiz feedback before using innerHTML"
date: 2026-05-18
category: architecture
component: frontend
tags: [quiz, vanilla-js, innerHTML, xss, json-content, feedback]
---

When the quiz UI was extended to render `question.explanation` inside the feedback panel, the implementation had to switch from plain `textContent` to `innerHTML` so the explanation block could be appended with markup. That creates an injection risk because the explanation text comes from JSON content, not trusted code. The safe pattern is to build the wrapper markup separately and HTML-escape all dynamic strings before insertion. Reuse this any time content authors can populate JSON fields that are later rendered with `innerHTML`; avoid inserting raw explanation or answer text directly.