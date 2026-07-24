# Auditoría del CEREBRO y del SISTEMA DE ENTRENAMIENTO del whatsapp-bot (destaperapido)

Fecha: 2026-07-23 · Código vivo: `/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot`
Archivos leídos: `src/brain.js`, `src/aprender.mjs`, `src/aprender-core.mjs`, `src/calidad.js`,
`src/precios.js`, `src/dudas.js`, `src/faltantes.js`, `src/config.js`, `src/store.js` (parcial),
`src/dashboard.mjs` (parcial), `.env` (claves de config no secretas + BOT_PERSONA),
`data/aprendizajes.jsonl|.md`, `data/feedback.jsonl`, `data/calificaciones.jsonl`,
`data/dudas.jsonl`, `data/entrenamiento-resumen.md`, `aprender.log`, `aprender.error.log`,
`ANALISIS-CEREBRO.md`, plist `~/Library/LaunchAgents/com.dixdy.whatsapp-aprender.plist`.

---

## (a) Cómo se construye el prompt del cerebro hoy

### Arquitectura general

El cerebro es conmutable (`src/brain.js:16-26`): `stub` / `cli` / `api`. En producción corre
en modo **`cli`** con **modelo `opus`** (`.env`: `BRAIN_MODE=cli`, `CLAUDE_MODEL=opus` — ojo,
el default del código es `sonnet`, `src/config.js:124`, pero el `.env` lo sube a Opus). Cada
respuesta es un `spawn` de `claude -p <prompt> --output-format text --model opus`
(`src/brain.js:101-102`) con timeout duro de 120 s (`src/brain.js:105-109`). No hay API key,
no hay caché de prompt, no hay sesión: **cada turno re-manda el prompt completo desde cero**.

### Orden exacto de ensamblado (`buildSystemPrompt`, `src/brain.js:52-88`)

1. **`config.botPersona`** — la persona de venta completa. Vive en UNA línea del `.env`
   (`BOT_PERSONA=...`): **10.406 caracteres** medidos en vivo. Contiene tono, formato,
   método de venta (kit comuna+tiempo+cantidad), objeciones, [[SILENCIO]], [[FOTO]],
   política de factura, etc.
2. **`bloqueTrato(pushName)`** (`src/contacto.js:124`) — nombre y género del contacto
   (diccionario local de nombres chilenos, cero tokens). Va ANTES de los aprendizajes
   "para que una corrección tuya pueda anularlo" (`src/brain.js:65-66`).
3. **Reglas aprendidas** — `activeAprendizajesText()` (`src/store.js:170-174`): TODAS las
   reglas con `status:"active"` de `data/aprendizajes.jsonl`, como lista con guiones.
   Hoy: **68 reglas activas = 15.152 caracteres** (medido con Node en vivo). Encabezado:
   "respétalas por sobre todo lo anterior" (`src/brain.js:56-58`).
