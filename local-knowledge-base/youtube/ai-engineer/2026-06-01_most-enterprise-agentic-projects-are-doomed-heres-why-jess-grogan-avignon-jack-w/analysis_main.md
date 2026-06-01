# Most Enterprise Agentic Projects Are Doomed, Here's Why — Jess Grogan-Avignon & Jack Wang, Accenture
**Kanál:** AI Engineer  
**URL:** https://youtu.be/AGkzpxMdPn8?si=MLh1fF4otzqhSF8n

## Úvod
Jess a Jack z Accenture mluví o tom, proč jsou podle nich většina enterprise agentic projektů odsouzena k neúspěchu. Vycházejí z práce s velkými organizacemi – telekomy, utility, státní správou, zdravotnictvím i consumer produkty – tedy s prostředími, kde má každé rozhodnutí reálné důsledky. Jejich hlavní teze je, že problém není jen v modelech nebo v datech, ale v samotném enterprise „scaffoldingu“: procesech, governanci, schvalování a infrastruktuře, které byly navržené pro lidskou rychlost, ne pro rychlost strojů.

---

## Human speed vs. machine speed
**Jess říká:** „We work in the world of enormous enterprises.“ Na této škále mají i malé chyby velké následky. Špatný deployment může například shodit kritickou národní infrastrukturu, a proto si tyto organizace během let vybudovaly vrstvy kontroly, procesů, opakovatelnosti a governance. Dlouho to fungovalo velmi dobře – firmy rostly a dosahovaly úspěchů, ale vždycky „at human pace“.

To se podle nich změnilo. Vstupujeme do světa strojové rychlosti, která transformuje práci, klienty i společnosti, na nichž tyto enterprise firmy stojí. Z jejich výzkumu vyplývá, že jen 12 % společností dosahuje toho, co nazývají **AI achiever**. Většina organizací zůstává u pilotů, utrácí miliony a často nevidí dostatečnou návratnost. Problém přitom není jen zbytečné utrácení; skutečné riziko je, že firmy začnou zaostávat v prostředí, které se zrychluje mnohem víc, než jsou schopné absorbovat.

Poukazují na to, že v enterprise světě často trvá i jednoduché rozhodnutí šest měsíců nebo déle, zatímco firmy jako Octopus, Klarna nebo Shein jednají úplně jiným tempem a přepisují pravidla hry. Někteří lidé sice pravidla studují, vytvářejí playbooky a absolvují workshop, ale pak odejdou. Oni zůstali a „shipped through the reality“. A právě v tom je podle nich rozdíl: když zůstaneš, zjistíš věci, které slide decky nikdy neprozradí.

Nejde jen o dostupnost dat nebo API. Rozhodující je celý enterprise systém kolem nich – ten samý systém, který tyto firmy historicky dovedl k úspěchu, ale který je dnes začíná brzdit v tom, aby AI hodnotu škálovala.

---

## Pět enterprise napětí: kde projekty narážejí
Jess a Jack slibují pět enterprise tensions z jejich zkušeností s nasazováním AI ve velkých firmách za poslední roky. Pokud je člověk pochopí, podle nich dokáže dost dobře předpovědět úspěch dalšího AI projektu ještě před jeho startem.

### 1) Enterprise procesy běží na lidskou rychlost
Jack říká, že asi před 18 měsíci bylo ještě potřeba vysvětlovat, proč je AI důležitá a proč záleží na rychlosti. Tahle bitva je ale podle nich vyhraná: C-level je přesvědčený, CEO se bojí, že zůstane pozadu. Přesto se enterprise rychlost zásadně nezměnila.

Není to tím, že by AI neuměla psát dobrý kód, ani tím, že by inženýři neuměli řešit kontextový problém. Je to hlubší: skutečný problém je enterprise scaffolding, tedy lidský operační systém navržený pro lidskou rychlost. V praxi to znamená data access, security reviews, deployment process a další vrstvy, které jsou v běžném enterprise světě nastavené tak, aby kombinovaly minimální engineering investice s množstvím stakeholder meetingů.

Jack popisuje konkrétní zkušenost z velké korporace, kde dostali agentic solution a centralizované AI gateway. Každá změna konfigurace musela projít manuální review, než se vůbec mohli dostat k testování. A přestože aplikace samotná byla hotová asi za dva týdny, trvalo dalších 12 měsíců dostat ji do produkce. Musely se sladit infrastruktura, security, AI gateway, data governance i aplikační týmy.

Přirovnává to ke Google Search: než uvidíte výsledky, tři týmy je chtějí zkontrolovat, pak je potřeba legal sign-off, a nakonec „počkejte dva týdny, protože je quarter end a change freeze“. Přesně tak dnes podle nich vypadá AI delivery v enterprise prostředí.

Zatímco vývojáři dostanou AI coding agenta a zdánlivě tím urychlí tvorbu, skutečný bottleneck se přesune do code review a deploymentu. A bude to ještě horší, protože coding agents dělají z builderů i PMů, designérů a domain expertů. Nabídka deployovatelného kódu exploduje, ale approval infrastruktura a deployment infrastruktura zůstávají stejné, protože byly navrženy pro lidské tempo.

