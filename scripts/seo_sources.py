#!/usr/bin/env python3
"""
Inyecta una sección "Fuentes y referencias" al final del contenido de cada blog,
con citas verificables relevantes al tema. Idempotente.

Las fuentes están elegidas para mejorar señales E-E-A-T:
- Normativa chilena oficial (Ley Chile / SISS / MINSAL / SUBDERE)
- Estudios y agencias internacionales (EPA, WSU, ATSDR, NASSCO, Water UK)
- Trabajos académicos y técnicos (SciELO, iAgua)
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "public" / "blog"

MARKER = "<!-- sources-block -->"

# Fuentes individuales (id, título, url, descripción corta)
SRC = {
    # Chile - normativa
    "ds236": (
        "DS 236/1926 — Reglamento General de Alcantarillados Particulares (fosas sépticas, "
        "cámaras filtrantes y absorbentes), Biblioteca del Congreso Nacional de Chile.",
        "https://www.bcn.cl/leychile/Navegar?idNorma=171085",
    ),
    "ds4_2009": (
        "DS 4/2009 MINSEGPRES — Reglamento para el Manejo de Lodos generados en "
        "Plantas de Tratamiento de Aguas Servidas.",
        "https://www.bcn.cl/leychile/N?i=1007456",
    ),
    "ds609": (
        "DS 609/1998 MOP — Norma de emisión para descargas de RILes a sistemas "
        "de alcantarillado (límites para grasas, aceites y sólidos).",
        "https://www.bcn.cl/leychile/navegar?idNorma=121486",
    ),
    "ds10": (
        "DS 10/2010 MINSAL — Reglamento de condiciones sanitarias, ambientales y "
        "de seguridad para la realización de eventos masivos.",
        "https://www.bcn.cl/leychile/navegar?idNorma=1017350",
    ),
    "siss": (
        "Superintendencia de Servicios Sanitarios (SISS) — fiscaliza concesiones "
        "sanitarias y descargas a alcantarillado en Chile.",
        "https://www.siss.gob.cl/",
    ),
    "siss_consumo": (
        "SISS — Consumo de agua potable promedio en Chile (170 L/persona/día).",
        "https://www.siss.gob.cl/586/w3-article-7663.html",
    ),
    "subdere": (
        "SUBDERE — Manual de Soluciones de Saneamiento Sanitario para zonas rurales.",
        "https://www.subdere.gov.cl/sites/default/files/documentos/manual.pdf",
    ),
    "minsal_rsa": (
        "Ministerio de Salud de Chile — Reglamento Sanitario de los Alimentos (DS 977/96).",
        "https://www.minsal.cl/reglamento-sanitario-de-los-alimentos/",
    ),
    # Internacionales / científicas
    "epa_additives": (
        "U.S. EPA (2024) — Septic Tank Additives Fact Sheet: \"no scientific "
        "evidence that biological or chemical additives aid or are necessary "
        "for the operation of a properly functioning onsite system\".",
        "https://www.epa.gov/system/files/documents/2024-09/septictankadditivesfactsheet.pdf",
    ),
    "wadoh_additives": (
        "Washington State Department of Health — Listado de aditivos sépticos "
        "(la aprobación significa \"no tóxico\", NO eficacia).",
        "https://doh.wa.gov/sites/default/files/legacy/Documents/Pubs/337-025.pdf",
    ),
    "wsu_additives": (
        "WSU Extension — Septic Tank Additives: revisión de la evidencia y "
        "advertencias para propietarios.",
        "https://extension.wsu.edu/clark/naturalresources/smallacreageprogram/septic-tank-additives/",
    ),
    "pratt_pubmed": (
        "Pratt et al. (2008) — Septic tank additive impacts on microbial "
        "populations (estudio de 48 fosas, 12 meses): aditivos no tuvieron "
        "efecto significativo. PubMed.",
        "https://pubmed.ncbi.nlm.nih.gov/18236933/",
    ),
    "ftc_septic": (
        "FTC (2021) — Acción contra Environmental Safety International por "
        "marketing engañoso de productos sépticos (\"Activator 1000\").",
        "https://www.ftc.gov/news-events/news/press-releases/2021/07/ftc-takes-action-against-septic-tank-cleaning-company-made-millions-illegal-robocalls-consumers",
    ),
    "atsdr_formaldehido": (
        "ATSDR / CDC — Resumen de Salud Pública: Formaldehído (clasificado como "
        "carcinógeno humano por IARC).",
        "https://www.atsdr.cdc.gov/es/phs/es_phs111.html",
    ),
    "nassco_pacp": (
        "NASSCO — Pipeline Assessment Certification Program (PACP), estándar "
        "norteamericano de codificación de defectos en CCTV de alcantarillado.",
        "https://www.nassco.org/trenchless-technology/assessment/",
    ),
    "water_uk_fatbergs": (
        "Water UK — Fighting fatbergs: ~300.000 atascos al año en Reino Unido, "
        "costo aproximado £100M anuales (toallitas + grasas).",
        "https://www.water.org.uk/waste-water/fighting-fatbergs",
    ),
    "thames_wipes": (
        "Thames Water — Retira 3.800 millones de toallitas al año (£18M/año), "
        "incluye casos de fatbergs de 100 toneladas.",
        "https://www.thameswater.co.uk/news/2025/oct/thames-water-removes-100-tonne-fatberg",
    ),
    "iagua_fosa": (
        "iAgua / Juan José Salas — La humilde fosa séptica: fundamentos, tipos y diseño.",
        "https://www.iagua.es/blogs/juan-jose-salas/humilde-fosa-septica-fundamentos-tipos-y-diseno",
    ),
    "scielo_anaerobia": (
        "SciELO (Tecnología y Ciencias del Agua, 2012) — Digestión anaerobia "
        "de efluentes de fosas sépticas.",
        "https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S1405-77432012000300008",
    ),
    "une_16194": (
        "Norma UNE-EN 16194 — Cabinas sanitarias móviles no conectadas a la red "
        "de alcantarillado: requisitos y métodos de cálculo de unidades.",
        "https://www.une.org/encuentra-tu-norma/busca-tu-norma/norma?c=N0049834",
    ),
    "alar_quimica": (
        "Alar Química Chile — Insumos para baños químicos (proveedor industrial local).",
        "https://alarquimica.com/insumos-banos-quimicos/",
    ),
    "ley21442": (
        "Ley 21.442 (2022) — Nueva Ley de Copropiedad Inmobiliaria de Chile.",
        "https://www.bcn.cl/leychile/navegar?idNorma=1175479",
    ),
    "smart_water_olor": (
        "Smart Water Bio — Causas químicas y biológicas de olores en fosas sépticas (H₂S, "
        "mercaptanos).",
        "https://smartwaterbio.com/blog/fosa-septica-causas-procesos/",
    ),
    "rentokil_fog": (
        "Rentokil Chile — Importancia de las trampas de grasa en HORECA.",
        "https://www.rentokil.com/cl/blog/innovacion/importancia-de-una-trampa-de-grasa-en-restaurantes-hoteles-y-casinos",
    ),
}

# Mapeo: slug del blog → lista de IDs de fuentes (orden de relevancia)
MAP: dict[str, list[str]] = {
    "cuanto-cuesta-limpiar-fosa-septica-chile-2026": [
        "ds236", "ds4_2009", "siss", "subdere", "scielo_anaerobia",
    ],
    "cada-cuanto-limpiar-fosa-septica-segun-personas": [
        "siss_consumo", "ds236", "iagua_fosa", "scielo_anaerobia", "epa_additives",
    ],
    "biodigestor-vs-fosa-septica-cual-conviene-parcela": [
        "ds236", "subdere", "iagua_fosa", "scielo_anaerobia",
    ],
    "mal-olor-alcantarilla-casa-causas-soluciones": [
        "smart_water_olor", "epa_additives", "atsdr_formaldehido", "ds236",
    ],
    "raices-en-tuberias-detectar-eliminar-prevenir": [
        "nassco_pacp", "ds236",
    ],
    "inspeccion-camara-canerias-cuando-conviene-cuanto-cuesta": [
        "nassco_pacp", "siss",
    ],
    "pozo-absorbente-saturado-senales-causas-soluciones": [
        "ds236", "iagua_fosa", "scielo_anaerobia", "epa_additives",
    ],
    "senales-fosa-septica-al-limite": [
        "epa_additives", "ds236", "iagua_fosa",
    ],
    "hidrojet-vs-destape-mecanico-cual-elegir": [
        "nassco_pacp", "water_uk_fatbergs",
    ],
    "destape-cocina-restaurante-sushi": [
        "ds609", "rentokil_fog", "water_uk_fatbergs", "minsal_rsa",
    ],
    "por-que-se-tapa-desague-cocina": [
        "water_uk_fatbergs", "thames_wipes", "ds609",
    ],
    "prevenir-rebalse-alcantarillado-invierno-santiago": [
        "siss", "water_uk_fatbergs", "ds236",
    ],
    "inundacion-bano-que-hacer-primeros-minutos": [
        "siss", "ds236",
    ],
    "limpiar-canaletas-bajadas-agua-antes-invierno": [
        "siss",
    ],
    "quien-paga-destape-edificio-condominio-ley-chile": [
        "ley21442", "siss",
    ],
    "errores-pyme-contratan-destape-pirata": [
        "ds4_2009", "ds236", "ftc_septic", "siss",
    ],
    "destape-emergencia-cabanas-fin-semana-largo": [
        "ds236", "siss",
    ],
    "guia-mantencion-fosas-chicureo-pirque": [
        "ds236", "ds4_2009", "siss", "scielo_anaerobia",
    ],
    "como-destapar-wc-sin-romper-ceramica": [
        "thames_wipes", "water_uk_fatbergs",
    ],
    "como-destapar-lavaplatos-7-metodos-que-funcionan": [
        "water_uk_fatbergs", "ds609",
    ],
}


CTA_PATTERN = re.compile(
    r'(<div class="bg-brand-50 rounded-2xl p-8 mt-12 border border-brand-100 text-center">)'
)


def render_sources_block(ids: list[str]) -> str:
    items = []
    for sid in ids:
        if sid not in SRC:
            continue
        title, url = SRC[sid]
        items.append(
            f'<li><a href="{url}" target="_blank" rel="noopener nofollow" '
            f'class="text-blue-700 hover:underline">{title}</a></li>'
        )
    list_html = "\n              ".join(items)
    return f"""
        {MARKER}
        <section aria-label="Fuentes y referencias" class="mt-10 mb-2 bg-white border border-slate-200 rounded-2xl p-6">
            <h2 class="text-xl font-extrabold text-slate-900 m-0 mb-3 flex items-center gap-2">
              <i class="fa-solid fa-book-bookmark text-brand-600" aria-hidden="true"></i>
              Fuentes y referencias
            </h2>
            <p class="text-sm text-slate-600 m-0 mb-4">
              Donde aplicó usamos data oficial chilena (BCN, SISS, MINSAL) y referencias
              técnicas internacionales. Lo demás viene de nuestra propia experiencia en terreno
              en la Región Metropolitana.
            </p>
            <ul class="list-disc pl-6 space-y-2 text-sm text-slate-700">
              {list_html}
            </ul>
        </section>
"""


def process_file(slug: str, path: Path) -> bool:
    if slug not in MAP:
        return False
    src = path.read_text(encoding="utf-8")
    if MARKER in src:
        return False  # idempotente
    block = render_sources_block(MAP[slug])
    new = CTA_PATTERN.sub(block + r"\n            \1", src, count=1)
    if new == src:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def main() -> None:
    changed = []
    for f in sorted(BLOG.glob("*.html")):
        slug = f.stem
        if process_file(slug, f):
            changed.append(f.name)
    print(f"Modificados: {len(changed)}")
    for n in changed:
        print(f"  - {n}")


if __name__ == "__main__":
    main()
