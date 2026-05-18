// Take mobile + desktop screenshots of pilot & control pages and check for console errors.
// Usage: node scripts/screenshot_smoke.mjs
import { chromium, devices } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');
const OUTDIR = path.join(ROOT, 'mejoras-destaperapido', 'capturas-pre-push');
const BASE = 'http://localhost:5050';

const PAGES = {
    pilot: [
        '/',
        '/precios-orientativos.html',
        '/zonas/rural/lampa.html',
        '/zonas/rural/talagante.html',
        '/zonas/rural/isla-de-maipo.html',
        '/zonas/rural/colina.html',
        '/zonas/rural/buin-paine.html',
        '/zonas/rural/calera-de-tango.html',
        '/zonas/rural/pirque.html',
    ],
    control: [
        '/blog/index.html',
        '/zonas/urbano/las-condes.html',
        '/servicios/index.html',
        '/contacto.html',
    ],
};

const VIEWPORTS = [
    { name: 'mobile', viewport: { width: 412, height: 915 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true },
    { name: 'desktop', viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, isMobile: false, hasTouch: false },
];

function safeName(p) {
    return p.replace(/^\/+/, '').replace(/[\/\\]/g, '__').replace(/\.html$/, '') || 'home';
}

async function main() {
    if (!fs.existsSync(OUTDIR)) fs.mkdirSync(OUTDIR, { recursive: true });
    const browser = await chromium.launch();
    const report = { pages: [], errors: [], warnings: [] };

    for (const vp of VIEWPORTS) {
        const ctx = await browser.newContext({
            viewport: vp.viewport,
            deviceScaleFactor: vp.deviceScaleFactor,
            isMobile: vp.isMobile,
            hasTouch: vp.hasTouch,
        });
        for (const kind of ['pilot', 'control']) {
            for (const p of PAGES[kind]) {
                const page = await ctx.newPage();
                const consoleMsgs = [];
                const pageErrors = [];
                page.on('console', (msg) => {
                    if (msg.type() === 'error' || msg.type() === 'warning') {
                        consoleMsgs.push(`[${msg.type()}] ${msg.text()}`);
                    }
                });
                page.on('pageerror', (err) => pageErrors.push(err.message));
                const url = BASE + p;
                let status = 'ok';
                try {
                    const resp = await page.goto(url, { waitUntil: 'load', timeout: 30000 });
                    if (!resp || !resp.ok()) status = `bad-status:${resp ? resp.status() : 'no-response'}`;
                    await page.waitForTimeout(800);
                    const fname = `${safeName(p)}__${vp.name}.png`;
                    await page.screenshot({ path: path.join(OUTDIR, fname), fullPage: false });
                } catch (e) {
                    status = `error:${e.message.split('\n')[0]}`;
                }
                report.pages.push({ url: p, viewport: vp.name, kind, status, consoleMsgs, pageErrors });
                if (consoleMsgs.length) report.warnings.push(`${vp.name} ${p}: ${consoleMsgs.length} console msgs`);
                if (pageErrors.length) report.errors.push(`${vp.name} ${p}: ${pageErrors.join(' | ')}`);
                await page.close();
            }
        }
        await ctx.close();
    }

    await browser.close();
    // Write report
    fs.writeFileSync(path.join(OUTDIR, '_report.json'), JSON.stringify(report, null, 2));
    console.log(`\nCaptured ${report.pages.length} screenshots in ${OUTDIR}`);
    console.log(`Errors: ${report.errors.length}  Warnings: ${report.warnings.length}`);
    if (report.errors.length) {
        console.log('--- ERRORS ---');
        for (const e of report.errors.slice(0, 10)) console.log(' ', e);
    }
    if (report.warnings.length) {
        console.log('--- WARNINGS ---');
        for (const w of report.warnings.slice(0, 10)) console.log(' ', w);
    }
    // Surface any non-ok status
    const bad = report.pages.filter((p) => p.status !== 'ok');
    if (bad.length) {
        console.log('--- BAD STATUS ---');
        for (const b of bad) console.log(`  ${b.viewport} ${b.url}: ${b.status}`);
    }
}

main().catch((e) => {
    console.error('FAILED:', e);
    process.exit(1);
});
