# Plan 2026-04-21: YT Viewer: Sort channels by latest video, show relative time

Extend the channel API with newest-video metadata, sort the sidebar by that metadata, and render a small client-side relative timestamp without changing the existing video list behavior.

*Vytvoreno: 2026-04-21*
*Status: DRAFT*

---

## Progress

- [x] Faze 0: Config + Init
- [x] Faze 1: Research
- [x] Faze 2: Knowledge
- [x] Faze 3: Synthesis

## Problem

Channel list currently sorts alphabetically. The API should expose each channel's newest video date from the `YYYY-MM-DD_` folder prefix, sort channels by that date descending, and the sidebar should show a relative label such as `today` or `2 days ago` next to each channel.

## Available Skills

- `recall-knowledge`: pull repo learnings before finalizing implementation steps.
- `tdd`: follow for RED/GREEN evidence if the targeted `node:test` file is added.
- `validate-implementation`: optional post-implementation check against task scope.
- `save-learning`: run after task completion to persist new learnings.

## Analysis

### Kontext z codebase

- `yt-viewer/server.js:32-41` currently builds `/api/channels` from channel directories, counts child directories, then sorts alphabetically; this is the only place that must start deriving and sorting by `latestDate`.
- `yt-viewer/server.js:44-65` already parses video folder names with `^(\d{4}-\d{2}-\d{2})_(.+)$` and sorts videos by descending ISO date string; reuse the same folder-prefix convention for channel metadata instead of introducing a second date format.
- `yt-viewer/index.html:334-343` renders the sidebar directly from `/api/channels`; this is the only client callsite that needs to consume `latestDate`.
- `yt-viewer/index.html:263-397` is a single inline script with cached fetches and no module/build step; keep the change as a small helper near `loadChannels()` instead of adding new dependencies or framework structure.
- Sample data under `local-knowledge-base/youtube/<channel>/` already uses date-prefixed folders such as `2026-01-28_ai-is-scaling-faster-than-anyone-expected/`, so lexicographic comparison on `YYYY-MM-DD` is sufficient.

### Relevantni dokumentace

- `CLAUDE.md` confirms this repo has no special frontend build workflow for `yt-viewer`; keep changes minimal and do not add dependencies.
- No `yt-viewer`-specific README, docs, or PlantUML diagrams were found, so the plan should follow existing code patterns in `server.js` and `index.html` directly.

### Knowledge base

**Patterns:**
- `learnings/patterns/bright-vale-3672-zero-dependency-node-file-viewer-can-stay-simple-and-safe.md`: preserve the current zero-dependency Node HTTP server shape, rely on `URL` parsing and `fs.promises.readdir(..., { withFileTypes: true })`, and avoid unnecessary framework refactors.
- `learnings/patterns/zero-dep-nodejs-file-viewer.md`: keep route logic precise and prefer lightweight client caching over extra infrastructure.

**Rules:**
- `learnings/tooling/fresh-wave-2930-use-runtime-endpoint-checks-when-a-small-viewer-has-no-build-pipeline.md`: verification should be runtime-based for this app: syntax check inline JS separately if needed, then validate `/api/channels` and a representative browser flow over HTTP.
- `learnings/tooling/bright-vale-3672-verify-test-tooling-exists-before-running-unrelated-suite.md`: do not treat missing repo-wide Python tooling as relevant to this Node-only viewer task.

## Solutions

- In `/api/channels`, scan only subdirectories, extract valid `YYYY-MM-DD` prefixes, keep the max date per channel as `latestDate`, and return `null` when no dated video folder exists.
- Sort channels by `latestDate` descending with a stable fallback to `name.localeCompare(...)` when dates are equal or missing, so channels with undated folders do not float above active ones.
- In the sidebar renderer, add a tiny `formatRelativeDate(latestDate, now = new Date())` helper that converts ISO dates to labels like `today`, `2 days ago`, or `3 weeks ago`; render it next to or under the existing count without changing click targets.
- Keep `GET /api/channel/:name` untouched so video list sorting remains newest-first as required.

