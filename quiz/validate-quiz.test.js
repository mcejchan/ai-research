const assert = require('node:assert/strict');
const test = require('node:test');
const { validateLevelData } = require('./validate-quiz');

test('invalid level object returns the stable complete result', () => {
  assert.deepEqual(validateLevelData(null, 'fixture.json'), {
    file: 'fixture.json',
    ok: false,
    structuralErrors: ['Level must be a JSON object'],
    advisories: [],
    stats: {
      total: 0,
      correctIsLongest: 0,
      correctIndexCounts: {},
      correctMuchLongerThanDistractors: 0,
      typeMismatch: 0,
      missingExplanation: 0,
    },
  });
});

test('malformed questions are excluded from option statistics', () => {
  const result = validateLevelData({ title: 'Fixture', questions: [null] });
  assert.equal(result.stats.total, 1);
  assert.equal(result.stats.correctIsLongest, 0);
  assert.deepEqual(result.stats.correctIndexCounts, {});
  assert.deepEqual(result.structuralErrors, ['Q1: question must be an object']);
});

test('top-level title and questions diagnostics preserve order and early return', () => {
  assert.deepEqual(validateLevelData({ title: ' ', questions: [] }), {
    file: '<level>', ok: false,
    structuralErrors: ['Missing or invalid top-level "title"', 'Missing, empty, or invalid "questions" array'],
    advisories: [],
    stats: { total: 0, correctIsLongest: 0, correctIndexCounts: {}, correctMuchLongerThanDistractors: 0, typeMismatch: 0, missingExplanation: 0 },
  });
});

test('question errors, advisories, and counters retain their exact semantics', () => {
  const result = validateLevelData({ title: 'Fixture', questions: [{
    question: '', type: 'multi', points: 5, options: ['yes', 'no'], correct: [0, 0], explanation: '',
  }] });
  assert.deepEqual(result.structuralErrors, [
    'Q1: missing "question" text', 'Q1: "points" must be a finite number from 1 to 4', 'Q1: "correct" indices must be unique',
  ]);
  assert.deepEqual(result.advisories, ['Q1: missing "explanation"']);
  assert.deepEqual(result.stats, { total: 1, correctIsLongest: 1, correctIndexCounts: { 0: 2 }, correctMuchLongerThanDistractors: 0, typeMismatch: 0, missingExplanation: 1 });
});

test('valid results include length and position stats and threshold advisories', () => {
  const questions = Array.from({ length: 5 }, () => ({
    question: 'Q?', type: 'single', points: 1, options: ['extraordinarily long correct answer', 'no'], correct: [0], explanation: 'why',
  }));
  const result = validateLevelData({ title: 'Fixture', questions }, 'valid.json');
  assert.equal(result.file, 'valid.json');
  assert.equal(result.ok, true);
  assert.deepEqual(result.structuralErrors, []);
  assert.deepEqual(result.stats, { total: 5, correctIsLongest: 5, correctIndexCounts: { 0: 5 }, correctMuchLongerThanDistractors: 5, typeMismatch: 0, missingExplanation: 0 });
  assert.deepEqual(result.advisories, [
    'Q1: correct is 17.5x longer than longest distractor',
    'Q2: correct is 17.5x longer than longest distractor',
    'Q3: correct is 17.5x longer than longest distractor',
    'Q4: correct is 17.5x longer than longest distractor',
    'Q5: correct is 17.5x longer than longest distractor',
    'BIAS: correct answer is longest in 5/5 questions',
    'BIAS: correct answer is at index 0 in 5/5 answers',
    'BIAS: correct answer is over 1.6x longer than the longest distractor in 5/5 questions',
  ]);
});

test('invalid type and points produce ordered diagnostics without changing valid option statistics', () => {
  const result = validateLevelData({ title: 'Fixture', questions: [{
    question: 'Q?', type: 'unknown', points: 0, options: ['A', 'B'], correct: [0], explanation: 'why',
  }] });
  assert.equal(result.ok, false);
  assert.deepEqual(result.structuralErrors, [
    'Q1: "type" must be "single" or "multi"',
    'Q1: "points" must be a finite number from 1 to 4',
  ]);
  assert.deepEqual(result.stats, {
    total: 1, correctIsLongest: 1, correctIndexCounts: { 0: 1 },
    correctMuchLongerThanDistractors: 0, typeMismatch: 0, missingExplanation: 0,
  });
});

