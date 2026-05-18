#!/usr/bin/env python3
"""Add width/height attrs to specific <img> tags missing them in pilot pages.

Targets:
- Hero <img> in buin-paine (already has srcset but no width/height) -> 1920x1080
- WhatsApp icon SVG from wikimedia in precios -> 48x48
- transparenttextures.com decorative textures -> 800x800 (decorative, fills container)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"


def add_dims(tag: str, w: int, h: int) -> str:
    if 'width=' not in tag:
        tag = re.sub(r'^<img\b', f'<img width="{w}"', tag, count=1)
    if 'height=' not in tag:
        tag = re.sub(r'^<img\b', f'<img height="{h}"', tag, count=1)
    return tag


def transform(html: str, rel: str) -> tuple[str, list]:
    changes = []

    def fix_pattern(pattern: str, w: int, h: int, label: str):
        nonlocal html
        def _sub(m):
            old = m.group(0)
            new = add_dims(old, w, h)
            if new != old:
                changes.append(label)
            return new
        html = re.sub(pattern, _sub, html, flags=re.DOTALL)

    # 1. Hero img with src=/images/camion-haciendo-destape-en-zona-rural.webp (buin-paine specific)
    fix_pattern(
        r'<img\b(?:(?!\bwidth=)[^>])*?src="/images/camion-haciendo-destape-en-zona-rural\.webp"[^>]*?>',
        1920, 1080, "hero buin-paine"
    )

    # 2. WhatsApp.svg from wikimedia
    fix_pattern(
        r'<img\b(?:(?!\bwidth=)[^>])*?src="https://upload\.wikimedia\.org/[^"]+WhatsApp\.svg"[^>]*?>',
        48, 48, "whatsapp svg"
    )

    # 3. transparenttextures.com decorative
    fix_pattern(
        r'<img\b(?:(?!\bwidth=)[^>])*?src="https://www\.transparenttextures\.com[^"]+"[^>]*?>',
        800, 800, "texture decorative"
    )

    return html, changes


def main() -> int:
    pilots = [
        "public/index.html", "public/precios-orientativos.html",
        "public/zonas/rural/lampa.html", "public/zonas/rural/talagante.html",
        "public/zonas/rural/isla-de-maipo.html", "public/zonas/rural/colina.html",
        "public/zonas/rural/buin-paine.html", "public/zonas/rural/calera-de-tango.html",
        "public/zonas/rural/pirque.html",
    ]
    grand = 0
    for rel in pilots:
        f = ROOT / rel
        text = f.read_text(encoding="utf-8")
        new_text, changes = transform(text, rel)
        if changes:
            f.write_text(new_text, encoding="utf-8")
            print(f"  ok  {rel}: {changes}")
            grand += len(changes)
        else:
            print(f"  --  {rel}: 0")
    print(f"\nTotal img dim additions: {grand}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
