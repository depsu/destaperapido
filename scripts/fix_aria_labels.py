#!/usr/bin/env python3
"""Add aria-label to icon-only links/buttons in pilot pages.

Patterns:
- <a href="tel:..."><i fa-phone></i></a>  -> add aria-label="Llamar al +56 9 9794 6463"
- <a href="https://wa.me/..."><i fa-whatsapp></i></a> -> add aria-label="Escribir por WhatsApp"
- <button onclick="toggleReviewForm()"><i fa-xmark></i></button> -> aria-label="Cerrar formulario"
- <button onclick="deleteReview()"><i fa-trash-can></i></button> -> aria-label="Eliminar reseña"
- Hamburger menu buttons -> aria-label="Abrir/Cerrar menú"
"""
import re
import sys
from pathlib import Path

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

ROOT = Path(__file__).resolve().parent.parent


def add_aria_to_opening_tag(tag: str, label: str) -> str:
    """Add aria-label to the opening tag if not already present."""
    if "aria-label=" in tag:
        return tag
    # Insert after the tag name (e.g., <a or <button)
    return re.sub(r'^(<(?:a|button))(\s)', rf'\1 aria-label="{label}"\2', tag, count=1)


# Each rule: (regex on full element including inner, label, description)
RULES = [
    # tel: phone icon
    (
        re.compile(
            r'<a\s+(?![^>]*aria-label)href="tel:\+56997946463"[^>]*>\s*<i\s+[^>]*fa-phone[^>]*></i>\s*</a>',
            re.DOTALL,
        ),
        "Llamar al +56 9 9794 6463",
    ),
    # WhatsApp icon
    (
        re.compile(
            r'<a\s+(?![^>]*aria-label)[^>]*href="https://wa\.me/[^"]+"[^>]*>\s*<i\s+[^>]*fa-whatsapp[^>]*></i>\s*</a>',
            re.DOTALL,
        ),
        "Escribir por WhatsApp",
    ),
    # Close review modal
    (
        re.compile(
            r'<button\s+(?![^>]*aria-label)[^>]*onclick="toggleReviewForm\(\)"[^>]*>\s*<i\s+[^>]*fa-xmark[^>]*></i>\s*</button>',
            re.DOTALL,
        ),
        "Cerrar formulario",
    ),
    # Delete review
    (
        re.compile(
            r'<button\s+(?![^>]*aria-label)[^>]*onclick="deleteReview\(\)"[^>]*>\s*<i\s+[^>]*fa-trash[^>]*></i>\s*</button>',
            re.DOTALL,
        ),
        "Eliminar reseña",
    ),
]


def transform(html: str) -> tuple[str, int]:
    total = 0
    for regex, label in RULES:
        def _sub(m):
            nonlocal total
            tag = m.group(0)
            # Insert aria-label into the OPENING tag only
            opening_match = re.match(r'<(?:a|button)\b[^>]*>', tag, re.DOTALL)
            if not opening_match:
                return tag
            opening = opening_match.group(0)
            rest = tag[opening_match.end():]
            new_opening = add_aria_to_opening_tag(opening, label)
            if new_opening != opening:
                total += 1
            return new_opening + rest
        html = regex.sub(_sub, html)
    return html, total


def main() -> int:
    grand_total = 0
    for rel in PILOTS:
        f = ROOT / rel
        text = f.read_text(encoding="utf-8")
        new_text, n = transform(text)
        if n:
            f.write_text(new_text, encoding="utf-8")
            print(f"  ok  {rel}: +{n} aria-labels")
            grand_total += n
        else:
            print(f"  --  {rel}: 0")
    print(f"\nTotal aria-labels added: {grand_total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
