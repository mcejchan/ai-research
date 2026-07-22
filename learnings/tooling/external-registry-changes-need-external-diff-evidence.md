---
title: "External registry changes need external diff evidence"
date: 2026-07-22
category: tooling
component: ci-cd
tags: [acceptance, registry, test-gate, evidence, git]
file_type: rules
---

# External registry changes need external diff evidence

When a project task changes configuration stored outside the project repository, a project-scoped diff cannot prove that the change was delivered. Acceptance may reject correct runtime state if its evidence bundle contains only repository-local files.

For `ai-research`, the root `make test` gate lives in the project repository, but its authoritative `testCommand` lives in `/Users/michal/.openclaw/workspace/skills/opencode-dev/projects.yaml`. After changing that entry, capture the diff from the registry's own Git worktree and include it in the task evidence:

```bash
git -C /Users/michal/.openclaw/workspace diff -- skills/opencode-dev/projects.yaml
```

Also run the registered command exactly, rather than an equivalent command assembled manually. This proves both the external wiring and the delegated project behavior. If the behavioral RED/GREEN cycle was completed by a parent task, link its genuine proof and record only fresh GREEN verification; never manufacture a new RED for a YAML-only follow-up.
