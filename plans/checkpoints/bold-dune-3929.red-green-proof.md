# TDD Red-Green Proof: bold-dune-3929

<!-- proof-capture-metadata: {"version":1,"task_id":"bold-dune-3929","command":["sh","-c","node --test quiz/build-index.test.js; quiz_status=$?; (cd youtube-transcript-pipeline && python3 -m pytest test/test_config.py); python_status=$?; test \"$quiz_status\" -eq 0 -a \"$python_status\" -eq 0"],"command_sha256":"e01bf58ec545d25633f7df5d82f4b1c7f64cc0d93928014138588cb060054b4f"} -->

## RED Phase
- **Timestamp:** 2026-07-22T20:37:31.498113+00:00
- **Test command:** `sh -c 'node --test quiz/build-index.test.js; quiz_status=$?; (cd youtube-transcript-pipeline && python3 -m pytest test/test_config.py); python_status=$?; test "$quiz_status" -eq 0 -a "$python_status" -eq 0'`
- **Exit code:** 1

### Standard Output
````text
✖ buildLevelsIndex writes sorted static metadata and skips existing index (30.171791ms)
✔ quiz runtime is static and has no application server (1.500875ms)
ℹ tests 2
ℹ suites 0
ℹ pass 1
ℹ fail 1
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 101.742792

✖ failing tests:

test at quiz/build-index.test.js:10:1
✖ buildLevelsIndex writes sorted static metadata and skips existing index (30.171791ms)
  AssertionError [ERR_ASSERTION]: Expected values to be strictly deep-equal:
  + actual - expected
  
    {
      'Extra Easy': 'extra-easy',
      Easy: 'easy',
      Hard: 'hard',
  +   Unknown: 'weird'
  -   Unknown: 'hard'
    }
  
      at TestContext.<anonymous> (/Users/michal/Projects/ai-research/quiz/build-index.test.js:44:10)
      at async Test.run (node:internal/test_runner/test:1125:7)
      at async startSubtestAfterBootstrap (node:internal/test_runner/harness:358:3) {
    generatedMessage: true,
    code: 'ERR_ASSERTION',
    actual: { Hard: 'hard', 'Extra Easy': 'extra-easy', Easy: 'easy', Unknown: 'weird' },
    expected: { Hard: 'hard', 'Extra Easy': 'extra-easy', Easy: 'easy', Unknown: 'hard' },
    operator: 'deepStrictEqual',
    diff: 'simple'
  }
============================= test session starts ==============================
platform darwin -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/michal/Projects/ai-research/youtube-transcript-pipeline
configfile: pytest.ini
plugins: anyio-4.13.0
collected 1 item

test/test_config.py F                                                    [100%]

=================================== FAILURES ===================================
____________ test_pipeline_import_does_not_require_drive_folder_id _____________

    def test_pipeline_import_does_not_require_drive_folder_id():
        env = os.environ.copy()
        env.pop("DRIVE_FOLDER_ID", None)
        command = (
            "from unittest.mock import patch\n"
            "with patch('dotenv.load_dotenv', return_value=False):\n"
            "    import src.yt_pipeline\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", command],
            cwd=Path(__file__).resolve().parents[1],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
    
>       assert result.returncode == 0, result.stderr
E       AssertionError: Traceback (most recent call last):
E           File "<string>", line 3, in <module>
E             import src.yt_pipeline
E           File "/Users/michal/Projects/ai-research/youtube-transcript-pipeline/src/yt_pipeline.py", line 23, in <module>
E             DRIVE_FOLDER_ID = os.environ["DRIVE_FOLDER_ID"]
E                               ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
E           File "<frozen os>", line 709, in __getitem__
E         KeyError: 'DRIVE_FOLDER_ID'
E         
E       assert 1 == 0
E        +  where 1 = CompletedProcess(args=['/opt/homebrew/opt/python@3.14/bin/python3.14', '-c', "from unittest.mock import patch\nwith pa...       ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^\n  File "<frozen os>", line 709, in __getitem__\nKeyError: \'DRIVE_FOLDER_ID\'\n').returncode

test/test_config.py:24: AssertionError
=========================== short test summary info ============================
FAILED test/test_config.py::test_pipeline_import_does_not_require_drive_folder_id
============================== 1 failed in 1.42s ===============================
````

### Standard Error
````text

````

## GREEN Phase
- **Timestamp:** 2026-07-22T20:38:24.671105+00:00
- **Test command:** `sh -c 'node --test quiz/build-index.test.js; quiz_status=$?; (cd youtube-transcript-pipeline && python3 -m pytest test/test_config.py); python_status=$?; test "$quiz_status" -eq 0 -a "$python_status" -eq 0'`
- **Exit code:** 0

### Standard Output
````text
✔ buildLevelsIndex writes sorted static metadata and skips existing index (10.815458ms)
✔ quiz runtime is static and has no application server (0.891583ms)
ℹ tests 2
ℹ suites 0
ℹ pass 2
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 74.056667
============================= test session starts ==============================
platform darwin -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/michal/Projects/ai-research/youtube-transcript-pipeline
configfile: pytest.ini
plugins: anyio-4.13.0
collected 1 item

test/test_config.py .                                                    [100%]

============================== 1 passed in 1.20s ===============================
````

### Standard Error
````text

````
