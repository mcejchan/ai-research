---
title: "TDD důkaz v podprojektu: pracovní adresář určuje umístění"
date: 2026-10-16
category: tooling
component: tooling
tags: [tdd, pytest, proof-capture, monorepo]
file_type: checklist
---

# TDD proof helper: pracovní adresář určuje cestu kanonického důkazu

V repozitáři `ai-research` je Python projekt v `youtube-transcript-pipeline/`, ale úkolový důkaz musí vzniknout v kořenovém `plans/checkpoints/`. Pomocník `proof-capture.py` ukládá důkaz relativně k adresáři, ze kterého se spouští. Spuštění z adresáře pipeline by vytvořilo nesprávně umístěný artefakt.

Spouštěj pomocníka z kořene repozitáře a použij root-relativní cestu testu a explicitní pytest konfiguraci pipeline:

```bash
TASK_ID=<id> python3 /Users/michal/.config/opencode/skills/tdd/scripts/proof-capture.py red -- python3 -m pytest youtube-transcript-pipeline/test/test_refactor_contracts.py -q -c youtube-transcript-pipeline/pytest.ini
# stejný přesný příkaz použij ve fázi green
```

Testy importující `src` musí při tomto způsobu volání přidat kořen pipeline na `sys.path` před importem. V lokálním prostředí navíc není příkaz `python`, použij `python3`. Ověř `accepted_red` s nenulovým child exit a teprve pak upravuj produkční kód; následně `accepted_green` se stejným argv. Po běhu přečti kanonický soubor a zkontroluj obě sekce.
