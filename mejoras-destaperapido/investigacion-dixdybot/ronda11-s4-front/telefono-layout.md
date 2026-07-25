# El panel en el teléfono — qué medía, qué mide y qué regla lo arregló

25-jul-2026. Arreglo de los seis defectos que me tocaron de `visual-base.md` §4 (1, 2, 3, 4, 5
y 6). Solo toqué `panel/pwa/tokens.css` y la ESTRUCTURA de `panel/pwa/index.html`; más
`src/panel/diseno.ts` (+ su test) porque la vista Diseño declaraba por escrito el defecto 6 y
al arreglarlo tenía que dejar de mentir. **Cero líneas de `app.js` y cero del servidor.**

- **Medido con:** Chromium por el MCP de Playwright contra el panel vivo
  (`http://127.0.0.1:8793`), datos reales de destaperapido, a 390×844, 1024×800 y 1440×900.
- **Fotos y mediciones crudas:** `…/scratchpad/visual-tel/` (7 PNG a 390 + las huellas
  `fp-*.json` y los diffs `d1440.txt` / `d1024.txt`).
- **Primero verifiqué el informe base.** Los seis números estaban bien: heroline 344/270
  (decía 345), última métrica terminando en el píxel 432 (decía 433), hilo de 74 px, `ag-det`
  en 356..424, cabecera de Caminos 398/334, `.meta-f` 578/278, `.contenido` de Diseño 928/334
  y `grid-template-columns: 896px`. La pista del defecto 5 (`minmax(0,1fr)` / `min-width:0`)
  también resultó correcta. Encontré además dos cosas que el informe no traía: en Agentes el
  borde derecho real llegaba a **688 px** (no 424: el chip «activo» de la ficha se iba aún más
  lejos) y en Caminos a **454**.

---

## El patrón, en una frase

**En el teléfono se ve una capa a la vez y siempre hay cómo volver.** Donde el escritorio pone
dos columnas lado a lado (Chats: lista + hilo; Agentes: lista + ficha), en ≤700 px la lista
ocupa la pantalla completa y el detalle entra encima con una barra **«← Chats» / «← Agentes»**.
El mismo gesto en las dos vistas, así el panel se vuelve predecible.

Cómo funciona sin tocar `app.js`: un checkbox oculto por vista (`.tel-capa`) es el interruptor
de capa. La lista vive DENTRO de su `<label for="…">`, así que **tocar una fila avanza** (el
label conmuta el checkbox) y la barra de volver **retrocede**. El CSS lee el estado con
`:has()`. `app.js` ni se entera: sigue haciendo exactamente lo mismo que antes.

---

## Defecto por defecto

### 1. Hoy: la cuarta métrica dibujada fuera de la pantalla
- **Antes:** `.heroline` 344 px de contenido en 270 de hueco; «0 turnos del bot» ocupaba de 399
  a 433 en una pantalla de 390, sin forma de llegar (el `body` es `overflow:hidden`).
- **Ahora:** `.heroline` **302/302** (cabe entera) y «0 turnos del bot» se dibuja en
  **x72..146, segunda fila (y145)**: visible y completa. Borde derecho de la vista: 432 → **390**.
- **Regla:** `@media(max-width:700px) { .heroline { flex-wrap:wrap; gap:16px 26px } }` y
  `.col-centro { padding:22px 16px 60px }` (el hueco pasa de 270 a 302).

### 2. Chats: el hilo en 74 px — la vista principal, inservible
- **Antes:** `lista-conv 56..316`, `hilo-col 316..390` (74 px), «Elige un chat» en tres líneas,
  el botón Enviar cortado en el borde (contenido hasta el píxel 416).
- **Ahora:** capa 1 = lista **56..390 (334 px)**; al tocar una conversación, capa 2 = hilo
  **56..390 (334 px)** con barra «← Chats» (44..82), cabecera del chat (82..135), hilo
  (135..774) y el composer abajo con **Enviar completo en 304..367**. Borde derecho: 416 → **390**.
- **Reglas:** `.lista-conv { width:auto; flex:1; border-right:none }` +
  `.sublay:has(.tel-capa:checked) .lista-conv { display:none }` +
  `.sublay:not(:has(.tel-capa:checked)) .hilo-col { display:none }`, con el `<label>` alrededor
  de `#lista-conv` y `#dormidos-lista` y la barra `.tel-volver` dentro de `.hilo-col`.
- **Extra que destapó el arreglo:** con el hilo ya ancho, `.hilo-head` (48 px fijos) se
  desbordaba encima de la barra de volver (nombre + chip + botón no caben en 334). Lo arreglé
  en el mismo bloque: `.hilo-head { height:auto; min-height:48px; flex-wrap:wrap; row-gap:4px }`.
  Medido después: barra 44..82, cabecera 82..135, sin solape.

