# Auditoría funcional — dixdybot-prototipo.html (post 18 iteraciones)

Fecha: 2026-07-23 · Método: lectura completa del HTML+JS + verificación en navegador
(Playwright, justificado: layout y flujos de estado). Los hallazgos marcados **[verificado]**
se reprodujeron en vivo; el resto se confirmó por lectura de código.

Archivo auditado: `/private/tmp/claude-501/-Users-alejandroriveracarrasco-SaSS-DIXDY-clientes-destaperapido/5acfd0ef-e8b4-49b2-965d-26a7a76d1c5b/scratchpad/dixdybot-prototipo.html`

---

## Lista priorizada (20 arreglos concretos)

### 1. Hoy, Módulos y Diseño NO tienen scroll — contenido inalcanzable [verificado]
- **Elemento:** `#v-hoy`, `#v-modulos`, `#v-diseno` (secciones `display:block`) + `.contenido { flex:1; overflow-y:auto }`.
- **Problema:** las tres vistas son block, así que `flex:1` no aplica y `.contenido` crece a su altura natural (medido: scrollHeight == clientHeight, 1431px de contenido en una sección de 1272px). Con `body { overflow:hidden }` no hay ningún ancestro que scrollee: en un laptop normal (~800px) la mitad de Módulos y Diseño queda cortada sin forma de verla. Es lo primero que mata el recorrido.
- **Fix:** agregar la clase `vcol` a las tres secciones (`<section class="vista vcol" id="v-modulos">` etc.) — la regla `.vista.vcol.activa { display:flex; flex-direction:column }` ya existe (línea 74). Tres palabras, cero CSS nuevo.

### 2. Falta `<meta charset="utf-8">` — mojibake total fuera de condiciones ideales [verificado]
- **Elemento:** cabecera del archivo (línea 1 es `<title>`).
- **Problema:** servido sin header de charset (p.ej. `python3 -m http.server`, o algunos hostings/visores) TODO el texto se rompe: título "dixdybot â€”", "SofÃ­a", emojis ilegibles. El prototipo viaja como archivo suelto; es ruleta rusa.
- **Fix:** `<meta charset="utf-8">` como primera línea.

### 3. Aprobar Ranco es re-ejecutable y rompe los contadores de Hoy [verificado]
- **Elemento:** `aprobarRanco()` — llamable desde el botón de Hoy Y desde `#btn-accion-chat` del chat (que nunca cambia de estado).
- **Problema:** la segunda llamada duplica la fila en "Resueltas hoy" (quedan 2 filas idénticas), `nRes` llega a 2 y el badge de Hoy se vacía aunque la pausa de Carolina siga pendiente (verificado: cnt-hoy = ""). El guard `correoEnviado` solo protege los mensajes, no `resolverDecision`.
- **Fix:** mover `resolverDecision(...)` dentro del `if (!CHATS.ranco.correoEnviado)`, y tras aprobar cambiar `#btn-accion-chat` a "Cotización enviada ✓" deshabilitado (y `CHATS.ranco.accion`).

### 4. El borrador se publica dos veces y se puede "descartar" ya publicado [verificado]
- **Elemento:** `#pop-borrador`, `publicarBorrador()`, `descartarBorrador()`, card `#card-diff` de Hoy.
- **Problema:** el pop nunca cambia de estado. Publicar 2 veces duplica la entrada del historial del camino (verificado: 2× "publicado: +10%"). Peor: Publicar y luego Descartar → toast "todo sigue como estaba" pero el precio quedó en $176.000 y el chip "publicado 10:58" desaparece. La card de Hoy sigue reabriendo el pop con botones vivos tras cualquiera de los dos caminos.
- **Fix:** estado `BORRADOR = 'pendiente'|'publicado'|'descartado'`; el pop renderiza según estado (publicado → solo "ver historial"; descartado → "restaurar"); actualizar/retirar `#card-diff` en ambos desenlaces.

### 5. Los flags `espera` nunca se limpian — "Dudas del bot" queda mintiendo [verificado]
- **Elemento:** `CHATS.ranco.espera` / `CHATS.carolina.espera`, sección "Dudas del bot — necesita tu respuesta" de `renderLista()`, chip y tarjeta de Carolina.
- **Problema:** tras aprobar Ranco Y resolver la pausa completa, ambos siguen bajo "Dudas del bot"; Carolina mantiene chip "tema en pausa", preview vieja en la lista (el `prev` nuevo no se pinta porque `pausaCerrar` no llama `renderLista`) y tarjeta del tablero "tema en pausa ⏸". El estado estrella del producto (la pausa) queda incoherente justo después de demostrarla.
- **Fix:** en `aprobarRanco` → `espera=false; noleido=false`; en `pausaCerrar`/`pausaAfinar` → `CHATS.carolina.espera=false`, chip → `['vivo','cotizando']`, actualizar la tarjeta del tablero, y `renderLista()` al final de ambas.

