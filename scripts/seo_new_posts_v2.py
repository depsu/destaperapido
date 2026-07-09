#!/usr/bin/env python3
"""
Genera 7 nuevos artículos de blog informacionales con investigación verificable
y bloque de autor + fuentes integrado desde la creación.

Posts:
1. quimicos-fosa-septica-verdad-mentira-estafa
2. liquido-azul-banos-quimicos-que-tiene-riesgos
3. cuantos-banos-quimicos-evento-norma-calculo
4. toallitas-humedas-tapan-alcantarillado-fatberg
5. trampa-grasa-restaurante-norma-chilena-ds609
6. certificado-retiro-lodos-fosa-chile-ds-4-2009
7. inspeccion-camara-cctv-codigos-pacp-chile
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "public" / "blog"

BASE = "https://www.destaperapido.cl"
HERO_DEFAULT = f"{BASE}/images/camio-haciendo-servicio-en-la-calle.webp"
PHONE_E164 = "+56965889226"
PHONE_DISPLAY = "+56 9 6588 9226"

AUTHOR_NAME = "Alejandro Rivera Carrasco"
AUTHOR_LINKEDIN = "https://www.linkedin.com/in/alejandro-rivera-carrasco-61436b182/"
AUTHOR_IMG = f"{BASE}/images/autor-alejandro-rivera.svg"
AUTHOR_PAGE = f"{BASE}/nosotros"
AUTHOR_TITLE = "Especialista en saneamiento y destape industrial · 10+ años en terreno"
AUTHOR_BIO = (
    "Lleva más de una década dirigiendo operaciones de destape, limpieza de "
    "fosas e inspección con cámara en la Región Metropolitana. Trabaja a diario "
    "con condominios, parcelas, restaurantes y empresas, y conoce de primera "
    "mano qué funciona, qué es marketing y qué simplemente no se debe hacer "
    "con el sistema sanitario."
)


# ------------------------------------------------------------------
# Definición de posts
# ------------------------------------------------------------------
POSTS = {
    # 1) Verdad y mentira sobre los químicos para fosas sépticas
    "quimicos-fosa-septica-verdad-mentira-estafa": {
        "title": "Químicos para fosa séptica: verdad, mentira y la estafa de “nunca más limpiar”",
        "h1": "Químicos para fosa séptica: lo que sí funciona, lo que no, y la estafa que nadie te cuenta",
        "category_label": "Investigación · Mitos",
        "category_color": "red",
        "image": f"{BASE}/images/camio-haciendo-servicio-en-la-calle.webp",
        "img_alt": "Camión limpia fosas en parcela, junto a productos químicos para fosa séptica",
        "desc": "EPA, Washington State y la FTC ya lo dijeron: los químicos que prometen evitar la limpieza de fosa son marketing. Te mostramos la evidencia.",
        "lead": (
            "Si te dijeron que con un químico “mágico” no vas a tener que limpiar más tu "
            "fosa séptica, tenemos malas noticias. La evidencia oficial — EPA, "
            "Washington State Department of Health, FTC y estudios revisados por pares — "
            "es contundente: ningún aditivo elimina la necesidad de retirar el lodo. "
            "Acá separamos qué químicos sí ayudan, cuáles son inofensivos pero inútiles "
            "y cuáles son derechamente una estafa."
        ),
        "html": """
<h2>Lo primero: ¿por qué la fosa se llena igual?</h2>
<p>Una fosa séptica funciona por <strong>sedimentación + digestión anaerobia</strong>: la materia sólida cae al fondo y bacterias naturalmente presentes en las heces humanas la van degradando. El problema es que ese proceso solo reduce el lodo en alrededor de un 40% — el resto se acumula sí o sí. Lo confirma la literatura técnica especializada (<a href="https://www.iagua.es/blogs/juan-jose-salas/humilde-fosa-septica-fundamentos-tipos-y-diseno" target="_blank" rel="noopener nofollow">iAgua</a>, <a href="https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S1405-77432012000300008" target="_blank" rel="noopener nofollow">SciELO</a>).</p>
<p>Por eso, sin importar lo que prometa la etiqueta, el lodo <em>siempre</em> hay que sacarlo cada cierto tiempo.</p>

<h2>La afirmación más vendida: “con esto, no la limpias nunca más”</h2>
<p>Es la promesa estrella en redes y en mensajes pagados de Facebook. Ya tiene historia legal en EE.UU.:</p>
<ul>
  <li>En 2021 la <a href="https://www.ftc.gov/news-events/news/press-releases/2021/07/ftc-takes-action-against-septic-tank-cleaning-company-made-millions-illegal-robocalls-consumers" target="_blank" rel="noopener nofollow">Federal Trade Commission (FTC)</a> sancionó a Environmental Safety International (productos “Activator 1000”) tras 45 millones de llamadas con marketing engañoso.</li>
  <li>Los responsables de FBK Products se declararon culpables de fraude por vender “Septic Remedy”, prometiendo que reemplazaba el vaciado.</li>
  <li>El estado de Montana directamente <strong>prohíbe</strong> productos que afirmen eliminar la necesidad de pumping.</li>
</ul>
<p>En Chile no hay un símil regulatorio igual de explícito todavía, pero la promesa es la misma — y es igual de falsa.</p>

<h2>Qué dice la EPA, en una línea</h2>
<blockquote class="border-l-4 border-red-500 bg-red-50 p-4 my-6 text-slate-800">
  “No existe evidencia científica de que los aditivos biológicos o químicos ayuden o sean necesarios para el funcionamiento de un sistema séptico que ya opera correctamente.” — <a href="https://www.epa.gov/system/files/documents/2024-09/septictankadditivesfactsheet.pdf" target="_blank" rel="noopener nofollow">U.S. EPA, Septic Tank Additives Fact Sheet (2024)</a>.
</blockquote>

<h2>Qué dice el estudio más serio que existe</h2>
<p>El paper de referencia, publicado en <em>Water Environment Research</em> y citado por el <a href="https://pubmed.ncbi.nlm.nih.gov/18236933/" target="_blank" rel="noopener nofollow">PubMed (Pratt et al., 2008)</a>, midió 48 fosas reales en operación durante 12 meses comparando tres aditivos bacterianos vs. un grupo control. Resultado: <strong>ninguno de los aditivos generó diferencia estadísticamente significativa</strong> en la población microbiana ni en la reducción de lodos.</p>
<p>El <a href="https://extension.wsu.edu/clark/naturalresources/smallacreageprogram/septic-tank-additives/" target="_blank" rel="noopener nofollow">Departamento de Salud de Washington (DOH)</a> mantiene un registro de aditivos aprobados, pero deja en claro algo muy importante: la aprobación significa “no es tóxico”, NO significa “funciona”. Es la diferencia que la mayoría de las marcas se cuida de no contar.</p>

<h2>El tipo de químico más peligroso (para tu fosa)</h2>
<p>No todos los “químicos para fosa” son iguales. Los <strong>aditivos químicos fuertes</strong> — basados en hidróxidos cáusticos, ácido sulfúrico o peróxido de hidrógeno — son los que pueden hacer daño real:</p>
<ul>
  <li>Destruyen la flora bacteriana que sí está trabajando en la fosa.</li>
  <li>Degradan la estructura del suelo del pozo absorbente, reduciendo su capacidad de filtración (<a href="https://www.epa.gov/system/files/documents/2024-09/septictankadditivesfactsheet.pdf" target="_blank" rel="noopener nofollow">EPA, 2024</a>).</li>
  <li>Pueden contaminar la napa freática si la fosa filtra.</li>
</ul>
<p>Por eso el estado de Washington <strong>los prohibió</strong>: el costo ambiental supera con creces cualquier beneficio.</p>

