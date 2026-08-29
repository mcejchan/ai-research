.PHONY: test quiz-publication-check

test: quiz-publication-check
	node --test yt-viewer/server.test.js
	node --test test/knowledge-command-contracts.test.js
	cd youtube-transcript-pipeline && OPENAI_API_KEY=test_openai_key LANG=cs USE_WHISPER_FALLBACK=false MAKE_EMBEDDINGS=false DRIVE_FOLDER_ID=test_folder_id python3 -m pytest

quiz-publication-check:
	node --test quiz/build-index.test.js quiz/publication-check.test.js
	node quiz/build-index.js
