.PHONY: test quiz-publication-check

test: quiz-publication-check
	node --test yt-viewer/server.test.js
	node --test test/knowledge-command-contracts.test.js
	@project_root="$$(pwd -P)"; runtime="$$project_root/.venv/bin/python"; \
	if [ ! -x "$$runtime" ]; then \
	  printf 'Required project interpreter missing: %s (expected CPython 3.15.x). Provision the project .venv first.\n' "$$runtime" >&2; exit 1; \
	fi; \
	identity="$$("$$runtime" -c 'import platform,sys; print(platform.python_implementation()+" "+platform.python_version())' 2>&1)" || { printf 'Unable to inspect required project interpreter %s: %s\n' "$$runtime" "$$identity" >&2; exit 1; }; \
	patch=""; case "$$identity" in 'CPython 3.15.'*) patch="$${identity#CPython 3.15.}" ;; esac; \
	case "$$patch" in ''|*[!0-9]*) \
	  printf 'Invalid project interpreter %s: expected CPython 3.15.x, got %s\n' "$$runtime" "$$identity" >&2; exit 1 ;; \
	esac; \
	cd youtube-transcript-pipeline && OPENAI_API_KEY=test_openai_key LANG=cs USE_WHISPER_FALLBACK=false MAKE_EMBEDDINGS=false DRIVE_FOLDER_ID=test_folder_id "$$runtime" -m pytest

quiz-publication-check:
	node --test quiz/build-index.test.js quiz/publication-check.test.js
	node quiz/build-index.js
