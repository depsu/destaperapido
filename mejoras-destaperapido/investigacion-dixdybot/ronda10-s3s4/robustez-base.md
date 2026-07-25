# Auditoría de robustez de producción — dixdybot (base) · 2026-07-24

**Alcance:** `src/core/` (escritor, llm, cola, bus, ledger, config, db), `src/modulos/`
(rampa, cerebro, embudo, cotizador, migrador), `src/panel/`, `src/canales/`, `cli/`.
Ojo adversarial: esto correrá 24/7 con plata real, en el MISMO Mac donde vive el bot vivo.

**Línea base (antes y después de mis arreglos):**
- `pnpm exec tsc --noEmit` → **0** (limpio)
- `pnpm exec vitest run` → **193 passed** (eran 190; +3 tests de mis fixes)
- `node cli/doctor.ts` → esquema + 7 módulos OK

**Restricciones respetadas:** no toqué el proceso del bot vivo, no hice git. Toda función
nueva sigue el checklist de administrabilidad (el techo de concurrencia es config Zod en
`ConfigLLM` + se lee por turno + test de administrabilidad). Cero datos de cliente.

---

## Resumen de veredicto

La base está **notablemente bien construida** para robustez: un solo proceso, un solo
escritor tipado, failover del cerebro tipado con red de seguridad dura, dedup EN el dato
(UNIQUE + INSERT OR IGNORE), ledgers append-only, config validada por Zod antes de escribir,
webhook de Meta con verificación HMAC en tiempo constante, y **el panel corre en el MISMO
proceso que el bot** (no hay carrera cross-proceso entre panel y bot; JS es single-thread y
better-sqlite3 es síncrono → sin lecturas/escrituras a medias entre ambos, y el cache de
`Ajustes` es la misma instancia, así que un guardado desde el panel invalida bien).

Lo que ROMPE en producción se concentra en tres frentes: (1) fallos de disco que descartaban
respuestas buenas, (2) **ausencia de techo de concurrencia** → un pico de chats = un pico de
procesos `claude -p` capaz de voltear el Mac, y (3) el panel **sin autenticación** con un
campo de config que se hace `spawn()` (RCE si el dueño expone `0.0.0.0`). Arreglé (1) y (2)
(críticos/altos y acotados, tests verdes); (3) queda documentado con severidad ALTA porque el
arreglo real (auth) no es acotado y el default (127.0.0.1) lo mitiga.

---

## HALLAZGOS

### [ALTO · ARREGLADO] H1 — Un fallo al persistir `sesiones.json` descartaba una respuesta ya generada del cli
**Dónde:** `src/core/escritor.ts` `persistirSesiones()` (antes L165-168); disparado desde
`src/core/llm.ts` `crearMotorCli.intentar` L391-393 (guarda `session_id` tras un éxito) y
L367-370 (borra sesión muerta).

**Qué rompía:** `persistirSesiones()` hacía `writeFileSync(...)` sin try/catch. Ese guardado
ocurre **después** de que el cli ya devolvió una respuesta buena (y pagada). Si el disco
falla en ese instante (ENOSPC disco lleno, EROFS solo-lectura, EACCES permisos), la excepción
sube por `generar()` → la atrapa el `try` de `turno()` en llm.ts → se clasifica como `'error'`
→ **se degrada al siguiente motor y se tira la respuesta ya buena del cli**. Peor: si el disco
lleno también hace fallar el `ledger.apendear` de `cerrarTurno`, la red de seguridad final
(llm.ts L148, fuera de todo try) puede tirar y hacer que `consultar()` **rechace**, violando
su invariante "JAMÁS rechaza".

**Failure scenario concreto:** disco al 100% (o `data/` montado read-only tras un error de
FS). El cliente escribe, el cli responde perfecto, pero al guardar el `session_id` revienta →
el cliente recibe la respuesta de plantilla ("Dame un momento…") en vez de la real, y el
dueño recibe un aviso de "el cerebro no respondió" que es falso.

