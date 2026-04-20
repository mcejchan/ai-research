import os
from typing import Dict
from openai import OpenAI

# --- Prompty ---
BASE_SYSTEM = {
  "cs": "DŮLEŽITÉ: Jsi editor, NIKOLI summarizer! Tvým úkolem je ZACHOVAT většinu původního textu, jen ho vyčistit a reorganizovat. NESHRNOVEJ obsah - pouze odstraň duplicity, opravy ve větách a rozděl do kapitol. Výsledný text má být 50-70% původní délky s většinou původních vět a informací.",
  "en": "CRITICAL: You are a transcript EDITOR, NOT a summarizer! Your job is to PRESERVE the original English text, just clean and organize it. DO NOT translate to another language. DO NOT summarize. COPY most original sentences. Only remove: duplicates, speech fillers ('um', 'uh', 'like'), incomplete sentences. Keep 60-75% of original content length."
}

TEMPLATE_GENERAL = {
  "cs": """Přepracuj tento přepis rozhovoru do čitelnější formy:

# {{title}}
**Kanál:** {{channel}}  
**URL:** {{url}}

## Úvod
[Kdo jsou účastníci rozhovoru a o čem se bude bavit - krátký kontext]

## [Název kapitoly 1 - hlavní téma]
[Vyčistěný text z přepisu - odstraň "ehm", "jako", opakování, ale zachovej podstatu konverzace a důležité informace. Spojuj krátké věty do delších, logicky strukturovaných odstavců.]

## [Název kapitoly 2 - další téma]
[Pokračování vyčištěného přepisu...]

## [Název kapitoly 3 - další téma]
[Pokračování vyčištěného přepisu...]

## Zmíněné odkazy a zdroje
- [Seznam všech konkrétních odkazů, nástrojů, webů zmíněných v rozhovoru]

---

KRITICKY DŮLEŽITÉ INSTRUKCE:

🚨 **NESHRNOVEJ! NEZJEDNODUŠUJ! ZACHOVEJ VĚTŠINU TEXTU!** 🚨

1. **ZACHOVEJ 60-75% původního obsahu** - jen vymaž duplicity a výplně
2. **Zachovej původní věty:** Kopíruj celé věty, jen spoj fragmenty dohromady  
3. **Odstraň pouze:** "ehm", "jako", "víte", opakování stejné myšlenky, nedokončené věty
4. **Zachovej specifika:** všechny konkrétní informace, jména, čísla, příklady, citace
5. **Rozděl do kapitol:** podle témat, ale KAŽDÁ kapitola má obsahovat HODNĚ původního textu
6. **Nech to jako rozhovor:** zachovej "Craig říká", "host zmiňuje", atd.
7. **Kopíruj, nevymýšlej:** používej původní formulace, ne své shrnutí

❌ ŠPATNĚ: "Craig diskutuje o bezpečnosti" 
✅ SPRÁVNĚ: "Craig říká: 'Bylo by šílené mít API klíč k produkčnímu systému přístupný stochastickému agentovi'"

CÍLE: Výsledek 12,000-15,000 znaků (využij maximum modelu!), zachová většinu původních vět a detailů.
""",
  "en": """Extract key insights and practical information from this interview transcript:

# {{title}}
**Channel:** {{channel}}  
**URL:** {{url}}

## Key Takeaways (3-5 main points)
For each key point, provide:
- **Point title:** [Clear, specific insight]
- **Quote:** "[Most interesting/impactful quote supporting this point]" 
- **Why it matters:** [Brief context/significance]

### 1. [Point Title]
**Quote:** "[Exact quote from transcript]"
**Why it matters:** [2-3 sentences explaining significance]

### 2. [Point Title]  
**Quote:** "[Exact quote from transcript]"
**Why it matters:** [2-3 sentences explaining significance]

### 3. [Point Title]
**Quote:** "[Exact quote from transcript]"
**Why it matters:** [2-3 sentences explaining significance]

## Practical Tips & Procedures
Extract any step-by-step processes, implementation details, or actionable advice:

### [Tip/Process Name]
**What it does:** [Brief description]
**Steps:**
1. [Detailed step with specifics]
2. [Detailed step with specifics]
3. [Detailed step with specifics]
**Quote:** "[Supporting quote from transcript]"
**When to use:** [Specific scenarios]

## Tools & Technologies Mentioned
- **[Tool Name]:** [What it does, how to use it, link if mentioned]

## Important Warnings/Risks
- **[Risk]:** "[Quote about the risk]" - [Why it's dangerous]

---

INSTRUCTIONS:
- Focus on ACTIONABLE insights, not general discussion
- Use EXACT quotes from transcript - never paraphrase
- Look for practical processes, step-by-step instructions, specific recommendations
- Skip general conversation, focus on concrete takeaways
- Each point should teach something specific and useful
"""
}

def analyze_text(transcript: str, intent: str, lang: str, extra_context: Dict) -> str:
    client = OpenAI(
        base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:18800/v1"),
        api_key=os.getenv("OPENAI_API_KEY", "copilot-bridge"),
    )
    
    # Use English prompt for English content to avoid translation bias
    prompt_lang = "en" if transcript.strip().startswith(('I', 'We', 'You', 'The', 'This', 'That')) else lang
    
    system = BASE_SYSTEM.get(prompt_lang, BASE_SYSTEM["en"])
    template = TEMPLATE_GENERAL.get(prompt_lang, TEMPLATE_GENERAL["en"])
    
    content = template.replace("{{title}}", extra_context.get("title",""))\
                       .replace("{{channel}}", extra_context.get("channel",""))\
                       .replace("{{url}}", extra_context.get("url","")) + "\n\n" + transcript
    
    resp = client.chat.completions.create(
        model=os.getenv("LLM_MODEL", "gpt-4o"),
        messages=[{"role":"system","content": system}, {"role":"user","content": content}],
        temperature=0.2,
        max_tokens=15000,  # Využít maximum modelu pro dlouhé výstupy
    )
    return resp.choices[0].message.content


def embed_text(text: str):
    client = OpenAI(
        base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:18800/v1"),
        api_key=os.getenv("OPENAI_API_KEY", "copilot-bridge"),
    )
    return client.embeddings.create(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large"), 
        input=text
    ).data[0].embedding