## Implementation

### Pre-implementation checklist

- [ ] Confirm `local-knowledge-base/youtube/<channel>/<date>_<slug>/` remains the source of truth for latest activity.
- [ ] Keep `/api/channels` backwards-compatible for existing fields: `name` and `videoCount` stay present.
- [ ] Avoid npm/package changes and avoid altering `/api/channel/:name` sorting.

### Kroky implementace

1. Update `yt-viewer/server.js` so `/api/channels` derives `latestDate` from dated subdirectory names while counting all video directories as before.
2. Sort the returned channel objects by `latestDate` descending, then by channel name for deterministic ties; leave channels with missing dates at the end.
3. Update `yt-viewer/index.html` to render channel name, count, and a relative-time label from `latestDate` using a small client-side helper.
4. Adjust sidebar markup/CSS only enough to fit the extra timestamp cleanly on desktop and mobile without changing selection behavior.
5. Verify the endpoint response and sidebar rendering through runtime checks, including the user-provided `curl` assertion that the first channel is the most recent one.

## Files to Modify

| Soubor | Zmena |
|--------|-------|
| `yt-viewer/server.js` | Add `latestDate` derivation in `/api/channels` and sort channels by newest dated folder. |
| `yt-viewer/index.html` | Add relative-time formatter, render `latestDate` in sidebar, and make minimal CSS/layout adjustments for the extra metadata. |
| `yt-viewer/server.test.js` | Add a focused `node:test` regression around `/api/channels` ordering and `latestDate` shape if implementation introduces the test file. |

## TDD

**Workflow pro implementujiciho agenta:**

1. Create `yt-viewer/server.test.js` with the failing assertions below.
2. Run the targeted test command and confirm RED because `/api/channels` does not yet return `latestDate` or newest-first ordering.
3. Implement the server-side metadata and sorting changes.
4. Re-run the targeted test to reach GREEN.
5. Perform runtime verification for the inline client change against the live endpoint.

> Implementace TDD cyklu dle skill:tdd - RED/GREEN evidence se zapisuje do `plans/checkpoints/bright-crag-4248.red-green-proof.md`.

### Targeted Tests

**Test file:** `yt-viewer/server.test.js`
**Framework:** `node:test` using built-in `assert` and `child_process`, because `yt-viewer` has no existing package/test dependency setup.
**Run command:** `node --test yt-viewer/server.test.js`
**Edit hint:** `NEW FILE`

```js
import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';

const BASE_URL = 'http://127.0.0.1:4011';

test('GET /api/channels returns newest channel first with latestDate', async (t) => {
  const server = spawn(process.execPath, ['yt-viewer/server.js'], {
    env: { ...process.env, PORT: '4011' },
    stdio: 'ignore',
  });

  t.after(() => server.kill());

  await new Promise((resolve) => setTimeout(resolve, 500));
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
```

| Test | RED (pred impl) | GREEN (po impl) |
|------|------------------|-----------------|
| `GET /api/channels returns newest channel first with latestDate` | `channels[0].latestDate` assertion fails or ordering assertion fails because response is alphabetical | Response includes ISO `latestDate` and list is sorted descending by newest video date |

### Regression

- [ ] `node --check yt-viewer/server.js`
- [ ] `node --test yt-viewer/server.test.js`
- [ ] `curl -s http://localhost:4001/api/channels | python3 -c "import json,sys; channels=json.load(sys.stdin); print(channels[0]['name'], channels[0]['latestDate'])"`
- [ ] Browser/manual check: sidebar shows relative labels and channel selection still loads the same video lists/content.

## Dependencies

- Existing folder naming convention `YYYY-MM-DD_<slug>` inside `local-knowledge-base/youtube/<channel>/`.
- Built-in Node features only: `fs.promises`, `node:test`, `assert`, and browser `Date`/`Intl` APIs.
- Final task completion must end with the `save-learning` skill, per the task instructions.
