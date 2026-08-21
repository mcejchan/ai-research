---
title: "Rerun the exact gate for evidence-only acceptance fixes"
date: 2026-08-21
category: tooling
component: ci-cd
tags: [acceptance, test-gate, evidence, make]
file_type: rules
---

# Rerun the exact gate for evidence-only acceptance fixes

When acceptance rejects an otherwise correct implementation because historical command evidence is unavailable, do not edit production code or retroactively strengthen the parent checkpoint. First verify that the parent diff is already committed and that the rejection concerns evidence rather than behavior.

Then rerun the exact required command from the exact required working directory. Preserve the command, working directory, exit status, and suite outcomes in the follow-up session and checkpoint. A narrower substitute, such as running only `pytest` when the contract requires root `make test`, does not satisfy the gate because the root target may aggregate additional suites.

If the fresh gate passes, the follow-up remains evidence-only. Escalate to code changes only when the exact gate reveals a concrete defect attributable to the implementation.
