---
title: "Plán opravného úkolu potřebuje platnou hlavičku"
date: 2026-10-16
category: tooling
component: tooling
tags: [compound-plan, acceptance, invalid-header]
file_type: checklist
---

Když monitor obnovuje plán po chybě `plan_artifact_invalid: status=invalid_header`, nestačí mít pouze povolené `##` sekce: soubor musí začínat i titulkem `# Plan: ...`. Nejprve spusť přesně požadovaný `plan-path.py --task-id ... --project . --title ... --touch`, přečti existující plán na vrácené cestě a oprav jeho hlavičku bez zakládání druhého plánu. Před předáním znovu přečti soubor: titulní řádek musí být první a názvy `##` sekcí musí odpovídat povolenému seznamu zadání.