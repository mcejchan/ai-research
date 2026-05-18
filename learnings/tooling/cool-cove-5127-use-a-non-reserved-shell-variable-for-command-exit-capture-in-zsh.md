---
title: "Use a non-reserved shell variable for command exit capture in zsh"
date: 2026-05-18
category: tooling
component: tooling
tags: [zsh, shell-script, exit-code, cleanup, verification]
---

A focused verification command failed after successful checks because it assigned to `status`, which is a read-only variable in `zsh`. Renaming the capture variable to something neutral like `rc` fixed the issue. When writing portable verification one-liners with background process cleanup, avoid shell-special names for temporary variables or the cleanup path can fail even after the main assertions pass.