### 6. El filtro de agente es de mentira — todo lo bypasea [verificado]
- **Elemento:** `filtrarAgente()`, `renderLista()`, `enviarTu()`, `abrirChat()`.
- **Problema:** con "Destapes" seleccionado, escribir en el buscador repuebla la lista completa de Sofía (verificado); abrir cualquier chat igual. Y con la vista vacía de Destapes, el composer sigue activo: el mensaje se fue a Constructora Ranco sin que se vea (verificado — el peor caso: escribir al chat equivocado).
- **Fix:** variable global `agenteFiltro` que `renderLista()` respete; `filtrarAgente` solo setea y llama `renderLista`; `enviarTu` retorna si `#hilo` está vacío o el filtro no tiene chats.

### 7. "Ver" de Ranco en Hoy aterriza en el tablero, no en el chat [verificado]
- **Elemento:** `onclick="ir('chats');abrirChat('ranco')"` (decisión de Hoy) vs. el modo tablero persistente de `vistaChats`.
- **Problema:** si Chats quedó en Tablero, "Ver" muestra el tablero con el hilo renderizado invisible debajo (verificado: board display:flex). Orden de ejecución clásico del recorrido: mirar tablero → volver a Hoy → "Ver".
- **Fix:** que `abrirChat()` llame `vistaChats('lista')` al inicio (cubre también las tarjetas y cualquier caller futuro).

### 8. La nota "Enseñar por mensaje" muere para siempre al cambiar de chat [verificado]
- **Elemento:** `NOTAS[2]` anclada a `.hilo-head` + guard `if (notasOn && !document.querySelector('.nb'))` en `toggleNotas()`.
- **Problema:** `abrirChat` hace `hilo-head.innerHTML = ...` y borra el badge; re-togglear Notas no lo recrea porque quedan otros `.nb` vivos (verificado). En el recorrido de cierre las notas SON la guía del dueño.
- **Fix:** anclarla a `.composer` (estable) — o en `toggleNotas()` borrar todos los `.nb` y regenerarlos siempre al encender.

### 9. Números del tablero y de Hoy no cuadran entre sí ni con las fichas
- **Elemento:** columna "Cotizando 3 · $530mil"; tarjeta "Agrícola El Monte $230"; hero "$450mil en juego hoy".
- **Problema:** El Monte son 2 baños × $200.000 = $400mil según su propia ficha y su propio chat — la tarjeta dice $230. El total $530 no sale de ninguna combinación ($200+$230=430; con Carolina ~$1M tampoco). Y el hero $450mil no se reconstruye desde ningún dato visible (la nota de Hoy ya exige "declarar de qué módulos sale").
- **Fix:** tarjeta El Monte → $400; total → "2 · $600mil + 1 en pausa (~$1M)" (o computarlo de DATA); hero → cifra derivada y explicable (p.ej. cotizaciones activas del día) con tooltip de composición.

### 10. La tarjeta "Peñalolén" del tablero ES el chat de Pía, pero no lo abre
- **Elemento:** columna Cobrado, `<div class="tarjk" onclick="toast('Marcado por el repartidor…')">Peñalolén $160</div>` vs `CHATS.pia` (Peñalolén, cerrado · cobrado, $160).
- **Problema:** el dato existe de punta a punta pero el click da un toast; además la tarjeta dice "vie · transferencia" y el chat de Pía dice retiro "lunes". Rompe la promesa "tablero = mismos chats, otra vista".
- **Fix:** `onclick="vistaChats('lista');abrirChat('pia')"` + unificar el día; el toast del repartidor puede vivir en el punto de estado.

### 11. Ranco: la ficha se contradice con la decisión y no avanza al aprobar
- **Elemento:** decisión "confirmó 30+1 · $2.480.000 neto" vs ficha `['Accesible ×1','esperando tu precio'] · ['Estado','lista para tu OK']`.
- **Problema:** si el accesible no tiene precio, el total no puede ser $2.480.000 (30×80k = $2.400.000). Y tras aprobar, la ficha sigue diciendo "lista para tu OK".
- **Fix:** accesible "$80.000" desde el inicio, y en `aprobarRanco` actualizar `CHATS.ranco.ficha` → Estado "enviada a obras@ranco.cl" + re-render si es el chat activo.

### 12. "7 chats" en Hoy y sidebar, pero la lista tiene 6
- **Elemento:** hero de Hoy `7 chats`, sidebar `Chats · 7`, `ORDEN` (6 ids).
- **Problema:** el dueño va a contar. 6 ≠ 7 (la "Derivación 7 hoy" de Agentes también cuelga de ese 7).
- **Fix:** bajar ambos a 6, o sumar un 7º chat corto (mejor: uno de Destapes, que además le daría contenido real al filtro del hallazgo 6).

### 13. Crear el camino desde la pausa no mueve ningún contador [verificado]
- **Elemento:** `pausaAfinar()` vs sidebar "Caminos · 46", tab "Sofía · 34", grupo "Zonas lejanas · 5".
- **Problema:** nace el camino (momento mágico del demo) y los tres números quedan congelados (verificado).
- **Fix:** en `pausaAfinar` incrementar los tres → 47 / 35 / 6. Tres líneas que refuerzan la magia.

