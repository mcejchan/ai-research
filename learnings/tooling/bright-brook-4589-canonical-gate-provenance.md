---
title: "Treat repeated evidence rejection as a provenance problem"
date: 2026-08-21
category: tooling
component: ci-cd
tags: [acceptance, test-gate, evidence, provenance]
file_type: rules
---

# Treat repeated evidence rejection as a provenance problem

An evidence-only acceptance follow-up can pass the exact required command and still be rejected when the result is recorded only as task-authored checkpoint prose. The implementation and test behavior are not defective in that case; the missing property is caller-owned provenance.

For a retry, preserve the historical evidence gap, leave production code unchanged, and run the registered command from the exact working directory requested by the caller. Report the command, working directory, exit status, and per-suite outcomes so the orchestrator can attach them to its canonical Test Gate record. Do not relabel a prior local shell transcript as historical or caller-owned evidence.
