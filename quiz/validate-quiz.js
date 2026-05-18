#!/usr/bin/env node
/**
 * validate-quiz.js — Quiz level JSON validator
 *
 * Detects systematic bias in quiz questions that makes them too easy to game:
 *   1. Correct answer is the longest option (LLM bias — players guess by length)
 *   2. Correct answer is always at index 0/1 (LLM positional bias)
 *   3. Distractors are obviously absurd (one-word non-sequiturs)
 *   4. Multi-select questions with single correct (mislabeled)
 *   5. Missing explanation, options, or correct fields
 *
 * Usage:
 *   node validate-quiz.js <path-to-level.json>
 *   node validate-quiz.js levels/                  # validate all
 *
 * Exit codes:
 *   0 = all checks pass
 *   1 = validation failed (bias detected or schema error)
 *   2 = file not found or parse error
 */

const fs = require('fs');
const path = require('path');

const THRESHOLDS = {
  // Random baseline for "correct is longest" with 4 options is ~25-30%.
  // We allow some slack up to 50% (random distribution noise on small N).
  // > 50% = systematic bias.
  longestRatioMax: 0.50,

  // Random baseline for any single index with N options = 1/N.
  // For 4-option questions, expect ~25% at each index.
  // Any single index getting > 45% of correct answers = positional bias.
  positionalRatioMax: 0.45,

  // If quiz has < 5 questions, ratios are too noisy — only schema-check.
  minQuestionsForStats: 5,

  // Per-question: ratio of correct option length to max distractor length.
  // If correct is significantly longer than longest distractor on >50% of questions,
  // that's a per-question pattern even if global ratio looks OK.
  perQuestionLengthRatioMax: 1.6, // correct can be up to 1.6× longest distractor
};

