---
title: "A root test gate can expose previously hidden failures"
date: 2026-07-22
category: tooling
component: ci-cd
tags: [make, test-gate, pytest, node-test, ci]
---

After a root `make test` gate composed the quiz, viewer, and Python suites, fixing Python test collection exposed four latent LLM test failures. The failures were unrelated to the new gate: assertions expected an obsolete proxy URL and a custom mock method did not support `call_args`. When introducing an authoritative cross-language gate, run each delegated suite independently before running the aggregate command. Treat newly visible failures as potentially pre-existing fixture or expectation drift, and repair those without changing production behavior unless the production contract is actually wrong.