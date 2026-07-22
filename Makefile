.PHONY: test

test:
	node --test quiz/build-index.test.js
	node --test yt-viewer/server.test.js
	cd youtube-transcript-pipeline && OPENAI_API_KEY=test_openai_key LANG=cs USE_WHISPER_FALLBACK=false MAKE_EMBEDDINGS=false DRIVE_FOLDER_ID=test_folder_id python3 -m pytest
