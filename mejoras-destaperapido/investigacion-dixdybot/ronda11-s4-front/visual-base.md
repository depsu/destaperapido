# Foto del panel ANTES de tocarlo — 25-jul-2026

Constancia visual del panel del dueño tal como se ve hoy, con los datos reales de
destaperapido, antes de que nadie lo modifique. No cambié ni una línea de código: solo miré,
medí y fotografié.

- **Qué fotografié:** `http://127.0.0.1:8793` (servicio vivo del panel), datos reales.
- **Cuándo:** 25-07-2026, entre las 05:30 y las 06:40.
- **Con qué:** Chromium por el MCP de Playwright. El tema lo forcé con
  `document.documentElement.dataset.theme = 'dark' | 'light'`, que es la palanca que el propio
  `tokens.css` deja para que mande el visor (líneas 25 y 33).
- **Dónde quedaron las fotos:** `/private/tmp/claude-501/-Users-alejandroriveracarrasco-SaSS-DIXDY-clientes-destaperapido/5acfd0ef-e8b4-49b2-965d-26a7a76d1c5b/scratchpad/visual-base/`
  (39 PNG, nombre `<vista>-<ancho>-<tema>.png`).
- **Estado en que dejé el navegador:** vista Hoy, sub-vista Lista, sin popups abiertos, sin
  tema forzado. Nada quedó a medias.

---

## 1. Qué muestra cada vista de verdad (números que se leen en pantalla)

### Hoy — con datos
Titular de plata **`$2,4M`** / `en juego hoy`. Al lado, tres métricas chicas: `108 chats`,
`0 cotizaciones`, `0 turnos del bot`. Debajo, la sección "Esperan tu decisión" **vacía**:
`Sin decisiones pendientes` + un botón `Ver chats`. Media pantalla a la derecha queda en blanco.

### Chats — con datos, dos sub-vistas
- **Lista:** 3 columnas (lista 340 px · hilo 560 px · ficha 300 px). La lista trae los chats
  reales con su último mensaje (JB Montaje Industrial, Michelle, Samu, Ale, Caro, Perfumes,
  Sebastian, Alejandro, Benja · Huechuraba, Oscar Pontigo, Fabiii…). Sin chat elegido, el hilo
  dice `Elige un chat` y la ficha queda **completamente vacía** (300 px de blanco).
  Al abrir un chat: burbujas reales, chip `pendiente bot`, ficha con `Aún sin datos extraídos`
  y un campo de escribir con el texto `Escribir desde el panel llega con S3` (apagado).
- **Tablero:** 4 columnas — `Cotizando 13 · $1,7M`, `Por confirmar 1 · $1`,
  `Por entregar 6 · $665mil`, `Cobrado 0` (vacío). 13+1+6 = los 20 pedidos del titular.

### Caminos — casi vacía arriba, llena abajo
Pestañas `Todos · 3` · `Ventas · 2` · `Soporte · 1` y, a la derecha, el chip ámbar
`30 borradores`. En la cascada solo hay **3 caminos activos** (Apertura, Cotización, Soporte),
todos con `0 usos · nuevo`. El campo de la guía está apagado con el texto
`La guía llega con el asistente — por ahora se administra desde aquí`.
Al abrir `30 borradores`: `Borradores por revisar · 30`, con **24 listos · 6 con avisos ·
0 rechazados**, el candado corrió en `59.8 ms`, `rigor de pruebas: declarada`, `tope por
lote: 50`, y 24 casillas premarcadas.

### Módulos — con datos
12 módulos, **2 apagados** (verificado contra `/api/modulos`): "Atiende de a poco mientras
aprende" (`rampa`) y "Atiende por WhatsApp oficial (Meta)" (`wa-cloud`). Los otros 10 encendidos,
en 4 grupos: Venta, Operación, Canales y "Base — siempre encendidos" (esos últimos con punto
verde en vez de interruptor).

