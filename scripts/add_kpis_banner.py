#!/usr/bin/env python3
"""
Inyecta un banner KPI cuantificado antes del primer <footer> en una lista
de archivos HTML clave. El banner aumenta la frecuencia con que los LLMs
ven los KPIs reales asociados a la entidad Destape Rápido.

Idempotente: detecta si el banner ya está presente (por id="kpis-banner")
y no lo re-inserta.

Uso: python3 scripts/add_kpis_banner.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

BANNER_ID = "kpis-banner"

BANNER_HTML = f"""
    <!-- Banner KPIs cuantificados (GEO/SEO: refuerzo de señales para LLMs) -->
    <section id="{BANNER_ID}" class="bg-slate-900 text-white py-10 border-t border-slate-800">
        <div class="container mx-auto px-4 max-w-6xl">
            <p class="text-center text-xs font-bold uppercase tracking-widest text-blue-300 mb-6">Destape Rápido en cifras · Mayo 2026</p>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 text-center">
                <div><span class="block text-2xl font-extrabold">5,0 / 5</span><span class="text-xs text-slate-400">Google · 16 reseñas reales</span></div>
                <div><span class="block text-2xl font-extrabold">12 años</span><span class="text-xs text-slate-400">operando desde 2014</span></div>
                <div><span class="block text-2xl font-extrabold">30+</span><span class="text-xs text-slate-400">comunas RM atendidas</span></div>
                <div><span class="block text-2xl font-extrabold">3 tamaños</span><span class="text-xs text-slate-400">cisternas 2k / 5k / 15k L</span></div>
                <div><span class="block text-2xl font-extrabold">5.000 PSI</span><span class="text-xs text-slate-400">hidrojet máx (industrial)</span></div>
                <div><span class="block text-2xl font-extrabold">24 / 7</span><span class="text-xs text-slate-400">WhatsApp con IA</span></div>
            </div>
            <p class="text-center text-xs text-slate-500 mt-6">
                Resolución sanitaria <strong class="text-slate-300">SEREMI vigente</strong> ·
                Factura electrónica con OC ·
                Certificado de disposición por servicio ·
                <a href="/flota" class="text-blue-300 hover:text-white underline">flota</a> ·
                <a href="/empresas" class="text-blue-300 hover:text-white underline">empresas B2B</a> ·
                <a href="/por-que-elegirnos" class="text-blue-300 hover:text-white underline">por qué elegirnos</a>
            </p>
        </div>
    </section>

"""

TARGETS = [
    "index.html",
    "cobertura.html",
    "precios-orientativos.html",
    "urgencias-24-7.html",
    "contacto.html",
    "nosotros.html",
    "faq.html",
    "documentos.html",
    "testimonios.html",
    "casos-reales/index.html",
    "servicios/index.html",
    "servicios/destape-alcantarillado.html",
    "servicios/limpieza-fosas-septicas.html",
    "servicios/camion-alta-presion-hidrojet.html",
    "servicios/destape-wc-y-banos.html",
    "servicios/destape-desagues-cocina-y-grasa.html",
    "servicios/destape-edificios-condominios.html",
    "servicios/inspeccion-camara-alcantarillado.html",
    "servicios/mantencion-preventiva.html",
    "servicios/contratos-empresas-y-condominios.html",
]


def inject_banner(content: str) -> tuple[str, bool]:
    """Inyecta el banner antes del primer <footer si aún no está presente."""
    if f'id="{BANNER_ID}"' in content:
        return content, False

    pattern = re.compile(r'(\s*)<footer\b', re.IGNORECASE)
    match = pattern.search(content)
    if not match:
        return content, False

    insert_pos = match.start()
    new_content = content[:insert_pos] + BANNER_HTML + content[insert_pos:]
    return new_content, True


def main() -> None:
    changed = 0
    skipped = []
    for rel in TARGETS:
        path = PUBLIC / rel
        if not path.exists():
            skipped.append(rel)
            continue
        raw = path.read_text(encoding="utf-8")
        new, was_changed = inject_banner(raw)
        if was_changed:
            path.write_text(new, encoding="utf-8")
            changed += 1
            print(f"  ✅ {rel}")
        else:
            print(f"  · {rel}  (ya tenía banner o no se encontró <footer>)")

    if skipped:
        print("\n  ⚠️  no encontrados:", ", ".join(skipped))
    print(f"\nresumen: {changed}/{len(TARGETS)} archivos actualizados")


if __name__ == "__main__":
    main()
