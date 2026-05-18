const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 4002;
const ROOT = __dirname;
const LEVELS_DIR = path.join(ROOT, 'levels');

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
};

function sendJson(res, status, data) {
  const body = JSON.stringify(data);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
  });
  res.end(body);
}

function sendError(res, status, message) {
  sendJson(res, status, { error: message });
}

function safeLevelPath(rawPath) {
  if (!rawPath || rawPath.includes('\\')) return null;
  const normalized = path.normalize(rawPath);
  if (normalized.startsWith('..') || path.isAbsolute(normalized) || !normalized.endsWith('.json')) {
    return null;
  }
  return normalized;
}

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
    } else if (entry.isFile() && entry.name.endsWith('.json')) {
      files.push(fullPath);
    }
  }

  return files;
}

async function getLevels() {
  const files = await walkJsonFiles(LEVELS_DIR);
  const levels = [];

  for (const file of files) {
    try {
      const raw = await fs.promises.readFile(file, 'utf8');
      const data = JSON.parse(raw);
      const questions = Array.isArray(data.questions) ? data.questions : [];
      const maxPoints = questions.reduce((total, question) => total + Number(question.points || 0), 0);
      const relativePath = path.relative(LEVELS_DIR, file).split(path.sep).join('/');
      const difficulty = data.difficulty === 'easy' ? 'easy' : 'hard';

      levels.push({
        path: relativePath,
        title: data.title || 'Untitled Level',
        channel: data.channel || 'Unknown Channel',
        thumbnail: data.thumbnail || '',
        date: data.date || '',
        difficulty,
        questionCount: questions.length,
        maxPoints,
      });
    } catch (error) {
      console.warn(`Skipping invalid level ${file}: ${error.message}`);
    }
  }

  return levels.sort((a, b) => (b.date || '').localeCompare(a.date || ''));
}

async function handleApi(req, res, url) {
  if (url.pathname === '/api/levels') {
    sendJson(res, 200, await getLevels());
    return;
  }

  if (url.pathname === '/api/level') {
    const levelPath = safeLevelPath(url.searchParams.get('path'));
    if (!levelPath) {
      sendError(res, 400, 'Invalid level path');
      return;
    }

    const filePath = path.join(LEVELS_DIR, levelPath);
    try {
      const raw = await fs.promises.readFile(filePath, 'utf8');
      JSON.parse(raw);
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(raw);
    } catch (error) {
      if (error.code === 'ENOENT') {
        sendError(res, 404, 'Level not found');
        return;
      }
      sendError(res, 500, 'Could not read level');
    }
    return;
  }

  sendError(res, 404, 'API endpoint not found');
}

function serveStatic(req, res, url) {
  const requestPath = decodeURIComponent(url.pathname === '/' ? '/index.html' : url.pathname);
  const normalized = path.normalize(requestPath).replace(/^[/\\]+/, '');
  const filePath = path.join(ROOT, normalized);

  if (!filePath.startsWith(ROOT) || normalized.startsWith('levels')) {
    res.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('Forbidden');
    return;
  }

  fs.readFile(filePath, (error, data) => {
    if (error) {
      res.writeHead(error.code === 'ENOENT' ? 404 : 500, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end(error.code === 'ENOENT' ? 'Not found' : 'Server error');
      return;
    }

    const contentType = MIME_TYPES[path.extname(filePath).toLowerCase()] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(data);
  });
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);

  if (url.pathname.startsWith('/api/')) {
    handleApi(req, res, url).catch((error) => {
      console.error(error);
      sendError(res, 500, 'Internal server error');
    });
    return;
  }

  serveStatic(req, res, url);
});

server.listen(PORT, () => {
  console.log(`YT Knowledge Quiz running at http://localhost:${PORT}`);
});
