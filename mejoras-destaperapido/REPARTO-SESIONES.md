# Reparto de sesiones — cómo avanzar dixdybot en varios chats sin pisarse

**Creado:** 25-jul-2026 · **Para:** cualquier sesión de Claude Code que vaya a tocar el molde
`SaSS/DIXDY/dixdybot/`. Léelo ANTES de empezar, junto con `DIXDYBOT-ESTADO.md`.

## La regla de oro

El reparto **NO es por tema** ("tú los cobros, yo los seguimientos"). Es **por archivos**.
Dos sesiones que editan el mismo archivo se pisan: la segunda en guardar borra a la primera
y ninguna se entera. Antes de abrir una sesión nueva, mira la tabla de archivos puente y
confirma que nadie más los tiene tomados.

## Archivos puente (los que casi todo toca)

| Archivo | Qué es | Piezas que lo tocan |
|---|---|---|
| `src/index.ts` | cableado del arranque | P1, P3, P7, P10 |
| `src/core/escritor.ts` | el único escritor | P7, P8, P9, P12, P16 |
| `src/db/esquema.sql` | las 6 tablas núcleo | P7, P11, P12 |
| `src/modulos/indice.ts` | registro de módulos | P1, P7, P8, P9, P14 |
| `src/panel/api.ts` | API del panel | P8, P10, P11, P15, P16 |
| `src/panel/consultas-registradas.ts` | registro de métricas | P8, P9 |
| `src/canales/factory.ts` | switch de canales | P1, P14 |
| `tests/arranque.test.ts` | integración | casi todas |

**Ventaja del diseño:** las migraciones NO viven en un archivo común — cada módulo lleva las
suyas en su `modulo.ts` y se enganchan en `indice.ts`. Dos piezas que crean **tablas nuevas**
no chocan. Solo chocan si tocan las 6 tablas núcleo (`esquema.sql`).

## Las piezas pendientes

| # | Pieza | Carpeta propia | Archivos puente que toca |
|---|---|---|---|
| ~~P1~~ | ~~adaptador `wa-baileys`~~ ✅ | `src/canales/wa-baileys/` | factory, indice |
| ~~P2~~ | ~~trasplante legado del emisor (Bad MAC, outbox)~~ ✅ | ídem P1 | — (va con P1) |
| ~~P4~~ | ~~`cli/vincular.ts`~~ ✅ | `cli/` | — |
| ~~P5~~ | ~~huecos del migrador (dudas del vivo)~~ ✅ | `src/modulos/migrador/` | — |
| P6 | MANUAL.md + cutover launchd | raíz | — (va al final) |
| ~~P3~~ | ~~compuerta `gating`~~ ✅ | `src/core/` + `src/modulos/gating/` | index.ts, api, consultas-reg |
| P7 | módulo `ficha` (bautizo + etiquetas, G3+G4) | `src/modulos/ficha/` | esquema, escritor, indice, index |
| P8 | módulo `seguimiento` (G6) | `src/modulos/seguimiento/` | indice, consultas-reg, api, escritor |
| P9 | módulo `cobros` (separar de embudo) | `src/modulos/cobros/` | escritor, indice, consultas-reg |
| P10 | `conexiones/` con permiso (G21) | `src/conexiones/` | **index, llm, orquestador, api** |
| P11 | buscador FTS5 del panel (G25) | `src/panel/buscar.ts` | **esquema**, api, consultas |
| P12 | deltas G2+G5+G8 (no leído, silencio, enseñanzas) | — | **esquema, escritor, api, ledger** |
| P13 | completar `wa-cloud` (media, plantillas, ventana) | `src/canales/wa-cloud/` | **ninguno** ✅ |
| P14 | Instagram DM + CTWA | `src/canales/ig/` | factory, indice (depende de P13) |
| P15 | onboarding de negocio nuevo | `src/panel/` | api (depende de P7) |
| P16 | Ley 21.719 ARCO+P (**dura: 1-dic**) | `src/panel/` | api, escritor |

## Tandas seguras

