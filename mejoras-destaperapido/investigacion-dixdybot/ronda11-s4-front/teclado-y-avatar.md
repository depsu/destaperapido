# Teclado y avatar — defectos 7 y 8 del panel · 25-jul-2026

Arreglo de los dos defectos que me tocaron de `visual-base.md` §4. Toqué **dos archivos**:
`dixdybot/panel/pwa/app.js` y `dixdybot/src/panel/consultas.ts` (+ un archivo nuevo y sus
tests). **No toqué `tokens.css` ni la estructura de `index.html`** — el otro agente está ahí.

- **Escritorio idéntico:** 0 píxeles de diferencia a 1440 y a 1024, en las seis vistas
  (medido, ver §4).
- `npx tsc --noEmit` limpio · `npx vitest run` entero verde: **38 archivos, 592 tests**
  (eran 590 antes; los 2 nuevos son míos).
- Consola del navegador: **0 errores** en todas las pruebas.

---

## 1. Lo que verifiqué del informe base antes de creerle

| Lo que decía la base | Lo que medí | Veredicto |
|---|---|---|
| Defecto 7: "el tabulador hace **12** paradas en Caminos" | **10** paradas | ❌ el número está mal |
| Defecto 7: ninguna cae en las tarjetas | ninguna cae en las tarjetas | ✅ confirmado |
| Defecto 8: el avatar de "🏋️ Práctica libre" es `"\ud83c"` | es `"\ud83c"` | ✅ confirmado |
| Defecto 8: "**el** chat 🏋️ Práctica libre" | **49 de los 128 chats** servidos salían rotos | ⚠️ mucho más grande |

