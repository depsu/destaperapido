// Check icons in production: take screenshots focusing on icon-heavy areas and report
// any failed font requests / missing glyphs.
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');
const OUTDIR = path.join(ROOT, 'mejoras-destaperapido', 'capturas-icons-prod');
const BASE = 'https://www.destaperapido.cl';

const URLS = [
    '/',
    '/precios-orientativos',
    '/zonas/rural/lampa',
    '/contacto',
];

function safe(p) {
    return p.replace(/^\/+/, '').replace(/[\/]/g, '__') || 'home';
}

async function main() {
    if (!fs.existsSync(OUTDIR)) fs.mkdirSync(OUTDIR, { recursive: true });
    const browser = await chromium.launch();
    const report = [];

    for (const u of URLS) {
        const ctx = await browser.newContext({
            viewport: { width: 412, height: 915 },
            deviceScaleFactor: 2,
            isMobile: true,
            hasTouch: true,
        });
        const page = await ctx.newPage();
        const failedReqs = [];
        const consoleErrs = [];
        page.on('requestfailed', (req) => {
            failedReqs.push({ url: req.url(), error: req.failure()?.errorText });
        });
        page.on('response', (resp) => {
            if (!resp.ok() && (resp.url().includes('font') || resp.url().endsWith('.woff2') || resp.url().endsWith('.woff') || resp.url().includes('fontawesome'))) {
                failedReqs.push({ url: resp.url(), status: resp.status() });
            }
        });
        page.on('console', (msg) => {
            if (msg.type() === 'error') consoleErrs.push(msg.text());
        });

        await page.goto(BASE + u, { waitUntil: 'load', timeout: 30000 });
        await page.waitForTimeout(1500);

        // Check FontFaceSet status (whether FA fonts loaded)
        const fontInfo = await page.evaluate(() => {
            const fonts = [];
            if (document.fonts && document.fonts.size !== undefined) {
                document.fonts.forEach(f => fonts.push({
                    family: f.family,
                    weight: f.weight,
                    status: f.status,
                    style: f.style,
                }));
            }
            // Check if FA icons have computed font-family
            const sample = document.querySelector('.fa-solid, .fa-brands, .fa-regular, [class*="fa-"]');
            const computed = sample ? {
                el: sample.outerHTML.slice(0, 120),
                fontFamily: getComputedStyle(sample).fontFamily,
                fontWeight: getComputedStyle(sample).fontWeight,
                content: getComputedStyle(sample, '::before').content,
                fontSize: getComputedStyle(sample).fontSize,
            } : null;
            return { fonts, sample: computed, totalFA: document.querySelectorAll('[class*="fa-"]').length };
        });

        // Find a region with many icons and capture it
        const region = await page.locator('header, nav, .fixed').first();
        try {
            await region.screenshot({ path: path.join(OUTDIR, `${safe(u)}__header.png`) });
        } catch (e) {}
        await page.screenshot({ path: path.join(OUTDIR, `${safe(u)}__viewport.png`), fullPage: false });

        report.push({ url: u, fontInfo, failedReqs, consoleErrs });
        await page.close();
        await ctx.close();
    }
    await browser.close();

    console.log(JSON.stringify(report, null, 2));
    fs.writeFileSync(path.join(OUTDIR, '_report.json'), JSON.stringify(report, null, 2));
}

main().catch((e) => { console.error(e); process.exit(1); });
