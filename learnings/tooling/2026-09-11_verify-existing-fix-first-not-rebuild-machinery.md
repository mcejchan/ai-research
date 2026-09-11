---
title: "Verification-only tasks: verify the existing fix first, don't rebuild the machinery"
date: 2026-09-11
category: tooling
component: general
tags: [planning, overengineering, tdd, verification-only, pytest]
file_type: rules
---

# Verification-only tasks: verify the existing fix first, don't rebuild the machinery

When a task is "verify/finish an already-applied repair," the plan must **lead with the
direct verification of the already-fixed root cause and the existing tests**, and only after
that offer any auxiliary evidence the brief requires.

## Problem
A plan for a one-line `pytest.ini` section fix (`[tool:pytest]` → `[pytest]`) was rejected
for overengineering: it led with venv recreation, proof-file relocation, a disposable
repository copy, and synthetic RED/GREEN capture instead of directly verifying the already-fixed
config and its existing regression tests.

## Rule
- For verification-only / "finish the repair" tasks, the **primary action is running the
  existing tests against the already-fixed config** (e.g. `pytest test/test_config.py -v` and
  the project's full `make test`), recording real commands/cwd/exits.
- Any mandated structured RED/GREEN evidence is a **secondary, explicitly-labelled supplement**
  (a fresh isolated reproduction in a disposable copy), never the main event and never claimed
  as original development chronology.
- Do not invent new regression tests, venv rebuilds, or artifact relocations just to "look
  like TDD."

## When to use
- Tasks whose goal states "finish verification of the EXISTING repair, not a second implementation."
- Any plan-review retry where feedback says "overengineered / directly verify the already-fixed root cause."

## Concrete
- The plan's first concrete step = the verification command, not setup choreography.
- Keep venv/install steps minimal and clearly a prerequisite, not a headline.