Podle nich je skutečný technický dluh mnohem širší než legacy code v samotných aplikacích. Je to i dlouholeté podinvestování do engineering automation, CI/CD a všeho, co firmám dovoluje pohybovat se rychle a přitom zachovat kontrolu.

**Řešení?** Každý lidský proces musí být adaptovatelný a převoditelný do executable code. Ne další meeting, ne další sign-off chain, ale code. A dobrá zpráva je, že AI může pomoci tyto věci postavit rychleji a levněji. Nejde o nové schopnosti, ale o zásadní změnu mindsetu.

### 2) Business case není vždy správný rámec
Další téma je financování a business case. Jack připomíná, že každý, kdo někdy začínal projekt s business case kvůli internímu financování, pozná tenhle svět. Business case sám o sobě není špatný – klade správné otázky, vytváří dohled a hlídá ROI. Jenže předpokládá, že tři věci lze znát předem: scope a solution, očekávanou hodnotu a náklady s časem dodání.

U AI je to ale často obráceně. Řešení i business case se člověk učí až během práce. A jakmile náklady na prototypování, experimentování a buildování spadnou téměř na nulu, už nejde jen o efektivitu. Otevírají se zcela nové schopnosti a celé kategorie věcí, které dřív ekonomicky nešly dělat.

To znamená nové produkty, nové služby, nové customer experiences – věci, které čekají na to, až budou znovu vymyšlené. Podle jejich dat dosahují AI achievers zhruba o 50 % vyššího revenue growth než jejich peer group, a není to způsobené cost cuttingem, ale tím, že dělají úplně nové věci.

Jako příklady uvádějí AI produkty, které vznikaly emergentně. Cursor měl user base live coders, která v podstatě neexistovala v době, kdy produkt začali stavět nebo vydali. Cloud code také nebyl něco, co by bylo dlouho dopředu plánované v product roadmapě. Na enterprise straně zmiňují Walmart, který vytvořil social media trend scanner a generative designer, díky čemuž může konkurovat novým způsoby hráčům jako Shein a Temu. Nebo JP Morgan, který začal s interním productivity tool a nakonec jej produktizoval do nového revenue streamu.

Současné enterprise finance je ale nastavené na jistotu. Projekty se obvykle obhajují přes committed benefits a předvídatelné cost phasing. Tenhle rámec může projekt zabít ještě před začátkem, protože se ptá, jestli lze ospravedlnit konkrétní věc na základě predikovatelnosti, místo aby se ptal, co je nově možné.

Proto podle nich správná otázka zní: **What is the impact of not doing this? What is the cost of not doing this?** CFO by měl u agentic transformace přemýšlet jako VC. Venture capital nevsází na jeden projekt a nechce tříletý fixní guaranteed payback, protože ví, že certainty z business case je iluze. Místo toho staví portfolio betů a hledá ty, které se složí do exponenciální hodnoty. Stejně by se k AI mělo přistupovat i v enterprise: ne „dá se tento projekt obhájit?“, ale „děláme dost sázek napříč portfoliem, abychom trefili ty, které nám změní hru?“

Pokud finance neumí myslet tímto způsobem, podle nich by právě tam měla začít transformace. Všechno ostatní je downstream.

### 3) Delivery: scope podle hypotéz, ne podle tradičních feature plánů
Když se Jack ptá na data science a machine learning engineering lidi v publiku, říká, že by měli znát princip hypothesize and experiment, statistical confidence. Podle nich byli často v enterprise světě vnímáni jako „modern IT crowd“ – slušní, užiteční, ale víceméně ignorovaní, zatímco „nahoře“ se dělala skutečná práce přes Jira board a PI planning.

Tady ale vidí příležitost. Agentic delivery je jejich svět, ne svět tradičního enterprise řízení. Modely jsou non-deterministic, agent behavior is emergent, a nedává smysl je plánovat jako klasický feature build nebo fixní program. Přesto se o to organizace pořád snaží.

V delivery praxi podle nich problém není jen samotná stavba, ale hlavně překlenutí mezery mezi tím, jak systém skutečně funguje, a tím, co stakeholderi očekávají. Čas se pak utápí v utopickém návrhu dopředu, v nekonečných debatách o guaranteed performance a v endless status updates, které nevedou k rozhodnutí. To je to, co dnes nejvíc spotřebovává energii při delivery agentic systémů.

IT crowd není problém. Problém je, že se organizace musí naučit jejich jazyk. A tím jazykem je podle nich hypothesis-driven delivery. Program je potřeba stavět kolem jednoho cíle: building statistical confidence. Malé smyčky build, evaluate, iterate, fast evidence.

Delivery tým má zároveň vypadat jinak než klasický software tým. Jsou potřeba lidé, kteří zvládají ambiguity, umí formulovat, co se naučili, ne jen co dodali, a hlavně dokážou převádět statistická čísla do stakeholder confidence. To je jiný skill set, který je potřeba najímat, trénovat a také oceňovat.

