# Don't Ship Skills Without Evals — Philipp Schmid, Google DeepMind  
**Kanál:** AI Engineer  
**URL:** https://youtu.be/0vphxNt4wyk?si=nK8XmI-CcySIALwr

## Úvod

Philip Schmid říká, že je z Německa a pracuje v týmu Google DeepMind, hlavně na Gemini API a agentech. Tématem rozhovoru je, proč by se skills neměly nasazovat bez evalů. Hned na začátku se ptá publika, kdo používá coding agenty k psaní kódu, kdo s nimi používá skills a kdo má pro tyto skills evaly. Pointa je okamžitá: skills používá skoro každý, ale evaly má jen málokdo.

Philip upozorňuje, že v produkci velmi záleží na tom, proč checks selhávají. Zmiňuje také Skill Bench, velmi populární benchmark, který indexuje přes 50 000 skills z internetu, a téměř žádné z nich neměly evaly. Většina byla AI-generated, nebyla pořádně testovaná a je těžké poznat, zda je skill dobrý nebo špatný, protože agenti jsou nedeterminističtí. Člověk pak neví, jestli task selhal kvůli špatnému skillu, nebo protože je problém prostě příliš těžký pro model.

## Agenti, které používáme, a agenti, které stavíme

Philip zdůrazňuje důležitý rozdíl mezi agenty, které sami používáme, a agenty, které budujeme pro uživatele. Většina z nás používá agenty na psaní kódu nebo produktivní práci — například Anti-Gravity, Cursor nebo Claude Code. V takovém případě je člověk inženýr, má kontext o skills a velmi rychle pozná, když agent skill nepoužije správně. Stačí task zastavit a znovu jej zadat, případně použít slash command pro spuštění daného skillu.

Když ale stavíte agenta uvnitř aplikace pro zákazníky, situace je úplně jiná. Uživatelé nemají tušení, co je skill, a nezačínají svůj prompt stylem „use customer support skill“ nebo „use refund skill“. Proto je mezi agenty, které používáme my sami, a agenty, které stavíme pro zákazníky, zásadní rozdíl v tom, jak se skills objevují a používají v kontextu.

## Co je skill a jak funguje

Philip shrnuje, že skill je v praxi složka s `skills.md` souborem a dalšími assets, které pomáhají modelu skill skutečně používat. Hlavní princip je progressive disclosure. Nejprve je tu title a description, které jsou součástí kontextu modelu a model díky nim pozná, kdy skill použít. Druhá vrstva je samotný `skills.md` s dalšími instrukcemi, detaily a odkazy na externí soubory. A pak existuje třetí vrstva — reference files, kde je veškerý detail, který model potřebuje, aby úlohu zvládl.

Rozlišuje dva typy skills: capability skills a preference skills. Capability skills učí model něco, co zatím nedokáže dělat spolehlivě, například tracing logů nebo vytvoření nového React appu. Tyto skills jsou dočasné; jakmile se model zlepší, měly by se odstranit, a evaly ukážou kdy. Preference skills jsou naproti tomu trvalejší a často zachycují specifické workflow, styl, jazyk nebo firemní preference. Právě tyto skills bývají velmi cenné, protože foundation models často neznají doménově specifické znalosti a nechcete, aby update agenta degradoval výkon.

Philip také říká, že skills skutečně fungují. Odkazuje na Skills Bench 1.1, který ukázal, že skills zlepšují výkon v průměru asi o 15 %. Skills Bench pokrývá zhruba 100 různých úloh z oblasti kódování i produktivity napříč jazyky, je veřejně dostupný, má leaderboard a je otevřený komunitním příspěvkům. Další analýza ukázala, že human-written skills jsou nejlepší, zatímco AI-generated skills mohou výkon dokonce zhoršovat. Zmiňuje také, že `skills.md` soubory by měly být pod 500 řádků; pokud má někdo skill delší, měl by ho po session určitě projít.

## Model-invoked a user-invoked skills

Další důležité rozdělení je mezi model-triggered skills a user-invoked skills. Model-triggered skill se spustí podle kontextu a popisu, kdy se model sám rozhodne skill přečíst nebo použít, aby získal další kontext pro řešení úlohy. Philip upozorňuje, že lidé často podceňují, jak silné user-invoked skills jsou. U workflow typů úloh, jako je vytváření pull requestu, staging dokumentace nebo běžná dev práce, která by klidně šla přes skript, je často lepší použít user-invoked skill.

Když ale stavíte agenty pro zákazníky, user-invoked skills nemáte. Zůstává jen model-invoked varianta, a právě na tu se zaměřuje i praktická část o evalech.

## Jak psát dobré skills

