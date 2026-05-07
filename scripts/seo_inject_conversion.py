#!/usr/bin/env python3
"""
seo_inject_conversion.py
------------------------
Inserta <script src="/js/conversion.js" defer></script> en TODAS las páginas
HTML antes del </body> (si aún no está incluido).

Uso:
    python3 scripts/seo_inject_conversion.py [--dry]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

DRY = "--dry" in sys.argv

TAG = '<script src="/js/conversion.js" defer></script>'
TAG_RE = re.compile(r'<script[^>]+conversion\.js', re.IGNORECASE)
BODY_END_RE = re.compile(r"</body>", re.IGNORECASE)


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if TAG_RE.search(text):
        return False
    if not BODY_END_RE.search(text):
        return False
    new_text = BODY_END_RE.sub("    " + TAG + "\n</body>", text, count=1)
    if new_text == text:
        return False
    if not DRY:
        path.write_text(new_text, encoding="utf-8")
    return True


def main():
    files = sorted(PUBLIC.rglob("*.html"))
    n = 0
    for f in files:
        if process(f):
            n += 1
            print(f"  ✓ {f.relative_to(ROOT)}")
    print(f"\n{'[DRY] ' if DRY else ''}Archivos actualizados: {n}")


if __name__ == "__main__":
    main()
