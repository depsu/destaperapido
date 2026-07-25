# Regresión visual del panel — 25-jul-2026

Comparación contra la foto del antes (`visual-base.md`, misma noche). Recorrí las 6 vistas a
1440, 1024 y 390, en claro y en oscuro, con el MCP de Playwright, y además comparé **píxel a
píxel** cada foto nueva contra su gemela de la línea base.

- **Panel:** `http://127.0.0.1:8793` — **vivo y sano** todo el rato (no se cayó).
- **Fotos nuevas:** `/private/tmp/claude-501/…/scratchpad/visual-nuevo/` (49 PNG, mismos
  nombres que la base + los nuevos que abajo se explican).
- **Consola del navegador: CERO mensajes** en toda la sesión (`all:true`, nivel `debug`), igual
  que la línea base. **Cero errores nuevos.** Las 48 llamadas a la API devolvieron 200.
- **Arreglé un roto nuevo** (el motivo cortado en el popup de "sin monto"); está abajo con foto
  del antes y del después. `npx tsc --noEmit` limpio y `npx vitest run` verde: **37 archivos,
  581 pruebas**.

---

## 0. AVISO IMPORTANTE: los datos se movieron a media sesión

A las **10:31:14** otro proceso escribió en la base (`bot.db-wal` y `migrar-huerfanos.jsonl`
tienen esa hora; el panel arrancó a las 10:13). El titular pasó solo, sin que nadie tocara el
front, de:

```
$2.370.001 (18 de 20 pedidos abiertos) · 2 sin monto por confirmar     ← 10:16 (estado A)
$5.275.000 (22 de 23 pedidos abiertos) · 1 sin monto por confirmar     ← 10:33 (estado B)
```

y **`108 chats` pasó a `98 chats`**. Eso NO es una regresión del front: es la migración de
huérfanos que corrió en paralelo. Lo digo porque, mirando solo pantallas, parece que
desapareció un número.

**Todas las fotos comparables las tomé antes de las 10:31**, o sea en el estado A — el mismo que
describe el encargo (20 pedidos, 2 sin monto, 108 chats). La comparación es limpia. Aparte dejé
cuatro fotos etiquetadas `-datos-b` para dejar constancia del estado nuevo.

---

## 1. Antes → después, vista por vista

| Vista | Antes (línea base) | Después | Veredicto |
|---|---|---|---|
| **hoy** | `$2,4M` · `en juego hoy` · 108 chats · 0 cotizaciones · 0 turnos del bot · "Sin decisiones pendientes" + botón Ver chats | Lo mismo **más** un chip ámbar tocable `2 sin monto` pegado a "en juego hoy". Ni un número perdido: 108/0/0 siguen ahí | **CAMBIA — a mejor.** El diff son 6.937 px (0,54 %) y todos dentro del recuadro del chip |
| **chats · lista** | 3 columnas 340/560/300, mismos chats | **Píxel por píxel IDÉNTICA** a 1440 claro y a 390 claro (diff = 0) | **IGUAL** |
| **chats · hilo** | burbujas, chip `pendiente bot`, ficha, "Escribir desde el panel llega con S3" | Idéntica salvo el anillo de foco del menú (28×36 px) que la base traía por haber hecho clic con el mouse | **IGUAL** |
| **chats · tablero** | `Cotizando 13 · $1,7M` · `Por confirmar 1 · $1` · `Por entregar 6 · $665mil` · `Cobrado 0` | Los cuatro totales intactos **más** un chip `1 sin monto` en Cotizando y otro en Por entregar | **CAMBIA — a mejor, con un detalle feo** (ver N2) |
| **caminos** | Cajones `Apertura` · `Cotización` · `Soporte`, 3 caminos, `0 usos · nuevo` | Cajones **renombrados y con descripción**: `Primer contacto` / "Saludar y entender qué necesita", `Cotización` / "Dar el valor con el tarifario en la mano", `Después de cotizar` / "Dudas de lo ya enviado, recordatorios y postventa". Siguen siendo 3 caminos, mismos textos, mismos `0 usos · nuevo`. Pestañas `Todos·3 · Ventas·2 · Soporte·1` y chip `30 borradores` sin cambio | **CAMBIA — a mejor**, con un texto que se corta en el teléfono (N3) |
| **caminos · popup de borradores** | `24 listos · 6 con avisos · 0 rechazados`, 24 premarcados, candado 59,8 ms | `17 listos · 13 con avisos · 0 rechazados`, 17 premarcados, candado ~30 ms. **Bloque nuevo**: "Caminos repetidos que conviene juntar" con botón `Juntarlos en uno`. Total 30, rigor `declarada`, tope 50: iguales | **CAMBIA — a mejor** (ver juicio en §3) |
| **modulos** | 12 módulos, 2 apagados, 4 grupos | **Píxel por píxel IDÉNTICA** a 1440 claro y a 390 claro | **IGUAL** |
| **agentes** | 184 derivados, gate 4, ficha de Ventas | **Píxel por píxel IDÉNTICA** a 1440 claro y a 390 claro | **IGUAL** |
| **diseno** | 18 colores, 8 tipografías, 31 componentes, 2 "le falta", 6 reglas | **Píxel por píxel IDÉNTICA** a 1440 claro y a 390 claro-top; los conteos de `/api/diseno` calzan uno a uno | **IGUAL** |

