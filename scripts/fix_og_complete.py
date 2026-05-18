#!/usr/bin/env python3
"""Complete Open Graph + Twitter meta in pilot pages.

- Replace broken og-{comuna}.jpg references with /images/og.jpg (1200x630).
- Add og:image:width, og:image:height, og:image:alt, og:image:type after og:image.
- Ensure twitter:card="summary_large_image".
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PILOTS = [
    "public/index.html",
    "public/precios-orientativos.html",
    "public/zonas/rural/lampa.html",
    "public/zonas/rural/talagante.html",
    "public/zonas/rural/isla-de-maipo.html",
    "public/zonas/rural/colina.html",
    "public/zonas/rural/buin-paine.html",
    "public/zonas/rural/calera-de-tango.html",
    "public/zonas/rural/pirque.html",
]

# (width, height, type) for the og.jpg fallback
OG_WIDTH = "1200"
OG_HEIGHT = "630"
OG_TYPE = "image/jpeg"
OG_FALLBACK = "https://www.destaperapido.cl/images/og.jpg"


def transform(html: str, og_alt: str) -> tuple[str, list]:
    changes = []
    # 1. Replace broken og-{comuna}.jpg references with og.jpg
    new_html = re.sub(
        r'(<meta\s+property="og:image"\s+content=")[^"]*og-[^"/]+\.jpg(")',
        rf'\1{OG_FALLBACK}\2',
        html,
    )
    if new_html != html:
        changes.append("og:image fixed (was broken og-<comuna>.jpg)")
    html = new_html

    # Determine actual og:image URL after fix
    m = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html)
    og_url = m.group(1) if m else OG_FALLBACK
    # Detect type from extension
    if og_url.endswith(".jpg") or og_url.endswith(".jpeg"):
        og_type = "image/jpeg"
    elif og_url.endswith(".webp"):
        og_type = "image/webp"
    elif og_url.endswith(".png"):
        og_type = "image/png"
    else:
        og_type = "image/jpeg"

    # 2. Add og:image:width/height/alt/type after the og:image line
    additions = []
    if 'property="og:image:width"' not in html:
        additions.append(f'<meta property="og:image:width" content="{OG_WIDTH}">')
    if 'property="og:image:height"' not in html:
        additions.append(f'<meta property="og:image:height" content="{OG_HEIGHT}">')
    if 'property="og:image:type"' not in html:
        additions.append(f'<meta property="og:image:type" content="{og_type}">')
    if 'property="og:image:alt"' not in html:
        additions.append(f'<meta property="og:image:alt" content="{og_alt}">')

    if additions:
        insertion = "\n    ".join(additions)
        # Insert after the LAST og:image line
        og_image_pattern = re.compile(r'(<meta\s+property="og:image"\s+content="[^"]+">)')
        matches = list(og_image_pattern.finditer(html))
        if matches:
            last = matches[-1]
            html = html[:last.end()] + "\n    " + insertion + html[last.end():]
            changes.append(f"+{len(additions)} og:image:* meta tags")

    # 3. Ensure twitter:card=summary_large_image (some have just twitter:image)
    if 'name="twitter:card"' not in html:
        # Insert before </head>
        html = html.replace('</head>', '    <meta name="twitter:card" content="summary_large_image">\n</head>', 1)
        changes.append("twitter:card added")

    return html, changes


def derive_og_alt(path: str) -> str:
    if path.endswith("/index.html"):
        return "Destape Rápido - Destape de alcantarillado 24/7 en Santiago, Chile"
    name = Path(path).stem
    if name == "precios-orientativos":
        return "Precios orientativos de destape de alcantarillado y fosas en Santiago"
    # zonas rurales
    pretty = name.replace("-", " ").title()
    return f"Destape Rápido en {pretty} - Servicio 24/7 en zonas rurales"


def main() -> int:
    grand = 0
    for rel in PILOTS:
        f = ROOT / rel
        text = f.read_text(encoding="utf-8")
        alt = derive_og_alt(rel)
        new_text, changes = transform(text, alt)
        if changes:
            f.write_text(new_text, encoding="utf-8")
            print(f"  ok  {rel}: {'; '.join(changes)}")
            grand += len(changes)
        else:
            print(f"  --  {rel}: nothing to change")
    print(f"\nTotal changes: {grand}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
