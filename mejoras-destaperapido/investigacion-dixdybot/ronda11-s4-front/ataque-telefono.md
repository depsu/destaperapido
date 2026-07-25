# Ataque al arreglo del teléfono — 25-jul-2026

Rol: romper lo que dos agentes acaban de arreglar (layout de teléfono, estados del botón,
teclado, avatar). Método: **código y datos, sin navegador** — leer el CSS y el JS, correr la
función suelta contra emoji de verdad, medir el contraste con la fórmula WCAG sobre los
tokens reales, y consultar los endpoints vivos del panel (127.0.0.1:8793).

**Resultado: 10 agujeros reales, los 10 arreglados, cada uno con su test en ROJO verificado
a mano.** `npx tsc --noEmit` limpio y `npx vitest run` entero verde: **39 archivos, 612
pruebas** (venían de 38/592; sumé 1 archivo y 20 pruebas).

Un solo píxel del escritorio cambia, y es justo el defecto que arreglo (§6).

---

## 1. EL AVATAR — 2 agujeros reales, y el resto aguantó

Ataqué `inicial()` con 28 nombres hostiles corriendo la función de verdad
(`node --experimental-strip-types`).

**Aguantó todo lo que el encargo pedía probar** — banderas, familias, género, piel, RTL:

| nombre | sale | code points |
|---|---|---|
| `🇨🇱` | `🇨🇱` | U+1F1E8 U+1F1F1 (entera) |
| `👨‍👩‍👧` | `👨‍👩‍👧` | U+1F468 200D 1F469 200D 1F467 |
| `🏋️‍♀️ Gimnasio` | `G` | U+0047 |
| `🏋️‍♀️` (sola) | `🏋️‍♀️` | U+1F3CB FE0F 200D 2640 FE0F |
| `👍🏽` | `👍🏽` | U+1F44D U+1F3FD |
| `أحمد` / `שלום` | `أ` / `ש` | primera letra lógica |
| `‏أحمد` (con marca RTL) | `أ` | la marca se salta |
| `   Juan` / `"Don Pepe"` / `'Nacho'` | `J` / `D` / `N` | |
| `😀` / `` (vacío) / `   ` | `😀` / `?` / `?` | |

**AGUJERO 1 — una letra cuya mayúscula son DOS.** `"ß".toUpperCase() === "SS"` y
`"ﬁ".toUpperCase() === "FI"`. La función subía a mayúscula *después* de cortar, así que
devolvía dos glifos dentro de un círculo de 32px. Rompe su propio contrato declarado
("siempre devuelve UN solo carácter visible") y el test que lo afirmaba no probaba ningún
caso así.

```
inicial('ßeta')     → "SS"   (2 grafemas)   ahora → "S"
inicial('ﬁnanzas')  → "FI"   (2 grafemas)   ahora → "F"
```

**AGUJERO 2 — un nombre hecho solo de caracteres invisibles dejaba el círculo VACÍO.** Pasa
de verdad en WhatsApp (nombres con juntador o espacio de ancho cero). No hay letra, así que
caía en "el primer carácter completo" y ese carácter no pinta nada:

```
inicial('‍')  → "‍"  (ZWJ)              ahora → "?"
inicial('​')  → "​"  (espacio ancho 0)  ahora → "?"
inicial('️')  → "️"  (selector variac.) ahora → "?"
inicial('﻿')  → "﻿"  (BOM)              ahora → "?"
```

Arreglo (`src/panel/inicial.ts`, espejado en `app.js`): la mayúscula se corta **después** de
subirla, y si no hay letra se busca el primer grafema que **pinte** algo (todo lo que sea
solo `\p{Cf}\p{Cc}\p{Zs}\p{Zl}\p{Zp}\p{Mn}\p{Me}` se salta). Un tono de piel suelto (`🏽`,
categoría Sk) sí se considera visible y sale.

**AGUJERO 3 — el espejo no tenía quién lo vigilara.** La regla está escrita dos veces
(`inicial.ts` para el servidor, `inicialAvatar()` en `app.js` para los avatares que arma el
navegador) y solo un comentario pedía mantenerlas iguales. Ahora hay un test que **saca la
copia de app.js del archivo, la ejecuta** y la compara con el original nombre por nombre
(31 nombres). Verificado en rojo: desincronizando una línea de app.js, falla con
`«ßeta» difiere entre app.js e inicial.ts`.

