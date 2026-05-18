#!/usr/bin/env python3
"""Add hreflang="es-CL" and hreflang="x-default" links right after each canonical.

Skips pages with noindex meta.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

CANONICAL_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"\s*/?>')
NOINDEX_RE = re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex', re.IGNORECASE)


def transform(html: str) -> tuple[str, bool]:
    if NOINDEX_RE.search(html):
        return html, False
    m = CANONICAL_RE.search(html)
    if not m:
        return html, False
    canonical_url = m.group(1)
    if 'hreflang="es-CL"' in html:
        return html, False
    insertion = (
        f'\n    <link rel="alternate" hreflang="es-CL" href="{canonical_url}">'
        f'\n    <link rel="alternate" hreflang="x-default" href="{canonical_url}">'
    )
    return html[: m.end()] + insertion + html[m.end():], True


def main() -> int:
    changed = 0
    skipped = 0
    for html_file in PUBLIC.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8")
        new_text, ok = transform(text)
        if ok:
            html_file.write_text(new_text, encoding="utf-8")
            changed += 1
        else:
            skipped += 1
    print(f"Changed: {changed}  Skipped: {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
