---
title: "Volitelný odvozený soubor nesmí předstírat úspěch"
date: 2026-08-11
category: architecture
component: general
tags: [youtube-pipeline, analysis-artifact, graceful-degradation, contract-tests]
file_type: rules
---

# Volitelný odvozený soubor nesmí předstírat úspěch

V tomto repozitáři je přítomnost `analysis_main.md` veřejný completion signal: viewer i knowledge příkazy podle existence souboru rozhodují, zda je strukturovaná analýza dostupná. Chybovou hlášku proto nelze bezpečně uložit pod stejným názvem jako úspěšný výstup.

## Pravidlo

Po úspěšném zachycení přepisu a selhání volitelné LLM analýzy:

- zachovat `transcript_clean.txt`,
- chybu ponechat v existujícím logování,
- nevytvářet ani neuploadovat `analysis_main.md`,
- nepřidávat paralelní status manifest, pokud už absence souboru jednoznačně vyjadřuje nedostupnost.

## Integrační kontrola

Změnu producenta je nutné ověřit přes všechny repository-owned konzumenty. Pro transcript-only složku testovat:

- viewer listing vrací `hasTranscript: true` a `hasAnalysis: false`,
- analysis endpoint zachová existující `404 Not found`,
- generátory strukturovaného obsahu zdroj explicitně přeskočí nebo zastaví,
- index video ponechá, ale nevygeneruje odkaz na chybějící analýzu.

Deterministický viewer test používá environment override kořene KB; produkční default zůstává beze změny. Markdown slash commands lze bez nové runtime vrstvy chránit dependency-free kontraktními testy nad jejich skutečnými specifikačními soubory a zahrnout je do root `make test` gate.
