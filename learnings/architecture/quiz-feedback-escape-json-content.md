---
title: "Quiz UI: escapovat JSON obsah ve feedbacku"
date: 2026-05-18
category: architecture
component: frontend
tags: [quiz, frontend, xss, vanilla-js, feedback]
---

# Quiz UI: zachovat data bezpečně při renderování feedbacku

V quiz dashboardu je feedback po odpovědi skládaný v klientském `app.js`. Pokud se k běžnému textu přidává volitelné HTML pro doplňující vysvětlení, je potřeba dál escapovat obsah z JSON dat.

## Praktický vzor

Text odpovědi i `question.explanation` nejdřív projdou přes existující `escapeHtml()` a teprve potom se vloží do `innerHTML` spolu s malým wrapperem pro stylování.

```js
const explanation = question.explanation
  ? `<div class="feedback-explanation">${escapeHtml(question.explanation)}</div>`
  : '';
feedback.innerHTML = `${escapeHtml(feedbackText)}${explanation}`;
```

## Proč

Level JSON je obsahová vrstva, ne kód. I u lokálních quiz dat je bezpečnější nepředpokládat, že texty otázek a vysvětlení nemohou obsahovat znaky HTML. Tím se dá přidat jednoduchý markup pro UI bez otevírání XSS díry.

## Kdy použít

Při dalších úpravách vanilla quiz UI, kde je potřeba kombinovat text z JSON dat s malým množstvím ručně řízeného HTML pro layout nebo stylování.