**Las 12 paradas eran 10.** El informe contó `#in-guia` (el campo de la guía) y `#btn-guia`
("Preguntar") como paradas del tabulador, pero los dos están `disabled` — y un control
deshabilitado **no recibe foco**, nunca. El propio informe lo dice en su defecto 6 ("está
`disabled=true`"), así que se contradice consigo mismo. Medido con la tecla Tab de verdad
(no con una consulta al DOM), 14 pulsaciones seguidas a 1440 y a 1024:

```
1..6   los seis botones del menú (Hoy · Chats · Caminos · Módulos · Agentes · Diseño)
7..9   Todos·3 · Ventas·2 · Soporte·1
10     30 borradores
11     BODY  → el foco SALE de la página y vuelve a empezar
```

**El tamaño del defecto 8 sí lo subestimó la base.** Contra el panel vivo
(`GET /api/chats`, 128 chats servidos): **49 avatares** eran media letra (`\ud83c`) — todos
los `🏋️ …` del gimnasio y los `🎬 Replay: …`. Más uno (`☺️😉😁😊`) que salía como un `☺`
descolorido porque perdía su modificador. Ahora: **0 rotos**.

---

## 2. Defecto 7 — las tarjetas ahora existen para el teclado

### Qué hice

Un ayudante único, `activable(el, alActivar, opciones)` en `app.js`, que a un `<div>` que se
comporta como botón le da **rol de botón, nombre, parada de tabulador y las teclas Enter y
Espacio**. Es idempotente (repintar una lista no encadena manejadores).

**Por qué no lo convertí en un `<button>` de verdad**, que sería lo ideal: un `<button>` nace
`inline-block` y con el texto centrado. `tokens.css` (que no puedo tocar, y que es la única
fuente visual del sistema) no tiene reglas que lo neutralicen, así que cambiar la etiqueta
cambiaría el dibujo en el escritorio — y eso ya no es un arreglo, es un cambio de diseño, que
lo decide Alejandro. La vista Diseño hace justo eso hoy con `.swc`, pero pagando el precio de
estilos en línea (`style="text-align:left;width:100%;display:block"`), que es el defecto 14
del propio informe. Con `role="button"` + `tabindex` + Enter/Espacio el teclado y el lector de
pantalla reciben exactamente lo mismo y el diseño no se mueve ni un píxel.
**Lo que hace falta para que sean `<button>` de verdad: dos líneas en `tokens.css`**
(`.bloque, .conv, .tarjk, .ag-item { display:block; width:100%; text-align:left; }`).
Lo dejo propuesto, no hecho.

### El patrón estaba en 10 sitios, no en uno

Busqué `addEventListener('click')` sobre `<div>` en todo `app.js`. Los arreglé todos:

| Vista | Qué era | Dónde |
|---|---|---|
| Caminos | tarjeta de camino `.bloque` | `app.js` · cascada |
| Caminos | "ver cuáles" (`.lnk`, un `<span>`) dentro del panel del camino | `app.js` · peek |
| Chats | fila de chat `.conv` | lista de activos |
| Chats | fila de chat dormido `.conv` | lista de dormidos |
| Chats | tarjeta del tablero `.tarjk` | board |
| Chats | pie "💤 Dormidos" (despliegue) | `#dormidos-f` |
| Hoy | "Resueltas hoy" (despliegue) | `#sec-resueltas` |
| Hoy | fila del flotante "sin monto por confirmar" | `abrirSinMonto` |
| Módulos | fila del módulo (despliega su configuración) | `cargarModulos` |
| Agentes | ítem de agente / recepción / gimnasio, y fila de práctica del gimnasio | `ag-lista`, `ag-det` |

Los despliegues (Resueltas, Dormidos, Módulos) además llevan **`aria-expanded`** y
`aria-controls`, que es lo que un lector de pantalla necesita para decir "contraído/expandido".

**Un detalle que cambió mi enfoque en Módulos:** la fila del módulo lleva el interruptor
(`.sw`) dentro, y ese interruptor es un `<input type="checkbox">` real. Si hubiera marcado la
fila entera como botón, el interruptor habría quedado *dentro* de un botón — y ARIA manda
ocultar los hijos de un botón, así que el lector de pantalla podría dejar de anunciarlo. Por
eso ahí el teclado entra por el **texto** de la fila (`.crece`) y el interruptor queda al lado,
con su propia parada. El clic del mouse sigue funcionando igual en toda la fila (verificado:
no se abre y cierra dos veces).

### El flotante de revisión en lote

`pop()` / `cerrarPop()` ahora se comportan como un diálogo de verdad:

- `role="dialog"`, `aria-modal="true"` y `aria-labelledby` apuntando al título (verificado:
  lee "Borradores por revisar · 30").
- **El foco entra** al contenedor al abrirse (para que el lector lea primero de qué es el
  panel) — con `preventScroll` para no mover la página.
- **Cerco de tabulación:** 20 pulsaciones seguidas de Tab dentro del flotante → **0 fugas**
  hacia lo que quedó detrás. Shift+Tab desde el principio salta al último control.
- **Escape cierra**, y el foco **vuelve** al botón "30 borradores".
- Funciona anidado: "ver cuáles" abre el flotante de pruebas doradas desde el panel del
  camino; Escape lo cierra y devuelve el foco a "ver cuáles"; otro Escape cierra el panel del
  camino y devuelve el foco a la tarjeta.

El panel lateral del camino (`.peek`) **no** es un diálogo (no tapa nada), así que no lleva
cerco: solo entra el foco al abrirse y vuelve a la tarjeta al cerrarse (con la ✕ o con
Escape). Y vuelve **a la tarjeta viva**, no al elemento recordado: si activaste o desactivaste
el camino, la cascada se repintó y aquel elemento ya no existe.

### Un error mío que la medición pilló

Escribí la guarda de visibilidad con `offsetParent !== null` — la forma de siempre. **Está
mal para este panel:** `offsetParent` devuelve `null` para todo lo que va `position:fixed`, y
los flotantes lo son. Resultado: el foco no entraba al flotante y yo lo habría dado por bueno
sin la prueba en el navegador. Corregido con una medición por caja
(`offsetWidth || offsetHeight || getClientRects().length`). Queda anotado porque es una
trampa que va a volver.

### Cómo quedó (medido con la tecla Tab)

```
Caminos, 1440:  1..10 igual que antes  →  11, 12, 13: las TRES tarjetas de camino
Enter sobre una tarjeta   → abre el panel; el foco entra en él ("Camino: Saludo y toma…")
Espacio sobre una tarjeta → lo mismo, y la columna NO se desplaza (scrollTop 0 → 0)
Escape                    → cierra y el foco vuelve a la tarjeta
```

### Lo que este arreglo NO resuelve (dicho claro)

- **La lista de Chats pasó de 9 a 108 paradas de tabulador** (una por chat: 98 filas + los 9
  controles de siempre). Es el precio de que las filas existan para el teclado, y es mejor que
  no existir. Lo correcto a la larga es un *roving tabindex* (una sola parada para la lista y
  flechas para moverse dentro), que ya es una decisión de comportamiento, no un arreglo.
  Paradas por vista hoy: Hoy 8 · Chats 108 · Caminos 13 · Módulos 26 · Agentes 10 · Diseño 120.
- **En el teléfono (390) activar una tarjeta de camino no muestra nada**, porque
  `tokens.css:342` esconde `.peek` bajo 900 px. El teclado ya llega a la tarjeta y no se pierde
  (verificado: el foco se queda en la tarjeta, no salta a un panel invisible, y no hay errores),
  pero **el panel del camino no tiene forma de verse en el celular**. Eso es del arreglo de
  layout del teléfono, no mío: lo dejo señalado para quien lo esté haciendo.
- Los globos `[data-tip]` siguen siendo solo de `:hover` (defecto 11), que no me tocaba.

---

## 3. Defecto 8 — el avatar con emoji

### La decisión, y por qué

La pregunta era: para "🏋️ Práctica libre", ¿el emoji o la P? **La P.** Está escrito en el
comentario de cabecera de `src/panel/inicial.ts`, y el razonamiento es este:

El avatar es un **monograma**: sirve para distinguir un chat de otro en una lista larga. En
WhatsApp el emoji del principio casi siempre es adorno, y **el adorno se repite**: en los datos
vivos hay 10 chats "🎬 Replay: …" y 20 "🏋️ …". Con el emoji, esos 30 avatares serían dos
dibujos repetidos, que no distinguen nada. Con la letra son P, U, R, E, C, V… que sí. Además es
lo que una persona espera cuando le dicen "la inicial".

La regla, entonces: **primera letra o número del nombre**; si el nombre no tiene ninguna letra
(uno hecho solo de emoji, como `☺️😉😁😊`), entonces sí el **primer carácter completo**, porque
es lo único que hay; y si no hay nada, `?`.

### `[...nom][0]` no bastaba — y lo demuestro en un test

La base proponía `[...nom][0]`. Parte por *code point*, no por lo que la persona ve:

- `[...'🇨🇱'][0]` → `'🇨'` (media bandera: se dibuja como una letra en un cuadrito)
- `[...'🏋️'][0]` → `'🏋'` (sin su U+FE0F: pierde el color)

Corto por **grafema** con `Intl.Segmenter`, que es la unidad que se ve. Cubre banderas
(dos indicadores regionales), familias (`👨‍👩‍👧`, unidas por ZWJ), tonos de piel (`👍🏽`) y las
tildes descompuestas (`a` + tilde suelta → `Á`, no `A`).

### Dónde estaba el bug (en 4 sitios, no en 1)

| Archivo | Qué era | Ahora |
|---|---|---|
| `src/panel/consultas.ts:111` | `ini: (nom[0] ?? '?').toUpperCase()` — el avatar de **cada chat** | `inicial(nom)` |
| `panel/pwa/app.js` | avatar del agente en las decisiones de Hoy | `inicialAvatar(...)` |
| `panel/pwa/app.js` | avatar del especialista en la lista de Agentes | `inicialAvatar(...)` |
| `panel/pwa/app.js` | avatar grande del especialista en su ficha | `inicialAvatar(...)` |

La regla vive en **`src/panel/inicial.ts`** (nuevo). En `app.js` hay un **espejo** de 9 líneas
con un comentario que lo dice: la PWA es estática, sin compilador, y no hay forma de compartir
código con el servidor sin inventar un paso de build. Si alguien cambia la regla, tiene que
cambiarla en los dos.

**De paso:** los círculos `.ava` ahora llevan `aria-hidden="true"`. La inicial es decoración —
el nombre está al lado — y sin eso un lector de pantalla leía "P, Práctica libre".

### Tests

- `src/panel/inicial.test.ts` (9 casos, emoji de verdad): el caso roto, emoji compuestos
  (bandera, familia, tono de piel, 🏋️, ☺️), la demostración de que `[...nom][0]` los parte,
  otros alfabetos (ñ, Á descompuesta, Дмитрий, 中), números y signos, vacíos, y que el
  resultado es **siempre un solo grafema**.
- `src/panel/api.test.ts`: un test de punta a punta — un chat llamado "🏋️ Práctica libre"
  sale de `GET /api/chats` con `ini: "P"`, y ninguna inicial servida contiene un sustituto
  UTF-16 suelto.

### Comprobado contra los datos vivos

```
antes:  128 chats servidos · 49 iniciales rotas
ahora:  128 chats servidos ·  0 iniciales rotas
🏋️ Práctica libre → P     🎬 Replay: Claudio → R     ☺️😉😁😊 → ☺️  (entero, con color)
```

---

## 4. La regla de oro: el escritorio no se movió

El otro agente cambió `tokens.css` e `index.html` mientras yo trabajaba, así que una foto de
"antes" tomada al empezar habría mezclado sus cambios con los míos. Para aislar **solo lo
mío**: dejé el `tokens.css`/`index.html` de él tal como están, cambié **únicamente `app.js`**
por su versión anterior, fotografié, lo devolví, fotografié otra vez, y comparé píxel a píxel
con PIL.

```
foto              píxeles distintos
agentes-1024              0
agentes-1440              0
caminos-1024              0
caminos-1440              0
chats-1024                0
chats-1440                0
diseno-1024               0
diseno-1440               0
hoy-1024                  0
hoy-1440                  0
modulos-1024              0
modulos-1440              0
TOTAL                     0
```

Tiene sentido: `role`, `tabindex` y `aria-*` no pintan nada, y el anillo de foco solo aparece
con `:focus-visible`, o sea con el teclado, nunca con el mouse.

**El único píxel del escritorio que sí cambia es el arreglo mismo.** Hice la prueba aparte
(servidor viejo vs servidor nuevo, misma vista Chats a 1440): **210 píxeles**, todos dentro de
un cuadrado de 16×16 en `(264,556)-(280,572)` — el dibujo dentro de un círculo de avatar, el
del chat `☺️😉😁😊`, que pasa de un `☺` gris descolorido al `☺️` de verdad. Nada más se movió.
Y la geometría es idéntica: 98 filas, alturas {63, 83} px, avatares 32×32 px, alto total de la
lista 6391 px — antes y después. No podía ser de otra forma: `.ava` es
`width:32px;height:32px;flex:none`, así que lo que haya adentro no puede empujar nada.

Fotos y recortes: `…/scratchpad/kb-antes-mismocss/`, `…/kb-final/`, `…/kb-avatar/`
(`fila-antes.png` y `fila-despues.png` son el mismo avatar ampliado ×3).

---

## 5. Archivos tocados

| Archivo | Qué |
|---|---|
| `dixdybot/src/panel/inicial.ts` | **nuevo** — la regla de la inicial, con la decisión escrita |
| `dixdybot/src/panel/inicial.test.ts` | **nuevo** — 9 casos con emoji de verdad |
| `dixdybot/src/panel/consultas.ts` | 2 líneas: importa y usa `inicial()` |
| `dixdybot/src/panel/api.test.ts` | 1 test de punta a punta + `ini` en el tipo de la respuesta |
| `dixdybot/panel/pwa/app.js` | `activable()`, foco/cerco/Escape de los flotantes y del peek, 10 sitios cableados, 3 avatares, `aria-hidden` en `.ava` |

**No tocados:** `tokens.css`, `index.html`, el bot vivo, la instancia del cliente. Ningún `git`.

## 6. Lo que dejo propuesto (no hecho)

1. **Dos líneas en `tokens.css`** para que las tarjetas puedan ser `<button>` de verdad:
   `.bloque, .conv, .tarjk, .ag-item { display:block; width:100%; text-align:left; }`.
   Con eso el HTML mejora y el dibujo no cambia.
2. **Roving tabindex en la lista de Chats** (108 paradas es mucho tabular).
3. **El panel del camino no existe en el teléfono** (`.peek` está en `display:none` bajo
   900 px): con el teclado ya se llega a la tarjeta, pero no hay dónde ver lo que abre.