### 3. Agentes: la ficha 34 px fuera de la pantalla
- **Antes:** `ag-lista 56..356`, `ag-det 356..424` (68 px de ancho, 34 fuera); el borde derecho
  real de la vista llegaba a **688**. No se veían ni la nota del juez ni el gate.
- **Ahora:** mismo patrón. Capa 1 = lista **56..390**; al tocar un agente (o Recepción, o el
  Gimnasio), capa 2 = ficha **56..390** con «← Agentes» arriba. Se leen enteros el nombre, el
  chip de estado, las 4 métricas, el gate, la personalidad y el ejemplo
  (`agentes-detalle-390-claro.png`). Borde derecho: 688 → **390**.
- **Reglas:** `#v-agentes { flex-direction:column }`, `.ag-lista { width:auto; flex:1 }`,
  `#v-agentes:has(.tel-capa:checked) .ag-lista { display:none }` y su `:not(...)` para la ficha
  y la barra. `#ag-lista` pasó de `<div>` a `<label>` (misma caja: verificado, 300×900 idéntico).

### 4. Caminos: el chip «30 borradores» cortado y la ayuda truncada
- **Antes:** cabecera 398 px de contenido en 334 (del chip solo se leía «bo»); la frase de ayuda
  (`.meta-f`, `white-space:nowrap`) 578 px en 278, cortada en «…por ahora los ca…».
- **Ahora:** cabecera **334/334** en tres renglones (título · pestañas · chip completo
  «30 borradores» alineado a la derecha) y la frase **306/306**, envuelta y completa: «La guía
  llega con el asistente: por ahora los caminos se revisan y aprueban con los botones de
  arriba.» Borde derecho: 454 → **390**.
- **Reglas:** `.vheader { height:auto; min-height:44px; flex-wrap:wrap; row-gap:6px }`,
  `.vheader .tabs { margin-left:0 }` y `.meta-f { white-space:normal }` (solo en ≤700: en el
  teléfono no hay globo del mouse que rescate un texto cortado, así que se envuelve).

### 5. Diseño: 928 px de catálogo en 334 de hueco
- **Antes:** `.contenido` 928/334 y `.specs` resolviendo a `grid-template-columns: 896px`.
- **Ahora:** `.contenido` **334/334**, `.specs` **302/302** y `grid-template-columns: 302px`.
  Las 31 fichas se leen en una columna, sin cortes (`diseno-botones-390-claro.png`).
- **Regla:** en el bloque de ≤900 px, `.specs { grid-template-columns:minmax(0,1fr) }` +
  `.spec { min-width:0 }`. **La pista del informe era correcta** y el mecanismo también: `1fr`
  no baja del mínimo automático de la ficha, y ese mínimo lo fijaban las líneas `nowrap` de
  adentro. Va en ≤900 (no en ≤700) porque el desborde empieza apenas la grilla pasa a una
  columna: a 900 px de ventana la columna de 896 ya se sale.

### 6. El botón mentiroso (y el campo, y el interruptor)
- **Antes:** `tokens.css` no tenía ni una regla `:disabled`. El «Preguntar» de Caminos estaba
  `disabled` pintado de verde primario `rgb(14,122,95)` con texto blanco y `cursor:pointer`; el
  «Enviar» de Chats igual; el campo de mensaje se veía vivo.
- **Ahora** (medido en los dos temas):
  - primario apagado — claro: fondo `#E7EBE9` (n3) texto `#69766F` (n9); oscuro: `#1F2523` /
    `#7C8983`. `cursor:not-allowed` en ambos.
  - secundario apagado: igual.
  - campo apagado: contenedor en n2, texto en n9, `cursor:not-allowed`, y el campo de la guía
    pierde la sombra (lo que no funciona no flota).
  - interruptor bloqueado: riel n4 y perilla n6 sin sombra.
- **Reglas:** `.btn:disabled/[disabled]`, `.btn.p:disabled, .btn.s:disabled`,
  `input/textarea/select:disabled`, `.composer:has(textarea:disabled)`,
  `.g-input:has(input:disabled)` y `.sw input:disabled ~ .p1/.p2`.
- **Trampa que solo aparece midiendo:** en oscuro, `:root[data-theme="dark"] .btn.p` (más peso)
  seguía imponiendo `color:#07130E` y el botón apagado quedaba con texto casi negro sobre n3
  (ilegible). Lo vi al medir el computado, no en el código. Arreglado con las dos reglas
  gemelas del tema (`:root[data-theme="dark"] .btn.p:disabled` y la del
  `prefers-color-scheme`), igual que ya hacía el sistema para el primario vivo.
- **La vista Diseño ya no miente** (`src/panel/diseno.ts`):
  - la ficha «botones» ofrece la **tercera clase copiable**: `btn p` · `btn s` · `btn[disabled]`,
    y el demo muestra un primario y un secundario apagados;
  - la ficha «interruptor» muestra el tercer estado (bloqueado);
  - **desapareció** la línea «estado deshabilitado del botón» de *Le falta al sistema*: la
    sección pasó de 2 huecos a 1 (queda «campo de texto suelto», que sigue siendo verdad);
  - el revisor del catálogo aprendió a validar `clase[atributo]`: si alguien borra las reglas
    `:disabled` de `tokens.css`, la vista lo **denuncia** en vez de dibujarlo igual (hay test).

