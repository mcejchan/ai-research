---
title: "Quiz validator: characterizing strict aggregate thresholds"
date: 2026-10-23
category: architecture
component: general
tags: [quiz, validation, statistics, testing]
---

# Quiz validator threshold characterization

Validator aggregate ratios are strict (`>`), so characterization fixtures should calculate the denominator across all correct-answer marks, not assume one answer per question creates every desired percentage. A position ratio of exactly 45% requires 20 correct marks (for example, 9 of 20); 4/10 is 40%, while 5/10 crosses the threshold. Also assert per-question advisories separately from aggregate `BIAS:` messages: a fixture with a correct option more than 1.6 times the longest distractor emits a question-level advisory even when aggregate thresholds are at equality.

The focused suite proved useful in exposing fixture mistakes before production changes: equal-length options count as `correctIsLongest`, invalid type/points do not make otherwise-analyzable options unavailable for statistics, and aggregate structural-error gating removes aggregate advisories while retaining accumulated question statistics. Preserve these existing semantics rather than adjusting validator code to fit a faulty expectation.
