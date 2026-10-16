---
title: "Use an absolute skill-script path outside its project"
date: 2026-10-16
category: tooling
component: tooling
tags: [save-learning, paths, monorepo]
file_type: rules
---

# Use an absolute skill-script path outside its project

The learning-save command failed because `.claude/skills/save-learning/add-frontmatter.py` did not exist relative to the project working directory. Invoking the installed script at `/Users/michal/.config/opencode/skills/save-learning/add-frontmatter.py` succeeded. Check where a skill script is installed before using a project-relative path.

## Context
Extracted from task: Tech debt: decompose YouTube processing and unify path slug ownership
