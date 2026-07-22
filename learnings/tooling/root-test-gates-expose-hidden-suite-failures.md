---
title: "Root test gates expose hidden suite failures"
date: 2026-07-22
category: tooling
component: ci-cd
tags: [make, test-gate, pytest, node, configuration, ci]
file_type: rules
---

# Root test gates should expose configuration and latent suite failures

A repository-level test gate should remain a thin delegator: invoke each maintained subsystem runner unchanged, in a deterministic order, and let the first non-zero status stop the gate. For this repository, `make test` composes the quiz Node test, yt-viewer Node test, and pipeline `python3 -m pytest` without merging subsystem architectures.

## Import-time secrets hide useful test results

The pipeline previously read `DRIVE_FOLDER_ID` at module import. This prevented pytest collection and concealed failures later in the suite. Resolve operator-only configuration at the execution boundary instead:

- Imports and test collection must not require production credentials.
- Local/mock storage can run without a Drive folder ID.
- A real Drive client should fail clearly when execution begins and the ID is absent.
- The root gate should still pass explicit non-secret test values and use `python3 -m pytest`, not a globally installed `pytest` executable.

## Re-run the complete suite after fixing collection

Once collection was repaired, the Python suite exposed stale LLM tests that had been unreachable: the expected proxy URL no longer matched production, and a custom mock returned a new completion object on every property access, so calls could not be inspected. Fixing collection is not enough; run the entire delegated suite and repair newly visible test-infrastructure defects before declaring the root gate healthy.

For inspectable custom API mocks, retain stable endpoint objects and implement methods with `MagicMock(return_value=...)`. This preserves realistic return values while making call arguments observable.

## Deployment scope

A deployment workflow may use a justified subsystem preflight rather than the full repository gate when it does not provision unrelated dependencies. The quiz Pages workflow runs its dependency-free Node test before building and uploading, while the project registry uses the complete root gate.
