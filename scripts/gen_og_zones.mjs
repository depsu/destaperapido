// Generate og:image cards (1200x630 JPG) for each zone page.
// Each card uses a base hero photo + dark overlay + zone-specific text + brand.
//
// Output: public/images/og-<slug>.jpg
//
// Strategy:
// 1. Take a base WebP (different for urbano vs rural).
// 2. Resize cover to 1200x630.
// 3. Composite a semi-transparent dark gradient overlay.
// 4. Composite an SVG with the zone name + service line + phone.

import sharp from 'sharp';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');
const PUBLIC = path.join(ROOT, 'public');
const IMG = path.join(PUBLIC, 'images');

const BASE_URBANO = path.join(IMG, 'Destape-alcantarillado-con-camion-en-subterraneo-de-edificio.webp');
const BASE_RURAL = path.join(IMG, 'camion-haciendo-destape-en-zona-rural.webp');

const ZONES = [
    // [slug, displayName, kind, secondary]
    ['lampa', 'Lampa', 'rural', 'Limpieza de fosas certificada'],
    ['talagante', 'Talagante', 'rural', 'Destape y fosas en parcelas'],
    ['isla-de-maipo', 'Isla de Maipo', 'rural', 'Servicio en viñas y campos'],
    ['colina', 'Colina', 'rural', 'Hidrojet en campos y bodegas'],
    ['buin-paine', 'Buin / Paine', 'rural', 'Destape y limpieza de fosas'],
    ['calera-de-tango', 'Calera de Tango', 'rural', 'Servicio en parcelas y casas'],
    ['pirque', 'Pirque', 'rural', 'Limpieza de fosas y biodigestores'],
    ['chicureo', 'Chicureo', 'rural', 'Mantención de fosas para condominios'],
    ['curacavi', 'Curacaví', 'rural', 'Servicio rural 24/7'],
    ['melipilla', 'Melipilla', 'rural', 'Destape y limpieza de fosas'],
    ['padre-hurtado', 'Padre Hurtado', 'rural', 'Servicio domiciliario y rural'],
    ['penaflor', 'Peñaflor', 'rural', 'Destape de alcantarillado'],
    ['san-jose-de-maipo', 'Cajón del Maipo', 'rural', 'Servicio cordillera 24/7'],
    ['cajon-maipo', 'Cajón del Maipo', 'rural', 'Servicio cordillera 24/7'],
    ['las-condes', 'Las Condes', 'urbano', 'Destape urgente 24/7'],
    ['vitacura', 'Vitacura', 'urbano', 'Destape de WC, lavaplatos y más'],
    ['providencia', 'Providencia', 'urbano', 'Destape de alcantarillado urgente'],
    ['lo-barnechea', 'Lo Barnechea', 'urbano', 'Destape 24/7 en sector oriente'],
    ['la-reina', 'La Reina', 'urbano', 'Destape urgente y hidrojet'],
    ['nunoa', 'Ñuñoa', 'urbano', 'Destape de WC y cocina'],
];

function escapeXml(s) {
    return String(s)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&apos;');
}

function buildSvg(name, secondary) {
    const safeName = escapeXml(name);
    const safeSec = escapeXml(secondary);
    return `<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="630" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="rgba(15,23,42,0.85)" />
      <stop offset="100%" stop-color="rgba(15,23,42,0.65)" />
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#g)" />
  <g font-family="Plus Jakarta Sans, Helvetica, Arial, sans-serif">
    <text x="80" y="170" font-size="32" font-weight="700" letter-spacing="8" fill="#67e8f9" text-transform="uppercase">DESTAPE RÁPIDO</text>
    <text x="80" y="290" font-size="84" font-weight="800" fill="#ffffff">${safeName}</text>
    <text x="80" y="370" font-size="36" font-weight="500" fill="#cbd5e1">${safeSec}</text>
    <text x="80" y="540" font-size="22" font-weight="600" fill="#94a3b8">24/7 · Cobertura Región Metropolitana</text>
    <text x="80" y="575" font-size="32" font-weight="700" fill="#ffffff">+56 9 6588 9226</text>
  </g>
  <g transform="translate(950, 60)">
    <rect x="0" y="0" width="170" height="60" rx="30" fill="#16a34a" />
    <text x="85" y="40" text-anchor="middle" font-size="22" font-weight="700" fill="#ffffff" font-family="Plus Jakarta Sans, Helvetica, Arial, sans-serif">WhatsApp</text>
  </g>
</svg>`;
}

async function makeOg(slug, displayName, kind, secondary) {
    const base = kind === 'urbano' ? BASE_URBANO : BASE_RURAL;
    const out = path.join(IMG, `og-${slug}.jpg`);
    const svg = Buffer.from(buildSvg(displayName, secondary));
    try {
        await sharp(base)
            .resize(1200, 630, { fit: 'cover', position: 'center' })
            .composite([{ input: svg, top: 0, left: 0 }])
            .jpeg({ quality: 82, progressive: true, mozjpeg: true })
            .toFile(out);
        const stats = fs.statSync(out);
        console.log(`  ok  og-${slug}.jpg (${(stats.size / 1024).toFixed(1)} KB) — ${displayName}`);
    } catch (e) {
        console.error(`  ERR ${slug}: ${e.message}`);
    }
}

(async () => {
    for (const [slug, name, kind, sec] of ZONES) {
        await makeOg(slug, name, kind, sec);
    }
    console.log(`\nGenerated ${ZONES.length} og:images`);
})();