**Fix aplicado:** `persistirSesiones()` ahora envuelve el `writeFileSync` en try/catch,
loguea a `console.error` y sigue. `sesiones.json` es estado vivo chico (no es historia, no va
al ledger); perder el id de sesión solo hace que el próximo turno arranque sin `--resume`. Es
**simétrico** a la lectura ya-tolerante del boot (un `sesiones.json` corrupto arranca con
sesiones en cero). La sesión igual queda en RAM para la vida del proceso.

**Test:** `escritor.test.ts` → "si el disco no deja escribir sesiones (ruta imposible), NO
tira: el turno ya respondió" (ruta con padre inexistente → ENOENT → `guardarSesionLLM` no
lanza y la sesión vive en memoria).

---

### [ALTO · ARREGLADO] H2 — Sin techo global de turnos: un pico de N chats = N procesos `claude -p` simultáneos
**Dónde:** `src/core/llm.ts` `crearLlm` / `turno()`; `src/schemas/llm.ts` `ConfigLLM`.

**Qué rompía:** la `cola` (core/cola.ts) serializa FIFO **dentro** de un chat, pero deja
**paralelismo ilimitado ENTRE chats** (claves distintas = cadenas independientes). No había
ningún tope global. Cada turno de un chat distinto spawnea su propio `claude -p` (proceso
pesado en RAM/CPU). En 24/7 real, un pico realista — el poller del buzón de Meta (S5) drena un
backlog tras una caída, o una campaña trae 50 leads nuevos casi a la vez — dispara **decenas o
cientos de `claude -p` a la vez** en el mismo Mac donde vive el bot vivo. Resultado: memoria y
CPU agotadas, el Mac se pone irresponsivo, y caen a la vez el bot, el panel y potencialmente
los otros clientes que corren en la máquina. Es el clásico fork-bomb accidental.

**Failure scenario concreto:** el bot estuvo caído 20 min; 60 clientes distintos escribieron;
al reanudar, el drenaje emite 60 eventos `mensaje` casi sincrónicos → 60 `claude -p` arrancan
juntos → OOM del Mac.

**Fix aplicado (administrable):** agregué `maxTurnosConcurrentes` a `ConfigLLM` (default 6) y
un **semáforo global de traspaso** en la puerta. `turno()` toma un permiso ANTES de spawnear
(`adquirirCupo(config.maxTurnosConcurrentes)`) y lo suelta en un `finally` (pase lo que pase:
éxito, red de seguridad o throw inesperado — nunca se fuga). Los turnos que exceden el tope
esperan su lugar (FIFO). No reemplaza la cola por conversación (esa sigue siendo FIFO por
chat); es el techo ENTRE chats. Sin deadlock: un turno solo espera si `max` turnos están
CORRIENDO (no esperando), y esos terminan y liberan (`max ≥ 1` por schema). Se lee por turno
→ subir/bajar el tope desde `data/ajustes/cerebro.json` sin tocar código ni reiniciar.

**Checklist de administrabilidad:** ✅ configSchema (`ConfigLLM.maxTurnosConcurrentes`), ✅
ajustes sin tocar código (se lee por turno), ✅ aporte — es config del módulo núcleo cerebro
(no pinta UI propia, como el resto de `ConfigLLM`), ✅ test de administrabilidad.

**Test:** `llm.test.ts` → "ADMINISTRABLE: con tope 1, dos chats DISTINTOS se serializan; el
default los deja en paralelo" + "el permiso se suelta aunque el turno reviente (no se fuga
cupo)".

**Nota:** el default 6 es un techo de seguridad, no un cuello de botella; conviene calibrarlo
en la instancia según los cores del Mac y si domina el motor `cli` (pesado) o `api` (liviano).

---

