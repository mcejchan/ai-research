---
title: "Final note je součást akceptačního kontraktu"
date: 2026-08-11
category: tooling
component: general
tags: [acceptance, final-note, verification, checkpoint]
file_type: checklist
---

# Final note je součást akceptačního kontraktu

Když akceptační cíl výslovně požaduje závěrečnou poznámku, úspěšné testy ani dokončený checkpoint ji nenahrazují. Monitor může správnou implementaci odmítnout, pokud chybí přesný seznam změněných souborů, konkrétní příkazy a výsledky ověření, úmyslné změny chování a stav odložených migrací.

## Postup opravy

Při dokumentačním acceptance follow-up neopakovat hotovou implementaci:

1. Dohledat commit původní implementace a z něj získat úplný file inventory.
2. Odkázat existující historický RED důkaz; po hotové implementaci nevyrábět falešný RED.
3. Spustit čerstvé focused testy i autoritativní široký gate.
4. Uložit přesné příkazy, počty testů a výsledky do task-specific checkpointu.
5. Výslovně uvést změny chování a to, zda historická data zůstávají samostatným follow-upem.

Takový checkpoint je restartovatelný důkaz, ale stejná fakta musí být také uvedena ve finální odpovědi, pokud je final note samostatným požadovaným deliverable.
