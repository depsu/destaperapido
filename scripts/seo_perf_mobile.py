#!/usr/bin/env python3
"""
seo_perf_mobile.py
------------------
Aplica fixes de performance/SEO mobile a TODAS las páginas HTML del sitio:

1. Añade preconnect a cdnjs.cloudflare.com y googletagmanager.com (si no existe).
2. Añade loading="lazy" + decoding="async" a <img> que no los tengan,
   excepto las marcadas con fetchpriority="high" (LCP).
3. Normaliza og:url eliminando .html (sólo cuando hay canonical equivalente).
4. Normaliza og:site_name a "Destape Rápido".

Uso:
    python3 scripts/seo_perf_mobile.py [--dry]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

DRY = "--dry" in sys.argv

PRECONNECT_BLOCK = """    <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
    <link rel="preconnect" href="https://www.googletagmanager.com">
    <link rel="dns-prefetch" href="https://cdnjs.cloudflare.com">
"""

CANONICAL_RE = re.compile(r'(<link\s+rel="canonical"[^>]*>)', re.IGNORECASE)
PRECONNECT_CDNJS_RE = re.compile(r'rel="preconnect"\s+href="https://cdnjs', re.IGNORECASE)
IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE | re.DOTALL)
OG_URL_RE = re.compile(r'(<meta\s+property="og:url"\s+content=")([^"]+)(")', re.IGNORECASE)
OG_SITE_NAME_RE = re.compile(r'(<meta\s+property="og:site_name"\s+content=")([^"]+)(")', re.IGNORECASE)


def add_preconnect(html: str) -> tuple[str, bool]:
    if PRECONNECT_CDNJS_RE.search(html):
        return html, False
    m = CANONICAL_RE.search(html)
    if not m:
        return html, False
    insert_at = m.end()
    new = html[:insert_at] + "\n" + PRECONNECT_BLOCK.rstrip("\n") + html[insert_at:]
    return new, True


def fix_img(tag: str) -> tuple[str, bool]:
    """Add loading=lazy + decoding=async if missing.
    Skip if fetchpriority="high" (LCP image, must load eagerly).
    """
    if re.search(r'fetchpriority\s*=\s*"high"', tag, re.IGNORECASE):
        return tag, False
    changed = False
    new_tag = tag
    if not re.search(r'\bloading\s*=', new_tag, re.IGNORECASE):
        new_tag = new_tag[:-1].rstrip() + ' loading="lazy">'
        changed = True
    if not re.search(r'\bdecoding\s*=', new_tag, re.IGNORECASE):
        new_tag = new_tag[:-1].rstrip() + ' decoding="async">'
        changed = True
    return new_tag, changed


def lazy_decode_imgs(html: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        tag, changed = fix_img(m.group(0))
        if changed:
            count += 1
        return tag

    return IMG_TAG_RE.sub(repl, html), count


def fix_og_url(html: str) -> tuple[str, bool]:
    """Normaliza og:url a la versión del canonical (sin .html).
    Sólo si encuentra canonical limpio + og:url con .html.
    """
    canon = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html, re.IGNORECASE)
    if not canon:
        return html, False
    canon_url = canon.group(1)
    if canon_url.endswith(".html"):
        return html, False  # nada que normalizar

    def repl(m: re.Match) -> str:
        url = m.group(2)
        if url.endswith(".html"):
            return f"{m.group(1)}{canon_url}{m.group(3)}"
        return m.group(0)

    new_html, n = OG_URL_RE.subn(repl, html)
    return new_html, n > 0 and new_html != html


def fix_og_site_name(html: str) -> tuple[str, bool]:
    def repl(m: re.Match) -> str:
        return f'{m.group(1)}Destape Rápido{m.group(3)}'

    new_html, n = OG_SITE_NAME_RE.subn(repl, html)
    if n == 0:
        return html, False
    if new_html == html:
        return html, False
    # solo reportar cambio si difería
    return new_html, True


def process(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    orig = text
    stats = {"file": str(path.relative_to(ROOT)), "preconnect": False, "imgs": 0, "og_url": False, "og_site": False}

    text, ch = add_preconnect(text)
    stats["preconnect"] = ch

    text, n = lazy_decode_imgs(text)
    stats["imgs"] = n

    text, ch = fix_og_url(text)
    stats["og_url"] = ch

    text, ch = fix_og_site_name(text)
    stats["og_site"] = ch

    if text != orig and not DRY:
        path.write_text(text, encoding="utf-8")
    stats["changed"] = text != orig
    return stats


def main():
    files = sorted(PUBLIC.rglob("*.html"))
    total_files = 0
    total_imgs = 0
    for f in files:
        s = process(f)
        if s["changed"]:
            total_files += 1
        total_imgs += s["imgs"]
        flags = []
        if s["preconnect"]:
            flags.append("preconnect")
        if s["imgs"]:
            flags.append(f"imgs={s['imgs']}")
        if s["og_url"]:
            flags.append("og_url")
        if s["og_site"]:
            flags.append("og_site")
        if flags:
            print(f"  ✓ {s['file']:55s} {' '.join(flags)}")
    print(f"\n{'[DRY] ' if DRY else ''}Archivos modificados: {total_files} · imgs lazyfied: {total_imgs}")


if __name__ == "__main__":
    main()