Philip pak přechází k doporučením, jak psát dobré skills. Nejvíc záleží na description, protože to jsou většinou jen dvě věty, které se dostanou do system instruction a mají modelu napovědět, kdy skill použít a kdy ne. Pokud je description příliš slabé, skill se buď bude spouštět moc často, nebo naopak vůbec ne.

Je důležité vysvětlit modelu proč by měl skill použít a jak ho má použít. Častý styl je například: „Use that skill if you are working on a React application.“ Philip zdůrazňuje, že je lepší psát directives než eseje. Místo vágního vysvětlování je potřeba dát modelu jasný pokyn: pokud děláš chat aplikaci, použij Interactions API.

Stejně tak je důležité udržet skill lean a vrstvit informace. Description je náklad, který platíte při každém model callu, protože je součástí contextu. Dlouhý `skills.md` se zase načítá do kontextu ve chvíli, kdy se model rozhodne skill použít, a to může být drahé. Proto je potřeba být co nejstručnější, ale stále zachovat všechny reference a detaily. Pro opravdu specifické věci, jako deployment do AWS, Google Cloud nebo Azure v multi-cloud prostředí, nepatří instrukce přímo do hlavního `skills.md`, ale do samostatných reference files.

## Správná míra svobody a negativní případy

Philip se také věnuje tomu, jakou míru svobody modelu ponechat. Mnoho lidí popisuje workflow přesně krok za krokem: step one, step two, step three. Pokud je proces vždy stejný, neměli byste vlastně používat skill, ale skript. Nechcete plýtvat modelem a tokeny na něco, co je deterministické. Lepší je definovat cíle a constraints a nechat model pracovat v rámci těchto hranic.

Podobně je potřeba nezapomínat na negativní případy. Všichni si všímají toho, kdy skill chceme použít, ale málo kdo zkoumá, kdy skill použít nechceme. Pokud skill popisujete jako něco pro web development, může se přehnaně triggerovat třeba i u Angularu, Reactu i dalších frameworků. Když ale řeknete, že je skill jen pro React components nebo Tailwind CSS, model lépe pozná, kdy je vhodný. Evals pak pomáhají tyto případy odhalit.

## Testování dřív, než skill nasadíte

Philip říká, že je potřeba testovat hned při vytváření nového skillu. Doporučuje vytvořit 10 až 20 promptů. Sám si dělá pět promptů pro happy path a pět promptů tam, kde skill nechce použít, aby viděl, jestli se model netriggeruje příliš často a nezačne se sám plést. Pokud už existují customer nebo production traces, je dobré je do testování zahrnout, protože nic není lepší než reálná data.

Pak zmiňuje tip, který připisuje Mattovi. Matt publikoval tweet i skill zaměřený na odstranění no-ops. AI-generated skills prý často obsahují spoustu no-op instrukcí, tedy instrukcí, které ve skutečnosti nic nemění na chování agenta. Příklad je věta typu „before making an implementation easy to read“, což model stejně už ví. Je tedy dobré tyto no-ops identifikovat a odstranit.

Nakonec zdůrazňuje, že je potřeba vědět, kdy skill retireovat. Skills nemají žít navždy. Modely se zlepšují, chování se mění, očekávání se mění a mění se i prostředí. Proto je důležité spouštět evaly s insertem i bez něj. Pokud model dosahuje stejného výkonu i bez skillu, je čas skill odstranit, ušetřit tokeny a omezit redundanci.

## Praktický příklad: Gemini Interactions API

Philip pak ukazuje konkrétní příklad. Začátkem roku tým chtěl vytvořit nový skill pro Gemini Interactions API, což je nová interface pro práci s Gemini modely a agenty. Protože Interactions API bylo vydané až po posledním tréninku Gemini, model neměl o této API žádný kontext. Proto vznikla potřeba skillu, který modelu pomůže generovat správný kód pro Interactions API a používat nejnovější modely.

Pro testování vytvořili 117 test cases. Ty vycházely z reálných dat od uživatelů, kteří se pokoušeli generovat Gemini code, ze synteticky generovaných testů i z feedbacku, například když model používal Gemini 2.0 i ve chvíli, kdy už bylo vhodné používat 3.0. Výsledek byl, že se výkon zlepšil až téměř na 90 % pro generování validního kódu pro Interactions API s nejnovějšími Gemini modely.

K tomu potřebovali jen dva jednoduché assets. Prvním byl JSON soubor se všemi test cases. Ten obsahoval prompt, tedy to, co očekáváme od uživatele, jazyk, protože testovali TypeScript i Python, dále `should trigger`, které říká, zda má agent skill přečíst, a pak různé expected checks, tedy jednoduché asserts k tomu, zda měl skill triggerovat nebo ne.

