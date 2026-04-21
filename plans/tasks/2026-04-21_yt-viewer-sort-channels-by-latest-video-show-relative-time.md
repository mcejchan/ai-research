# YT Viewer: Sort channels by latest video, show relative time

## Problem
Channels in sidebar are sorted alphabetically. Should be sorted by most recent video (newest first), with relative timestamp like "2 days ago" shown next to each channel.

## Changes

### `yt-viewer/server.js` — `GET /api/channels`
- For each channel dir, find the newest subdirectory (by date prefix `YYYY-MM-DD_` in folder name)
- Return `{name, videoCount, latestDate}` where `latestDate` is ISO date string from the newest video folder's prefix
- Sort response array by `latestDate` descending (newest first)

### `yt-viewer/index.html` — sidebar rendering
- Show relative time next to each channel (e.g. "2 days ago", "3 weeks ago", "today")
- Compute relative time client-side from `latestDate`
- Keep channel name + video count, add the relative time below or beside the count

## Verify
```bash
curl -s http://localhost:4001/api/channels | python3 -c "import json,sys; channels=json.load(sys.stdin); print(channels[0]['name'], channels[0]['latestDate'])"
```
First channel should be the one with the most recent video.

## DO NOT
- Change video list sorting (already newest first)
- Add npm dependencies
- Break existing functionality
