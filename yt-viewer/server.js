const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = Number(process.env.PORT) || 4001;
const ROOT = path.join(__dirname, "..", "local-knowledge-base", "youtube");

const send = (res, status, body, type = "text/plain; charset=utf-8") => {
  res.writeHead(status, { "Content-Type": type });
  res.end(body);
};

const json = (res, data) =>
  send(res, 200, JSON.stringify(data), "application/json; charset=utf-8");

const safeName = (n) => !n || n.includes("..") || n.includes("/") || n.includes("\\") ? null : n;

const isDir = async (p) => {
  try { return (await fs.promises.stat(p)).isDirectory(); } catch { return false; }
};

http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://${req.headers.host || "localhost"}`);
    if (req.method !== "GET") return send(res, 405, "Method not allowed");

    if (url.pathname === "/" || url.pathname === "/index.html") {
      const html = await fs.promises.readFile(path.join(__dirname, "index.html"), "utf8");
      return send(res, 200, html, "text/html; charset=utf-8");
    }

    if (url.pathname === "/api/channels") {
      const entries = await fs.promises.readdir(ROOT, { withFileTypes: true });
      const channels = [];
      for (const e of entries) {
        if (!e.isDirectory()) continue;
        const subs = await fs.promises.readdir(path.join(ROOT, e.name), { withFileTypes: true });
        channels.push({ name: e.name, videoCount: subs.filter(s => s.isDirectory()).length });
      }
      channels.sort((a, b) => a.name.localeCompare(b.name));
      return json(res, channels);
    }

    const chMatch = url.pathname.match(/^\/api\/channel\/([^/]+)$/);
    if (chMatch) {
      const ch = safeName(chMatch[1]);
      if (!ch) return send(res, 400, "Invalid channel");
      const dir = path.join(ROOT, ch);
      if (!(await isDir(dir))) return send(res, 404, "Not found");
      const entries = await fs.promises.readdir(dir, { withFileTypes: true });
      const videos = [];
      for (const e of entries) {
        if (!e.isDirectory()) continue;
        const m = e.name.match(/^(\d{4}-\d{2}-\d{2})_(.+)$/);
        const date = m ? m[1] : "";
        const title = m ? m[2] : e.name;
        const files = await fs.promises.readdir(path.join(dir, e.name));
        videos.push({
          folder: e.name, date, title,
          hasAnalysis: files.includes("analysis_main.md"),
          hasTranscript: files.includes("transcript_clean.txt"),
        });
      }
      videos.sort((a, b) => b.date.localeCompare(a.date));
      return json(res, videos);
    }

    const vidMatch = url.pathname.match(/^\/api\/video\/([^/]+)\/([^/]+)\/(analysis|transcript)$/);
    if (vidMatch) {
      const ch = safeName(vidMatch[1]);
      const folder = safeName(vidMatch[2]);
      const type = vidMatch[3];
      if (!ch || !folder) return send(res, 400, "Invalid path");
      const file = type === "analysis" ? "analysis_main.md" : "transcript_clean.txt";
      const content = await fs.promises.readFile(path.join(ROOT, ch, folder, file), "utf8");
      return send(res, 200, content);
    }

    return send(res, 404, "Not found");
  } catch (err) {
    if (err && err.code === "ENOENT") return send(res, 404, "Not found");
    return send(res, 500, "Internal server error");
  }
}).listen(PORT, () => console.log(`YT Viewer running on http://localhost:${PORT}`));
