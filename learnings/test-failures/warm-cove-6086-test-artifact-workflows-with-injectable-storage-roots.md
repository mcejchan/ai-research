---
title: "Test artifact workflows with injectable storage roots"
date: 2026-08-11
category: test-failures
component: backend
tags: [filesystem, isolation, integration-tests, dependency-injection]
---

Pipeline tests needed to verify both successful artifact creation and the absence of placeholder files after failures, including local-storage behavior. Injecting filesystem or storage roots made these assertions deterministic and isolated from real user data. Reuse configurable roots for artifact-producing integration tests instead of relying on fixed production-like paths.