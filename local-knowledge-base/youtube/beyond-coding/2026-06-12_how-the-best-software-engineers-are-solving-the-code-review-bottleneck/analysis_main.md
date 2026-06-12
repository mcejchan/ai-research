## Úvod

„How do you scale the reviewing process? Because now that is blocking your senior engineers.“ „It burns them out.“  
„One answer is don't do any code reviews at all.“

To je Florian Buetow, AI engineer at Xebia, a v tomhle rozhovoru řešíme jeden z největších bottlenecků v softwarovém inženýrství právě teď: code review. Bavíme se o tom, co dělat, když AI generuje víc a víc kódu, jak škálují review procesy velké firmy, proč záleží na harnessu víc než na modelu a jaké guardrails se v praxi ukazují jako nejcennější.

„What do you think of spec driven development? Which of these guardrails gave you the most value? Does it matter which harness I use? GitHub Copilot, Claude Code, Codex.“  
„It matters immensely.“

Florian vysvětluje, že zaměstnanci často dostanou do ruky „hand grenade“ — AI — a pak se po nich chce, aby ji používali, ale nic nevybouchlo. A právě takhle podle něj dnes nejlepší inženýři řeší code review bottleneck.

---

## Proč se code review stává úzkým hrdlem

„As we generate more code, this is really in the build phase code review and becomes a bottleneck.“

Florian říká, že návrat z Google I/O mu znovu potvrdil, že i uvnitř Googlu lidi přiznávají, že code review je bottleneck, ale zatím nevědí, jak ho vyřešit. „Google is an interesting case because in 2025, they already reported that 50% of the code is AI, and then I'm pushing for 75%.“

Podle něj je důležité sledovat velké hráče a dívat se, co skutečně dělají, ne jen jaké číslo reportují. Na jedné straně vidíme velká tvrzení typu „we automated our entire deployment layer with AI“ nebo různé dramatické efficiency gains, ale mnohem méně často je vidět, jak se to dá přenést do vlastní práce. „That part is often missing.“

Florian říká, že ve velkých firmách je vidět posun směrem ke standardizovanějším review procesům. Když je generování kódu levné a rychlé, bottleneck se přesouvá jinam. Někteří lidé sice tvrdí, že psaní kódu nikdy nebyl hlavní bottleneck, ale realita je taková, že se najednou generuje „ten times more code“, a tím roste tlak na review a na inženýry.

Zmiňuje také, že Amazon po některých incidentech, kde došlo k outage a ztrátě revenue kvůli AI generovanému kódu, zavedl policy, podle kterých se určité části kódu nebo systémů musejí před mergem nebo deployem reviewovat senior inženýry. „They are identifying that, you know, in some cases, AI generated code has to be scrutinized stronger than in other cases.“

---

## Horizontální a vertikální škálování AI engineeringu

Florian rozlišuje dva směry škálování. „There is a horizontal way of scaling AI engineering, and the vertical one.“

Horizontální přístup znamená automatizovat existující procesy. Například PR review: vytvořený PR se automaticky pošle do Copilotu nebo jiného nástroje k review. Hodně firem tohle dělá, ale podle něj často neřeší, jak to skutečně zlepšuje kvalitu.

Vertikální směr je jiný. Tady máš projekt a malý specializovaný tým, který si sám buduje tooling a prostředí, aby produkt shipoval tak, jak má. Neexistuje jedna blueprint šablona, která by automaticky seděla na celý produkt; místo toho se prostředí i pravidla dolaďují podle konkrétního systému. „They refine it.“

Když se mluví o agentech, není to jen o modelu. Je to celé vrstvení schopností: model, pak harness kolem modelu a pak prostředí, ve kterém ten harness běží. A právě to prostředí je podle něj klíčové.

---

## Jak škálovat review proces bez přetížení seniorů

Florian se vrací k tomu, jak software engineering fungoval dřív. V klasickém SDLC byl review částečně lidský, protože code nebyl dodáván rychleji, než se dal zkontrolovat. To se změnilo.

„Now the question becomes, well, how do you scale the reviewing process?“

Senior inženýři jsou tím dnes blokovaní a přetěžovaní. Florian zmiňuje studie o rostoucí cognitive debt, o tom, že lidé často nechápou vlastní codebase, protože nemají čas si všechno projít, nebo se jim ani nechce dívat na AI generovaný kód.

