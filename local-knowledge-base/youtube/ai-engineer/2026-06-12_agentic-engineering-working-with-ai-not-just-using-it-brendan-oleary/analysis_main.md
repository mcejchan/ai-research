# Agentic Engineering: Working With AI, Not Just Using It — Brendan O'Leary  
**Kanál:** AI Engineer  
**URL:** https://youtu.be/BEKc4P87XKo?si=2451H8mN51BXQzts

## Úvod

Brendan O'Leary otevírá rozhovor tím, co myslí pod pojmem **agentic engineering**. Ptá se, jak lidé vlastně používají AI v práci: ne jenom „pomáhá mi to psát kód rychleji“, ale jaký je skutečný workflow, co člověk AI předává, co si nechává a jak se rozhoduje mezi tím. Tvrdí, že většina inženýrů už AI nějak používá, ale málokdo by dokázal přesně popsat, **jak s ní skutečně pracuje**. A právě ten rozdíl mezi „používám AI“ a „umím s ní pracovat“ je podle něj hlavní téma celého rozhovoru.

Říká také, že vývoj AI ve vztahu k softwarovému inženýrství je velmi rychlý a přitom překvapivě krátký. Na začátku 20. let uměly modely doplňovat řádky kódu, pak přišla v roce 2022 schopnost navrhovat celé funkce a vznik GitHub Copilotu, a v roce 2025 se začalo lámat něco zásadního: modely už nejen navrhují, ale i **vykonávají**. Umí vzít úkol, rozdělit ho, zjistit, které soubory je potřeba změnit, provést změny, spustit testy a vrátit pull request. To už podle něj není jen rychlejší autocomplete, ale spolupracovník.

Brendan cituje také Armina, autora Flasku, který to vystihl větou, že už **nepoužíváme stroje, ale pracujeme s nimi**. A právě to je podle něj ten správný mentální model: AI agenti jsou někde mezi nástrojem a kolegou, spíš jako další inženýr, jen s tím rozdílem, že „četl každý Stack Overflow post na světě“. Zároveň ale zdůrazňuje, že je potřeba je vnímat jako **nadšeného, extrémně dobře načteného, ale často sebevědomě chybn ého juniora**. Jsou rychlí, neunavují se, nemají ego a bez problému něco přepíšou šestkrát, ale nemají judgment, neznají byznysový kontext a snadno udělají něco technicky správně, ale kontextově špatně.

Brendan zmiňuje i Armina, který říká, že mu stroj ušetřil víc než 30 % času. Ale ten zisk podle něj nevznikl tím, že by nechal AI dělat všechno. Vznikl proto, že přesně ví, co může delegovat a co si musí nechat. To je podle něj rozdíl mezi používáním AI a prací s AI.

## Context engineering: co dát modelu a co nechat mimo

Pak se dostává k tomu, co považuje za úplně nejdůležitější dovednost: **context engineering**. Cituje Karpathyho, který to popisuje jako citlivé umění a vědu zaplnění kontextového okna přesně tím, co je potřeba, aby agent měl správný kontext pro další krok. To je důležité hned z několika důvodů.

Za prvé, kontext je drahý. Každý token, který pošlete do kontextu, zvyšuje cenu, protože se celá historie chatu vrací jako vstupní tokeny při každém dalším kroku. A za druhé, víc kontextu neznamená automaticky lepší výsledky. Naopak, příliš velký kontext může model zhoršit, až někam kolem 50 % zaplnění se kvalita může začít lámat a model může působit „hloupěji“.

Brendan upozorňuje, že problém nejsou jen velké kontexty, ale i **špatné kontexty**. To se stává, když se smíchají dvě nesouvisející úlohy, když v kontextu zůstávají zastaralé komentáře nebo když se člověk s agentem vydá špatným směrem a později se pokouší ho vrátit zpátky. Agent ale nerazí stejný typ logického přemýšlení jako člověk. Všechen předchozí kontext si nese dál, může se v něm ztratit a může si přinášet i staré negativní vzory. Proto je podle něj lepší nenechat tyhle chyby narůstat a v momentě, kdy se věci začnou rozjíždět špatným směrem, **začít novou session**.

Říká, že skutečná práce inženýra je v tom, aby uměl kontext řídit. To znamená:

- ukládat důležité informace mimo kontextové okno, například do scratch padů, memory files nebo agents.md,
- vybírat jen relevantní informace pro aktuální krok,
- nechat v kontextu jen to, co je skutečně potřeba,
- zmenšovat, trimovat a komprimovat kontext po větších debugovacích nebo rešeršních seancích,
- izolovat kontext a rozdělovat práci do více agentů nebo více sessions.