### Agentes — con datos
Recepción: `Derivación silenciosa · 184 derivados · 0 dudas hoy`. Dos especialistas: **Ventas**
(punto verde) y **Soporte** (punto ámbar). Gimnasio: `Prácticas · gate 4`. La ficha de Ventas:
`2 caminos`, `— nota del juez`, `0 chats`, `0 dudas abiertas`, gate `Todavía no ha practicado ·
nota — · mínimo 4 para atender clientes`, personalidad `Cercana` + `Nunca inventa`, y
`Todavía no ha practicado en el gimnasio`.

### Diseño — llena, es el catálogo
**18 fichas de color** (17 colores + la sombra `flot`) con nombre + hex + para qué sirve (los
hex **se recalculan solos** con el tema: en oscuro muestra `#0E100F`, en claro `#FAFBFA`),
**8 tamaños de tipografía** y **31 fichas de componente** (contados contra `/api/diseno`), cada una con su nombre de clase copiable
(`pto ok`, `chip vivo`, `tag`, `origen-chip cam`, `obj`, `btn p`, `btn s`, `gchip`, `sw`,
`mini`, `buscador`, `composer`, `g-input`, `panelcard`, `fila`, `titulo-f`, `meta-f`,
`crece`…). Todos los componentes renderizan; el único que no se ve es la sombra (ver defecto 14).
Al final trae dos secciones más: **`Le falta al sistema · 2`** (el propio catálogo declara sus
huecos: *"estado deshabilitado del botón"* y *"campo de texto suelto"*) y `Reglas`, con 6 reglas.
Foto: `diseno-1440-claro-fin.png`.

---

## 2. El HERO de Hoy, texto literal (foto del antes)

Lo que se lee en pantalla, exactamente:

```
$2,4M
en juego hoy
```

Y el `title` (globo del mouse) de esa misma cifra, literal:

```
$2.370.001 (20 pedidos abiertos)
```

La API confirma el dato crudo (`GET /api/hoy`):
`{"id":"pedidos-en-juego-hoy","etiqueta":"en juego hoy","tipo":"hero","valor":2370001,
"texto":"$2.370.001 (20 pedidos abiertos)"}`.

**Dónde se esconde la plata (visible en el Tablero de Chats):** de los 20 pedidos, tres no
suman lo que valen — `Alejandro · Arriendo de baño químico` sale con **—** (sin monto) en
Cotizando, `German Sanchez · Colina · Arriendo de baño químico + ducha portátil` sale con **—**
en Por entregar, y `Oscar Pontigo · San Bernardo` está registrado en **$1** en Por confirmar.
Foto: `chats-tablero-1440-claro.png`.

---

## 3. Tabla vista × ancho × tema

Prioricé lo que pidió el encargo; lo que falta lo digo abierto.

| Vista | 1440 claro | 1440 oscuro | 1024 claro | 390 claro | 390 oscuro |
|---|---|---|---|---|---|
| hoy | `hoy-1440-claro.png` | `hoy-1440-oscuro.png` | `hoy-1024-claro.png` | `hoy-390-claro.png` | `hoy-390-oscuro.png` |
| chats | `chats-1440-claro.png` + `chats-hilo-1440-claro.png` + `chats-tablero-1440-claro.png` | `chats-1440-oscuro.png` + `chats-hilo-1440-oscuro.png` | `chats-1024-claro.png` | `chats-390-claro.png` + `chats-tablero-390-claro.png` | — (no tomada) |
| caminos | `caminos-1440-claro.png` + `caminos-borradores-avisos-1440-claro.png` | `caminos-1440-oscuro.png` + `caminos-borradores-1440-oscuro.png` + `caminos-borradores-avisos-1440-oscuro.png` | `caminos-1024-claro.png` | `caminos-390-claro.png` | `caminos-390-oscuro.png` |
| modulos | `modulos-1440-claro.png` | `modulos-1440-oscuro.png` | `modulos-1024-claro.png` | `modulos-390-claro.png` | — (no tomada) |
| agentes | `agentes-1440-claro.png` | `agentes-1440-oscuro.png` | `agentes-1024-claro.png` | `agentes-390-claro.png` | — (no tomada) |
| diseno | `diseno-1440-claro.png` (+ `-b`, `-c`, `-fin` desplazadas) | `diseno-1440-oscuro.png` + `diseno-1440-oscuro-b.png` | `diseno-1024-claro.png` | `diseno-390-claro.png` + `-top` | `diseno-390-oscuro.png` |

