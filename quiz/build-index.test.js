const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const { levelUrl } = require('./app');
const { buildLevelsIndex } = require('./build-index');

test('buildLevelsIndex writes sorted static metadata and skips existing index', async () => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'quiz-levels-'));
  const channelDir = path.join(root, 'futurecast');
  await fs.mkdir(channelDir, { recursive: true });
  await fs.writeFile(path.join(root, 'index.json'), JSON.stringify([{ path: 'stale.json' }]));
  await fs.writeFile(path.join(channelDir, 'hard.json'), JSON.stringify({
    title: 'Hard',
    date: '2026-01-03',
    difficulty: 'hard',
    questions: [],
  }));
  await fs.writeFile(path.join(channelDir, 'extra-easy.json'), JSON.stringify({
    title: 'Extra Easy',
    date: '2026-01-02',
    difficulty: 'extra-easy',
    questions: [],
  }));
  await fs.writeFile(path.join(channelDir, 'easy.json'), JSON.stringify({
    title: 'Easy',
    date: '2026-01-01',
    difficulty: 'easy',
    questions: [],
  }));
  await fs.writeFile(path.join(channelDir, 'unknown.json'), JSON.stringify({
    title: 'Unknown',
    date: '2025-01-01',
    difficulty: 'weird',
    questions: [{ points: 4 }],
  }));

  const levels = await buildLevelsIndex(root, path.join(root, 'index.json'));
  const written = JSON.parse(await fs.readFile(path.join(root, 'index.json'), 'utf8'));

  assert.deepEqual(written, levels);
  assert.deepEqual(
    Object.fromEntries(levels.map(({ title, difficulty }) => [title, difficulty])),
    { Hard: 'hard', 'Extra Easy': 'extra-easy', Easy: 'easy', Unknown: 'hard' },
  );
  assert.equal(levels.find(({ title }) => title === 'Unknown').questionCount, 1);
  assert.equal(levels.find(({ title }) => title === 'Unknown').maxPoints, 4);
});

test('quiz runtime is static and has no application server', async () => {
  const appSource = await fs.readFile(path.join(__dirname, 'app.js'), 'utf8');

  await assert.rejects(
    fs.access(path.join(__dirname, 'server.js')),
    { code: 'ENOENT' },
  );
  assert.match(appSource, /fetchJson\('levels\/index\.json'\)/);
  assert.doesNotMatch(appSource, /\/api\/levels?\b/);
  assert.equal(levelUrl('channel/level.json'), 'levels/channel/level.json');
});
