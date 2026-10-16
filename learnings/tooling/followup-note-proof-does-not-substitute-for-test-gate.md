---
title: "Důkaz následného artefaktu nezastupuje kanonickou Test Gate"
date: 2026-10-16
category: tooling
component: tooling
tags: [acceptance, tdd, test-gate, provenance]
file_type: checklist
---

Při evidence-only follow-upu k již implementovanému refaktoru zachovej historický genuine RED pro produkční změnu. Pokud následný úkol vyžaduje nový RED/GREEN, otestuj skutečně chybějící následný artefakt před jeho vytvořením a výslovně odděl tento důkaz od původního refaktoru. Proof-capture.py potvrzuje pouze identitu cíleného příkazu a jeho RED/GREEN výsledek, nikoli širší suite. Lokálně úspěšný `make test` dokumentuj s pracovním adresářem a výsledky, ale bez caller-owned gate ID ho nikdy nepovyšuj na kanonický Test Gate záznam. V checkpointu pojmenuj tuto mezeru otevřeně.