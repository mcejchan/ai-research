---
title: "Dead-code removal needs a maintained-document boundary"
date: 2026-07-21
category: tooling
component: general
tags: [dead-code, documentation, scope, verification]
file_type: rules
---

# Dead-code removal needs a maintained-document boundary

A repository-wide text match is not automatically an active caller. Separate maintained runtime code, current documentation, durable learnings, and CI configuration from historical plans, task records, and explicitly out-of-scope staging artifacts.

- Run one bounded caller search over the maintained paths before deletion.
- Update durable documentation that still instructs contributors to use the dead runtime.
- Leave historical records unchanged unless the task explicitly includes archival cleanup.
- Characterize the surviving runtime path and record unrelated baseline failures exactly instead of weakening assertions.

This keeps dead-code removal complete without turning it into unrelated repository cleanup.