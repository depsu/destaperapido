#!/usr/bin/env python3
"""
Complemento de seo_author_e_e_a_t.py + seo_sources.py para los 4 blogs que usan
la plantilla alternativa (CTA con gradiente naranja). Cubre:

- Reemplazo de autor "Organization → Destape Rápido" por Person Alejandro Rivera Carrasco
  (manteniendo publisher como Organization).
- Inserción del bloque visible de bio del autor antes del CTA gradiente.
- Inserción del bloque de fuentes según slug.

Idempotente.
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

AUTHOR_BLOCK_MARKER = "<!-- author-bio-block -->"
SOURCES_MARKER = "<!-- sources-block -->"

# Reusa fuentes del seo_sources.py
import importlib.util

spec = importlib.util.spec_from_file_location(
    "seo_sources", ROOT / "scripts" / "seo_sources.py"
)
seo_sources = importlib.util.module_from_spec(spec)
spec.loader.exec_module(seo_sources)


# CTA alterno: gradient
CTA_ALT_PATTERN = re.compile(
    r'(<div class="bg-gradient-to-br from-brand-600 to-brand-700[^"]*">)'
)


def update_jsonld_author_alt(html: str) -> str:
    """Reemplaza el author Organization por Person, sin tocar el publisher."""
    pattern = re.compile(
        r'"author":\s*\{\s*"@type":\s*"Organization",\s*"name":\s*"Destape Rápido",\s*"url":\s*"https://www\.destaperapido\.cl"\s*\}'
    )
    new_author = (
        '"author": {\n'
        '    "@type": "Person",\n'
        f'    "name": "{AUTHOR_NAME}",\n'
        '    "jobTitle": "Especialista en saneamiento",\n'
        f'    "url": "{AUTHOR_PAGE}",\n'
        f'    "image": "{AUTHOR_IMG}",\n'
        f'    "sameAs": ["{AUTHOR_LINKEDIN}"],\n'
        '    "worksFor": { "@type": "Organization", "name": "Destape Rápido", "url": "https://www.destaperapido.cl" }\n'
        '  }'
    )
    return pattern.sub(new_author, html)


def author_block_html(card_classes: str = "bg-slate-50") -> str:
    return f"""
        {AUTHOR_BLOCK_MARKER}
        <aside aria-label="Sobre el autor" class="mt-12 mb-2 {card_classes} border border-slate-200 rounded-2xl p-6 flex flex-col sm:flex-row gap-5 items-center sm:items-start">
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


def insert_author_block_alt(html: str) -> str:
    if AUTHOR_BLOCK_MARKER in html:
        return html
    block = author_block_html("bg-white")
    return CTA_ALT_PATTERN.sub(block + r"\n            \1", html, count=1)


def insert_sources_alt(slug: str, html: str) -> str:
    if SOURCES_MARKER in html:
        return html
    if slug not in seo_sources.MAP:
        return html
    block = seo_sources.render_sources_block(seo_sources.MAP[slug])
    return CTA_ALT_PATTERN.sub(block + r"\n            \1", html, count=1)


def process_file(path: Path) -> bool:
    src = path.read_text(encoding="utf-8")
    out = src
    out = update_jsonld_author_alt(out)
    out = insert_author_block_alt(out)
    out = insert_sources_alt(path.stem, out)
    if out != src:
        path.write_text(out, encoding="utf-8")
        return True
    return False


TARGETS = [
    "destape-cocina-restaurante-sushi.html",
    "errores-pyme-contratan-destape-pirata.html",
    "inundacion-bano-que-hacer-primeros-minutos.html",
    "destape-emergencia-cabanas-fin-semana-largo.html",
]


def main() -> None:
    for name in TARGETS:
        f = BLOG / name
        if not f.exists():
            print(f"  - {name}: NO EXISTE")
            continue
        changed = process_file(f)
        print(f"  - {name}: {'modificado' if changed else 'sin cambios'}")


if __name__ == "__main__":
    main()
