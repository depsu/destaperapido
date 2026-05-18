#!/usr/bin/env python3
"""Adjust desktop nav breakpoint from lg (1024px) to xl (1280px).

Why: 8+ links + tel button + WhatsApp CTA didn't fit comfortably at 1024px
with gap-8 (32px). They overlapped or wrapped awkwardly. Better UX:
- 1024-1279px: show hamburger mobile menu (same as <1024)
- 1280px+: full desktop nav with slightly tighter gap-6 (24px)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

# Map of replacements
REPLACEMENTS = [
    ('hidden lg:flex items-center gap-8 font-semibold', 'hidden xl:flex items-center gap-6 font-semibold'),
    ('flex items-center gap-4 lg:hidden', 'flex items-center gap-4 xl:hidden'),
    # Inner phone link breakpoint (was `hidden xl:block` already; keep)
]


def transform(html: str) -> tuple[str, int]:
    n = 0
    for old, new in REPLACEMENTS:
        count = html.count(old)
        if count:
            html = html.replace(old, new)
            n += count
    return html, n


def main() -> int:
    changed = 0
    total = 0
    for html_file in PUBLIC.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8")
        if 'hidden lg:flex items-center gap-8' not in text and 'flex items-center gap-4 lg:hidden' not in text:
            continue
        new_text, n = transform(text)
        if n:
            html_file.write_text(new_text, encoding="utf-8")
            changed += 1
            total += n
            print(f"  ok  {html_file.relative_to(PUBLIC)}: {n} reemplazos")
    print(f"\nArchivos modificados: {changed}  Reemplazos: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