**Las tres vistas que quedaron IGUAL de verdad (diff = 0 píxeles): Módulos, Agentes y Diseño.**
Chats también, salvo el anillo de foco de la base. Eso es información: la tanda no se filtró a
ninguna vista que no le tocaba.

### Lo que buscaba primero: ¿desapareció algo?

**No.** Revisé uno por uno los números literales que dejó anotados la línea base: `$2,4M`,
`108 chats`, `0 cotizaciones`, `0 turnos del bot`, `Sin decisiones pendientes`, `Ver chats`,
`13 · $1,7M`, `1 · $1`, `6 · $665mil`, `Cobrado 0`, `Todos·3 / Ventas·2 / Soporte·1`,
`30 borradores`, `Borradores por revisar · 30`, `rigor: declarada`, `tope: 50`, 12 módulos con
2 apagados, `184 derivados`, `gate 4`, 18 colores / 8 tipografías / 31 componentes / 2 huecos /
6 reglas. **Están todos.** Ninguna lista quedó vacía, ninguna vista en blanco, ningún botón
perdido. Los únicos números que cambiaron son los que la tanda cambió a propósito (24/6 → 17/13
avisos) y los que movió la migración de las 10:31 (§0).

---

## 2. Rotos NUEVOS

### N1 — El "por qué" del pedido sin monto salía cortado ✅ ARREGLADO

En el popup del chip, el motivo se pintaba con `.meta-f`, que es de **una sola línea con puntos
suspensivos**. Con el motivo corto ("nadie le puso monto todavía") no se notaba; en cuanto el
servidor devolvió el motivo largo se veía así, **incluso en un monitor de 1440**:

```
Alejandro
no encontré una cifra que pueda dar por buena: ni la ficha del chat ni lo q…
```

Medido: 603 px de texto en 428 px de caja (y 214 px en el teléfono). La explicación completa
quedaba solo en el atributo `title` — o sea, en el globo del mouse, que en un celular **no
existe** (es el defecto 11 de la línea base repitiéndose en sitio nuevo). El popup promete
"no les inventé un valor" y justo la razón era lo que no se leía.

**Arreglo:** cambié esa línea de `.meta-f` a `.cuerpo-n` en `panel/pwa/app.js` (función
`abrirSinMonto`). `.cuerpo-n` ya existe en `tokens.css` (línea 276) y está pensada
precisamente para el cuerpo de texto **dentro de un `.flotante`**, que es exactamente donde
vive este popup. Cero estilos nuevos, cero `<style>`, cero clases inventadas.

- Antes: `hoy-sinmonto-1440-claro-datos-b.png` y `hoy-sinmonto-390-claro-datos-b.png`
- Después: `hoy-sinmonto-1440-claro-arreglado.png` y `hoy-sinmonto-390-claro-arreglado.png`
- Comprobado corriendo: `scrollWidth 428 / clientWidth 428 → cortado: false`.
- `tsc` limpio · `vitest` 581/581 verde.

### N2 — La cabecera "Por entregar" del tablero ahora se parte en dos líneas

El chip `1 sin monto` cabe en `Cotizando` pero no en `Por entregar`: la cabecera pasó de 17 px
a **35 px de alto** y queda desalineada con las otras tres columnas ("Por" / "entregar" en una
línea, "6 ·" / "$665mil" en otra). **No desborda ni se corta nada** — es fealdad, no pérdida de
información, y pasa igual a 1440 y a 390.
Foto: `chats-tablero-1440-claro.png`. *No lo toqué*: arreglarlo pide una regla de layout que
`tokens.css` no tiene todavía.

