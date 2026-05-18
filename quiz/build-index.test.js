const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const { buildLevelsIndex } = require('./build-index');

test('buildLevelsIndex writes sorted static metadata and skips existing index', async () => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'quiz-levels-'));
  const channelDir = path.join(root, 'futurecast');
  await fs.mkdir(channelDir, { recursive: true });
  await fs.writeFile(path.join(root, 'index.json'), JSON.stringify([{ path: 'stale.json' }]));
  await fs.writeFile(path.join(channelDir, 'old.json'), JSON.stringify({
    title: 'Old',
    channel: 'FutureCast',
    thumbnail: 'old.jpg',
    date: '2024-01-01',
    difficulty: 'easy',
    questions: [{ points: 1 }, { points: 2 }],
  }));
  await fs.writeFile(path.join(channelDir, 'new.json'), JSON.stringify({
    title: 'New',
    channel: 'FutureCast',
    thumbnail: 'new.jpg',
    date: '2026-05-18',
    difficulty: 'weird',
    questions: [{ points: 4 }],
  }));

  const levels = await buildLevelsIndex(root, path.join(root, 'index.json'));
  const written = JSON.parse(await fs.readFile(path.join(root, 'index.json'), 'utf8'));

  assert.deepEqual(levels.map((level) => level.path), ['futurecast/new.json', 'futurecast/old.json']);
  assert.deepEqual(written, levels);
  assert.equal(levels[0].difficulty, 'hard');
  assert.equal(levels[0].questionCount, 1);
  assert.equal(levels[0].maxPoints, 4);
  assert.equal(levels[1].difficulty, 'easy');
  assert.equal(levels[1].maxPoints, 3);
});
