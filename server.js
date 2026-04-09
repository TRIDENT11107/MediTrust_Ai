const express = require("express");
const path = require("path");
const fs = require("fs");
const { createProxyMiddleware } = require("http-proxy-middleware");

const app = express();
const PORT = process.env.PORT || 5173;
const API_TARGET = process.env.API_TARGET || "http://localhost:3000";

const reactDistDir = path.join(__dirname, "meditrust-ai-react", "dist");
const legacyFrontendDir = path.join(__dirname, "Frontend");
const frontendDir = fs.existsSync(reactDistDir) ? reactDistDir : legacyFrontendDir;

app.use(
    ["/api", "/static"],
    createProxyMiddleware({
        target: API_TARGET,
        changeOrigin: true,
        onError(_error, _req, res) {
            if (!res.headersSent) {
                res.writeHead(502, { "Content-Type": "text/plain" });
            }
            res.end(`Backend unreachable. Start the API service at ${API_TARGET}.`);
        },
    })
);

app.use(express.static(frontendDir));

app.get("*", (_req, res) => {
    res.sendFile(path.join(frontendDir, "index.html"));
});

app.listen(PORT, () => {
    console.log(`Frontend server on http://localhost:${PORT}`);
    console.log(`Serving frontend from ${frontendDir}`);
    console.log(`Proxying /api and /static to ${API_TARGET}`);
});
