const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const LEVELS_DIR = path.join(ROOT, 'levels');
const INDEX_PATH = path.join(LEVELS_DIR, 'index.json');

async function walkJsonFiles(dir, indexPath = path.join(dir, 'index.json')) {
  const entries = await fs.promises.readdir(dir, { withFileTypes: true }).catch((error) => {
    if (error.code === 'ENOENT') return [];
    throw error;
  });
  const files = [];

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...await walkJsonFiles(fullPath, indexPath));
    } else if (entry.isFile() && entry.name.endsWith('.json') && fullPath !== indexPath) {
      files.push(fullPath);
    }
  }

  return files;
}

function levelFromJson(file, data, levelsDir = LEVELS_DIR) {
  const questions = Array.isArray(data.questions) ? data.questions : [];
  const maxPoints = questions.reduce((total, question) => total + Number(question.points || 0), 0);
  const relativePath = path.relative(levelsDir, file).split(path.sep).join('/');
  const difficulty = data.difficulty || 'hard';

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

async function buildLevelsIndex(levelsDir = LEVELS_DIR, indexPath = path.join(levelsDir, 'index.json')) {
  const files = await walkJsonFiles(levelsDir, indexPath);
  const levels = [];

  for (const file of files) {
    try {
      const raw = await fs.promises.readFile(file, 'utf8');
      levels.push(levelFromJson(file, JSON.parse(raw), levelsDir));
    } catch (error) {
      console.warn(`Skipping invalid level ${file}: ${error.message}`);
    }
  }

  levels.sort((a, b) => (b.date || '').localeCompare(a.date || '') || a.path.localeCompare(b.path));
  await fs.promises.mkdir(path.dirname(indexPath), { recursive: true });
  await fs.promises.writeFile(indexPath, `${JSON.stringify(levels, null, 2)}\n`);
  return levels;
}

if (require.main === module) {
  buildLevelsIndex(LEVELS_DIR, INDEX_PATH)
    .then((levels) => {
      console.log(`Wrote ${path.relative(process.cwd(), INDEX_PATH)} with ${levels.length} levels.`);
    })
    .catch((error) => {
      console.error(error);
      process.exitCode = 1;
    });
}

module.exports = { buildLevelsIndex };
