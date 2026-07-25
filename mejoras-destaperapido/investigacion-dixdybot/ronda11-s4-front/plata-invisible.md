# La plata invisible del panel — informe (2026-07-25)

**Tarea #10.** El panel abría con `$2.370.001 en juego (20 pedidos abiertos)`. Ese titular
mentía por dos motivos distintos y el `.001` del final era la pista. Este informe cuenta qué
encontré de verdad en los datos (no lo que decía el encargo), qué construí y qué pasa con
los 20 pedidos reales, con números antes y después.

---

## 1 · Lo que verifiqué a mano (y dónde el diagnóstico previo no daba)

Leí los datos reales del bot vivo (`whatsapp-bot/data/`, solo lectura) y la base de la
instancia. Tres correcciones al diagnóstico de entrada:

**(a) German Sánchez — Fluintek, Colina — $270.000 que valían $0. Confirmado, pero la causa
NO era la que se creía.** Su plata **no está en el registro `confirmacion`**: ese registro
solo trae `{correoId, asunto, faltan}` — nunca tuvo un campo `precio`. Los $270.000 están en
dos lugares:

- la **ficha** del extractor (`datos-lead.json`): `precio_clp: 170000`, `cantidad_banos: 1`,
  `extras: [{"ducha portátil", 100000}]` → 170.000 + 100.000 = **270.000**;
- la **nota de entrega**, que lo dice con todas sus letras:
  `(baño $170.000 + ducha portátil $100.000 = $270.000 neto + IVA = $321.300)`.

El espejo perdía esa plata porque `espejo.ts` solo leía `detalle.precio` de registros de tipo
`cotizacion` y **jamás miraba la ficha ni los extras**. Ese es el bug real.

**(b) El pedido de $1 — Oscar Pontigo, Vitanova, San Bernardo. Confirmado, con un matiz.**
El registro del bot vivo dice literalmente `"precio": 1`, y el formulario que lo causó ya está
arreglado en el bot vivo (`dashboard.mjs`, comentario sobre la línea 1200 — lo leí, no lo
toqué). Pero **hoy los $120.000 NO están en `extras`**: la ficha actual dice
`precio_clp: 120000`, `extras: null` (la re-analizó la IA el 23-jul, tres días después de la
cotización). O sea: el $1 vive solo en el libro histórico de envíos.

**(c) El caso de $255.000 = 3 × $85.000 es real y es peor de lo que parecía.** La ficha de
ese chat trae además `flete_clp: 30.000`, así que da **$285.000**, mientras el envío guardó
**$255.000**. Las dos cifras son defendibles y no calzan: ese pedido **no puede tener monto**
sin adivinar.

**(d) Bonus que encontré verificando:** el campo `precio_clp` del bot vivo es **por unidad**,
y el espejo lo guardaba como si fuera el total. Por eso 18 pedidos tenían un monto que era el
valor de UN baño en pedidos de 2, 3, 4 y 5 baños. Esa era la mayor pérdida de todas, y no
estaba en el encargo.

---

## 2 · Qué construí

### 2.1 `src/modulos/migrador/monto.ts` — el resolvedor honesto (nuevo, puro)

Una sola regla decide la plata de cada pedido migrado, con esta prioridad:

1. **La nota de entrega**, si declara el total ya cerrado (`= $270.000 neto`). Manda sobre
   todo: es el documento de cierre, escrito después de la ficha, y nombra la cifra sin la
   ambigüedad unidad-vs-total. (Caso real: una ficha decía $160.000 y su nota $190.000 porque
   el aseo acordado se pactó al despachar y nunca volvió a la ficha. La nota tenía razón.)
2. **La ficha**: `unitario × cantidad + cobros aparte + traslado` — la misma fórmula que usa
   el propio bot vivo (`integracion.js`), así que no es un criterio inventado por mí.
3. **Lo que salió al cliente** (el precio de un envío), cuando no hay ficha con qué armarlo.

Y ante la duda, **nada**:

