---
title: "Odstraneni mrtveho runtime vyzaduje charakterizaci udrzovane cesty"
date: 2026-07-21
category: tooling
component: frontend
tags: [dead-code, static-runtime, json-manifest, tdd]
file_type: checklist
---

# Odstraneni mrtveho runtime vyzaduje charakterizaci udrzovane cesty

Kdyz staticka aplikace po migraci stale obsahuje puvodni aplikacni server, nejbezpecnejsi odstraneni kombinuje omezenou kontrolu volajicich s testem cilove architektury.

## Postup

- Prohledej pouze udrzovany kod, dokumentaci, workflow a pomocne skripty. Historicke plany a docasne artefakty nejsou aktivni volajici.
- Pred smazanim pridej charakterizacni test, ktery soucasne dokazuje absenci serveru, staticke nacteni manifestu a konstrukci URL pro detailni JSON.
- Over generator manifestu presnou rovnosti mnoziny zdrojovych cest a manifestovych cest. Samotny pocet zaznamu by neodhalil zamenenou nebo duplicitni cestu.
- Aktualizuj reusable learnings, ktere aktivne doporucuji odstraneny runtime; historicke zaznamy nech beze zmeny.

## Quiz invariant

Jedinou runtime cestou je `quiz/levels/*.json` -> `quiz/build-index.js` -> `quiz/levels/index.json` -> staticke cteni v `quiz/app.js`. Lokalni HTTP lze pripadne zajistit generickym statickym serverem, nikoli kompatibilnim API.

## Gotcha

Sirsi test suite muze obsahovat znamy nesouvisejici baseline failure. Zachovej jeho plny vystup a nemen semantiku produkcniho kodu ani test jen proto, aby byl cely gate zeleny.
