.PHONY: help download test

help:
	@echo "YouTube Transcript Pipeline"
	@echo ""
	@echo "Available commands:"
	@echo "  make download url='URL'  - Download and process YouTube video"
	@echo "  make test                - Run tests"
	@echo "  make help                - Show this help message"

download:
	python -m src.yt_pipeline --url "$(url)"

test:
	pytest
