# Robustez S4 — atacando el resolvedor de montos, el guardia, los grupos y la fusión

Ronda 11 · 2026-07-25 · agente de robustez (trabaja EN CONTRA de lo recién construido).
Todo lo que dice este informe está **corrido**, no leído: cada hallazgo trae el comando o el
dato real con el que se reprodujo. Lo teórico va marcado como teórico y **no** se cuenta.

Estado de partida verificado: panel arriba en `http://127.0.0.1:8793` (`/api/salud` → ok),
`tsc` limpio, 569 tests en 37 archivos. Al cerrar: `tsc` limpio y **581 tests verdes**
(6 nuevos míos, cada uno comprobado en ROJO revirtiendo su arreglo a mano; el resto del delta
viene de otra sesión que también está tocando el repo).

---

## Resumen para Alejandro (sin tecnicismos)

- El panel mostraba **$2.370.001**. Después de esta ronda muestra **$5.275.000** con 22 de
  23 pedidos. Faltaban dos cosas: una ya estaba arreglada en el código pero **nadie había
  vuelto a correr la copia** de la historia del bot viejo, y la otra era un error nuevo que
  escondía un pedido entero de $285.000.
- El error nuevo era el más feo de todos: el sistema **escondía la plata justamente cuando
  la cotización que salió era más precisa**. Con una cotización vaga el pedido quedaba con
  su monto; con la cotización buena, quedaba en blanco.
- El guardia que pregunta por los precios ridículos podía dejar el buzón lleno de preguntas
  **para siempre** (22 medidas), sin ninguna forma de cerrarlas. Ahora se caen solas cuando
  dejan de tener sentido.
- La pregunta que te hace el guardia te mentía sobre tus propios precios: te decía que el
  piso de tu tabla eran $20.000 cuando lo más barato que vendes son $80.000.
- Juntar caminos repetidos podía meter texto **que nadie revisó** dentro de un camino que ya
  le habla a los clientes. Ahora no: sin la firma del candado, no se junta.

---

## 1 · ARREGLADOS (con test que se pone rojo sin el arreglo)

### 1.1 🔴 La plata se escondía cuando la cotización era DEMASIADO precisa

**Archivo:** `/Users/alejandroriveracarrasco/SaSS/DIXDY/dixdybot/src/modulos/migrador/monto.ts`

El resolvedor aceptaba dos lecturas para la cifra que salió al cliente: que fuera el **total**
de la ficha, o que fuera el **valor por unidad**. Faltaba la tercera, que es igual de legítima:
el **subtotal** (unitario × cantidad) de antes de sumarle el traslado y los cobros aparte.

Caso real de la instancia (chat de un evento en Huechuraba, 3 unidades):

| fuente | cifra |
|---|---|
| ficha: `precio_clp` 85.000 · `cantidad_banos` 3 · `flete_clp` 30.000 | 285.000 |
| 1ª cotización que salió | 85.000 (el unitario) |
| 2ª cotización que salió (la última, la buena) | 255.000 (= 85.000 × 3) |

Resultado antes del arreglo: `monto = null`, motivo *"lo que salió al cliente dice $255.000 y
la ficha da $285.000: no sé cuál es el monto de verdad"*. Y lo perverso, medido:

```
envío 85.000  → monto 285.000   (cotización vaga: SÍ hay plata)
envío 255.000 → monto null      (cotización precisa: NO hay plata)
```

Más información daba menos plata. Arreglo: `CandidatoFicha` ahora expone `subtotal` y `calza`
lo acepta como tercera lectura conciliable. Una **cuarta** cifra sigue dejando el monto en
null, como manda la doctrina.

- Impacto medido HOY: 1 pedido de 23, **$285.000** que estaban invisibles.
- Tests: `el envío que trae el subtotal (sin traslado) NO es un desacuerdo` y
  `más información no puede dar MENOS plata` en `monto.test.ts`.

### 1.2 🟠 El guardia del absurdo podía dejar el buzón con preguntas eternas

**Archivo:** `.../src/modulos/migrador/espejo.ts`

Reproducido de punta a punta contra los datos reales, sobre una copia de la instancia:

```
minimo_pct_tabla = 999  → plata: 0 con monto · 23 sin monto · 22 preguntas abiertas
minimo_pct_tabla = 25   → plata: 22 con monto ·  1 sin monto ·  0 preguntas
                          …y las 22 preguntas viejas SEGUÍAN 'pendiente' en la base
```