Faltan a propósito, por tiempo: los tres 390-oscuro de chats/modulos/agentes y todo el juego de
1024 en oscuro. **A 1024 no hay ningún desborde en ninguna vista** (medido: body 1024/1024 y
`.contenido` 784/784 en las seis), así que ese ancho es el más sano de los tres.

---

## 4. Defectos que YA existen hoy

Numerados por gravedad. Cada uno con cómo reproducirlo.

### 1. En el teléfono, la cuarta métrica de Hoy se sale de la pantalla y no hay forma de verla
`0 turnos del bot` queda dibujado entre los píxeles **399 y 433** de un teléfono de 390 de
ancho: no se ve, y no se puede desplazar hasta él porque el `body` tiene `overflow:hidden`.
La fila `.heroline` mide 345 px dentro de un hueco de 270 px, con `overflow-x: visible`.
**Reproducir:** ancho 390 → vista Hoy → se leen solo tres métricas ($2,4M, 108 chats,
0 cotizaciones). En consola, con la vista Hoy abierta:
`const h=[...document.querySelectorAll('.heroline')].find(x=>x.offsetParent); [h.scrollWidth, h.clientWidth]`
→ `[345, 270]`, y la última métrica termina en el píxel 433 de una pantalla de 390.
**Foto:** `hoy-390-claro.png`. *Confirmado.*

### 2. En el teléfono, la vista Chats es inusable: el hilo queda en 74 px de ancho
El `@media (max-width:900px)` encoge la barra lateral y esconde `.ctx`, pero **no toca
`.sublay`**: la lista se queda en 260 px y el hilo recibe los 74 px que sobran. "Elige un chat"
se parte en tres líneas y el botón `Enviar` queda medio cortado en el borde.
Medido: `lista-conv 56..316`, `hilo-col 316..390 (74 px)`, `ctx 0 px`.
**Reproducir:** ancho 390 → Chats → mirar la columna derecha.
**Foto:** `chats-390-claro.png`. *Confirmado.*

### 3. En el teléfono, la ficha del agente se sale de la pantalla
Misma raíz que el 2, en la vista Agentes: `ag-lista` ocupa 56..356 y `ag-det` queda en
356..**424** (68 px de ancho, 34 px fuera del teléfono). El dueño no puede ver la nota del
juez ni el gate desde el celular.
**Reproducir:** ancho 390 → Agentes → a la derecha solo se ve una línea vertical y blanco.
**Foto:** `agentes-390-claro.png`. *Confirmado.*

### 4. En el teléfono, el chip "30 borradores" queda cortado y el aviso de la guía se trunca
En Caminos a 390, la cabecera mide 398 px en un hueco de 334 (`overflow-x: visible`, sin
scroll): del chip ámbar solo se alcanza a leer "bo". Y la frase de ayuda (`.meta-f`, que nace
`white-space:nowrap`) mide 578 px en 278 y se corta en "…por ahora los ca…".
**Reproducir:** ancho 390 → Caminos → mirar la esquina superior derecha.
**Foto:** `caminos-390-claro.png`. *Confirmado.*

