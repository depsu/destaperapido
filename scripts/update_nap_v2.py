#!/usr/bin/env python3
"""
Actualiza el NAP en todas las páginas del sitio para reflejar:

1. Empresa SERVICE AREA BUSINESS — sin streetAddress ni postalCode en schema.org
   (la dirección legal Andalucía 3661 queda solo para SII, no se expone públicamente).
2. Añade Instagram y Facebook reales al footer (hoy son href="/" placeholder).
3. Añade Google Business, Facebook e Instagram al array `sameAs` del JSON-LD.

Ejecutar desde la raíz del repo:
    python3 scripts/update_nap_v2.py

Es idempotente: si ya se aplicó, no rompe.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

# --- URLs canónicas ---
URL_FACEBOOK = "https://www.facebook.com/profile.php?id=61586933706026"
URL_INSTAGRAM = "https://www.instagram.com/destaperapidorm/"
URL_GOOGLE_BUSINESS = "https://maps.app.goo.gl/e97qNtXnJ37A5cWe9"
URL_EMPRESA_HERMANA = "https://www.limpiafosasydestape.cl"

# --- Patrones de schema.org a remover ---
RE_STREET_ADDRESS = re.compile(
    r'^\s*"streetAddress":\s*"Gaspar de Orense 831",?\s*\n',
    re.MULTILINE,
)
RE_POSTAL_CODE = re.compile(
    r'^\s*"postalCode":\s*"8500000",?\s*\n',
    re.MULTILINE,
)

# --- Reemplazo de hrefs sociales en footer ---
# Patrón 1 (footer principal, iconos grandes)
FB_OLD_1 = '<a href="/" class="text-slate-500 hover:text-brand-600 transition" aria-label="Facebook">'
FB_NEW_1 = f'<a href="{URL_FACEBOOK}" target="_blank" rel="noopener noreferrer" class="text-slate-500 hover:text-brand-600 transition" aria-label="Facebook">'

IG_OLD_1 = '<a href="/" class="text-slate-500 hover:text-brand-600 transition" aria-label="Instagram">'
IG_NEW_1 = f'<a href="{URL_INSTAGRAM}" target="_blank" rel="noopener noreferrer" class="text-slate-500 hover:text-brand-600 transition" aria-label="Instagram">'

# Patrón 2 (footer copyright, iconos pequeños)
FB_OLD_2 = '<a href="/" class="hover:text-slate-800 transition" aria-label="Facebook">'
FB_NEW_2 = f'<a href="{URL_FACEBOOK}" target="_blank" rel="noopener noreferrer" class="hover:text-slate-800 transition" aria-label="Facebook">'

IG_OLD_2 = '<a href="/" class="hover:text-slate-800 transition" aria-label="Instagram">'
IG_NEW_2 = f'<a href="{URL_INSTAGRAM}" target="_blank" rel="noopener noreferrer" class="hover:text-slate-800 transition" aria-label="Instagram">'

# --- sameAs en JSON-LD ---
# Solo enriquece si el sameAs tiene únicamente el dominio hermano
SAMEAS_OLD = (
    '"sameAs": [\n'
    '    "https://www.limpiafosasydestape.cl"\n'
    '  ]'
)
SAMEAS_NEW = (
    '"sameAs": [\n'
    f'    "{URL_GOOGLE_BUSINESS}",\n'
    f'    "{URL_FACEBOOK}",\n'
    f'    "{URL_INSTAGRAM}",\n'
    f'    "{URL_EMPRESA_HERMANA}"\n'
    '  ]'
)

def process_html(path: Path) -> dict:
    """Aplica todos los reemplazos a un HTML. Devuelve dict con cambios."""
    text = path.read_text(encoding="utf-8")
    original = text
    changes = {
        "street_removed": 0,
        "postal_removed": 0,
        "fb_links_updated": 0,
        "ig_links_updated": 0,
        "sameas_enriched": 0,
    }

    # 1. Remover líneas de streetAddress y postalCode
    text, n = RE_STREET_ADDRESS.subn("", text)
    changes["street_removed"] = n

    text, n = RE_POSTAL_CODE.subn("", text)
    changes["postal_removed"] = n

    # 2. Reemplazar hrefs sociales
    if FB_OLD_1 in text:
        text = text.replace(FB_OLD_1, FB_NEW_1)
        changes["fb_links_updated"] += 1
    if FB_OLD_2 in text:
        text = text.replace(FB_OLD_2, FB_NEW_2)
        changes["fb_links_updated"] += 1
    if IG_OLD_1 in text:
        text = text.replace(IG_OLD_1, IG_NEW_1)
        changes["ig_links_updated"] += 1
    if IG_OLD_2 in text:
        text = text.replace(IG_OLD_2, IG_NEW_2)
        changes["ig_links_updated"] += 1

    # 3. Enriquecer sameAs
    if SAMEAS_OLD in text:
        text = text.replace(SAMEAS_OLD, SAMEAS_NEW)
        changes["sameas_enriched"] = 1

    if text != original:
        path.write_text(text, encoding="utf-8")
        return changes
    return None


def process_llms_txt(path: Path) -> bool:
    """Actualiza la línea de dirección operativa en llms.txt."""
    text = path.read_text(encoding="utf-8")
    original = text
    # Reemplazo de línea completa (manejamos ambas variantes con/sin paréntesis)
    text = re.sub(
        r"- \*\*Dirección operativa:\*\* Gaspar de Orense 831[^\n]*",
        "- **Dirección operativa:** Empresa de servicios a domicilio. No atendemos en oficina al público. Cobertura: toda la Región Metropolitana (urbano + rural). Casilla legal en Maipú (consultar por facturación).",
        text,
    )
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    if not PUBLIC.exists():
        print(f"ERROR: no existe {PUBLIC}", file=sys.stderr)
        sys.exit(1)

    html_files = list(PUBLIC.rglob("*.html"))
    totals = {
        "files_changed": 0,
        "street_removed": 0,
        "postal_removed": 0,
        "fb_links_updated": 0,
        "ig_links_updated": 0,
        "sameas_enriched": 0,
    }
    for html in html_files:
        result = process_html(html)
        if result:
            totals["files_changed"] += 1
            for k, v in result.items():
                totals[k] += v
            print(f"OK  {html.relative_to(ROOT)}  {result}")

    # llms.txt
    llms = PUBLIC / "llms.txt"
    if llms.exists() and process_llms_txt(llms):
        print(f"OK  {llms.relative_to(ROOT)}  (línea de dirección operativa actualizada)")
        totals["files_changed"] += 1

    print("\n=== RESUMEN ===")
    for k, v in totals.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