Es decir: dejar el ajuste mal puesto **una sola corrida** ensuciaba el buzón para siempre. El
espejo nunca cerraba sus propias preguntas y el panel **no tiene ningún endpoint para
responder o descartar una duda** (verificado: las rutas del panel son solo `/api/caminos*`,
`/api/hoy`, `/api/chats*`, `/api/tablero`, `/api/modulos`, `/api/agentes`, `/api/gimnasio/*`),
así que nadie podía sacarlas de ahí.

Arreglo: el espejo **cierra sus propias preguntas** cuando el monto de ese pedido deja de ser
absurdo (marca `migracion:monto-bajo-tabla` + `pedidoId`). Solo toca las que siguen
`pendiente`: si el dueño ya empezó a contestarla, es suya. Sale en el parte de la corrida
(`dudasCerradas`) — nada en silencio.

Medido después del arreglo, sobre la misma copia sucia: `21 pregunta(s) mía(s) se cayeron
solas`, y quedó **1 pendiente**, la del pedido anotado en $1, que sigue siendo rara de verdad.

- Test: `la pregunta del guardia se CAE SOLA cuando el monto deja de ser absurdo`.

### 1.3 🟠 La fusión de caminos activaba contenido que nadie revisó

**Archivo:** `.../src/panel/api-caminos.ts` (`POST /api/caminos/fusionar`)

`proponerFusiones` conserva el `estado` del camino base. El endpoint publicaba el resultado
directo, con el comentario *"sigue en borrador — el candado se corre después, al aprobar"*:
eso es cierto **solo si el base es un borrador**. Si el base ya está **activo** y absorbe un
borrador, los disparadores, las relaciones y las pruebas de un camino que nadie revisó entran
a un camino que ya le habla a los clientes, **saltándose el candado** (`verificarParaActivar`),
que es el único control que existe.