### 5. En el teléfono, la vista Diseño mide 928 px de ancho: el catálogo del design system se sale
`.contenido` de Diseño tiene 928 px de contenido en 334 de hueco. El culpable es `.specs`:
aunque el `@media (max-width:900px)` de `tokens.css:344` lo pasa a una columna, la columna
resuelve a **896 px fijos** (medido: `grid-template-columns: 896px`), porque el mínimo
automático de `1fr` es el ancho mínimo de las fichas, y dentro de cada ficha hay líneas
`.meta-f` que nacen `white-space:nowrap` (`tokens.css:90`) y no se dejan encoger.
Pista para quien lo arregle: `minmax(0,1fr)` o `min-width:0` en `.spec`.
(El mecanismo exacto — cuál línea manda — **no lo verifiqué al 100%**; el síntoma sí está medido.)
**Reproducir:** ancho 390 → Diseño → bajar hasta "Componentes": las tarjetas se cortan por la
derecha. En consola: `getComputedStyle(document.querySelector('.specs')).gridTemplateColumns`.
**Foto:** `diseno-390-claro.png`. *Confirmado el síntoma.*

### 6. Los botones apagados se ven exactamente igual que los encendidos (botón mentiroso)
`tokens.css` **no tiene ni una regla `:disabled`** (verificado grep). Consecuencias vivas:
- Caminos: `#btn-guia` ("Preguntar") está `disabled=true` pero con `opacity: 1`,
  fondo `rgb(14,122,95)` (el verde del primario) y `cursor: pointer`. Se ve como el botón
  más importante de la vista y no hace nada.
- Chats: el `Enviar` del hilo (`btn s`) también está `disabled=true` con `opacity: 1`.
- La propia vista Diseño lo confiesa: junto a `Aprobar` / `Descartar` / `Sin permiso` dice
  *"primario · secundario · deshabilitado (hoy se ve igual: ver lo que falta)"*, y la ficha
  solo ofrece dos clases copiables (`btn p`, `btn s`): la tercera no existe. Y al final de la
  vista, en "Le falta al sistema", está escrito con todas sus letras: *"tokens.css no tiene
  regla para .btn[disabled] ni .sw con input disabled: un botón apagado se ve igual que uno
  vivo (pasa hoy en el campo de mensaje de Chats)"*. O sea: **el defecto está declarado, no
  descubierto** — lo que aporto es la foto y la segunda instancia (el "Preguntar" de Caminos,
  que además es primario).
**Reproducir:** cualquier ancho → Caminos → apuntar a "Preguntar" y hacer clic: no pasa nada.
**Fotos:** `caminos-1440-claro.png`, `diseno-1440-oscuro-b.png`. *Confirmado.*

### 7. Las tarjetas de camino no se alcanzan con el teclado
En Caminos, el tabulador recorre: 6 botones del menú → `Todos·3` / `Ventas·2` / `Soporte·1` →
`30 borradores` → campo de la guía → `Preguntar`. **Las tres tarjetas de camino no aparecen
nunca**: son `<div class="bloque">` con un `addEventListener('click')` (`app.js:527`), sin
`tabindex`, sin `role`, sin manejo de teclas. Abrir un camino — la acción principal de la
vista — es imposible sin mouse, y un lector de pantalla ni las nombra.
Ojo: el anillo de foco **sí se ve** donde hay foco de verdad
(`:focus-visible { outline:2px solid var(--ac) }`, `tokens.css:346`); el problema no es que el
foco sea invisible, es que no hay foco que poner.
**Reproducir:** Caminos → Tab repetido → contar 12 paradas, ninguna en las tarjetas.
*Confirmado.*

### 8. Con nombres que empiezan con emoji, el avatar sale roto
El chat "🏋️ Práctica libre" muestra un rombo con interrogante. El avatar es literalmente
`"\ud83c"`: media letra. Nace en el servidor, `src/panel/consultas.ts:111` →
`ini: (nom[0] ?? '?').toUpperCase()`, que corta el primer *code unit* UTF-16 en vez del primer
carácter. Arreglo natural: `[...nom][0]`.
**Reproducir:** Chats → mirar el avatar de "🏋️ Práctica libre". En consola:
`document.querySelectorAll('.ava')[6].textContent.codePointAt(0).toString(16)` → `d83c`.
**Foto:** `chats-1440-claro.png`. *Confirmado en el código y en pantalla.*

