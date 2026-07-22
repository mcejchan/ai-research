---
title: "Use live tracked inventory for artifact cleanup scope"
date: 2026-07-22
category: tooling
component: general
tags: [git, repository-hygiene, planning, stale-artifacts]
file_type: rules
---

# Use live tracked inventory for artifact cleanup scope

A review snapshot can become stale before cleanup begins. In this repository, the task described five tracked `tmp/` artifacts, while `git ls-files 'tmp/**'` showed six because newer agent staging files had since been committed.

Use the live tracked inventory as the deletion scope, then evaluate every listed file for maintained callers and unique durable content. Treat the older count as rationale, not an allowlist; otherwise recently added artifacts survive the cleanup and violate the invariant that no files remain tracked under the disposable directory.

Before deleting, compare each live artifact with canonical `learnings/` entries. Migrate only information that is both unique and accurate; Git history is sufficient for stale or duplicate staging prose.