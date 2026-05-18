#!/usr/bin/env python3
"""
Agrega aggregateRating al schema LocalBusiness/Plumber existente en cada
página de zona urbana/rural. Idempotente.

ratingValue y reviewCount deben coincidir con el global del negocio.
"""
import json
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"

RATING = {
    "@type": "AggregateRating",
    "ratingValue": "5.0",
    "reviewCount": "16",
    "bestRating": "5",
    "worstRating": "1"
}

def patch_ld_block(block_text):
    """Recibe el contenido entre <script type=ld+json> y </script>.
    Devuelve (nuevo_texto, changed)."""
    try:
        data = json.loads(block_text)
    except json.JSONDecodeError:
        return block_text, False

    items = data if isinstance(data, list) else [data]
    changed = False
    for item in items:
        types = item.get("@type")
        if not types:
            continue
        types_list = types if isinstance(types, list) else [types]
        if not any(t in ("LocalBusiness", "Plumber") for t in types_list):
            continue
        if "aggregateRating" in item:
            continue
        item["aggregateRating"] = RATING
        changed = True

    if not changed:
        return block_text, False
    return json.dumps(data if isinstance(data, list) else items[0], ensure_ascii=False, indent=2), True

def main():
    targets = list((PUBLIC / "zonas" / "urbano").glob("*.html")) + \
              list((PUBLIC / "zonas" / "rural").glob("*.html"))
    added = 0
    for f in targets:
        text = f.read_text(encoding="utf-8")
        # Encuentra todos los bloques ld+json y procesa el primero que tenga LocalBusiness/Plumber
        new_text = text
        any_changed = False
        for m in re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>', text):
            block = m.group(1)
            new_block, changed = patch_ld_block(block)
            if changed:
                new_text = new_text.replace(m.group(0),
                    f'<script type="application/ld+json">\n{new_block}\n</script>', 1)
                any_changed = True
                break  # solo el primero
        if any_changed:
            f.write_text(new_text, encoding="utf-8")
            added += 1
            print(f"+ {f.relative_to(PUBLIC)}")
    print(f"\nTotal: {added} archivos con aggregateRating agregado")

if __name__ == "__main__":
    main()
