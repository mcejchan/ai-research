const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const { buildLevelsIndex } = require('./build-index');

function validLevel() {
  return {
    title: 'Fixture',
    questions: Array.from({ length: 5 }, (_, index) => ({
      question: `Question ${index}`,
      type: 'single',
      points: 1,
      options: ['The deliberately longest correct answer', 'No'],
      correct: [0],
      explanation: 'Fixture explanation',
    })),
  };
}

async function fixtureRoot() {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'quiz-publication-'));
  const sourceDir = path.join(root, 'levels');
  const indexPath = path.join(sourceDir, 'index.json');
  await fs.mkdir(sourceDir);
  return { root, sourceDir, indexPath };
}

test('malformed source fails without writing a partial index', async (t) => {
  const { root, sourceDir, indexPath } = await fixtureRoot();
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  await fs.writeFile(path.join(sourceDir, 'valid.json'), JSON.stringify(validLevel()));
  await fs.writeFile(path.join(sourceDir, 'broken.json'), '{');

  await assert.rejects(buildLevelsIndex(sourceDir, indexPath), /broken\.json/);
  await assert.rejects(fs.access(indexPath), { code: 'ENOENT' });
});

test('schema-invalid source fails publication', async (t) => {
  const { root, sourceDir, indexPath } = await fixtureRoot();
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  await fs.writeFile(
    path.join(sourceDir, 'invalid.json'),
    JSON.stringify({ title: 'Invalid', questions: 'no' }),
  );

  await assert.rejects(buildLevelsIndex(sourceDir, indexPath), /questions/);
  await assert.rejects(fs.access(indexPath), { code: 'ENOENT' });
});

test('bias findings warn but do not block publication', async (t) => {
  const { root, sourceDir, indexPath } = await fixtureRoot();
  const warnings = [];
  const originalWarn = console.warn;
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  t.after(() => { console.warn = originalWarn; });
  console.warn = (message) => warnings.push(String(message));
  await fs.writeFile(path.join(sourceDir, 'biased.json'), JSON.stringify(validLevel()));

  await assert.doesNotReject(buildLevelsIndex(sourceDir, indexPath));
  assert.ok(warnings.some((warning) => warning.includes('BIAS')));
  assert.equal(JSON.parse(await fs.readFile(indexPath, 'utf8')).length, 1);
});

test('Make and Pages use one quiz publication gate', async () => {
  const makefile = await fs.readFile(path.join(__dirname, '..', 'Makefile'), 'utf8');
  const workflow = await fs.readFile(
    path.join(__dirname, '..', '.github', 'workflows', 'deploy-quiz.yml'),
    'utf8',
  );

  assert.match(makefile, /^quiz-publication-check:/m);
  assert.match(workflow, /run: make quiz-publication-check/);
  assert.doesNotMatch(workflow, /node --test quiz\/build-index\.test\.js|node quiz\/build-index\.js/);
});
