## Úvod
V rozhovoru se řeší hlavně agentic engineering workflow, práce s modely, skills a to, co Matt Pocock považuje za skutečnou výhodu při používání AI. Hned na začátku zdůrazňuje, že většina lidí se upíná na samotný model, ale mnohem důležitější je harness: tedy prostředí, prompty, skills a to, jak je systém kolem modelu navržený. Podle něj má člověk nad harness mnohem větší kontrolu než nad modelem samotným.

## Model vs. harness
Matt říká, že „everyone's obsessed with the model“, ale podle něj by měli být lidé mnohem víc zainteresovaní do harnessu. Zmiňuje, že stejně jako u Fable je model užitečný, ale harness má podle něj stejně práce a mnohem větší prostor ke zlepšování. Lidé se podle něj dívají na „big shiny new thing“, místo aby se soustředili na věci, které fungují už 30 nebo 40 let.

Když padne otázka, jak optimalizovat token spend, odpovídá jednoduše: mít codebase, ve které se dá snadno provádět změny. Tím podle něj začíná skutečná efektivita. Nejde jen o to mít lepší model, ale mít lepší systém, do kterého model pracuje.

## Strategické vs. taktické programování
Na otázku, co odliší lidi, kteří s AI utečou ostatním, od těch, kteří dostanou jen malý boost, Matt navazuje na Johna Osterhuta a jeho rozlišení mezi tactical a strategic programming.

Tactical programming podle něj znamená každodenní práci: psaní kódu, zápasení se syntaxí, řešení bugů, vytváření commitů, práci na jednotlivých úkolech. Strategic programming je naopak o tom vyhrávat válku, ne bitvu. Je to dlouhodobé přemýšlení: jak má codebase vypadat, jaké strategie zvýší velocity, jak celou práci posunout dopředu.

Matt říká, že strategické programování ho vždycky bavilo nejvíc, už jako juniora. AI podle něj v podstatě „sežrala“ tactical programming. Je lepší v tom dělat drobnou výkonnou práci než člověk, a navíc levněji. Proto je teď potřeba být skvělý v strategic programming, abys uměl vytěžit z „infinite fleet of tactical programmers“, kterou AI představuje.

## Jak se naučit delegovat na AI
Na otázku, jestli to znamená hlavně umět orchestraci agentů a základy software designu, Matt říká, že strategic programming se s AI vlastně nezměnilo. Místo juniorů nebo mid-level programátorů teď delegujeme na AI, ale principy dobré delegace jsou stejné.

Je potřeba:
- navrhnout těžké části dopředu,
- dobře vymezit scope úkolů,
- přemýšlet o interface mezi moduly,
- dbát na testy a testovací scénáře,
- navrhnout codebase tak, aby se v ní dobře pracovalo,
- a mít jen tolik dokumentace, aby AI věděla, kam sáhnout a co změnit.

Matt zdůrazňuje, že AI není náhrada strategického myšlení. Je to jen nový způsob delegace.

## Upskilling a proč jsou skills důležitější než dřív
Když přijde řeč na to, že si lidé musejí sami zvyšovat úroveň, Matt říká, že jeho vlastní schopnosti jsou pro AI multiplikátor. Když umí dobře dohlédnout na codebase a rozumí tomu, jak se má software stavět, může AI zadávat mnohem lepší instrukce a dostane z ní mnohem bohatší výstup.

Zmiňuje, že mnoho CTO a lidí z konferencí mu říká, že AI dělá seniory „10 times better“. Juniory sice taky trochu posune, ale seniorní vývojář získá mnohem větší boost. Proto podle něj tvoje skills nastavují strop toho, co AI dokáže. Když jsou tvoje skills slabé, AI se přes ten strop nedostane.

Matt proto říká, že getting good with AI znamená getting good at your domain. Lepší učitel může s AI učit mnohem líp než náhodný člověk. Podle něj jsou skills dnes důležitější než dřív, právě proto, že máš k dispozici silný multiplier a můžeš víc delegovat.

