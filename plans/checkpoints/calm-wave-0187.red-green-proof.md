# TDD Red-Green Proof: calm-wave-0187

<!-- proof-capture-metadata: {"version":1,"task_id":"calm-wave-0187","command":["node","--test","--test-name-pattern=quiz runtime is static and has no application server","quiz/build-index.test.js"],"command_sha256":"f5adc2f33de65674f7d99ba16005852a81f6936ea01d14a655ae58db029f892e"} -->

## RED Phase
- **Timestamp:** 2026-07-21T21:19:10.054175+00:00
- **Test command:** `node --test '--test-name-pattern=quiz runtime is static and has no application server' quiz/build-index.test.js`
- **Exit code:** 1

### Standard Output
````text
✖ quiz runtime is static and has no application server (2.575667ms)
ℹ tests 1
ℹ suites 0
ℹ pass 0
ℹ fail 1
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 64.393541

✖ failing tests:

test at quiz/build-index.test.js:44:1
✖ quiz runtime is static and has no application server (2.575667ms)
  AssertionError [ERR_ASSERTION]: Missing expected rejection.
      at async TestContext.<anonymous> (/Users/michal/Projects/ai-research/quiz/build-index.test.js:47:3)
      at async Test.run (node:internal/test_runner/test:1125:7)
      at async startSubtestAfterBootstrap (node:internal/test_runner/harness:358:3) {
    generatedMessage: false,
    code: 'ERR_ASSERTION',
    actual: undefined,
    expected: { code: 'ENOENT' },
    operator: 'rejects',
    diff: 'simple'
  }
````

### Standard Error
````text

````

## GREEN Phase
- **Timestamp:** 2026-07-21T21:20:23.087015+00:00
- **Test command:** `node --test '--test-name-pattern=quiz runtime is static and has no application server' quiz/build-index.test.js`
- **Exit code:** 0

### Standard Output
````text
✔ quiz runtime is static and has no application server (3.371458ms)
ℹ tests 1
ℹ suites 0
ℹ pass 1
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 72.432417
````

### Standard Error
````text

````
