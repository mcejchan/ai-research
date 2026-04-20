---
title: "Use the globally installed save-learning helper path"
date: 2026-04-20
category: tooling
component: tooling
tags: [save-learning, path-resolution, opencode-skills, scripts]
---

A first attempt to run `.claude/skills/save-learning/add-frontmatter.py` failed because that helper did not exist inside the project. The working invocation used `/Users/michal/.config/opencode/skills/save-learning/add-frontmatter.py`. Reuse: for shared OpenCode skills, resolve helper scripts from the global skill installation path rather than assuming a repo-local `.claude/skills` copy. Avoid hardcoding project-relative skill paths unless the repository actually vendors them.