const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const LEVELS_DIR = path.join(ROOT, 'levels');
const INDEX_PATH = path.join(LEVELS_DIR, 'index.json');

async function walkJsonFiles(dir) {
  const entries = await fs.promises.readdir(dir, { withFileTypes: true }).catch((error) => {
    if (error.code === 'ENOENT') return [];
    throw error;
  });
  const files = [];

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...await walkJsonFiles(fullPath));
    } else if (entry.isFile() && entry.name.endsWith('.json') && fullPath !== INDEX_PATH) {
      files.push(fullPath);
    }
  }

  return files;
}

function levelFromJson(file, data) {
  const questions = Array.isArray(data.questions) ? data.questions : [];
  const maxPoints = questions.reduce((total, question) => total + Number(question.points || 0), 0);
  const relativePath = path.relative(LEVELS_DIR, file).split(path.sep).join('/');
  const difficulty = data.difficulty === 'easy' ? 'easy' : 'hard';

  return {
    path: relativePath,
    title: data.title || 'Untitled Level',
    channel: data.channel || 'Unknown Channel',
    thumbnail: data.thumbnail || '',
    date: data.date || '',
    difficulty,
    questionCount: questions.length,
    maxPoints,
  };
}

async function buildIndex() {
  const files = await walkJsonFiles(LEVELS_DIR);
  const levels = [];

  for (const file of files) {
    try {
      const raw = await fs.promises.readFile(file, 'utf8');
      levels.push(levelFromJson(file, JSON.parse(raw)));
    } catch (error) {
      console.warn(`Skipping invalid level ${file}: ${error.message}`);
    }
  }

  levels.sort((a, b) => (b.date || '').localeCompare(a.date || '') || a.path.localeCompare(b.path));
  await fs.promises.mkdir(LEVELS_DIR, { recursive: true });
  await fs.promises.writeFile(INDEX_PATH, `${JSON.stringify(levels, null, 2)}\n`);
  return levels;
}

if (require.main === module) {
  buildIndex()
    .then((levels) => {
      console.log(`Wrote ${path.relative(process.cwd(), INDEX_PATH)} with ${levels.length} levels.`);
    })
    .catch((error) => {
      console.error(error);
      process.exitCode = 1;
    });
}

module.exports = { buildIndex, levelFromJson };
