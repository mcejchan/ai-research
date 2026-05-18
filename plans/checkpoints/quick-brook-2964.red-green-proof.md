# RED/GREEN Proof: quick-brook-2964

## RED Phase

Created before production code changes. Targeted test requirement: `cd quiz && node --test build-index.test.js` should fail before the missing planned test/export behavior is implemented or verified.

Command: `cd quiz && node --test build-index.test.js`

Result: failed as expected before production code changes because `buildLevelsIndex` was not exported.

```text
✖ buildLevelsIndex writes sorted static metadata and skips existing index
TypeError: buildLevelsIndex is not a function
ℹ pass 0
ℹ fail 1
```

## GREEN Phase

Command: `cd quiz && node --test build-index.test.js`

Result: passed after adding `buildLevelsIndex(levelsDir, indexPath)` and keeping the generator dependency-free.

```text
✔ buildLevelsIndex writes sorted static metadata and skips existing index (11.174417ms)
ℹ tests 1
ℹ suites 0
ℹ pass 1
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 80.377458
```

Additional focused verification:

```text
node --check quiz/build-index.js
node --check quiz/app.js
node --check quiz/server.js
node quiz/build-index.js
Wrote quiz/levels/index.json with 6 levels.
node -e "...validate generated quiz index..."
node -e "...validate level path guard..."
```