- **Tanda A (ahora):** `P1+P2+P4` en UNA sesión (misma carpeta, no se pueden separar) ‖
  `P13` ‖ `P5`. Cero colisiones entre las tres.
- ~~**Sacar sola y primero:** `P12`.~~ **CORREGIDO 25-jul** (ver §"Lo que el reconocimiento
  cambió"): P12 ya NO bloquea `esquema.sql` ni va primero.
- **Nunca juntas:** P8 con P9 (chocan en `escritor.ts` y `consultas-registradas.ts`);
  P7 con P10 (chocan en `src/index.ts`); P11 con P12 (chocan en `esquema.sql`).
- **Paralelo permanente:** `P13` no toca ningún archivo puente — corre junto a lo que sea.

## Protocolo de cada sesión

**Al abrir:**
1. Leer `DIXDYBOT-ESTADO.md` y este archivo.
2. Anunciar en la tabla de abajo qué pieza toma (editar este archivo y commitear ANTES de
   empezar, para que las otras sesiones lo vean).
3. `git pull` si hay otra sesión activa.

**Al cerrar:**
1. `pnpm exec tsc --noEmit` y `pnpm exec vitest run` verdes, o no hay commit.
2. Commit con la pieza en el mensaje.
3. Actualizar `DIXDYBOT-ESTADO.md` (qué quedó hecho, qué falta).
4. Liberar la pieza en la tabla de abajo.
5. `python3 /Users/alejandroriveracarrasco/SaSS/DIXDY/scripts/actividad.py`.

**Prohibido siempre:** tocar el bot vivo en `~/SaSS/destaperapido/whatsapp-bot/` (es lo que
vende hoy, solo lectura) y meter datos de cliente en el molde.

## Lo que el reconocimiento del 25-jul cambió (leer ANTES de tomar P7, P11 o P12)

Cuatro lectores independientes + un crítico que fue al código a arbitrar. Lo que sigue está
verificado contra el código y contra la base VIVA, no deducido de un documento.

### 🚨 Regla nueva: NUNCA agregar una columna a `src/db/esquema.sql`

Es el error más caro que puede cometer una sesión acá, porque **pasa todos los controles y
revienta en producción**:

- `abrirDb` ejecuta `esquema.sql` entero en cada arranque, pero todo son `CREATE TABLE IF
  NOT EXISTS`. Si la tabla YA existe, SQLite **ignora la definición nueva en silencio**
  (comprobado: exit 0 y `PRAGMA table_info` sigue devolviendo las columnas viejas).
- Los tests usan bases nuevas en `:memory:`, así que la columna sí está ahí → **verde**.
  `tsc` → **verde**. Commit → **verde**.
- La instancia viva (`~/SaSS/destaperapido/dixdybot-data/bot.db`, 186 chats reales) **no la
  tiene**, y la primera consulta que la nombre revienta con `no such column`.
- No existe herramienta de migración que lo salve: en todo `src/` no hay ni un `ALTER
  TABLE` ni un `PRAGMA table_info`, y `esquema_version` lleva congelada en 1.

**La salida que SÍ funciona, y está probada en producción:** tabla lateral en las
`migraciones` del módulo que la necesita (`CREATE TABLE IF NOT EXISTS`, idempotente). La
tabla `pausas` que nació con P3 **llegó a la base viva** por ese camino. Si alguna pieza
necesita de verdad una columna en las 6 tablas núcleo, eso es una **pieza previa propia**
(construir la migración guardada), no un pedazo de P7 ni de P12 — el problema es compartido
y decidirlo dentro de una pieza es construir infraestructura de todos a espaldas de todos.

### Correcciones a la tabla de piezas

- **P12 se achica y deja de ir primero.** La lista canónica G1-G25 vive en un solo archivo:
  `investigacion-dixdybot/ronda8/contrato-backend.md` §4. De sus tres deltas:
  - **G5 (silencio tras el dueño) ya está RESUELTO por P3**, y con mejor diseño que el que
    pedía el contrato: éste quería una columna `bot_silencio_hasta`; `pausas` ya distingue
    `dueno` (30 min) de `takeover` (indefinida) **con motivo y autor**. Agregar la columna
    ahora crearía dos verdades sobre el mismo hecho.
  - **G2 (no leído)** hoy es un sucedáneo DERIVADO (`consultas.ts`) que **miente**: un chat
    que el bot ya contestó nunca aparece como no leído aunque nadie lo haya abierto. No
    tiene NI UN test (único consumidor: `panel/pwa/app.js`). Y **no hay cicatriz que
    trasplantar**: el bot vivo nunca tuvo no-leído. Hay que diseñarlo, no copiarlo.
  - **G8 (enseñanzas)** está entero en el bot vivo (feedback.jsonl → destilación con
    `claude -p` → regla reversible, 3 endpoints, con mutex y escritura atómica). Pero
    **copiarlo tal cual reabre el agujero que costó cerrar**: allá la regla destilada entra
    al prompt SIN pasar por candado, y acá el equivalente es un Camino, que sí lo tiene.
    Esa tensión (instantáneo vs. con candado) se decide ANTES de escribir código.
- **P7 vale menos de lo que parece, y lo roto es otra cosa.** De 186 conversaciones, **170
  ya se muestran con nombre real**; solo 16 caen al número. La lista de chats NO se ve como
  una guía telefónica. Lo que sí está roto: el pipeline nunca llama a `crearContacto`, así
  que **todo chat nuevo va a verse como un número**. Ojo: `MensajeEntrante` **no tiene campo
  de nombre** — arreglarlo pide tocar `src/schemas/canal.ts` (el contrato de canal, del que
  depende P14), no es media hora.

### Dos trampas que pueden costar caro

- **El interruptor `activo` de un canal NO apaga un canal ya conectado.** Solo se lee en
  `factory.ts` al arrancar. Alejandro puede creer que apagó el bot y seguir contestando.
  El interruptor que SÍ manda es `gating.bot_responde` (se lee por decisión).
- **El proceso que corre NO es "el panel": es el bot completo.** `arrancar()` monta base,
  cerebro, orquestador, gating, mensajero, ingesta y canales, y **después** el panel en el
  MISMO proceso. Consecuencias: (1) el cutover **no necesita un .plist nuevo** — es
  agregarle `CANALES` al que ya está cargado; (2) levantar un segundo proceso abriría **dos
  escritores sobre la misma base**.

### Deuda conocida (no bloquea, pero que la próxima pieza no la empeore)

- **`gating.ts` escribe `conversaciones.asignado` con un UPDATE directo** mientras el
  escritor YA expone ese campo en `CambiosConversacion`. Son dos caminos vivos al mismo dato
  de una tabla núcleo — contra la doctrina de 1 escritor. Lo introdujo P3 (mío). Quien toque
  "quién lleva el chat" que lo unifique en vez de sumar un tercer camino.

### El gate de corte no está lejos: está trabado en un punto

Son **5 días** de sombra (no 48 h; el ajuste real está en `gimnasio.json` del clon).
**Dos de las cinco condiciones ya están cumplidas** (tsc y vitest verdes) y nadie lo sabía.
La de sombra va en 0 y **no puede ni empezar**: su servicio no está cargado y cargarlo
cuesta cuota → es una **decisión de plata de Alejandro**, no de código.

## Tablero de piezas tomadas

| Pieza | Sesión | Desde | Estado |
|---|---|---|---|
| **P1+P2+P4** (adaptador wa-baileys, legado del emisor, `cli/vincular.ts`) | sesión del 25-jul | 25-jul | ✅ **hecha** (commit `201b208`) |
| **P5** (huecos del migrador: dudas del vivo + clases de huérfanos) | sesión del 25-jul | 25-jul | ✅ **hecha** (commit `86615eb`) |
| **P3** (compuerta `gating`) | sesión del 25-jul | 25-jul | ✅ **hecha** (commit `6de0907`) |
| **PS** (la salida del panel: enviar, contestar la Duda, entrada de prueba) | sesión del 25-jul | 25-jul | ✅ **hecha** — pieza NUEVA, no estaba en P1-P16 |
| resto | — | — | libre |

> **PS · el panel dejó de ser un espejo** (25-jul). No figuraba en el reparto y era lo único
> que impedía probar el sistema con las manos. `DepsPanel` no recibía el mensajero: había
> **cero rutas de envío** y el composer estaba muerto. Ahora:
> - `POST /api/chats/:convId/enviar` — le escribes tú al cliente. Sale por el **mismo
>   mensajero** que usa el bot (nunca hablándole al canal directo: sería una segunda salida
>   y los ✓✓ del hilo dejarían de significar lo mismo) y **dispara `duenoIntervino`**:
>   escribir desde el panel es entrar al chat, igual que desde el teléfono.
> - `POST /api/dudas/:id/responder` y `/decidir` — el bucle junior→senior, cerrado. En
>   `decidir` **primero sale al cliente y después avanza la fase**: `check1_listo` significa
>   literalmente "el cliente ya tiene su respuesta"; si el envío se cae, devuelve 502 y la
>   duda NO avanza. `referencia: null` es honesto, no un pendiente.
> - `POST /api/simular/entrante` — escribirle al bot como si fueras un cliente, detrás del
>   ajuste `panel.entrada_de_prueba` (**apagado por defecto**). Recorre el pipeline COMPLETO
>   sin vincular un WhatsApp de verdad.
> - `GET /api/chats/:id` ganó **`puedeEnviar`**, para que el composer sepa antes de intentar.
>
> **Para el front:** los 5 endpoints están arriba con su forma exacta. Todos devuelven
> `{ok:false, error}` legible; el envío devuelve además `entregado` y `motivo` — **guardado
> y entregado no son lo mismo y el panel no debe mostrarlos igual**.
>
> 16 tests nuevos (765 en total), las 5 mutaciones deliberadas cayeron donde correspondía.

> **P1** liberó `src/canales/factory.ts` y `src/modulos/indice.ts`. **Ojo para P14
> (Instagram):** el `switch` de `factory.ts` ya tiene su `case 'wa-baileys'` como molde a
> copiar, y `OpcionesFabrica` ganó `rutaDatos` (lo usan los canales que guardan sesión).
>
> **P3** liberó `src/index.ts`, `src/panel/api.ts` y `src/panel/consultas-registradas.ts`.
> Lo que dejó cambiado y hay que saber antes de tocar esos archivos:
> - **El pipeline ya NO es lineal.** `atenderMensaje` persiste, pasa por la compuerta y
>   **agenda**; el turno corre después, dentro de `gating.agendar(...)` y serializado por
>   chat con `colaDeTurnos`. Cualquier pieza que quiera meterse "después del cerebro" va
>   DENTRO de ese callback, no debajo de `atenderMensaje`.
> - **`MensajeEntrante` ganó `propio`** (`src/schemas/canal.ts`): el mensaje lo escribió el
>   dueño desde la cuenta del negocio. Todo canal nuevo (P14) debe marcarlo — y descartar
>   siempre el eco de sus propios envíos, que es otra cosa.
> - **`Canal.contactoEscribiendo?()`** es opcional: si el canal no expone presencia, la
>   compuerta no espera. No lo inventes.
> - **`ContextoConsulta` ganó `ahora`** (epoch ms) para métricas de ESTADO, no de día.
> - **Nace la tabla `pausas`** (migración del módulo gating). Es la única verdad sobre qué
>   chats están tomados a mano; `conversaciones.asignado` la refleja y ya no es una columna
>   huérfana. P7/P8/P12 no deberían escribirla por su cuenta.
> - **`wa-baileys.ignorar_propios` ya no existe:** es `escuchar_al_dueno` (sentido inverso).

> P1 liberó `src/canales/factory.ts` y `src/modulos/indice.ts`. **Ojo para P14
> (Instagram):** el `switch` de `factory.ts` ya tiene su `case 'wa-baileys'` como molde a
> copiar, y `OpcionesFabrica` ganó `rutaDatos` (lo usan los canales que guardan sesión).
