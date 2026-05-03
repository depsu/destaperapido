#!/usr/bin/env python3
"""
Genera 4 nuevas páginas de zona rural a partir del template lampa.html,
con contenido único por comuna (evita duplicate content).

Comunas: Peñaflor, Padre Hurtado, Melipilla, Curacaví
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
RURAL = PUBLIC / "zonas" / "rural"

# Contenido único por comuna
COMUNAS: dict[str, dict] = {
    "penaflor": {
        "name": "Peñaflor",
        "title": "Limpieza de Fosas Sépticas en Peñaflor | Parcelas 24/7",
        "desc": (
            "Limpieza de fosas sépticas en Peñaflor: Trapiche, Malloco y "
            "Las Mercedes. Parcelas, condominios y empresas con camiones "
            "de alto tonelaje. 24/7."
        ),
        "site_suffix": "Peñaflor",
        "h1_html": "Limpieza de Fosas en Peñaflor <br>",
        "subtitle": "Atendemos <strong>Trapiche, Malloco, Las Mercedes y La Estrella</strong>.",
        "intro_problem": (
            "En Peñaflor el suelo es mixto entre arcilloso y arenoso, con napas "
            "freáticas relativamente altas por la cercanía al río Mapocho. "
            "Limpiamos a fondo con equipos preparados para drenajes saturados."
        ),
        "trees_text": (
            "Las parcelas de Peñaflor tienen árboles maduros que con frecuencia "
            "invaden la red. Usamos cortadores especializados sin romper "
            "tuberías."
        ),
        "expertise_text": (
            "Conocemos las parcelas de Trapiche y Malloco: muchas tienen las "
            "fosas alejadas de la calle, escondidas tras antejardines o detrás "
            "del estacionamiento. Llevamos manguera extra-larga y carro de carga."
        ),
        "respectful_text": (
            "Cuidamos el entorno típico de Peñaflor —árboles frutales, "
            "huertas— y usamos productos biodegradables que no dañan la "
            "vegetación."
        ),
        "soil_quote": (
            "El suelo cerca del río Mapocho exige mantenciones más frecuentes."
        ),
        "common_problem": (
            "Es muy común en Peñaflor por las raíces de árboles frutales y "
            "alamedas. Usamos máquinas eléctricas con sondas cortadoras de "
            "raíces para despejar sin romper."
        ),
        "septic_warning": (
            "La grasa de cocina es la principal causa de impermeabilización "
            "de pozos de absorción en parcelas de Peñaflor."
        ),
        "pump_text": (
            "Muchas parcelas de Trapiche y Malloco usan bombas elevadoras. "
            "Las limpiamos y revisamos junto con la fosa."
        ),
        "rural_caveat": (
            "Sabemos que en Peñaflor las fosas a menudo están lejos del acceso "
            "principal o detrás de cercos altos."
        ),
        "sectors": [
            ("Trapiche", "fa-tractor"),
            ("Malloco", "fa-house-chimney"),
            ("Las Mercedes", "fa-tree"),
            ("La Estrella", "fa-mountain-sun"),
        ],
        "subsectors": [
            ("Trapiche", "Sector residencial principal"),
            ("Malloco", "Parcelas y condominios"),
            ("Las Mercedes", "Zona rural"),
            ("La Estrella", "Cercano al río"),
        ],
        "calles": [
            "Av. Vicuña Mackenna",
            "Camino a Malloco",
            "Av. Manuel Rodríguez",
        ],
        "faq": [
            (
                "¿Llegan hasta Malloco o sectores alejados?",
                (
                    "Sí, cubrimos toda la comuna de Peñaflor incluyendo Trapiche, "
                    "Malloco, Las Mercedes y La Estrella. Nuestros camiones "
                    "están preparados para caminos de tierra y entradas "
                    "estrechas de parcelas."
                ),
            ),
            (
                "¿Qué pasa si la fosa rebalsa por la cercanía al río?",
                (
                    "Activamos protocolo de emergencia: vaciamos primero el "
                    "exceso, sellamos puntos críticos y luego programamos "
                    "limpieza profunda. Importante actuar rápido para evitar "
                    "contaminación al napa."
                ),
            ),
            (
                "¿Limpian también las cámaras de grasa de cocina?",
                (
                    "Sí, y es muy recomendable. La grasa de cocina es la "
                    "principal causa de impermeabilización de los pozos de "
                    "absorción en Peñaflor."
                ),
            ),
            (
                "¿Cobran extra por entrada angosta o pasajes?",
                (
                    "No, nuestros camiones medianos pueden ingresar a la "
                    "mayoría de las parcelas. Si el acceso es muy estrecho, "
                    "te avisamos antes y coordinamos manguera extra."
                ),
            ),
        ],
        "reviews": [
            ("Mauricio L.", "Trapiche", 5, "Llegaron en menos de una hora a mi parcela. Trabajo prolijo y se llevaron todo el residuo."),
            ("Ana V.", "Malloco", 5, "Excelente servicio. Limpiaron la fosa, la cámara de grasa y dejaron todo ordenado."),
            ("Sergio P.", "Las Mercedes", 4, "Buen precio. Conocían bien el sector y entraron sin problema con el camión."),
            ("Karina M.", "La Estrella", 5, "Salvaron la fiesta de cumpleaños familiar. Vinieron un domingo en la tarde."),
            ("Don Hugo", "Peñaflor centro", 5, "Servicio limpio y respetuoso. Recomendados 100%."),
        ],
    },

    "padre-hurtado": {
        "name": "Padre Hurtado",
        "title": "Limpieza de Fosas en Padre Hurtado | Parcelas y Empresas 24/7",
        "desc": (
            "Limpieza de fosas sépticas en Padre Hurtado: Catemito, El "
            "Trebal y Los Bajos. Parcelas, condominios e industria con "
            "atención 24/7."
        ),
        "site_suffix": "Padre Hurtado",
        "h1_html": "Limpieza de Fosas en Padre Hurtado <br>",
        "subtitle": "Atendemos <strong>Catemito, Los Bajos de San Agustín y El Trebal</strong>.",
        "intro_problem": (
            "Padre Hurtado combina parcelas residenciales, condominios y "
            "zona industrial El Trebal. Cada perfil tiene exigencias "
            "distintas y nosotros traemos el equipo correcto para cada uno."
        ),
        "trees_text": (
            "Las parcelas en Catemito tienen árboles añosos que invaden las "
            "redes. Limpiamos con corta-raíces eléctrico sin romper tuberías."
        ),
        "expertise_text": (
            "El sector industrial de El Trebal nos contrata habitualmente "
            "para limpieza de cámaras desgrasadoras y fosas de altos "
            "volúmenes. Tenemos certificado de retiro y boleta/factura."
        ),
        "respectful_text": (
            "En condominios privados de Padre Hurtado coordinamos con la "
            "administración el horario de ingreso y dejamos limpio el área "
            "de trabajo."
        ),
        "soil_quote": (
            "Las parcelas grandes de Catemito requieren mantención cada 18 meses."
        ),
        "common_problem": (
            "Las raíces de plátanos orientales y eucaliptos son frecuentes "
            "en Padre Hurtado. Usamos sondas eléctricas con cabezal cortador "
            "para abrir sin romper."
        ),
        "septic_warning": (
            "Para empresas en El Trebal recomendamos contratos mensuales — "
            "evitan multas sanitarias y aseguran continuidad operacional."
        ),
        "pump_text": (
            "Empresas de la zona industrial usan plantas elevadoras y "
            "trampas de grasa industriales. Tenemos camiones de 8.000 L "
            "para esos volúmenes."
        ),
        "rural_caveat": (
            "Conocemos los caminos rurales de Padre Hurtado y los "
            "condominios cerrados. Llegamos al horario coordinado."
        ),
        "sectors": [
            ("Catemito", "fa-tractor"),
            ("Los Bajos", "fa-house-chimney"),
            ("El Trebal", "fa-industry"),
            ("Centro", "fa-building"),
        ],
        "subsectors": [
            ("Catemito", "Parcelas y casas"),
            ("Los Bajos de San Agustín", "Sector residencial"),
            ("El Trebal", "Industria y bodegas"),
            ("Centro", "Comercio y servicios"),
        ],
        "calles": [
            "Av. San Francisco",
            "Camino El Trebal",
            "Camino Padre Hurtado",
        ],
        "faq": [
            (
                "¿Atienden a empresas del sector industrial El Trebal?",
                (
                    "Sí, somos especialistas en cámaras desgrasadoras, "
                    "plantas de tratamiento y fosas industriales. Entregamos "
                    "boleta o factura y certificado de retiro de residuos."
                ),
            ),
            (
                "¿Pueden ingresar a condominios cerrados?",
                (
                    "Sí, coordinamos con administración el horario y los "
                    "permisos. Llegamos en camión apto para la mayoría de "
                    "calles internas."
                ),
            ),
            (
                "¿Cada cuánto debo limpiar la fosa de mi parcela?",
                (
                    "Para parcelas con 4 personas, cada 2-3 años. Si tienes "
                    "huerta, lavandería intensiva o piscina, se reduce a "
                    "12-18 meses."
                ),
            ),
            (
                "¿Trabajan los fines de semana?",
                (
                    "Sí, tenemos cobertura 24/7. Para urgencias en Padre "
                    "Hurtado contactanos por WhatsApp y agendamos al instante."
                ),
            ),
        ],
        "reviews": [
            ("Empresa Aguilar", "El Trebal", 5, "Servicio mensual hace 2 años. Siempre puntuales y con boleta."),
            ("Familia Riquelme", "Catemito", 5, "Vinieron un sábado al mediodía. Excelente trato y precio justo."),
            ("Cond. Los Aromos", "Los Bajos", 5, "Coordinaron con la administración sin problema. Limpios y ordenados."),
            ("María José", "Centro", 4, "Buen servicio. La fosa quedó como nueva."),
            ("Jorge T.", "Catemito", 5, "Conocían el camino y llegaron rápido. Recomendados."),
        ],
    },

    "melipilla": {
        "name": "Melipilla",
        "title": "Limpieza de Fosas Sépticas en Melipilla | Agroindustria 24/7",
        "desc": (
            "Limpieza de fosas en Melipilla: Pomaire, Bollenar, Codigua y "
            "San Pedro. Parcelas, agricultura y agroindustria con camiones "
            "preparados."
        ),
        "site_suffix": "Melipilla",
        "h1_html": "Limpieza de Fosas en Melipilla <br>",
        "subtitle": "Atendemos <strong>Pomaire, Bollenar, Codigua y San Pedro</strong>.",
        "intro_problem": (
            "Melipilla es una de las zonas agrícolas más activas de la RM. "
            "Nuestro servicio cubre desde parcelas familiares hasta "
            "agroindustria y plantas lecheras, con camiones de alto tonelaje "
            "y certificación sanitaria al día."
        ),
        "trees_text": (
            "En Melipilla los nogales y palmas chilenas son comunes en "
            "parcelas — sus raíces son agresivas. Cortamos con cabezales "
            "eléctricos sin dañar la red."
        ),
        "expertise_text": (
            "Trabajamos con lecherías, plantas avícolas y agroindustria de "
            "la zona. Realizamos limpieza de fosas industriales, cámaras "
            "desgrasadoras y plantas de tratamiento con disposición certificada."
        ),
        "respectful_text": (
            "Respetamos la actividad agrícola: coordinamos los servicios "
            "para no interferir con cosechas, ordeñas o faenas en curso."
        ),
        "soil_quote": (
            "El terreno arcilloso de Melipilla impermeabiliza los drenes — "
            "exige limpieza más frecuente."
        ),
        "common_problem": (
            "En Melipilla el problema clásico son raíces y la grasa "
            "industrial de pequeñas plantas. Tenemos máquinas eléctricas y "
            "hidrojet de alta presión para ambos casos."
        ),
        "septic_warning": (
            "Las parcelas con piscina o riego intensivo en Pomaire saturan "
            "antes los pozos absorbentes. Recomendamos limpieza cada 18 meses."
        ),
        "pump_text": (
            "Las parcelas grandes de Bollenar y Codigua suelen tener "
            "estanques elevados o bombas presurizadoras. Las limpiamos junto "
            "con la fosa."
        ),
        "rural_caveat": (
            "Conocemos los caminos rurales de Melipilla, incluso los más "
            "alejados como Mandinga o Cholqui."
        ),
        "sectors": [
            ("Pomaire", "fa-jar"),
            ("Bollenar", "fa-tractor"),
            ("Codigua", "fa-tree"),
            ("San Pedro", "fa-mountain-sun"),
        ],
        "subsectors": [
            ("Pomaire", "Pueblo de la greda"),
            ("Bollenar", "Sector agrícola"),
            ("Codigua", "Parcelas grandes"),
            ("San Pedro", "Zona rural"),
        ],
        "calles": [
            "Av. Vicuña Mackenna (Melipilla)",
            "Camino a Pomaire",
            "Ruta G-78",
        ],
        "faq": [
            (
                "¿Atienden agroindustria, lecherías o avícolas en Melipilla?",
                (
                    "Sí, somos especialistas en limpieza de fosas y cámaras "
                    "industriales para agroindustria. Trabajamos con boleta "
                    "o factura, con certificado de retiro y cumpliendo el "
                    "DS 236/1926."
                ),
            ),
            (
                "¿Cuánto cuesta limpiar una fosa grande en parcela?",
                (
                    "Depende del volumen (m³) y la accesibilidad. Para "
                    "parcelas de Bollenar o Codigua nuestros precios parten "
                    "desde valores muy competitivos. Cotiza por WhatsApp."
                ),
            ),
            (
                "¿Atienden eventos en Pomaire (Fiestas Patrias, ferias)?",
                (
                    "Sí, arrendamos baños químicos y limpiamos fosas para "
                    "eventos masivos en Melipilla. Coordinación previa "
                    "recomendada."
                ),
            ),
            (
                "¿Llegan a Mandinga, Cholqui o sectores alejados?",
                (
                    "Sí, cubrimos toda la comuna de Melipilla incluyendo "
                    "Mandinga, Cholqui, Puangue y Culiprán."
                ),
            ),
        ],
        "reviews": [
            ("Lechería S.", "Bollenar", 5, "Contrato mensual. Siempre cumplen y entregan certificado."),
            ("Restaurante Pomaire", "Pomaire", 5, "Limpiaron la cámara de grasa antes del fin de semana largo. Top."),
            ("Don Aurelio", "Codigua", 5, "Vinieron a mi parcela en una hora. Excelente."),
            ("Avícola del Sur", "San Pedro", 4, "Buen servicio para empresa. Boleta y factura sin problema."),
            ("Sra. Inés", "Melipilla centro", 5, "Servicio respetuoso y profesional."),
        ],
    },

    "curacavi": {
        "name": "Curacaví",
        "title": "Limpieza de Fosas Sépticas en Curacaví | Ruta 68 24/7",
        "desc": (
            "Limpieza de fosas en Curacaví: Cuyuncaví, Lo Aguirre y Lo "
            "Prado. Parcelas, viñedos y empresas a lo largo de la Ruta 68. "
            "Atención 24/7."
        ),
        "site_suffix": "Curacaví",
        "h1_html": "Limpieza de Fosas en Curacaví <br>",
        "subtitle": "Atendemos <strong>Cuyuncaví, El Mariscal, Lo Aguirre y Lo Prado</strong>.",
        "intro_problem": (
            "Curacaví está en pleno corredor Ruta 68: desde parcelas hasta "
            "restaurantes carreteros y viñedos boutique. Cada uno con "
            "necesidades distintas y nosotros con el camión correcto para "
            "cada caso."
        ),
        "trees_text": (
            "En Curacaví los espinos y palmas son comunes y sus raíces son "
            "duras. Cortamos con sondas eléctricas y recuperamos la red sin "
            "tener que excavar."
        ),
        "expertise_text": (
            "Atendemos restaurantes y centros de eventos de la Ruta 68: "
            "limpieza de cámaras desgrasadoras, fosas y plantas de "
            "tratamiento con boleta o factura."
        ),
        "respectful_text": (
            "En viñedos boutique trabajamos con cuidado especial — sin "
            "alterar las labores de viña ni la disposición del terreno."
        ),
        "soil_quote": (
            "Los terrenos en pendiente de Curacaví requieren camiones con "
            "buena tracción. Los tenemos."
        ),
        "common_problem": (
            "En Curacaví las raíces de árboles añosos son la causa #1 de "
            "obstrucciones. Las cortamos con sondas eléctricas — sin romper "
            "ni excavar."
        ),
        "septic_warning": (
            "Restaurantes y centros de eventos en Curacaví requieren "
            "limpieza frecuente de cámaras de grasa: idealmente cada 60-90 días."
        ),
        "pump_text": (
            "Las parcelas en pendiente suelen tener bombas elevadoras. Las "
            "limpiamos y testeamos junto con la fosa principal."
        ),
        "rural_caveat": (
            "Conocemos los caminos de Cuyuncaví y El Mariscal, incluso los "
            "más empinados o los pasos de viñedos."
        ),
        "sectors": [
            ("Cuyuncaví", "fa-tractor"),
            ("El Mariscal", "fa-mountain-sun"),
            ("Lo Aguirre", "fa-tree"),
            ("Lo Prado", "fa-wine-glass"),
        ],
        "subsectors": [
            ("Cuyuncaví", "Sector residencial"),
            ("El Mariscal", "Parcelas grandes"),
            ("Lo Aguirre", "Zona rural"),
            ("Lo Prado", "Viñedos y agro"),
        ],
        "calles": [
            "Ruta 68 (km 35-50)",
            "Camino Cuyuncaví",
            "Camino El Mariscal",
        ],
        "faq": [
            (
                "¿Atienden restaurantes y centros de eventos de la Ruta 68?",
                (
                    "Sí, somos especialistas en cámaras desgrasadoras y "
                    "fosas para gastronomía y eventos. Trabajamos con boleta "
                    "o factura, en horarios fuera de servicio para no "
                    "interrumpir."
                ),
            ),
            (
                "¿Pueden subir a parcelas en pendiente de El Mariscal?",
                (
                    "Sí, nuestros camiones tienen tracción suficiente para "
                    "las pendientes habituales de Curacaví. Si la pendiente "
                    "es extrema, llevamos manguera extra-larga."
                ),
            ),
            (
                "¿Cuánto cuesta limpiar una fosa en Curacaví?",
                (
                    "Depende del volumen y la distancia desde Santiago. "
                    "Para Curacaví tenemos tarifa rural. Cotiza por WhatsApp "
                    "para precio exacto."
                ),
            ),
            (
                "¿Atienden eventos y matrimonios en Curacaví?",
                (
                    "Sí, arrendamos baños químicos y limpiamos fosas para "
                    "eventos en centros de eventos y viñedos. Coordina con "
                    "10 días de anticipación si es posible."
                ),
            ),
        ],
        "reviews": [
            ("Centro Eventos La Higuera", "Cuyuncaví", 5, "Servicio mensual hace años. Siempre antes y después de cada matrimonio."),
            ("Familia Pizarro", "El Mariscal", 5, "Subieron sin problema a mi parcela en pendiente. Excelente."),
            ("Restaurante Las Vertientes", "Lo Aguirre", 5, "Limpieza de cámara desgrasadora rápida y limpia."),
            ("Viña Boutique", "Lo Prado", 4, "Trabajo respetuoso. Cuidaron las parras."),
            ("Don Mario", "Curacaví centro", 5, "Servicio rápido y profesional."),
        ],
    },
}


def transform_zone(slug: str, data: dict) -> None:
    path = RURAL / f"{slug}.html"
    raw = path.read_text(encoding="utf-8")
    new = raw

    name = data["name"]
    sectors = data["sectors"]

    # ----- HEAD -----
    new = new.replace(
        "<title>Limpieza Fosas Sépticas Lampa | Norte RM y Estancias 24/7</title>",
        f"<title>{data['title']}</title>",
    )
    new = new.replace(
        '<meta name="description" content="Limpieza de fosas sépticas en Lampa, Batuco y Estaciones. Parcelas, condominios y empresas con camiones de alto tonelaje. Atención 24/7.">',
        f'<meta name="description" content="{data["desc"]}">',
    )
    new = new.replace(
        '<meta property="og:site_name" content="Destape Rápido Lampa">',
        f'<meta property="og:site_name" content="Destape Rápido {data["site_suffix"]}">',
    )
    new = new.replace(
        '<meta property="og:title" content="Limpieza Fosas Sépticas Lampa | Norte RM y Estancias 24/7">',
        f'<meta property="og:title" content="{data["title"]}">',
    )
    new = new.replace(
        '<meta property="og:description" content="Limpieza de fosas sépticas en Lampa, Batuco y Estaciones. Parcelas, condominios y empresas con camiones de alto tonelaje. Atención 24/7.">',
        f'<meta property="og:description" content="{data["desc"]}">',
    )
    new = new.replace(
        '<meta name="twitter:title" content="Limpieza Fosas Sépticas Lampa | Norte RM y Estancias 24/7">',
        f'<meta name="twitter:title" content="{data["title"]}">',
    )
    new = new.replace(
        '<meta name="twitter:description" content="Limpieza de fosas sépticas en Lampa, Batuco y Estaciones. Parcelas, condominios y empresas con camiones de alto tonelaje. Atención 24/7.">',
        f'<meta name="twitter:description" content="{data["desc"]}">',
    )

    # canonical & og:url
    new = re.sub(
        r'<link rel="canonical" href="https://www\.destaperapido\.cl/zonas/rural/lampa">',
        f'<link rel="canonical" href="https://www.destaperapido.cl/zonas/rural/{slug}">',
        new,
    )
    new = re.sub(
        r'<meta property="og:url" content="https://www\.destaperapido\.cl/zonas/rural/lampa\.html">',
        f'<meta property="og:url" content="https://www.destaperapido.cl/zonas/rural/{slug}">',
        new,
    )

    # ----- JSON-LD areaServed / Service / Breadcrumb -----
    new = new.replace(
        '"name": "Lampa, Región Metropolitana, Chile"',
        f'"name": "{name}, Región Metropolitana, Chile"',
    )
    new = new.replace(
        '"name": "Limpieza de fosas sépticas y destape de alcantarillado en Lampa, Región Metropolitana, Chile"',
        f'"name": "Limpieza de fosas sépticas y destape de alcantarillado en {name}, Región Metropolitana, Chile"',
    )
    new = new.replace(
        '"description": "Limpieza de fosas sépticas y destapes en Lampa, Batuco y Valle Grande. Camiones con mangueras extra largas para parcelas. Resolución sanitaria y cuidado de jardines."',
        f'"description": "{data["desc"]}"',
    )
    # Breadcrumb leaf name
    new = re.sub(
        r'"position": 4,\s*"name": "Lampa",\s*"item": "https://www\.destaperapido\.cl/zonas/rural/lampa"',
        f'"position": 4,\n        "name": "{name}",\n        "item": "https://www.destaperapido.cl/zonas/rural/{slug}"',
        new,
    )
    new = new.replace(
        '"@id": "https://www.destaperapido.cl/zonas/rural/lampa"',
        f'"@id": "https://www.destaperapido.cl/zonas/rural/{slug}"',
    )

    # ----- HERO + intro -----
    new = new.replace('alt="Paisaje rural Lampa"', f'alt="Paisaje rural {name}"')
    new = new.replace(
        "Limpieza de Fosas en Lampa <br>",
        data["h1_html"],
    )
    new = new.replace(
        "Atendemos <strong>Batuco, Valle Grande y Estación Colina</strong>.",
        data["subtitle"],
    )
    new = new.replace("En Lampa - 25 min", f"En {name} - 25 min")
    new = new.replace("¿Emergencia en Lampa?", f"¿Emergencia en {name}?")
    new = new.replace(
        "de Lampa:",
        f"de {name}:",
    )
    new = new.replace(
        "tierra y accesos difíciles típicos de Lampa y Batuco.",
        f"tierra y accesos difíciles típicos de {name}.",
    )

    # 4 sub-sectores con icono (líneas 1049-1055 originales)
    # Reemplazamos cada bloque "fa-..." individualmente
    # Bloque tipo: <i class="fa-solid fa-mountain-sun text-2xl"></i> Batuco</div>
    # Mapeo a los 4 nuevos sectores
    old_sectors = [
        ("fa-mountain-sun", "Batuco"),
        ("fa-city", "Valle Grande"),
        ("fa-train", "Estación Colina"),
        ("fa-tree", "Lipangue"),
    ]
    for (old_icon, old_label), (new_label, new_icon) in zip(old_sectors, sectors):
        new = new.replace(
            f'class="fa-solid {old_icon} text-2xl"></i> {old_label}',
            f'class="fa-solid {new_icon} text-2xl"></i> {new_label}',
        )

    # ----- Cuerpo: secciones de problema/solucion -----
    new = new.replace(
        "En Lampa, el suelo arcilloso y las napas son un desafío. Ofrecemos limpieza profunda con equipo",
        f"{data['intro_problem']} Ofrecemos limpieza profunda con equipo",
    )
    new = new.replace(
        'alt="Limpieza de fosas en Lampa"',
        f'alt="Limpieza de fosas en {name}"',
    )
    new = new.replace(
        "Los árboles grandes de Lampa suelen invadir las tuberías. Usamos cortadores especializados",
        f"{data['trees_text']}",
    )
    new = new.replace(
        "Opiniones de vecinos en Lampa",
        f"Opiniones de vecinos en {name}",
    )

    # placeholder del select de sectores (input "Ej: Batuco")
    new = new.replace(
        'placeholder="Ej: Batuco"',
        f'placeholder="Ej: {sectors[0][0]}"',
    )

    # ----- Sección "Expertos en parcelas" -----
    new = new.replace(
        "Expertos en Parcelas de Lampa",
        f"Expertos en Parcelas de {name}",
    )
    new = new.replace(
        "Sabemos que en Lampa y Batuco las fosas a menudo están lejos del acceso principal o escondidas",
        data["rural_caveat"] + " Las fosas a menudo están lejos del acceso principal o escondidas",
    )
    new = new.replace(
        "Respetamos el entorno natural de Lampa. Trabajamos limpio y utilizamos productos",
        f"{data['respectful_text']} Trabajamos limpio y utilizamos productos",
    )
    new = new.replace('alt="Parcela en Lampa"', f'alt="Parcela en {name}"')
    new = new.replace(
        '"El suelo arcilloso de Lampa requiere mantenciones',
        f'"{data["soil_quote"]}',
    )
    new = new.replace('alt="Camino rural en Lampa"', f'alt="Camino rural en {name}"')

    # ----- Bombas elevadoras -----
    new = new.replace(
        "Muchas parcelas en Lampa usan bombas elevadoras. Realizamos su limpieza y chequeo",
        f"{data['pump_text']} Realizamos su limpieza y chequeo",
    )

    # ----- CTA cobertura final -----
    new = new.replace(
        "Cobertura total en Lampa, Batuco y Valle Grande.",
        f"Cobertura total en {name}: {sectors[0][0]}, {sectors[1][0]} y {sectors[2][0]}.",
    )

    # ----- FAQ visible (4 preguntas) -----
    # En lampa.html están en las líneas 1473-1530 más o menos.
    # Los items siguen patrones:
    #   <span>¿Llegan hasta Batuco o sectores alejados?</span> ... <p>... </p>
    # Usaremos regex específicos.
    faq_pairs = data["faq"]

    faq_replacements = [
        ("¿Llegan hasta Batuco o sectores alejados?", faq_pairs[0]),
        # second FAQ depends on what original says — let's not do generic replace
    ]
    # Reemplazo de pregunta 1
    new = new.replace(
        "<span>¿Llegan hasta Batuco o sectores alejados?</span>",
        f"<span>{faq_pairs[0][0]}</span>",
    )
    new = re.sub(
        r"<p>Sí, cubrimos toda la comuna de Lampa, incluyendo <strong>Batuco, Valle Grande, Estación\s+Colina y Lipangue</strong>\. Nuestros camiones están preparados para transitar por",
        f"<p>{faq_pairs[0][1]} Nuestros camiones están preparados para transitar por",
        new,
    )
    # Reemplazo del texto sobre grasa (pregunta 2)
    new = new.replace(
        "causa de impermeabilización de los pozos de absorción y drenajes en Lampa.",
        f"{data['septic_warning']}",
    )
    # Reemplazo del texto sobre raíces (pregunta 3)
    new = new.replace(
        "Es un problema muy común en Lampa debido a la vegetación. Utilizamos máquinas eléctricas con",
        f"{data['common_problem']} Utilizamos máquinas eléctricas con",
    )

    # ----- FAQ JSON-LD -----
    new = new.replace(
        '"name": "¿Llegan hasta Batuco o sectores alejados?"',
        f'"name": "{faq_pairs[0][0]}"',
    )
    new = new.replace(
        '"text": "Sí, cubrimos toda la comuna de Lampa, incluyendo Batuco, Valle Grande, Estación Colina y Lipangue. Nuestros camiones están preparados para caminos rurales."',
        f'"text": "{faq_pairs[0][1]}"',
    )
    new = new.replace(
        '"text": "Sí, y es muy recomendable hacerlo junto con la fosa. La grasa de la cocina es la principal causa de impermeabilización de los pozos de absorción en Lampa."',
        f'"text": "Sí, y es muy recomendable hacerlo junto con la fosa. {data["septic_warning"]}"',
    )
    new = new.replace(
        '"text": "Es muy común en Lampa por la vegetación. Utilizamos máquinas eléctricas con sondas cortadoras de raíces (Root Cutter) para despejar el interior de los ductos sin romperlos."',
        f'"text": "{data["common_problem"]}"',
    )

    # ----- Cobertura detallada -----
    new = new.replace(
        "Preguntas Frecuentes en Lampa",
        f"Preguntas Frecuentes en {name}",
    )
    new = new.replace(
        "Cobertura detallada en Lampa",
        f"Cobertura detallada en {name}",
    )

    # Sub-sectores en la lista (líneas 1537-1542 originales)
    # Patrón: <a href="/zonas/rural/lampa#X" ...>Batuco</a>
    # Reemplazaremos cada anchor para que apunte al fragmento del slug actual.
    old_subs = [
        "Batuco</a></li>",
        "Valle Grande</a></li>",
        "Estación Colina</a></li>",
        '<li><a href="/zonas/rural/lampa" class="hover:text-brand-600 hover:underline">Lipangue</a>',
    ]
    new_subs_html = data["subsectors"]
    new = new.replace(
        f"Batuco</a></li>",
        f"{new_subs_html[0][0]}</a></li>",
        1,
    )
    new = new.replace(
        f"Valle Grande</a></li>",
        f"{new_subs_html[1][0]}</a></li>",
        1,
    )
    new = new.replace(
        f"Estación Colina</a></li>",
        f"{new_subs_html[2][0]}</a></li>",
        1,
    )
    new = re.sub(
        r'<li><a href="/zonas/rural/lampa" class="hover:text-brand-600 hover:underline">Lipangue</a>',
        f'<li><a href="/zonas/rural/{slug}" class="hover:text-brand-600 hover:underline">{new_subs_html[3][0]}</a>',
        new,
    )

    # Calles
    new = new.replace("<li>Camino a Lampa</li>", f"<li>{data['calles'][0]}</li>")
    new = new.replace("<li>Av. España (Batuco)</li>", f"<li>{data['calles'][1]}</li>")
    # Posible tercera calle: lampa.html tiene 2-3 items.

    # ----- WhatsApp prefill + chat msg -----
    new = new.replace(
        "Hola, ¿necesitas vaciar tu fosa en Lampa?",
        f"Hola, ¿necesitas vaciar tu fosa en {name}?",
    )
    new = new.replace(
        "Hola,%20necesito%20presupuesto%20para%20limpieza%20de%20fosa%20en%20Lampa",
        f"Hola,%20necesito%20presupuesto%20para%20limpieza%20de%20fosa%20en%20{name.replace(' ', '%20')}",
    )

    # ----- Reseñas JS array -----
    new = new.replace("// Lógica de Reseñas (Adaptada a Lampa)", f"// Lógica de Reseñas (Adaptada a {name})")
    # Reemplaza cada entry en el array reviews (5 entradas)
    old_reviews = [
        ('{ name: "Juan P.", sector: "Batuco"', 0),
        ('{ name: "Sra. María", sector: "Valle Grande"', 1),
        ('{ name: "Carlos R.", sector: "Estación Colina"', 2),
        ('{ name: "Andrea", sector: "Lipangue"', 3),
        ('{ name: "Pedro S.", sector: "Lampa Centro"', 4),
    ]
    # Re-escribimos el array completo. Buscar el array y reemplazarlo.
    # Marker: const reviews = [   ...   ];
    revs_js = ",\n            ".join(
        f'{{ name: "{r[0]}", sector: "{r[1]}", stars: {r[2]}, text: "{r[3]}", '
        f'initial: "{r[0][0]}", color: "bg-{c}-100 text-{c}-{600}" }}'
        for r, c in zip(data["reviews"], ["blue", "purple", "orange", "green", "yellow"])
    )
    new = re.sub(
        r"const realReviews\s*=\s*\[\s*\{[^\]]*\];",
        f"const realReviews = [\n            {revs_js}\n        ];",
        new,
        count=1,
        flags=re.DOTALL,
    )

    if new == raw:
        print(f"  ⚠️ {slug}: sin cambios — verificar template")
    else:
        path.write_text(new, encoding="utf-8")
        # validar tamaño y unicidad
        lampa_marker = new.count("Lampa")
        print(f"  ✅ {slug}.html  ({len(new)} bytes, restos 'Lampa': {lampa_marker})")


def main() -> None:
    for slug, data in COMUNAS.items():
        transform_zone(slug, data)


if __name__ == "__main__":
    main()
