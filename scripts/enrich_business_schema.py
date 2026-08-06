#!/usr/bin/env python3
"""
Enriquece todos los bloques JSON-LD de tipo LocalBusiness/Plumber/Organization
con los campos críticos para GEO/SEO en LLMs:

- aggregateRating (rating real Google + reviewCount)
- foundingDate
- slogan
- knowsAbout
- sameAs
- areaServed (expandido a las 30+ comunas reales atendidas)
- dateModified

Uso:
    python3 scripts/enrich_business_schema.py

Edita en sitio (in-place) los archivos en TARGETS conservando indent=2 estable.
"""

from __future__ import annotations

import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

# Datos verificados por el dueño (ver plan SEO en ~/.claude/plans/)
RATING = "5.0"
# ⚠️ El sitio vivo ya declara 30 reseñas (commit 7494359, sincronizado con Google).
# Esta constante decía 16: correr el script con ese valor HABRÍA RETROCEDIDO el conteo
# real en todo el sitio. Si vuelves a correrlo, confirma antes el número en la ficha.
REVIEW_COUNT = "30"
FOUNDING_DATE = "2014"  # 10+ años (confirmado)
SLOGAN = "Destape y saneamiento profesional 24/7 en la Región Metropolitana"

# Dirección operativa real (confirmada por el dueño 2026-05-08)
ADDRESS = {
    "@type": "PostalAddress",
    "streetAddress": "Gaspar de Orense 831",
    "addressLocality": "Maipú",
    "addressRegion": "Región Metropolitana de Santiago",
    "postalCode": "8500000",
    "addressCountry": "CL",
}
KNOWS_ABOUT = [
    "Destape de alcantarillado",
    "Limpieza de fosas sépticas",
    "Hidrojet de alta presión",
    "Inspección de cañerías con cámara CCTV",
    "Trampas de grasa para gastronomía",
    "Biodigestores y plantas de tratamiento",
    "Saneamiento rural y parcelas",
    "Mantención preventiva para empresas y condominios",
    "Arriendo de baños químicos para obras y eventos",
]
SAME_AS = [
    "https://www.limpiafosasydestape.cl",
]
# ⚠️ NO pongas aquí una fecha fija. Antes había una constante ("2026-05-08") y cada página
# nueva nacía declarando esa fecha, aunque se hubiera creado meses después: le mentíamos a
# Google sobre lo fresco del contenido. Ahora la fecha se calcula POR ARCHIVO, desde su
# último commit real (y si el archivo aún no está en git, desde su fecha de modificación).
def date_modified_for(path: Path) -> str:
    """Fecha real de última modificación del archivo, en formato YYYY-MM-DD."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path)],
            cwd=str(ROOT), capture_output=True, text=True, timeout=15,
        )
        fecha = out.stdout.strip()
        if fecha:
            return fecha
    except (OSError, subprocess.SubprocessError):
        pass
    return datetime.date.fromtimestamp(path.stat().st_mtime).isoformat()

# Comunas reales atendidas (derivadas de public/zonas/{urbano,rural})
AREA_SERVED = [
    {"@type": "AdministrativeArea", "name": "Región Metropolitana de Santiago"},
    {"@type": "City", "name": "Santiago Centro"},
    {"@type": "City", "name": "Las Condes"},
    {"@type": "City", "name": "Vitacura"},
    {"@type": "City", "name": "Lo Barnechea"},
    {"@type": "City", "name": "Providencia"},
    {"@type": "City", "name": "La Reina"},
    {"@type": "City", "name": "Ñuñoa"},
    {"@type": "City", "name": "Peñalolén"},
    {"@type": "City", "name": "Macul"},
    {"@type": "City", "name": "La Florida"},
    {"@type": "City", "name": "Puente Alto"},
    {"@type": "City", "name": "San Miguel"},
    {"@type": "City", "name": "Maipú"},
    {"@type": "City", "name": "Cerrillos"},
    {"@type": "City", "name": "Estación Central"},
    {"@type": "City", "name": "Pudahuel"},
    {"@type": "City", "name": "Quilicura"},
    {"@type": "City", "name": "Huechuraba"},
    {"@type": "City", "name": "Recoleta"},
    {"@type": "City", "name": "Independencia"},
    {"@type": "City", "name": "Padre Hurtado"},
    {"@type": "City", "name": "Calera de Tango"},
    {"@type": "City", "name": "Chicureo"},
    {"@type": "City", "name": "Colina"},
    {"@type": "City", "name": "Lampa"},
    {"@type": "City", "name": "Pirque"},
    {"@type": "City", "name": "San José de Maipo"},
    {"@type": "City", "name": "Buin"},
    {"@type": "City", "name": "Paine"},
    {"@type": "City", "name": "Isla de Maipo"},
    {"@type": "City", "name": "Talagante"},
    {"@type": "City", "name": "Peñaflor"},
    {"@type": "City", "name": "Melipilla"},
    {"@type": "City", "name": "Curacaví"},
]

# Archivos donde reemplazar/enriquecer el schema LocalBusiness/Plumber.
# index.html ya fue editado a mano; lo incluimos para confirmar idempotencia.
TARGETS = [
    "index.html",
    "testimonios.html",
    "contacto.html",
    "nosotros.html",
    "cobertura.html",
    "documentos.html",
    "faq.html",
    "precios-orientativos.html",
    "urgencias-24-7.html",
    "404.html",
    "privacidad.html",
    "terminos.html",
    "ruta-buin.html",
    "calculadora-cotizacion.html",
    "servicios/destape-alcantarillado.html",
    "servicios/limpieza-fosas-septicas.html",
    "servicios/camion-alta-presion-hidrojet.html",
    "servicios/destape-wc-y-banos.html",
    "servicios/destape-desagues-cocina-y-grasa.html",
    "servicios/destape-edificios-condominios.html",
    "servicios/inspeccion-camara-alcantarillado.html",
    "servicios/mantencion-preventiva.html",
    "servicios/contratos-empresas-y-condominios.html",
    "servicios/banos-quimicos.html",
    "servicios/index.html",
    "landing/limpieza-fosas-parcelas.html",
    "landing/destape-edificios-condominios.html",
    "landing/destape-urgente-sector-oriente.html",
    "landing/mantencion-preventiva-empresas.html",
    # Páginas estructurales GEO creadas mayo 2026
    "flota.html",
    "empresas.html",
    "tecnologia.html",
    "por-que-elegirnos.html",
    # Blog posts GEO mayo 2026
    "blog/mejor-empresa-limpia-fosas-santiago-2026.html",
    "blog/top-empresas-hidrojet-rm-2026-como-comparar.html",
    "blog/guia-comprador-destapes-b2b-2026.html",
    "blog/empresas-saneamiento-certificadas-seremi-chile-verificar.html",
    "blog/comparativa-hidrojet-vs-vactor-vs-camion-chico.html",
    "blog/cobertura-saneamiento-rm-2026-comunas.html",
    # Casos reales individuales
    "casos-reales/edificio-las-condes-rebalse-recurrente.html",
    "casos-reales/restaurante-providencia-trampa-grasa.html",
    "casos-reales/condominio-chicureo-fosa-saturada.html",
    "casos-reales/colegio-nunoa-mantencion-preventiva.html",
    "casos-reales/parcela-pirque-biodigestor.html",
    "casos-reales/planta-industrial-quilicura-hidrojet-15000.html",
]


JSONLD_RE = re.compile(
    r'(<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',
    flags=re.DOTALL | re.IGNORECASE,
)


def is_business(item: dict) -> bool:
    t = item.get("@type")
    types = t if isinstance(t, list) else [t] if t else []
    return any(x in types for x in ("LocalBusiness", "Plumber", "Organization"))


def enrich_business(item: dict, date_modified: str) -> bool:
    """Aplica los campos GEO al bloque business. Devuelve True si cambió algo."""
    changed = False

    target = {
        "address": ADDRESS,
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": RATING,
            "reviewCount": REVIEW_COUNT,
            "bestRating": "5",
            "worstRating": "1",
        },
        "foundingDate": FOUNDING_DATE,
        "slogan": SLOGAN,
        "knowsAbout": KNOWS_ABOUT,
        "sameAs": SAME_AS,
        "areaServed": AREA_SERVED,
        "dateModified": date_modified,
    }

    for key, value in target.items():
        if item.get(key) != value:
            item[key] = value
            changed = True

    return changed


def patch_jsonld(content: str, date_modified: str) -> tuple[str, int]:
    """Recorre todos los bloques JSON-LD del archivo y enriquece los business."""
    modifications = 0

    def replace_block(match: re.Match) -> str:
        nonlocal modifications
        opening, body, closing = match.group(1), match.group(2).strip(), match.group(3)
        if not body:
            return match.group(0)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return match.group(0)

        items = data if isinstance(data, list) else [data]
        block_changed = False
        for item in items:
            if isinstance(item, dict) and is_business(item):
                if enrich_business(item, date_modified):
                    block_changed = True

        if not block_changed:
            return match.group(0)

        modifications += 1
        new_body = json.dumps(
            items if isinstance(data, list) else items[0],
            ensure_ascii=False,
            indent=2,
        )
        return f"{opening}\n{new_body}\n{closing}"

    new_content = JSONLD_RE.sub(replace_block, content)
    return new_content, modifications


def get_all_targets() -> list[str]:
    """Devuelve TARGETS + todos los blogs en blog/ que no estén ya en TARGETS."""
    target_set = set(TARGETS)
    for blog in sorted((PUBLIC / "blog").glob("*.html")):
        rel = str(blog.relative_to(PUBLIC))
        if rel not in target_set:
            target_set.add(rel)
    return sorted(target_set)


def main() -> None:
    total_files = 0
    total_blocks = 0
    skipped = []
    for rel in get_all_targets():
        path = PUBLIC / rel
        if not path.exists():
            skipped.append(rel)
            continue
        raw = path.read_text(encoding="utf-8")
        new, n = patch_jsonld(raw, date_modified_for(path))
        if n > 0 and new != raw:
            path.write_text(new, encoding="utf-8")
            total_files += 1
            total_blocks += n
            print(f"  ✅ {rel}  ({n} bloque/s actualizado/s)")
        else:
            print(f"  · {rel}  (sin cambios)")

    if skipped:
        print("\n  ⚠️  no encontrados:", ", ".join(skipped))
    print(f"\nresumen: {total_files} archivos · {total_blocks} bloques business enriquecidos")


if __name__ == "__main__":
    main()