### 4) Trust není vedlejší efekt, ale hlavní produkt
Další napětí se týká trustu. Jack říká, že jako společnost se učíme AI důvěřovat. Nikdo už dnes znovu nekontroluje Google výsledky a většina lidí v místnosti je pravděpodobně pohodlná s používáním AI nástrojů. Ne každý ale kontroluje každý kódový output, který generuje.

AI jde stejným směrem, ale ještě tam není. A úkolem AI inženýrů je tu mezeru překlenout. V enterprise prostředí je ta trust gap obrovská. Důležité přitom není jen dokončení jednotlivých features. Často je cennější důvěra, kterou si systém buduje v čase – v outputech, v přesnosti, v responsible use, v privacy a ve všem, co dohromady umožňuje end userům systému důvěřovat.

Agentic delivery přirovnávají k depositu nebo withdrawal do trust accountu u stakeholderů, leadershipu i koncových zákazníků. To, co přežije, není nutně konkrétní feature, ale trust, který se postupně vytvořil, když se věci vyvíjely a měnily.

Proto se ptají: jak budovat trust rychle, záměrně a s evidence? Jednou z odpovědí je progressive autonomy. Mnoho firem vidí agenty jen jako jinou formu tradiční automatizace: něco postavíte, spustíte a hotovo. Jenže agenti se takhle nechovají. Nemůžete předem odhadnout každou jejich odpověď nebo chování a otestovat je všechny.

Zmiňují proto exposure ladder:
- nejdřív **shadow mode**, kdy agent běží vedle lidského procesu, ale nemůže ovlivnit výsledky,
- pak **advisory mode**, kde agent běží live a jen doporučuje, zatímco člověk stále schvaluje nebo zamítá,
- potom **controlled autonomy**, kde agent může spouštět akce v úzkých, nízkorizikových scénářích, s jasnými limity a kill switchem,
- a teprve postupně se autonomie rozšiřuje podle toho, jak roste confidence v požadované chování.

Každý krok je gated by evidence in outcomes, ne podle dokončení aktivit v project plánu nebo pass-fail testů. Klíčové je budovat confidence a trust v reálných výsledcích. Jejich závěr je jednoduchý: engineer for trust, not just for completion.

### 5) Moat v agentickém světě je feedback
Poslední téma je moat. V recursive world, kde AI píše AI, může být cokoli, co vypustíte a co se stane virálním, během minuty zkopírováno. Proto je důležitá otázka: co je unikátní právě pro vás?

Podle Jess a Jacka vás k jednacímu stolu dostane vaše existující enterprise knowledge – CRM, ERP, SOPs. Nazývají to transactional memory. Jenže každý konkurent má nějakou verzi stejné věci. Je to floor, ne fortress.

Skutečný moat je podle nich v momentě, kdy zákazník interaguje s vaším produktem: edge cases, corrections, emotional intent a actual behavior ve vaší konkrétní škále a ve vašem konkrétním kontextu. Tyto signály patří vám. Nazývají je living memory.

Den, kdy něco vypustíte, není finiš, ale moment, kdy začíná závod. Rozhoduje, jak rychle dokážete compoundovat a iterovat, jak rychle umíte převádět signál do hodnoty. Je to race against yourself – stavět vlastní konkurenční výhodu rekurzivně a neustále.

Každá feature, kterou shipnete, má buď generovat feedback signal, nebo vycházet z toho, co vám už feedback ukázal. Pokud nedělá ani jedno, stavíte něco, co může kdokoli zkopírovat. Feedback podle nich není volitelný doplněk. Feedback is the only moat.

---

## Co si z toho odnést
Jess a Jack uzavírají, že enterprise agentic projekty nepadnou kvůli tomu, že AI neumí dost dobře. Padají na tom, že organizace zůstávají uzamčené ve struktuře navržené pro lidskou rychlost, jistotu a lineární řízení. Řešení podle nich stojí na pěti věcech: rychlost, value, delivery, trust a moat.

Doporučení formulují přímo:
- **Start now** a deliver differently.
- Měřit v terms of confidence.
- Stavět projekt kolem hypotheses, ne around requirements.
- Běhat delivery v malých smyčkách experimentation, iteration a evaluation.
- Udělat z financí transformačního partnera, ne jen gatekeepera.
- Přenést governance speed mezi top engineering problémy CTO.
- A pro CEO platí, že moat není v tom, co držíte ze včerejška, ale v tom, co se každý den učíte a kumulujete.

Technologie se bude dál zrychlovat. Přežijí ti, kdo nebudou jen prvními adoptery, ale hlavně ti, kdo se naučí učit. Ti, kdo budou budovat living memory přes feedback loops, a ti, kdo dokážou kultivovat trust u lidí i zákazníků. To se nedá koupit ani okopírovat. Dá se to jen začít budovat hned a nikdy nepovažovat cestu za hotovou.

---

## Zmíněné odkazy a zdroje
- YouTube video: https://youtu.be/AGkzpxMdPn8?si=MLh1fF4otzqhSF8n
- GitHub statistics: 1 billion commits in 2025, 275 million commits per week, projected 14 billion by end of year
- Příklady zmíněných firem a nástrojů: Octopus, Klarna, Shein, Cursor, Cloud Code, Walmart, Temu, JP Morgan