<h2>Tabla rápida: qué sí, qué no</h2>
<div class="overflow-x-auto">
  <table class="w-full text-left border-collapse my-6">
    <thead><tr class="bg-slate-100"><th class="p-3 border">Producto / promesa</th><th class="p-3 border">Veredicto técnico</th></tr></thead>
    <tbody>
      <tr><td class="p-3 border">“Nunca más limpia tu fosa”</td><td class="p-3 border text-red-700 font-bold">Falso. FTC ya sancionó casos así.</td></tr>
      <tr><td class="p-3 border">Aditivos enzimáticos / bacterianos en sobre</td><td class="p-3 border text-amber-700">Inocuos. Sin efecto demostrado en estudios.</td></tr>
      <tr><td class="p-3 border">Sosa cáustica, ácido o peróxido</td><td class="p-3 border text-red-700 font-bold">Dañinos. Matan la flora útil y degradan el dren.</td></tr>
      <tr><td class="p-3 border">Limpieza física por camión limpia fosas</td><td class="p-3 border text-emerald-700 font-bold">Único método validado. Cada 1 a 4 años según uso.</td></tr>
      <tr><td class="p-3 border">Mantención preventiva con inspección</td><td class="p-3 border text-emerald-700 font-bold">Lo más costo-eficiente a largo plazo.</td></tr>
    </tbody>
  </table>
</div>

<h2>“Pero compré uno y me bajó el olor, ¿es mentira?”</h2>
<p>Lo que muchas veces sucede no es que el lodo desapareció: lo que cambia es la <strong>capa flotante</strong> y los gases ácidos del proceso (sulfuro de hidrógeno, mercaptanos) que generan el mal olor (<a href="https://smartwaterbio.com/blog/fosa-septica-causas-procesos/" target="_blank" rel="noopener nofollow">referencia técnica</a>). Es un alivio real, pero <em>cosmético</em>: el lodo del fondo sigue creciendo y, si no lo retiras, la fosa colapsa igual.</p>

<h2>Qué hacemos nosotros y por qué</h2>
<p>En <strong>Destape Rápido</strong> no vendemos químicos milagrosos por una razón sencilla: si funcionaran, dejaríamos sin trabajo a la mitad de la flota — y la EPA, la FTC, Washington DOH y los estudios científicos coinciden en que <em>no funcionan</em>. Lo que sí ofrecemos es:</p>
<ul>
  <li><strong>Inspección + medición de lodo</strong> antes de cotizar (te decimos si <em>realmente</em> necesitas vaciado).</li>
  <li><strong>Limpieza con camión + lavado interior</strong> y certificado de retiro a planta autorizada.</li>
  <li><strong>Plan preventivo</strong> según el número de personas, tamaño de fosa y uso, alineado al <a href="https://www.bcn.cl/leychile/Navegar?idNorma=171085" target="_blank" rel="noopener nofollow">DS 236/1926</a>.</li>
</ul>

<div class="bg-blue-50 border-l-4 border-blue-500 p-5 my-8">
  <p class="font-bold text-blue-900 m-0 mb-1">Resumen rápido</p>
  <p class="m-0 text-blue-800 text-sm">Si te ofrecen “no limpiar nunca más” con un químico: corre. La única solución validada por la ciencia y la normativa chilena sigue siendo la limpieza física, hecha por una empresa con resolución sanitaria y certificado de disposición de lodos.</p>
</div>

<h2 id="faq">Preguntas frecuentes</h2>
<div class="bg-slate-50 rounded-lg p-5 mb-3 border border-slate-200">
  <h3 class="font-bold text-slate-900 mb-2">¿Hay algún químico que sí ayude a la fosa?</h3>
  <p class="m-0 text-slate-700">Los productos enzimáticos suaves no dañan, pero ningún estudio serio demuestra que reduzcan el lodo de forma sostenida. Pueden ayudar puntualmente con olores. La limpieza física sigue siendo obligatoria.</p>
</div>
<div class="bg-slate-50 rounded-lg p-5 mb-3 border border-slate-200">
  <h3 class="font-bold text-slate-900 mb-2">¿La sosa cáustica no “destapa” la fosa?</h3>
  <p class="m-0 text-slate-700">Te puede destapar una cañería puntualmente, pero al llegar a la fosa mata las bacterias útiles y ataca el sistema de absorción. Tu fosa funciona peor después, no mejor.</p>
</div>
<div class="bg-slate-50 rounded-lg p-5 mb-3 border border-slate-200">
  <h3 class="font-bold text-slate-900 mb-2">¿Cómo sé si la empresa que contrato es seria?</h3>
  <p class="m-0 text-slate-700">Tres señales: (1) entrega <strong>certificado de retiro</strong> firmado, (2) tiene <strong>resolución sanitaria</strong>, (3) declara la disposición a planta autorizada bajo el <a href="https://www.bcn.cl/leychile/N?i=1007456" target="_blank" rel="noopener nofollow">DS 4/2009</a> sobre manejo de lodos.</p>
</div>
""",
        "faq": [
            ("¿Hay algún químico que sí ayude a la fosa?", "Los productos enzimáticos suaves no dañan, pero ningún estudio serio demuestra que reduzcan el lodo de forma sostenida. Pueden ayudar puntualmente con olores. La limpieza física sigue siendo obligatoria."),
            ("¿La sosa cáustica no \"destapa\" la fosa?", "Te puede destapar una cañería puntualmente, pero al llegar a la fosa mata las bacterias útiles y ataca el sistema de absorción. Tu fosa funciona peor después, no mejor."),
            ("¿Cómo sé si la empresa que contrato es seria?", "Tres señales: (1) entrega certificado de retiro firmado, (2) tiene resolución sanitaria, (3) declara la disposición a planta autorizada bajo el DS 4/2009 sobre manejo de lodos."),
        ],
        "sources": [
            ("U.S. EPA (2024) — Septic Tank Additives Fact Sheet.", "https://www.epa.gov/system/files/documents/2024-09/septictankadditivesfactsheet.pdf"),
            ("Pratt et al. (2008) — Septic tank additive impacts on microbial populations. PubMed.", "https://pubmed.ncbi.nlm.nih.gov/18236933/"),
            ("Washington State DOH — Listado oficial de aditivos sépticos (no implica eficacia).", "https://doh.wa.gov/sites/default/files/legacy/Documents/Pubs/337-025.pdf"),
            ("WSU Extension — Septic Tank Additives.", "https://extension.wsu.edu/clark/naturalresources/smallacreageprogram/septic-tank-additives/"),
            ("FTC (2021) — Caso Environmental Safety International.", "https://www.ftc.gov/news-events/news/press-releases/2021/07/ftc-takes-action-against-septic-tank-cleaning-company-made-millions-illegal-robocalls-consumers"),
            ("DS 236/1926 — Reglamento General de Alcantarillados Particulares (BCN).", "https://www.bcn.cl/leychile/Navegar?idNorma=171085"),
            ("DS 4/2009 MINSEGPRES — Reglamento de Lodos de Plantas de Tratamiento.", "https://www.bcn.cl/leychile/N?i=1007456"),
            ("iAgua — La humilde fosa séptica: fundamentos, tipos y diseño (Juan José Salas).", "https://www.iagua.es/blogs/juan-jose-salas/humilde-fosa-septica-fundamentos-tipos-y-diseno"),
        ],
        "related": [
            ("/blog/cada-cuanto-limpiar-fosa-septica-segun-personas", "Cada cuánto limpiar la fosa según N° de personas"),
            ("/blog/cuanto-cuesta-limpiar-fosa-septica-chile-2026", "Cuánto cuesta limpiar una fosa séptica en Chile 2026"),
            ("/blog/senales-fosa-septica-al-limite", "5 señales de que tu fosa séptica está al límite"),
        ],
    },

    # 2) Líquido azul de los baños químicos
    "liquido-azul-banos-quimicos-que-tiene-riesgos": {
        "title": "Líquido azul de los baños químicos: qué tiene, por qué huele a “químico” y cuál es el riesgo real",
        "h1": "El líquido azul de los baños químicos: composición, mitos y la nueva generación libre de formaldehído",
        "category_label": "Baños químicos",
        "category_color": "blue",
        "image": f"{BASE}/images/camio-haciendo-servicio-en-la-calle.webp",
        "img_alt": "Baños químicos portátiles con líquido azul para evento",
        "desc": "Qué tiene realmente el líquido azul de los baños químicos, por qué se cambió a alternativas sin formaldehído, y cómo elegir un proveedor serio en Chile.",
        "lead": (
            "El “líquido azul” no es solo color. Es un cóctel de biocidas, surfactantes "
            "y fragancia diseñado para frenar la fermentación dentro del estanque del "
            "baño portátil. La industria pasó de usar formaldehído — clasificado por "
            "la IARC como carcinógeno humano — a fórmulas más seguras. "
            "Te explicamos qué hay adentro, qué cuidar y cómo distinguir un servicio "
            "serio de uno improvisado."
        ),
        "html": """