### 9. En el hilo, quién habló se distingue apenas por dónde está la burbuja
`.bur.cli` usa `--n3` (#E7EBE9) y `.bur.bot` usa `--ac-sub` (#E9F2EE): en tema claro son
prácticamente el mismo gris (relación de contraste entre ambos ≈ 1.03:1). Como los mensajes
largos del bot ocupan todo el ancho y pierden el sangrado, hay burbujas donde no se sabe quién
habló. En oscuro se distinguen algo mejor (#1F2523 vs #122A20, el segundo tira a verde).
**Reproducir:** Chats → abrir "JB Montaje Industrial" → comparar "Al traslado de llevar el
baño…" (bot) con "A qué se refiere con traslados" (cliente).
**Fotos:** `chats-hilo-1440-claro.png` vs `chats-hilo-1440-oscuro.png`. *Confirmado con medición.*

### 10. En la revisión en lote, las filas se meten por debajo de la barra de Aprobar
La barra pegajosa (`position:sticky; bottom:0; background:var(--n1)`) no llega al borde del
panel: por debajo de ella asoma la línea de la fila siguiente ("listo para aprobar · ventas ·
2 ejemplo(s) de conversación"). Pasa igual en claro y en oscuro.
**Reproducir:** Caminos → `30 borradores` → desplazar la lista → mirar bajo los botones.
**Fotos:** `caminos-borradores-avisos-1440-claro.png` y `…-oscuro.png`. *Confirmado.*

### 11. La cifra exacta del titular vive en un `title`: en el celular no existe
`$2,4M` es un redondeo de `$2.370.001` — la pantalla muestra 30 mil pesos de más — y el número
real solo aparece al dejar el mouse encima (atributo `title`). En un teléfono no hay "dejar el
mouse encima": el dueño nunca ve el monto real. Lo mismo con las métricas `cotizaciones` y
`turnos del bot`, cuyo detalle (`turnos 0 · con camino 0 · dudas 0`) también vive en el `title`.
Y los globos propios del panel se pintan con `[data-tip]:hover::after` (`tokens.css:337`), sin
variante de foco: quien navega con teclado tampoco los ve.
**Reproducir:** ancho 390 → Hoy → tocar la cifra: no aparece nada.
*Confirmado (el `title` está; que el teléfono no lo muestre es cómo funciona el navegador táctil).*

### 12. El mismo panel da dos números de chats sin explicar la diferencia
El menú y Hoy dicen `108 chats`; Agentes dice `184 derivados`. La API aclara lo que la pantalla
no: `chatsActivos: 108`, `dormidos: 76` (108+76 = 184). Nadie que mire el panel puede deducirlo.
**Reproducir:** Hoy (108) → Agentes (184). Contraste: `curl -s localhost:8793/api/hoy`.
*Confirmado.*

### 13. A 1440 la mitad derecha de Hoy y Caminos queda en blanco
`.col-centro` tiene `max-width:760px` y va centrado, pero el contenido de Hoy arranca pegado a
la izquierda: en una pantalla de escritorio el titular, las métricas y el bloque de decisiones
ocupan un tercio y el resto es vacío. En Chats, además, la columna `ctx` (300 px) se queda
completamente en blanco mientras no elijas chat.
**Reproducir:** ancho 1440 → Hoy. **Foto:** `hoy-1440-claro.png`. *Confirmado (es diseño, no
error técnico: lo dejo anotado para que se decida a propósito.)*

### 14. Menudencias del design system que ya se cuelan
- `app.js:517` pinta el chip de borradores con estilo en línea
  (`chip.style.cssText = 'border-color:var(--amb);color:var(--amb)'`) en vez de una clase de
  `tokens.css`; en el popup de borradores hay varios `style="margin-bottom:8px"` y
  `style="cursor:default"`. Va contra la regla de "solo clases que existan en tokens.css".
  El propio catálogo ya anota un caso hermano: *"campo de texto suelto: solo hay campos DENTRO
  de un contenedor (.buscador, .composer, .g-input, .resp): para un formulario, la vista
  Módulos los dibuja con estilos a mano en app.js"*.
- En Diseño, la ficha `sombra` no se ve en tema oscuro: es una caja oscura con sombra oscura
  sobre fondo oscuro. Igual la ficha del color `n1` (#0E100F), indistinguible del fondo.
- Las clases de la vista Diseño son texto seleccionable, pero **no hay botón de copiar**: hay
  que seleccionar a mano. No sé si eso importa para el encargo — lo dejo dicho.
*Confirmado lo de los estilos en línea y la sombra; lo del botón de copiar es observación.*

---

## 5. Lo que revisé y NO está roto

- **Consola del navegador: limpia.** Cero mensajes en toda la sesión, en los tres anchos y en
  los dos temas, incluyendo nivel `info` (`browser_console_messages` con `all:true` → 0/0/0).
  No hay ningún error que reportar textualmente porque no hubo ninguno.
- **Scroll horizontal del `body`: no se puede detectar con la prueba clásica.** En las seis
  vistas `document.documentElement.scrollWidth == clientWidth` porque `body` lleva
  `overflow:hidden` (`tokens.css:47`). Midiendo el contenido de verdad a 390:
  `hoy 390/390` pero `.contenido 377/334` · `chats 416/390` · `caminos 454/390` ·
  `modulos 390/390` (única sana) · `agentes 424/390` · `diseno 390/390` pero
  `.contenido 928/334`. O sea: **sí hay desborde en 5 de 6 vistas, solo que clipeado**.
  Quien arregle esto: no confíe en `scrollWidth` del documento, mida los contenedores.
- **El anillo de foco se ve** (2 px de acento con 2 px de separación, `:focus-visible`), en
  claro y en oscuro. El problema del teclado es el defecto 7, no la visibilidad.
- **A 1024 no hay ningún desborde.**
- **Los puntos verde/ámbar/rojo del veredicto se leen bien en oscuro** en el popup de
  borradores (verde `#3BC796`, ámbar `#E09A4B` sobre `#151918`). No encontré ninguno rojo
  porque hoy hay 0 rechazados: **el punto rojo en oscuro queda sin verificar**.
- **Los hex de la vista Diseño se recalculan solos con el tema** (no están escritos a mano).
- **La vista Diseño renderiza los 31 componentes** y todos traen su nombre de clase.

## 6. Cosa que no es defecto pero conviene saber

El Tablero de Chats **sí** se desplaza de lado a propósito (`.board`, `overflow-x:auto`,
1036 px de contenido): a 390 solo se ve la primera columna y hay que arrastrar. No tiene ninguna
señal visual de que se pueda arrastrar. Lo dejo como aviso, no como falla.

Sobre la regla del molde: la vista Diseño usa de ejemplo `Mensual céntrico · $160.000 neto` y
`Mensual periferia · $190.000`. Lo rastreé: salen de `dixdybot/src/panel/diseno.ts` (líneas 74,
238 y 346), que declara en su cabecera que los demos son *"HTML del molde (constantes de este
archivo, no entrada de nadie)"*. **No es una fuga de datos del cliente** — son constantes de
ejemplo, sin nombre, teléfono ni comuna reales. Dicho eso, los montos se parecen mucho al
tarifario de destaperapido; si el molde va a servir a otros rubros, conviene un ejemplo más
neutro. Lo dejo como observación, no como falla.
