---
title: "Create missing task checkpoints before resuming work"
date: 2026-05-18
category: tooling
component: tooling
tags: [checkpointing, task-resume, missing-file, workflow]
---

The task resume flow expected `plans/checkpoints/calm-vale-5131.checkpoint.md`, but the file did not exist and the initial read failed. The work proceeded cleanly after creating the checkpoint first and then updating it through each implementation/verification step.

Reuse this pattern when resuming tasks: if a checkpoint is required but absent, create it immediately instead of treating the missing file as a blocker. This keeps the task auditable and avoids losing progress context. Avoid assuming checkpoint files already exist just because a task ID exists.