<h2>¿Para qué sirve el líquido azul?</h2>
<p>El estanque de un baño portátil acumula desechos sin oxígeno. Sin biocida, en horas comienza la fermentación anaerobia y aparecen <strong>sulfuro de hidrógeno (H₂S)</strong> y mercaptanos: el famoso “olor a alcantarilla”. El líquido azul cumple cuatro funciones:</p>
<ol>
  <li><strong>Biocida:</strong> frena la población bacteriana que produce los gases.</li>
  <li><strong>Surfactante:</strong> reduce la tensión superficial para mejor limpieza.</li>
  <li><strong>Fragancia:</strong> enmascara el olor remanente.</li>
  <li><strong>Colorante (azul):</strong> indicador visual — cuando se ve verde o marrón, es momento de vaciar.</li>
</ol>

<h2>Qué tenía “antes” y por qué se está dejando</h2>
<p>Históricamente el biocida principal era <strong>formaldehído</strong>: barato y muy efectivo. El problema es que está clasificado por la IARC como carcinógeno humano (Grupo 1) y la <a href="https://www.atsdr.cdc.gov/es/phs/es_phs111.html" target="_blank" rel="noopener nofollow">ATSDR / CDC</a> lo ha documentado como irritante de ojos, vías respiratorias y piel. Por eso la industria global migró a opciones más seguras.</p>

<h2>Qué se usa hoy</h2>
<p>En Chile y el resto del mercado serio, los biocidas más comunes hoy son:</p>
<ul>
  <li><strong>Glutaraldehído (pentanodial):</strong> efectivo, pero también irritante en alta concentración.</li>
  <li><strong>Compuestos de amonio cuaternario (Quats):</strong> menos agresivos, ampliamente usados.</li>
  <li><strong>Bronopol</strong> y otras sales orgánicas como reemplazos de bajo perfil.</li>
  <li><strong>Fórmulas enzimáticas/probióticas:</strong> 100% biodegradables, sin biocidas duros — la generación más nueva, ideal para eventos al aire libre.</li>
</ul>
<p>Proveedores locales como <a href="https://alarquimica.com/insumos-banos-quimicos/" target="_blank" rel="noopener nofollow">Alar Química Chile</a> ya distribuyen líneas libres de formaldehído.</p>

<h2>Cómo identificar un baño con líquido en mal estado</h2>
<ul>
  <li>Olor metálico-ácido fuerte (no la fragancia mentolada del azul nuevo).</li>
  <li>Líquido café-grisáceo en vez de azul.</li>
  <li>Espuma blanca seca en el borde del estanque.</li>
</ul>
<p>Si lo ves en un evento o faena: ese baño no fue mantenido en su frecuencia correcta.</p>

<h2>El gran mito: “mientras más químico, mejor”</h2>
<p>Falso. La sobredosis genera tres problemas:</p>
<ol>
  <li>Aumenta el costo sin mejora de desempeño (la curva es plana después de la dosis recomendada).</li>
  <li>Puede gasificar el cubículo y generar irritación de ojos a los usuarios.</li>
  <li>Cuando los lodos se transportan a planta de tratamiento, pueden interferir con los procesos biológicos.</li>
</ol>

<h2>¿Cuál es el riesgo real para usuarios?</h2>
<p>Para un usuario común que entra dos minutos a un baño portátil bien mantenido, el riesgo de los biocidas modernos es <strong>bajo</strong>. Donde sí importa la composición es para:</p>
<ul>
  <li><strong>Operadores de bombas y limpieza</strong> que manipulan el líquido concentrado (deben usar EPP).</li>
  <li><strong>Eventos largos al aire libre con poca ventilación</strong> en espacios cerrados.</li>
  <li><strong>Faenas en ambientes calurosos</strong>, donde la volatilización es mayor.</li>
</ul>

<h2>Cómo elegir un proveedor de baños químicos serio</h2>
<p>Cinco preguntas para hacer antes de arrendar:</p>
<ol>
  <li>¿Usan formaldehído o ya migraron a fórmulas sin formaldehído?</li>
  <li>¿Cuál es la frecuencia de mantención según número de usuarios?</li>
  <li>¿Tienen <strong>resolución sanitaria</strong> y <strong>plan de disposición</strong> de los lodos?</li>
  <li>¿Cuántas unidades calculan según asistentes y duración del evento?</li>
  <li>¿Se ajusta el pedido a la <a href="https://www.bcn.cl/leychile/navegar?idNorma=1017350" target="_blank" rel="noopener nofollow">norma chilena de eventos masivos</a> (DS 10/2010 MINSAL)?</li>
</ol>

<div class="bg-blue-50 border-l-4 border-blue-500 p-5 my-8">
  <p class="font-bold text-blue-900 m-0 mb-1">Resumen rápido</p>
  <p class="m-0 text-blue-800 text-sm">El líquido azul moderno es seguro si está bien dosificado y la mantención es regular. Pide proveedor con fórmula libre de formaldehído, resolución sanitaria y certificado de disposición.</p>
</div>

<h2 id="faq">Preguntas frecuentes</h2>
<div class="bg-slate-50 rounded-lg p-5 mb-3 border border-slate-200">
  <h3 class="font-bold text-slate-900 mb-2">¿El líquido azul es tóxico para la piel?</h3>
  <p class="m-0 text-slate-700">El líquido diluido dentro del estanque no es de contacto directo. El concentrado sí requiere EPP. La línea “sin formaldehído” reduce significativamente el riesgo dermatológico.</p>
</div>
<div class="bg-slate-50 rounded-lg p-5 mb-3 border border-slate-200">
  <h3 class="font-bold text-slate-900 mb-2">¿Se puede tirar el contenido del estanque al alcantarillado?</h3>
  <p class="m-0 text-slate-700">No. Por reglamento chileno, debe ser retirado por empresa con resolución sanitaria y dispuesto en planta autorizada. Los lodos están regulados por el <a href="https://www.bcn.cl/leychile/N?i=1007456" target="_blank" rel="noopener nofollow">DS 4/2009</a>.</p>
</div>
<div class="bg-slate-50 rounded-lg p-5 mb-3 border border-slate-200">
  <h3 class="font-bold text-slate-900 mb-2">¿Sirven las pastillas “azules” caseras de motorhome?</h3>
  <p class="m-0 text-slate-700">Sí, son la versión doméstica del mismo principio. Vienen con dosificación calculada para estanques pequeños (10-20 L). Para baños portátiles industriales se usan formulaciones líquidas distintas.</p>
</div>
""",
        "faq": [
            ("¿El líquido azul es tóxico para la piel?", "El líquido diluido dentro del estanque no es de contacto directo. El concentrado sí requiere EPP. La línea \"sin formaldehído\" reduce significativamente el riesgo dermatológico."),
            ("¿Se puede tirar el contenido del estanque al alcantarillado?", "No. Por reglamento chileno, debe ser retirado por empresa con resolución sanitaria y dispuesto en planta autorizada. Los lodos están regulados por el DS 4/2009."),
            ("¿Sirven las pastillas \"azules\" caseras de motorhome?", "Sí, son la versión doméstica del mismo principio. Vienen con dosificación calculada para estanques pequeños (10-20 L). Para baños portátiles industriales se usan formulaciones líquidas distintas."),
        ],
        "sources": [
            ("ATSDR / CDC — Resumen de Salud Pública: Formaldehído.", "https://www.atsdr.cdc.gov/es/phs/es_phs111.html"),
            ("Alar Química Chile — Insumos para baños químicos (proveedor industrial local).", "https://alarquimica.com/insumos-banos-quimicos/"),
            ("DS 10/2010 MINSAL — Reglamento de eventos masivos (incluye baños químicos).", "https://www.bcn.cl/leychile/navegar?idNorma=1017350"),
            ("DS 4/2009 MINSEGPRES — Reglamento de Lodos.", "https://www.bcn.cl/leychile/N?i=1007456"),
            ("Norma UNE-EN 16194 — Cabinas sanitarias móviles, requisitos y cálculo.", "https://www.une.org/encuentra-tu-norma/busca-tu-norma/norma?c=N0049834"),
        ],
        "related": [
            ("/blog/cuantos-banos-quimicos-evento-norma-calculo", "Cuántos baños químicos para tu evento"),
            ("/servicios/banos-quimicos", "Servicio de baños químicos"),
            ("/blog/quimicos-fosa-septica-verdad-mentira-estafa", "Verdad y mentira de los químicos para fosa"),
        ],
    },

    # 3) Cuántos baños químicos
    "cuantos-banos-quimicos-evento-norma-calculo": {
        "title": "Cuántos baños químicos necesitas para tu evento (cálculo según norma y experiencia)",
        "h1": "Cuántos baños químicos necesitas para tu evento: cálculo según norma y experiencia",
        "category_label": "Baños químicos · Eventos",
        "category_color": "blue",
        "image": f"{BASE}/images/camio-haciendo-servicio-en-la-calle.webp",
        "img_alt": "Calculadora de baños químicos para eventos masivos en Chile",
        "desc": "Tabla de cálculo de baños químicos por asistentes y duración, basada en norma UNE-EN 16194 y la experiencia en terreno chileno.",
        "lead": (
            "La pregunta más repetida cuando alguien organiza un matrimonio, fiesta "
            "patria, faena o feria es la misma: ¿cuántos baños químicos pido? "
            "Acá la tabla de cálculo basada en estándares internacionales "
            "(UNE-EN 16194) y la experiencia en eventos chilenos."
        ),
        "html": """
