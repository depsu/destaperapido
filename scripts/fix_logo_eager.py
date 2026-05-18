#!/usr/bin/env python3
"""Replace the FIRST occurrence of logo-nav.webp (header) loading=lazy to loading=eager + fetchpriority=high.

The footer logo keeps lazy because it's below-the-fold.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "public"
IMG_RE = re.compile(
    r'(<img\s+src="/logo-nav\.webp"[^>]*?)\bloading="lazy"([^>]*?>)',
    re.DOTALL,
)
FP_RE = re.compile(r'fetchpriority="[^"]+"')


def transform(html: str) -> tuple[str, int]:
    """Replace only the FIRST occurrence per file."""
    match = IMG_RE.search(html)
    if not match:
        return html, 0
    full = match.group(0)
    new = full.replace('loading="lazy"', 'loading="eager"')
    if "fetchpriority=" not in new:
        new = new.replace('loading="eager"', 'loading="eager" fetchpriority="high"')
    return html[: match.start()] + new + html[match.end():], 1


def main() -> int:
    changed = 0
    skipped = 0
    for html_file in ROOT.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8")
        new_text, n = transform(text)
        if n:
            html_file.write_text(new_text, encoding="utf-8")
            changed += 1
            print(f"  ok  {html_file.relative_to(ROOT)}")
        else:
            skipped += 1
    print(f"\nChanged: {changed}  Skipped (no match): {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