### Corrección al informe base
El agente 2 dijo "49 de los 128 chats servidos". Medido exacto contra `/api/chats` en vivo
aplicando el código viejo (`(nom[0] ?? '?').toUpperCase()`): **50 de 128**. Y hay **51** chats
cuyo nombre empieza con emoji o símbolo — el 51.º es `☺️😉😁😊`, que no se rompía porque
U+263A cabe en 16 bits. Hoy: 0 rotas, 0 de dos grafemas, 0 invisibles.

---

## 2. LOS ESTADOS DEL BOTÓN — el contraste está bien, pero el interruptor desapareció

Contraste medido con la fórmula WCAG sobre los valores reales de `tokens.css` (no estimado):

| qué | claro | oscuro | veredicto |
|---|---|---|---|
| texto del botón apagado (n9 sobre n3) | **3,95** | **4,28** | ✅ se lee |
| texto del botón apagado en hover | 3,95 | 4,28 | ✅ (la regla gemela gana) |
| campo apagado (n9 sobre n2 del contenedor) | 4,29 | 4,87 | ✅ |
| referencia: texto normal (n12 sobre n1) | 15,83 | 16,87 | — |
| **perilla del interruptor bloqueado (n6 sobre pista n4)** | **1,16** | **1,30** | ❌ **invisible** |

**El botón apagado está bien.** La trampa que el agente 1 dice haber cazado en oscuro está
cazada de verdad: `:root[data-theme="dark"] .btn.p:disabled` y su gemela de
`prefers-color-scheme` existen y ganan por orden de fuente. 3,95 / 4,28 se lee de sobra, y
los controles deshabilitados están además exentos del 4,5 de la WCAG (1.4.3, "incidental").

**AGUJERO 4 — el interruptor bloqueado se volvió invisible.** Al aplanar la pista a `--n4`
(igual encendido que apagado) el bulto blanco quedaba como única señal de posición… y lo
pintaron de `--n6` **quitándole la sombra**: contraste 1,16. En el catálogo de Diseño el
interruptor "bloqueado" es un óvalo gris liso donde no se ve si está encendido o apagado.
Apagado se había vuelto *no está*. Con `--n9`: **3,65 / 3,72** — se ve, y sigue viéndose
más apagado que el vivo.

**AGUJERO 5 — `.btn[disabled]` cubierto a medias.** La línea del cursor engancha las dos
formas; la del color, solo `:disabled`:

```css
.btn:disabled, .btn[disabled]      { cursor:not-allowed; filter:none; }   /* las dos */
.btn.p:disabled, .btn.s:disabled   { background:var(--n3); … }            /* solo una */
```

`:disabled` **solo existe para controles de formulario**. Y la vista Diseño publica
`btn[disabled]` como clase copiable, o sea invita explícitamente a copiarla a cualquier
cosa: un `<a class="btn p" disabled>` salía con el cursor de bloqueado y el verde de vivo.
Arreglado enganchando el color también del atributo.

**AGUJERO 6 — el test de mutación del agente 1 se volvió falso-verde.** Su prueba borraba
las líneas que contuvieran `:disabled` y esperaba que el catálogo denunciara el hueco. En
cuanto existen reglas escritas `[disabled]`, esas sobreviven a la mutación y el test pasa
sin haber probado nada. Corregido: la mutación borra las dos grafías.

**`aria-disabled`: no está cubierto — y es teórico.** Nadie en el panel lo usa (grep: cero
apariciones); todo apaga con el atributo nativo, que es lo correcto. Recomendación: seguir
así y no inventar CSS para un estado que el sistema no usa.

---

## 3. EL TECLADO — el teléfono entero era inalcanzable

**AGUJERO 7 — con el teclado no se podía cambiar de capa. En ninguna dirección.**
El interruptor de capas del agente 1 era un `<label for>` alrededor de la lista. Un `<label>`
solo reacciona al **clic**. Consecuencia medida leyendo el código:

- Tabular a una fila `.conv` y pulsar Enter → `abrirChat()` pinta el hilo, pero
  `.hilo-col` sigue en `display:none` porque el checkbox no se marcó. **No pasa nada.**
