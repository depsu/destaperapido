#!/usr/bin/env python3
"""
Apunta og:image y twitter:image a /assets/og-image-1200x630.jpg (1200x630 real,
JPG estándar compatible con Facebook/LinkedIn) en lugar de la WebP 1032x576.

La imagen original (camio-haciendo-servicio-en-la-calle.webp) se sigue usando como
contenido visual del sitio (hero, etc.) — solo cambia el meta OG/Twitter.

Ejecutar desde la raíz del repo:
    python3 scripts/update_og_image.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

OLD_URL = "https://www.destaperapido.cl/images/camio-haciendo-servicio-en-la-calle.webp"
NEW_URL = "https://www.destaperapido.cl/assets/og-image-1200x630.jpg"

OLD_TYPE = '<meta property="og:image:type" content="image/webp">'
NEW_TYPE = '<meta property="og:image:type" content="image/jpeg">'

# Reemplazos puntuales (solo en contexto de og:image o twitter:image)
REPLACEMENTS = [
    (f'<meta property="og:image" content="{OLD_URL}">',
     f'<meta property="og:image" content="{NEW_URL}">'),
    (f'<meta name="twitter:image" content="{OLD_URL}">',
     f'<meta name="twitter:image" content="{NEW_URL}">'),
    (OLD_TYPE, NEW_TYPE),
]

def main():
    total = 0
    for html in PUBLIC.rglob("*.html"):
        text = html.read_text(encoding="utf-8")
        original = text
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if text != original:
            html.write_text(text, encoding="utf-8")
            total += 1
            print(f"OK  {html.relative_to(ROOT)}")
    print(f"\n{total} archivos actualizados.")

if __name__ == "__main__":
    main()
