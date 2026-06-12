# Ralph Loops: Build Dumb AI Loops That Ship — Chris Parsons, Cherrypick  
**Kanál:** AI Engineer  
**URL:** https://youtu.be/2TLXsxkz0zI?si=H1UL2kKGa36wXIRT

## Úvod
Chris Parsons uvádí 2hodinový workshop o „Ralph loopech“. Ptá se, kdo už ví, co to je, a je vidět, že většina lidí v místnosti už o tom něco slyšela. Vysvětluje, že workshop nebude jen teorie: účastníci mají pracovat na vlastních laptopech, společně si vyzkoušet praktické použití a na konci si odnést něco funkčního.

Říká, že ukáže jen pár slidů, většina bude živá demonstrace a interakce. Jako cíl zmiňuje jednoduchý toy projekt — Pomodoro timer — ale s tím, že principy by měly být použitelné i na reálnou práci.

Ptá se také, kdo používá Claude Code nebo Codex ke psaní kódu, a pak i kdo je používá na veškerý kód. V místnosti je podle něj vidět obrovská změna oproti minulosti. Stejně tak se ptá, kdo tyto nástroje používá i na neprogramátorské úkoly. Naznačuje, že „budoucnost už je v místnosti“, ale stále jsme na začátku té cesty.

Nakonec se ptá, kdo už někdy stavěl Ralph loops. Jen pár lidí zvedne ruku, a Chris říká, že se na ně bude spoléhat. Představuje se: jmenuje se Chris Parsons, je CTO backgroundem, pracoval na několika VC-backed startupch a scale-upech a dnes většinu času pomáhá týmům přemýšlet, jak s AI vůbec pracovat. Má zhruba 30 let zkušeností se softwarem, byl i CEO agentury, dělal agile consulting a training. Dodává, že principy, které se kdysi učily v agilním světě, jsou pořád velmi relevantní i pro AI.

## Od těžkopádných workflow k jednoduchým loopům
Chris ukazuje, jak dříve pracoval s AI: měl složitý n8n workflow pro tvorbu newsletteru. Trvalo mu asi týden, než ho napsal, nemluvě o testování a ladění. Workflow obsahovalo několik větví, například pro featured article flow, který četl různé články z blogu, kontroloval, jestli už byly publikované, shrnoval je pomocí AI a vkládal do newsletteru. Další část tahala odkazy z určitého seznamu a dělala k nim komentář.

Říká, že to sice fungovalo, ale bylo to křehké. Každé pondělí kolem druhé odpoledne dostal dreaded notification z n8n, že workflow selhalo, a musel běžet zpět do workflow, hledat, co se rozbilo, a opravovat to. Zdůrazňuje, že to není útok na n8n — je to skvělý nástroj a bez něj by AI orchestraci tímto způsobem vůbec nedokázal. Umí dobře spravovat API keys a všechno spojit dohromady. Jenže při téhle úrovni komplexity to bylo moc křehké a výsledný užitek nebyl moc velký. Často bylo jednodušší napsat newsletter ručně než udržovat systém, který ho generoval.

Pak ukazuje, že budoucnost je spíš v loopu, ne v těžké orchestraci. V Claude Code má skill, který pro něj píše newslettery. Vzal n8n JSON a nechal Claude napsat skill na základě toho flow. Claude pak postupně čte instrukce, rozhoduje, co udělat dál, volá nástroje a zpracovává úlohu v několika krocích, než se dostane ke konci a vyprodukuje newsletter. Chris říká, že je to stejný princip jako u kódu: popíšete, co chcete, a Claude to postupně udělá.

Podstatné podle něj je, že Claude Code běží v loopu: přečte skill, zavolá nástroj, vrátí se na začátek, přečte znovu, zavolá další nástroj a nakonec se samo ukončí. Výsledkem jsou lepší, koherentnější newslettery než z předchozí workflow. Skill samotný téměř neupravuje, jen po dokončení procesu Claude požádá, aby si z běhu zapsal, co by příště měl dělat jinak. Občas něco málo upraví, ale je to mnohem jednodušší než dřívější workflow.

