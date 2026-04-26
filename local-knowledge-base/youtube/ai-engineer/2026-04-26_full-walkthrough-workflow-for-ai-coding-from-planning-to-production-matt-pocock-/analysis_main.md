# Kompletní průvodce: Workflow pro AI kódování od plánování po produkci — Matt Pocock  
**Kanál:** AI Engineer  
**URL:** [Odkaz na video](https://youtu.be/-QFHIoCo-Ko)

---

## Úvod  
Matt Pocock, učitel a odborník na AI, představuje dvouhodinový workshop zaměřený na workflow pro práci s AI v oblasti kódování. Hlavní myšlenkou je, že i když AI přináší nové paradigma, základní principy softwarového inženýrství stále platí. Matt se snaží ukázat, jak tyto principy aplikovat při práci s AI, a zároveň zdůrazňuje důležitost efektivního plánování a spolupráce mezi lidmi a AI.

---

## AI a její omezení: Smart zóna a Dumb zóna  
Matt vysvětluje, že při práci s velkými jazykovými modely (LLMs) je klíčové pochopit jejich omezení. Dex Hy, zakladatel společnosti Human Layer, popisuje koncept "smart zóny" a "dumb zóny".  

- **Smart zóna:** LLM funguje nejlépe na začátku konverzace, kdy je kontext minimální a vztahy mezi tokeny nejsou přetížené.  
- **Dumb zóna:** Jakmile se kontext rozšiřuje (např. přidáváním tokenů), model začíná ztrácet přesnost a dělat chyby. Matt uvádí, že tento problém nastává přibližně po 100k tokenů, bez ohledu na velikost kontextového okna.  

### Jak pracovat v rámci smart zóny  
Matt doporučuje rozdělit velké úkoly na menší části, které lze zpracovat v rámci smart zóny. Tento přístup připomíná tradiční softwarové inženýrské praktiky, jako je refaktoring nebo iterativní vývoj.  

---

## Multi-fázové plánování a iterace  
Matt popisuje svůj přístup k řešení komplexních úkolů pomocí multi-fázového plánování. Tento přístup zahrnuje:  
1. Rozdělení velkého úkolu na menší části.  
2. Iterativní zpracování každé části v rámci smart zóny.  
3. Kompaktování kontextu, aby se minimalizovalo přetížení modelu.  

### Kompaktování vs. resetování  
Matt preferuje resetování kontextu na základní stav (jako ve filmu "Momento"), místo aby se spoléhal na kompaktování. Resetování zajišťuje konzistenci a eliminuje riziko, že se model "zahltí" historickými daty.  

---

## Práce s AI: Grill Me Skill  
Matt představuje nástroj "Grill Me Skill", který pomáhá dosáhnout společného porozumění mezi uživatelem a AI. Tento nástroj:  
- Klade otázky k objasnění plánu.  
- Poskytuje doporučení pro každou otázku.  
- Umožňuje uživateli iterativně dolaďovat plán.  

### Příklad použití  
Matt demonstruje použití Grill Me Skill na příkladu gamifikace vzdělávací platformy. Klient (fiktivní Sarah Chen) požaduje přidání gamifikačních prvků, aby zlepšil retenci uživatelů. AI klade otázky, jako například:  
- Jaké akce budou odměňovány body?  
- Budou body přidělovány zpětně?  
- Jak bude vypadat uživatelské rozhraní pro gamifikaci?  

Tento proces umožňuje uživateli a AI dosáhnout společného porozumění a vytvořit plán, který je v souladu s požadavky klienta.  

---

## Spolupráce mezi lidmi a AI  
Matt zdůrazňuje důležitost spolupráce mezi lidmi a AI. Doporučuje:  
- Používat AI jako partnera při párovém programování.  
- Zapojit více lidí do rozhodování, zejména při klíčových otázkách.  
- Využívat AI k rychlejšímu provádění implementačních úkolů, ale zachovat lidský dohled nad kritickými rozhodnutími.  

---

## Doporučení pro plánování s AI  
Matt varuje před přílišnou závislostí na předem připravených nástrojích a frameworkech. Doporučuje:  
- Vlastnit a přizpůsobit si svůj plánovací stack.  
- Udržovat přehled o celém procesu, aby bylo možné řešit problémy.  
- Experimentovat s různými přístupy a nástroji, ale zachovat kontrolu nad procesem.  

---

## Zmíněné odkazy a zdroje  
- [AI Hero](https://aihero.com) – Článek o sledování tokenů.  
- Grill Me Skill – Nástroj pro dosažení společného porozumění s AI.  
- Gemini Meetings – Nástroj pro analýzu schůzek.  

---

Tento workshop poskytuje praktické rady a nástroje pro efektivní práci s AI, přičemž zdůrazňuje důležitost základních principů softwarového inženýrství a spolupráce mezi lidmi a AI.