### 14. Los dormidos NO están en el buscador, aunque el panel lo promete [verificado]
- **Elemento:** `renderLista()` (solo busca en `CHATS`) vs el texto del pie de dormidos: "siguen en el buscador".
- **Problema:** buscar "marcela" → «Nada con "marcela"» (verificado). Promesa visible incumplida en la misma pantalla. Extra: el haystack incluye HTML crudo de la ficha — buscar "span" matchea un chat (verificado).
- **Fix:** incluir `DORMIDOS` en la búsqueda (pintados con opacity .55 bajo su sección) y strip de tags antes de comparar.

### 15. El hilo no scrollea al fondo al abrir un chat ni al llegar mensajes
- **Elemento:** `abrirChat()` (sin scroll; solo `enviarTu` lo hace), mensajes nuevos de `aprobarRanco`/`pausaCerrar`.
- **Problema:** al abrir Ranco se ve el mensaje más viejo; tras aprobar, la tarjeta de correo llega fuera de pantalla.
- **Fix:** última línea de `abrirChat`: `const h=document.getElementById('hilo'); h.scrollTop=h.scrollHeight;`.

### 16. Los flotantes no cierran con Escape ni mueven el foco
- **Elemento:** `pop()` / `cerrarPop()` — no hay ningún `addEventListener` en todo el archivo.
- **Problema:** única salida: el ✕ chico o navegar. En un recorrido con 10+ popups se siente tosco; con teclado es una trampa.
- **Fix:** `document.addEventListener('keydown', e => { if (e.key==='Escape') cerrarPop(); })` + en `pop()` enfocar el botón `.cerrar`. Dos líneas.

### 17. El 💡 de enseñar es invisible para teclado y tablet + aria perdida
- **Elemento:** `.b-ens` (solo `display:flex` con `:hover` del wrapper); input de la pausa dinámica.
- **Problema:** sin mouse no existe la interacción estrella de "enseñar por mensaje". Y `pausaHTML()` perdió el `aria-label="Respuesta"` que el HTML estático sí tenía.
- **Fix:** burbujas bot con `tabindex="0"` + regla `.bwrap.der:focus-within .b-ens { display:flex }`; en pantalla táctil mostrarlo siempre con opacidad baja. Restaurar `aria-label` en `pausaHTML`.

### 18. Contraste roto del badge de notas en dark
- **Elemento:** `.nb { background:var(--amb); color:#fff }`.
- **Problema:** en dark `--amb:#E09A4B` con texto blanco ≈ 2.4:1 (falla WCAG incluso para texto bold 12px).
- **Fix:** `:root[data-theme="dark"] .nb, @media dark → color:#291E10` (el propio `--amb-sub`). Una línea.

### 19. Humo que vale la pena simular ANTES de congelar (3 rentables, el resto puede esperar)
- **(a) Guardar etapas** (`guardarEtapas`): el toast promete "el tablero se redibuja con tus etapas" y es falso — mapear cada `.et-nom` editado a su `h5` de columna (`#board .colk h5`) es ~5 líneas y demuestra la tesis "etapas = datos".
- **(b) Cancelar seguimiento** (prog-card de Jorge): que el botón elimine la tarjeta del hilo (`m.cancelado=true` + re-render) — hoy es toast; es LA prueba de que el dueño controla al bot.
- **(c) Tomar el chat**: banner azul "Tú llevas este chat — Sofía en silencio" + botón "Devolver a Sofía" (estado `c.tomado`); conecta con el mensaje del composer "Escribe y Sofía se calla".
- Pueden quedar como toast sin pena: Instagram/Meta, catálogo de conexiones, "+ Etapa/Reordenar", "Cambiar" preset, tab Destapes de Caminos.

### 20. Limpieza: markup estático muerto de la pausa (bomba latente)
- **Elemento:** HTML inicial de `#dec-pausa` (líneas ~370-373): `id="in-pausa"` y `onclick="pausaResponder()"` sin argumento.
- **Problema:** hoy es código muerto porque `pintarPausa()` lo reemplaza en el init — pero si el init se reordena o falla, ese botón revienta (`getElementById('in-pausa-undefined')` → TypeError). Igual de muertos: `REPLAYS.pruebas` y `REPLAYS.historial` (c:'').
- **Fix:** dejar `#pausa-cuerpo` vacío en el HTML (pintarPausa es la única fuente) y borrar las dos entradas muertas de REPLAYS.

---

## Notas transversales

- **Patrón raíz de los hallazgos 3-5, 9, 13:** el prototipo tiene DATA como fuente única para
  chats/caminos, pero los **contadores y totales están hardcodeados en el HTML** (cnt-hoy "2",
  Chats "7", Caminos "46", totales de columnas, hero $450mil, `Math.max(0, 2 - nRes)`).
  Al congelar para backend conviene una función `recontar()` que derive TODO de DATA — es
  además la interfaz natural con el backend futuro ("solo cambia esta fuente", como promete
  el comentario de la línea 759).
- El fix del scroll (nº 1) es el único que bloquea físicamente el recorrido; el charset (nº 2)
  bloquea compartirlo. Recomiendo aplicarlos antes de cualquier otra cosa.
- Verificación en navegador hecha con servidor local temporal (ya detenido); sin cambios en
  el archivo auditado.
