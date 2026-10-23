---
title: "Aggregate quiz validator threshold fixtures"
date: 2026-10-23
category: architecture
component: general
tags: [quiz, validation, testing, statistics]
---

# Aggregate quiz threshold fixtures

Aggregate validator thresholds use strict `>` comparisons: longest-answer ratio is 0.50 and much-longer ratio is 0.40. Pin equality and one-question-over cases using ten-question fixtures. For much-longer cases, ensure correct options are actually longer than distractors only on the intended rows; equal-length options count as longest because ties are included. Keep assertions focused on aggregate `BIAS:` advisories separately from per-question length advisories.

The TDD proof helper requires a captured failing RED before it will publish GREEN. When behavior already exists and the valid task plan prohibits manufacturing a failing expectation, the helper cannot create a fresh proof under that contract; record the evidence limitation rather than inventing a mismatch.
