# Propuesta de enlazado interno — julio 2026

**Objetivo:** des-orfanar las páginas del blog que Google no puede descubrir navegando el
sitio (0 enlaces entrantes). Cada huérfana recibe 1 enlace primario + 1 refuerzo desde
páginas con equity, con **anchor = query objetivo** (nunca «clic aquí»).

**Evidencia:** crawl de solo-lectura del sitio vivo, 2026-07-05
(`scripts/crawl-sitio.py --site https://www.destaperapido.cl`): 110 páginas revisadas,
109 en sitemap, 0 rotas. Re-correr ese comando (con `--out crawl.json`) reproduce el
reporte completo.

> ⚠️ **Nota técnica del crawl:** correrlo contra `https://destaperapido.cl` (apex) da falsos
> «0 huérfanas»: el apex responde **308 → www** y el Python 3.9 del venv no sigue 308.
> Siempre crawlear con `--site https://www.destaperapido.cl`.

## Resultado: son 5 huérfanas del blog (no 3)

La cola hablaba de 3; el crawl confirmó **5** (idéntico en el clon y en el sitio vivo):

| # | Página huérfana | Query objetivo |
|---|---|---|
| 1 | `/blog/cobertura-saneamiento-rm-2026-comunas` | cobertura saneamiento Región Metropolitana comunas |
| 2 | `/blog/como-digitalizamos-solicitudes-destape-en-15-minutos` | solicitudes de destape respuesta 15 minutos |
| 3 | `/blog/comparativa-hidrojet-vs-vactor-vs-camion-chico` | hidrojet vs vactor vs camión chico |
| 4 | `/blog/empresas-saneamiento-certificadas-seremi-chile-verificar` | empresas de saneamiento certificadas SEREMI verificar |
| 5 | `/blog/top-empresas-hidrojet-rm-2026-como-comparar` | comparar empresas de hidrojet RM |

**Causa raíz:** la grilla estática de `public/blog/index.html` lista 28 posts de 35; estos
5 (más `guia-comprador-destapes-b2b-2026`, que se salva porque `empresas.html` lo enlaza)
quedaron fuera y ninguna otra página los menciona.

**Convención de este sitio:** `cleanUrls: true` en `vercel.json` → los `href` van **sin
`.html`** (`/blog/slug`). Estilo de enlace dentro de artículos:
`<a href="/blog/slug" class="text-blue-600 hover:underline">anchor</a>`.

---

## Arreglo 0 (estructural): completar la grilla de `blog/index.html`

Agregar a la grilla estática de `public/blog/index.html` las tarjetas de los 5 posts
huérfanos (mismo markup que las 28 tarjetas existentes). Esto solo ya los des-orfana;
los enlaces contextuales de abajo son los que pasan equity y relevancia de verdad.

---

## 1 · `/blog/cobertura-saneamiento-rm-2026-comunas`

- **Primario — desde `public/cobertura.html`** (el hub de cobertura, afinidad total).
  **Lugar:** párrafo intro de la sección «Nuestras Zonas de Cobertura» (~línea 1065,
  el `<p class="text-slate-500">Desplegamos nuestros equipos…`). Añadir al final del párrafo:

  > … tiempos de respuesta cortos. Revisa el detalle en nuestra guía de
  > `<a href="/blog/cobertura-saneamiento-rm-2026-comunas">cobertura de saneamiento en la Región Metropolitana: las 30+ comunas que atendemos</a>`,
  > con tiempos de respuesta por zona.

- **Refuerzo — desde `public/zonas/rural/index.html`**, sección «Rutas Diarias en tu
  Sector» (~línea 886): frase al cierre del párrafo de esa sección con anchor
  «comunas con cobertura de saneamiento en la RM».

## 2 · `/blog/como-digitalizamos-solicitudes-destape-en-15-minutos`

- **Primario — desde `public/tecnologia.html`** (la página cuenta la misma historia).
  **Lugar:** párrafo del hero (~línea 358, «No somos un destape pirata con un teléfono…»).
  Añadir al final:

  > Aquí contamos el detrás de escena:
  > `<a href="/blog/como-digitalizamos-solicitudes-destape-en-15-minutos">cómo digitalizamos las solicitudes de destape para responder en 15 minutos</a>`.

- **Refuerzo:** tarjeta en la grilla de `blog/index.html` (Arreglo 0). Opcional extra:
  `por-que-elegirnos.html` donde se hable de rapidez de respuesta, mismo anchor.

