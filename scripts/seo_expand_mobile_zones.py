#!/usr/bin/env python3
"""
seo_expand_mobile_zones.py
--------------------------
Expande el menú móvil "Zonas" para listar TODAS las comunas urbanas (19)
y rurales (13) del sitio, en lugar de sólo 6+9 como estaba antes.

Inserta las comunas faltantes antes del enlace "Ver todas..." de cada grupo.

Idempotente.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
DRY = "--dry" in sys.argv or "--dry-run" in sys.argv

# Comunas según el sitio actual
URBANAS = [
    ("cerrillos", "Cerrillos"),
    ("estacion-central", "Estación Central"),
    ("independencia", "Independencia"),
    ("la-florida", "La Florida"),
    ("la-reina", "La Reina"),
    ("las-condes", "Las Condes"),
    ("lo-barnechea", "Lo Barnechea"),
    ("macul", "Macul"),
    ("maipu", "Maipú"),
    ("nunoa", "Ñuñoa"),
    ("penalolen", "Peñalolén"),
    ("providencia", "Providencia"),
    ("pudahuel", "Pudahuel"),
    ("puente-alto", "Puente Alto"),
    ("quilicura", "Quilicura"),
    ("recoleta", "Recoleta"),
    ("san-miguel", "San Miguel"),
    ("santiago-centro", "Santiago Centro"),
    ("vitacura", "Vitacura"),
]
RURALES = [
    ("buin-paine", "Buin / Paine"),
    ("calera-de-tango", "Calera de Tango"),
    ("chicureo", "Chicureo"),
    ("colina", "Colina"),
    ("curacavi", "Curacaví"),
    ("isla-de-maipo", "Isla de Maipo"),
    ("lampa", "Lampa"),
    ("melipilla", "Melipilla"),
    ("padre-hurtado", "Padre Hurtado"),
    ("penaflor", "Peñaflor"),
    ("pirque", "Pirque"),
    ("san-jose-de-maipo", "San José de Maipo"),
    ("talagante", "Talagante"),
]

LINK_CLASS = "block px-4 py-2 text-sm font-medium text-slate-600 hover:text-brand-600"


def render_link(slug: str, label: str, base: str) -> str:
    return (
        f'<a href="/zonas/{base}/{slug}" onclick="closeMenu()"\n'
        f'                            class="{LINK_CLASS}">{label}</a>'
    )


SUB_ZONAS_RE = re.compile(
    r'(<div\s+id="sub-zonas"[^>]*>)([\s\S]*?)(</div>\s*</div>)',
    re.IGNORECASE,
)
HREF_RE = re.compile(r'href="/zonas/(urbano|rural)/([a-z\-]+)"', re.IGNORECASE)
VER_TODAS_URB_RE = re.compile(
    r'<a\s+href="/zonas/urbano/"[\s\S]*?Ver\s+todas\s+Urbano[\s\S]*?</a>',
    re.IGNORECASE,
)
VER_TODAS_RUR_RE = re.compile(
    r'<a\s+href="/zonas/rural/"[\s\S]*?Ver\s+todas\s+las\s+zonas[\s\S]*?</a>',
    re.IGNORECASE,
)


def expand(html: str) -> tuple[str, bool]:
    m = SUB_ZONAS_RE.search(html)
    if not m:
        return html, False
    inner = m.group(2)

    present_urb = set()
    present_rur = set()
    for hm in HREF_RE.finditer(inner):
        if hm.group(1).lower() == "urbano":
            present_urb.add(hm.group(2).lower())
        else:
            present_rur.add(hm.group(2).lower())

    missing_urb = [(s, l) for s, l in URBANAS if s.lower() not in present_urb]
    missing_rur = [(s, l) for s, l in RURALES if s.lower() not in present_rur]

    if not missing_urb and not missing_rur:
        return html, False

    new_inner = inner
    if missing_urb:
        block_urb = "\n                        ".join(
            render_link(s, l, "urbano") for s, l in missing_urb
        )
        block_urb_full = block_urb + "\n                        "
        new_inner_test = VER_TODAS_URB_RE.sub(
            lambda mm: block_urb_full + mm.group(0),
            new_inner,
            count=1,
        )
        if new_inner_test != new_inner:
            new_inner = new_inner_test
    if missing_rur:
        block_rur = "\n                        ".join(
            render_link(s, l, "rural") for s, l in missing_rur
        )
        block_rur_full = block_rur + "\n                        "
        new_inner_test = VER_TODAS_RUR_RE.sub(
            lambda mm: block_rur_full + mm.group(0),
            new_inner,
            count=1,
        )
        if new_inner_test != new_inner:
            new_inner = new_inner_test

    if new_inner == inner:
        return html, False

    return html[: m.start(2)] + new_inner + html[m.end(2):], True


def process_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    out, changed = expand(raw)
    if changed and not DRY:
        path.write_text(out, encoding="utf-8")
    return changed


def main() -> int:
    files = sorted(PUBLIC.rglob("*.html"))
    n = 0
    for f in files:
        if process_file(f):
            print(f"  {'[dry] ' if DRY else ''}{f.relative_to(PUBLIC)}")
            n += 1
    print(f"\nHTMLs modificados: {n}")
    if DRY:
        print("(dry-run)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
