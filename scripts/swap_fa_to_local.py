#!/usr/bin/env python3
"""
Reemplaza todas las referencias al CDN de Font Awesome (cdnjs.cloudflare.com)
por el CSS local /fonts/fontawesome/all.min.css. Idempotente.

También elimina los <link rel="preconnect" href="https://cdnjs.cloudflare.com">
que ya no aporta nada para FA.
"""
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"
LOCAL_CSS = "/fonts/fontawesome/all.min.css"

# Cualquier URL de FA en cdnjs (cualquier versión)
CDN_URL_RE = re.compile(
    r'https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[\d.]+/css/all\.min\.css'
)

# Líneas de preconnect/dns-prefetch a cdnjs cuando ya no se usan
PRECONNECT_RE = re.compile(
    r'\s*<link[^>]*rel="(?:preconnect|dns-prefetch)"[^>]*href="https://cdnjs\.cloudflare\.com[^"]*"[^>]*>'
)

def find_html_files():
    for p in PUBLIC.rglob("*.html"):
        if "node_modules" in p.parts:
            continue
        yield p

def main():
    swapped_files = 0
    swapped_refs = 0
    cleaned_preconnect = 0
    for f in find_html_files():
        text = f.read_text(encoding="utf-8")
        new_text, n = CDN_URL_RE.subn(LOCAL_CSS, text)

        # Si ya no quedan referencias a cdnjs (más allá de preconnect),
        # limpiar también los preconnects/dns-prefetch a cdnjs
        non_preconnect_remains = bool(re.search(r'cdnjs\.cloudflare\.com', PRECONNECT_RE.sub('', new_text)))
        if not non_preconnect_remains:
            new_text2, m = PRECONNECT_RE.subn("", new_text)
            if m:
                cleaned_preconnect += m
                new_text = new_text2

        if new_text != text:
            f.write_text(new_text, encoding="utf-8")
            swapped_files += 1
        swapped_refs += n

    print(f"Archivos modificados: {swapped_files}")
    print(f"Referencias FA reemplazadas: {swapped_refs}")
    print(f"Preconnects cdnjs limpiados: {cleaned_preconnect}")

if __name__ == "__main__":
    main()
