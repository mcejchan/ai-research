#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const THRESHOLDS = {
  longestRatioMax: 0.50,
  positionalRatioMax: 0.45,
  minQuestionsForStats: 5,
  perQuestionLengthRatioMax: 1.6,
};

function validateLevelData(data, file = '<level>') {
  const structuralErrors = [];
  const advisories = [];
  const stats = {
    total: 0,
    correctIsLongest: 0,
    correctIndexCounts: {},
    correctMuchLongerThanDistractors: 0,
    typeMismatch: 0,
    missingExplanation: 0,
  };

  if (!data || typeof data !== 'object' || Array.isArray(data)) {
    structuralErrors.push('Level must be a JSON object');
    return { file, ok: false, structuralErrors, advisories, stats };
  }
  if (typeof data.title !== 'string' || !data.title.trim()) {
    structuralErrors.push('Missing or invalid top-level "title"');
  }
  if (!Array.isArray(data.questions) || data.questions.length === 0) {
    structuralErrors.push('Missing, empty, or invalid "questions" array');
    return { file, ok: false, structuralErrors, advisories, stats };
  }

  data.questions.forEach((question, index) => {
    const prefix = `Q${index + 1}`;
    stats.total++;

    if (!question || typeof question !== 'object' || Array.isArray(question)) {
      structuralErrors.push(`${prefix}: question must be an object`);
      return;
    }
    if (typeof question.question !== 'string' || !question.question.trim()) {
      structuralErrors.push(`${prefix}: missing "question" text`);
    }
    if (!['single', 'multi'].includes(question.type)) {
      structuralErrors.push(`${prefix}: "type" must be "single" or "multi"`);
    }
    if (typeof question.points !== 'number' || !Number.isFinite(question.points)
      || question.points < 1 || question.points > 4) {
      structuralErrors.push(`${prefix}: "points" must be a finite number from 1 to 4`);
    }

    const validOptions = Array.isArray(question.options)
      && question.options.length >= 2
      && question.options.every((option) => typeof option === 'string');
    if (!validOptions) {
      structuralErrors.push(`${prefix}: needs at least 2 string options`);
    }

    const validCorrect = Array.isArray(question.correct)
      && question.correct.length > 0
      && question.correct.every(Number.isInteger);
    if (!validCorrect) {
      structuralErrors.push(`${prefix}: "correct" must contain integer indices`);
    } else {
      if (new Set(question.correct).size !== question.correct.length) {
        structuralErrors.push(`${prefix}: "correct" indices must be unique`);
      }
      if (validOptions && question.correct.some((answer) => answer < 0 || answer >= question.options.length)) {
        structuralErrors.push(`${prefix}: "correct" indices out of range`);
      }
      if (question.type === 'single' && question.correct.length !== 1) {
        structuralErrors.push(`${prefix}: type="single" must have exactly 1 correct answer`);
      }
      if (question.type === 'multi' && question.correct.length === 1) {
        stats.typeMismatch++;
        advisories.push(`${prefix}: type="multi" has only 1 correct answer; consider "single"`);
      }
    }

    if (typeof question.explanation !== 'string' || !question.explanation.trim()) {
      stats.missingExplanation++;
      advisories.push(`${prefix}: missing "explanation"`);
    }

    const canAnalyze = validOptions && validCorrect
      && question.correct.every((answer) => answer >= 0 && answer < question.options.length);
    if (!canAnalyze) return;

    const lengths = question.options.map((option) => option.length);
    const maxLength = Math.max(...lengths);
    const correctLengths = question.correct.map((answer) => question.options[answer].length);
    const maxCorrectLength = Math.max(...correctLengths);
    const distractorLengths = question.options
      .filter((_, optionIndex) => !question.correct.includes(optionIndex))
      .map((option) => option.length);
    const maxDistractorLength = distractorLengths.length ? Math.max(...distractorLengths) : 0;

    if (correctLengths.some((length) => length === maxLength)) stats.correctIsLongest++;
    if (maxDistractorLength > 0
      && maxCorrectLength / maxDistractorLength > THRESHOLDS.perQuestionLengthRatioMax) {
      stats.correctMuchLongerThanDistractors++;
      advisories.push(
        `${prefix}: correct is ${(maxCorrectLength / maxDistractorLength).toFixed(1)}x longer than longest distractor`,
      );
    }
    question.correct.forEach((answer) => {
      stats.correctIndexCounts[answer] = (stats.correctIndexCounts[answer] || 0) + 1;
    });
  });

  if (stats.total >= THRESHOLDS.minQuestionsForStats && structuralErrors.length === 0) {
    const longestRatio = stats.correctIsLongest / stats.total;
    if (longestRatio > THRESHOLDS.longestRatioMax) {
      advisories.push(
        `BIAS: correct answer is longest in ${stats.correctIsLongest}/${stats.total} questions`,
      );
    }

    const totalCorrectMarks = Object.values(stats.correctIndexCounts).reduce((total, count) => total + count, 0);
    for (const [answer, count] of Object.entries(stats.correctIndexCounts)) {
      if (count / totalCorrectMarks > THRESHOLDS.positionalRatioMax) {
        advisories.push(`BIAS: correct answer is at index ${answer} in ${count}/${totalCorrectMarks} answers`);
      }
    }

    if (stats.correctMuchLongerThanDistractors / stats.total > 0.4) {
      advisories.push(
        `BIAS: correct answer is over 1.6x longer than the longest distractor in ${stats.correctMuchLongerThanDistractors}/${stats.total} questions`,
      );
    }
  }

  return {
    file,
    ok: structuralErrors.length === 0,
    structuralErrors,
    advisories,
    stats,
  };
}

