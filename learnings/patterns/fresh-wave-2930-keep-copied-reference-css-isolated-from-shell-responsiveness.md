---
title: "Keep copied reference CSS isolated from shell responsiveness"
date: 2026-04-21
category: patterns
component: frontend
tags: [viewer, css, responsive, markdown, source-of-truth]
---

A mobile viewer update initially mixed responsive layout overrides directly into the copied markdown styling block, which broke the requirement to match the reference `ai-education` styles exactly. The fix was to keep the imported `.markdown-content` CSS verbatim and apply responsive behavior only in outer shell/layout wrappers. Reuse this pattern whenever a UI must inherit a canonical style block from another app: copy the reference CSS unchanged, scope it to an inner wrapper, and put app-specific layout rules outside that boundary.