4. **`contexto`** — bloque armado por el orquestador (`src/index.js:554-567`) juntando
   con `\n\n`, en este orden:
   - `contextoEntrega` (`src/entregas.js`): si el cliente ya tiene entrega en el panel → "no lo re-cotices".
   - `contextoTarifario` (`src/precios.js:458-492`): el TARIFARIO OFICIAL de la comuna
     detectada + estado del KIT (comuna/cantidad/tiempo calculados por CÓDIGO, no por el
     modelo), o el **candado anti-invento** si no hay comuna ("PROHIBIDO dar cualquier
     número", `src/precios.js:485-490`). Con kit completo entrega SOLO la fila del caso con
     frase guía y política de IVA (~1.500-2.500 caracteres). Incluye `ordenIvaManual`
     (`src/precios.js:442-452`) si Alejandro fijó neto/con-IVA para ese chat en el panel.
   - `contextoFaltantes` (`src/faltantes.js:86-134`): qué datos faltan para cotizar (con
     rescate determinista por regex del email/comuna en el historial, `faltantes.js:26-37`),
     gated a que el extractor haya detectado `quiere_cotizacion` (`faltantes.js:93-94`).
   - `contextoDudas` (`src/dudas.js:145-180`): decisiones que Alejandro ya tomó en ESTE
     chat vía buzón de dudas + "encargos" (datos que le pidió al bot conseguir).
5. **Hora del día** ("ahora es de mañana/tarde/noche", `src/brain.js:74-76`).
6. **Bloque de FORMATO** (`src/brain.js:77-86`): solo el mensaje final, "prueba del espejo"
   anti-fuga de razonamiento, máximo 3 globos separados por `///`, máximo 2 preguntas.

Después del system prompt va el transcript: `--- Conversación hasta ahora ---` +
últimos **60 mensajes** (`HISTORY_LIMIT=60` en `.env`; default del código 12,
`config.js:132`) con roles Cliente/Dueño/Asistente y **neutralización anti-inyección** de
etiquetas de rol en el texto del cliente (`limpiarRoles`, `src/brain.js:31-33`).

### Tamaño

Solo el "maletín" fijo: persona 10,4 KB + reglas 15,2 KB + formato ~1 KB + contextos
variables (~2-4 KB) ≈ **27-30 KB (~7-8 k tokens) ANTES del transcript**, en cada turno,
para cada chat, sin caché. El propio `ANALISIS-CEREBRO.md` §4.1 lo llama "el maletín está
SOBRECARGADO" y admite dilución: "bajo presión las reglas del montón pesan menos — por eso
algunas 'no se le quedan'".

### El principio de diseño que sí funciona

Los NÚMEROS viven en código, no en el modelo (`src/precios.js:1-20`): tabla de 40 comunas
céntricas + 5 tramos lejanos, detectores de comuna (con comunas ambiguas, negaciones
"no en Maipú", respuestas peladas), cantidad ("4 und", "solo uno", rangos "1 o 2" que NO
fijan cantidad) y tiempo (evento/2 semanas/3 semanas/mensual, hueco 16-29 días resuelto).
El cerebro recibe la fila exacta y copia el número. Anti-loop: `vecesQuePregunto`
(`precios.js:285-289`) — a la 2ª repregunta sin respuesta abre el "abanico" de precios en
vez de insistir (`precios.js:316-351`). Este archivo tiene 492 líneas y casi cada bloque
lleva un comentario "caso real / bug del 20-jul": es conocimiento de negocio fosilizado a
punta de parches de regex, todos con test (`_test-precios.mjs`, ~100+ asserts).

---

## (b) Cómo aprende hoy

### Fuente de las correcciones

- **Dashboard (:8789)**: Alejandro deja una corrección ✏️ sobre un mensaje puntual
  (`target=<msgId>`) o una nota sobre el chat entero (`target="__chat__"`). Se guarda en
  `data/feedback.jsonl` (35 registros, todos `status:"applied"`; formato en
  `feedback.jsonl` línea 1: `{id, ts, jid, target, comment, status}`).
- **Gimnasio `/entrenar`** (`dashboard.mjs:1700+`): Alejandro juega de cliente contra el
  cerebro real; las correcciones ahí usan el mismo canal de feedback. Resumen en
  `data/entrenamiento-resumen.md`.
- **👍👎 y notas 1-5** (`src/calidad.js`): NO alimentan reglas — son solo métrica
  (`calificaciones.jsonl`: 184 registros, 112 de Alejandro con 82 likes / 28 dislikes,
  72 notas del juez IA). El juez Opus evalúa chats cerrados (2 por pasada,
  `juezAuto`, `calidad.js:254-270`) con los 6 criterios del negocio + las reglas vigentes,
  pero **sus hallazgos no se destilan automáticamente en reglas**: quedan como comentario.

### Destilación (`src/aprender-core.mjs`)

Dos disparadores:
1. **Al instante**: `POST /api/feedback` (`dashboard.mjs:1552-1571`) guarda la corrección
   y llama `aprenderPendientes()` con mutex (dos correcciones seguidas lanzaban dos
   `claude -p` en carrera → reglas duplicadas; el mutex `_aprendiendo` lo arregló).
2. **Cron red-de-seguridad** (`src/aprender.mjs`): el comentario del código dice "cada
   hora", pero el plist real (`com.dixdy.whatsapp-aprender.plist`) corre **una vez al día
   a las 00:30** — una corrección que quede pendiente por caída del panel espera hasta 24 h.
   El log confirma que hace semanas casi todo es "sin correcciones nuevas" (el camino vivo
   es el instantáneo). `aprender.error.log`: 0 bytes.

El prompt de destilación (`destilar`, `aprender-core.mjs:68-88`) incluye: persona base +
reglas YA activas con la instrucción "NO repitas ni contradigas; si ya está cubierta
devuelve []" + ventana de contexto del chat (±6/+4 mensajes alrededor del corregido, o
últimos 20 si es nota de chat, `aprender-core.mjs:54-62`) + la corrección → pide un array
JSON de 0-3 reglas "cortas, imperativas y GENERALES".

### Aplicación

