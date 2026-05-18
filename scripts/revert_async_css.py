#!/usr/bin/env python3
"""Revert async CSS loading (media=print + onload media swap) to blocking.

Why: the deferred CSS technique only works if the inline critical CSS covers
all above-the-fold styles. Our critical extraction missed enough Tailwind
utilities to cause visible FOUC ("the page dances") when output.css arrived.

Reverting to blocking load is safer:
- One extra ~50ms of render-block on first paint.
- No layout shift / FOUC.
- The user perceives a single clean render instead of two stages.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

# Patterns to convert (any URL):
#   <link rel="stylesheet" href="X" media="print" onload="this.media='all'">
# To:
#   <link rel="stylesheet" href="X">
PATTERN_STYLESHEET = re.compile(
    r'<link\s+rel="stylesheet"\s+href="([^"]+)"\s+media="print"\s+onload="this\.media=\'all\'"\s*/?>',
)

# Also strip duplicate preload-as-style on the same href + noscript fallback for the same href.
NOSCRIPT_FALLBACK = re.compile(
    r'\s*<noscript>\s*<link\s+rel="stylesheet"\s+href="[^"]+"\s*/?>\s*</noscript>',
)

# Preload-as-style lines that target the SAME href as a stylesheet right below (FA pattern)
PRELOAD_AS_STYLE = re.compile(
    r'\s*<link\s+rel="preload"\s+as="style"\s+href="([^"]+)"\s*/?>',
)


def transform(html: str) -> tuple[str, int]:
    n = 0

    # Step 1: convert async stylesheets to blocking
    def _stylesheet(m):
        nonlocal n
        n += 1
        return f'<link rel="stylesheet" href="{m.group(1)}">'

    new_html = PATTERN_STYLESHEET.sub(_stylesheet, html)

    # Step 2: drop preload-as-style that mirrored those stylesheets
    new_html = PRELOAD_AS_STYLE.sub("", new_html)

    # Step 3: drop noscript fallbacks (no longer needed since CSS loads blocking now)
    new_html = NOSCRIPT_FALLBACK.sub("", new_html)

    return new_html, n


def main() -> int:
    changed = 0
    total = 0
    for html_file in PUBLIC.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8")
        if 'media="print" onload' not in text and 'rel="preload" as="style"' not in text:
            continue
        new_text, n = transform(text)
        if new_text != text:
            html_file.write_text(new_text, encoding="utf-8")
            changed += 1
            total += n
            print(f"  ok  {html_file.relative_to(PUBLIC)}: {n} stylesheets revertidos")
    print(f"\nArchivos modificados: {changed}  Stylesheets revertidos: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
