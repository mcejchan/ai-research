---
title: "Normalize unknown metadata values at the index boundary"
date: 2026-07-22
category: patterns
component: frontend
tags: [normalization, metadata, fallback, static-build]
---

The quiz index builder passed an unknown difficulty value (`weird`) through unchanged, producing metadata outside the supported difficulty set. Normalize values while building the static index: preserve recognized values such as `extra-easy`, `easy`, and `hard`, and map unknown values to the safe `hard` fallback. Boundary normalization keeps the generated artifact valid and avoids requiring every runtime consumer to handle arbitrary source data.