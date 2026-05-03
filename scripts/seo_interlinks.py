#!/usr/bin/env python3
"""
Inyecta bloques de enlazado interno contextual en páginas de servicio y blog
que no los tengan. Mejora distribución de equity y reduce páginas casi-huérfanas.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
DRY = "--dry-run" in sys.argv

# Marcador para evitar dupes
MARKER_SVC = "<!-- seo-related-services -->"
MARKER_BLOG = "<!-- seo-related-articles -->"

FOOTER_OPEN = '<footer class="bg-slate-50 text-slate-500 py-12 text-sm border-t border-slate-200">'

# Catálogo de páginas para construir enlaces
SERVICES = [
    ("/servicios/destape-alcantarillado", "Destape de alcantarillado", "fa-faucet-drip"),
    ("/servicios/limpieza-fosas-septicas", "Limpieza de fosas sépticas", "fa-truck-droplet"),
    ("/servicios/destape-wc-y-banos", "Destape de WC y baños", "fa-toilet"),
    ("/servicios/destape-desagues-cocina-y-grasa", "Destape de desagües y grasa", "fa-bowl-food"),
    ("/servicios/camion-alta-presion-hidrojet", "Camión hidrojet alta presión", "fa-spray-can"),
    ("/servicios/contratos-empresas-y-condominios", "Contratos para empresas", "fa-file-signature"),
    ("/servicios/inspeccion-camara-alcantarillado", "Inspección con cámara HD", "fa-camera"),
    ("/servicios/destape-edificios-condominios", "Destape edificios y condominios", "fa-building"),
    ("/servicios/mantencion-preventiva", "Mantención preventiva", "fa-shield-halved"),
    ("/servicios/banos-quimicos", "Arriendo de baños químicos", "fa-restroom"),
]

ZONES_URBAN = [
    ("/zonas/urbano/las-condes", "Las Condes"),
    ("/zonas/urbano/vitacura", "Vitacura"),
    ("/zonas/urbano/lo-barnechea", "Lo Barnechea"),
    ("/zonas/urbano/providencia", "Providencia"),
    ("/zonas/urbano/nunoa", "Ñuñoa"),
    ("/zonas/urbano/la-reina", "La Reina"),
]

ZONES_RURAL = [
    ("/zonas/rural/chicureo", "Chicureo"),
    ("/zonas/rural/colina", "Colina"),
    ("/zonas/rural/lampa", "Lampa"),
    ("/zonas/rural/pirque", "Pirque"),
    ("/zonas/rural/buin-paine", "Buin / Paine"),
    ("/zonas/rural/talagante", "Talagante"),
    ("/zonas/rural/penaflor", "Peñaflor"),
    ("/zonas/rural/padre-hurtado", "Padre Hurtado"),
    ("/zonas/rural/melipilla", "Melipilla"),
    ("/zonas/rural/curacavi", "Curacaví"),
]

BLOG_POSTS = [
    ("/blog/cuanto-cuesta-limpiar-fosa-septica-chile-2026", "Cuánto cuesta limpiar una fosa séptica en Chile (2026)"),
    ("/blog/cada-cuanto-limpiar-fosa-septica-segun-personas", "Cada cuánto limpiar la fosa según N° de personas"),
    ("/blog/como-destapar-wc-sin-romper-ceramica", "Cómo destapar un WC sin romper la cerámica"),
    ("/blog/hidrojet-vs-destape-mecanico-cual-elegir", "Hidrojet vs destape mecánico: cuál elegir"),
    ("/blog/por-que-se-tapa-desague-cocina", "Por qué se tapa el desagüe de la cocina"),
    ("/blog/senales-fosa-septica-al-limite", "Señales de que tu fosa séptica está al límite"),
    ("/blog/guia-mantencion-fosas-chicureo-pirque", "Mantención de fosas en Chicureo y Pirque"),
]


def html_related_services_block(current_slug: str) -> str:
    """Bloque de 6 servicios + 4 zonas urbano/rural + parcelas, excluyendo current."""
    others = [s for s in SERVICES if s[0] != current_slug][:6]
    zones = (
        ZONES_URBAN[:2]
        + ZONES_RURAL[:2]
        + [("/zonas/parcelas-y-condominios-cerrados", "Parcelas y condominios")]
    )
    svc_html = "\n".join(
        f'''        <a href="{url}" class="flex items-center gap-3 p-4 bg-white rounded-xl border border-slate-200 hover:border-blue-500 hover:shadow-md transition group">
          <i class="fa-solid {icon} text-blue-600 text-xl"></i>
          <span class="font-semibold text-slate-700 group-hover:text-blue-700">{label}</span>
        </a>'''
        for url, label, icon in others
    )
    zone_html = " · ".join(
        f'<a href="{url}" class="text-blue-600 hover:underline font-medium">{name}</a>'
        for url, name in zones
    )
    return f"""    {MARKER_SVC}
    <section aria-labelledby="related-services-title" class="bg-slate-50 py-16 px-4 border-t border-slate-200">
      <div class="max-w-6xl mx-auto">
        <h2 id="related-services-title" class="text-2xl md:text-3xl font-bold text-slate-800 mb-2">Otros servicios que te pueden interesar</h2>
        <p class="text-slate-600 mb-8">Cobertura integral de saneamiento en la Región Metropolitana — sin romper, con maquinaria propia y atención 24/7.</p>
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
{svc_html}
        </div>
        <p class="mt-8 text-sm text-slate-600">
          <span class="font-semibold">Zonas más solicitadas:</span> {zone_html} · <a href="/cobertura" class="text-blue-600 hover:underline">ver todas las comunas que cubrimos</a>.
        </p>
      </div>
    </section>
