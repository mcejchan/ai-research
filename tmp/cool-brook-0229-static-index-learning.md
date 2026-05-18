# Static quiz apps need a generated manifest and static access to JSON

For a vanilla app deployed as static files, replace dynamic discovery endpoints like `/api/levels` with a committed/generated manifest such as `levels/index.json`.

Key implementation details:
- Generate the manifest from source JSON files with a Node script that uses `__dirname`, so it works from both repository root (`node quiz/build-index.js`) and the app directory (`node build-index.js`).
- Exclude the generated `levels/index.json` from the recursive scan to avoid indexing the manifest itself on later runs.
- Store level paths relative to the `levels/` directory, then fetch details with `levels/${path}` from the browser.
- If a local dev server previously blocked static access to `levels/`, remove that block or static verification through the server will fail even though GitHub Pages can serve the files.

This keeps local dev server/API compatibility while making the browser app independent from runtime Node APIs.
