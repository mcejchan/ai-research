# Jak vyčistit kódovou základnu zničenou AI (s jednou dovedností)  
**Kanál:** Matt Pocock  
**URL:** [https://www.youtube.com/watch?v=3MP8D-mdheA](https://www.youtube.com/watch?v=3MP8D-mdheA)  

---

## Úvod  
Matt Pocock v tomto videu diskutuje o problémech, které přináší AI do vývoje softwaru. AI sice urychluje vývoj, ale zároveň zvyšuje entropii kódu, což vede k rychlejšímu rozpadu kódových základen. Matt se zaměřuje na to, jak zachránit kódovou základnu, která se zdá být neopravitelná, pomocí základních softwarových principů a dovednosti zlepšování architektury kódu.  

---

## Co je problém s AI a kódem?  
Matt začíná tím, že upozorňuje na časté příspěvky na LinkedIn, kde lidé tvrdí, že díky AI je vývoj rychlejší a levnější. Ve skutečnosti však AI často urychluje rozpad kódu. Každá změna, která nebere v úvahu celou kódovou základnu, přidává malé problémy, které se časem hromadí. Výsledkem je „koule bláta“ – chaotický kód, který je těžké opravit.  

Matt již dříve natočil video o prevenci tohoto problému pomocí konceptu hlubokých modulů. Tentokrát se však zaměřuje na „léčbu“ – jak zachránit kódovou základnu pomocí základních softwarových principů a své dovednosti zlepšování architektury kódu.  

---

## Základy: Moduly, rozhraní a implementace  
Matt vysvětluje klíčové pojmy:  
- **Modul:** Jednotka v aplikaci, například sada React komponent tvořící stránku nebo funkce odpovědné za autentizaci.  
- **Rozhraní:** Vše, co musí volající vědět, aby modul správně používal (např. metody jako `signIn` a `signOut`).  
- **Implementace:** To, co modul skutečně dělá, když je volán.  

Moduly mohou být buď **hluboké**, nebo **mělké**:  
- **Hluboký modul** skrývá složitou implementaci za jednoduchým rozhraním.  
- **Mělký modul** má složité rozhraní, ale málo funkcionality.  

Hluboké moduly jsou lepší, protože volající potřebuje znát jen malé rozhraní, aby získal přístup k rozsáhlé funkcionalitě. Tento koncept pochází z knihy Johna Osterhouta *A Philosophy of Software Design*.  

---

## Závislosti, švy a adaptéry  
Moduly v aplikaci spolu komunikují prostřednictvím závislostí. Místa, kde se moduly propojují, se nazývají **švy**. Švy jsou klíčové pro testování – například při testování modulu můžete na švu použít mock.  

Matt zavádí pojem **adaptér** (z hexagonální architektury), což je konkrétní implementace rozhraní na švu. Například:  
- V aplikaci může být adaptér pro reálné hodiny.  
- V testech můžete použít adaptér pro falešné hodiny, abyste nemuseli čekat na skutečný čas.  

---

## Výhody hlubokých modulů  
Hluboké moduly přinášejí dvě hlavní výhody:  
1. **Lokalita:** Změny a opravy se soustředí na jedno místo.  
2. **Pákový efekt:** Uživatelé modulu získají více funkcionality na jednotku rozhraní, kterou se musí naučit.  

Cílem při zlepšování kódu je maximalizovat tyto dvě vlastnosti.  

---

## Praktická ukázka: Zlepšení kódové základny  
Matt ukazuje, jak použít svou dovednost zlepšování architektury kódu na reálné kódové základně – správci videokurzů. Tato aplikace má přes 1 500 commitů a není dokonalá. Matt spouští svou dovednost v nástroji Claude, který analyzuje kód a hledá příležitosti k prohloubení modulů.  

Nástroj identifikuje šest možností, kde lze zlepšit lokalitu a pákový efekt. Například:  
- Jeden koncept nemá jednotný šev, což znamená, že změny na frontendu mohou být nekompatibilní s backendem.  
- Matt vybírá tento problém k refaktoringu, aby získal lepší lokalitu.  

Nástroj navrhuje konkrétní změny, jako je sjednocení švů a návrh TypeScript rozhraní. Matt diskutuje návrhy s AI a vytváří GitHub issue, které může být zpracováno dalším agentem.  

---

## Role programátora a AI  
Matt zdůrazňuje, že tato dovednost vyžaduje aktivní zapojení programátora. AI je skvělá na taktické úrovni – rychle provádí změny. Programátor však musí být strategický, rozhodovat o dlouhodobém zdraví kódu a řídit AI.  

Doporučuje spouštět tuto dovednost každých pár dní, zejména v rychle se měnících kódových základnách. Hlubší moduly zlepšují testovatelnost a kvalitu výstupu AI.  

---

## Práce s legacy kódem  
Matt uzavírá otázkou, jak začít s AI v legacy kódu. Legacy kód často obsahuje mělké moduly a je těžké v něm provádět změny. Klíčem je vytvořit testovací rámec, který zajistí, že změny nic nerozbijí.  

Dovednost zlepšování architektury kódu je skvělým výchozím bodem pro práci s legacy kódem.  

---

## Zmíněné odkazy a zdroje  
- Kniha: *A Philosophy of Software Design* – John Osterhout  
- Nástroj: [GitHub Skills Repo](https://github.com/) (41,5k hvězd)  
- Video o Sandcastle: [Odkaz na video](https://www.youtube.com/)  
- Newsletter a dokumentace: [Odkaz na stránky Matta Pococka](https://www.mattpocock.com/)  

---

Matt uzavírá poděkováním divákům a zdůrazňuje, že hluboké moduly, testy a strategické rozhodování jsou klíčem k udržení kvalitní kódové základny.