Jeden možný přístup je podle něj nedělat code review vůbec. Ale pak je nutné přesně řešit, jak to celé funguje. Jeho odpověď je: navrhnout prostředí, ve kterém agent pracuje, tak, aby nepotřeboval lidskou zpětnou vazbu na běžné věci.

Začíná to jednoduchými věcmi: formátování, security checks, nástroje typu SonarQube a další automatické feedback systémy. V minulosti to dělal člověk ručně, teď to mohou dělat agenti sami. Důležité je, aby feedback přišel co nejblíž místu, kde agent kód skutečně generuje — ideálně na developerově laptopu, ne až v GitHubu po commitu nebo PR. „Then you're suddenly in this world of where you're trying to engineer feedback to the agents in a way that helps the agents to run for a long time without human intervention.“

„I think it's very easy to get started with it. A lot of it will feel like, but we've been doing this before, but now you're giving the agent that feedback. You're not taking it as a human anymore.“

---

## Harness je důležitější než model

Na otázku, jestli záleží na tom, jestli používáš GitHub Copilot, Claude Code nebo Codex, Florian odpovídá bez váhání: „Absolutely. Well, in my experience, the harness matters more than the model.“

Harness je podle něj to, co poskytuje nástroje, prompting, memory layer a další části, které se pak posílají do modelu. Když model potřebuje udělat tool call, harness je ten, kdo mu poskytne možnost nástroj spustit. „It matters immensely.“

Vypráví o experimentu na jednom projektu, kde zkoušel implementaci podle specifikací a testů. Nejprve se snažil udělat full suite specifications — čisté specification driven development. Myšlenka byla, že když produkt specifikuješ dost přesně, model ho implementuje přesně podle specifikace. „Which is unfortunately not true.“

Pak zkusil TDD přístup: dopředu vygenerovat paralelní testy a použít je jako feedback pro agenta, který má specifikaci následovat. A výsledek? Záleželo na harnessu. „Depending on the harness that I used, it worked or didn't work. Even if I was using the top frontier model in both harnesses.“

Na tehdejší době mu nejlépe vyšel Claude Code. Později by řekl, že se to přesunulo směrem ke Codexu pro implementační práci. Ale zároveň zdůrazňuje, že je to moving target. „You can't really stop experimenting.“

Florian varuje před tendencí software inženýrů všechno zprocesovat a uzavřít do pravidel typu „musíme používat jenom tenhle tool“. Modely se rychle mění, mají různé „personalities“ — některé jsou lepší v instruction following, jiné v doplňování mezer, když člověk nedá dost kontextu. Proto je potřeba být opatrný nejen při výběru harnessu, ale i modelu.

---

## Spec driven development, TDD a feedback loop

Na doplňující otázku, co mu fungovalo víc — spec driven development, nebo TDD s feedbackem — Florian říká, že první pokus s dobře napsanou specifikací nevyšel. „It was the typical okay, I create the perfect prompt and then the model does something different I didn't intend.“

Když ale přidal feedback mechanismus, který modelu řekne, kde je off track, fungovalo to lépe. Znovu ale připomíná, že výsledky nejsou nutně přenosné na každý projekt. „It really depends on the project.“

Pak popisuje, jak v CLI nástrojích fungují stop hooks. Agent dokončí práci, harness spustí event, který je možné napojit na shell script. Ten může automaticky spouštět test suite nebo guardrails. „So you can automate running your test suite or your guardrails.“

Florian říká, že guardrails je třeba navrhnout tak, aby vracely zpětnou vazbu v přirozeném jazyce: „This is forbidden. Do it in this way.“ Tím se k modelu vrací stejný typ instrukce, jakou by psal člověk. A následně to spustí další iteraci modelu.

Zmiňuje také „roof loop“ a nové příkazy typu goal v Codexu a Claude Code, které umožňují nechat systém běžet dlouho, dokud se problém neopraví. „The idea is the same.“

---

## Guardrails, které dávají největší hodnotu

Na otázku, které guardrails mu přinesly největší hodnotu, Florian říká, že se stal velkým fanouškem semantic grep. „Because it allows you to put regex for things that it could catch and code.“