| Situación | Qué hace |
|---|---|
| El envío dice una cifra que no es ni el total ni el unitario de la ficha | `monto: null` + motivo |
| Un cobro aparte viene sin valor ("ducha portátil" sin cifra) | `monto: null` + motivo |
| No se sabe la cantidad y el ajuste pide ser estricto | `monto: null` + motivo |
| No hay ninguna cifra que dar por buena | `monto: null` + motivo |

El motivo se escribe **en la ficha del pedido** (`monto_por_confirmar`) en castellano de
persona. Cuando sí hay monto, se guarda además **cómo salió** (`monto_origen`:
`"la ficha del chat: $170.000 + $100.000 aparte"`), así el número queda auditable sin abrir
el bot viejo. Los dos nombres viven en `src/schemas/embudo.ts` para que quien escribe
(migrador) y quien muestra (embudo) no puedan desincronizarse.

### 2.2 El hero dice la verdad

`enJuegoHoy` ya no suma los pedidos sin monto como si valieran cero. Devuelve
`{ total, cantidad, conMonto, sinMonto[], texto }` y el titular pasa de
`$2.370.001 (20 pedidos abiertos)` a `$2.370.001 (18 pedidos abiertos) · 2 sin monto por
confirmar`. En el panel, el "**2 sin monto**" es un `chip draft` tocable al lado de la cifra
grande: abre un flotante con los pedidos, su motivo, y al tocar una fila salta a ese chat.
Solo clases que ya existen en `tokens.css` (`fila`, `crece`, `titulo-f`, `meta-f`, `chip
draft`, `panelcard`, `vacio`), cero estilos nuevos.

### 2.3 Un monto absurdo levanta una duda, no entra callado

Si el monto queda ridículamente bajo **tu tabla**, el sistema pregunta en vez de guardarlo.
La vara sale del tarifario del cotizador (`pisoTarifario()` = la fila más barata, en pesos) y
el umbral es config: `minimo_pct_tabla`, por defecto **25%** — prudente, solo caza el
disparate, nunca una rebaja real. La pregunta usa el **buzón que ya existe**
(`core/duda-motor.ts` → `abrirDuda` → `escritor.crearDuda`): aparece en "Esperan tu decisión"
de Hoy y se puede responder por el código de 5 letras. **No hay ningún canal de avisos nuevo.**
Es idempotente: la duda lleva una marca en su snapshot, así que la segunda corrida del espejo
no vuelve a preguntar.

### 2.4 Todo administrable (checklist #1)

`ConfigMigrador.monto` (Zod, editable desde la vista Ajustes del panel o
`data/ajustes/migrador.json`): `campo_unitario`, `campo_cantidad`, `campo_extras`,
`campo_extra_valor`, `campo_extra_nombre`, `campo_flete`, `campo_precio_envio`,
`campo_resumen_envio`, `tipos_con_precio`, `patron_neto_nota`, `sin_cantidad`,
`extra_sin_valor`, `solo_envio`, `tolerancia_pct`, `minimo_pct_tabla`.

Los nombres de campo son config **porque tienen que serlo**: `cantidad_banos` es del rubro de
destaperapido y el molde no puede saberlo. El molde trae `cantidad` genérico; el clon lo
apunta a lo suyo en `dixdybot-data/ajustes/migrador.json` (ya escrito, 4 líneas).

---

## 3 · Verificación con los datos reales

Sobre una **copia** de `dixdybot-data` en el scratchpad y un **snapshot de solo lectura** del
`data/` del bot vivo. Nada vivo fue tocado.

### 3.1 El titular

| | antes | después |
|---|---|---|
| Hero | `$2.370.001 (20 pedidos abiertos)` | `$4.990.000 (21 pedidos abiertos) · 2 sin monto por confirmar` |
| Pedidos abiertos | 20 | 23 (el bot vivo creó 3 más desde la última migración) |
| Con monto | 18 | 21 |
| Sin monto | 2 (sin explicación) | 2 (**con motivo escrito**) |
| Dudas en Hoy | 0 | 1 |

**Comparación limpia sobre los MISMOS 20 pedidos** (los 3 nuevos aparte):
total **$2.370.001 → $4.180.000**, con 18 con monto y 2 sin monto en ambos lados — pero no
son los mismos dos, y esa es la gracia.

### 3.2 Pedido por pedido (los 20 que el panel muestra hoy)

