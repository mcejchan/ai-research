---
title: "Expose quiz-page logic for testing without a browser"
date: 2026-10-23
category: architecture
component: frontend
tags: [quiz, vanilla-javascript, testing, static-hosting]
file_type: rules
---

# Expose quiz-page logic for testing without a browser

For static quiz pages built with vanilla JavaScript, move pure logic for level filtering/rendering and quiz answer evaluation/transitions into a separate script, then load it before the page controller. This made the logic testable with Node’s built-in test runner without a browser or bundler. Keep DOM initialization separate: extracting helpers alone does not complete controller decomposition, and DOM-level loading and error states still need characterization tests.

## Context
Extracted from task: Tech debt: decompose quiz page controllers
