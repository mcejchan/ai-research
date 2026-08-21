---
title: "Canonical test-gate evidence cannot be replaced by checkpoint prose"
date: 2026-08-21
category: tooling
component: ci-cd
tags: [acceptance, test-gate, evidence, provenance]
file_type: rules
---

# Canonical test-gate evidence cannot be replaced by checkpoint prose

When an acceptance goal requires a caller-owned canonical Test Gate, a task checkpoint that says `make test` passed is only a claim, even if it includes suite counts. The evidence must preserve the canonical runner's command, effective project-root working directory, exit status, and output or outcome reference.

If historical task evidence contains no exact command/outcome pair, keep that gap explicit. Do not rerun tests and attribute the fresh result to the parent session. Run the registered gate afresh for the follow-up task, link its canonical run identifier from follow-up state, and treat repository-authored checkpoint text only as a reference to that record.

For evidence-only follow-ups, leave completed production work unchanged unless the fresh gate exposes a concrete defect.
