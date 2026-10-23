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