Podle něj je to mimochodem podobné tomu, co by řekl novému engineering managerovi o řízení juniorního vývojáře. Vypráví vlastní zkušenost z prvního manažerského jobu ve zdravotnické softwarové firmě. Tehdy se objevoval iPad a on dostal nápad použít ho pro sběr pacientské historie, tedy formuláře, který se vyplňuje každý rok u doktora. Vytvořil wireframe v Balsamiqu, klasickém nástroji pro mockupy, který používá například Comic Sans a směšné smajlíky jako placeholdery. Ten wireframe předal internům s tím, že je to skvělý greenfield projekt.

Po několika týdnech dostal zpět funkční prototyp, který měl Comic Sans a emoji placeholdery. A to přesně proto, že to bylo ve specifikaci. Brendan z toho vyvozuje, že chyba nebyla na straně internů, ale na jeho straně jako manažera: nedodal správný kontext o tom, co je důležité a co ne, a jaký problém se vlastně řeší.

Z toho podle něj plyne několik jednoduchých návyků: neřešit pro každý úkol všechny čtyři aspekty najednou, ale držet se principu **jedna úloha na jednu session**, sledovat svůj „context meter“ a když máte pocit, že se to rozjíždí špatně, pravděpodobně se to skutečně rozjelo špatně. V takovém případě je lepší začít novou session a nechat AI, aby sama shrnula, kde se nacházíte. „Turns out that AI is really great at writing prompts for AI,“ říká, a doporučuje nechat agenta shrnout dosavadní práci, zkontrolovat, že to odpovídá vaší představě, a teprve pak začít novou session se správným kontextem.

## Research, plan, implement: lepší workflow než „napiš mi funkci“

Pak přechází k tomu, jak to celé používat v praxi. Zmiňuje, že existuje spousta workflow a že část z nich má sepsanou i na **path.kilo.ai**, kde jsou různé trendy, nápady a workflow patterny. On se ale pořád vrací k jednomu z jednodušších a přitom velmi účinných přístupů: **research → plan → implement**.

Podle něj je to důležité hlavně proto, že spousta lidí při prvním použití agentického inženýrství rovnou řekne: „Pomoz mi implementovat tuhle feature.“ Modely sice umějí generovat hodně kódu, ale skočit hned do implementace často vede k chybným předpokladům, plýtvání časem a frustraci. To pak živí představu, že AI je k ničemu, nebo že je to jen „garbage in, garbage out“. Brendan připomíná, že i vizuální a modelové schopnosti AI se za poslední roky dramaticky posunuly, ale aby výsledky byly dobré, musíme jim vytvořit dobré podmínky.

Základ je podle něj nejdřív **pochopit problém** a ujistit se, že mu rozumíte vy i agent. Pak je potřeba rozepsat explicitní kroky implementace. A teprve potom má smysl přejít k psaní kódu. Cituje Dex Horthyho, který říká, že špatný výzkum může znamenat stovky řádků špatného kódu. Proto je podle Brendana klíčové investovat čas do výzkumu a plánu.

V první fázi používá nástrojový režim zaměřený čistě na rešerši. V Kilo to nazývají **ask mode**. Ten neumí nic měnit, může jen chatovat, případně číst soubory, pokud mu to dovolíte, ale nemůže začít přímo kódovat řešení. Cílem je pochopit systém: jak dnes funguje, které soubory se budou měnit, jaké existují existující vzory, jak se liší od něčeho, co už v projektu je, kudy teče data a jaké edge cases je potřeba zvážit. AI je podle něj v brainstormingu skvělá, takže umí upozornit na slepé skvrny.

Výstupem z této fáze je dokument s výsledky rešerše, který si člověk přečte a potvrdí si, že odpovídá jeho chápání problému. Pak teprve přichází plánovací fáze. Tam se definují další kroky, konkrétní soubory, které se mají vytvořit nebo změnit, případné kódové ukázky, ale ne nutně vždy, a hlavně způsob ověření: jak poznáme, že je změna správně? Jaké testy upravíme nebo přidáme? Co je v rozsahu a co už ne?

Výsledkem je jasný plánovací soubor, často v repozitáři ve složce **plans**. Ten má být krok za krokem, se specifickými změnami a testovacími příkazy, aby bylo možné změnu verifikovat. Díky tomu je pak možné použít i menší, rychlejší nebo levnější model pro samotnou implementaci, protože nejdůležitější myšlení už proběhlo předtím. Při implementaci pak může člověk začít novou session, dát jí jen plán a držet kontext malé.

Brendan říká, že tady má velký význam i **Git**. Na lokálu ho používá jako první vlastní code review ještě předtím, než se vytváří pull request pro kolegy. Postupné iterace a časté commity pomáhají držet pod kontrolou změny, které agent dělá. A znovu zdůrazňuje, že lidský čas v plánování a rešerši je ten s nejvyšší návratností. Když se začne implementovat, mělo by být už všechno těžké přemýšlení hotové. Dex Horthy podle něj správně říká, že AI neumí nahradit myšlení, jen zesiluje myšlení, které už bylo odvedeno, nebo naopak zesiluje to, co odvedeno nebylo.