- Impacto HOY: no reproducible en la instancia (los 3 gemelos detectados —
  `cam-precio-kit-completo` + 2 — son los tres borradores). Pero pasa a ser el caso **normal**
  apenas Alejandro apruebe el lote de 30 (tarea #9 pendiente): ahí toda fusión futura tendrá
  base activo.
- Arreglo: si el resultado queda `activo`, corre el MISMO candado que `/estado`; si no firma,
  devuelve 409 con los motivos en castellano y **no fusiona nada**.
- Test: `si el camino que queda sigue ACTIVO, el candado corre igual: sin firma no hay fusión`
  (usa un borrador con una prueba dorada fantasma; sin el arreglo el endpoint responde 200 y
  el camino vivo se queda con el texto sin revisar).

### 1.4 🟡 La pregunta le mentía al dueño sobre su propia tabla

La duda decía: *"ni se acerca al **piso de tu tabla** ($20.000)"*. Pero $20.000 no es el piso
de su tabla: es el 25 % de lo más barato que vende ($80.000 en el tarifario del clon). Le
estaba informando mal sus propios precios, que es exactamente lo que este proyecto no puede
hacer. Ahora dice: *"no llega ni al 25 % de lo más barato de tu tabla ($80.000)"* —
`MontoAbsurdo` lleva las dos cifras separadas (`piso` = la raya, `barato` = la tabla, `pct`).

- Verificado en la instancia real: la duda `ockbe` que vive hoy en el buzón ya trae la
  frase honesta.
- Test: el assert del mensaje en `el monto disparatado se pregunta en vez de guardarse`.

### 1.5 🟡 La traza no cuadraba con el monto si un cargo venía en negativo

Con `flete_clp: -50.000` (un descuento anotado así) el monto era 150.000 y la fórmula guardada
en la ficha decía `la ficha del chat: $100.000 x 2` → 200.000. El dueño no puede auditar una
cifra cuya explicación da otro número. Ahora se muestran todos los términos distintos de cero,
con su signo. (Hoy no hay negativos en los datos: 0 de 35 fichas. Es la traza la que mentía,
no el monto.)

- Test: `la fórmula CUADRA con el monto aunque un cargo venga en negativo`.

### 1.6 🟡 Una pregunta que no se podía hacer mataba la migración entera

`abrirDuda(...)` quedaba **fuera** del `try`: solo el INSERT estaba protegido. Si el generador
de códigos se queda sin códigos libres (`codigoUnico` lanza a los 50 intentos), la corrida
entera moría a mitad y los pedidos que venían después no se migraban. Ahora todo el bloque va
adentro: se anota el huérfano y la migración sigue.

- Test: `si no puede hacer UNA pregunta, la migración sigue` (sin el arreglo, el test explota
  con `ErrorDuda`).

---

## 2 · ATACADO Y NO CAYÓ (lo que aguantó)

- **Grupo que ya no existe en la lista (punto 3 del encargo).** Comprobado de verdad, no en
  teoría: `/api/caminos` mete los caminos de un cajón desconocido en su propio grupo, lo manda
  **al final** y lo marca `enLista: false`; `panel/pwa/app.js` pinta el chip
  *"fuera de tu lista"*. Los borradores del destilador se listan **planos** (sin agrupar), así
  que tampoco desaparecen. Además hay test previo (`un grupo que ya no está en la lista se
  muestra igual, al final y marcado`). Los 30 borradores reales usan 10 cajones, todos en la
  lista, y `grupo_nuevo` viene vacío: nadie pidió cajones nuevos.
- **Fusión reversible (punto 4).** Los absorbidos quedan `retirado`, nunca borrados, y
  `POST /api/caminos/:id/estado {estado:'borrador'}` los devuelve a la lista (hay test).
  **No se pierde ninguna prueba dorada**: se suman por id, se deduplican y las que faltaban en
  el ajuste se guardan al pool. Caveat honesto y ya documentado en la respuesta del endpoint:
  deshacer **no** le quita al base los disparadores que se llevó; eso queda a mano.
- **Idempotencia del espejo.** Dos corridas seguidas sobre los datos reales: `0 creados ·
  0 movimientos · 0 preguntas`, mismo total. Tres corridas, misma base.
- **Ajuste negativo.** `minimo_pct_tabla: -5` → no corre y lo dice en simple: *"El ajuste de
  'migrador' … no sirve: monto.minimo_pct_tabla: Too small: expected number to be >=0"*. Nada
  se escribe a medias (el guardado del panel es atómico: temporal + rename).
- **Casos límite del encargo:** 0 pedidos (corre limpio, todo en cero) · cantidad `0`, `2.5`,
  `"tres"`, `-2` (los cuatro → sin monto **con motivo legible**, jamás un número) · cobro
  aparte sin cifra (sin monto, nombrando el cobro) · dos notas de entrega distintas (gana la
  última, que es la regla declarada) · nota que contradice la ficha (gana la nota: es el
  documento de cierre).
- **Administrabilidad (punto 5).** Ningún umbral nuevo quedó cableado: el subtotal usa
  `tolerancia_pct` y el cierre de preguntas no tiene número propio. Verificado corriendo el
  MISMO binario contra tres `data/ajustes/migrador.json` distintos (25 / 999 / 0) → tres
  conductas distintas, cero cambios de código.
- **Datos de destaperapido en el molde (punto 6).** Grep sobre `src cli panel plantillas data
  config.example.env`: las únicas apariciones son (a) fixtures marcados como tales
  (`cotizador.fixture.ts`, `personas.fixture.ts`, `solape.fixture.ts` — con cabecera "no es
  config de producción ni el default del molde"), (b) tests, y (c) comentarios. Los defaults
  del molde son genéricos (`TARIFARIO_EJEMPLO` con "Comuna A/B", `GRUPOS_EJEMPLO` sin una
  palabra del rubro, `PERSONAS_MOLDE` con teléfonos sintéticos). `data/` del molde solo tiene
  `.gitignore`. **Limpio.**

---

## 3 · ABIERTO (reportado, NO arreglado — decisión o diseño)

1. **El guardia mira solo el piso, nunca el techo.** Un `precio_clp` de 170.000.000 entra sin
   chistar y le infla el hero al dueño; el mismo guardia que caza $1 no ve $170 millones.
   No lo arreglé porque un techo honesto necesita una decisión tuya (un pedido grande de
   verdad puede ser de varios millones) y un ajuste nuevo. Hoy no hay ningún monto así en los
   datos (el mayor es $450.000). **Impacto hoy: cero; riesgo: un dedo torpe del extractor.**
2. **La pregunta del monto no tiene dónde aterrizar.** Si mañana respondes *"vale $120.000"*,
   la Duda produce un **camino**, no el monto del pedido; y hoy ni siquiera hay endpoint para
   responderla (el panel dice, honestamente, *"responder llega con S3"*). El arreglo 1.2 al
   menos hace que la pregunta se caiga sola si el monto se corrige por otro lado. Queda para
   S3/S5: que una duda de dominio `migrador` escriba el `monto_neto`.
3. **Extras duplicados se suman dos veces.** Confirmado en el resolvedor (dos "ducha" de
   100.000 → 200.000). **No lo toqué a propósito:** deduplicar por nombre inventaría un número
   más bajo cuando el cliente sí arrendó dos duchas. En los datos reales no hay ni un caso
   (0 de 35 fichas). Lo dejo dicho, no arreglado.
4. **Ficha con solo traslado y sin unitario** (`flete_clp` sin `precio_clp`): se descarta antes
   de mirarla y el motivo dice *"ni la ficha … guardaron un valor claro"*, que es falso —
   la ficha sí guardó el traslado. **Teórico**: 0 de 35 fichas. No lo cambié porque hacerlo
   contar puede volver `null` un caso que hoy sí da monto (chocaría con el precio del envío):
   el arreglo prudente es solo el texto del motivo, y prefiero que lo decida quien siga.
5. **Apagar el guardia (`minimo_pct_tabla: 0`) puede QUITAR plata.** Medido: con el guardia
   encendido, 21 pedidos con monto; apagado, 20. Con el guardia, el precio de $1 se descarta y
   manda la ficha ($120.000); sin guardia, el $1 compite con la ficha, no calzan y el pedido
   queda sin monto. Es coherente con "ante la duda, nada", pero es lo contrario de lo que
   espera quien apaga un guardia. Es un tema de documentación del ajuste, no de código.
6. **`"= $270.000.- neto"` no calza** el patrón por defecto de la nota (el `.-` chileno).
   Cae de vuelta a la ficha, así que no inventa nada, y el patrón es configurable
   (`patron_neto_nota`). Menor.
7. **5 de los 30 borradores tienen dominio sin especialista** (`general` ×3, `agenda` ×2,
   contra `ventas`/`soporte` en el ajuste de agentes). No desaparecen —la cascada "Todos" los
   muestra y la selección por palabras clave igual los alcanza—, pero no aparecen bajo ninguna
   pestaña de agente. Vale la pena mirarlo al aprobar el lote.

---

## 4 · Efecto en la instancia (lo que se corrió de verdad)

Se volvió a correr el espejo sobre la instancia del cliente
(`/Users/alejandroriveracarrasco/SaSS/destaperapido/dixdybot-data`) — solo lectura del bot
vivo, nunca escritura. Respaldo del `bot.db` anterior en el scratchpad de la sesión.

```
antes:  $2.370.001 (18 de 20 pedidos abiertos) · 2 sin monto
después: $5.275.000 (22 de 23 pedidos abiertos) · 1 sin monto · 1 pregunta en el buzón
```

El único pedido sin monto es honesto: no hay ninguna cifra en su historia
(*"ni la ficha del chat ni lo que salió guardaron un valor claro"*). La única pregunta abierta
es la del pedido anotado en $1.

**No se tocó** el bot vivo (`~/SaSS/destaperapido/whatsapp-bot`), no se hizo git, no se
reinició el panel y no se aplicó ninguna fusión ni aprobación de caminos (eso es de Alejandro,
tarea #9).

## 5 · Archivos tocados

- `src/modulos/migrador/monto.ts` — tercera lectura (subtotal), traza que cuadra, `MontoAbsurdo`
  con la tabla y el %.
- `src/modulos/migrador/espejo.ts` — cierre de las propias preguntas, mensaje honesto,
  `abrirDuda` dentro del `try`, `dudasCerradas` en el parte.
- `cli/migrar.ts` — el parte dice cuántas preguntas se cayeron solas.
- `src/panel/api-caminos.ts` — el candado corre si la fusión deja un camino activo.
- `src/modulos/migrador/monto.test.ts` (5) y `src/panel/api-caminos.test.ts` (1) — 6 tests
  nuevos, cada uno verificado en rojo revirtiendo su arreglo a mano.
