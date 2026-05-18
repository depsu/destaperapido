#!/usr/bin/env python3
"""Generate a segmented sitemap structure:

- sitemap.xml (index)
- sitemap-pages.xml (static pages)
- sitemap-blog.xml (blog posts)
- sitemap-zonas.xml (urban + rural zones)
- sitemap-servicios.xml (services + casos-reales + landing kept noindex are excluded)

Scans public/ and excludes:
- pages with <meta name="robots" content="...noindex...">
- 404.html, gracias.html, servicios/test.html
- /api/ endpoints
"""
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
BASE = "https://www.destaperapido.cl"

# Files excluded by name
EXCLUDE_NAMES = {
    "404.html", "gracias.html",
}
EXCLUDE_RELS = {
    "servicios/test.html",
}

NOINDEX_RE = re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex', re.IGNORECASE)


def page_url(rel_path: str) -> str:
    """Convert public/foo/bar.html -> https://www.destaperapido.cl/foo/bar.
    /index.html -> / (root)
    """
    if rel_path == "index.html":
        return f"{BASE}/"
    p = rel_path
    if p.endswith("/index.html"):
        p = p[: -len("/index.html")]
        return f"{BASE}/{p}"
    if p.endswith(".html"):
        p = p[:-5]
    return f"{BASE}/{p}"


def categorize(rel_path: str) -> str:
    if rel_path.startswith("blog/"):
        return "blog"
    if rel_path.startswith("zonas/"):
        return "zonas"
    if rel_path.startswith("servicios/") or rel_path.startswith("casos-reales/") or rel_path.startswith("landing/"):
        return "servicios"
    return "pages"


PRIORITY_DEFAULTS = {
    "pages": 0.7,
    "blog": 0.6,
    "zonas": 0.7,
    "servicios": 0.8,
}
CHANGEFREQ_DEFAULTS = {
    "pages": "monthly",
    "blog": "monthly",
    "zonas": "monthly",
    "servicios": "monthly",
}
# Special priorities by exact rel_path
SPECIAL_PRIORITIES = {
    "index.html": 1.0,
    "contacto.html": 0.9,
    "servicios/index.html": 0.9,
    "cobertura.html": 0.9,
    "precios-orientativos.html": 0.9,
    "calculadora-cotizacion.html": 0.8,
}
SPECIAL_CHANGEFREQ = {
    "index.html": "weekly",
    "blog/index.html": "weekly",
}


def collect_pages() -> dict:
    """Return {category: [(url, lastmod, priority, changefreq)]}"""
    out = {"pages": [], "blog": [], "zonas": [], "servicios": []}
    for html in PUBLIC.rglob("*.html"):
        rel = html.relative_to(PUBLIC).as_posix()
        if html.name in EXCLUDE_NAMES:
            continue
        if rel in EXCLUDE_RELS:
            continue
        text = html.read_text(encoding="utf-8", errors="ignore")
        if NOINDEX_RE.search(text):
            continue
        url = page_url(rel)
        lastmod = datetime.fromtimestamp(html.stat().st_mtime).strftime("%Y-%m-%d")
        cat = categorize(rel)
        priority = SPECIAL_PRIORITIES.get(rel, PRIORITY_DEFAULTS[cat])
        changefreq = SPECIAL_CHANGEFREQ.get(rel, CHANGEFREQ_DEFAULTS[cat])
        out[cat].append((url, lastmod, priority, changefreq))
    for k in out:
        out[k].sort(key=lambda x: x[0])
    return out


def render_urlset(entries: list) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, lastmod, priority, changefreq in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def render_index(sub_files: list, today: str) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for name in sub_files:
        lines.append("  <sitemap>")
        lines.append(f"    <loc>{BASE}/{name}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append("  </sitemap>")
    lines.append("</sitemapindex>")
    return "\n".join(lines) + "\n"


def main() -> int:
    data = collect_pages()
    today = datetime.now().strftime("%Y-%m-%d")
    files_written = []

    mapping = {
        "pages": "sitemap-pages.xml",
        "blog": "sitemap-blog.xml",
        "zonas": "sitemap-zonas.xml",
        "servicios": "sitemap-servicios.xml",
    }
    for cat, fname in mapping.items():
        entries = data[cat]
        out = PUBLIC / fname
        out.write_text(render_urlset(entries), encoding="utf-8")
        print(f"  ok  {fname}: {len(entries)} URLs")
        files_written.append(fname)

    # Index
    idx = PUBLIC / "sitemap.xml"
    idx.write_text(render_index(files_written, today), encoding="utf-8")
    print(f"  ok  sitemap.xml (index): {len(files_written)} sub-sitemaps")
    total = sum(len(v) for v in data.values())
    print(f"\nTotal URLs: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