<h2>Tabla de cálculo rápido</h2>
<div class="overflow-x-auto">
  <table class="w-full text-left border-collapse my-6">
    <thead><tr class="bg-slate-100"><th class="p-3 border">Asistentes</th><th class="p-3 border">Evento ≤4 h</th><th class="p-3 border">Evento 4-8 h</th><th class="p-3 border">Evento >8 h</th></tr></thead>
    <tbody>
      <tr><td class="p-3 border">50</td><td class="p-3 border">1</td><td class="p-3 border">2</td><td class="p-3 border">2</td></tr>
      <tr><td class="p-3 border">100</td><td class="p-3 border">2</td><td class="p-3 border">3</td><td class="p-3 border">4</td></tr>
      <tr><td class="p-3 border">250</td><td class="p-3 border">4</td><td class="p-3 border">6</td><td class="p-3 border">8</td></tr>
      <tr><td class="p-3 border">500</td><td class="p-3 border">7</td><td class="p-3 border">10</td><td class="p-3 border">14</td></tr>
      <tr><td class="p-3 border">1.000</td><td class="p-3 border">14</td><td class="p-3 border">20</td><td class="p-3 border">28</td></tr>
      <tr><td class="p-3 border">3.000+</td><td class="p-3 border">cotizar plan</td><td class="p-3 border">cotizar plan</td><td class="p-3 border">cotizar plan</td></tr>
    </tbody>
  </table>
</div>
<p class="text-sm text-slate-500">Tabla referencial alineada a la <a href="https://www.une.org/encuentra-tu-norma/busca-tu-norma/norma?c=N0049834" target="_blank" rel="noopener nofollow">norma UNE-EN 16194</a> y a la práctica habitual en eventos masivos.</p>

<h2>Reglas que ajustan la cifra</h2>
<ul>
  <li><strong>Si hay alimentos o alcohol:</strong> +30% sobre la base.</li>
  <li><strong>Si más del 50% del público es femenino:</strong> +30% (filas más largas, mayor frecuencia).</li>
  <li><strong>Cada 20 baños:</strong> al menos 1 unidad accesible para personas con movilidad reducida.</li>
  <li><strong>Faena de construcción:</strong> 1 baño cada 15-20 trabajadores con mantención 2-3 veces por semana.</li>
</ul>

<h2>Marco regulatorio en Chile</h2>
<p>Eventos masivos (≥3.000 personas) requieren autorización municipal y un informe técnico de prevención de riesgos que incluye servicios higiénicos, según el <a href="https://www.bcn.cl/leychile/navegar?idNorma=1017350" target="_blank" rel="noopener nofollow">DS 10/2010 MINSAL</a>. Para faenas de construcción, los baños químicos no pueden estar a más de 75 m del área de trabajo.</p>

<h2>Cuántos por hora aguanta un baño</h2>
<p>Una unidad estándar (~250 L) atiende cómodamente 8-10 usuarios por jornada antes de necesitar mantención. Si en tu evento sirves comida y alcohol, considera mantención intermedia para no llegar al rebalse.</p>

<h2>Errores típicos de cálculo</h2>
<ol>
  <li><strong>Pedir según el aforo, no según la asistencia real esperada</strong> (siempre subestima).</li>
  <li><strong>Olvidar que el horario peak concentra el 60% del uso</strong> en 2-3 horas.</li>
  <li><strong>Saltarse la mantención</strong> en eventos de más de 8 horas.</li>
  <li><strong>No contar accesibilidad</strong> y exponerse a una multa municipal.</li>
</ol>

<div class="bg-blue-50 border-l-4 border-blue-500 p-5 my-8">
  <p class="font-bold text-blue-900 m-0 mb-1">Consejo en una línea</p>
  <p class="m-0 text-blue-800 text-sm">Si tu evento dura más de 6 horas y hay alcohol, redondea hacia arriba sin culpa: cuesta menos un baño extra que un evento manchado por filas y mal olor.</p>
</div>

<h2 id="faq">Preguntas frecuentes</h2>
<div class="bg-slate-50 rounded-lg p-5 mb-3 border border-slate-200">
  <h3 class="font-bold text-slate-900 mb-2">¿Quién paga los baños químicos en una boda en parcela?</h3>
  <p class="m-0 text-slate-700">Habitualmente el novio/novia o el productor del evento. El proveedor entrega lavamanos y mantención según horas.</p>
</div>
<div class="bg-slate-50 rounded-lg p-5 mb-3 border border-slate-200">
  <h3 class="font-bold text-slate-900 mb-2">¿Necesito permiso municipal para arrendar baños?</h3>
  <p class="m-0 text-slate-700">Para eventos masivos sí (>3.000 personas, DS 10/2010). En eventos privados no, pero igual debes asegurar saneamiento mínimo y disposición legal de los residuos.</p>
</div>
""",
        "faq": [
            ("¿Quién paga los baños químicos en una boda en parcela?", "Habitualmente el novio/novia o el productor del evento. El proveedor entrega lavamanos y mantención según horas."),
            ("¿Necesito permiso municipal para arrendar baños?", "Para eventos masivos sí (>3.000 personas, DS 10/2010). En eventos privados no, pero igual debes asegurar saneamiento mínimo y disposición legal de los residuos."),
        ],
        "sources": [
            ("DS 10/2010 MINSAL — Reglamento de eventos masivos (BCN).", "https://www.bcn.cl/leychile/navegar?idNorma=1017350"),
            ("Norma UNE-EN 16194 — Cabinas sanitarias móviles.", "https://www.une.org/encuentra-tu-norma/busca-tu-norma/norma?c=N0049834"),
            ("ChileAtiende — Solicitar autorización para eventos masivos.", "https://www.chileatiende.gob.cl/fichas/3784-solicitar-autorizacion-para-realizar-eventos-masivos"),
        ],
        "related": [
            ("/blog/liquido-azul-banos-quimicos-que-tiene-riesgos", "Líquido azul de baños químicos: composición y riesgos"),
            ("/servicios/banos-quimicos", "Servicio de baños químicos"),
        ],
    },

    # 4) Toallitas húmedas y fatbergs
    "toallitas-humedas-tapan-alcantarillado-fatberg": {
        "title": "Toallitas húmedas y fatbergs: por qué tapan tu alcantarillado (y cuánto le cuestan al sistema)",
        "h1": "Por qué las toallitas húmedas tapan tu alcantarillado: los “fatbergs” explicados",
        "category_label": "Mantención · Investigación",
        "category_color": "amber",
        "image": f"{BASE}/images/camion-haciendo-destape-en-subterraneo.webp",
        "img_alt": "Cañería tapada con toallitas húmedas y grasa - fatberg",
        "desc": "Toallitas, grasa y compresas crean fatbergs que bloquean alcantarillados. Datos UK + lo que vemos en condominios chilenos.",
        "lead": (
            "Las toallitas “biodegradables”, las compresas y la grasa de cocina son la "
            "tríada que está volcando alcantarillados en todo el mundo. Reino Unido "
            "gasta cerca de £100 millones al año desbloqueando los llamados “fatbergs”. "
            "En Chile, las matrices de condominios viven la misma película — solo que "
            "sin la prensa."
        ),
        "html": """