```
   cotizando       sin monto →   sin monto  (repartidor)        SIN MONTO: no encontré una cifra que pueda dar por buena
-> cotizando        $255.000 →   sin monto  Benja               SIN MONTO: lo que salió al cliente dice $255.000 y la ficha da $285.000
-> por-entregar      $75.000 →    $150.000  Huechuraba          la ficha del chat: $75.000 x 2
-> por-entregar    sin monto →    $270.000  German Sanchez      la nota de entrega: $270.000 neto
   cotizando        $100.000 →    $100.000  Renca               la ficha del chat: $100.000
   por-entregar     $160.000 →    $160.000  Colina              la nota de entrega: $160.000 neto
-> cotizando         $80.000 →    $400.000  Colina              la ficha del chat: $80.000 x 5
   cotizando        $160.000 →    $160.000  La Florida          la ficha del chat: $160.000
-> cotizando        $180.000 →    $450.000  Colina              la ficha: $180.000 x 2 + $60.000 aparte + $30.000 de traslado
-> por-confirmar          $1 →    $120.000  San Bernardo        la ficha del chat: $120.000   ← + DUDA por el $1
-> cotizando         $80.000 →    $360.000  Ñuñoa               la ficha del chat: $80.000 x 4 + $40.000 aparte
-> por-entregar      $80.000 →    $160.000  Colina              la nota de entrega: $160.000 neto
-> cotizando        $130.000 →    $260.000  Raul                la ficha del chat: $130.000 x 2
   por-entregar     $190.000 →    $190.000  Buin                la ficha del chat: $190.000
-> cotizando        $150.000 →    $300.000  Quilicura           la ficha del chat: $150.000 x 2
   cotizando        $200.000 →    $200.000  (sin ficha)         lo que salió al cliente: $200.000
-> cotizando        $160.000 →    $260.000  (sin nombre)        la ficha del chat: $160.000 + $100.000 aparte
-> cotizando         $80.000 →    $320.000  Renca               la ficha del chat: $80.000 x 4
   cotizando        $130.000 →    $130.000  Pintando            la ficha del chat: $130.000
-> por-entregar     $160.000 →    $190.000  Vitacura            la nota de entrega: $190.000 neto
```

Los tres pedidos que el bot vivo creó después de la última migración entran ya con monto:
$450.000, $180.000 y $180.000.

### 3.3 Los dos que quedan sin monto — y por qué está bien

1. **Benja · Huechuraba** — `lo que salió al cliente dice $255.000 y la ficha da $285.000: no
   sé cuál es el monto de verdad`. Antes tenía $255.000 *por casualidad* (era el último
   `precio` del envío). Hoy el sistema admite que no sabe y te lo muestra en el titular: se
   arregla en 5 segundos abriendo el chat desde el chip.
2. **El chat del repartidor (+56930153632)** — `no encontré una cifra que pueda dar por buena:
   ni la ficha del chat ni lo que salió guardaron un valor claro`. Su única nota dice
   `COBRAR AL CLIENTE: $160.000` **sin decir si es neto o con IVA** y sin ficha detrás.
   Deliberadamente no lo adiviné. *(Ojo: este "pedido" es un artefacto del bot viejo — una
   entrega manual registrada contra el jid del propio repartidor, no un cliente. Vale la pena
   sacarlo del tablero a mano.)*

### 3.4 La duda que se levantó

```
[código de 5 letras] pendiente · San Bernardo
  falta: el precio que traía ($1 en lo que salió al cliente) ni se acerca al piso de tu
         tabla ($20.000)
  pregunta: ¿cuánto vale de verdad? No lo guardé con esa cifra.
  snapshot: {origen:"migracion:monto-bajo-tabla", pedidoId:"p-mig-mrtpp44h-1ebd4a",
             valor:1, piso:20000}
```

El $1 **no se guardó**. El pedido tomó los $120.000 de su ficha, que es lo que sí se pudo
confirmar, y la duda queda esperando el OK de Alejandro en Hoy.

### 3.5 Idempotencia (sigue intacta)

Segunda corrida sobre la misma copia: `0 nuevas · 0 insertados · 0 creados · 0 movimientos ·
0 fichas al día · 0 dudas`. Correrlo N veces = mismo estado, incluido el buzón.