function validateLevel(filePath) {
  return validateLevelData(JSON.parse(fs.readFileSync(filePath, 'utf8')), filePath);
}

function formatResult(result) {
  const status = result.ok ? 'PASS' : 'FAIL';
  let output = `\n${status}  ${result.file}\n`;
  if (result.stats.total > 0) {
    output += `  ${result.stats.total} questions\n`;
  }
  if (result.structuralErrors.length) {
    output += `  ERRORS:\n${result.structuralErrors.map((error) => `    ${error}`).join('\n')}\n`;
  }
  if (result.advisories.length) {
    output += `  ADVISORIES:\n${result.advisories.map((warning) => `    ${warning}`).join('\n')}\n`;
  }
  return output;
}

function levelFiles(inputPath) {
  const stat = fs.statSync(inputPath);
  if (stat.isFile()) return [inputPath];

  const files = [];
  const walk = (directory) => {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const fullPath = path.join(directory, entry.name);
      if (entry.isDirectory()) walk(fullPath);
      else if (entry.isFile() && entry.name.endsWith('.json') && entry.name !== 'index.json') {
        files.push(fullPath);
      }
    }
  };
  walk(inputPath);
  return files;
}

function main(argv = process.argv.slice(2)) {
  const inputPath = argv[0];
  if (!inputPath) {
    console.error('Usage: node validate-quiz.js <path-to-level.json | directory>');
    return 2;
  }

  let files;
  try {
    files = levelFiles(inputPath);
  } catch (error) {
    console.error(`Cannot read ${inputPath}: ${error.message}`);
    return 2;
  }
  if (files.length === 0) {
    console.error('No JSON files found');
    return 2;
  }

  let failed = 0;
  for (const file of files) {
    let result;
    try {
      result = validateLevel(file);
    } catch (error) {
      console.error(`Cannot parse ${file}: ${error.message}`);
      return 2;
    }
    process.stdout.write(formatResult(result));
    if (!result.ok) failed++;
  }
  console.log(`\n${files.length - failed}/${files.length} levels structurally valid`);
  return failed > 0 ? 1 : 0;
}

if (require.main === module) process.exitCode = main();

module.exports = { formatResult, main, validateLevel, validateLevelData };