### [ALTO · DOCUMENTADO, no arreglado] H3 — Panel sin autenticación + `ConfigLLM.rutaCli` sin restricción = spawn arbitrario (RCE) si se expone `0.0.0.0`
**Dónde:** `src/panel/api.ts` PUT `/api/modulos/:id` y PUT `/api/modulos` (sin auth);
`src/schemas/llm.ts` `rutaCli: z.string().default('claude')`; usado en `llm.ts` L356
`ejecutar(config.rutaCli, args, ...)` → `spawn(comando, args)`.

**Qué rompe:** ningún endpoint del panel tiene autenticación. El default de `host` es
`127.0.0.1` (seguro), PERO `ConfigPanel.host` permite `'0.0.0.0'` y la doctrina contempla
exponerlo por Tailscale. Con el panel en `0.0.0.0` y sin auth, cualquiera en esa red puede:
- **RCE:** `PUT /api/modulos/cerebro` con `{"rutaCli":"/ruta/a/binario-malicioso"}`. Pasa el
  `safeParse` (rutaCli es string libre) → se escribe a `data/ajustes/cerebro.json` → el
  siguiente turno hace `spawn(esa_ruta, args)`. `spawn` sin shell neutraliza metacaracteres,
  pero el binario mismo es controlado por el atacante = ejecución de código arbitrario.
- **Sabotaje sin RCE:** poner `cadena:["plantilla"]` (apaga el cerebro), reescribir
  `plantillaRespuesta`, inflar `maxTokensApi`, cambiar el `puerto`/`negocio`, editar el
  tarifario del cotizador (precios), el embudo, etc. Todo lo administrable es atacable.

**Failure scenario concreto:** el dueño pone `host:"0.0.0.0"` para ver el panel desde su
iPhone por Tailscale (patrón documentado). Un dispositivo comprometido en el tailnet hace el
PUT de arriba → RCE en el Mac que maneja la plata de Ads y los datos de clientes.

**Por qué NO lo arreglé:** el arreglo real (autenticación en los endpoints mutantes) no es
acotado. Restringir `rutaCli` a una whitelist rompería despliegues legítimos (destaperapido
usa un shim con ruta absoluta específica; `spawn` sin shell ya evita inyección de shell — el
único vector es apuntar a otro ejecutable, imposible de distinguir de una ruta legítima).

**Mitigación recomendada (para el operador, en orden):**
1. Mantener `host:"127.0.0.1"` (default) y llegar por Tailscale con `tailscale serve`/proxy en
   loopback, NO con `0.0.0.0`.
2. Si se expone, agregar un secreto compartido (header `Authorization`) exigido solo en los
   PUT (`guardarModulo`), leído de `.env.local` de la instancia. Es acotado y compatible con
   la doctrina (el molde ya lee env por instancia).
3. Opcional defensa en profundidad: validar `rutaCli` contra un patrón por instancia
   (`data/ajustes` no debería poder repuntar el binario del cerebro fuera de una lista).

---

### [MEDIO · documentado] H4 — Dos procesos escritores sobre `bot.db` (migrador vs bot vivo): el "1 escritor" es intra-proceso
**Dónde:** `cli/migrar.ts` (abre su PROPIA conexión a `bot.db` de la instancia y escribe vía
su propio `escritor`) vs. el proceso del bot (`src/index.ts`, escribe en cada mensaje).

**Qué rompe:** la garantía "1 escritor" de `escritor.ts` es **por proceso**. Cross-proceso
solo la cubre WAL + `busy_timeout=5000` (db.ts). Las LECTURAS del panel durante una migración
están OK (WAL permite lectores concurrentes con un escritor; cada statement ve un snapshot
consistente) → la parte del concern (d) "migrador mientras el panel lee" es segura. El riesgo
real es **dos ESCRITORES**: si se corre `migrar.ts --desde ...` (pasada incremental) con el
bot VIVO, y el lote del migrador tiene el lock de escritura >5 s, las escrituras del bot pegan
`SQLITE_BUSY` al vencer el `busy_timeout` y lanzan (ver H5 para la consecuencia).

