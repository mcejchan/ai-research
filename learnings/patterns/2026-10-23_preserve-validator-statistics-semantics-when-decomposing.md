---
title: "Preserve validator statistics semantics when decomposing"
date: 2026-10-23
category: patterns
component: shared
tags: [quiz, validation, refactoring, statistics, characterization-tests]
file_type: rules
---

# Preserve validator statistics semantics when decomposing

During the quiz validator decomposition, a characterization assertion expected questions with duplicate correct indices to be excluded from option statistics. The captured RED run showed that this expectation did not match the existing behavior, so the assertion was corrected before refactoring. When splitting validation into structural and statistical stages, characterize and preserve existing behavior—including edge cases that may seem unintended—rather than letting an assumed rule silently change the contract.

## Context
Extracted from task: Tech debt: decompose quiz level validation stages
