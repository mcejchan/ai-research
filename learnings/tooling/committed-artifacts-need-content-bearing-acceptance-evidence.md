---
title: "Committed artifacts need content-bearing acceptance evidence"
date: 2026-07-23
category: tooling
component: tooling
tags: [acceptance, evidence, git, verification]
file_type: rules
---

# Committed artifacts need content-bearing acceptance evidence

When acceptance evaluates an already committed documentation or learning artifact but the supplied task diff omits its addition hunk, attach the artifact's full content with immutable commit-and-path provenance. Include a bounded search for distinctive guidance so reviewers can assess both semantic accuracy and uniqueness; a path-only diff or checkpoint summary cannot support that review.

Keep historical verification provenance honest. If historical task evidence is unavailable, record that gap and provide a separate fresh canonical test-gate result instead of reconstructing or implying a result that was never captured.