- El `← Chats` era un `<label>`: **nunca recibe foco**. No había forma de volver.

O sea: los 108 tab-stops que el agente 2 agregó a Chats (su "coste honesto") en 390px no
hacían **nada visible**. Es exactamente lo que el encargo pedía cazar: tabular a algo que no
hace nada.

**AGUJERO 8 — el `<label>` se traga TODOS los toques, no solo los de una fila.** Las listas
las pinta `app.js` con más cosas que filas dentro. Con el label puesto, tocar cualquiera de
estas 7 zonas muertas te sacaba de la lista y te tiraba al detalle sin haber elegido nada:

| vista | zona muerta que navegaba |
|---|---|
| Chats | título «Dudas del bot — necesita tu respuesta» |
| Chats | título «Activos» |
| Chats | el aviso «Nada con "…"» de la búsqueda sin resultados |
| Chats | el pie «duermen solos sin actividad ni pendientes…» de Dormidos |
| Agentes | título «Recepción» |
| Agentes | título «Especialistas» |
| Agentes | título «Gimnasio» |

**AGUJERO 9 — el orden del tabulador no seguía el orden visual.** En Agentes el
`← Agentes` lleva `order:-1` (se pinta arriba de todo) pero estaba **al final del HTML**, y
el tabulador sigue el HTML: había que recorrer la ficha entera para encontrar cómo salir.
Movido antes de `.ag-det` (en el escritorio va `display:none`, así que no mueve nada).

### El arreglo: el interruptor lo mueve el código, no un `<label>`

Cambié el mecanismo, no el patrón. El checkbox `.tel-capa` y las reglas `:has()` del agente 1
siguen intactas; lo que cambia es **quién lo marca**:

```js
function capaTelefono(id, verDetalle) { … }   // app.js
```

- `abrirChat()` marca la capa **cuando el hilo ya está pintado** — venga de la lista, del
  tablero o de una tarjeta de Hoy. Esto tapa de paso la limitación que el agente 1 declaró
  abierta ("abrir un chat desde el Tablero o desde Hoy deja al dueño en la lista").
- `ir()` la desmarca: entrar a una vista siempre te deja en la LISTA (antes, volver a
  «Chats» desde el menú te dejaba en el hilo de anoche).
- `vistaChats('lista')` la desmarca: volver a «Lista» a mano muestra la lista.
- En Agentes se marca en el **clic/Enter del dueño**, no dentro de `verAgente()`: esa función
  también preselecciona un agente al cargar la vista, y eso no es una elección suya.
- `← Chats` / `← Agentes` pasan a ser `<button>` de verdad: reciben foco, Enter funciona
  solo, y bajo 700px son la primera parada del tabulador.