Uvádí příklad, že nechce žádné default values v metodách v Pythonu. Default parametry jsou podle jeho zkušenosti jeden z největších zdrojů frustrace při pozdějším review a debugování. Proto je lepší mít pravidlo, které tenhle pattern detekuje a vyhodí error: „You must not write it in that way. It's against policy.“

Semantic grep je podle něj velmi flexibilní. Kdykoli se AI na napsaný kód „ptá“ a objeví se otázka „Why did you do it that way? It doesn't make any sense“, je to signál přidat další guardrail. „So what then happens over time is you're shaping your environment, you're iterating towards it to be tighter and tighter.“

Cílem je přiblížit prostředí tomu, co jako člověk považuješ za správné. Nejde jen o „taste“, ale i o to, aby AI generovala kód, který je snadno pochopitelný nejen pro lidi, ale i pro další AI. „Write code is context.“ Když se kód napíše bez disciplíny, dřív nebo později se v něm začne AI sama plést.

---

## Modularita, architektura a architecture unit tests

Florian zdůrazňuje, že udržitelnost codebase se nezměnila: kód má být jednoduchý a snadno měnitelný. S agenty si ale dovolujeme generovat víc kódu a část z něj nemusí být jednoduchá, jenže pak na to často mávneme rukou: „Well, it works, right?“

Podobně jako lidé tolerují, že některý modul je uvnitř trochu messy, pokud je izolovaný za abstrakcí. „As long as it's modular, it doesn't matter.“

Právě modularita mu u AI velmi pomáhá: jasné hranice mezi moduly, dobře definovaná rozhraní, která se nesmí měnit. A tady přichází další typ guardrailů — architektonická omezení. Některé jazyky nebo nástroje umí architecture unit tests, které rychle kontrolují závislosti mezi moduly. Například lze zakázat, aby UI přistupovalo přímo k databázi, a vynutit průchod přes business logic layer.

AI podle něj vytváří podivné interconnection patterns, které by člověk nikdy nenavrhl. Když necháš AI navrhnout systém a pak si necháš vykreslit diagram, můžeš vidět „the weirdest things“. A právě tyto bizarní vazby pak přeložíš do dalších architecture unit tests.

---

## Co zůstává lidskou odpovědností

Na otázku, co už podle něj nejde plně automatizovat, Florian říká, že klasická softwarová práce pořád začíná tím samým: „What do we want to build? How do we build it? How do we keep it maintainable?“

Architektura by měla stále vzniknout dopředu. Nejprve je třeba přesně pochopit, co se má stavět, a pak si nakreslit, jak software systém vypadá: služby, moduly, funkce, vzájemné vazby. „You specify pretty much the entire architecture except the implementation.“

A až potom je možné tu architekturu přepsat do pravidel. Tohle je podle něj zásadní i kvůli cognitive dissonance, která vzniká, když už člověk nerozumí vlastní codebase a neumí o ní jako člověk přemýšlet. Ten problém nevzniká jen na úrovni kódu, ale hlavně na úrovni architektury a vztahů mezi komponentami.

„You need to do everything to combat that as much as possible.“

Florian zároveň říká, že je pro něj těžké představit si, kam to celé půjde dál, protože souhlasí s tím, že implementace je už teď postupně automatizovaná. S dostatkem guardrails se dá code review zúžit jen na podstatu, případně na behavior, a část lidí už dnes reviewuje i specifikace. Ale když si představí juniora v organizaci, která vlastní systém dobře nezná, je těžké určit, co je potřeba pochopit dopředu a kolik investigace má proběhnout předem. To, co dřív vznikalo za pochodu, se teď přesouvá do upfront práce.

„It’s very, very, very difficult to be messy in your approach now.“

---

## Nový způsob práce, prototyping a role juniorů

Florian připouští, že to může být jeden z důvodů, proč někteří lidé novému způsobu práce resistují. Dřív se věci objevovaly za pochodu a bylo možné iterovat postupně, teď je často potřeba udělat velkou část práce dopředu. „You probably have to do a couple of iterations on your implementation to get a better idea of how good actually looks like.“

To ale neznamená, že se to nedá dělat s vibe codingem. „That is going to be the new normal for some time to come before things change again.“

