---
title: "Oddělte TDD důkaz od kanonické brány a finálního shrnutí"
date: 2026-10-16
category: tooling
component: ci-cd
tags: [acceptance, test-gate, tdd, final-note]
file_type: checklist
---

U evidence-only opravy YouTube pipeline prokazuje historický RED/GREEN proof pouze soustředěnou sadu (6 testů). Souhrn počtů v checkpointu není kanonickým důkazem dalších sad. Vyžádejte od caller/orchestratoru čerstvou kanonickou Test Gate pro přesné focused i širší příkazy, s argv, cwd, návratovým kódem a referencí; neoznačujte lokální shell za caller-owned gate. Samostatně zapište finální note s přesnými výsledky, 24 řádky run_for_url, vlastníkem path_slugs.py, napojenými volajícími a odlišným chováním title slug. Historický RED zachovejte; nevyrábějte nový RED po hotové implementaci.