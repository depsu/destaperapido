#!/usr/bin/env python3
"""
Extrae todos los iconos Font Awesome (solid, brands, regular) usados en los
HTML del sitio, los agrupa por estilo y los imprime como JSON listo para
fontawesome-subset.

Uso: python3 scripts/extract_fa_icons.py > scripts/fa-icons.json
"""
import json
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"

PATTERN = re.compile(r'fa-(solid|brands|regular)\s+fa-([a-z0-9\-]+)')

def main():
    bucket = {"solid": set(), "brands": set(), "regular": set()}
    for f in PUBLIC.rglob("*.html"):
        if "node_modules" in f.parts:
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        for style, name in PATTERN.findall(text):
            bucket[style].add(name)

    out = {k: sorted(v) for k, v in bucket.items()}
    print(json.dumps(out, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