**Recomendación:** correr el migrador solo con el bot detenido (es lo esperado en el cutover
S5); si se necesita incremental en vivo, envolver la pasada del migrador en UNA transacción
corta o subir `busy_timeout`. Documentar en `migrar.ts` que la pasada en vivo es best-effort.

---

### [MEDIO · documentado] H5 — Un mensaje entrante se pierde EN SILENCIO si una escritura falla
**Dónde:** `src/index.ts` `atenderMensaje` (todo el pipeline); `bus.escuchar('canal', async …)`
en L124-126; el `catch` del bus está en `src/core/bus.ts` L40-42 (solo `console.error`).

**Qué rompe:** si cualquier escritura de `atenderMensaje` lanza (SQLITE_BUSY por H4, disco
lleno, constraint inesperada), la promesa del handler async del bus se rechaza y `bus.emitir`
solo la loguea con `console.error`. El webhook de Meta ya fue ACKeado por el poller → **el
mensaje del lead se pierde sin reintento y sin aviso al dueño**. En un bot con plata real, un
lead perdido en silencio = una venta perdida invisible.

**Recomendación (fix acotado posible, no aplicado por ser MEDIO):** envolver `atenderMensaje`
en un try/catch que, ante fallo, emita `bus.emitir({tipo:'aviso', …})` para que al menos el
dueño se entere (idealmente un dead-letter/reintento). Requiere un test del pipeline.

---

### [MEDIO · documentado] H6 — Los avisos no llegan al dueño: solo `console.log`
**Dónde:** `src/index.ts` L127 `bus.escuchar('aviso', (ev) => { log(...) })`; emisores:
`llm.ts` cerrarTurno (plantilla respondió) y `index.ts` (rampa llena).

**Qué rompe:** el comentario de `llm.ts` dice "el dueño DEBE enterarse" cuando el cerebro cae
y el cliente recibió la plantilla. Pero el handler de `aviso` solo hace `console.log`, que
nadie lee a las 3 AM. La doctrina DIXDY tiene `avisos-worker` + `scripts/avisar.py` (push al
celular de Alejandro) justo para esto. En 24/7, "el cerebro está caído y los clientes reciben
la plantilla" debería sonar el timbre, no morir en un log.

**Recomendación:** cablear el handler de `aviso` a `avisar.py`/`avisos-worker` en la instancia
(config del clon, no del molde). Es infraestructura que YA existe (doctrina: no reinventar).

---

### [MEDIO · documentado] H7 — `leerConfig()` puede tirar y hacer que `consultar()` rechace (config corrupta a mano)
**Dónde:** `src/core/llm.ts` `leerConfig` (L85-86, `ConfigLLM.parse(dep.config())`); origen del
throw en `src/core/config.ts` `deModulo` (lanza `ErrorConfig` si el JSON no parsea o no valida).

**Qué rompe:** `dep.config()` = `ajustes.deModulo(cerebro)`, que RELEE `cerebro.json` (TTL 30 s).
Si alguien edita ese archivo a mano y queda medio-escrito o inválido durante la ventana de
30 s, `deModulo` lanza `ErrorConfig`; `leerConfig()` no lo atrapa → `turno()` rechaza →
`consultar()` rechaza (viola su invariante) → vía H5, el mensaje se pierde. La ruta del panel
valida ANTES de escribir, así que este vector es la edición manual (o un guardado no-atómico).

**Recomendación:** en `leerConfig`, atrapar `ErrorConfig` y caer al último-config-bueno o a
defaults + emitir un `aviso`, para que una config mala nunca tumbe el cerebro a media
conversación. (Trade-off: no enmascarar silenciosamente un error de config → por eso avisar.)

---

### [BAJO · documentado] H8 — `ejecutarProceso` acumula stdout/stderr sin tope (OOM por un cli runaway)
**Dónde:** `src/core/llm.ts` `ejecutarProceso` L265-266 (`stdout += d.toString()` sin límite).
Un `claude -p` que por bug escupa gigas de salida crece la string sin cota → OOM. Con
`--output-format json` normal está acotado. Recomendación: cortar y matar el hijo si la salida
supera un tope (p.ej. 4 MB).