### N3 — En el teléfono, la descripción del tercer cajón de Caminos se corta

Las descripciones de grupo son texto nuevo. Dos caben; la tercera no:

```
Dudas de lo ya enviado, recordatorios y p…
```

Medido a 390: 286 px de texto en 252 px de caja. Se corta con puntos suspensivos (no desborda),
pero el dueño pierde el final en el celular. Misma raíz que el defecto 4 y el 5 de la línea
base: `.meta-f` nace `white-space:nowrap` (`tokens.css:90`).
Foto: `caminos-390-claro.png` y `caminos-390-oscuro.png`.
**No lo arreglé y explico por qué:** aquí `.cuerpo-n` no sirve — está scopeada a `.flotante` y
este texto vive en la cascada. No hay ninguna otra clase en `tokens.css` que dé texto chico,
apagado y que envuelva. La cabecera del propio archivo manda: *"si algo falta, se agrega EN el
prototipo primero"*. Ruta corta: agregar al prototipo congelado una variante de `.meta-f` que
envuelva, y recién ahí usarla.

### N4 — El chip funciona, pero en el teléfono aterriza en una vista rota

Toqué el chip a 390, se abrió el popup, toqué la fila y me llevó al chat correcto (verificado
con `German Sanchez · Colina` y con `Alejandro`). **El chip hace exactamente lo que promete.**
Pero al llegar a Chats en el teléfono, el hilo mide 74 px de ancho: es el **defecto 2 de la
línea base**, que ya existía. Lo anoto porque el chip nuevo crea un camino nuevo hacia él: hoy
ese recorrido "titular → chip → arreglar el monto" **no se puede completar desde el celular**.
No es culpa de esta tanda, pero sube la urgencia del defecto 2.
Foto: `hoy-sinmonto-vachat-390-claro.png`.

---

## 3. El chip "2 sin monto": ¿se entiende?

Lo toqué a 1440 y a 390. Funciona en los dos:

- **Abre** un popup titulado `2 sin monto por confirmar` con las dos filas
  (`German Sanchez · Colina` y `Alejandro`), cada una con su motivo y un chip `ver chat`.
- **Cierra** con la ✕ de la esquina, y también al tocar una fila.
- **Lleva al chat correcto**: verificado con los dos.
- **A 390 entra completo** en pantalla, sin desbordes, con las filas tocables.
- El chip mismo, a 390, **baja solo** a la línea de abajo de "en juego hoy" y se ve entero
  (no se corta como el chip de borradores de Caminos).

**Se entiende.** La frase de cierre del popup — *"No les inventé un valor: la cifra grande suma
solo lo que sí se pudo confirmar"* — dice en una línea lo que un dueño necesita saber. Dos
peros de redacción, chicos: el chip dice "2 sin monto" pero el popup dice "2 sin monto **por
confirmar**" (dos nombres para la misma cosa), y `ver chat` está pintado como chip, que en el
resto del panel es una etiqueta que no se toca, no un botón.

---

## 4. Los 13 avisos ámbar de Caminos: juicio, no solo medición

Texto literal de tres, tal como se leen en pantalla:

> ⚠ se pisa con 'cam-ubicacion-especial': los dos arrancan casi con lo mismo (50% parecido) — el
> tuyo dice "La comuna no está en ninguna zona del tarifario" y el otro "La comuna no aparece en
> las zonas del tarifario"

> ⚠ se pisa con 'cam-precio-kit-completo': los dos arrancan casi con lo mismo (89% parecido) —
> el tuyo dice "Ya están comuna, cantidad y tiempo" y el otro "Ya están comuna, cantidad y
> tiempo en la conversación"

> ⚠ en medio de este camino el bot te pregunta a ti antes de seguir

**¿Se leen enteros?** Sí. Ni uno se corta, en ningún ancho: envuelven en varias líneas dentro de
su fila, a 1440 y a 390.

**¿Se distingue el ámbar del verde de un vistazo?** Regular. La única marca de color es un punto
de **8×8 píxeles**. El texto del aviso está en el mismo gris apagado que el resto de la ficha
(`rgb(92,105,99)` en claro, idéntico a las otras líneas). O sea: **el problema no es que el
ámbar grite demasiado, es que casi no se ve**. Para encontrar los 13 hay que leer línea por
línea la frase "se puede aprobar — mira el aviso". Lo digo como juicio de diseño, no como falla
medida.

