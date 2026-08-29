---
title: "Publication gates must validate before projecting derived manifests"
date: 2026-08-29
category: tooling
component: ci-cd
tags: [quiz, publication-gate, fail-closed, generated-manifest, github-pages]
file_type: rules
---

# Publication gates must validate before projecting derived manifests

For this repository's static quiz, catalog generation is part of acceptance rather than a best-effort discovery operation. If the builder catches a malformed source and continues, a successful deployment only proves that some levels were publishable.

Use one component-level Make target as the publication contract. It should run focused runtime tests and then build the real manifest through the same importable structural validator used by validator tooling. The builder must finish reading, parsing, and structurally validating every source before writing the derived index.

Keep content heuristics separate from structural integrity: unreadable files, malformed JSON, and runtime-invalid question shapes fail; answer-position/length bias and optional explanation quality warn. Test both paths with injected temporary level/index roots, and statically assert that Pages delegates to the shared target instead of copying its commands.