Druhým assetem byl jednoduchý Python script, který spustí coding agenta, v tomto případě Gemini CLI, vezme output a vyhodnotí, jestli vznikl validní kód pro Interactions API. Philip říká, že většina skill evalů může být postavená na regex. V jejich případě šlo hlavně o to, zda byl použit správný SDK, správný model, správné metody a zda se nepoužívají staré patterny. Pro to vytvořili jednoduché a levné asserts, které se dají spouštět opakovaně. Když přijde nový model, je snadné upravit asserts na nové model IDs.

Když je problém složitější, lze použít i LLM as a judge, tedy rubric založenou na tom, co má být splněno. Výstup se pošle do LLM judge, který vrátí pass nebo fail, a pokud selže, člověk se podívá na data a skill upraví. Přesně takhle dnes evalují skills i v Google DeepMind.

## Jak vypadají interní evaly v Google DeepMind

Philip říká, že interně u Google DeepMind mají pro každý skill připojené evaly. Nepoužívají YAML jen jako příklad, ale princip je podobný. Každý test má více cases s promptem, běží v izolovaném workspace, kde lze definovat prostředí i přídavné soubory, například application environments. Dále existují startup commands, které předem instalují knihovny nebo připraví prostředí.

Pak jsou tu script evals nebo data, což jsou právě regex a další jednoduché kontroly nad trace, například zda skill triggeroval nebo zda byl spuštěn určitý command či CLI. Kromě toho používají také LLM as a judge, kde jsou očekávání porovnávána s tím, co se skutečně stalo — například jestli se skill aktivoval nebo zda byl spuštěn konkrétní bash command.

Tyto evaly se spouštějí při každé změně skillu. Pokud vznikne diff ve skill file, eval proběhne a výsledek rozhodne, zda se změna může mergnout. Jinými slovy, každý skill má regresní testy pro každou změnu a skill lze změnit jen tehdy, když to zlepšuje test cases nebo přidává nové evaly.

## Deset best practices a závěrečné doporučení

Na závěr Philip shrnuje několik dalších best practices. Znovu zdůrazňuje, že skill description je velmi důležitý a že velká část selhání pochází z toho, že skill nebyl správně triggernutý, protože prompt uživatele nebyl dostatečně detailní. To je obzvlášť důležité, když stavíte agenty pro jiné lidi — ti neznají vaše interní skill descriptions.

Dále opakuje, že je lepší psát direktivy než pasivní informace. Místo neurčitých návodů je potřeba agentovi říct, co má dělat, nebo naopak co dělat nemá. Je důležité zahrnout negative tests, začít v malém a i deset až dvacet eval samples je lepší než nic. Často se vyplatí měřit outcomes, ne jen cesty: netestovat jen to, jestli model načetl skill na první turn, ale jestli skutečně splnil task.

Stejně důležité jsou isolated runs, protože coding agents jsou chytré a umí „podvádět“, pokud běží ve vašem existujícím prostředí s přístupem k předchozím chatům nebo dřívějším executionům. Je dobré spouštět více trialů na case, protože modely jsou nedeterministické a první běh může projít, zatímco druhý ne. Philip doporučuje testovat napříč různými harnesses, protože různé nástroje a různé modely se chovají odlišně. Skill, který funguje dobře s Geminim, může být slabý s Codexem nebo v jiném prostředí.

Ještě jednou zdůrazňuje, že evaly nemají mizet jen proto, že jste skill odstranili. Pokud model už skill nepotřebuje, eval je stále užitečný, protože hlídá, aby výkon neklesl. Když se objeví degradace, můžete skill znovu zavést nebo upravit jiné nástroje a workflow.

## Homework

Na závěr dává Philip domácí úkol: pokud se po víkendu vrátíte do práce, vezměte nejpoužívanější skill a napište pro něj pět test promptů. Je možné použít i coding agenta, aby z trajektorií zjistil, které skills se používají nejvíc, a pomohl navrhnout testy. Vysvětluje, že eval harness je jednoduchý: JSON nebo YAML soubor a malý Python script, který spustí agenta a zkontroluje výsledek.

Doporučuje také odstranit no-ops, protože i když to nemusí změnit eval performance, ušetří to tokeny a tedy peníze. A znovu zdůrazňuje ablation test: vždy spouštět evaly se skill loaded i bez skillu. Jen tak poznáte, kdy skill opravdu pomáhá a kdy už je možné ho retireovat.

Philip uzavírá jasným poselstvím: **do not ship skills without evals**.

## Zmíněné odkazy a zdroje

- YouTube: https://youtu.be/0vphxNt4wyk?si=nK8XmI-CcySIALwr
- Google DeepMind
- Gemini API
- Gemini Interactions API
- Skills Bench
- Claude Code
- Cursor
- Anti-Gravity
- Matt
- GitHub skills repository