**¿En oscuro el ámbar es legible?** **Sí, y bien.** La línea base avisó que el ámbar sobre fondo
oscuro suele quedar ilegible; lo medí ahora que hay 13 y **no pasa**: el chip `⚠ 13 con avisos`
da **6,91:1** de contraste (`#E09A4B` sobre `#291E10`) y el punto ámbar **8,09:1** sobre el
fondo del popup. Los dos por encima de 4,5:1. El aviso de la base no se cumple aquí.

**¿Se volvió un muro de ámbar?** **No.** 13 puntitos de 8 px entre 17 verdes no son un muro.

**El problema real de la vista es otro, y es de largo:** el popup mide ahora **4.528 px de alto
en una ventana de 808** — unas **5,6 pantallas** de scroll para revisar 30 borradores, con la
barra de Aprobar pegada abajo todo el rato. En el teléfono son **7.362 px en 752**: casi **10
pantallas**. Aprobar en lote 30 caminos desde el celular hoy es un ejercicio de paciencia. Los
avisos no lo causaron solos (sumaron 24 líneas nuevas), pero lo empujaron. Si esto va a crecer,
lo que pide la vista es plegar cada fila, no más color.

**Un detalle de lenguaje que sí molesta:** de los 24 avisos, **18 muestran un id interno** tipo
`'cam-precio-kit-completo'`. El dueño no sabe qué es eso. Está a un paso de estar bien: el
aviso ya cita las dos frases enfrentadas, que es lo que de verdad se entiende; sobra el id.
(Es texto del servidor — **no lo toqué**.)

---

## 5. ¿Los textos nuevos desbordan a 390?

Medí el contenido real de las 6 vistas a 390 (no el `scrollWidth` del documento, que miente
porque `body` lleva `overflow:hidden`):

| Vista | Contenido / hueco a 390 | ¿Cambió respecto de la base? |
|---|---|---|
| hoy | 377 / 334 · `.heroline` 345 / 270 | **Idéntico.** El chip baja de línea, no ensancha nada |
| chats | 416 / 390 | Idéntico |
| caminos | 454 / 390 | Idéntico |
| modulos | 390 / 390 (única sana) | Idéntico |
| agentes | 424 / 390 | Idéntico |
| diseno | 928 / 334 | Idéntico |

**Ningún texto nuevo agrandó el desborde de ninguna vista.** Lo único que se pierde en el
teléfono es lo del N3 (una descripción de cajón, cortada con puntos suspensivos) y lo que ya
arreglé en el N1.

---

## 6. Lo que vi de paso y no es mío para arreglar (servidor)

1. **La tarjeta de "Esperan tu decisión" se vio por primera vez** (con los datos nuevos de las
   10:31; la línea base nunca tuvo decisiones pendientes). No es de esta tanda — el molde ya la
   traía — pero conviene saber cómo se ve: a **390 el texto queda en una columna de 102 px de
   ancho y la tarjeta mide 719 px de alto**, casi una pantalla entera para una sola decisión.
   Además el resumen mete el pedido completo donde debería ir una frase corta, arranca con
   `San Bernardo` (una comuna, no un nombre) y trae un punto doble ("…solo se succiona y
   limpia.."). Fotos: `hoy-1440-claro-datos-b.png`, `hoy-390-claro-datos-b.png`.
2. **Un pedido "sin monto" cuya ficha sí muestra un precio.** Al abrir `German Sanchez · Colina`
   desde el chip, el popup decía "nadie le puso monto todavía" y la ficha de al lado mostraba
   `precio clp 170000`. (Ya se resolvió solo con la migración de las 10:31, que le puso 270.000
   — lo dejo anotado por si el criterio vuelve a discrepar.)
   Foto: `hoy-sinmonto-vachat-1440-claro.png`.
3. **El nombre del cajón y el de la pestaña ya no coinciden**: la pestaña dice `Soporte · 1` y
   el cajón donde cae ese camino ahora se llama `Después de cotizar`. Es correcto (son cosas
   distintas: agente vs grupo), pero al ojo parece un error.

---

## 7. Lo que toqué

Un solo archivo, una sola línea de verdad (más su comentario):

- `/Users/alejandroriveracarrasco/SaSS/DIXDY/dixdybot/panel/pwa/app.js` — función
  `abrirSinMonto`: el motivo del pedido pasa de `class="meta-f"` a `class="cuerpo-n"`.

Nada más. No toqué `tokens.css`, no toqué el servidor, no toqué el bot vivo, no hice git, no
reinicié el panel (el servidor sirve `panel/pwa/` directo del disco, así que el cambio se ve
recargando).
