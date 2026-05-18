// Generate critical CSS for home and inline it.
// Usage: node scripts/gen_critical_home.js
// Requires: npm i -D critical  (already installed)

import path from 'path';
import { fileURLToPath } from 'url';
import { generate } from 'critical';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

(async () => {
    const base = path.resolve(__dirname, '..', 'public');
    try {
        const result = await generate({
            base,
            src: 'index.html',
            target: { html: 'index.critical.html', css: 'css/critical-home.css' },
            inline: true,
            extract: false,
            width: 412,
            height: 915,
            penthouse: { timeout: 60000 },
        });
        console.log('Critical CSS size:', result.css.length, 'bytes');
        console.log('HTML output: public/index.critical.html');
        console.log('CSS output:  public/css/critical-home.css');
    } catch (e) {
        console.error('critical failed:', e.message);
        process.exit(1);
    }
})();