Y se cae el acoplamiento que el agente 1 anotó ("las filas `.conv` deben seguir siendo
`div`, si pasan a `button` el teléfono deja de avanzar"): ya da igual qué etiqueta sean.

### Lo que SÍ estaba bien (contra-comprobado)

- **No se puede quedar atrapado el foco en el flotante**: Escape lo cierra (manejador
  global), la ✕ lo cierra, y clicar fuera saca el foco. El cerco solo actúa mientras el foco
  está dentro.
- `activable()` es idempotente (`dataset.activable`), así que repintar una lista no encadena
  manejadores ni duplica paradas.
- Ninguna parada de tabulador nueva en el escritorio: los dos `<button class="tel-volver">`
  van `display:none` sobre 700px, y `display:none` no se tabula.

---

## 4. EL @MEDIA — la frontera, el teléfono girado y el zoom al 200%

**901px vs 900px.** A 901 no aplica nada del bloque angosto: `aside` 240 + `.lista-conv` 340
+ `.ctx` 300 = 880 fijos, y la columna del hilo se queda con **21px** — con 48px de padding
adentro (`.hilo { padding:20px 24px }`). A 1024 son 144px. **Es de la base, no de esta
tanda**, y subir el corte movería el escritorio de 1024: lo dejo dicho, no tocado. Decide
Alejandro.

A 700 vs 701: 701 sigue en dos columnas (56 + 260 + hilo) sin desbordar; 700 entra el patrón
de una capa. Frontera limpia.

**AGUJERO 10 — bajo 900px el panel del camino no existía, y eso deja Caminos muerto.**
`tokens.css` tenía `.ctx, .peek { display:none !important; }`. Tocar una tarjeta de camino
llamaba a `abrirCamino()`, traía los datos, marcaba la tarjeta… y **no mostraba nada**.
Afecta a tres situaciones reales, no solo al teléfono:

| situación | ancho de CSS | ¿aplica ≤900? | ¿aplica ≤700? |
|---|---|---|---|
| teléfono de pie | 390 | sí | sí |
| **teléfono girado** | **844** | **sí** | no |
| **escritorio de 1440 con zoom al 200%** | **720** | **sí** | no |

Las dos últimas son las peores: el patrón de "una capa a la vez" ni siquiera entra, así que
no había ninguna otra puerta. Y la del zoom es literalmente el caso "alguien que no ve bien"
del encargo. El agente 2 lo detectó y lo dejó como «PENDIENTE AJENO»; lo tomo.

Arreglo, entero dentro de `@media (max-width:900px)` (o sea: **imposible que toque 1024 o
1440**): el `!important` se queda solo en `.ctx`, y `.peek.ver` entra **encima**, a pantalla
completa. Se cierra con su ✕ o con Escape, y `enfocarPanel()` —que se saltaba el peek por
invisible— ahora mete el foco de verdad.

**Teléfono girado (844x390) en el resto de las vistas:** revisado columna por columna, todas
las zonas largas tienen su propio `overflow-y:auto` (`.contenido`, `.ag-det`, `.caminos-izq`,
`.hilo`, `.lista-conv`), así que 390px de alto no desbordan la página. Sin hallazgos.

---

## 5. ¿ALGUIEN INVENTÓ CSS? ¿SIGUE SIENDO UN MOLDE? — grep, y limpio

- **`<style>` sueltos:** cero, en index.html y en app.js. Tampoco `insertRule` ni
  `createElement('style')`.
- **`!important`:** siguen siendo 3 y son los del prototipo (2 de `prefers-reduced-motion`,
  1 de `.ctx`). Yo **quité uno** (el de `.peek`) y no agregué ninguno.
- **Clases inventadas:** cero. index.html usa 56 clases y app.js 85 (leídas vaciando las
  interpolaciones `${…}` de las plantillas): **todas** existen en tokens.css.
- **Datos de cliente en el molde:** cero. Ni nombres de clientes ni teléfonos reales.

**Lo que faltaba y agregué:** el molde validaba el catálogo → tokens.css, pero **nadie
vigilaba index.html ni app.js**. Cualquiera podía escribir `class="mi-clase"` en app.js y
ningún test se enteraba. Ahora sí (`src/panel/pwa.test.ts`).

**La vista Diseño sigue siendo verdad… en un sentido y medio.** «Toda clase que muestra
existe» está probado (`revisarCatalogo`) y pasa. La otra dirección, «toda clase pública que
existe se muestra», **sigue abierta**: haría falta marcar en tokens.css cuáles son públicas,
porque de las clases del sistema muchas son internas (`.p1`, `.crece`, `.c1`, `.d`, `.m`).
No lo invento yo — es una decisión de diseño del catálogo. Lo dejo declarado.

---

## 6. LA REGLA DE ORO — el único píxel que se mueve, y por qué

Cambio por cambio, qué le pasa al escritorio a 1440 y 1024:

| cambio | efecto en 1440/1024 |
|---|---|
| `inicial()` + espejo en app.js | **ninguno**: medido contra los 131 nombres vivos (128 chats + 2 especialistas + recepción), **0 iniciales cambian de dibujo** |
| `<label id=lista-conv>` → `<div>` (y las otras 2 listas) | **ninguno**: el label llevaba `display:block` puesto a mano, un div lo es de nacimiento — misma caja |
| `<label class=tel-volver>` → `<button>` | **ninguno**: `display:none` sobre 700px |
| mover el `← Agentes` antes de `.ag-det` | **ninguno**: va `display:none`, no ocupa lugar en el flex |
| `.btn.p[disabled], .btn.s[disabled]` | **ninguno**: hoy todos los `.btn` apagados son `<button>`, que ya casaban con `:disabled` con las mismas declaraciones |
| bloque del `.peek` a pantalla completa | **ninguno**: vive entero dentro de `@media (max-width: 900px)` |
| borrar `.tel-lista` | **ninguno**: solo se aplicaba a elementos que ya no existen |
| **perilla del interruptor bloqueado n6 → n9** | **SÍ**: un círculo de 18×18 px (≈254 px pintados) en el tercer interruptor del catálogo de Diseño |

**Lo digo abierto: ese círculo es el único píxel de escritorio que cambia, y es exactamente
el defecto que arreglé.** Ese interruptor bloqueado no existía en la foto del *antes*
(`visual-base/`) — lo agregó el agente 1 en esta misma tanda, junto con los otros 6 cambios
de color de los controles apagados que él ya declaró. Mi corrección es dentro de ese mismo
cambio declarado: lo dibujó tan apagado que desapareció, y ahora se ve.

Comprobaciones de seguridad además de los tests: `node --check app.js` (sintaxis), balance de
llaves y declaraciones de tokens.css (323 reglas, 0 sospechosas), y el panel reiniciado con
`launchctl kickstart` responde 200 sirviendo los tres archivos nuevos.

---

## 7. REAL PERO NO ARREGLADO — decide Alejandro

No los toco porque arreglarlos **cambia el diseño**, y el diseño lo decide él.

1. **Burbujas del bot que prometen un clic que no existe.** `.bur.bot` tiene
   `cursor:pointer` y `outline` al pasar el mouse, y **cero manejadores** (grep en app.js).
   Igual `.pill-sys.tema` (cursor:pointer) y `.b-ens` (el botón de "enseñar" que el CSS
   dibuja al pasar por encima de una burbuja) — este último app.js no lo pinta nunca. Son
   restos del prototipo. Las dos salidas cambian el dibujo: cablear "enseñar" de verdad, o
   quitarles el señuelo. **No las hice focoables a propósito**: tabular a algo que no hace
   nada es peor que no poder tabular.
2. **`aria-modal="true"` sin fondo ni `inert`.** El flotante le dice al lector de pantalla
   "todo lo demás no existe", pero mide 320px y lo de atrás sigue clicable: un usuario con
   ratón sale del cerco cuando quiere. O se hace modal de verdad (`inert` en `.shell`
   mientras esté abierto) o se baja a popover sin `aria-modal`. Prefiero no dejar la app
   `inert` colgada por un cierre que no corra.
3. **La frontera de 900px aprieta** (§4): a 901px el hilo mide 21px. Es de la base. Subir el
   corte movería 1024.
4. **El catálogo se valida en un solo sentido** (§5).

**Teórico, no real:** un `<a class="btn p" disabled>` (ya no se rompe, pero nadie lo usa
hoy); y que un navegador sin `Intl.Segmenter` cortaría las banderas por la mitad — todos los
navegadores actuales lo traen, y el respaldo por code point ya evita el caso peor de partir
una letra UTF-16.

---

## 8. Tocado

| archivo | qué |
|---|---|
| `dixdybot/src/panel/inicial.ts` | mayúscula antes del corte; se salta los grafemas que no pintan |
| `dixdybot/src/panel/inicial.test.ts` | +4 pruebas: ß/ﬁ, invisibles, RTL, y un barrido de 30 nombres hostiles |
| `dixdybot/src/panel/pwa.test.ts` | **nuevo**: contraste medido de los apagados, etiquetas del teléfono, espejo del avatar, cero CSS inventado, cero datos de cliente |
| `dixdybot/src/panel/diseno.test.ts` | la mutación del apagado borra las dos grafías (era falso-verde) |
| `dixdybot/panel/pwa/app.js` | `capaTelefono()` + los 5 sitios que la mueven; espejo del avatar al día |
| `dixdybot/panel/pwa/index.html` | 3 `<label>` → `<div>`, 2 `<label>` → `<button>` con `data-capa`, el volver de Agentes antes de la ficha |
| `dixdybot/panel/pwa/tokens.css` | color del apagado también por atributo; perilla n6→n9; `.peek` a pantalla completa bajo 900px; fuera `.tel-lista` |

Cero cambios en el servidor, en el bot vivo y en la instancia del cliente. Cero git.
