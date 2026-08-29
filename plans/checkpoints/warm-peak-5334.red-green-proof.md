# TDD Red-Green Proof: warm-peak-5334

<!-- proof-capture-metadata: {"version":1,"task_id":"warm-peak-5334","command":["node","--test","quiz/publication-check.test.js","quiz/build-index.test.js"],"command_sha256":"b52ee4e11459dd74353f2b5ec3be801604d14004d1b347fc14a1d3690b0f4b97"} -->

## RED Phase
- **Timestamp:** 2026-08-29T08:19:12.489143+00:00
- **Test command:** `node --test quiz/publication-check.test.js quiz/build-index.test.js`
- **Exit code:** 1

### Standard Output
````text
✔ buildLevelsIndex writes sorted static metadata and skips existing index (11.706917ms)
✔ quiz runtime is static and has no application server (1.389625ms)
Skipping invalid level /Users/michal/.openclaw/tmp/quiz-publication-H9GNs2/levels/broken.json: Expected property name or '}' in JSON at position 1 (line 1 column 2)
✖ malformed source fails without writing a partial index (5.736167ms)
✖ schema-invalid source fails publication (2.379209ms)
✖ bias findings warn but do not block publication (4.115542ms)
✖ Make and Pages use one quiz publication gate (1.194083ms)
ℹ tests 6
ℹ suites 0
ℹ pass 2
ℹ fail 4
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 56.202792

✖ failing tests:

test at quiz/publication-check.test.js:31:1
✖ malformed source fails without writing a partial index (5.736167ms)
  AssertionError [ERR_ASSERTION]: Missing expected rejection.
      at async TestContext.<anonymous> (/Users/michal/Projects/ai-research/quiz/publication-check.test.js:37:3)
      at async Test.run (node:internal/test_runner/test:1208:7)
      at async startSubtestAfterBootstrap (node:internal/test_runner/harness:385:3) {
    generatedMessage: false,
    code: 'ERR_ASSERTION',
    actual: undefined,
    expected: /broken\.json/,
    operator: 'rejects',
    diff: 'simple'
  }

test at quiz/publication-check.test.js:41:1
✖ schema-invalid source fails publication (2.379209ms)
  AssertionError [ERR_ASSERTION]: Missing expected rejection.
      at async TestContext.<anonymous> (/Users/michal/Projects/ai-research/quiz/publication-check.test.js:49:3)
      at async Test.run (node:internal/test_runner/test:1208:7)
      at async Test.processPendingSubtests (node:internal/test_runner/test:831:7) {
    generatedMessage: false,
    code: 'ERR_ASSERTION',
    actual: undefined,
    expected: /questions/,
    operator: 'rejects',
    diff: 'simple'
  }

test at quiz/publication-check.test.js:53:1
✖ bias findings warn but do not block publication (4.115542ms)
  AssertionError [ERR_ASSERTION]: The expression evaluated to a falsy value:
  
    assert.ok(warnings.some((warning) => warning.includes('BIAS')))
  
      at TestContext.<anonymous> (/Users/michal/Projects/ai-research/quiz/publication-check.test.js:63:10)
      at async Test.run (node:internal/test_runner/test:1208:7)
      at async Test.processPendingSubtests (node:internal/test_runner/test:831:7) {
    generatedMessage: true,
    code: 'ERR_ASSERTION',
    actual: false,
    expected: true,
    operator: '==',
    diff: 'simple'
  }

test at quiz/publication-check.test.js:67:1
✖ Make and Pages use one quiz publication gate (1.194083ms)
  AssertionError [ERR_ASSERTION]: The input did not match the regular expression /^quiz-publication-check:/m. Input:
  
  '.PHONY: test\n' +
    '\n' +
    'test:\n' +
    '\tnode --test quiz/build-index.test.js\n' +
    '\tnode --test yt-viewer/server.test.js\n' +
    '\tnode --test test/knowledge-command-contracts.test.js\n' +
    '\tcd youtube-transcript-pipeline && OPENAI_API_KEY=test_openai_key LANG=cs USE_WHISPER_FALLBACK=false MAKE_EMBEDDINGS=false DRIVE_FOLDER_ID=test_folder_id python3 -m pytest\n'
  
      at TestContext.<anonymous> (/Users/michal/Projects/ai-research/quiz/publication-check.test.js:74:10)
      at async Test.run (node:internal/test_runner/test:1208:7)
      at async Test.processPendingSubtests (node:internal/test_runner/test:831:7) {
    generatedMessage: true,
    code: 'ERR_ASSERTION',
    actual: '.PHONY: test\n\ntest:\n\tnode --test quiz/build-index.test.js\n\tnode --test yt-viewer/server.test.js\n\tnode --test test/knowledge-command-contracts.test.js\n\tcd youtube-transcript-pipeline && OPENAI_API_KEY=test_openai_key LANG=cs USE_WHISPER_FALLBACK=false MAKE_EMBEDDINGS=false DRIVE_FOLDER_ID=test_folder_id python3 -m pytest\n',
    expected: /^quiz-publication-check:/m,
    operator: 'match',
    diff: 'simple'
  }
````

### Standard Error
````text

````

## GREEN Phase
- **Timestamp:** 2026-08-29T08:21:57.545260+00:00
- **Test command:** `node --test quiz/publication-check.test.js quiz/build-index.test.js`
- **Exit code:** 0

### Standard Output
````text
✔ buildLevelsIndex writes sorted static metadata and skips existing index (14.319458ms)
✔ quiz runtime is static and has no application server (0.888625ms)
Advisory for /Users/michal/.openclaw/tmp/quiz-publication-tc15p2/levels/valid.json: Q1: correct is 19.5x longer than longest distractor
Advisory for /Users/michal/.openclaw/tmp/quiz-publication-tc15p2/levels/valid.json: Q2: correct is 19.5x longer than longest distractor
Advisory for /Users/michal/.openclaw/tmp/quiz-publication-tc15p2/levels/valid.json: Q3: correct is 19.5x longer than longest distractor
Advisory for /Users/michal/.openclaw/tmp/quiz-publication-tc15p2/levels/valid.json: Q4: correct is 19.5x longer than longest distractor
Advisory for /Users/michal/.openclaw/tmp/quiz-publication-tc15p2/levels/valid.json: Q5: correct is 19.5x longer than longest distractor
Advisory for /Users/michal/.openclaw/tmp/quiz-publication-tc15p2/levels/valid.json: BIAS: correct answer is longest in 5/5 questions
Advisory for /Users/michal/.openclaw/tmp/quiz-publication-tc15p2/levels/valid.json: BIAS: correct answer is at index 0 in 5/5 answers
Advisory for /Users/michal/.openclaw/tmp/quiz-publication-tc15p2/levels/valid.json: BIAS: correct answer is over 1.6x longer than the longest distractor in 5/5 questions
✔ malformed source fails without writing a partial index (6.720167ms)
✔ schema-invalid source fails publication (2.700459ms)
✔ bias findings warn but do not block publication (2.989458ms)
✔ Make and Pages use one quiz publication gate (0.645375ms)
ℹ tests 6
ℹ suites 0
ℹ pass 6
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 52.124625
````

### Standard Error
````text

````