<h2>¿Qué es un fatberg?</h2>
<p>Un fatberg es una masa sólida formada por <strong>grasa, aceites y materiales no biodegradables</strong> (toallitas, hilo dental, papel absorbente) que se aglomeran y endurecen en el alcantarillado. La <a href="https://www.water.org.uk/waste-water/fighting-fatbergs" target="_blank" rel="noopener nofollow">Water UK</a> calcula ~300.000 atascos al año en Reino Unido y un costo cercano a £100 millones. <a href="https://www.thameswater.co.uk/news/2025/oct/thames-water-removes-100-tonne-fatberg" target="_blank" rel="noopener nofollow">Thames Water retiró en 2025 un fatberg de 100 toneladas en Feltham</a> (equivalente a 8 buses de dos pisos).</p>

<h2>Lo que pasa en Chile (sin las noticias)</h2>
<p>En condominios y edificios de Santiago vemos el mismo patrón a menor escala:</p>
<ul>
  <li>Matriz tapada en piso -1 después de un fin de semana largo (toallitas + grasa).</li>
  <li>Sumideros de comunidad rebalsados tras lluvias intensas (basura del patio + grasa).</li>
  <li>Restaurantes con trampas saturadas que descargan grasa al alcantarillado.</li>
</ul>

<h2>El mito “biodegradable”</h2>
<p>Muchas toallitas se publicitan como “biodegradables” o “flushable”. La realidad: <strong>no se desintegran en el tiempo de tránsito típico del alcantarillado</strong>. Estudios y demandas en EE.UU. han llevado a que la rotulación cambie en marcas líderes. La regla de oro: solo papel higiénico al WC.</p>

<h2>Los 5 ítems que más fatbergs causan</h2>
<ol>
  <li>Toallitas húmedas (incluso “flushable”).</li>
  <li>Aceite de cocina vertido al lavaplatos.</li>
  <li>Restos de comida cocinada con grasa (caldos, frituras).</li>
  <li>Toallas higiénicas y tampones.</li>
  <li>Hilo dental y bastoncillos.</li>
</ol>

<h2>Cómo se detectan y eliminan</h2>
<ul>
  <li><strong>Cámara de inspección</strong> primero — para ver tamaño y ubicación. Codificación PACP (NASSCO) para defectos.</li>
  <li><strong>Hidrojet de alta presión</strong> con boquilla rotatoria para fragmentar y arrastrar.</li>
  <li><strong>Aspiración con camión limpia fosas</strong> si hay material acumulado en cámaras.</li>
  <li>En matriz urbana, coordinación con la sanitaria local (Aguas Andinas / Smapa).</li>
</ul>

<h2>Qué puede hacer una comunidad para prevenirlos</h2>
<ol>
  <li>Cartelería en baños comunes (hall, gimnasio, piscina): “solo papel higiénico”.</li>
  <li>Trampa de grasa en cafetería o sala de eventos.</li>
  <li>Mantención preventiva con cámara cada 12-18 meses para matriz vertical.</li>
  <li>Plan anual con empresa de saneamiento (siempre sale más barato que la urgencia).</li>
</ol>

<h2>El estándar técnico que usamos</h2>
<p>Para diagnóstico con cámara seguimos el estándar <a href="https://www.nassco.org/trenchless-technology/assessment/" target="_blank" rel="noopener nofollow">NASSCO PACP</a>, que asigna códigos de defectos y un grado de severidad de 1 a 5. Esto permite reportes objetivos y trazables, no “a ojo”.</p>

<div class="bg-blue-50 border-l-4 border-blue-500 p-5 my-8">
  <p class="font-bold text-blue-900 m-0 mb-1">Resumen rápido</p>
  <p class="m-0 text-blue-800 text-sm">Si vives en condominio: pide al administrador inspección con cámara una vez al año. Es la diferencia entre cobrar gasto común normal o tener un fatberg de 200 kg en piso -1.</p>
</div>
""",
        "faq": [
            ("¿Las toallitas \"flushable\" se pueden tirar al WC?", "Técnicamente sí, pero generan atascos igual. Recomendamos siempre desecharlas en basurero, incluso las que dicen \"biodegradables\"."),
            ("¿Cuánto cuesta destapar un fatberg en un condominio?", "Depende del tamaño y acceso. Una matriz de 4-6 pisos puede ir de $200.000 a $600.000 si requiere hidrojet + cámara + aspiración. Mantención preventiva cuesta menos de la mitad."),
        ],
        "sources": [
            ("Water UK — Fighting fatbergs.", "https://www.water.org.uk/waste-water/fighting-fatbergs"),
            ("Thames Water — Fatberg de 100 toneladas en Feltham (2025).", "https://www.thameswater.co.uk/news/2025/oct/thames-water-removes-100-tonne-fatberg"),
            ("NASSCO — PACP / Pipeline Assessment Certification Program.", "https://www.nassco.org/trenchless-technology/assessment/"),
            ("DS 609/1998 MOP — Norma para descargas de RILes a alcantarillado.", "https://www.bcn.cl/leychile/navegar?idNorma=121486"),
        ],
        "related": [
            ("/blog/por-que-se-tapa-desague-cocina", "Por qué se tapa el desagüe de tu cocina"),
            ("/blog/hidrojet-vs-destape-mecanico-cual-elegir", "Hidrojet vs destape mecánico"),
            ("/blog/inspeccion-camara-cctv-codigos-pacp-chile", "Inspección con cámara y códigos PACP"),
        ],
    },

    # 5) Trampa de grasa y normativa
    "trampa-grasa-restaurante-norma-chilena-ds609": {
        "title": "Trampa de grasa en restaurantes: qué exige la norma chilena (DS 609) y cuándo limpiarla",
        "h1": "Trampa de grasa en cocinas comerciales: norma chilena, mantención y errores que cuestan caro",
        "category_label": "HORECA · Cumplimiento",
        "category_color": "orange",
        "image": f"{BASE}/images/camio-haciendo-servicio-en-la-calle.webp",
        "img_alt": "Trampa de grasa en cocina comercial siendo intervenida",
        "desc": "Qué dice el DS 609/1998 sobre grasas en alcantarillado, cómo dimensionar tu trampa y cuándo limpiarla para evitar multas e infracciones.",
        "lead": (
            "Si tienes restaurante, casino, cocina industrial o cafetería en Chile, "
            "la trampa de grasa no es un lujo: es una exigencia normativa. El "
            "DS 609/1998 del Ministerio de Obras Públicas regula los límites de "
            "grasas, aceites y sólidos que puedes descargar al alcantarillado. "
            "Te explicamos cómo cumplir sin sobre-pagar."
        ),
        "html": """
<h2>Qué dice la norma chilena</h2>
<p>El <a href="https://www.bcn.cl/leychile/navegar?idNorma=121486" target="_blank" rel="noopener nofollow">DS 609/1998 del Ministerio de Obras Públicas</a> establece los límites máximos para descargas de RILes (residuos industriales líquidos) al alcantarillado: aceites y grasas, sólidos suspendidos, DBO5, pH, entre otros. Lo fiscaliza la <a href="https://www.siss.gob.cl/" target="_blank" rel="noopener nofollow">SISS</a>. Para HORECA (Hoteles, Restaurantes, Catering), la trampa de grasa es la pieza obligatoria para no superar esos límites.</p>

<h2>Cómo funciona</h2>
<p>Es una caja (acero inox o polietileno) instalada lo más cerca posible del lavaplatos industrial. El agua entra, baja su velocidad, y por diferencia de densidad la grasa flota arriba mientras el agua clarificada sale por el sifón inferior hacia la red.</p>

<h2>Cuándo se debe limpiar</h2>
<p>La regla técnica internacional, también recomendada por proveedores como <a href="https://www.rentokil.com/cl/blog/innovacion/importancia-de-una-trampa-de-grasa-en-restaurantes-hoteles-y-casinos" target="_blank" rel="noopener nofollow">Rentokil Chile</a>, es vaciarla cuando la grasa o lodo ocupa el <strong>25% del volumen útil</strong>. En restaurantes con frituras o sushi de delivery 24/7, eso es:</p>
<ul>
  <li>Cocina pequeña (10-30 cubiertos): cada 30-60 días.</li>
  <li>Cocina mediana (30-100 cubiertos): cada 15-30 días.</li>
  <li>Cocina industrial / casino: semanal a quincenal.</li>
