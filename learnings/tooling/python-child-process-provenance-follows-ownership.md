---
title: "Python child-process provenance follows ownership"
date: 2026-10-25
category: tooling
component: tooling
tags: [python, makefile, runtime, testing]
file_type: rules
---

# Aggregate quiz threshold fixtures

Aggregate validator thresholds use strict `>` comparisons: longest-answer ratio is 0.50 and much-longer ratio is 0.40. Pin equality and one-question-over cases using ten-question fixtures. For much-longer cases, ensure correct options are actually longer than distractors only on the intended rows; equal-length options count as longest because ties are included. Keep assertions focused on aggregate `BIAS:` advisories separately from per-question length advisories.

The TDD proof helper requires a captured failing RED before it will publish GREEN. When behavior already exists and the valid task plan prohibits manufacturing a failing expectation, the helper cannot create a fresh proof under that contract; record the evidence limitation rather than inventing a mismatch.
# Python child-process provenance must follow ownership

When a project test gate selects a pinned Python runtime, audit each child process by what it executes. Python children owned by the project should use and verify the selected interpreter; external binaries such as `yt-dlp` remain external tools and should not be rewritten as Python invocations. A regression should observe the child’s actual executable and version, and exercise the real Make recipe with hostile ambient `python3`. Focused mocked launcher evidence does not establish success of the canonical root gate.
