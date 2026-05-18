---
title: "GitHub Pages subdirectory apps need Actions artifact deploy"
date: 2026-05-18
category: tooling
component: ci-cd
tags: [github-pages, github-actions, static-deploy, planning]
file_type: rules
---

# GitHub Pages for subdirectory apps needs Actions artifact, not branch subfolder

When planning a static deploy for a project kept in a repository subdirectory such as `quiz/`, do not assume GitHub Pages can publish directly from `main:/quiz`. Branch-based Pages sources only support the repository root or `/docs`.

Use Pages source `GitHub Actions` instead:

```yaml
- run: node quiz/build-index.js
- uses: actions/upload-pages-artifact@v3
  with:
    path: quiz
```

This publishes the contents of `quiz/` as the site root, so the project Pages URL is `https://<owner>.github.io/<repo>/`, not `https://<owner>.github.io/<repo>/quiz/`.

If the app also needs a generated static manifest, commit a baseline generated file for local/static use and regenerate it in the Actions workflow before artifact upload.
