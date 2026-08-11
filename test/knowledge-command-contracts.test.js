import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const readCommand = (name) => readFile(`.claude/commands/${name}.md`, 'utf8');

test('mindmap skips and reports transcript-only folders', async () => {
  const source = await readCommand('mindmap');
  assert.match(source, /<missing_analysis>/);
  assert.match(source, /analysis_main\.md/);
  assert.match(source, /skip/i);
  assert.match(source, /report/i);
  assert.match(source, /no eligible analysis/i);
});

test('kb-index includes transcript-only videos without broken links', async () => {
  const source = await readCommand('kb-index');
  assert.match(source, /<missing_analysis>/);
  assert.match(source, /analysis_main\.md/);
  assert.match(source, /include/i);
  assert.match(source, /without.*link/i);
  assert.match(source, /analysis unavailable/i);
});

test('expand-analysis stops before confirmation or file access when analysis is missing', async () => {
  const source = await readCommand('expand-analysis');
  assert.match(source, /<missing_analysis>/);
  assert.match(source, /analysis_main\.md/);
  assert.match(source, /report/i);
  assert.match(source, /stop before.*confirm/i);
  assert.match(source, /do not read or write/i);
});

test('flashcards handles missing analysis in direct and search modes', async () => {
  const source = await readCommand('flashcards');
  assert.match(source, /<missing_analysis>/);
  assert.match(source, /analysis_main\.md/);
  assert.match(source, /direct.*report.*stop/is);
  assert.match(source, /search.*skip.*report/is);
  assert.match(source, /no eligible analysis/i);
});