## Módy, pravidla, agents.md a skills.md

Další část se věnuje tomu, jak si agenty nastavit. Brendan mluví o **modech** a customizacích, například o režimech **ask, code, architect**. Každý z nich má jinou roli: ask je na rešerši, architect na plánování a code na samotnou implementaci.

Vedle toho je potřeba mít i sadu pravidel pro workspace, tedy pro konkrétní repozitář nebo globálně na stroji. Agent je umí načíst a použít, ale jen tehdy, když jsou napsaná. Tady podle něj hodně pomáhá i to, že si člověk průběžně ladí chování agentů podle toho, jak se s nimi učí pracovat. Kolik agentů spouštět paralelně, jestli používat work trees, jak moc auto-approve povolit, co všechno může agent dělat samostatně, jestli může číst soubory mimo workspace, spouštět testy a podobně. To všechno je potřeba nastavit podle míry komfortu a postupně měnit, jak se člověk s nástroji sžívá.

Pak přidává užitečný rámec tří hlavních vrstev konfigurace: **módy**, **agents.md** a **skills.md**.  
- **agents.md** je podle něj dnes de facto standard pro vždy dostupné informace o projektu, něco jako README pro agenty. Má obsahovat minimum toho, co agent potřebuje vědět: konvence, build a test příkazy, požadavky před commitem.  
- **skills.md** jsou naproti tomu konkrétní workflow a opakovaně použitelné playbooky. Pokud něco děláte často, třeba generování changelogů nebo nějaké pravidelné procesy, je dobré z toho udělat skill, který agent použije, když je potřeba. Skill je tedy obvykle na vyžádání, zatímco agents.md je skoro vždy načtený v kontextu.

Na závěr přidává několik power-user tipů z Kilo, ale s tím, že většina z nich se hodí i pro jiné agenty. Zmiňuje at-mentioning pro rychlé přidání souborů, commitů nebo výstupu z terminálu do kontextu, slash commandy pro start nové úlohy nebo zkomprimování kontextu, a také možnost ve VS Code označit část kódu, kliknout pravým a přidat ji do Kilo, aby s ní šlo dál pracovat. Užitečné je i autocomplete, nejen v kódu, ale i při samotném promptování.

Mluví také o tom, že použití agentů se přesouvá mimo IDE. Dnes je podle něj čím dál přirozenější mít je v CLI, na mobilu, v cloud agentu nebo přímo ve Slacku. A je to podle něj dobře, protože se tím AI posouvá blíž k představě asistenta nebo kolegy, který je dostupný tam, kde ho zrovna potřebujete.

## MCP, nástroje a přístup k dalšímu kontextu

Další důležitá část rozhovoru se věnuje **model context protocolu, MCP**. Brendan zdůrazňuje, že slovo „context“ je součástí názvu schválně. Modely byly původně jen systémy, které přijímají vstupní tokeny a vrací výstupní tokeny. Postupně se ale naučily používat nástroje, například spouštět testy nebo měnit prostředí. MCP tuto možnost rozšiřuje o další nástroje, které může agent používat.

Jako příklad uvádí **GitHub MCP**, který dává agentovi přístup k GitHub API, pull requestům, komentářům a issue, nebo **Context7**, který pomáhá s aktuální dokumentací frameworků. To je důležité, protože modely mají cutoff date a neznají vše, co vzniklo později. MCP servery jsou podle něj velmi užitečné a existují jich tisíce.

Zároveň ale varuje před jejich nadměrným používáním. Každý MCP server přidává do systému informace o nástrojích a ty se posílají do promptu při každé interakci. Pokud některý server právě nepoužíváte, měli byste ho vypnout. Uvádí příklad s Postgres MCP: když člověk dělá čistě front-endovou práci a databáze do toho vůbec nevstupuje, je zbytečné mít databázový MCP zapnutý. Nejenže plýtvá tokeny, ale může i zmást agenta a navést ho k tomu, aby si myslel, že má databázi používat.

Na konci přechází k tomu, že enterprise týmy často řeší i přístup k interním platform APIs. Říká, že existují zhruba čtyři různé způsoby, jak to dělat, ale v přepisu tato část už pokračuje dál.

## Zmíněné odkazy a zdroje

- https://youtu.be/BEKc4P87XKo?si=2451H8mN51BXQzts
- https://path.kilo.ai/
- GitHub Copilot
- Flask
- Balsamiq
- GitLab
- Model Context Protocol (MCP)
- GitHub MCP
- Context7