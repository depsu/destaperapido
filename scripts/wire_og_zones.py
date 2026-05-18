#!/usr/bin/env python3
"""Wire each zone page to its newly generated og-<slug>.jpg.

Replaces:
- og:image content pointing to /images/og.jpg (generic fallback)
- og:image content pointing to /images/og-<wrong>.jpg

with the correct /images/og-<slug>.jpg matching the page's filename.
Also updates twitter:image accordingly.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
ZONES_DIR = PUBLIC / "zonas"

GENERATED = {
    "lampa", "talagante", "isla-de-maipo", "colina", "buin-paine",
    "calera-de-tango", "pirque", "chicureo", "curacavi", "melipilla",
    "padre-hurtado", "penaflor", "san-jose-de-maipo", "cajon-maipo",
    "las-condes", "vitacura", "providencia", "lo-barnechea",
    "la-reina", "nunoa",
}


def transform(html: str, slug: str) -> tuple[str, int]:
    n = 0
    target = f"https://www.destaperapido.cl/images/og-{slug}.jpg"

    def _sub_og(m):
        nonlocal n
        url = m.group(1)
        if "/images/og" in url:
            new_url = target
            if new_url != url:
                n += 1
                return f'<meta property="og:image" content="{new_url}">'
        return m.group(0)

    html = re.sub(r'<meta\s+property="og:image"\s+content="([^"]+)"\s*/?>', _sub_og, html)

    def _sub_tw(m):
        nonlocal n
        url = m.group(1)
        if "/images/og" in url or "/images/camio" in url:
            new_url = target
            if new_url != url:
                n += 1
                return f'<meta name="twitter:image" content="{new_url}">'
        return m.group(0)

    html = re.sub(r'<meta\s+name="twitter:image"\s+content="([^"]+)"\s*/?>', _sub_tw, html)

    # Update og:image:type and og:image:alt to match new asset
    if "twitter:image" in html or "og:image" in html:
        # Force type to image/jpeg (since we generated JPG)
        html = re.sub(
            r'<meta\s+property="og:image:type"\s+content="[^"]+">',
            '<meta property="og:image:type" content="image/jpeg">',
            html,
        )

    return html, n


def main() -> int:
    changed = 0
    total = 0
    for html_file in ZONES_DIR.rglob("*.html"):
        slug = html_file.stem
        if slug not in GENERATED:
            # Use slug "san-jose-de-maipo" when file is san-jose-de-maipo, etc.
            continue
        text = html_file.read_text(encoding="utf-8")
        new_text, n = transform(text, slug)
        if n:
            html_file.write_text(new_text, encoding="utf-8")
            changed += 1
            total += n
            print(f"  ok  {html_file.relative_to(PUBLIC)} -> og-{slug}.jpg ({n} meta)")
    print(f"\nArchivos modificados: {changed}  Meta actualizadas: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