## 3 · `/blog/comparativa-hidrojet-vs-vactor-vs-camion-chico`

- **Primario — desde `public/servicios/camion-alta-presion-hidrojet.html`**.
  **Lugar:** sección «Capacidad para Grandes Desafíos», tras el párrafo «Nuestros equipos
  de hidrojet están diseñados…» (~líneas 1260-1263). Añadir:

  > ¿No sabes qué equipo corresponde a tu caso? Mira la comparativa
  > `<a href="/blog/comparativa-hidrojet-vs-vactor-vs-camion-chico">hidrojet vs vactor vs camión chico: qué necesita tu propiedad</a>`.

- **Refuerzo — desde `public/blog/hidrojet-vs-destape-mecanico-cual-elegir.html`**,
  sección «Cuándo conviene cada uno» (~línea 409-410): cerrar la sección con
  «Si dudas entre equipos de succión y presión, revisa
  `<a href="/blog/comparativa-hidrojet-vs-vactor-vs-camion-chico">hidrojet, vactor o camión chico</a>`.»
  Y sumar tarjeta en su bloque «Artículos relacionados».

## 4 · `/blog/empresas-saneamiento-certificadas-seremi-chile-verificar`

- **Primario — desde `public/blog/mejor-empresa-limpia-fosas-santiago-2026.html`**.
  **Lugar:** criterio «1. Resolución sanitaria SEREMI vigente» (~línea 473). Al final del
  párrafo del criterio:

  > Guía paso a paso:
  > `<a href="/blog/empresas-saneamiento-certificadas-seremi-chile-verificar">cómo verificar una empresa de saneamiento certificada SEREMI</a>`.

- **Refuerzo — desde `public/blog/errores-pyme-contratan-destape-pirata.html`**, sección
  «Cómo verificar que una empresa es formal» (~línea 132), ítem 3 del listado («Pídele
  resolución sanitaria SEREMI en PDF»): enlazar ahí mismo con anchor
  «verificar la resolución sanitaria SEREMI». Opcional extra: `empresas.html`, tarjeta
  «Certificado SEREMI de disposición» (~línea 585).

## 5 · `/blog/top-empresas-hidrojet-rm-2026-como-comparar`

- **Primario — desde `public/servicios/camion-alta-presion-hidrojet.html`**.
  **Lugar:** sección «¿Por qué elegir Hidrojet?» (~línea 1220s) o en la FAQ de hidrojet;
  una frase tipo:

  > Antes de contratar, revisa los criterios técnicos para
  > `<a href="/blog/top-empresas-hidrojet-rm-2026-como-comparar">comparar empresas de hidrojet en la RM</a>`
  > (PSI, caudal, alcance, certificación).

- **Refuerzo — desde `public/blog/mejor-empresa-limpia-fosas-santiago-2026.html`**,
  intro de «Comparativa auto-aplicada» (~línea 529): «la misma lógica aplica al
  `<a href="/blog/top-empresas-hidrojet-rm-2026-como-comparar">comparar empresas de hidrojet en la RM</a>`».

---

## Hallazgos extra del crawl (fuera de esta propuesta, para encolar)

- **6 casos reales huérfanos** (`/casos-reales/*`): la página índice existe y varias
  páginas enlazan a `/casos-reales/`, pero nadie enlaza los casos individuales.
- **`/nosotros`, `/testimonios`, `/ruta-buin` huérfanas:** el nav estático no las incluye.
- **4 landings huérfanas** (`/landing/*`): probablemente intencional (destinos de Ads);
  decidir con Alejandro si se dejan así (y quizá sacarlas del sitemap para no confundir).
- 23 páginas «poco enlazadas» (≤1 enlace entrante) en el reporte del crawl.

## Ejecución (constructor o sesión)

1. Editar los archivos de `public/` listados (enlaces sin `.html`, kebab-case intacto).
2. **Publicar:** este clon despliega por **Vercel** → NO está graduado; desatendido queda
   **PROPUESTO** con el comando exacto listo. En sesión: OK de Alejandro y deploy.
3. Tras publicar: `python3 scripts/indexnow-ping.py <URLs de las 5 huérfanas + las páginas
   editadas>` desde el clon si hay `INDEXNOW_KEY` en su `scripts/.env.local`.
4. **Verificar:** re-crawl `--site https://www.destaperapido.cl` → las 5 deben salir de
   `huerfanas` (in_links ≥ 2). En 2-3 semanas, revisar impresiones/posición en GSC.