"""


def html_related_articles_block(current_slug: str) -> str:
    others = [b for b in BLOG_POSTS if b[0] != current_slug][:3]
    items = "\n".join(
        f'''        <a href="{url}" class="block p-5 bg-white rounded-xl border border-slate-200 hover:border-blue-500 hover:shadow-md transition">
          <span class="text-xs uppercase tracking-wide text-blue-600 font-bold">Sigue leyendo</span>
          <h3 class="mt-2 font-bold text-slate-800">{title}</h3>
        </a>'''
        for url, title in others
    )
    return f"""    {MARKER_BLOG}
    <section aria-labelledby="related-articles-title" class="bg-slate-50 py-12 px-4 border-t border-slate-200">
      <div class="max-w-5xl mx-auto">
        <h2 id="related-articles-title" class="text-2xl font-bold text-slate-800 mb-6">Artículos relacionados</h2>
        <div class="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
{items}
        </div>
        <p class="mt-6 text-sm text-slate-600">
          ¿Necesitas el servicio ahora? <a href="/contacto" class="text-blue-600 hover:underline font-semibold">Cotiza por WhatsApp</a> o revisa nuestras <a href="/servicios/" class="text-blue-600 hover:underline font-semibold">páginas de servicio</a>.
        </p>
      </div>
    </section>
"""


def replace_or_insert(content: str, snippet: str, marker: str) -> str:
    """Si existe un bloque previo con `marker`, reemplazarlo. Si no, insertar antes del footer."""
    if marker in content:
        # Quitar el bloque previo: desde marker hasta cierre </section>
        pattern = re.compile(
            rf"\s*{re.escape(marker)}.*?</section>\s*",
            re.DOTALL,
        )
        content = pattern.sub("\n    ", content, count=1)
    if FOOTER_OPEN not in content:
        return content
    return content.replace(FOOTER_OPEN, f"{snippet}\n    {FOOTER_OPEN}", 1)


def process_service(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    rel_url = "/" + str(path.relative_to(PUBLIC)).replace("\\", "/").replace(".html", "")
    block = html_related_services_block(rel_url)
    new = replace_or_insert(raw, block, MARKER_SVC)
    if new == raw:
        return False
    if not DRY:
        path.write_text(new, encoding="utf-8")
    return True


def process_blog_post(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    rel_url = "/" + str(path.relative_to(PUBLIC)).replace("\\", "/").replace(".html", "")
    block = html_related_articles_block(rel_url)
    new = replace_or_insert(raw, block, MARKER_BLOG)
    if new == raw:
        return False
    if not DRY:
        path.write_text(new, encoding="utf-8")
    return True


def main() -> None:
    changed: list[str] = []
    for f in sorted(PUBLIC.glob("servicios/*.html")):
        if f.name in ("test.html", "index.html"):
            continue
        if process_service(f):
            changed.append(str(f.relative_to(ROOT)))

    for f in sorted(PUBLIC.glob("blog/*.html")):
        if f.name == "index.html":
            continue
        if process_blog_post(f):
            changed.append(str(f.relative_to(ROOT)))

    print(f"{'[dry-run] ' if DRY else ''}páginas con interlinks añadidos: {len(changed)}")
    for c in changed:
        print(f"  - {c}")


if __name__ == "__main__":
    main()