Zároveň tvrdí, že ve skutečnosti děláš pořád stejnou práci — jen jí děláš dřív. A když se někdo ptá, co mají dělat junior inženýři, když AI generuje kód, odpověď je podle něj jasná: tohle se dá naučit a je to obrovská dovednost.

Vypráví, že nejlepší software inženýři, které viděl, se dělili na dva typy. Jedni si předem sedli s tužkou a papírem a kreslili si věci ještě před psaním kódu. Druzí museli hned psát, protože si neuměli dobře představit řešení v hlavě, ale byli přesto extrémně efektivní. Oba typy fungují jinak, ale fungují.

A právě AI podle něj umožňuje tu první fázi ještě víc rozvinout. „If you allow yourself to do that, to do the prototyping, to go in this discovery before you put your specifications not into stone, but before you kind of say, okay, this is what we want to build, it's incredibly rewarding.“

Florian říká, že často tráví hodinu rozhovorem s AI jen proto, aby prozkoumal jednu ideu, pak jinou odbočku, a i když třeba odbočil špatně, naučí ho to přemýšlet o systémech. Současně ho to posouvá na produktovou úroveň: neřeší už jen implementaci, ale i to, co je vlastně skutečně potřeba a co potřebuje zákazník.

„Engineers get much more elevated. They start to think at that product level much more now because of that.“

---

## Únava, context switching a práce s agentními systémy

Na otázku, jaké to je pracovat paralelně s více AI úlohami, Florian říká, že to umí být vyčerpávající. „The burnout, because you're constantly exposed to stimuli and you're constantly context switching.“

Zmiňuje, že AI potřebuje třeba 20 minut na odpověď, a mezitím člověk pořád reaguje. Popisuje výrok jednoho developera, že ve středu je jeho mozek celý den jen „on standby“. To považuje za 100% reálné.

Jako protiopatření doporučuje disciplínu. První krok je být si vědom toho, co člověk dělá. Pak se dá učit tasky různě prokládat. Například jedna práce je na prostředí, které vede agenta, a druhá je samotný produkt. Mezi nimi může člověk přepínat, ale zůstává v podobném kontextu, místo aby skákal mezi nesouvisejícími projekty.

Když to nedělá, musí se pak v session ptát: „Please tell me, what did we do in the last half hour?“ Jen aby mu AI připomněla, co vlastně dělal. „It’s weird sometimes.“

Zmiňuje, že Claude Code už podobnou UX věc dělá automaticky: když jsi dlouho mimo session, nabídne summary toho, co se dělo, aby ses nemusel ptát.

---

## Cognitive debt, odpovědnost a „hand grenade“ AI

Rozhovor se pak vrací k tématu ownership. Podle Floiana bude cognitive debt a to, kdo za co nese odpovědnost, zásadní téma. Zmiňuje i pojem cognitive surrender — stav, kdy člověk nechá agenta, aby převzal řízení, a když se něco pokazí, je to chyba agenta; když to funguje, je to taky agent. On sám ale nechce úplně pustit vlastní odpovědnost.

„That’s quite risky.“

Podle něj jsou právě tyto debaty důležité, protože dávají lidem perspektivu, co zmizí a co zůstane jako jejich accountability. „Basically what employees are doing is they give people a hand grenade, which is AI, and then say, don't blow up the hand grenade, but use it.“

AI rizika podle něj nezmizí, ale časem se zstandardizují. Budou vznikat pravidla, co je s AI povolené a co ne. Stejně jako už dnes Amazon rozlišuje kritické části kódu a míru review, do budoucna se podobná pravidla stanou běžnou součástí procesu. „If you just want to YOLO it, okay, let's not touch the billing system, please.“

A současně i to, co lidé nechtějí dělat ručně, může být outsourcované na AI. I myšlenka „nedělat žádné code reviews“ je sice záměrně provokativní, ale podle něj vede k důležitým zjištěním: jsou tu cheap wins v podobě deterministic guardrails, pak přichází diskuse o architektuře, o specifikacích a o validaci specifikací předem. A i když člověk později reviewuje architekturu, může si na to vzít AI.

---

## Zmíněné odkazy a zdroje

- Beyond Coding
- Google I/O
- Google
- Amazon
- Spotify
- GitHub Copilot
- Claude Code
- Codex
- SonarQube
- semantic grep
- TDD
- spec driven development
- CLI tools
- stop hooks
- roof loop / loop
- goal command