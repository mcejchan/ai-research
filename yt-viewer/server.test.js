import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const BASE_URL = 'http://127.0.0.1:4011';

async function waitForServer(url, attempts = 20) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      const res = await fetch(url);
      if (res.ok) return;
    } catch {}
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error(`Server did not start at ${url}`);
}

test('GET /api/channels returns newest channel first with latestDate', async (t) => {
  const server = spawn(process.execPath, ['yt-viewer/server.js'], {
    env: { ...process.env, PORT: '4011' },
    stdio: 'ignore',
  });

  t.after(() => server.kill());

  await waitForServer(`${BASE_URL}/api/channels`);
  const res = await fetch(`${BASE_URL}/api/channels`);
  const channels = await res.json();

  assert.equal(res.status, 200);
  assert.ok(Array.isArray(channels));
  assert.ok(channels[0].latestDate, 'RED: latestDate is currently missing');
  assert.match(channels[0].latestDate, /^\d{4}-\d{2}-\d{2}$/);
  assert.ok(
    channels.every((channel, index, arr) =>
      index === 0 || (arr[index - 1].latestDate ?? '') >= (channel.latestDate ?? '')
    ),
    'RED: channels are currently sorted alphabetically instead of newest-first'
  );
});

test('transcript-only video reports analysis unavailable', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'yt-viewer-'));
  const channel = 'transcript-only-channel';
  const folder = '2026-08-11_transcript-only-video';
  const videoDir = join(root, channel, folder);
  await mkdir(videoDir, { recursive: true });
  await writeFile(join(videoDir, 'transcript_clean.txt'), 'Captured transcript', 'utf8');

  const port = '4012';
  const baseUrl = `http://127.0.0.1:${port}`;
  const server = spawn(process.execPath, ['yt-viewer/server.js'], {
    env: { ...process.env, PORT: port, YT_KB_ROOT: root },
    stdio: 'ignore',
  });

  t.after(async () => {
    server.kill();
    await rm(root, { recursive: true, force: true });
  });

  await waitForServer(`${baseUrl}/api/channels`);
  const listing = await fetch(`${baseUrl}/api/channel/${channel}`);
  const videos = await listing.json();
  assert.equal(listing.status, 200);
  assert.deepEqual(videos, [{
    folder,
    date: '2026-08-11',
    title: 'transcript-only-video',
    hasAnalysis: false,
    hasTranscript: true,
  }]);

  const analysis = await fetch(`${baseUrl}/api/video/${channel}/${folder}/analysis`);
  assert.equal(analysis.status, 404);
  assert.equal(await analysis.text(), 'Not found');
});