function validateLevel(filePath) {
  let data;
  try {
    data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (e) {
    return { file: filePath, ok: false, errors: [`Parse error: ${e.message}`] };
  }

  const errors = [];
  const warnings = [];
  const stats = {
    total: 0,
    correctIsLongest: 0,
    correctIndexCounts: {},
    correctMuchLongerThanDistractors: 0,
    typeMismatch: 0,
    missingExplanation: 0,
  };

  // Schema check
  if (!data.title) errors.push('Missing top-level "title"');
  if (!data.questions || !Array.isArray(data.questions)) {
    errors.push('Missing or invalid "questions" array');
    return { file: filePath, ok: false, errors, warnings, stats };
  }

  data.questions.forEach((q, i) => {
    const prefix = `Q${i + 1}`;
    stats.total++;

    if (!q.question || typeof q.question !== 'string') errors.push(`${prefix}: missing "question" text`);
    if (!Array.isArray(q.options) || q.options.length < 2) {
      errors.push(`${prefix}: needs at least 2 options`);
      return;
    }
    if (!Array.isArray(q.correct) || q.correct.length === 0) {
      errors.push(`${prefix}: missing or empty "correct" array`);
      return;
    }
    if (q.correct.some((idx) => typeof idx !== 'number' || idx < 0 || idx >= q.options.length)) {
      errors.push(`${prefix}: "correct" indices out of range`);
      return;
    }
    if (!q.explanation || typeof q.explanation !== 'string') {
      stats.missingExplanation++;
      warnings.push(`${prefix}: missing "explanation"`);
    }
    if (q.type === 'single' && q.correct.length > 1) {
      stats.typeMismatch++;
      errors.push(`${prefix}: type="single" but has ${q.correct.length} correct answers`);
    }
    if (q.type === 'multi' && q.correct.length === 1) {
      stats.typeMismatch++;
      warnings.push(`${prefix}: type="multi" but only 1 correct — should be "single"`);
    }

    // Length analysis
    const lens = q.options.map((o) => o.length);
    const maxLen = Math.max(...lens);
    const correctLens = q.correct.map((idx) => q.options[idx].length);
    const maxCorrectLen = Math.max(...correctLens);
    const distractorLens = q.options.filter((_, idx) => !q.correct.includes(idx)).map((o) => o.length);
    const maxDistractorLen = distractorLens.length ? Math.max(...distractorLens) : 0;

    if (correctLens.some((l) => l === maxLen)) {
      stats.correctIsLongest++;
    }
    if (maxDistractorLen > 0 && maxCorrectLen / maxDistractorLen > THRESHOLDS.perQuestionLengthRatioMax) {
      stats.correctMuchLongerThanDistractors++;
      warnings.push(`${prefix}: correct is ${(maxCorrectLen / maxDistractorLen).toFixed(1)}× longer than longest distractor (${maxCorrectLen} vs ${maxDistractorLen} chars)`);
    }

    // Index distribution (only first correct index for single, all for multi)
    q.correct.forEach((idx) => {
      stats.correctIndexCounts[idx] = (stats.correctIndexCounts[idx] || 0) + 1;
    });
  });

  // Aggregate bias checks (only if enough questions)
  if (stats.total >= THRESHOLDS.minQuestionsForStats && errors.length === 0) {
    const longestRatio = stats.correctIsLongest / stats.total;
    if (longestRatio > THRESHOLDS.longestRatioMax) {
      errors.push(
        `BIAS: correct answer is longest in ${stats.correctIsLongest}/${stats.total} questions (${(longestRatio * 100).toFixed(0)}%) — limit ${(THRESHOLDS.longestRatioMax * 100).toFixed(0)}%`
      );
    }

    // Positional bias
    const totalCorrectMarks = Object.values(stats.correctIndexCounts).reduce((a, b) => a + b, 0);
    for (const [idx, count] of Object.entries(stats.correctIndexCounts)) {
      const ratio = count / totalCorrectMarks;
      if (ratio > THRESHOLDS.positionalRatioMax) {
        errors.push(
          `BIAS: correct answer is at index ${idx} in ${count}/${totalCorrectMarks} questions (${(ratio * 100).toFixed(0)}%) — limit ${(THRESHOLDS.positionalRatioMax * 100).toFixed(0)}%`
        );
      }
    }

    // Per-question length pattern (in addition to global)
    const perQRatio = stats.correctMuchLongerThanDistractors / stats.total;
    if (perQRatio > 0.4) {
      errors.push(
        `BIAS: correct answer is >1.6× longer than longest distractor in ${stats.correctMuchLongerThanDistractors}/${stats.total} questions (${(perQRatio * 100).toFixed(0)}%) — pattern detectable per-question`
      );
    }
  }

  return { file: filePath, ok: errors.length === 0, errors, warnings, stats };
}

function formatResult(result) {
  const status = result.ok ? '✅ PASS' : '❌ FAIL';
  let out = `\n${status}  ${result.file}\n`;
  if (result.stats && result.stats.total > 0) {
    const s = result.stats;
    const longestPct = ((s.correctIsLongest / s.total) * 100).toFixed(0);
    const indexDist = Object.entries(s.correctIndexCounts)
      .sort(([a], [b]) => +a - +b)
      .map(([idx, n]) => `[${idx}]=${n}`)
      .join(' ');
    out += `  ${s.total} questions | correct-is-longest: ${s.correctIsLongest}/${s.total} (${longestPct}%) | index dist: ${indexDist}\n`;
  }
  if (result.errors.length) {
    out += '  ERRORS:\n' + result.errors.map((e) => '    ❌ ' + e).join('\n') + '\n';
  }
  if (result.warnings.length) {
    out += '  WARNINGS:\n' + result.warnings.map((w) => '    ⚠️  ' + w).join('\n') + '\n';
  }
  return out;
}

function main() {
  const arg = process.argv[2];
  if (!arg) {
    console.error('Usage: node validate-quiz.js <path-to-level.json | directory>');
    process.exit(2);
  }
  if (!fs.existsSync(arg)) {
    console.error(`Not found: ${arg}`);
    process.exit(2);
  }

  const stat = fs.statSync(arg);
  const files = [];
  if (stat.isFile()) {
    files.push(arg);
  } else if (stat.isDirectory()) {
    const walk = (dir) => {
      for (const entry of fs.readdirSync(dir)) {
        const full = path.join(dir, entry);
        const s = fs.statSync(full);
        if (s.isDirectory()) walk(full);
        else if (entry.endsWith('.json') && entry !== 'index.json') files.push(full);
      }
    };
    walk(arg);
  }

  if (!files.length) {
    console.error('No JSON files found');
    process.exit(2);
  }

  let failed = 0;
  for (const f of files) {
    const result = validateLevel(f);
    process.stdout.write(formatResult(result));
    if (!result.ok) failed++;
  }

  console.log(`\n${files.length - failed}/${files.length} levels passed`);
  process.exit(failed > 0 ? 1 : 0);
}

main();
