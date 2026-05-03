#!/usr/bin/env python3
"""
Sincroniza el `aggregateRating` de los JSON-LD con datos reales de Google
Business. Pega el rating + total que ves en tu perfil cuando lo corras.

Uso:
    python3 scripts/sync_aggregate_rating.py 4.9 183

(rating, total). Actualiza index.html, testimonios.html, contacto.html y
nosotros.html (las páginas más relevantes para EEAT).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

TARGETS = [
    "index.html",
    "testimonios.html",
    "contacto.html",
    "nosotros.html",
]


def patch_jsonld(content: str, rating: float, total: int) -> str:
    """Para cada bloque JSON-LD, si contiene LocalBusiness/Plumber, agrega o actualiza aggregateRating."""

    def replace_block(match: re.Match) -> str:
        body = match.group(1).strip()
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return match.group(0)

        items = data if isinstance(data, list) else [data]
        for item in items:
            if not isinstance(item, dict):
                continue
            t = item.get("@type")
            types = t if isinstance(t, list) else [t] if t else []
            if "LocalBusiness" in types or "Plumber" in types or "Organization" in types:
                item["aggregateRating"] = {
                    "@type": "AggregateRating",
                    "ratingValue": str(rating),
                    "reviewCount": str(total),
                    "bestRating": "5",
                }

        new_body = json.dumps(items if isinstance(data, list) else items[0],
                              ensure_ascii=False, indent=2)
        return f'<script type="application/ld+json">\n{new_body}\n    </script>'

    return re.sub(
        r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
        replace_block,
        content,
        flags=re.DOTALL | re.IGNORECASE,
    )


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("uso: python3 sync_aggregate_rating.py <rating> <total>\nej:  python3 sync_aggregate_rating.py 4.9 183")
    try:
        rating = float(sys.argv[1])
        total = int(sys.argv[2])
    except ValueError:
        sys.exit("rating debe ser float y total debe ser int")
    if not (1 <= rating <= 5) or total < 1:
        sys.exit("rating fuera de 1-5 o total < 1")

    changed = 0
    for rel in TARGETS:
        path = PUBLIC / rel
        if not path.exists():
            print(f"  ⚠️  no existe: {rel}")
            continue
        raw = path.read_text(encoding="utf-8")
        new = patch_jsonld(raw, rating, total)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            changed += 1
            print(f"  ✅ {rel}  ({rating}★ · {total} reseñas)")
        else:
            print(f"  · sin cambios: {rel}")
    print(f"\nactualizados: {changed}/{len(TARGETS)}")


if __name__ == "__main__":
    main()
