---
title: "Prefer globally installed skill helpers over repo-local assumptions"
date: 2026-04-21
category: tooling
component: general
tags: [skills, paths, save-learning, workspace, portability]
---

Saving the learning failed at first because the workflow assumed a repo-local helper path (`.claude/skills/save-learning/add-frontmatter.py`) that did not exist in this workspace. The successful workaround was to call the globally installed skill helper under the shared OpenCode config directory instead. Avoid baking repo-specific helper paths into reusable workflows; when a skill is provided by the environment, use the canonical global path so the workflow remains portable across repositories.