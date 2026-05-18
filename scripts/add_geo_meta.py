#!/usr/bin/env python3
"""Add geo meta tags (geo.region, geo.placename, geo.position, ICBM) to pilot pages."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

# Per-page coordinates: (placename, lat, lng)
GEO = {
    "index.html": ("Santiago de Chile", -33.4489, -70.6693),
    "precios-orientativos.html": ("Santiago de Chile", -33.4489, -70.6693),
    "zonas/rural/lampa.html": ("Lampa, Región Metropolitana", -33.2833, -70.8833),
    "zonas/rural/talagante.html": ("Talagante, Región Metropolitana", -33.6667, -70.9333),
    "zonas/rural/isla-de-maipo.html": ("Isla de Maipo, Región Metropolitana", -33.7569, -70.9036),
    "zonas/rural/colina.html": ("Colina, Región Metropolitana", -33.2008, -70.6772),
    "zonas/rural/buin-paine.html": ("Buin, Región Metropolitana", -33.7330, -70.7430),
    "zonas/rural/calera-de-tango.html": ("Calera de Tango, Región Metropolitana", -33.6286, -70.7639),
    "zonas/rural/pirque.html": ("Pirque, Región Metropolitana", -33.6390, -70.5800),
}


def transform(html: str, placename: str, lat: float, lng: float) -> tuple[str, bool]:
    if 'name="geo.region"' in html:
        return html, False
    geo_block = (
        f'    <meta name="geo.region" content="CL-RM">\n'
        f'    <meta name="geo.placename" content="{placename}">\n'
        f'    <meta name="geo.position" content="{lat};{lng}">\n'
        f'    <meta name="ICBM" content="{lat}, {lng}">\n'
    )
    # Insert just before </head>
    if '</head>' not in html:
        return html, False
    new_html = html.replace('</head>', geo_block + '</head>', 1)
    return new_html, True


def main() -> int:
    changed = 0
    for rel, (placename, lat, lng) in GEO.items():
        f = PUBLIC / rel
        if not f.exists():
            print(f"  ??  {rel}: not found")
            continue
        text = f.read_text(encoding="utf-8")
        new_text, ok = transform(text, placename, lat, lng)
        if ok:
            f.write_text(new_text, encoding="utf-8")
            print(f"  ok  {rel}: geo set to {placename} ({lat}, {lng})")
            changed += 1
        else:
            print(f"  --  {rel}: already has geo or no </head>")
    print(f"\nChanged: {changed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