</ul>

<h2>Errores que vemos seguido</h2>
<ol>
  <li><strong>Usar la trampa subdimensionada</strong> que vino “de fábrica”. Generalmente queda chica.</li>
  <li><strong>Vaciar con balde y tirar al WC.</strong> Va contra el DS 609; corres riesgo de sanción de la sanitaria.</li>
  <li><strong>Tratar de “derretir” la grasa con químicos cáusticos.</strong> No la elimina, la traslada al alcantarillado y vuelve a cuajar.</li>
  <li><strong>No tener registro de mantención</strong> firmado por empresa autorizada — clave si te fiscalizan.</li>
</ol>

<h2>Cómo dimensionar tu trampa de grasa</h2>
<p>Regla simple: el volumen útil debe ser equivalente al consumo de agua de tu cocina en 30 minutos peak. Para un restaurante chico es ~150 L; para uno mediano 300-500 L; para una cocina industrial 1.000+ L.</p>

<h2>Costo de no cumplir</h2>
<p>Más allá de la multa formal, los costos reales son:</p>
<ul>
  <li>Atasco interno con cierre temporal de la cocina.</li>
  <li>Daño a tu trampa por sobrecarga.</li>
  <li>Atascos en la matriz comunitaria (si estás en mall/edificio): el responsable termina pagando la reparación.</li>
</ul>

<div class="bg-blue-50 border-l-4 border-blue-500 p-5 my-8">
  <p class="font-bold text-blue-900 m-0 mb-1">Consejo</p>
  <p class="m-0 text-blue-800 text-sm">Pide siempre el certificado de retiro y disposición de los lodos de tu trampa. Es tu respaldo si la sanitaria fiscaliza.</p>
</div>
""",
        "faq": [
            ("¿Mi cafetería pequeña necesita trampa de grasa?", "Sí, si emites grasas y aceites al alcantarillado. La norma DS 609 aplica a toda fuente HORECA."),
            ("¿Puedo limpiar la trampa con mi propio personal?", "Para una pequeña, técnicamente sí, pero el residuo debe ser dispuesto por empresa autorizada. Lo más eficiente es contratar el servicio integral."),
            ("¿Cada cuánto debo cambiar la trampa?", "El cuerpo dura 10-15 años en acero inox. Lo que se cambia regularmente son sellos, deflectores y bandeja recolectora."),
        ],
        "sources": [
            ("DS 609/1998 MOP — Norma para descargas de RILes a alcantarillado (BCN).", "https://www.bcn.cl/leychile/navegar?idNorma=121486"),
            ("MINSAL — Reglamento Sanitario de los Alimentos (DS 977/96).", "https://www.minsal.cl/reglamento-sanitario-de-los-alimentos/"),
            ("Rentokil Chile — Importancia de las trampas de grasa en HORECA.", "https://www.rentokil.com/cl/blog/innovacion/importancia-de-una-trampa-de-grasa-en-restaurantes-hoteles-y-casinos"),
            ("Water UK — Fighting fatbergs (impacto de FOG en alcantarillado).", "https://www.water.org.uk/waste-water/fighting-fatbergs"),
        ],
        "related": [
            ("/blog/destape-cocina-restaurante-sushi", "Caso real: destape de cocina en restaurante de sushi"),
            ("/blog/por-que-se-tapa-desague-cocina", "Por qué se tapa el desagüe de la cocina"),
            ("/servicios/destape-desagues-cocina-y-grasa", "Servicio de destape de cocinas y trampas de grasa"),
        ],
    },

    # 6) Certificado de retiro y DS 4/2009
    "certificado-retiro-lodos-fosa-chile-ds-4-2009": {
        "title": "Certificado de retiro de lodos en Chile: qué es, qué exige el DS 4/2009 y por qué guardarlo",
        "h1": "Certificado de retiro de lodos: tu mejor seguro frente a la SEREMI (DS 4/2009)",
        "category_label": "Normativa Chile",
        "category_color": "blue",
        "image": f"{BASE}/images/camion-haciendo-destape-en-zona-rural.webp",
        "img_alt": "Camión limpia fosas con certificado de retiro de lodos en Chile",
        "desc": "El DS 4/2009 regula los lodos de plantas y fosas. Te explicamos qué debe decir el certificado de retiro y por qué guardarlo 5 años.",
        "lead": (
            "Cada vez que limpiamos una fosa séptica o trampa de grasa entregamos un "
            "certificado de retiro y disposición. No es un trámite cosmético: es la "
            "evidencia que protege al dueño del inmueble frente a una eventual "
            "fiscalización sanitaria. El marco legal chileno es el DS 4/2009 de "
            "MINSEGPRES."
        ),
        "html": """
<h2>Qué es el DS 4/2009</h2>
<p>El <a href="https://www.bcn.cl/leychile/N?i=1007456" target="_blank" rel="noopener nofollow">DS 4/2009 del Ministerio Secretaría General de la Presidencia (MINSEGPRES)</a> es el “Reglamento para el manejo de lodos generados en plantas de tratamiento de aguas servidas”. Establece la clasificación sanitaria, los requisitos mínimos para almacenamiento, transporte y disposición final, y obliga a las plantas a tener un proyecto aprobado por la autoridad sanitaria.</p>
<p>Para los privados (dueños de fosas, condominios, restaurantes), el reglamento aplica indirectamente: <strong>los lodos retirados de tu fosa terminan en una de estas plantas</strong>, y la cadena de custodia queda registrada vía el Sistema Nacional de Declaración de Residuos (SINADER).</p>

<h2>Qué debe decir un certificado bien hecho</h2>
<ul>
  <li>Razón social y RUT de la empresa con resolución sanitaria.</li>
  <li>Patente del camión y placa.</li>
  <li>Nombre del operador y firma.</li>
  <li>Dirección donde se realizó el retiro.</li>
  <li>Volumen retirado en m³ o litros.</li>
  <li>Fecha y hora del servicio.</li>
  <li>Planta de disposición de destino y código SINADER.</li>
  <li>Tipo de lodo (Clase A, Clase B u otro).</li>
</ul>

<h2>Por qué guardarlo 5 años</h2>
<p>La SEREMI de Salud puede fiscalizar a inmuebles con sistemas particulares en cualquier momento. Si no tienes el certificado, la presunción es que descargaste donde no debías. La multa puede ir desde UTM modestas hasta clausura del sistema y obligación de reemplazarlo (varios millones).</p>

<h2>El típico “lo botamos en cualquier parte”</h2>
<p>Los camioneros informales sin resolución descargan en quebradas, predios baldíos o cauces. Eso convierte al dueño del inmueble en cómplice involuntario. La diferencia de precio entre un servicio formal y uno “al lote” suele ser $30.000 a $60.000 — el ahorro no compensa la responsabilidad legal.</p>

<h2>Cadena de custodia: cómo funciona en práctica</h2>
<ol>
  <li>El camión llega y vacía tu fosa o trampa.</li>
  <li>El operador firma certificado en duplicado: una copia para ti, otra para él.</li>
  <li>El camión va directo a planta autorizada.</li>
  <li>La planta emite ticket de recepción del volumen.</li>
  <li>La empresa declara el movimiento al SINADER (depende del tipo de generador).</li>
</ol>

<h2>Cómo verificar que tu proveedor es formal</h2>
<ul>
  <li>Pide el N° de resolución sanitaria de transporte de RILes/lodos.</li>
  <li>Pide la patente del camión.</li>
  <li>Pide el destino — debe ser una planta nombrada (Mapocho, La Farfana, Trebal, El Trebal, Hospital, etc., según comuna).</li>
  <li>Confirma que entrega boleta o factura.</li>
</ul>

<div class="bg-blue-50 border-l-4 border-blue-500 p-5 my-8">
  <p class="font-bold text-blue-900 m-0 mb-1">Regla práctica</p>
  <p class="m-0 text-blue-800 text-sm">Si la empresa cobra muy bajo y no quiere darte certificado: te está vendiendo un problema legal a futuro, no un ahorro.</p>
