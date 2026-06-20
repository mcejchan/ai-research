# The Agent Development Lifecycle: Build, Test, Deploy, Monitor | Interrupt 26
**Kanál:** LangChain  
**URL:** https://youtu.be/jWy39wavbjY?si=0Qr9h9xHxDCozPG8

## Úvod
[Úvodní video o „intelligence“, které běží před začátkem rozhovoru, staví do kontrastu inteligenci a schopnost jednat: „If it can't act, what does it do? It waits for us.“ Pak se mluví o tom, že je potřeba dát modelům dovednosti, nástroje, paměť a harness, aby mohly plánovat, jednat, učit se, být testované, nasazované a znovu opravované. Následuje přivítání Harrisona, co-foundera a CEO LangChain, a krátký kontext k akci Interrupt 26.]

Harrison říká, že video před začátkem nečekal, ale líbilo se mu. Zároveň přivítal publikum na druhém ročníku Interruptu, který se letos rozšířil na dva dny. Říká, že letošní program je nabitý a že je nadšený, že se všichni připojili. Loni začali rozhovorem o tom, jak je stavění agentů těžké: prototyp jde vytvořit snadno, ale dostat agenta do produkce je složité. Za poslední rok ale mnoho firem, včetně těch, které dnes na akci vystupují, našlo způsoby, jak tyto překážky překonat.

Hlavní myšlenka úvodu je, že budování agentů je jiné než běžný software. Důvodem jsou podle Harrisona hlavně dva faktory: vstupy a výstupy. Agenti pracují s přirozeným jazykem, který může mít nekonečné množství podob, a dnes už i s obrázky, videem nebo audiem. Stejně velký je i výstupní prostor. LLM jsou navíc nedeterministické a citlivé i na malé změny promptu. Proto je těžké předem předpovědět, jak si agent povede, než ho pustíte k uživatelům.

## Build: od LangChainu k Deep Agents
Harrison popisuje, že týmy, které dokázaly nasadit agenty spolehlivě, obvykle dělají dvě věci: shipují brzy a iterují rychle. Z toho se podle něj postupně vyvinul nový „agent development lifecycle“, paralelní ke klasickému software development lifecycle, ale odlišný, protože agenti jsou odlišní. Potřebují víc iterací a i kroky v jednotlivých fázích jsou jiné. Celé to rámuje tak, že LangChain se snaží všechny nástroje přizpůsobit právě tomuto lifecycle a pomoci týmům dostat agenty do reality.

Pak se vrací k historii projektu. LangChain začal jako balíček vydaný měsíc před ChatGPT a původně se zaměřoval na LLM a agentic aplikace. Harrison s úsměvem připomíná, že v LangChainu existovala třída `Agent` ještě před startem ChatGPT. Zmiňuje, že tehdy v San Diegu o svátcích přemýšlel, jak to pojmenovat, a místo `agent` nakonec použil `agent-executor`, což označuje jako příklad jejich slabšího názvu. Později přišel LangGraph, protože aplikace, které lidé stavěli, se z jednoduchých chainů měnily na složitější grafy. Následoval LangChain 1.0 a asi před devíti měsíci Deep Agents.

Harrison vysvětluje základní koncept agenta takto: je to v zásadě LLM běžící v loopu a volající nástroje. Uživatelský požadavek přijde dovnitř, LLM se rozhodne zavolat tool, tool se provede a proces se opakuje, dokud LLM neřekne, že skončilo. To je podle něj jádro toho, co lidé myslí slovem agent.

Deep Agents popisuje jako agent harness, který tento loop „supercharges“ a přidává další baterie-included komponenty. Jednou z nich je execution environment, tedy místo, kde agent běží. Často je to sandbox: dáte mu přístup k file systemu, kódu, čtení a zápisu souborů a možnost vykonávat kód. Na jedné straně spektra je klasický sandbox pro coding agenty, na druhé straně deep agents používá virtuální file system, což je v podstatě databáze vystavená agentovi jako file system. LLM podle něj dobře umí číst a zapisovat soubory, takže je možné ho „oklamat“ a nechat ho fungovat v jakémsi mock execution environmentu. Hlavní pointa je ale stejná: dát agentovi prostředí, se kterým může pracovat.

## Deep Agents 0.6: open models, execution environment, streaming
Harrison pak přechází k tomu, že Deep Agents obsahují i hodně zabudovaného context managementu. Jako příklady uvádí skills a memory, dále summarization jako krátkodobou paměť, když je konverzace moc dlouhá, context offloading pro velmi dlouhé tool cally a prompt caching, aby se počáteční část requestu cacheovala a v budoucnu byla rychlejší a levnější. Všechno tohle je podle něj součást harnessu a funguje automaticky.

Důležitá je i steering. Deep agents jsou dlouhohorizontoví, ale neznamená to, že jsou plně autonomní. Člověk má být pořád v loopu, a proto Deep Agents přichází s dobrými human-in-the-loop controls. Další důležitý prvek je delegation: agent harness může spouštět jiné agenty, plánovací agenty nebo subagenty pro specifické úkoly a řešit jejich komunikaci zpět.

Harrison říká, že tým LangChainu věnuje hodně času výzkumu i applied AI práci, aby například summarization nebo subagents fungovaly co nejlépe. Následně oznamuje Deep Agents 0.6 a tři velké změny, které odpovídají třem trendům v oboru.

První trend je vzestup open modelů. Zmiňuje DeepSeek V4, který podle něj vyšel minulý týden a na některých úlohách je stejně výkonný jako frontier modely. Současně rostou i náklady na frontier modely a usage. Proto chce Deep Agents 0.6 být co nejlepší místo pro použití open source modelů. Nově podporuje GLM5, DeepSeek a Nemotron modely, má integrace s inference partnery jako Fireworks, Base10 a NVIDIA, a jako open source příklad pro coding agenta nad deep agents přidává deep agents code.

Druhý trend je rostoucí význam execution environmentu. Harrison vrací pozornost k virtuálnímu file systemu na jednom konci spektra a plnohodnotnému code sandboxu na druhém. Co je ale mezi tím? V Deep Agents 0.6 přichází CodeInterpreter. Používá QuickJS, JavaScript runtime, a umožňuje agentovi psát a vykonávat kód v něco jako REPL-like prostředí. Není to plný sandbox, nelze v něm dělat všechno jako v Dockeru, ale lze programově volat tooly, manipulovat s datovými soubory a číst i zapisovat do file systemu. Harrison zdůrazňuje, že je to lehké na deployment a není potřeba spouštět separátní sandbox pro každého agenta.

Třetí trend je potřeba dělat dobrá UI. Agenti jsou složitější a eventy, které emitují, jsou také složitější: text, tool cally, obrázky, reasoning, subagenti. Proto Harrison říká, že chtějí co nejvíc usnadnit napojení agent harnessů na „delightful UIs“. Deep Agents 0.6 proto přidává lepší support pro streaming, nový streaming protocol, čtyři front-end SDK pro různé front-end jazyky a integrace s UI frameworky jako Co-PilotKit, Assistant UI a Vercel.

## Test: evaluace a měření
Další část je testování. Harrison říká, že poté, co agenta postavíte, je potřeba zjistit, jestli opravdu funguje. Tady přichází LangSmith evaluations, na kterých tým pracuje už dva roky. Testování agentů je podle něj jiné než testování klasického softwaru: je potřeba vytvářet datasety s referenčními vstupy a výstupy nebo s kritérii, podle kterých se výkon posuzuje. Pak je potřeba definovat metriky, například correctness nebo hallucinations, a spouštět agenta nad těmito datasety, skórovat výsledky a vytvářet experimenty. Ty se pak dají použít k hill climbing nebo k tomu, aby se zabránilo regresím při změnách.

Harrison říká, že evaluace jsou klíčovou součástí LangSmithu, a že k nim budou ještě další novinky později. Tím přechází dál k deploymentu.

## Deploy: do produkce a LangSmith sandboxes
Když je agent hotový a běží lokálně, další krok je produkce. Harrison popisuje, že se objeví mnoho nových výzev. Z jednoho uživatele se najednou stává mnoho uživatelů, environment variables a memory musí být specifické pro jednotlivé uživatele, je potřeba řídit přístup a nedovolit, aby se vše otevřelo každému. Navíc lokální běh je jen test; v produkci musí být systém durabilní a zvládnout škálování.

Aby tohle řešil, před rokem vznikl LangSmith deployments. Harrison zmiňuje, že obsahuje zhruba 30 API endpointů pro streaming, human-in-the-loop, auth a další věci. Jde o jednotný deployment pattern. Podle něj už přes něj běží více než 100 milionů agent runů a důvěřují mu firmy jako Workday, Cisco, Etsy, Podium a ByteDance.

Současně ale říká, že deployments samotné nestačí. Potřebný je také execution environment, a jedním z nejlepších je sandbox. I když agent není čistě coding agent, schopnost číst a zapisovat kód může být pro něj velmi užitečná: může manipulovat s daty, používat CLI a podobně. Proto oznamují, že LangSmith sandboxes jsou obecně dostupné. Publikum tleská.

Sandboxy lze podle něj spustit za méně než sekundu, mají persistenci, takže přežijí mezi interakcemi, a podporují snapshots i forks. Jednou z nejzajímavějších novinek je off proxy. Harrison vysvětluje, že když chcete dát LLM nebo agentovi přístup ke službě přes API key, nechcete, aby ten klíč přímo viděl, protože by mohl být prompt-injected a uniknout. Off proxy sedí mimo sandbox, zachytává traffic a klíče vkládá za běhu. Všechno je součástí LangSmith SDK a je to framework agnostic. Dá se to použít s deep agents, bez deep agents, pro testování, RL i pro produkční agenty.

Jako konkrétní příklad uvádí Monday, které sandboxy používá pro AI assistant sidekick. Říká také, že zpětná vazba od prvních zákazníků je velmi pozitivní.

## Context Hub: prompty, skills a memory
Další velké téma je context. Harrison říká, že LLM sama o sobě nic moc neví a lidé taky nevědí všechno, takže když něco potřebujeme, jdeme do knihovny nebo si čteme knihy. Přesně to podle něj dělají i agenti — jen místo knih používají context. Ten se postupně vyvíjí: dlouho měl LangSmith prompt hub pro ukládání promptů, ale v posledních měsících se kontext pro agenty posunul od promptů k agent.md souborům a skills, tedy velmi detailním instrukcím a schopnostem.

Z toho vychází nový LangSmith Context Hub. Harrison vysvětluje, že do něj lze ukládat agent.md soubory, skills i LLM wikis, tedy kondenzované znalosti v markdown souborech, které podle něj dělá stále více lidí. Context Hub nabídne versioning, tagy a komentáře. Kontext pak lze stáhnout lokálně, použít v coding CLI, v deep agents jako virtual file system nebo v jakémkoli jiném agent harnessu.

Současně dodává, že Context Hub je podle nich první krok k memory. Memory je pro budoucnost agentů extrémně důležitá a agent.md a skills už lze chápat jako ranou formu paměti. Harrison zdůrazňuje, že jde o open standardy, a tedy že i memory by měla být otevřená, ne uzamčená v jednom LLM, frameworku nebo platformě. Proto LangChain spolupracuje s Redis, Elastic, Mongo a Pinecone na tom, aby se tato první verze memory proměnila v otevřený standard pro agenty.

## Monitor: observability, governance a LLM Gateway
Na závěr Harrison přechází k monitoringu. Když je agent nasazený, je potřeba vědět, co vlastně dělá. Tady přichází tracing: je možné vidět každý krok agenta, vstupy i výstupy. K tomu slouží dashboardy pro sledování costu a latency v čase, online evals, kde lze použít LLM jako judge nebo kód nad tracey, získat feedback a připojit ho zpět, případně sbírat user feedback. To vše patří do LangSmith Observability.

Pak Harrison říká, že po nasazení a provozu ve větším měřítku vyvstává i otázka governance. Když má agent běžet pro 10 nebo 100 různých use caseů, je potřeba řešit škálování, cost efficiency a security. Dvě největší obavy jsou podle něj cost a data exposure. LLM jsou drahá, takže je potřeba vědět, kolik agenti utrácejí, kolik utrácí jednotliví uživatelé, a vyhnout se překvapivým účtům. Zároveň LLM sice umějí pracovat s daty, ale neměly by mít přístup ke všem zdrojům dat. Proto oznamují LangSmith LLM Gateway v beta verzi.

LLM Gateway sedí mezi agenty a jejich LLM calls. Umožňuje nastavit spend limits, mít plnou viditelnost nad spendem a také nastavovat guardrails pro PII a secret detection. Integruje se s řadou coding agentů, protože právě ty jsou dnes podle Harrisona nejpopulárnější a zároveň často generují největší náklady. Gateway funguje se všemi LLM providery, ke kterým umí LangChain přistupovat, a vše se automaticky traceuje do LangSmith.

## Manage Deep Agents
Na konci Harrison říká, že tohle je celý agent development lifecycle: build, test, deploy, monitor. Připouští, že je toho hodně a že přechod od agenta k produkci znamená mnoho dílčích částí. Proto chtějí celý proces co nejvíc zjednodušit.

Aby všechno bylo v jedné API vrstvě, oznamuje v private preview novinku Manage Deep Agents. Tato služba je single API pro práci se všemi komponentami. Pod kapotou běží deep agent harness, deployment je přes LangSmith deployments, modely mohou být jakékoli — Harrison zmiňuje OpenAI, Anthropic i open source providery jako Fireworks a Base10. Instrukce a memory jsou uložené v Context Hub, kde lze sledovat změny, versionovat je a spravovat. Agent má oddělený deployment a oddělený sandbox pro běh nástrojů, a sandboxy jsou poháněné LangSmith sandboxes.

Pro propojení s nástroji slouží MCPs, které lze přidat přímo, nebo přes partnery jako Arcade. Celý výstup potom streamuje novým streaming protocol, aby šel snadno napojit na Co-PilotKit, Assistant UI a další frameworky. Harrison to uzavírá tím, že LangChain Open Source a LangSmith pohánějí celý agent development lifecycle a že trace je jeho středem.

## Závěr a předání Ankushovi
Harrison říká, že se společnost hodně soustředí na traces a že nikdo ve firmě o nich nepřemýšlí víc než jeho co-founder Ankush. Dodává, že už téměř rok řeší, jak udělat zkušenost kolem trace co nejlepší, protože právě trace pohání celý loop. Pak ho představuje na pódiu: Ankush Gola, co-founder a CTO LangChain.

## Traces, data infrastructure a observability
Ankush začíná tím, že opravdu tráví hodně času přemýšlením o agent traces, protože podle něj jsou trace ve středu agent development lifecycle. Každý trace zachycuje unikátní behaviorální záznam toho, co agent v určitém okamžiku skutečně udělal.

Zároveň říká, že agent traces a obecně agent observability představují zvláštní problém pro data infrastrukturu. Traces jsou velmi hluboce zanořené a mohou obsahovat tisíce až desetitisíce mezikroků. Payloady jsou velké a neomezené. To je podle něj přímý důsledek toho, že agenti běží na delších horizontech a že se zvyšují context windows u LLM. Navíc roste počet traceů, které obsahují modality jako obrázky a voice. Hlas je podle něj obzvlášť populární například v customer support aplikacích. K tomu se přidávají i složité query patterns, protože efektivní mining traceů pro useful insights vyžaduje specifické a komplexní dotazy.

Ankush zdůrazňuje, že agent traces nejsou jen bohatší, ale rostou i objemově, protože agenti se stávají všudypřítomnějšími. Ukazuje údaj od jednoho reálného zákazníka LangSmithu, kde weekly trace volume postupně rostl: v rané fázi testování a vývoje byly objemy malé, ale jakmile se agent dostal do produkce a přibyli další agenti, týdenní objem překročil 150 milionů. Poukazuje na to, že payloads jsou large, a tím je rozjezd observability ještě náročnější.

## Zmíněné odkazy a zdroje
- LangChain: https://www.langchain.com
- LangGraph
- LangChain 1.0
- Deep Agents
- Deep Agents 0.6
- Deep Agents Code
- LangSmith
- LangSmith Evaluations
- LangSmith Deployments
- LangSmith Sandboxes
- LangSmith Context Hub
- LangSmith Observability
- LangSmith LLM Gateway
- Co-PilotKit
- Assistant UI
- Vercel
- QuickJS
- Fireworks
- Base10
- NVIDIA
- OpenAI
- Anthropic
- Redis
- Elastic
- Mongo
- Pinecone
- Arcade
- MCP / Model Context Protocol