---

## La regla de oro: el escritorio no se movió

Método: huella de **todos** los elementos de `.shell` en las 6 vistas (etiqueta, clase, x, y,
ancho, alto, fondo, color, tamaño de letra, opacidad) antes y después, a 1440 y a 1024. Antes de
usarla la corrí dos veces seguidas sin tocar nada: **0 líneas de diferencia**, o sea la medición
no tiene ruido.

Resultado (`d1440.txt` y `d1024.txt`, 28 líneas cada uno, idénticas entre sí):

- **Ni un píxel movido.** Cero cambios de x, y, ancho o alto en las dos resoluciones.
- 2 líneas son solo el cambio de etiqueta `<div>`→`<label>` de `#lista-conv` y `#ag-lista`, con
  **la misma caja exacta** (339×6391 y 300×900).
- 6 líneas son los colores del defecto 6: el composer de Chats, el campo de la guía y los tres
  botones apagados (`#btn-guia`, el «Enviar» y el «Sin permiso» del catálogo).

O sea: lo único que cambia en el escritorio son los controles apagados — que es exactamente lo
que se pidió arreglar. **Eso sí es un cambio visible en 1440 y 1024**, y lo digo abierto: si
Alejandro prefiere que el apagado se vea de otra forma (más suave, o solo el cursor), es un
ajuste de una línea; lo que no puede volver es que un botón muerto se vea como el más
importante de la vista.

Verificaciones sueltas: `.hilo-head` a 1440 sigue midiendo exactamente 48 px de alto, la lista
340, el hilo 560 y la ficha 300; la barra de volver no existe (no se dibuja) sobre 700 px.

---

## Lo que NO pude arreglar sin cambiar el diseño (o sin tocar app.js)

1. **Entrar a un chat desde fuera de la lista deja al dueño en la lista.** Si abres un chat
   desde el Tablero, desde «Ver chat» de Hoy o desde el globo de «sin monto», el teléfono te
   deja en la capa de la lista con esa conversación marcada, y hay que tocarla otra vez.
   Medido y confirmado. Es el precio de conmutar la capa sin JS: el interruptor solo lo mueve
   el dedo sobre la lista. **Se arregla con una línea en `app.js`** (marcar el checkbox dentro
   de `abrirChat()`), que es del otro agente de esta tanda.
2. **Acoplamiento que hay que respetar:** las filas `.conv` y `.ag-item` tienen que seguir
   siendo `<div>`. Si alguien las convierte en `<button>` (contenido interactivo), el `<label>`
   deja de activarse y el teléfono ya no avanza solo. Lo dejé escrito en `index.html`, al lado
   del interruptor. (Ojo: mientras yo trabajaba, el otro agente les agregó `tabindex`/`role` —
   eso **no** rompe nada, lo verifiqué en vivo; lo que rompería es cambiar la etiqueta.)
   Relacionado: quien navegue con **teclado** en una pantalla angosta cambia de capa solo si el
   manejador de teclas dispara un `click()` sobre la fila.
3. **El tablero de Chats sigue siendo una sola columna a la vez con arrastre lateral** y sin
   señal de que se pueda arrastrar (aviso 6 del informe base). Cambiarlo es diseño: habría que
   decidir si en el teléfono el tablero se apila, se pagina o se queda así.
4. **La mitad derecha vacía a 1440** (defecto 13) y **la cifra exacta escondida en el `title`**
   (defecto 11) no los toqué: el primero es decisión de diseño de Alejandro y el segundo
   necesita que alguien decida dónde va el número real en una pantalla sin mouse (además el
   contenido lo pinta `app.js`).
5. **Entre 701 y 900 px** (tablet angosta, iPad partido) sigue habiendo dos columnas: es el
   comportamiento de hoy y ahí sí caben (lista 260 + hilo ≥400). Solo bajé el `.specs` de
   Diseño a ese rango porque ahí ya se desbordaba de verdad.
6. **`:has()`** es la pieza que sostiene el patrón: necesita Safari 15.4+ / Chrome 105+. En un
   iPhone actualizado no es problema; en un navegador viejo se vería el estado de hoy (dos
   columnas apretadas), no una pantalla rota.

---

## Estado en que dejé todo

- `npx tsc --noEmit` limpio y `npx vitest run` entero verde: **38 archivos, 592 pruebas**.
- Panel reiniciado (`launchctl kickstart`) y respondiendo 200; `/api/diseno` sirve
  `faltan: ['campo de texto suelto']` y `botones: ['btn p','btn s','btn[disabled]']`.
- Navegador: vista Chats, capa de lista, sin tema forzado, sin popups.
