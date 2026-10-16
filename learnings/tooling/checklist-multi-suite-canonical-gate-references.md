---
title: "Kanonická brána pro více offline sad potřebuje samostatné reference"
date: 2026-10-16
category: tooling
component: ci-cd
tags: [acceptance, test-gate, pytest, provenance]
file_type: checklist
---

Při evidence-only opravě se seznamem několika focused a broader příkazů vyžádej od caller-owned Test Gate výsledek pro každý přesný příkaz a jeho pracovní adresář. Pokud brána přijímá jediný příkaz na běh, ulož samostatné run ID pro každou sadu a v checkpointu je propojuj s argv, cwd, exit code a počtem testů. Samotný historický RED/GREEN proof ani lokální make test tento původ výsledku nedokládají. U ai-research je širší registrovaná brána cd ~/Projects/ai-research && make test, která spouští také quiz, viewer a command-contract testy.