## Teach skill a učební workflow
Když se dostane na novou teach skill, Matt vysvětluje, že se dlouhodobě věnuje výuce. Deset let učil zpěv a voice hned po univerzitě, pak se stal developerem a poslední čtyři roky učí vývojáře. Přemýšlel tedy, co kdyby vzal principy výuky, které zná — třeba zone of proximal development nebo rozdíl mezi knowledge, skills a wisdom — a zakódoval je do skillu, který vytvoří kurz na libovolné téma na míru.

Říká, že to funguje extrémně dobře. Sám se takto učí třeba Rubikovu kostku a dokáže ji teď složit z paměti. Také si zkoušel, jak by teach skill pomohl naučit se být senior developerem, a výsledek byl podle něj skvělý. Skill prošel přes trusted resources, poskládal curriculum a vytvořil velmi kvalitní materiál.

## Praktická ukázka: naučit se systems design
David navrhuje, že by si to mohli vyzkoušet na systems design. Matt ale přidává jiný úhel: hodně lidí k němu přichází jako lidé, kteří už umí být engineer, a on učí hlavně takové lidi. Zajímá ho spíš, jestli skill umí naučit i úplné základy engineeringu, například člověka, který je „vibe coder“ a má mezery v základních znalostech.

Matt proto předvádí scénář, kde se v prázdném adresáři spustí teach skill. Zadá prompt v duchu: „I am a vibe coder and I want to fill in my knowledge gap so that I can ship better software.“ Popisuje, že zná jen základní CLI příkazy, umí trochu číst kód a používat terminal, ale to je všechno. Ptá se, co by se měl naučit dál.

Matt zdůrazňuje, že takový prompt je v čisté angličtině a může ho napsat kdokoli. Neptá se na samotný subject, ale na mission: proč tam člověk je, co chce získat, co znamená „ship better software“. Podle něj je to collaborative effort — člověk mluví s učitelem a agent je učitel.

## Mission, stateful skills a personalizované učení
Teach skill podle Matta nejdřív zjišťuje, kdo je člověk, co chce buildit, proč na tom záleží a jak vypadá úspěch. V ukázce se to překlápí třeba do: umět shipnout aplikaci, nerozbít ji, dostat ji ven a věřit, že funguje pro skutečné studenty.

Matt vysvětluje, že skill si vytváří learning record a pracuje statefully. Rozlišuje mezi stateless skills, které nepotřebují lokální paměť, a stateful skills, které si informace ukládají lokálně. Teach skill je stateful, protože dobrý učitel si pamatuje, co už žák dělal, kam míří a jaká je jeho mission.

Vytváří se i reference cheat sheet a první lesson, a protože je to HTML, je to podle Matta mnohem příjemnější než jen terminal. Learning se tak dá otevřít v browseru a pracovat s bohatším obsahem.

## Git jako nejvyšší leverage pro začátečníka
Když skill vyhodnotí, že uživatel je vibe coder, který umí trochu pracovat s terminalem a číst kód, dojde k závěru, že největší gap není syntaxe, ale věci kolem kódu, které umožňují shipovat bez strachu. Matt s tím souhlasí: git, čtení chyb, debugging, testování a pochopení, jak software skutečně shipuje, jsou podle něj první věci, které mají smysl.

Skill pak začíná s git. Učí jednoduché otázky typu:
- which command saves a snapshot of your staged changes?
- what command shows what has changed right now?
- what does git add do to a change?
- a commit je nejlepší chápat jako safe point.
- pokud rozbiješ soubor, ale ještě jsi necommitnul, použiješ git restore.

Matt říká, že to využívá známé vzdělávací techniky, hlavně quizzes. Ty sice nemá moc rád, ale jsou prý „unreasonably effective“ pro posílení paměti. Skill zároveň odkazuje na primary source, třeba na progit book, a pak vybízí k dalším otázkám a dalším lekcím.

