---
title: "Preserve distinct title and path slug semantics"
date: 2026-10-16
category: patterns
component: shared
tags: [slugs, compatibility, refactoring]
file_type: rules
---

# Preserve distinct title and path slug semantics

When moving slug normalization into one owner, keep the callers’ existing contracts distinct. Title slugs discard slashes, retain underscores, allow an empty result for punctuation-only titles, and truncate at 80 characters. Path slugs treat slashes and underscores as separators. Focused caller tests helped verify that centralizing the implementation did not silently change either behavior.

## Context
Extracted from task: Tech debt: decompose YouTube processing and unify path slug ownership