### [BAJO · documentado] H9 — La cola no tiene profundidad máxima por conversación
**Dónde:** `src/core/cola.ts`. Un flood en un solo chat (miles de mensajes) encadena miles de
promesas + un backlog de spawns secuenciales sin cota de memoria. FIFO lo serializa (1 spawn a
la vez por chat), pero el backlog crece. Recomendación: tope de profundidad por clave (soltar/
avisar al exceder) — administrable.

### [BAJO · documentado] H10 — `extraerJson` no rescata arrays envueltos en prosa
**Dónde:** `src/core/llm.ts` `extraerJson` L209-216. Un array `[…]` limpio sí pasa (startsWith
'['), pero un array envuelto en prosa solo busca `{`/`}` → no lo extrae → `parse` → failover.
Caso borde de `salidaEsquema` de tipo array. Recomendación: rescatar también `[`/`]`.

### [BAJO · documentado] H11 — Append al ledger sin fsync: un crash puede truncar la última línea
**Dónde:** `src/core/ledger.ts` `apendear` (appendFileSync O_APPEND, atómico por línea, pero no
fsync). Un corte de energía puede dejar la última línea a medias. Los lectores de
`uso-llm`/`eventos` deben tolerar una línea final corrupta (el migrador y las etiquetas ya lo
hacen; conviene la misma tolerancia dondequiera que se lean esos ledgers).

### [BAJO · documentado] H12 — PUT del panel sin límite de tamaño de body
**Dónde:** `src/panel/api.ts` `c.req.json()`. Sin cota de tamaño → un body gigante se lee a
memoria (DoS menor). Recomendación: límite de bytes en el body de los PUT.

---

## Verificado SANO (no son hallazgos, para que conste)
- **Panel y bot = mismo proceso** → sin carrera cross-proceso entre ambos; el cache de
  `Ajustes` es compartido y `guardar` invalida bien (test "ADMINISTRABILIDAD en vivo").
- **Failover del cerebro** bajo fallos en cadena (timeout parcial, salida corrupta, sesión
  `--resume` inválida): tipado, con reintento-una-vez de rate_limit, sesión muerta se borra y
  reintenta sin ella, y red de seguridad dura que responde aunque hasta la plantilla explote.
- **Dedup EN el dato** (UNIQUE conversacion_id+source_id_externo, INSERT OR IGNORE) → reentrega
  de webhook no duplica ni ensucia el hilo; el espejo del migrador es idempotente por claves
  naturales (N corridas = mismo estado).
- **Zombis de `claude -p`:** `ejecutarProceso` mata por timeout (SIGKILL) con guardia `listo`
  para no resolver dos veces, y limpia el timer — no deja el proceso colgado por la ruta normal.
- **HMAC del webhook de Meta** en tiempo constante sobre los bytes crudos (no re-serializa).
- **`moverPedido`** valida etapa/transición/origen/`requiere`/motivo-de-pérdida contra el
  ConfigEmbudo antes de tocar `pedidos.etapa` (única puerta).

---

## Cambios de código (solo H1 y H2, ambos con tests verdes)
- `src/core/escritor.ts` — `persistirSesiones()` tolera fallos de escritura (H1).
- `src/schemas/llm.ts` — `ConfigLLM.maxTurnosConcurrentes` (default 6) (H2).
- `src/core/llm.ts` — semáforo global de traspaso en la puerta; `turno()` toma/suelta permiso
  en `finally` (H2).
- `src/core/escritor.test.ts` — test de H1.
- `src/core/llm.test.ts` — 2 tests de H2 (administrabilidad + no-fuga de permiso).

`tsc --noEmit` = 0 · `vitest run` = 193 passed · `doctor` OK.