## Proč je teach skill dobrý
Matt vysvětluje, že knowledge není jen seznam faktů. Představuje si ji jako graph nebo forest, kterým se člověk pohybuje. Teach skill z toho dělá lineární cestu: ví, co už ses naučil, má to uložené v learning recordu a navazuje dalším krokem.

Zmíní, že na obrazovce je vidět mission i learning record, tedy počáteční stav a to, co už bylo zjištěno. Podle něj je to skvělý způsob, jak lidi učit, hlavně ve vývoji, protože sám ví, jak se developerské vzdělávání dělá, a tenhle know-how do skillu promítl.

## Kde to najít a jak to používat
David se ptá, jestli je to na GitHubu. Matt odpovídá, že ano: „GitHub Matt Pocock skills“. Pak stačí spustit CLI příkaz `npx skills latest add matt skills` a vybrat teach skill. Skill se uloží do lokálního setupu a funguje jak v claw code, tak v codeex. Potom můžeš teach volat v novém workspace.

## Co dělá dobrý agent skill
Na otázku, co odlišuje dobrý agent skill od špatného, Matt říká, že je to hluboká otázka a záleží na tom, co od skillu chceš. Rozlišuje dva typy skills:

1. **Procedures** — něco, co chceš spouštět sám.
2. **Abilities** — něco, co má model používat sám.

Jako ability uvádí třeba coding standards. Když agent píše React kód, může si načíst skill s pravidly, jak má React kód vypadat. Jako procedure uvádí svůj oblíbený grill me skill.

## Grill me skill a práce s kontrolou
Grill me skill je podle Matta velmi krátký, ale extrémně efektivní. V podstatě změní model na adversarial interviewer, který klade otázky, zpochybňuje návrhy a pomáhá dojít ke shared understanding. Matt říká, že ho používá i jako náhradu plan mode před implementací: řekne nápad, nechá se vyzpovídat a společně se vyjasní nejasnosti.

Dodává, že tahle forma je pro něj čistě procedure, ne ability. On chce být v kontrole, nejdřív použít grill me, potom třeba napsat product requirements document a z něj udělat jednotlivé issues, přes které se pak postupuje. To je podle něj osobní preference, ale dává mu to smysl.

## Proč nechat AI řídit všechno
V rozhovoru padne úvaha, že někdo chce AI nechat, aby sama vytvářela seznam schopností, knowledge a rozhodnutí, které odlišují 100x vývojáře od 1x vývojáře. Matt ale namítá, že skills jsou těžké na psaní právě proto, že každá skill description se leakuje do context window. To je podle něj důležitý problém.

Zmíní, že některé skills mají `disable model invocation true`, takže je může vyvolat jen uživatel a jejich popis se do contextu modelu nenačítá. Zdůrazňuje, že nechce přenášet příliš mnoho znalostí do AI, ale spíš je držet v člověku. Developer má být driver, držet volant a řídit.

## Tři věci: knowledge, skills, wisdom
Na závěr Matt rozlišuje tři věci, které potřebuješ být dobrý v čemkoli:
- **knowledge** – rozumět tomu v hlavě,
- **skills** – umět to dělat opakovaně a mít to v muscle memory,
- **wisdom** – vědět, kdy to použít a jak to zapadá do reálného světa.

Dodává, že wisdom je skoro nemožné získat bez toho, aby člověk danou věc opravdu dělal v praxi. V tom je podle něj ta skutečná hodnota zkušenosti.

## Zmíněné odkazy a zdroje
- https://youtu.be/nQwJVHCtDDY?si=v1jf4sZjn3RZkmSw
- Fable
- Philosophy of Software Design — John Ousterhout
- progit book
- SER API
- Whisper Flow
- GitHub Matt Pocock skills
- `npx skills latest add matt skills`
- Claw Code
- Codeex