`addAprendizaje` (`store.js:143-155`) hace append a `aprendizajes.jsonl` con
`status:"active"` y `origin:{feedbackId, jid}` (trazabilidad: las 79 reglas tienen origen),
y regenera el `.md` legible. Desde ese instante la regla entra al system prompt de TODOS
los chats (no hay ámbito por tipo de cliente, servicio ni etapa). El panel solo puede
**prender/apagar** reglas (`/api/aprendizajes/estado`, `dashboard.mjs:1577-1584`;
estados `active|off|retired`) — no hay endpoint de edición de texto.

Números del loop: **35 correcciones → 79 registros de regla (68 activas, 9 off,
2 retired)** entre el 06-jul y el 21-jul (≈2,3 reglas por corrección: el destilador tiende
a multiplicar).

---

## (c) "Aprende algo nuevo pero choca con otra cosa después": evidencia

**Sí, hay evidencia abundante y documentada por el propio sistema:**

1. **El flip-flop del IVA (el caso más claro).** Cadena en `aprendizajes.jsonl`:
   regla 17-jul "precio en NETO redondo" (hoy `off`) → regla 20-jul "precio por DEFECTO
   CON IVA INCLUIDO" (hoy `off`) → regla 21-jul "EN EL CHAT el precio se dice en NETO…"
   (hoy `off`, reescrita) → regla activa actual (aprendizajes.md línea 71). El comentario
   de cabecera de `precios.js:13-20` lo confiesa: "ya se dio vuelta dos veces en un mismo
   día por interpretar solo la mitad de la política". Y **el conflicto sigue vivo hoy**: la
   BOT_PERSONA del `.env` todavía ordena cotizar "'$190.400 IVA incluido mensual'" y
   "cotizas con IVA incluido por defecto" (bloque FACTURA), mientras 7 reglas activas
   mencionan IVA y el tarifario dice "En el CHAT el precio se dice en NETO… manda sobre
   cualquier otra instrucción". Funciona por posición en el prompt y mayúsculas, no porque
   el conflicto esté resuelto.
2. **El "140 fantasma"** (`ANALISIS-CEREBRO.md` §7-H4): dos reglas aprendidas traían
   "140mil" como EJEMPLO de redacción y Opus copió el número del ejemplo como precio real
   — dos veces (Puente Alto y la sim H4). Se corrigió apagando las reglas y reescribiéndolas
   sin montos (las versiones con "140mil" están `off` con fecha 21-jul en el jsonl).
3. **Reglas corruptas del propio destilador**: en el jsonl hay, apagadas a mano el 21-jul,
   una regla cuyo texto es `[]`, otra que es ` ``` ` (fence de código) y otra que es un
   comentario meta ("La corrección… ya está cubierta por dos reglas vigentes…"). Es el
   fallback de `parseRules` (`aprender-core.mjs:43-51`): si el modelo no devuelve JSON,
   parte por líneas y CUALQUIER cosa se vuelve regla activa. Estuvieron inyectándose al
   prompt hasta que la revisión humana del 21-jul las apagó (`ANALISIS-CEREBRO.md` §4:
   "apagué 3 corruptas").
4. **Conflicto persona vs reglas de RESERVA** (`ANALISIS-CEREBRO.md` §4.2): la persona
   empuja "le reservamos el baño" como gancho; reglas aprendidas dicen "no confirmes
   reserva sin dirección". Fue el fallo nº1 del juez "3 rondas seguidas" — "el modelo
   queda entre dos jefes".
5. **Conflicto regla 67 vs tabla** (§4.3): "recinto especial → deriva al equipo" choca con
   "Colina = céntrica 160" del tarifario.
6. **Redundancia como forma blanda de conflicto**: §4 tabla — 5 reglas de IVA "dicen lo
   mismo de 5 formas", 10 de kit "algo redundantes", 2 de cierre "medio contradictorias".
7. Hasta el código flip-flopea: commit `f9db1a9 Revert "Arriendo de varios meses: cobrar
   los meses, no uno solo"` (el precio mensual vs total del período se dio vuelta y volvió).

**¿Hay detección de conflictos?** No en código. La única barrera es la instrucción al
destilador ("NO repitas ni contradigas") — o sea, se le pide al mismo LLM que no choque,
y la evidencia de arriba muestra que no basta. No hay comparación semántica entre reglas,
ni entre regla nueva y persona, ni entre regla nueva y tarifario.

