#!/usr/bin/env python3
"""
Reescribe title + meta description + og:title/desc + twitter:title/desc
para páginas con near-duplicate content (zonas urbanas y rurales).

Diversifica el ángulo por comuna y respeta el rango 50-62 chars (title)
y 140-160 chars (description).
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

# title (≤ 62 chars), description (≤ 160 chars)
PLAN: dict[str, dict[str, str]] = {
    # === ZONAS URBANAS ===
    "zonas/urbano/las-condes.html": {
        "title": "Destape Alcantarillado Las Condes | Edificios y Casas 24/7",
        "desc": (
            "Destape de alcantarillado y cañerías en Las Condes para casas, "
            "edificios y comercios. Servicio sin romper, urgencias 24/7. "
            "Cotiza por WhatsApp."
        ),
    },
    "zonas/urbano/vitacura.html": {
        "title": "Destape de Cañerías en Vitacura | Casas y Condominios 24/7",
        "desc": (
            "Destape de cañerías y alcantarillado en Vitacura. Atención a "
            "casas, departamentos y condominios con maquinaria sin romper. "
            "Urgencias 24/7."
        ),
    },
    "zonas/urbano/lo-barnechea.html": {
        "title": "Destape Alcantarillado Lo Barnechea | Cordillera 24/7",
        "desc": (
            "Servicio de destape en Lo Barnechea: La Dehesa, El Arrayán y "
            "sectores cordillera. Camión hidrojet y máquinas eléctricas. "
            "Urgencias 24/7."
        ),
    },
    "zonas/urbano/providencia.html": {
        "title": "Destape Alcantarillado Providencia | Departamentos 24/7",
        "desc": (
            "Destape en Providencia para departamentos, locales y oficinas. "
            "Maquinaria eléctrica sin daño a la cerámica. Disponibilidad "
            "24/7 con WhatsApp."
        ),
    },
    "zonas/urbano/nunoa.html": {
        "title": "Destape de Cañerías en Ñuñoa | Casas y Comunidades 24/7",
        "desc": (
            "Destape de WC, cocinas y alcantarillado en Ñuñoa. Servicio "
            "para casas, comunidades y locales con respuesta rápida y sin "
            "romper. Cotiza ahora."
        ),
    },
    "zonas/urbano/la-reina.html": {
        "title": "Destape Alcantarillado La Reina | Casas y Condominios 24/7",
        "desc": (
            "Destape de cañerías en La Reina Alta y centro: casas, "
            "condominios y comercios. Camión hidrojet y máquina eléctrica. "
            "Urgencias 24/7."
        ),
    },

    # === ZONAS RURALES ===
    "zonas/rural/buin-paine.html": {
        "title": "Limpieza de Fosas Sépticas Buin y Paine | Parcelas 24/7",
        "desc": (
            "Limpieza de fosas sépticas en Buin y Paine: parcelas, "
            "agroindustria y empresas. Camiones de alto tonelaje y "
            "certificado de retiro. Cotiza."
        ),
    },
    "zonas/rural/calera-de-tango.html": {
        "title": "Limpieza de Fosas en Calera de Tango | Parcelas Rurales",
        "desc": (
            "Servicio de limpieza de fosas sépticas en Calera de Tango. "
            "Parcelas grandes, agrícolas y eventos. Disponibilidad 24/7 y "
            "certificado al día."
        ),
    },
    "zonas/rural/chicureo.html": {
        "title": "Limpieza de Fosas en Chicureo | Parcelas y Condominios 24/7",
        "desc": (
            "Limpieza de fosas sépticas en Chicureo: condominios cerrados, "
            "parcelas y casas. Camiones certificados, retiro con boleta y "
            "factura. WhatsApp 24/7."
        ),
    },
    "zonas/rural/lampa.html": {
        "title": "Limpieza Fosas Sépticas Lampa | Norte RM y Estancias 24/7",
        "desc": (
            "Limpieza de fosas sépticas en Lampa, Batuco y Estaciones. "
            "Parcelas, condominios y empresas con camiones de alto "
            "tonelaje. Atención 24/7."
        ),
    },
    "zonas/rural/pirque.html": {
        "title": "Limpieza Fosas Sépticas Pirque | Precordillera 24/7",
        "desc": (
            "Limpieza de fosas en Pirque y Cajón del Maipo: parcelas, "
            "casas y eventos. Acceso a sectores difíciles con camiones "
            "compactos y retiro certificado."
        ),
    },
    "zonas/rural/talagante.html": {
        "title": "Limpieza Fosas en Talagante | Parcelas y Eventos 24/7",
        "desc": (
            "Limpieza de fosas sépticas en Talagante e Isla de Maipo. "
            "Parcelas, eventos y baños químicos. Servicio con boleta o "
            "factura, 24/7 por WhatsApp."
        ),
    },
    "zonas/rural/isla-de-maipo.html": {
        "title": "Limpieza de Fosas en Isla de Maipo | Parcelas y Viñas 24/7",
        "desc": (
            "Limpieza de fosas sépticas en Isla de Maipo: parcelas, "
            "viñedos y eventos rurales. Camiones de alto tonelaje y "
            "certificado de retiro."
        ),
    },
    "zonas/rural/san-jose-de-maipo.html": {
        "title": "Limpieza de Fosas San José de Maipo | Cajón del Maipo 24/7",
        "desc": (
            "Limpieza de fosas en San José de Maipo y todo el Cajón. "
            "Acceso a parcelas y cabañas con vehículos preparados para "
            "alta cordillera. 24/7."
        ),
    },
    "zonas/rural/colina.html": {
        "title": "Limpieza Fosas Sépticas Colina | Industrial y Residencial",
        "desc": (
            "Limpieza de fosas en Colina, Esmeralda y Peldehue: parcelas, "
            "industria y condominios. Resolución sanitaria al día y retiro "
            "certificado."
        ),
    },
}


def update(file_rel: str, title: str, desc: str) -> bool:
    path = PUBLIC / file_rel
    if not path.is_file():
        print(f"  ⚠️ no existe: {file_rel}")
        return False
    raw = path.read_text(encoding="utf-8")
    new = raw

    # 1) <title>
    new = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", new, count=1, flags=re.DOTALL)

    # 2) <meta name="description">
    new = re.sub(
        r'<meta\s+name="description"\s*[^>]*content="[^"]*"\s*/?>',
        f'<meta name="description" content="{desc}">',
        new,
        count=1,
        flags=re.IGNORECASE,
    )
    # Variant where attributes are split across lines
    new = re.sub(
        r'<meta\s+name="description"\s*\n\s*content="[^"]*"\s*/?>',
        f'<meta name="description" content="{desc}">',
        new,
        count=1,
        flags=re.IGNORECASE,
    )

    # 3) og:title / og:description
    new = re.sub(
        r'<meta\s+property="og:title"\s*content="[^"]*"\s*/?>',
        f'<meta property="og:title" content="{title}">',
        new,
        count=1,
    )
    new = re.sub(
        r'<meta\s+property="og:description"\s*\n?\s*content="[^"]*"\s*/?>',
        f'<meta property="og:description" content="{desc}">',
        new,
        count=1,
    )

    # 4) twitter:title / twitter:description
    new = re.sub(
        r'<meta\s+name="twitter:title"\s*content="[^"]*"\s*/?>',
        f'<meta name="twitter:title" content="{title}">',
        new,
        count=1,
    )
    new = re.sub(
        r'<meta\s+name="twitter:description"\s*content="[^"]*"\s*/?>',
        f'<meta name="twitter:description" content="{desc}">',
        new,
        count=1,
    )

    if new != raw:
        path.write_text(new, encoding="utf-8")
        print(f"  ✅ {file_rel}  (title {len(title)}c, desc {len(desc)}c)")
        return True
    print(f"  · sin cambios: {file_rel}")
    return False


def main() -> None:
    print(f"Actualizando {len(PLAN)} páginas con titles/metas únicos...")
    changed = 0
    for f, payload in PLAN.items():
        # Validate lengths
        tl, dl = len(payload["title"]), len(payload["desc"])
        if not (40 <= tl <= 65):
            print(f"  ⚠️ title fuera de rango ({tl}c): {f}")
        if not (130 <= dl <= 165):
            print(f"  ⚠️ desc fuera de rango ({dl}c): {f}")
        if update(f, payload["title"], payload["desc"]):
            changed += 1
    print(f"\nTotal cambiados: {changed}/{len(PLAN)}")


if __name__ == "__main__":
    main()
