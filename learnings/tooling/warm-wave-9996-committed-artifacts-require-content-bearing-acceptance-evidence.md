---
title: "Committed artifacts require content-bearing acceptance evidence"
date: 2026-07-23
category: tooling
component: tooling
tags: [acceptance, evidence, git, provenance, verification]
---

When acceptance reviews an artifact already committed outside the current diff, a path reference or checkpoint summary is insufficient for semantic review. Attach the artifact's full content with immutable commit-and-path provenance, verify it is unchanged with a commit-scoped diff, and run bounded searches for distinctive text to establish uniqueness. If historical test evidence was not captured, state that gap explicitly and provide a separate fresh canonical test result rather than reconstructing or implying historical success.