test('invalid points variants and malformed options have exact structural diagnostics', () => {
  for (const points of [NaN, Infinity, '1', 0, 5]) {
    const result = validateLevelData({ title: 'Fixture', questions: [{
      question: 'Q?', type: 'single', points, options: ['A', 'B'], correct: [0], explanation: 'why',
    }] });
    assert.deepEqual(result.structuralErrors, ['Q1: "points" must be a finite number from 1 to 4']);
  }

  for (const options of [undefined, ['A'], ['A', 2]]) {
    const result = validateLevelData({ title: 'Fixture', questions: [{
      question: 'Q?', type: 'single', points: 1, options, correct: [0], explanation: 'why',
    }] });
    assert.deepEqual(result.structuralErrors, ['Q1: needs at least 2 string options']);
    assert.deepEqual(result.stats.correctIndexCounts, {});
  }
});

test('invalid correct indices preserve ordered diagnostics and do not enter option statistics', () => {
  for (const [correct, expected] of [
    [[0.5], 'Q1: "correct" must contain integer indices'],
    [[2], 'Q1: "correct" indices out of range'],
  ]) {
    const result = validateLevelData({ title: 'Fixture', questions: [{
      question: 'Q?', type: 'single', points: 1, options: ['A', 'B'], correct, explanation: 'why',
    }] });
    assert.equal(result.ok, false);
    assert.deepEqual(result.structuralErrors, [expected]);
    assert.deepEqual(result.stats.correctIndexCounts, {});
  }
});

test('single and multi correct-answer consistency retains structural and advisory semantics', () => {
  const single = validateLevelData({ title: 'Fixture', questions: [{
    question: 'Q?', type: 'single', points: 1, options: ['A', 'B'], correct: [0, 1], explanation: 'why',
  }] });
  assert.deepEqual(single.structuralErrors, ['Q1: type="single" must have exactly 1 correct answer']);
  assert.deepEqual(single.advisories, []);

  const multi = validateLevelData({ title: 'Fixture', questions: [{
    question: 'Q?', type: 'multi', points: 1, options: ['A', 'B'], correct: [0], explanation: 'why',
  }] });
  assert.equal(multi.ok, true);
  assert.deepEqual(multi.structuralErrors, []);
  assert.deepEqual(multi.advisories, ['Q1: type="multi" has only 1 correct answer; consider "single"']);
  assert.equal(multi.stats.typeMismatch, 1);
});

test('aggregate bias uses strict thresholds and suppresses aggregate advisories after structural errors', () => {
  const build = (correctIndices, longestIndices = []) => correctIndices.map((correct, index) => ({
    question: `Q${index + 1}?`, type: 'single', points: 1,
    options: longestIndices.includes(index) ? ['AAA', 'B', 'C'] : ['A', 'B', 'C'],
    correct: [correct], explanation: 'why',
  }));
  const atThreshold = validateLevelData({
    title: 'Fixture', questions: build([...Array(9).fill(0), ...Array(9).fill(1), 2, 2]),
  });
  const boundary = atThreshold;
  assert.deepEqual(boundary.advisories.filter((advisory) => advisory.startsWith('BIAS:')), [
    'BIAS: correct answer is longest in 20/20 questions',
  ]);
  assert.deepEqual(boundary.structuralErrors, []);

  const acrossPositionBoundary = validateLevelData({
    title: 'Fixture', questions: build([...Array(10).fill(0), ...Array(8).fill(1), 2, 2]),
  });
  assert.deepEqual(acrossPositionBoundary.advisories.filter((advisory) => advisory.startsWith('BIAS:')), [
    'BIAS: correct answer is longest in 20/20 questions',
    'BIAS: correct answer is at index 0 in 10/20 answers',
  ]);

  const acrossLongestBoundary = validateLevelData({
    title: 'Fixture', questions: build([0, 1, 0, 1, 0, 1, 0, 1, 0, 1], [0, 1, 2, 3, 4, 5]),
  });
  assert.deepEqual(acrossLongestBoundary.advisories, [
    'Q1: correct is 3.0x longer than longest distractor',
    'Q3: correct is 3.0x longer than longest distractor',
    'Q5: correct is 3.0x longer than longest distractor',
    'BIAS: correct answer is longest in 7/10 questions',
    'BIAS: correct answer is at index 0 in 5/10 answers',
    'BIAS: correct answer is at index 1 in 5/10 answers',
  ]);

  const structurallyInvalid = validateLevelData({ title: 'Fixture', questions: [
    ...build([...Array(9).fill(0), ...Array(9).fill(1), 2, 2]),
    { question: 'Broken?', type: 'single', points: 1, options: ['A'], correct: [0], explanation: 'why' },
  ] });
  assert.deepEqual(structurallyInvalid.structuralErrors, ['Q21: needs at least 2 string options']);
  assert.equal(structurallyInvalid.advisories.some((advisory) => advisory.startsWith('BIAS:')), false);
  assert.deepEqual(structurallyInvalid.stats.correctIndexCounts, { 0: 9, 1: 9, 2: 2 });
});