---

## 4 · Tests

`src/modulos/migrador/monto.test.ts` (nuevo, 22 tests, fixtures sintéticos genéricos):

- **Un registro ambiguo NO recibe monto inventado** — envío $300.000 vs ficha $100.000 →
  `monto: null`, `formula: null`, motivo con las dos cifras. Además: la misma cifra puede ser
  el unitario o el total (las dos lecturas valen), una tercera no.
- **Administrabilidad del umbral, dos valores → dos conductas** — `minimo_pct_tabla: 25`
  (default) → el $1 levanta duda y no se guarda; `minimo_pct_tabla: 0` → el mismo $1 entra sin
  preguntar. Y al revés: `minimo_pct_tabla: 200` hace dudar de un monto que antes pasaba.
- Más: `sin_cantidad` y `solo_envio` como dos ajustes → dos conductas; extras sumados; precio
  en un registro que no es `cotizacion`; la nota de entrega manda; el buzón idempotente
  (dos corridas = una pregunta); `enJuegoHoy` y `GET /api/hoy` sirviendo el "N sin monto"
  tocable (verificado **en proceso** con `app.request()`, sin levantar servidor ni navegador).

**Estado: `npx tsc --noEmit` limpio · `npx vitest run` 32 archivos / 496 tests verdes.**

---

## 5 · Archivos tocados

| Archivo | Qué |
|---|---|
| `dixdybot/src/modulos/migrador/monto.ts` | **nuevo** — el resolvedor puro + `ConfigMonto` + `netoDeNota` + `pisoDeTabla` |
| `dixdybot/src/modulos/migrador/monto.test.ts` | **nuevo** — 22 tests |
| `dixdybot/src/modulos/migrador/espejo.ts` | usa el resolvedor, marca la ficha, abre la duda idempotente, reporta `montos` |
| `dixdybot/src/modulos/migrador/modulo.ts` | `ConfigMigrador.monto` |
| `dixdybot/src/schemas/embudo.ts` | `CAMPO_SIN_MONTO` / `CAMPO_ORIGEN_MONTO` (contrato compartido) |
| `dixdybot/src/modulos/embudo/consultas.ts` | `enJuegoHoy` con `conMonto` + `sinMonto[]` + texto honesto |
| `dixdybot/src/modulos/cotizador/consultas.ts` | `pisoTarifario()` — la vara del guardia sale de TU tabla |
| `dixdybot/src/panel/consultas-registradas.ts` | `ValorMetrica.sinConfirmar` |
| `dixdybot/src/panel/api.ts` | `/api/hoy` sirve `sinConfirmar` |
| `dixdybot/panel/pwa/app.js` | chip "N sin monto" en el hero + flotante con motivos (solo clases de `tokens.css`) |
| `dixdybot/cli/migrar.ts` | pasa el piso del tarifario y la config de dudas; imprime la línea "plata" |
| `destaperapido/dixdybot-data/ajustes/migrador.json` | **nuevo** (instancia) — `campo_cantidad: "cantidad_banos"` |

No se tocó el bot vivo, ni el módulo caminos, ni el gimnasio.

---

## 6 · Lo que queda para Alejandro

1. **Correr el espejo sobre la instancia real** para que el panel tome los montos nuevos:
   `node cli/migrar.ts --vivo ~/SaSS/destaperapido/whatsapp-bot/data --datos
   ~/SaSS/destaperapido/dixdybot-data`. Es idempotente y no le escribe nada al bot vivo. No lo
   corrí yo: la verificación se hizo sobre una copia, como pedía el encargo.
2. **Responder la duda del pedido de San Bernardo** ($1 → ¿$120.000 por limpieza?).
3. **Decidir el de Benja**: ¿$255.000 o $285.000 (con el traslado)?
4. **Sacar del tablero** el "pedido" que es en realidad el chat del repartidor.
5. Si el titular queda demasiado optimista, el ajuste está a mano: `sin_cantidad: "ambiguo"`
   y `solo_envio: "ambiguo"` dejan sin monto todo lo que no esté probado, y el hero lo dirá.