Z toho vyvozuje obecnou myšlenku: agenti, workflow i automatizace mají v jádru loop. Novější modely — podle něj hlavně GPT-5.1 a výš a Claude Opus 4.6 / Sonnet 4.6 a výš — začínají tento model zvládat opravdu dobře. Zmiňuje, že u Metys/Methos si není jistý, slyšel o něm různé věci, ale nechce spekulovat. Naznačuje, že možná ani nebudeme potřebovat skills v dnešní podobě, možná bude stačit jen „write a newsletter“ a model to udělá sám. Hlavní pointa je, že místo složitých workflow používáme mnohem víc context a loops.

## Co je Ralph loop a proč se tomu tak říká
Chris přechází k tomu, co je vlastně Ralph loop. Říká, že myšlenka přišla od Jeffreye Hintona Lee „v dávných dobách AI“, což ironicky označuje jako „asi loňský červen“. Základní princip popisuje jednoduše: kdykoli dokončíme použití AI pro nějaký úkol, měli bychom ten samý úkol zkusit znovu. Zadáme stejný prompt a sledujeme, co se stane.

Vysvětluje, že název je podle Ralpha Wigguma ze Simpsonových, který prostě zkouší totéž pořád dokola, dokud to nevyjde. Podstata Ralph loopu je podle něj přesně tohle: dej modelu úkol, a když řekne, že je hotovo, spusť ho znovu. Model si často při dalším průchodu všimne, že něco vynechal nebo nedokončil. To byl velký problém starších AI coding tools — nikdy nebyly úplně hotové. Když je pustíte znovu, samy najdou něco, co měly ještě opravit. Postupně se dopracují k „už jsem fakt hotový“.

Chris zdůrazňuje, že to není nic magického, jen opakované znovuzadání téhož úkolu. Výsledkem je, že model sám postupně opravuje, co přehlédl, a dělá lepší práci. Říká, že je to užitečný způsob, jak přimět AI, aby se „dovyrobila“ až do skutečného konce.

## Live demo: jednoduchý Pomodoro timer
Chris přechází k živé ukázce. Zkouší sdílení obrazovky a ukazuje velmi jednoduchý Pomodoro timer, který sám předtím napsal asi za tři minuty. Říká, že není dobrý, ale právě o to jde. Když v Pythonu spustí `pomodoro start`, timer se jen spustí. Neexistuje způsob, jak zjistit, kolik času zbývá nebo jestli je hotovo — a přesně to chce změnit.

Projekt má aspoň testy, protože „každý self-respecting vibe coded AI projekt musí mít testy“. Ukazuje, že je tam jedna testovací kontrola, která ověřuje, že start funguje. Vysvětluje strukturu: skript jen spustí start command a uloží čas do souboru `~/.pomodoro` v home directory. Je to velmi jednoduchý projekt, ale má nový folder s „tickets“ — tedy seznam vylepšení, která by se dala implementovat.

První ticket říká, že by bylo fajn vidět, kolik času zbývá do konce Pomodora, ne jen ho umět spustit. Chris připravil jednoduchý ticket systém, který má sloužit jako vstup do loopu. Přiznává, že neví, jestli jsou ty tickets dobré, protože je nezkoumal do detailu. Cílem je ale použít je k rozběhnutí práce v loopu.

Pak spouští Claude a říká mu, aby implementoval první ticket. Claude si přečte ticket, provede změny a po diffech je vidět, že přidal nový status command a dokonce i nový test, i když o něj nebylo výslovně požádáno. Chris s nadsázkou říká, že to je k neuvěření: AI přidala test sama od sebe.

Pak to zkusí znovu se stejným zadáním. Zmiňuje, že před rokem by to byla zásadní fáze, protože by model určitě něco vynechal. Teď už je Claude Opus lepší a často si všimne, že něco chybí. V jednom průchodu dokonce pochopí, že má aktualizovat status na done. Chris to označuje za ukázku raného Ralph loop principu: opakování přiměje model odhalit, co neudělal. Když to pustí ještě jednou, Claude už jen vrací, že pokud běží Ralph loop, vezme další ticket. Chris se směje, že mu model „kazí prezentaci“.

