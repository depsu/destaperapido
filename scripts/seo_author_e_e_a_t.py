#!/usr/bin/env python3
"""
Aplica E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) a los blogs:

1. Reemplaza autor genérico ("Equipo Destape Rápido", "Experto Sanitario") por
   "Alejandro Rivera Carrasco" en el header visual del artículo.
2. Actualiza el JSON-LD del autor a un Person con sameAs LinkedIn (señal E-E-A-T para Google).
3. Inserta un bloque visible de bio del autor antes del CTA final.

Diseñado para correr de forma idempotente: si ya aplicó el cambio, no lo duplica.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "public" / "blog"

AUTHOR_NAME = "Alejandro Rivera Carrasco"
AUTHOR_LINKEDIN = "https://www.linkedin.com/in/alejandro-rivera-carrasco-61436b182/"
AUTHOR_IMG = "https://www.destaperapido.cl/images/autor-alejandro-rivera.svg"
AUTHOR_PAGE = "https://www.destaperapido.cl/nosotros"
AUTHOR_TITLE = "Especialista en saneamiento y destape industrial · 10+ años en terreno"
AUTHOR_BIO = (
    "Lleva más de una década dirigiendo operaciones de destape, limpieza de "
    "fosas e inspección con cámara en la Región Metropolitana. Trabaja a diario "
    "con condominios, parcelas, restaurantes y empresas, y conoce de primera "
    "mano qué funciona, qué es marketing y qué simplemente no se debe hacer "
    "con el sistema sanitario."
)

# ------------------------------------------------------------------
# 1) Header visual del artículo
# ------------------------------------------------------------------
# El header tiene un span con icono y nombre del autor. Cubrimos las dos
# variantes que vimos en el repo.
HEADER_REPLACEMENTS = [
    ("Equipo Destape Rápido", AUTHOR_NAME),
    ("Experto Sanitario", AUTHOR_NAME),
]


def update_header(html: str) -> str:
    for old, new in HEADER_REPLACEMENTS:
        # Solo reemplazamos cuando aparece dentro del bloque del autor del header
        # (icono fa-user adyacente). Patrón conservador.
        pattern = re.compile(
            r'(<i class="fa-regular fa-user[^"]*"[^>]*></i>\s*)' + re.escape(old)
        )
        html = pattern.sub(r"\1" + new, html)
    return html


# ------------------------------------------------------------------
# 2) JSON-LD: autor pasa a ser Person con sameAs LinkedIn
# ------------------------------------------------------------------
def update_jsonld_author(html: str) -> str:
    # Patrón: bloque "author" con name "Equipo Destape Rápido"
    # Lo reemplazamos por un Person estructurado (mantiene compatibilidad con BlogPosting).
    pattern = re.compile(
        r'"author":\s*\{[^{}]*?"name":\s*"(?:Equipo Destape Rápido|Experto Sanitario)"[^{}]*?\}',
        re.DOTALL,
    )
    new_author = (
        '"author": {\n'
        '      "@type": "Person",\n'
        f'      "name": "{AUTHOR_NAME}",\n'
        '      "jobTitle": "Especialista en saneamiento",\n'
        f'      "url": "{AUTHOR_PAGE}",\n'
        f'      "image": "{AUTHOR_IMG}",\n'
        f'      "sameAs": ["{AUTHOR_LINKEDIN}"],\n'
        '      "worksFor": { "@id": "https://www.destaperapido.cl/#business" }\n'
        '    }'
    )
    return pattern.sub(new_author, html)


# ------------------------------------------------------------------
# 3) Bloque visible de bio del autor (antes del CTA final)
# ------------------------------------------------------------------
AUTHOR_BLOCK_MARKER = "<!-- author-bio-block -->"

AUTHOR_BLOCK = f"""
        {AUTHOR_BLOCK_MARKER}
        <aside aria-label="Sobre el autor" class="mt-12 mb-2 bg-slate-50 border border-slate-200 rounded-2xl p-6 flex flex-col sm:flex-row gap-5 items-center sm:items-start">
            <img src="/images/autor-alejandro-rivera.svg" alt="Foto de Alejandro Rivera Carrasco, especialista en saneamiento" class="w-20 h-20 rounded-full border-2 border-brand-200 shadow-sm shrink-0" width="80" height="80" loading="lazy" decoding="async">
            <div class="text-center sm:text-left">
                <p class="text-xs uppercase tracking-wide text-brand-600 font-bold mb-1">Sobre el autor</p>
                <p class="text-lg font-extrabold text-slate-900 m-0">{AUTHOR_NAME}</p>
                <p class="text-sm text-slate-500 m-0 mb-2">{AUTHOR_TITLE}</p>
                <p class="text-sm text-slate-700 m-0 mb-3">{AUTHOR_BIO}</p>
                <a href="{AUTHOR_LINKEDIN}" target="_blank" rel="noopener nofollow" class="inline-flex items-center gap-2 text-sm font-semibold text-blue-700 hover:underline">
                    <i class="fa-brands fa-linkedin" aria-hidden="true"></i>
                    Perfil en LinkedIn
                </a>
            </div>
        </aside>
"""

# Ancla: el div del CTA "¿Necesitas ayuda profesional?" que aparece al final.
CTA_PATTERN = re.compile(
    r'(<div class="bg-brand-50 rounded-2xl p-8 mt-12 border border-brand-100 text-center">)'
)


def insert_author_block(html: str) -> str:
    if AUTHOR_BLOCK_MARKER in html:
        return html  # idempotente
    return CTA_PATTERN.sub(AUTHOR_BLOCK + r"\n            \1", html, count=1)


# ------------------------------------------------------------------
# Pipeline
# ------------------------------------------------------------------
def process_file(path: Path) -> bool:
    src = path.read_text(encoding="utf-8")
    out = src
    out = update_header(out)
    out = update_jsonld_author(out)
    out = insert_author_block(out)
    if out != src:
        path.write_text(out, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    skipped = []
    for f in sorted(BLOG.glob("*.html")):
        if f.name == "index.html":
            continue
        if process_file(f):
            changed.append(f.name)
        else:
            skipped.append(f.name)
    print(f"Modificados: {len(changed)}")
    for n in changed:
        print(f"  - {n}")
    if skipped:
        print(f"Sin cambios: {len(skipped)}")
        for n in skipped:
            print(f"  - {n}")


if __name__ == "__main__":
    main()
