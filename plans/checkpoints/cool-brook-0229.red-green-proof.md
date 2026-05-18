# Red-Green Proof: cool-brook-0229

## RED Phase

Created before production code changes.

Expected current failure before implementation:
- `quiz/build-index.js` does not exist, so `node build-index.js` cannot generate `levels/index.json`.
- `quiz/app.js` still needs verification/update to avoid `/api/levels` for GitHub Pages static deployment.

## GREEN Phase

Focused quiz verification passed after implementation.

```text
$ cd /Users/michal/Projects/ai-research/quiz && node build-index.js
Wrote levels/index.json with 6 levels.

$ cd /Users/michal/Projects/ai-research/quiz && node -c app.js && node -c server.js && node -c build-index.js
(no output)

$ cd /Users/michal/Projects/ai-research/quiz && node -e "const fs=require('fs'); const levels=JSON.parse(fs.readFileSync('levels/index.json','utf8')); if (levels.length !== 6) throw new Error('expected 6 levels'); for (const level of levels) { for (const key of ['path','title','channel','thumbnail','date','difficulty','questionCount','maxPoints']) if (!(key in level)) throw new Error('missing '+key); if (!level.path.endsWith('.json')) throw new Error('bad path '+level.path); } const sorted=[...levels].sort((a,b)=>(b.date||'').localeCompare(a.date||'')||a.path.localeCompare(b.path)); if (JSON.stringify(levels)!==JSON.stringify(sorted)) throw new Error('levels not sorted newest first'); console.log('levels/index.json OK:', levels.length, 'levels');"
levels/index.json OK: 6 levels

$ grep equivalent: /api/ in quiz/app.js
No matches.
```

Broader project test status:

```text
$ cd /Users/michal/Projects/ai-research/youtube-transcript-pipeline && pytest
zsh:1: command not found: pytest

$ cd /Users/michal/Projects/ai-research/youtube-transcript-pipeline && python -m pytest
zsh:1: command not found: python

$ cd /Users/michal/Projects/ai-research/youtube-transcript-pipeline && DRIVE_FOLDER_ID=test python3 -m pytest
39 collected; 37 passed; 4 failed in test/test_llm_client.py.
Failures are unrelated to the quiz static deployment changes.
```