## Jak s loopem pracovat prakticky
Chris vysvětluje, že další možnost je úplně smazat kontext a znovu zadat totéž: `implement doc ticket 001`. Tím testuje, co model udělá bez předchozího stavu. I tak ticket najde a testy projdou. Zmiňuje, že první nápad na Ralph loops u některých lidí byl jednoduchý stop hook v Claude Code pluginu, který po dokončení jen znovu spustil ten samý příkaz. To ale moc nefungovalo, protože se tím nepokročilo dost daleko.

Prakticky užitečnější podle něj bylo spouštět Claude Code v explicitní smyčce, například přes `while true` a uvnitř opakovaně volat `Claude implement ticket 001`. Říká tomu „nejhloupější Ralph loop“, ale přesně to funguje: jednoduchý loop, který pořád dokola implementuje věci. Je to snadné a funguje to překvapivě dobře.

## Cvičení pro účastníky
Chris pak vrací pozornost k publiku. Říká lidem, aby si otevřeli notebooky, stáhli si kód z jeho GitHubu pod názvem `pomodoro workshop` a rozjeli projekt. Vysvětluje, že možná bude potřeba nastavit Python, ale mělo by to být jednoduché. Pak mají spustit testy a firem Claude Code nebo Codex a nechat je implementovat ticket 001.

Výslovně říká, aby zatím nepřidávali další tickety. Má to zůstat na jednom kroku, aby si všichni vyzkoušeli základní loop. Pokud už to pro ně bude úplně triviální, mají zkusit Codex nebo podobný nástroj, případně totéž aplikovat na vlastní projekt. Zatím chce dát lidem pár minut na setup a potom bude pokračovat dál.

## Otázky z publika
Následuje Q&A. Jeden z účastníků se ptá na „B Mad method“ a na to, jestli Chris zkoušel workflow, kde agent prochází celý software development lifecycle, build, test, a všechny fáze procesu. Chris odpovídá, že ano, a že je to velmi zajímavé, protože to otevírá dobré otázky kolem kontextu i skutečné hodnoty práce. Slíbí, že se k tomu možná ještě vrátí na konci, a žertem dodává, aby se ho na stejnou otázku zeptali znovu, pokud se k ní dostatečně nedostal.

Ptá se, jestli někdo už implementoval první ticket. Několik lidí zdvihne ruku. Chris si všimne, že někteří asi jen signalizují, že jsou hotovi, i když nebyli přímo vyzváni k otázce. Říká, že je dobře, že už se několik lidí rozjelo, a vrací se k tomu, jak to celé dál škálovat.

Zmínkou o Mattu Pocockovi říká, že tuto myšlenku dostal právě od něj. Pokud Matt sleduje záznam, děkuje mu. Na začátku mu totiž Ralph loops přišly jen jako zajímavý trik, který občas pomůže najít chybu, ale nemění všechno. Později ale zjistil, že to opravdu mění celý jeho způsob práce s kódem.

Pak vysvětluje další krok: nejde jen o to zajistit, že Claude dokončí jeden ticket. Zajímavější je, co se stane, když ten loop namíříte na celý seznam úkolů. Původně zkoušel, jestli model zvládne rozbít velký projekt na spoustu menších ticketů, pak z těch udělat ještě menší, určit dependencies a navrhnout práci více agentů. Přiznává, že to byla spíš ukázka selhání, než úspěchu, ale bylo to užitečné právě tím, že ukázalo hranice tohoto přístupu.

## Zmíněné odkazy a zdroje
- YouTube video: https://youtu.be/2TLXsxkz0zI?si=H1UL2kKGa36wXIRT
- GitHub projekt: `pomodoro workshop`
- n8n
- Claude Code
- Codex
- Cursor
- Python
- Pomodoro timer
- Claude Opus 4.6
- Claude Sonnet 4.6
- GPT-5.x / GPT-5.1
- Mattt Pocock / Matt Pocock
- B Mad method