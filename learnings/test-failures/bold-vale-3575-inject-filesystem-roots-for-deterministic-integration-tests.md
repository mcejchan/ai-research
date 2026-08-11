---
title: "Inject filesystem roots for deterministic integration tests"
date: 2026-08-11
category: test-failures
component: e2e
tags: [filesystem, dependency-injection, environment-variable, isolation]
---

The viewer already behaved correctly for transcript-only directories, but its hard-coded knowledge-base root prevented an isolated test from reaching that behavior and produced a plain `Not found` response at the wrong route.

Allow the filesystem root to be overridden, such as with `YT_KB_ROOT`, while retaining the production default. Tests can then construct a temporary knowledge base and verify API semantics without depending on workstation data or mutating the real repository.