**¿Versionado?** Mínimo: `status` (active/off/retired) + `origin` con el feedbackId. No hay
historial de texto (las reescrituras del 21-jul se hicieron creando registros nuevos y
apagando los viejos, a mano en sesión de Claude; una regla del 17-jul que aparece en
`entrenamiento-resumen.md` — "siempre pregunta o confirma la cantidad… antes o junto con
dar el precio", que contradice la regla literal actual — ya ni existe en el jsonl, señal
de ediciones/limpiezas sin rastro). No hay diff, no hay "por qué se apagó".

**¿Tests de regresión de conversaciones?** No. Existe regresión determinista de los
DETECTORES (`_test-precios.mjs`, cubre bugs reales; `_selftest.mjs`, `_test-calidad.mjs`,
`_smoke-brain.mjs`), que es valioso pero cubre el código, no el comportamiento del cerebro.
Lo más cercano a regresión conversacional es el **replay 🎬** (`calidad.js:300-344`:
actor-IA re-juega un chat real contra el cerebro y el juez lo nota), pero es manual,
fire-and-forget, de a un chat, y NO se corre automáticamente al agregar una regla. Nada
impide que la regla nueva rompa un escenario que ayer funcionaba; se descubre cuando el
juez (nota promedio) o Alejandro lo pillan después.

---

## (d) Distancia a la idea de "caminos" del dueño

La visión: conocimiento del negocio como rutas explícitas; si falta un camino, el bot pausa
ese chat, pregunta al humano, aprende la regla en el momento y crea el camino; edición
visual/conversacional. En `docs/24` del maestro la palabra "camino" ni aparece — es visión
nueva. Contra lo que existe:

**Lo que YA apunta en esa dirección (más cerca de lo que parece):**
- **El buzón de dudas (`src/dudas.js`) es el embrión exacto de "pausa y pregunta al
  humano"**: tipos PRECIO/COTIZAR/ENTREGA/RETOMA/DATO, pregunta con opciones concretas,
  dedup por clave (no pregunta dos veces, ni tras reinicio), la respuesta se guarda y
  se aplica sola la próxima vez, y el modo "pregúntaselo tú" convierte la respuesta en
  encargo al bot (`dudas.js:156-163`). El comentario de cabecera (líneas 9-13) describe
  literalmente la filosofía de caminos: "cada duda resuelta lo deja más autónomo".
  **Pero** las respuestas son POR CHAT (`jid` está en la clave): lo aprendido muere con
  la conversación, jamás se generaliza a un camino global.
- **El tarifario/kit (`precios.js`) ES un camino** — el único: "cotizar baño químico"
  como ruta explícita (comuna → cantidad → tiempo → fila exacta → frase guía), con estados
  intermedios (kit incompleto → una pregunta; 2ª insistencia → abanico; sin comuna →
  candado). Solo que está escrito como 492 líneas de regex y strings en código: cada caso
  nuevo es un commit, no una edición del dueño.
- **`ULTIMO_CLICK`** (`config.js:157-174`) es el dial de autonomía por acción
  (todo/entrega/off) — compatible con caminos que "maduran".
- **`FORMULARIO-NEGOCIO.md`** (17 preguntas ❓) es el reconocimiento explícito de que
  faltan caminos y hay que preguntárselos al dueño — pero como documento markdown estático,
  no como flujo en el momento.

**Lo que FALTA para ser caminos:**
1. Las 68 reglas aprendidas son una **lista plana, global y sin estructura**: sin
   condición de activación, sin ámbito (evento vs mensual vs soporte), sin prioridad, sin
   relación entre sí. Un camino es un grafo con condiciones; esto es un montón.
2. **El cerebro nunca pausa por falta de conocimiento**: cuando no sabe, dice "el equipo
   confirma el valor" (deriva y la venta se enfría — `ANALISIS-CEREBRO.md` §2.3 lo lista
   como "venta que se enfría") o responde [[SILENCIO]]. Las dudas las dispara el motor de
   integración en momentos específicos (cotizar/despachar), no el cerebro al detectar
   "no tengo camino para esto". La pieza "pausa el CHAT, pregunta la regla, aprende y
   sigue" no existe como comportamiento general.
3. **Lo aprendido no crea camino**: una corrección se vuelve texto en el prompt (dilución
   comprobada), no una ruta verificable; una duda resuelta se queda en su chat.
4. **Edición visual/conversacional: no hay.** El panel solo prende/apaga reglas; el texto
   se edita en sesiones de Claude a mano; la persona vive en una línea de 10 KB en un
   `.env`.
5. **Multi-canal: nada abstraído** — todo está cosido a Baileys/WhatsApp y a este cliente.

