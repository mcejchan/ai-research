# AI Research

Live quiz dashboard: https://mcejchan.github.io/ai-research/

The quiz is deployed to GitHub Pages from the `quiz/` Actions artifact. The Pages source should be set to GitHub Actions, not a branch subfolder.

## Repository Health

Run the authoritative repository test gate from the project root:

```bash
make test
```

The gate runs the quiz tests, yt-viewer tests, and YouTube transcript pipeline pytest suite in order. It stops and returns non-zero if any subsystem fails.

Quiz publication has a focused contract used locally and by GitHub Pages:

```bash
make quiz-publication-check
```

This command structurally validates every source level, rebuilds `quiz/levels/index.json` without skipping invalid files, and tests the static runtime/index integration. Schema, read, and parse failures block publication; content-quality and bias findings are advisory warnings only.

Quiz level difficulty supports `extra-easy`, `easy`, and `hard`. Missing or unknown values default to `hard` when the levels index is built.
