// Restore @font-face declarations into the subsetted Font Awesome CSS.
// Background: the previous build used a subset script that stripped @font-face
// blocks. As a result, icons render as empty squares in production because
// the browser doesn't know where to load "Font Awesome 7 Free" fonts.
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const ORIGINAL = path.join(ROOT, 'node_modules/@fortawesome/fontawesome-free/css/all.min.css');
const TARGET = path.join(ROOT, 'public/fonts/fontawesome/all.min.css');

const orig = fs.readFileSync(ORIGINAL, 'utf8');
const subset = fs.readFileSync(TARGET, 'utf8');

if (subset.includes('@font-face')) {
    console.log('Subset already has @font-face — nothing to do.');
    process.exit(0);
}

const fontFaces = orig.match(/@font-face\{[^}]+\}/g) || [];
if (fontFaces.length === 0) {
    console.error('No @font-face blocks found in original. Aborting.');
    process.exit(1);
}

// Keep only the families we actually use: Free (regular+solid), Brands.
// The @font-face URLs in original use `../webfonts/fa-*.woff2` which resolves
// to `/fonts/webfonts/fa-*.woff2` from `/fonts/fontawesome/all.min.css`. Good.
const keep = fontFaces.filter((ff) => {
    // Drop -v4compatibility unless we need it; keep Free and Brands main weights.
    return /fa-(solid-900|regular-400|brands-400|v4compatibility)\.woff2/.test(ff);
});

console.log('Keeping', keep.length, 'of', fontFaces.length, '@font-face blocks');

const newCss = keep.join('\n') + '\n' + subset;
fs.writeFileSync(TARGET, newCss);
console.log('Wrote', TARGET, '(size:', newCss.length, 'bytes)');
