---
title: "Evidence-only follow-up nerozšiřuje původ důkazu Test Gate"
date: 2026-10-16
category: tooling
component: tooling
tags: [acceptance, tdd, test-gate, provenance]
file_type: checklist
---

# Evidence-only follow-up: proof o poznámce není kanonická Test Gate

Když už existuje historický RED/GREEN pro produkční refaktor, nový RED lze pořídit pouze pro skutečně chybějící následný artefakt (například ověřovací poznámku); v důkazu výslovně uveď, že se netýká původního refaktoru. `proof-capture.py` ověří shodu cíleného příkazu a zaznamená skutečný výstup RED/GREEN, ale nevydává záznam caller-owned Test Gate.

V tomto projektu lokálně prošly zaměřené pytest sady (6, 4, 22 testů), celá pipeline (50 testů) i kořenové `make test` (quiz 6, viewer 2, contracts 4, pipeline 50). Přesto nelze výsledek označit za kanonický, pokud prostředí nevystavuje Test Gate s vlastními run ID, cwd, argv, exit code a statusy. Do checkpointu zapiš přesné lokální výsledky a blokaci, nepřisuzuj shellovým běhům původ brány. Pro uzavření acceptance musí volající připojit své gate reference.