**Veredicto de distancia:** conceptualmente cerca (dudas + kit + último-click son el 60%
de las ideas), estructuralmente lejos: hay que invertir la arquitectura — hoy el
conocimiento vive en 3 capas que se pisan (persona monolítica, reglas planas, código), y
los caminos exigirían UNA representación única, con huecos detectables que disparen la
pausa-y-pregunta, y que tanto el prompt como los detectores se GENEREN desde ahí.

---

## (e) Veredicto honesto: ¿mejora de verdad o acumula parches?

**Las dos cosas, y es medible cuál mejora y cuál acumula.**

Mejora real, con números:
- Nota del juez Opus por día (`calificaciones.jsonl`, 72 notas): 20-jul 2,44 (n=41) →
  21-jul 2,65 (n=23) → 22-jul 4,0 (n=2, muestra chica). `ANALISIS-CEREBRO.md` §5:
  rondas 1,6 → 2,4 → 2,8; embudo real: 59 chats con bot, 12 cotizaciones formales,
  6 entregas (cierre 50% post-cotización).
- Bugs graves con causa raíz y test: candado anti-invento de precios, negación de comuna,
  rangos "1 o 2", hueco de 16-29 días — todo en `precios.js` + `_test-precios.mjs`.

Pero la mejora de fondo NO vino del loop de reglas: vino de **mover conocimiento del
prompt al código** (tarifario, kit, candados) y de auditorías manuales profundas (el
`ANALISIS-CEREBRO.md` del 21-jul, las 6 simulaciones adversariales). Eso lo hizo
Alejandro+Claude en sesiones, no `aprender.mjs`.

El loop de reglas, en cambio, **acumula**: 35 correcciones → 79 reglas (2,3× de
multiplicación), 68 activas / 15 KB inyectados a todo chat, 7 reglas activas hablando de
IVA, redundancia admitida (5 de IVA = 1), tres reglas basura que corrieron en producción
hasta que un humano las apagó, un flip-flop de política (IVA) que dio tres vueltas en
cuatro días, y una persona de 10,4 KB que contradice a las reglas y nadie actualizó. Sin
detección de conflictos, sin regresión conversacional automática, sin edición: la única
"consolidación" propuesta (66 → ~30 reglas, §4.1) es otra tarea manual pendiente. El
sistema funciona hoy porque Opus aguanta un maletín contradictorio de 30 KB y porque los
números están blindados en código — no porque el loop converja. Con Sonnet (el default del
template) o con más reglas, la dilución que el propio análisis admite empeora.

**Conclusión para dixdybot:** conservar el principio "números/lógica en código, LLM solo
redacta", el buzón de dudas (generalizándolo a conocimiento global, no por chat) y el
juez/replay como arnés de regresión automática POR REGLA. Reemplazar la tríada
persona-monolítica + lista-plana-de-reglas + regex-parche por la representación única de
caminos con: ámbito y condición por regla, detección de conflicto al ingresar (contra
persona, tarifario y reglas), versionado con historial, y pausa-del-chat cuando el camino
no existe. El loop actual demostró la parte más difícil (el dueño SÍ corrige y el sistema
SÍ puede aplicar al instante); lo que no tiene es una estructura donde eso converja en vez
de apilarse.

---

## Anexo: cifras rápidas

| Métrica | Valor | Fuente |
|---|---|---|
| Persona | 10.406 chars, 1 línea de `.env` | medido en vivo |
| Reglas activas | 68 (15.152 chars) | `aprendizajes.jsonl` |
| Reglas totales / off / retired | 79 / 9 / 2 | `aprendizajes.jsonl` |
| Correcciones de Alejandro | 35 (todas applied) | `feedback.jsonl` |
| Calificaciones | 184 (112 Alejandro: 82👍 28👎; 72 juez) | `calificaciones.jsonl` |
| Nota juez por día | 2,44 (20-jul) → 2,65 (21-jul) → 4,0 (22-jul, n=2) | `calificaciones.jsonl` |
| Historial al cerebro | 60 mensajes (`HISTORY_LIMIT=60`) | `.env` |
| Modelo vendedor / juez / actor | opus / opus / sonnet | `.env` + `config.js:124-128` |
| Timeout por respuesta | 120 s (`claude -p`) | `brain.js:105-109` |
| Cron aprender | diario 00:30 (código dice "cada hora") | plist + `aprender.mjs:1` |
| Dudas registradas | 8 (3 pendientes, 1 resuelta, 3 anuladas + 1 entrega resuelta) | `dudas.jsonl` |
| Embudo | 59 chats con bot → 12 cotizaciones → 6 entregas | `ANALISIS-CEREBRO.md` §5 |
