const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5173;

app.use(express.static('.'));
app.get('/', (_req, res) => {
	// Try a list of candidate index files (prefer React apps if present)
	const candidates = [
		path.join(__dirname, 'meditrust-ai-react', 'index.html'),
		path.join(__dirname, 'MediTrust_Ai', 'index.html'),
		path.join(__dirname, 'index.html'),
		path.join(__dirname, 'index_1.html'),
			// 'trial.html' intentionally excluded: it is unrelated to the main app
	];
	const fs = require('fs');
	for (const c of candidates) {
		if (fs.existsSync(c)) {
			if (c !== path.join(__dirname, 'index.html')) console.warn(`Serving ${c} as index`);
			return res.sendFile(c);
		}
	}
	// If none found
	res.status(404).send('No index file found in expected locations. Check meditrust-ai-react/index.html or root index.html');
});

app.listen(PORT, () => console.log(`Static server on http://localhost:${PORT}`));
