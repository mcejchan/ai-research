---
title: "Quiz validator: structural errors and option statistics"
date: 2026-10-23
category: architecture
component: general
tags: [quiz, validation, statistics, testing]
---

# Quiz validator decomposition preserves a subtle statistics rule

The quiz validator separates top-level checks, per-question structural checks, option-derived statistics, aggregate bias advisories, and result construction. Keep the mutable validation context explicit and scoped to one `validateLevelData` call.

A question with structurally invalid correct indices can still contribute option statistics when the indices themselves are integer and in-range. For example, duplicate correct indices trigger a structural error but are still counted individually in `correctIndexCounts`; do not gate statistical analysis on all structural validation having passed. The all-questions structural-error gate applies only to aggregate bias advisories.

When characterizing established behavior, inspect actual complete stats as well as error text. An initial expectation that duplicate indices would be excluded from stats was disproven by execution and corrected before the production refactor.