</div>
""",
        "faq": [
            ("¿Y si perdí el certificado anterior?", "Una empresa formal mantiene registros por al menos 5 años. Pídelo a tu proveedor por correo electrónico — debería poder reemitirlo."),
            ("¿Necesito certificado para una trampa de grasa?", "Sí. La grasa es un residuo regulado y debe ir a planta autorizada. El certificado es el respaldo frente a la SISS."),
            ("¿La SEREMI fiscaliza casas particulares?", "Sí, especialmente en sectores rurales y parcelas con fosa propia. Cada vez es más frecuente, sobre todo en denuncias por olores."),
        ],
        "sources": [
            ("DS 4/2009 MINSEGPRES — Reglamento para el Manejo de Lodos (BCN).", "https://www.bcn.cl/leychile/N?i=1007456"),
            ("DS 236/1926 — Reglamento General de Alcantarillados Particulares.", "https://www.bcn.cl/leychile/Navegar?idNorma=171085"),
            ("Superintendencia de Servicios Sanitarios (SISS).", "https://www.siss.gob.cl/"),
            ("RETC / SINADER — Sistema único para reportar manejo de lodos.", "https://retc.mma.gob.cl/sinader-sera-unico-medio-oficial-para-reportar-el-manejo-de-lodos-de-las-plantas-de-tratamiento-de-aguas-servidas/"),
        ],
        "related": [
            ("/blog/cuanto-cuesta-limpiar-fosa-septica-chile-2026", "Cuánto cuesta limpiar una fosa séptica en Chile 2026"),
            ("/blog/errores-pyme-contratan-destape-pirata", "Errores que cometen las pymes al contratar destape pirata"),
            ("/blog/quimicos-fosa-septica-verdad-mentira-estafa", "Verdad y mentira de los químicos para fosa"),
        ],
    },

    # 7) Inspección con cámara CCTV y códigos PACP
    "inspeccion-camara-cctv-codigos-pacp-chile": {
        "title": "Inspección con cámara CCTV en alcantarillado: códigos PACP y cómo leer un informe técnico",
        "h1": "Inspección con cámara CCTV: cómo se hace, qué significan los códigos PACP y cómo leer el informe",
        "category_label": "Diagnóstico técnico",
        "category_color": "indigo",
        "image": f"{BASE}/images/limpieza-con-camara.webp",
        "img_alt": "Cámara CCTV inspeccionando cañería de alcantarillado",
        "desc": "Cómo se hace una inspección CCTV de alcantarillado, qué códigos NASSCO PACP usamos y cómo leer un informe técnico bien hecho.",
        "lead": (
            "Pasar la cámara a una cañería no es solo grabar video. Una inspección "
            "técnica seria sigue un estándar — el NASSCO PACP — que asigna códigos "
            "y grados de severidad a cada defecto. Eso te permite tomar decisiones "
            "con datos, no por sensación."
        ),
        "html": """
<h2>¿Qué es PACP?</h2>
<p>El <a href="https://www.nassco.org/trenchless-technology/assessment/" target="_blank" rel="noopener nofollow">PACP (Pipeline Assessment Certification Program) de NASSCO</a> es el estándar norteamericano para inspecciones CCTV de alcantarillado. Existe desde 2001 y es el lenguaje común que usan municipios, sanitarias y consultoras serias para reportar el estado de una red.</p>
<p>Cada defecto se codifica con letras y se le asigna una severidad de 1 (leve) a 5 (crítico). Algunos códigos comunes:</p>

<div class="overflow-x-auto">
  <table class="w-full text-left border-collapse my-6">
    <thead><tr class="bg-slate-100"><th class="p-3 border">Código</th><th class="p-3 border">Defecto</th><th class="p-3 border">Acción típica</th></tr></thead>
    <tbody>
      <tr><td class="p-3 border">CL</td><td class="p-3 border">Crack longitudinal</td><td class="p-3 border">Vigilancia o sleeve</td></tr>
      <tr><td class="p-3 border">FM</td><td class="p-3 border">Fracturas múltiples</td><td class="p-3 border">Reparación urgente</td></tr>
      <tr><td class="p-3 border">HSV</td><td class="p-3 border">Hueco con suelo visible</td><td class="p-3 border">Reparación inmediata</td></tr>
      <tr><td class="p-3 border">RFC</td><td class="p-3 border">Raíces finas continuas</td><td class="p-3 border">Hidrojet + tratamiento</td></tr>
      <tr><td class="p-3 border">DSF</td><td class="p-3 border">Sedimento fino</td><td class="p-3 border">Limpieza con hidrojet</td></tr>
    </tbody>
  </table>
</div>

<h2>Cómo se hace una inspección bien hecha</h2>
<ol>
  <li><strong>Limpieza previa</strong> con hidrojet (si hay sedimento, no se ve nada).</li>
  <li><strong>Cámara axial o rotatoria</strong> según diámetro (Ridgid SeeSnake, Envirosight, IBAK, etc.).</li>
  <li><strong>Grabación con metraje</strong> e identificación de cada defecto en distancia y orientación horaria.</li>
  <li><strong>Informe escrito</strong> con códigos PACP, fotos y recomendaciones priorizadas.</li>
  <li><strong>Plano sintético</strong> con la ubicación de los hallazgos.</li>
</ol>

<h2>Cuándo conviene pedirla</h2>
<ul>
  <li>Antes de comprar una propiedad rural o con sistema antiguo.</li>
  <li>Después de una inundación o atasco repetitivo.</li>
  <li>En condominios, antes de cambiar matrices.</li>
  <li>Para definir si hay raíces, fracturas o hundimientos antes de cotizar reparación.</li>
  <li>Para resolver disputas entre vecinos: el video es prueba.</li>
</ul>

<h2>Errores típicos al “pasar cámara” sin método</h2>
<ol>
  <li>Saltarse la limpieza previa: la cámara solo ve barro.</li>
  <li>No medir el avance de cable: no sabes <em>dónde</em> está el problema.</li>
  <li>No entregar informe escrito: solo video.</li>
  <li>No clasificar por severidad: la decisión queda en el aire.</li>
</ol>

<h2>Qué deberías recibir tú</h2>
<ul>
  <li>Video completo (USB, link nube o WhatsApp).</li>
  <li>Informe en PDF con códigos y severidad.</li>
  <li>Fotos extraídas de los principales defectos.</li>
  <li>Recomendación priorizada (qué hacer ahora vs. qué vigilar).</li>
  <li>Cotización separada para cualquier reparación.</li>
</ul>

<div class="bg-blue-50 border-l-4 border-blue-500 p-5 my-8">
  <p class="font-bold text-blue-900 m-0 mb-1">Consejo de compra</p>
  <p class="m-0 text-blue-800 text-sm">Si vas a comprar parcela: una inspección con cámara cuesta ~$80.000-$150.000 y te puede ahorrar millones en reparaciones que no se ven a simple vista.</p>
