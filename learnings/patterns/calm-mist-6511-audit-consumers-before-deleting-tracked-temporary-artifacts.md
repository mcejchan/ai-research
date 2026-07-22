---
title: "Audit consumers before deleting tracked temporary artifacts"
date: 2026-07-22
category: patterns
component: general
tags: [cleanup, references, temporary-files, gitignore]
---

Before removing tracked staging artifacts, inventory the exact tracked paths, search maintained code, workflows, documentation, and scripts for consumers, and confirm any durable content already has canonical counterparts. Distinguish active dependencies from historical mentions and unrelated absolute `/tmp/**` configuration. After deletion, add a root-relative `tmp/` ignore rule and verify it with `git check-ignore -v` to prevent recurrence.