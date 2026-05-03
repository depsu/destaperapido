#!/usr/bin/env python3
"""
Genera 4 nuevos artículos de blog informacionales.

Posts:
- cuanto-cuesta-limpiar-fosa-septica-chile-2026
- como-destapar-wc-sin-romper-ceramica
- cada-cuanto-limpiar-fosa-septica-segun-personas
- hidrojet-vs-destape-mecanico-cual-elegir
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "public" / "blog"

BASE = "https://www.destaperapido.cl"
HERO = f"{BASE}/images/camio-haciendo-servicio-en-la-calle.webp"
PHONE_E164 = "+56997946463"
PHONE_DISPLAY = "+56 9 9794 6463"


POSTS: dict[str, dict] = {
    "cuanto-cuesta-limpiar-fosa-septica-chile-2026": {
        "title": "Cuánto cuesta limpiar una fosa séptica en Chile 2026",
        "h1": "Cuánto cuesta limpiar una fosa séptica en Chile (2026)",
        "lead": (
            "El precio de limpiar una fosa séptica en Chile depende de tres "
            "variables: el volumen de la fosa, la distancia desde Santiago "
            "y la accesibilidad del terreno. Aquí te damos rangos reales de "
            "2026 y cómo cotizar correctamente."
        ),
        "category_label": "Precios y costos",
        "category_color": "green",
        "desc": (
            "Precios reales 2026 de limpieza de fosas sépticas en Chile: "
            "rangos por volumen, factor distancia y qué evitar. Cotiza al "
            "tiro por WhatsApp."
        ),
        "img_alt": "Camión limpia fosas haciendo servicio en parcela",
        "sections": [
            (
                "Rangos de precio referenciales 2026",
                "<p>Los valores que vamos a comentar son <strong>rangos referenciales</strong> "
                "del mercado en la Región Metropolitana. Cada caso debe cotizarse según "
                "tu fosa real:</p>"
                "<ul>"
                "<li><strong>Fosa residencial pequeña (3-5 m³):</strong> desde $80.000 a $150.000.</li>"
                "<li><strong>Fosa residencial mediana (6-10 m³):</strong> $130.000 a $220.000.</li>"
                "<li><strong>Fosa de parcela / condominio (10-15 m³):</strong> $200.000 a $350.000.</li>"
                "<li><strong>Fosa industrial o agrícola (15+ m³):</strong> a cotizar — depende del retiro de RILes.</li>"
                "</ul>"
                "<p>Los precios incluyen vaciado, lavado básico y transporte hasta planta de "
                "tratamiento autorizada. <strong>El certificado de retiro lo entregamos siempre</strong>, "
                "porque es la prueba sanitaria que tú necesitas conservar.</p>"
            ),
            (
                "Qué hace que el precio suba",
                "<p>Hay tres factores que pueden mover el valor:</p>"
                "<ol>"
                "<li><strong>Distancia desde Santiago centro:</strong> sectores rurales como "
                "Curacaví, Melipilla, Pirque o San José de Maipo agregan tarifa "
                "kilometraje (entre $15.000 y $40.000 según comuna).</li>"
                "<li><strong>Acceso al lugar de la fosa:</strong> si está lejos de la calle "
                "principal, en pendiente, o detrás de cercos, podemos requerir "
                "manguera extra-larga (50-80 metros) o un camión más pequeño. "
                "Cotiza con foto del acceso para evitar sorpresas.</li>"
                "<li><strong>Estado de la fosa:</strong> si está rebalsada, con costras "
                "antiguas o totalmente impermeabilizada, requiere lavado profundo "
                "con hidrojet de alta presión, lo que aumenta el tiempo y el costo.</li>"
                "</ol>"
            ),
            (
                "¿Cuánto cobra una empresa formal vs informal?",
                "<p>En el mercado chileno hay <strong>tres niveles de oferta</strong>:</p>"
                "<ul>"
                "<li><strong>Informal (camionetas con tambor):</strong> los más baratos "
                "($40.000-$70.000) pero <strong>NO entregan certificado de retiro</strong> "
                "y muchas veces vacían en quebradas o calles. Si la SEREMI te audita, "
                "tú quedas con la responsabilidad.</li>"
                "<li><strong>Empresa formal pequeña:</strong> precios en línea con los rangos "
                "del primer apartado, con boleta y certificado.</li>"
                "<li><strong>Empresa con flota propia y resolución sanitaria:</strong> precios "
                "similares pero con respaldo legal completo y atención 24/7.</li>"
                "</ul>"
                "<p>Para casas y parcelas habituales, la empresa formal pequeña es lo "
                "óptimo. Para empresas, condominios o agroindustria, lo recomendable es "
                "la empresa con flota.</p>"
            ),
            (
                "Cómo evitar que te cobren de más",
                "<p>Tres señales de alerta:</p>"
                "<ul>"
                "<li>Cotizan por teléfono sin preguntar el volumen ni la accesibilidad — luego "
                "suben el valor en terreno.</li>"
                "<li>No te muestran resolución sanitaria ni patente de transporte de RILes.</li>"
                "<li>No entregan certificado de retiro firmado.</li>"
                "</ul>"
                "<p>Pide siempre cotización con: <strong>volumen estimado, distancia desde tu "
                "comuna, foto del acceso y boleta/factura</strong>. Si te lo entregan claro, "
                "es buena empresa.</p>"
            ),
            (
                "Cuánto cuesta el destape de cañerías o WC (no es lo mismo)",
                "<p>Mucha gente confunde <strong>limpieza de fosa</strong> con <strong>destape de cañerías</strong>. "
                "Son servicios distintos:</p>"
                "<ul>"
                "<li><strong>Destape WC o lavaplatos en casa:</strong> $35.000 a $65.000 con máquina eléctrica.</li>"
                "<li><strong>Destape de alcantarillado en edificio:</strong> $80.000 a $200.000 según gravedad.</li>"
                "<li><strong>Hidrojet alta presión para grasa o raíces:</strong> $150.000 a $350.000.</li>"
                "</ul>"
                "<p>Si no sabes cuál servicio necesitas, "
                "<a href='/contacto' class='text-blue-600 hover:underline'>cuéntanos por WhatsApp</a> y "
                "te orientamos antes de cotizar.</p>"
            ),
        ],
        "faq": [
            (
                "¿Cuánto se demora el servicio de limpieza de fosa?",
                "Una fosa residencial típica toma entre 30 y 60 minutos en terreno. Una fosa industrial o muy llena puede llevar 2-3 horas.",
            ),
            (
                "¿El precio incluye el lavado interior de la fosa?",
                "El lavado básico siempre. El lavado profundo con hidrojet (cuando la fosa está impermeabilizada) tiene cargo adicional, pero te avisamos antes de hacerlo.",
            ),
            (
                "¿Atienden el mismo día o hay que agendar con anticipación?",
                "Para urgencias atendemos 24/7. Para limpieza programada, lo ideal es agendar con 24-48 horas de anticipación, especialmente en sectores rurales.",
            ),
            (
                "¿El certificado de retiro me sirve si me audita la SEREMI?",
                "Sí. Es el documento que prueba que el lodo fue dispuesto en planta autorizada. Guárdalo siempre por al menos 5 años.",
            ),
        ],
        "cta_intro": (
            "Si quieres precio exacto para tu fosa, escríbenos por WhatsApp con la "
            "dirección, el volumen aproximado y una foto del acceso. Cotizamos en menos "
            "de 10 minutos."
        ),
    },

    "como-destapar-wc-sin-romper-ceramica": {
        "title": "Cómo destapar un WC sin romper la cerámica (guía 2026)",
        "h1": "Cómo destapar un WC sin romper la cerámica",
        "lead": (
            "Un WC tapado se resuelve en el 80% de los casos sin romper, ni "
            "químicos agresivos. Aquí te enseñamos qué hacer paso a paso, "
            "qué NO hacer, y cuándo llamar a un profesional."
        ),
        "category_label": "Urbano / Casa",
        "category_color": "blue",
        "desc": (
            "Guía paso a paso para destapar un WC tapado sin romper la "
            "cerámica ni usar químicos peligrosos. Métodos caseros y "
            "cuándo llamar al técnico."
        ),
        "img_alt": "Baño moderno con cerámica blanca",
        "sections": [
            (
                "Antes de empezar: lo que NO debes hacer",
                "<p>Hay tres cosas que la gente prueba y EMPEORAN el problema:</p>"
                "<ul>"
                "<li><strong>Soda cáustica en exceso:</strong> en cantidad alta puede cristalizarse "
                "dentro de la cañería, formando un tapón aún más duro. Y daña los sellos del WC.</li>"
                "<li><strong>Agua hirviendo:</strong> la cerámica del WC puede agrietarse con shock "
                "térmico. Mejor agua tibia.</li>"
                "<li><strong>Alambre o gancho:</strong> rayan el sifón interno y a la larga generan "
                "fugas. Existen sondas plásticas mucho más seguras.</li>"
                "</ul>"
            ),
            (
                "Método 1 — Sopapa (siempre primero)",
                "<p>La sopapa es la mejor primera línea. Pero hay un truco que pocos "
                "conocen:</p>"
                "<ol>"
                "<li>Asegúrate de que la sopapa quede sumergida — agrega un poco de agua "
                "tibia si el WC está vacío.</li>"
                "<li>Presiona la sopapa contra el desagüe SIN aire en su interior (al "
                "principio inclínala para sacar el aire).</li>"
                "<li>Bombea con movimiento firme y constante — no demasiado rápido — "
                "durante 20-30 segundos.</li>"
                "<li>Levanta de golpe. Si el agua baja, descarga.</li>"
                "</ol>"
                "<p>Repite 3-5 veces. Si el agua no avanza después de 5 intentos, "
                "pasa al método 2.</p>"
            ),
            (
                "Método 2 — Sonda manual (espiral)",
                "<p>La sonda espiral o «culebra» es una mano santa para destapar. Se vende "
                "en ferreterías a partir de $8.000.</p>"
                "<ol>"
                "<li>Inserta la punta en el desagüe del WC.</li>"
                "<li>Gira la manilla mientras empujas — la espiral va avanzando dentro de la "
                "cañería.</li>"
                "<li>Cuando sientas resistencia, sigue girando: la espiral atraviesa o engancha "
                "el tapón.</li>"
                "<li>Tira hacia atrás extrayendo lo que enganchaste.</li>"
                "</ol>"
            ),
            (
                "Método 3 — Bicarbonato + vinagre (ecológico)",
                "<p>Para tapaduras leves de papel o restos orgánicos:</p>"
                "<ol>"
                "<li>Vierte 1 taza de bicarbonato de sodio en el WC.</li>"
                "<li>Agrega 2 tazas de vinagre blanco.</li>"
                "<li>Espera 30 minutos — la reacción burbujeante disuelve grasas y papel.</li>"
                "<li>Tira agua tibia para enjuagar.</li>"
                "</ol>"
                "<p>Es seguro para la cerámica y no daña la red sanitaria.</p>"
            ),
            (
                "Cuándo llamar a un profesional",
                "<p>Llama si:</p>"
                "<ul>"
                "<li>Has probado los 3 métodos y el WC sigue tapado.</li>"
                "<li>Más de un baño de la casa está tapado al mismo tiempo (es atasco "
                "en la red, no en el WC).</li>"
                "<li>Hay olor a alcantarilla o se devuelve agua oscura.</li>"
                "<li>Tienes sospecha de objeto sólido (juguete, paño, etc.) atascado.</li>"
                "</ul>"
                "<p>Un técnico con máquina eléctrica de cabezal cortador raspa las paredes "
                "internas sin romper el WC. Si "
                "<a href='/servicios/destape-wc-y-banos' class='text-blue-600 hover:underline'>"
                "necesitas destape de WC profesional</a>, atendemos 24/7 en toda la RM.</p>"
            ),
        ],
        "faq": [
            (
                "¿La soda cáustica daña el WC?",
                "En dosis bajas no, pero si se acumula puede dañar los sellos del fitting interno y, en cantidades altas, cristalizarse dentro de la cañería formando un tapón aún más duro.",
            ),
            (
                "¿Sirve el destapacañerías líquido del supermercado?",
                "Sirve para tapaduras leves de pelo o jabón en lavamanos. Para WC con tapón sólido, generalmente no. Y si lo usas y luego llama a un técnico, debe saberlo: el químico puede salpicar al destapar.",
            ),
            (
                "¿Cuánto cuesta un destape profesional de WC?",
                "Entre $35.000 y $65.000 según gravedad y comuna. Si el atasco es de la red mayor, el costo sube. Cotizamos al instante por WhatsApp.",
            ),
            (
                "¿Por qué se tapa el WC si solo bajamos papel?",
                "El papel se acumula con grasa y minerales del agua. Si el WC no está bien ventilado o la red tiene poca pendiente, el atasco es cuestión de tiempo. Una limpieza preventiva cada 2 años evita el problema.",
            ),
        ],
        "cta_intro": (
            "Si los métodos caseros no funcionaron, llamamos a un técnico con maquinaria "
            "profesional. Atendemos Las Condes, Vitacura, Ñuñoa, Providencia y todo RM."
        ),
    },

    "cada-cuanto-limpiar-fosa-septica-segun-personas": {
        "title": "Cada cuánto limpiar la fosa séptica (según N° de personas)",
        "h1": "Cada cuánto limpiar una fosa séptica según el número de personas",
        "lead": (
            "La frecuencia ideal para limpiar tu fosa séptica depende del "
            "número de personas que viven en la casa, el tamaño de la fosa "
            "y cuánta agua se usa. Acá te dejamos una tabla simple para "
            "saber cuándo te toca."
        ),
        "category_label": "Mantención",
        "category_color": "purple",
        "desc": (
            "Frecuencia recomendada para limpiar fosa séptica según N° de "
            "personas: tabla 2026 con tamaños y signos de alerta. Calcula "
            "fácil tu próxima fecha."
        ),
        "img_alt": "Casa rural con fosa séptica",
        "sections": [
            (
                "Tabla rápida: frecuencia recomendada (volumen vs personas)",
                "<div class='overflow-x-auto'>"
                "<table class='w-full text-left border-collapse my-6'>"
                "<thead><tr class='bg-slate-100'>"
                "<th class='p-3 border'>Personas</th><th class='p-3 border'>Fosa 3 m³</th>"
                "<th class='p-3 border'>Fosa 5 m³</th><th class='p-3 border'>Fosa 8 m³</th>"
                "</tr></thead>"
                "<tbody>"
                "<tr><td class='p-3 border'>1-2</td><td class='p-3 border'>cada 4 años</td><td class='p-3 border'>cada 6 años</td><td class='p-3 border'>cada 8 años</td></tr>"
                "<tr><td class='p-3 border'>3-4</td><td class='p-3 border'>cada 2-3 años</td><td class='p-3 border'>cada 3-4 años</td><td class='p-3 border'>cada 5 años</td></tr>"
                "<tr><td class='p-3 border'>5-6</td><td class='p-3 border'>cada 1-2 años</td><td class='p-3 border'>cada 2-3 años</td><td class='p-3 border'>cada 3-4 años</td></tr>"
                "<tr><td class='p-3 border'>7+</td><td class='p-3 border'>anual</td><td class='p-3 border'>cada 1-2 años</td><td class='p-3 border'>cada 2-3 años</td></tr>"
                "</tbody></table></div>"
                "<p class='text-sm text-slate-500'>Tabla referencial. Reduce el intervalo si "
                "tienes lavandería intensiva, piscina, mucha grasa de cocina o riego con "
                "aguas grises.</p>"
            ),
            (
                "Por qué importa el número de personas",
                "<p>Cada persona genera entre 100 y 150 litros de aguas servidas al día. "
                "Una familia de 4 produce ~16.000 litros al mes. Esa carga llega a la fosa, "
                "donde la materia sólida sedimenta como lodo en el fondo y la grasa "
                "flota arriba.</p>"
                "<p>Cuando el lodo ocupa más del 50% del volumen útil, la fosa "
                "<strong>deja de tratar correctamente</strong> el efluente — y los pozos de "
                "absorción se saturan, generando malos olores, retornos al baño o "
                "rebalse en el patio.</p>"
            ),
            (
                "5 señales claras de que ya te toca limpieza",
                "<ol>"
                "<li><strong>Olor a alcantarilla</strong> en el patio o cerca de la fosa.</li>"
                "<li><strong>Pasto verde fluorescente</strong> sobre la fosa o pozos absorbentes (la "
                "filtración fertiliza el suelo).</li>"
                "<li><strong>Desagüe lento</strong> en lavaplatos o ducha sin causa aparente.</li>"
                "<li><strong>Ruido de gorgoteo</strong> al bajar el WC.</li>"
                "<li><strong>Agua que sube por la rejilla del baño</strong> al usar la lavadora.</li>"
                "</ol>"
                "<p>Si tienes 2 o más de estas señales, llama a un técnico — no esperes "
                "el rebalse total.</p>"
            ),
            (
                "Mantención preventiva vs limpieza de emergencia",
                "<p>El precio entre limpiar a tiempo o llamar después del rebalse es muy "
                "distinto:</p>"
                "<ul>"
                "<li><strong>Limpieza programada (preventiva):</strong> $80.000-$220.000.</li>"
                "<li><strong>Emergencia (fosa rebalsada):</strong> $150.000-$400.000 + posible reparación de "
                "drenajes saturados.</li>"
                "</ul>"
                "<p>Una limpieza a tiempo cuesta a la mitad y evita olores, plagas y "
                "obras adicionales. Si "
                "<a href='/servicios/mantencion-preventiva' class='text-blue-600 hover:underline'>"
                "te interesa un plan preventivo anual</a>, lo coordinamos en menos de un día.</p>"
            ),
            (
                "DS 236/1926: la norma chilena de fosas",
                "<p>El Reglamento Sanitario chileno (DS 236/1926, modificaciones posteriores) "
                "establece las exigencias técnicas para fosas sépticas, pozos absorbentes y "
                "drenes. Aunque es antiguo, sigue vigente y es lo que la SEREMI usa para "
                "fiscalizar.</p>"
                "<p>Lo más relevante para ti como dueño:</p>"
                "<ul>"
                "<li>El lodo debe ser retirado por empresa con resolución sanitaria.</li>"
                "<li>El destino del lodo debe ser una planta autorizada (no quebradas ni cauces).</li>"
                "<li>Tienes que conservar el certificado de retiro.</li>"
                "</ul>"
            ),
        ],
        "faq": [
            (
                "¿Cómo sé el volumen exacto de mi fosa?",
                "Mide largo × ancho × alto interior y multiplica. Si no tienes acceso, lo medimos en terreno antes de cotizar. Para fosas estándar de 4-6 personas, el volumen típico es 3-5 m³.",
            ),
            (
                "¿Es lo mismo limpiar la fosa que el pozo absorbente?",
                "No. La fosa contiene el lodo y debe vaciarse periódicamente. El pozo absorbente recibe el efluente líquido y NO se vacía: se reemplaza o repermeabiliza si se satura.",
            ),
            (
                "¿Puedo usar productos enzimáticos para alargar la limpieza?",
                "Pueden ayudar a reducir el lodo gradualmente, pero no reemplazan la limpieza física. Funcionan como complemento, no como sustituto.",
            ),
            (
                "¿Qué pasa si nunca limpio la fosa?",
                "El lodo termina ocupando el 100% del volumen y satura los pozos absorbentes. El efluente sin tratar contamina la napa, genera retornos al WC y obliga a obras costosas: cambio de pozo o instalación de planta de tratamiento ($1-3 millones).",
            ),
        ],
        "cta_intro": (
            "Si calculaste con la tabla y estás cerca de la fecha, programa la limpieza "
            "antes que sea urgencia. Cotizamos al tiro por WhatsApp para tu comuna y "
            "tamaño de fosa."
        ),
    },

    "hidrojet-vs-destape-mecanico-cual-elegir": {
        "title": "Hidrojet vs Destape Mecánico: cuál elegir y por qué",
        "h1": "Hidrojet vs destape mecánico: cuál elegir y cuándo",
        "lead": (
            "El destape mecánico (máquina eléctrica) y el hidrojet (camión "
            "de alta presión) NO compiten — se complementan. Aquí "
            "explicamos cuándo conviene cada uno y por qué a veces hay "
            "que combinarlos."
        ),
        "category_label": "Tecnología",
        "category_color": "orange",
        "desc": (
            "Comparativa entre destape mecánico (sondas eléctricas) y "
            "hidrojet de alta presión: cuándo usar cada uno, costos y "
            "casos típicos en Chile."
        ),
        "img_alt": "Camión hidrojet de alta presión",
        "sections": [
            (
                "Qué es el destape mecánico",
                "<p>El destape mecánico usa una <strong>sonda metálica flexible</strong> con "
                "un cabezal cortador en la punta. Un motor eléctrico la hace girar mientras "
                "avanza dentro de la cañería, raspando paredes y triturando el tapón.</p>"
                "<p>Tipos:</p>"
                "<ul>"
                "<li><strong>Sonda manual:</strong> 5-10 metros, para WC o lavamanos doméstico.</li>"
                "<li><strong>Máquina eléctrica residencial (Ridgid K-50, K-60):</strong> 15-30 m, "
                "típica para tapaduras de cocina y baño.</li>"
                "<li><strong>Máquina eléctrica industrial:</strong> 30-60 m con cabezales "
                "intercambiables (corta-raíces, lava-paredes).</li>"
                "</ul>"
            ),
            (
                "Qué es el hidrojet (camión de alta presión)",
                "<p>El hidrojet usa <strong>agua a alta presión</strong> (típicamente 3.000-4.000 PSI) "
                "que se inyecta por una manguera con boquillas direccionadas. La presión "
                "rompe grasa, raíces blandas y residuos compactos.</p>"
                "<p>Es montado en un camión que carga 4.000-8.000 litros de agua. Se "
                "usa para:</p>"
                "<ul>"
                "<li>Limpieza profunda de redes de alcantarillado de edificios.</li>"
                "<li>Cámaras desgrasadoras de restaurantes y casinos.</li>"
                "<li>Drenajes de fosas saturados.</li>"
                "<li>Líneas de cañería con depósitos minerales o sedimentos.</li>"
                "</ul>"
            ),
            (
                "Tabla comparativa rápida",
                "<div class='overflow-x-auto'>"
                "<table class='w-full text-left border-collapse my-6'>"
                "<thead><tr class='bg-slate-100'>"
                "<th class='p-3 border'>Característica</th><th class='p-3 border'>Mecánico</th><th class='p-3 border'>Hidrojet</th>"
                "</tr></thead><tbody>"
                "<tr><td class='p-3 border'>Costo</td><td class='p-3 border'>$35.000-$120.000</td><td class='p-3 border'>$150.000-$350.000</td></tr>"
                "<tr><td class='p-3 border'>Mejor para</td><td class='p-3 border'>Tapaduras puntuales, raíces blandas</td><td class='p-3 border'>Grasa, sedimentos, redes largas</td></tr>"
                "<tr><td class='p-3 border'>Alcance</td><td class='p-3 border'>5-60 m</td><td class='p-3 border'>30-150 m</td></tr>"
                "<tr><td class='p-3 border'>Daño potencial</td><td class='p-3 border'>Mínimo si se usa bien</td><td class='p-3 border'>Mínimo en cañerías sanas</td></tr>"
                "<tr><td class='p-3 border'>Ruido</td><td class='p-3 border'>Bajo</td><td class='p-3 border'>Alto (motor del camión)</td></tr>"
                "</tbody></table></div>"
            ),
            (
                "Cuándo conviene cada uno",
                "<p><strong>Mecánico es ideal cuando:</strong></p>"
                "<ul>"
                "<li>El atasco es puntual (un WC, un lavaplatos, una rejilla).</li>"
                "<li>Sospechas raíces o un objeto sólido.</li>"
                "<li>El presupuesto es ajustado y la red está en buen estado general.</li>"
                "</ul>"
                "<p><strong>Hidrojet es ideal cuando:</strong></p>"
                "<ul>"
                "<li>La red es larga (edificio, condominio, restaurante).</li>"
                "<li>Hay grasa o sedimentos acumulados a lo largo de la cañería.</li>"
                "<li>Buscas <strong>mantención preventiva</strong> que limpie en profundidad.</li>"
                "<li>Tienes cámaras desgrasadoras o pozos de absorción saturados.</li>"
                "</ul>"
            ),
            (
                "Cuándo se combinan los dos",
                "<p>En atascos serios, primero usamos <strong>sonda mecánica</strong> para "
                "abrir un canal, identificar el tipo de tapón y eventualmente cortar "
                "raíces. Luego pasamos <strong>hidrojet</strong> para limpiar las paredes "
                "del tubo y sacar todos los residuos.</p>"
                "<p>Es la fórmula estándar en mantención de edificios y restaurantes: "
                "primero abre, luego lava. Si "
                "<a href='/servicios/camion-alta-presion-hidrojet' class='text-blue-600 hover:underline'>"
                "necesitas servicio combinado de hidrojet</a>, lo coordinamos según el caso.</p>"
            ),
        ],
        "faq": [
            (
                "¿El hidrojet daña las cañerías?",
                "En cañerías en buen estado (PVC, hormigón sano), no. En cañerías muy antiguas o con grietas previas, puede agravar fugas. Por eso siempre revisamos con cámara antes de meter alta presión en redes viejas.",
            ),
            (
                "¿Cuándo conviene la inspección con cámara?",
                "Antes de obras grandes (alquilar/comprar casa, remodelación), si tienes atascos repetidos en el mismo punto, o para diagnosticar el estado general de la red.",
            ),
            (
                "¿Hidrojet vale para destapar un WC residencial?",
                "Es excesivo y caro. Un WC residencial se resuelve con sonda mecánica o sopapa. El hidrojet tiene sentido para redes de varios departamentos o más.",
            ),
            (
                "¿Qué máquinas usan ustedes?",
                "Para residencial usamos máquinas eléctricas Ridgid serie K. Para edificios y empresas tenemos camión hidrojet propio con presión regulable de 1.000 a 4.000 PSI y mangueras de 30 a 100 m.",
            ),
        ],
        "cta_intro": (
            "Si tienes un atasco y no sabes qué método te conviene, mándanos foto y "
            "una breve descripción por WhatsApp. Te decimos al tiro qué equipo "
            "necesitas y cuánto cuesta."
        ),
    },
}


TEMPLATE = """<!DOCTYPE html>
<html lang="es" class="scroll-smooth">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{canonical}">
    <link rel="stylesheet" href="/output.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap"
        rel="stylesheet">
    <link rel="preload" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"></noscript>

    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
        :root {{ --wa-green: #25D366; }}
        .prose h2 {{ font-size: 1.6rem; font-weight: 800; color: #0f172a; margin: 2rem 0 1rem; }}
        .prose p {{ line-height: 1.75; margin-bottom: 1.25rem; color: #334155; }}
        .prose ul, .prose ol {{ margin: 1rem 0 1.5rem 1.5rem; }}
        .prose li {{ margin-bottom: 0.5rem; line-height: 1.6; color: #334155; }}
        .prose table {{ font-size: 0.95rem; }}
        .prose th, .prose td {{ border: 1px solid #e2e8f0; }}
        .wa-floating-btn {{
            position: fixed; bottom: 20px; left: 20px; width: 60px; height: 60px;
            background-color: var(--wa-green); color: white; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3); cursor: pointer; z-index: 1000;
            animation: pulse-green 2s infinite; transition: all 0.3s ease;
        }}
        .wa-floating-btn:hover {{ transform: scale(1.1); }}
        @keyframes pulse-green {{
            0%   {{ box-shadow: 0 0 0 0 rgba(37,211,102,0.7); }}
            70%  {{ box-shadow: 0 0 0 15px rgba(37,211,102,0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(37,211,102,0); }}
        }}
    </style>

    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{hero}">
    <meta property="og:locale" content="es_CL">
    <meta property="og:site_name" content="Destape Rápido">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{hero}">

    <script type="application/ld+json">
{jsonld}
    </script>

    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start': new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-PG2RQNCD');</script>
    <!-- End Google Tag Manager -->
</head>

<body class="bg-white text-slate-700 antialiased">
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PG2RQNCD" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

    <nav class="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-50">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <a href="/" class="flex items-center gap-1">
                    <span class="block font-extrabold text-slate-900 text-lg">DESTAPE<span class="text-brand-600">RÁPIDO</span></span>
                </a>
                <div class="flex items-center gap-4">
                    <a href="/blog" class="text-slate-600 font-semibold hover:text-brand-600">Volver al Blog</a>
                    <a href="tel:{phone}" class="bg-brand-600 text-white px-4 py-2 rounded-full font-bold hover:bg-brand-700 transition">Llamar</a>
                </div>
            </div>
        </div>
    </nav>

    <article class="max-w-3xl mx-auto px-4 py-12">
        <header class="mb-10 text-center">
            <div class="inline-block bg-{color}-100 text-{color}-700 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide mb-4">{category_label}</div>
            <h1 class="text-3xl md:text-5xl font-extrabold text-slate-900 mb-6 leading-tight">{h1}</h1>
            <div class="flex items-center justify-center gap-4 text-slate-500 text-sm">
                <span><i class="fa-regular fa-calendar mr-2"></i>Publicado: Mayo 2026</span>
                <span><i class="fa-regular fa-user mr-2"></i>Equipo Destape Rápido</span>
            </div>
        </header>

        <div class="rounded-2xl overflow-hidden shadow-xl mb-12">
            <img src="{hero}" alt="{img_alt}" class="w-full h-64 object-cover" width="1200" height="630" loading="eager" fetchpriority="high">
        </div>

        <div class="prose prose-lg prose-slate mx-auto">
            <p class="lead text-xl text-slate-700 font-medium mb-8">{lead}</p>
{sections_html}
            <div class="bg-blue-50 border-l-4 border-blue-500 p-5 my-8">
                <p class="font-bold text-blue-900 m-0 mb-1">Resumen rápido</p>
                <p class="m-0 text-blue-800 text-sm">{cta_intro}</p>
            </div>

            <h2 id="faq">Preguntas frecuentes</h2>
{faq_html}
        </div>

        <div class="bg-brand-50 rounded-2xl p-8 mt-12 border border-brand-100 text-center">
            <h3 class="text-2xl font-bold text-brand-900 mb-4">¿Necesitas ayuda profesional?</h3>
            <p class="text-brand-700 mb-6">Atendemos toda la Región Metropolitana 24/7. Cotizamos por WhatsApp en menos de 10 minutos.</p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <a href="tel:{phone}" class="bg-brand-600 hover:bg-brand-700 text-white font-bold py-3 px-8 rounded-xl shadow-lg transition"><i class="fa-solid fa-phone mr-2"></i> Llama al {phone_display}</a>
                <a href="https://wa.me/{phone_wa}" class="bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-8 rounded-xl shadow-lg transition"><i class="fa-brands fa-whatsapp mr-2"></i> WhatsApp</a>
            </div>
        </div>
    </article>

    <footer class="bg-slate-50 text-slate-500 py-12 text-sm border-t border-slate-200">
        <div class="container mx-auto px-4 max-w-5xl">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                <div class="md:col-span-2">
                    <a href="/" class="flex items-center gap-3 mb-4">
                        <span class="block font-extrabold text-slate-900 text-xl">DESTAPE<span class="text-brand-600">RÁPIDO</span></span>
                    </a>
                    <p class="mb-4">Soluciones sanitarias profesionales para hogares y empresas en toda la Región Metropolitana. Atención 24/7.</p>
                    <p class="text-xs">Diseñado por <a href="https://www.paginasfast.cl/" target="_blank" rel="noopener" class="hover:text-brand-600">PaginasFast.cl</a></p>
                </div>
                <div>
                    <h4 class="text-slate-900 font-bold mb-3 uppercase text-xs tracking-wider">Servicios</h4>
                    <ul class="space-y-2">
                        <li><a href="/servicios/destape-alcantarillado" class="hover:text-brand-600">Destape alcantarillado</a></li>
                        <li><a href="/servicios/limpieza-fosas-septicas" class="hover:text-brand-600">Limpieza de fosas</a></li>
                        <li><a href="/servicios/camion-alta-presion-hidrojet" class="hover:text-brand-600">Hidrojet</a></li>
                        <li><a href="/servicios/" class="font-medium text-brand-600 hover:underline">Ver todos</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-slate-900 font-bold mb-3 uppercase text-xs tracking-wider">Blog</h4>
                    <ul class="space-y-2">
                        <li><a href="/blog/" class="hover:text-brand-600">Más artículos</a></li>
                        <li><a href="/contacto" class="hover:text-brand-600">Contacto</a></li>
                        <li><a href="/cobertura" class="hover:text-brand-600">Cobertura</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-slate-200 pt-6 text-center">
                <p>&copy; <span id="year"></span> Destape Rápido. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>

    <a href="https://wa.me/{phone_wa}" class="wa-floating-btn" aria-label="WhatsApp">
        <i class="fa-brands fa-whatsapp" style="font-size: 32px;"></i>
    </a>

    <script>
        document.getElementById('year').textContent = new Date().getFullYear();
    </script>
</body>

</html>
"""


def render_post(slug: str, data: dict) -> str:
    canonical = f"{BASE}/blog/{slug}"

    # Sections
    sections_html = "\n".join(
        f'            <h2>{title}</h2>\n            {body}'
        for title, body in data["sections"]
    )

    # FAQ visible
    faq_html = "\n".join(
        f'''            <div class="bg-slate-50 rounded-lg p-5 mb-3 border border-slate-200">
              <h3 class="font-bold text-slate-900 mb-2">{q}</h3>
              <p class="m-0 text-slate-700">{a}</p>
            </div>'''
        for q, a in data["faq"]
    )

    # JSON-LD: BlogPosting + FAQPage + LocalBusiness ref + Breadcrumb
    jsonld = [
        {
            "@context": "https://schema.org",
            "@type": ["LocalBusiness", "Plumber"],
            "@id": f"{BASE}/#business",
            "name": "Destape Rápido",
            "url": BASE,
            "telephone": PHONE_E164,
            "email": "contacto@destaperapido.cl",
            "priceRange": "$$",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Santiago",
                "addressRegion": "Región Metropolitana",
                "addressCountry": "CL",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": data["title"],
            "description": data["desc"],
            "datePublished": "2026-05-02",
            "dateModified": "2026-05-02",
            "author": {
                "@type": "Person",
                "name": "Equipo Destape Rápido",
                "url": f"{BASE}/nosotros",
            },
            "publisher": {"@id": f"{BASE}/#business"},
            "mainEntityOfPage": canonical,
            "image": HERO,
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in data["faq"]
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE}/blog/"},
                {"@type": "ListItem", "position": 3, "name": data["title"], "item": canonical},
            ],
        },
    ]

    return TEMPLATE.format(
        title=data["title"],
        desc=data["desc"],
        canonical=canonical,
        hero=HERO,
        h1=data["h1"],
        lead=data["lead"],
        category_label=data["category_label"],
        color=data["category_color"],
        img_alt=data["img_alt"],
        cta_intro=data["cta_intro"],
        sections_html=sections_html,
        faq_html=faq_html,
        jsonld=json.dumps(jsonld, ensure_ascii=False, indent=2),
        phone=PHONE_E164,
        phone_display=PHONE_DISPLAY,
        phone_wa=PHONE_E164.lstrip("+"),
    )


def main() -> None:
    BLOG.mkdir(parents=True, exist_ok=True)
    for slug, data in POSTS.items():
        target = BLOG / f"{slug}.html"
        html = render_post(slug, data)
        target.write_text(html, encoding="utf-8")
        # Validar JSON-LD
        import re
        for block in re.findall(
            r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
            html,
            re.DOTALL,
        ):
            json.loads(block.strip())
        print(f"  ✅ {target.relative_to(ROOT)}  ({len(html)} bytes)")


if __name__ == "__main__":
    main()