</div>
""",
        "faq": [
            ("¿Sirve para fosas o solo para cañerías?", "Para cañerías y matrices. Para el interior de la fosa se usa cámara con foco propio o se baja con varilla con cámara. La inspección visual de fosa es complementaria al CCTV."),
            ("¿Cuánto demora una inspección típica?", "Entre 30 minutos (un tramo doméstico) y 2-3 horas (matriz completa de condominio o parcela)."),
        ],
        "sources": [
            ("NASSCO — Pipeline Assessment Certification Program (PACP).", "https://www.nassco.org/trenchless-technology/assessment/"),
            ("DS 236/1926 — Reglamento General de Alcantarillados Particulares.", "https://www.bcn.cl/leychile/Navegar?idNorma=171085"),
            ("Superintendencia de Servicios Sanitarios (SISS).", "https://www.siss.gob.cl/"),
        ],
        "related": [
            ("/blog/inspeccion-camara-canerias-cuando-conviene-cuanto-cuesta", "Cuándo conviene la inspección con cámara"),
            ("/blog/raices-en-tuberias-detectar-eliminar-prevenir", "Raíces en tuberías"),
            ("/servicios/inspeccion-camara-alcantarillado", "Servicio de inspección con cámara"),
        ],
    },
}


# ------------------------------------------------------------------
# Plantilla HTML
# ------------------------------------------------------------------
COLOR_MAP = {
    "red": ("bg-red-100", "text-red-700"),
    "blue": ("bg-blue-100", "text-blue-700"),
    "amber": ("bg-amber-100", "text-amber-700"),
    "orange": ("bg-orange-100", "text-orange-700"),
    "indigo": ("bg-indigo-100", "text-indigo-700"),
    "green": ("bg-green-100", "text-green-700"),
    "purple": ("bg-purple-100", "text-purple-700"),
}


def render_template(slug: str, p: dict) -> str:
    bg, fg = COLOR_MAP.get(p["category_color"], COLOR_MAP["blue"])
    canonical = f"{BASE}/blog/{slug}"
    image = p.get("image", HERO_DEFAULT)

    # JSON-LD
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
            "headline": p["title"],
            "description": p["desc"],
            "datePublished": "2026-05-07",
            "dateModified": "2026-05-07",
            "author": {
                "@type": "Person",
                "name": AUTHOR_NAME,
                "jobTitle": "Especialista en saneamiento",
                "url": AUTHOR_PAGE,
                "image": AUTHOR_IMG,
                "sameAs": [AUTHOR_LINKEDIN],
                "worksFor": {"@id": f"{BASE}/#business"},
            },
            "publisher": {"@id": f"{BASE}/#business"},
            "mainEntityOfPage": canonical,
            "image": image,
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
                for q, a in p["faq"]
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE}/blog/"},
                {"@type": "ListItem", "position": 3, "name": p["title"], "item": canonical},
            ],
        },
    ]

    sources_html = "\n              ".join(
        f'<li><a href="{url}" target="_blank" rel="noopener nofollow" '
        f'class="text-blue-700 hover:underline">{title}</a></li>'
        for title, url in p["sources"]
    )
    related_html = "\n        ".join(
        f'<a href="{href}" class="block p-5 bg-white rounded-xl border border-slate-200 '
        f'hover:border-blue-500 hover:shadow-md transition">'
        f'<span class="text-xs uppercase tracking-wide text-blue-600 font-bold">Sigue leyendo</span>'
        f'<h3 class="mt-2 font-bold text-slate-800">{label}</h3></a>'
        for href, label in p["related"]
    )

    return f"""<!DOCTYPE html>
<html lang="es" class="scroll-smooth">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{p["title"]}</title>
    <meta name="description" content="{p["desc"]}">
    <link rel="canonical" href="{canonical}">
    <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
    <link rel="preconnect" href="https://www.googletagmanager.com">
    <link rel="dns-prefetch" href="https://cdnjs.cloudflare.com">
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
        .prose blockquote {{ font-style: italic; }}
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

    <meta property="og:title" content="{p["title"]}">
    <meta property="og:description" content="{p["desc"]}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{image}">
    <meta property="og:locale" content="es_CL">
    <meta property="og:site_name" content="Destape Rápido">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{p["title"]}">
    <meta name="twitter:description" content="{p["desc"]}">
    <meta name="twitter:image" content="{image}">

    <script type="application/ld+json">
{json.dumps(jsonld, ensure_ascii=False, indent=2)}
    </script>

    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start': new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-PG2RQNCD');</script>
    <!-- End Google Tag Manager -->
</head>

<body class="bg-white text-slate-700 antialiased">
    <a href="#main-content" id="skip-to-content-link" class="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-[100] focus:bg-brand-600 focus:text-white focus:px-4 focus:py-2 focus:rounded-lg focus:shadow-lg focus:font-bold">Saltar al contenido</a>

    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PG2RQNCD" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

    <nav class="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-50">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <a href="/" class="flex items-center gap-1">
                    <span class="block font-extrabold text-slate-900 text-lg">DESTAPE<span class="text-brand-600">RÁPIDO</span></span>
                </a>
                <div class="flex items-center gap-4">
                    <a href="/blog" class="text-slate-600 font-semibold hover:text-brand-600">Volver al Blog</a>
                    <a href="tel:{PHONE_E164}" class="bg-brand-600 text-white px-4 py-2 rounded-full font-bold hover:bg-brand-700 transition">Llamar</a>
                </div>
            </div>
        </div>
    </nav>

    <main id="main-content">
    <article class="max-w-3xl mx-auto px-4 py-12">
        <header class="mb-10 text-center">
            <div class="inline-block {bg} {fg} text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide mb-4">{p["category_label"]}</div>
            <h1 class="text-3xl md:text-5xl font-extrabold text-slate-900 mb-6 leading-tight">{p["h1"]}</h1>
            <div class="flex items-center justify-center gap-4 text-slate-500 text-sm">
                <span><i class="fa-regular fa-calendar mr-2" aria-hidden="true"></i>Publicado: Mayo 2026</span>
                <span><i class="fa-regular fa-user mr-2" aria-hidden="true"></i>{AUTHOR_NAME}</span>
            </div>
        </header>

        <div class="rounded-2xl overflow-hidden shadow-xl mb-12">
            <img src="{image}" alt="{p["img_alt"]}" class="w-full h-64 object-cover" width="1200" height="630" loading="eager" fetchpriority="high" decoding="async">
        </div>

        <div class="prose prose-lg prose-slate mx-auto">
            <p class="lead text-xl text-slate-700 font-medium mb-8">{p["lead"]}</p>
{p["html"]}
        </div>

        <!-- author-bio-block -->
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

        <!-- sources-block -->
        <section aria-label="Fuentes y referencias" class="mt-10 mb-2 bg-white border border-slate-200 rounded-2xl p-6">
            <h2 class="text-xl font-extrabold text-slate-900 m-0 mb-3 flex items-center gap-2">
              <i class="fa-solid fa-book-bookmark text-brand-600" aria-hidden="true"></i>
              Fuentes y referencias
            </h2>
            <p class="text-sm text-slate-600 m-0 mb-4">
              Donde aplicó usamos data oficial chilena (BCN, SISS, MINSAL) y referencias técnicas internacionales. Lo demás viene de nuestra propia experiencia en terreno en la Región Metropolitana.
            </p>
            <ul class="list-disc pl-6 space-y-2 text-sm text-slate-700">
              {sources_html}
            </ul>
        </section>

        <div class="bg-brand-50 rounded-2xl p-8 mt-12 border border-brand-100 text-center">
            <h3 class="text-2xl font-bold text-brand-900 mb-4">¿Necesitas ayuda profesional?</h3>
            <p class="text-brand-700 mb-6">Atendemos toda la Región Metropolitana 24/7. Cotizamos por WhatsApp en menos de 10 minutos.</p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <a href="tel:{PHONE_E164}" class="bg-brand-600 hover:bg-brand-700 text-white font-bold py-3 px-8 rounded-xl shadow-lg transition"><i class="fa-solid fa-phone mr-2" aria-hidden="true"></i> Llama al {PHONE_DISPLAY}</a>
                <a href="https://wa.me/{PHONE_E164.lstrip("+")}" class="bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-8 rounded-xl shadow-lg transition"><i class="fa-brands fa-whatsapp mr-2" aria-hidden="true"></i> WhatsApp</a>
            </div>
        </div>
    </article>

    <section aria-labelledby="related-articles-title" class="bg-slate-50 py-12 px-4 border-t border-slate-200">
      <div class="max-w-5xl mx-auto">
        <h2 id="related-articles-title" class="text-2xl font-bold text-slate-800 mb-6">Artículos relacionados</h2>
        <div class="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
        {related_html}
        </div>
        <p class="mt-6 text-sm text-slate-600">
          ¿Necesitas el servicio ahora? <a href="/contacto" class="text-blue-600 hover:underline font-semibold">Cotiza por WhatsApp</a> o revisa nuestras <a href="/servicios/" class="text-blue-600 hover:underline font-semibold">páginas de servicio</a>.
        </p>
      </div>
    </section>
    </main>

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

    <a href="https://wa.me/{PHONE_E164.lstrip("+")}" class="wa-floating-btn" aria-label="WhatsApp">
        <i class="fa-brands fa-whatsapp" style="font-size: 32px;" aria-hidden="true"></i>
    </a>

    <script>
        document.getElementById('year').textContent = new Date().getFullYear();
    </script>
    <script src="/js/conversion.js" defer></script>
</body>

</html>
"""


def main() -> None:
    for slug, p in POSTS.items():
        path = BLOG / f"{slug}.html"
        path.write_text(render_template(slug, p), encoding="utf-8")
        print(f"  - {slug}.html ({len(p['html'])} chars)")


if __name__ == "__main__":
    main()
