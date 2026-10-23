const assert = require('node:assert/strict');
const test = require('node:test');

const { renderLevelCards, filterLevels, evaluateAnswer, createQuizSession } = require('./quiz-page-logic');
const { levelUrl, initQuizPage } = require('./app');

test('quiz controller exposes its production initialization boundary for characterization', () => {
  assert.equal(typeof initQuizPage, 'function');
});

test('levels filter, count, cards, badges and external text are rendered safely', () => {
  const levels = [
    { path: 'channel/a.json', title: '<A>', channel: 'C & D', difficulty: 'easy', questionCount: 2, maxPoints: 3, date: '2026', thumbnail: 'https://example.test/a&b', },
    { path: 'channel/b.json', title: 'B', difficulty: 'hard', questionCount: 1, maxPoints: 1 },
  ];
  assert.deepEqual(filterLevels(levels, 'easy'), [levels[0]]);
  assert.deepEqual(filterLevels(levels, 'unknown'), []);
  const html = renderLevelCards([levels[0]], { 'channel/a.json': { best: 2, max: 3 } });
  assert.match(html, /&lt;A&gt;/);
  assert.match(html, /C &amp; D/);
  assert.match(html, /played-badge/);
  assert.match(html, /difficulty-easy/);
  assert.match(html, /channel%2Fa.json/);
  assert.doesNotMatch(html, /<A>/);
});

test('quiz session evaluates selections, reports no selection, advances and persists best only', () => {
  const stored = {};
  const session = createQuizSession({
    levelPath: 'c/l.json',
    questions: [
      { question: '<Q>', type: 'single', points: 2, options: ['<yes>', 'no'], correct: [0], explanation: '<why>' },
      { question: 'Multi', type: 'multi', points: 3, options: ['a', 'b'], correct: [0, 1] },
    ],
    saveScore: (path, score, max) => {
      const previous = stored[path];
      if (!previous || score > previous.best) stored[path] = { best: score, max };
      return stored[path];
    },
  });
  assert.equal(session.submit([]).message, 'Vyber alespoň jednu odpověď.');
  assert.deepEqual(session.submit([0]), { correct: true, earned: 2, max: 2, correctIndexes: [0], feedback: 'Správně. +2 bodů.', explanation: '<why>' });
  assert.equal(session.progress().status, '2/5 pts');
  session.next();
  assert.equal(session.submit([0, 1]).correct, true);
  const result = session.next();
  assert.equal(result.complete, true);
  assert.equal(result.score, 5);
  assert.equal(result.max, 5);
  assert.deepEqual(result.best, { best: 5, max: 5 });
  assert.equal(result.results.length, 2);
  assert.deepEqual(stored['c/l.json'], { best: 5, max: 5 });
});

test('levelUrl rejects traversal and schemes', () => {
  assert.throws(() => levelUrl('../bad.json'));
  assert.throws(() => levelUrl('https://example.test/a.json'));
});
