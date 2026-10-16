---
title: "Canonical plan recovery requires a valid top-level header"
date: 2026-10-16
category: tooling
component: tooling
tags: [compound-plan, planning, acceptance, test-gate]
file_type: rules
---

# Canonical plan recovery requires a valid top-level header

When resuming an existing plan after `plan_artifact_invalid: status=invalid_header`, inspect the canonical file returned by `plan-path.py --touch` before writing another plan. A file with valid `##` sections can still fail if its first line is a descriptive title instead of `# Plan: ...`. Repair that file in place; never invent a new filename or change `plans/tasks/`.

If the caller restricts `##` headings to an exact vocabulary, obey that constraint even when a generic skill template suggests additional headings or `## TDD: skip`. For an evidence-only plan, use `## TDD` and explicitly state that no new RED is warranted. Distinguish successful local verification from the caller-owned Test Gate record, which needs its own run reference.
