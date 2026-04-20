---
title: "Separate test runner availability failures from product regressions"
date: 2026-04-20
category: test-failures
component: tooling
tags: [pytest, path, python, environment, verification]
---

Verification failed in two distinct tooling layers: `pytest` was not on `PATH`, and `python3 -m pytest` then failed because `pytest` was not installed in the active interpreter environment. This is a useful diagnostic pattern: if the direct CLI is missing, retry through the interpreter to distinguish shell-path problems from missing dependencies. Reuse this split when reporting failures so environment/tooling issues are not mistaken for code regressions, and avoid concluding that a change is broken until the test runner itself is confirmed available.