# dixdybot — Arquitectura por EVOLUCIÓN INCREMENTAL

**Ángulo:** el bot vivo no se reemplaza: se transforma en dixdybot por etapas cortas, cada una
en producción al día siguiente, con rollback trivial (git revert) y prueba de no-regresión
(tests + replay del gimnasio + nota del juez). El bot vende HOY (59 chats con bot, 12
cotizaciones, 6 entregas, 50% de cierre post-cotización) y nunca deja de vender durante la
migración.

**Principio rector (patrón estrangulador, versión DIXDY):** no se construye un dixdybot "al
lado" que algún día reemplace al bot. El bot ACTUAL es dixdybot v0. Cada etapa mueve una
pieza a su forma final dentro del mismo repo y el mismo proceso; el corte a multi-proceso o
multi-canal ocurre solo cuando la pieza ya demostró funcionar. Así se cumple la doctrina
(no reinventar, sumar a lo que existe) y el riesgo de cada paso es el de un commit, no el
de un big-bang.

Código vivo: `/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot` (24 archivos
en src/, ~7.119 líneas). Template maestro: `/Users/alejandroriveracarrasco/SaSS/DIXDY/whatsapp-bot`
(12 archivos, ~1.912 líneas — desactualizado, se re-sincroniza en la etapa final).

---

## 1. De qué partimos (estado real verificado)

Lo que ya ES dixdybot embrionario (se conserva y se generaliza):

| Pieza viva | Archivo | Qué aporta al diseño final |
|---|---|---|
| Cerebro conmutable stub/cli/api | `src/brain.js` (getReply, brainCli 120s, brainApi YA implementado) | El fallback de cerebro ya existe: solo hay que cablearlo automático |
| Buzón de dudas con acción ejecutable | `src/dudas.js` (TIPOS, addDuda, respuestaPrevia, contextoDudas) | Es el embrión EXACTO de "caminos": pausa la decisión, pregunta con opciones, no repregunta |
| Cola de salida anti-duplicado | `src/outbox.js` (ids estables, MAX_TRIES=5, reconciliar) | Transactional outbox por canal, listo |
| Envío en frío con sanación Bad MAC | `src/enviar.js` (enviarSeguro, sanarSesion, revisarPendientes) | Sobrevive tal cual dentro del adaptador WhatsApp |
| Política anti-ban por chat + global | `src/gating.js` (debounce, gen, topes 40/h y 200/día) | Se vuelve "política por canal" con parámetros por transporte |
| Libro mayor de envíos | `data/envios.jsonl` + `logEnvio` (integracion.js:604-610) | Ledger append-only del tracking punta a punta |
| Guardianes puros | `integracion.js`: fechaISO (105-201), precioCoherente (277-294), construirConfigCotizacion (321), construirEntrega (406) | Se extraen como módulo de validación, intactos |
| Destilador de correcciones | `src/aprender-core.mjs` (aprenderPendientes, claude -p) | Se convierte en el escritor de caminos |
| Juez/actor/replay | `src/calidad.js` (juezIA, replayChat, resumenSemanal) | Es la base de la red de regresión conversacional |
| Extractor de datos | `src/extraer.js` (analizarConversacion, ventana 200 msgs) | Sobrevive; se le pone cola y presupuesto |

Deudas que la migración paga (de las auditorías):

- `src/index.js` (650 líneas) mezcla transporte + turno de respuesta; el jid de WhatsApp es
  clave primaria de TODO → bloquea Instagram.
- 4 spawns distintos de `claude -p` sin cola ni límite (brain 120s, extraer 90s sin --model,
  calidad 150s, aprender-core SIN timeout).
- Conocimiento en 3 capas que chocan: BOT_PERSONA de 10.406 chars en el .env (aún ordena
  "$190.400 IVA incluido"), 68 reglas planas inyectadas a todos los chats (15.152 chars),
  y tarifario en código. Prompt de ~27-30 KB por turno, sin selección.
- Fixes críticos del 21/22-jul SIN COMMITEAR en src/index.js y src/quiet.js.
- 401 loggedOut deja el proceso vivo pero ciego para siempre (index.js:303-306) y nadie avisa.
- seenMsgIds y el tope de respuestas viven solo en RAM (reinicio = amnesia).
- `dashboard.mjs` (1.897 líneas, ~50 endpoints) re-implementa extracción y comuna con
  lógica DIVERGENTE de la del bot (dashboard.mjs:314 vs precios.js:88).
- Rutas absolutas hardcodeadas: integracion.js:55 (avisar.py), aprender-core.mjs:19
  (actividad.py), bridge/entrega_bridge.py:16-18.
- Sin rotación de logs (bot.error.log llegó a 53 MB); 2.631 Bad MAC solo el 22-jul.

---

## 2. Arquitectura destino (a la que se llega por etapas, no de una)

Misma carpeta, mismo launchd, mismos 3 procesos al principio (bot, panel, cron). El src/
se reorganiza así SOLO al final de la etapa 4; hasta entonces los archivos nuevos conviven
planos con los actuales para que cada diff sea chico:

```
whatsapp-bot/                    (después: dixdybot/ en el maestro)
├── src/
│   ├── core/
│   │   ├── mensaje.js           # contrato MensajeCanonico + convId
│   │   ├── turno.js             # el turno de respuesta (hoy closure de index.js:499-644)
│   │   ├── llm.js               # ÚNICA puerta a claude -p / API: cola, timeout, failover
│   │   ├── prompt.js            # ensamblador por capas (persona + caminos + contextos)
│   │   ├── caminos.js           # CRUD + matcher + conflictos + métricas
│   │   ├── pausa.js             # pausa-y-pregunta (generaliza dudas.js)
│   │   ├── pipeline.js          # orquestador de integración en pasos (ex procesarIntegracion)
│   │   ├── validar.js           # fechaISO, precioCoherente, datosCompletos* (extraídos)
│   │   ├── acciones/            # cotizar.js, entregar.js (ex doCotizacion/doEntrega)
│   │   └── politica.js          # gating por canal (ex gating.js, parametrizado)
│   ├── canales/
│   │   ├── whatsapp/
│   │   │   ├── transporte.js    # conexión Baileys, reconexión, Bad MAC, recibos (ex index.js)
│   │   │   └── adaptador.js     # Baileys ⇄ MensajeCanonico; implementa la interfaz Canal
│   │   └── instagram/
│   │       ├── adaptador.js     # Graph API send + ventana 24h
│   │       └── buzon.js         # polling del Worker CF que recibe el webhook (patrón timbre v2)
│   ├── panel/
│   │   ├── api.mjs              # ex dashboard.mjs, SOLO API JSON
│   │   └── (web/ sirve estático)
│   ├── brain.js, extraer.js, enviar.js, outbox.js, store.js, dudas.js,
│   │   precios.js, portero.js, contacto.js, calidad.js, aprender-core.mjs   # SOBREVIVEN
│   └── index.js                 # arranque: monta canal(es) + timers (queda de ~60 líneas)
├── data/
│   ├── caminos/                 # UN .md por camino (git-versionado)
│   ├── caminos-uso.jsonl        # métrica de uso por turno
│   ├── persona.md               # ex BOT_PERSONA (solo identidad y tono)
│   ├── tarifario.json           # ex tablas CENTRICAS/LEJANAS de precios.js
│   ├── ajustes.json             # config caliente editable desde el panel
│   ├── identidad.json           # convId → {telefono, email, nombre, alias[]}
│   ├── vistos.jsonl             # dedup de mensajes persistente
│   └── (todo lo actual: conversaciones.jsonl, envios.jsonl, dudas.jsonl, …)
└── launchd/                     # com.dixdy.whatsapp-bot.plist (+ healthcheck)
```

### 2.1 Capa de canales

**Contrato `MensajeCanonico`** (src/core/mensaje.js):

```json
{
  "convId": "wa:56998765432@s.whatsapp.net",
  "canal": "whatsapp",
  "from": "client",
  "text": "hola, necesito un baño químico",
  "ts": 1753200000000,
  "nombre": "Pía",
  "telefono": "56998765432",
  "media": null,
  "nativeId": "3EB0A9..."
}
```

- `convId = canal + ":" + claveNativa` (wa:jid hoy; `ig:<igsid>` mañana). Es la NUEVA clave
  primaria. Compatibilidad: `convIdDe(jid)` y `jidDe(convId)` en mensaje.js; los archivos
  históricos siguen con jid y el lector los normaliza al vuelo (no se migran datos en frío).
- `telefono` puede ser null (Instagram): el cruce chat↔entrega (entregas.js) pasa a
  resolverse vía `data/identidad.json`, que enlaza convIds de canales distintos cuando el
  pipeline extrae teléfono o email. `enlaces.json` (jid↔entrega) se absorbe ahí.

**Interfaz `Canal`** (lo que todo adaptador implementa):

```js
{
  id: "whatsapp",
  enviar(convId, { text?, document?, image? }, { typingMs }),  // Promise<{nativeId}>
  typing(convId, on),          // no-op donde no exista
  marcarLeido(convId),         // no-op donde no exista
  listo(),                     // ¿conexión sana? (hoy conexionLista() de enviar.js)
  politica: { replyDelayMs, followupDelayMs, maxRepliesPerChat, maxHora, maxDia, ventanaRespuesta } 
}
```

- WhatsApp/Baileys: `transporte.js` es el index.js actual menos el turno (reconexión con
  backoff, append/eco fromMe, stub CIPHERTEXT, recibos por los 2 canales — todo el
  conocimiento ganado a golpes se conserva línea a línea). `adaptador.js` envuelve
  enviarSeguro/outbox.
- Instagram (etapa 5): SOLO vía oficial (Instagram API with Instagram Login, sin página de
  Facebook; Standard Access basta porque la cuenta es del cliente de DIXDY con rol en la
  app). El webhook de Meta cae en un Worker de Cloudflare (infra que DIXDY ya opera:
  correo-worker/avisos-worker) que encola en D1/KV; el Mac lo drena por polling cada 10 s
  (patrón timbre v2 del correo-worker — NO se abre un puerto en el Mac). `politica` de IG:
  ventanaRespuesta 24 h, sin typing simulado, sin HUMAN_AGENT jamás para el bot (Meta lo
  audita y lo revoca).
- El outbox se vuelve por-canal: `outbox.json` gana campo `canal` (default "whatsapp");
  el drenador elige adaptador. Cambio de 10 líneas sobre outbox.js.

### 2.2 Cerebro: una puerta, capas, fallback automático

**`src/core/llm.js`** — la única forma de hablar con un modelo en todo el sistema:

```js
runLLM({ rol: "cerebro"|"extractor"|"juez"|"actor"|"destilador"|"conflictos",
         prompt, model?, timeoutMs?, formato: "text"|"json" })
```

- Unifica los 4 spawns de hoy (brain.js:101, extraer.js, calidad.js:183, aprender-core.mjs:26).
- Cola con concurrencia 2 y prioridad: `cerebro` > `extractor` > resto (un extractor de 200
  mensajes no puede robarle el turno a un cliente esperando).
- Timeouts por rol (cerebro 120s, extractor 90s, juez 150s, destilador 120s — hoy aprender
  no tiene NINGUNO).
- **Failover automático de cerebro** (hoy es manual vía BRAIN_MODE): si `cli` devuelve
  null/timeout 2 veces seguidas → conmuta a `brainApi` (YA implementado en brain.js:130-173,
  Haiku 4.5) por 10 minutos y avisa por avisos-worker. `.env` nuevo: `BRAIN_FALLBACK=api`.
- Blindaje contra el gotcha `--bare` (verificado en doc oficial): NUNCA pasar --bare, fijar
  `autoUpdatesChannel: stable` + `minimumVersion`, y usar `claude setup-token`
  (CLAUDE_CODE_OAUTH_TOKEN, 1 año) para que un login caducado no mate el bot headless.
- Registra latencia y fallos por rol en `data/llm-metricas.jsonl` (después alimenta la
  decisión de migrar tráfico conversacional a API Messages delgada, que el análisis de ToS
  marca como destino necesario del tráfico del bot; el switch ya existirá).

**`src/core/prompt.js`** — el prompt deja de ser una pared de 27-30 KB y pasa a capas:

1. `data/persona.md` — SOLO identidad, tono, formato (globos ///, [[SILENCIO]], [[FOTO]],
   [[NOSE]]). Meta: ≤ 3 KB. Toda política de negocio SALE de aquí (mata estructuralmente el
   conflicto vivo del IVA: persona dice "$190.400 IVA incluido" mientras 7 reglas mandan NETO).
2. Caminos seleccionados este turno (≤ 5-8, ver 2.3).
3. Contextos vivos (ya existen): tarifario por comuna (precios.js), estado de entrega
   (entregas.js), faltantes (faltantes.js), decisiones del chat (contextoDudas), trato
   (contacto.js).
4. Bloque de formato final (el actual de brain.js:77-86).

### 2.3 Caminos: la pieza central

**Estructura de datos** — un archivo por camino en `data/caminos/<slug>.md`, markdown con
frontmatter YAML (parser propio de ~40 líneas, mismo espíritu del parseo de .env de
config.js: cero dependencias). Es el formato de Agent Skills / Parlant traducido al sistema:

```markdown
---
id: cam-0042
titulo: Precio que no calza con el tarifario
cuando: cliente menciona o pide un precio distinto al oficial de su comuna
palabras: [precio, descuento, "más barato", rebaja]
prioridad: normal        # alta = entra SIEMPRE al prompt; normal = entra si matchea
ambito: [whatsapp, instagram]
estado: activo           # activo | apagado | retirado
version: 3
origen: duda:d-8842      # de qué duda/corrección nació (trazabilidad)
creado: 2026-07-28T10:00:00Z
actualizado: 2026-08-02T09:12:00Z
---
Si el precio conversado no calza con el tarifario oficial:
1. NO confirmes ese precio.
2. Dile que confirmas el valor con el equipo y sigue juntando los demás datos.
3. El sistema abrirá la consulta a Alejandro solo.
PROHIBIDO: inventar montos. Todo número sale del tarifario o de una respuesta de Alejandro.
```

Reglas duras del formato (lecciones del "140 fantasma"): **cero cifras en el cuerpo** — los
montos viven en `data/tarifario.json` o en el frontmatter `datos:` y el sistema los inyecta
como contexto; el candado `precioCoherente()` sigue vigente como segunda muralla.

**Selección por turno** (caminos.js `seleccionar(historial, convId)`): prioridad `alta` +
matching barato por `palabras`/`cuando` contra los últimos mensajes + caminos ya usados en
esta conversación (continuidad). Tope 8. Índice compilado `data/caminos-index.json`
regenerado al guardar. Esto implementa la carga selectiva que Parlant/Skills hacen y que
mata la dilución de atención (caída de precisión de hasta 85% con prompts atiborrados,
según la doc de Parlant). Registro de lo seleccionado en `data/caminos-uso.jsonl`:
`{ts, convId, turnoId, caminos:[ids]}`.

**Pausa-y-pregunta (el bucle del dueño)** — generaliza `dudas.js`, que ya hace el 80%:

1. **Detección del hueco** por DOS vías:
   - El cerebro declara: la persona instruye que si no hay camino ni dato para responder
     algo del negocio, responda `[[NOSE: pregunta corta para el dueño]]` en vez de
     improvisar o enfriar con "el equipo confirma".
   - El pipeline detecta (ya existe): precio incoherente, dato faltante, confirmación sin
     fecha — los casos de integracion.js:744-906 siguen igual.
2. **Pausa de TEMA, no de chat**: se crea `addDuda({tipo: "camino", clave: <slug del tema>,
   pregunta, opciones})` (nuevo TIPOS.CAMINO en dudas.js:24-30). El chat NO cae a manual: el
   cerebro recibe en contexto "hay una consulta pendiente sobre X: no la respondas tú; di
   que lo estás confirmando y sigue con lo demás". Al cliente le sale al tiro el mensaje
   honesto: "déjeme confirmarlo, le escribo en unos minutos" (respuesta enlatada del
   sistema, no redactada — rubro de urgencia, verificado como el riesgo #1 del aprendizaje
   en caliente).
3. **Aviso**: push por `scripts/avisar.py` al avisos-worker (ya integrado en
   integracion.js:52). Si en 30 min hábiles no hay respuesta → seguimiento.js manda al
   cliente "seguimos gestionándolo" y re-avisa a Alejandro.
4. **Aprendizaje en caliente**: Alejandro responde en el panel (opciones + texto libre). Al
   resolver, el panel pregunta UNA cosa más: "¿vale solo para este cliente o siempre?".
   - *Solo este chat* → queda como hoy (respuestaPrevia por jid, dudas.js:84-88).
   - *Siempre* → `aprender-core` destila la respuesta en un camino nuevo (o edición de uno
     existente), corre la detección de conflictos, y lo activa. **El chat pausado se
     reanuda en ese instante**: `scheduleReply(convId, …)` se re-dispara con el camino ya
     cargado (respetando gen para no pisar mensajes nuevos).
5. `respuestaPrevia` sigue evitando repreguntar; los caminos son la generalización global
   que hoy falta (las dudas actuales mueren por-chat y jamás se promueven).

**Detección de conflictos** (caminos.js `conflictosDe(caminoNuevo)`): al crear/editar, se
comparan con `runLLM({rol:"conflictos"})` el camino nuevo + los 10 más parecidos (overlap
de palabras del frontmatter). Salida JSON `[{caminoId, motivo, gravedad}]`. Si hay choque,
el panel lo muestra y NO activa hasta que Alejandro elija: "el nuevo manda" (el viejo pasa
a `retirado` con nota) o "conviven" (se les acota `cuando`/`ambito`). Es el mecanismo de
ARIA (repositorio timestampeado + resolución por comparación) con el destilador que ya
existe. Se acabó el "IVA dio tres vueltas en cuatro días": la vuelta 2 habría chocado en
la puerta.

**Versionado y rollback**: `data/` del clon ya puede ser repo git (o sumarse al del clon);
cada guardado de camino = commit `camino: <slug> v<N> (<origen>)`. El panel expone "ver
versiones / volver a la anterior" = `git log`/`git checkout -- <archivo>` sobre ese único
path. Gratis, como demuestra Decagon cobrándolo caro.

**Edición conversacional**: endpoint `POST /api/caminos/editar {instruccion}` — Alejandro
escribe "en las fosas sépticas ofrece visita técnica antes de dar precio"; el destilador
propone el diff sobre el/los caminos afectados (o uno nuevo); el panel muestra
antes/después; un toque confirma (commit). Nada de editar YAML a mano: él nunca ve el
frontmatter, ve "cuándo aplica / qué hace / desde cuándo".

**Métricas por camino** (vista Conocimiento): cruzando `caminos-uso.jsonl` con
`envios.jsonl` por convId → por camino: usos, chats distintos, cotizaciones en las que
participó, entregas/cobros en las que participó, última vez. Lista de huecos = dudas tipo
`camino` abiertas + frecuencia de `[[NOSE]]` por tema. Con esto se ve qué camino vende y
cuál estorba.

**Arranque en frío**: script `migrar-reglas.mjs` (una vez): toma las 68 reglas activas de
`aprendizajes.jsonl` + `ANALISIS-CEREBRO.md` + la BOT_PERSONA y propone con claude -p unos
20-30 caminos agrupados (técnica Agent Workflow Memory aplicada a nuestros datos:
conversaciones.jsonl y envios.jsonl como trayectorias). Alejandro aprueba en lote desde el
panel. Las reglas quedan `retired` con `origen` apuntando al camino que las absorbió.

### 2.4 Pipeline de negocio (la joya se conserva)

`procesarIntegracion` (integracion.js:694-911) se parte en pasos nombrados, mismos
comportamientos, y las funciones puras se van a `validar.js` y `acciones/` SIN tocar su
lógica:

```
pipeline.js:  detectar(historial) → extraer (extraer.js, vía llm.js) → fusionarFicha
  → normalizar (fechaISO) → validar (precioCoherente, datosCompletos*)
  → decidir (ultimoClick / dudas / respuestaPrevia)  → ejecutar (acciones/cotizar|entregar)
  → registrar (logEnvio APENAS sale lo irreversible — contrato intacto)
```

- Se mantienen: dedup `yaCotizado(45d)`/`yaDespachado(∞)`, Set `enVuelo`, integración
  desacoplada de la respuesta (index.js:509 → turno.js), `prepararEntrega` que construye
  sin enviar (la costura multi-canal ya insinuada), bridge a Supabase con upsert
  idempotente y aviso al repartidor aunque Supabase caiga.
- Deudas que se pagan al partirlo: seguimiento.js deja de enviar directo y pasa TODO por
  outbox (hoy hay dos vías de envío); rutas absolutas a `.env`
  (AVISAR_PY, ACTIVIDAD_PY, y bridge/entrega_bridge.py:16-18 lee de argv/env).
- **Evento de cobro (brecha del embudo económico)**: el panel ya lee `entrega_estado` de
  Supabase en vivo; cuando un estado pasa a `cobrado` y no hay evento previo, se agrega
  `{tipo:"cobro", convId, entrega_id, monto_pactado, ts}` a envios.jsonl. Con eso el
  embudo queda completo: chat → cotización → entrega → cobro, todo en un solo ledger.

### 2.5 Panel de configuración (evoluciona, no se reescribe)

`dashboard.mjs` no se tira: se parte en `panel/api.mjs` (JSON) y estático, endpoint por
endpoint, y **toda lógica duplicada se borra a favor de consumir la del bot** (la comuna
de dashboard.mjs:314 muere; manda precios.js:88). Vistas finales:

1. **📊 Kanban** (existe): 4 columnas + Dormidos; sin cambios de fondo. La etapa se cambia
   por UN mecanismo (drag); los botones de ficha se reducen a eso.
2. **💬 Ficha del chat** (existe): precio editable en UN solo lugar (hoy 3); preview
   editable antes de enviar se conserva tal cual (patrón ganador).
3. **🧠 Conocimiento** (NUEVA — la que hoy no existe y el dueño pide):
   - Caminos: lista con estado/uso/cierres, editar texto (hoy solo on/off), crear directo,
     versiones, conflictos pendientes, edición conversacional.
   - Persona: `persona.md` visible y editable (hoy invisible en el .env línea 9).
   - Tarifario: `tarifario.json` editable con validación (hoy exige editar código + tests +
     reiniciar); los tests `_test-precios.mjs` corren al guardar y bloquean si fallan.
4. **❓ Dudas** (existe): bandeja única — dudas de acción (cotizar/entregar/precio) + huecos
   de camino, con el flujo "responder → se ejecuta/aprende → chat sigue".
5. **🏋️ Gimnasio** (existe): mismas piezas (práctica, replay, juez), pero las 5 entradas de
   feedback bajan a 2 (enseñar por mensaje, nota de chat con estrellas — muere el prompt()
   nativo), y la lista duplicada de chats usa la del dashboard.
6. **⚙️ Ajustes** (NUEVA): interruptor global del bot (hoy no existe), vista de pausas de
   todos los chats, gating visible (delays, topes 40/200, horario), número del repartidor,
   dial `ultimoClick` (todo/entrega/off), canal(es) conectado(s) y su salud. Respaldado por
   `data/ajustes.json` con hot-reload: config.js pasa a mergear `.env < ajustes.json`
   (el .env queda como bootstrap; el panel edita sin reiniciar).

### 2.6 Entrenamiento y calidad

- El loop actual se conserva (aprender.mjs por launchd como red de seguridad + destilado
  instantáneo desde el panel), pero su SALIDA cambia: en vez de apilar reglas planas,
  escribe/edita caminos con detección de conflictos. `parseRules` (aprender-core.mjs:43-51)
  se endurece: si la salida no es JSON válido, se descarta y se reintenta UNA vez — nunca
  más un "```" corriendo en producción como regla activa.
- **Red de regresión conversacional** (hoy inexistente, incidentes 16 y 22-jul): se
  formalizan 6-10 "chats dorados" (los mejores reales: cotización limpia, precio raro,
  cliente que confirma sin fecha, fosa séptica, cliente antiguo de soporte). Tras cada
  cambio de camino/tarifario/persona, `calidad.js` corre el replay de los dorados
  (replayChat ya existe) + juez con nota; si la nota media cae > 0,7 vs el último corte, el
  cambio queda "activo en observación" y se avisa. Mismo mecanismo del gimnasio, cero
  librerías nuevas (DeepEval se imita, no se adopta).
- La nota del juez ya probó servir de brújula: 2,44 (20-jul) → 2,65 (21-jul) → 4,0 (22-jul).
  Se registra por semana en el resumen que ya existe (resumenSemanal, calidad.js:159).

### 2.7 Despliegue: Mac mini vs VPS, y el cerebro

**Recomendación: Mac mini hoy, portabilidad diseñada, VPS solo con causa.**

| | Mac local (actual) | VPS Linux |
|---|---|---|
| Costo cerebro | claude -p con Max = costo marginal $0 (consume cupo compartido de la cuenta) | Igual viable (Claude Code es 1ª clase en Linux, setup-token 1 año), pero un bot comercial 24/7 en suscripción es zona gris de ToS; la vía limpia es API: ~$27-40/mes en Haiku 4.5 a 300 invocaciones/día |
| Uptime | Depende de luz/internet de la casa; launchd + KeepAlive ya probados (57 reinicios absorbidos) | Mejor uptime e IP fija; systemd equivalente trivial |
| Ecosistema | TODO está aquí: scripts python del clon, bridge Supabase, avisos-worker, Tailscale al iPhone, sesión Claude | Habría que llevarse bridge+scripts o llamarlos remoto; la sesión de WhatsApp (auth/) es portable, el resto es trabajo |
| Riesgo | Único punto de falla físico | Migración = riesgo puntual para la sesión Baileys |

Todo el diseño es file-based + launchd → se muda a systemd copiando la carpeta (la sesión
auth/ es portable, ya probado en la mudanza maestro→clon). La decisión VPS se re-evalúa
cuando dixdybot se venda a terceros — y ahí **API key por cliente es obligatoria** (los ToS
prohíben enrutar peticiones de terceros por credenciales Max; verificado).

**Cadena de fallback del cerebro** (etapa 1): `cli` (Max, $0) → auto-conmuta a `api`
(Haiku 4.5) ante 2 fallos/timeouts → si tampoco, respuesta enlatada de cortesía y duda al
panel. Los precios/validaciones NO dependen del modelo (viven en código+JSON), así que el
fallback no degrada la seguridad de negocio, solo el estilo. A mediano plazo el tráfico
conversacional (90% de las invocaciones) debería migrar a API Messages con caching; el
switch es `BRAIN_MODE=api`, ya existe, y llm.js medirá los tokens para decidir con números.

**Plan B WhatsApp (documentado, no activado)**: si Baileys se vuelve insostenible (ban o
Bad MAC crónico), la Cloud API oficial cuesta hoy ~$0 en flujo inbound; desde el
01-oct-2026 los mensajes de servicio pasan a tarifa utility Chile (~US$0,02 ≈ CLP 19) —
presupuesto < CLP 10.000/mes al volumen actual. La arquitectura de canal (2.1) hace que
sea UN adaptador nuevo, no una reescritura. Coexistence permite mantener el mismo número.

---

## 3. Qué sobrevive y qué muere

**Sobreviven casi intactos:** enviar.js, outbox.js (+campo canal), store.js (writeAtomic se
vuelve la ley para TODOS los json), portero.js, contacto.js, extraer.js (su prompt es de lo
mejor del sistema), precios.js (lógica; tablas → tarifario.json), dudas.js (+TIPOS.CAMINO),
calidad.js, aprender-core.mjs (nueva salida), seguimiento.js y recordatorios.js (pasan por
outbox), bridge/entrega_bridge.py (rutas por env), faltantes.js, entregas.js, quiet.js,
launchd/*.plist, y TODAS las funciones puras de integracion.js.

**Se transforman:** index.js (650 → ~60 líneas de arranque; su contenido vive en
canales/whatsapp/transporte.js + core/turno.js), gating.js (→ core/politica.js
parametrizado por canal, con contadores persistidos), integracion.js (→ core/pipeline.js +
validar.js + acciones/), brain.js (conserva getReply; el spawn se muda a llm.js),
config.js (merge .env < ajustes.json), dashboard.mjs (→ panel/api.mjs sin lógica duplicada).

**Mueren:** BOT_PERSONA en el .env (→ persona.md, y la política de negocio → caminos), las
68 reglas planas inyectadas a todo chat (→ caminos seleccionados), la detección de comuna
duplicada del panel (dashboard.mjs:314), las 3 regex de precio repetidas, los 4 spawns
sueltos de claude -p, el prompt() nativo del gimnasio, las 2 taxonomías de embudo
divergentes (STAGES manda; el Kanban la consume), y los números desactualizados del
MANUAL.md (60s/tope 3-4 vs 30s/12 reales).

---

## 4. PLAN DE MIGRACIÓN (cada etapa termina en producción)

### Etapa 0 — "Cinturón de seguridad" (1-2 días) ← entregable en DÍAS
1. **Commitear lo vivo**: los fixes del 21/22-jul en src/index.js y src/quiet.js están sin
   commit (riesgo #1 real hoy: un `git checkout` accidental los borra).
2. **Aviso de muerte silenciosa**: en index.js:303-306 (401 loggedOut) y en fallo doble del
   cerebro, llamar `python3 …/DIXDY/scripts/avisar.py` (el worker de avisos YA existe;
   integracion.js:52 ya lo usa). +Healthcheck launchd cada 15 min: si bot.log no avanza en
   30 min con mensajes entrantes pendientes → aviso.
3. **Backup atómico de auth/** diario (tar a backups/ con retención 7) — 4 corrupciones de
   sesión en julio lo justifican.
4. **Rotación de logs** (bot.error.log llegó a 53 MB en 5 días).
5. **Dedup y topes persistentes**: seenMsgIds a data/vistos.jsonl (ventana 24 h) y
   botReplies re-contado desde conversaciones.jsonl en hydrate() — cierra la doble
   respuesta tras reinicio y el tope fantasma.
6. **persona.md**: mover BOT_PERSONA a data/persona.md (config.js: si existe el archivo,
   manda; el .env queda de fallback). Cero cambio de comportamiento, primer paso del
   conocimiento-como-datos. De paso se corrige ahí el "$190.400 IVA incluido" que
   contradice a las 7 reglas NETO.
   *Prueba*: `npm run check` + `_test-precios.mjs` + `_smoke-brain.mjs` + 1 replay dorado.
   *Rollback*: git revert; el bot no cambió de conducta.

### Etapa 1 — "Una sola puerta al modelo" (3-4 días)
- `src/llm.js` (cola, timeouts, métricas) y los 4 llamadores lo adoptan uno por uno (4
  commits separados, cada uno reversible).
- Failover cli→api automático + `BRAIN_FALLBACK` (brainApi ya existe; solo cablear) +
  `claude setup-token` + fijar canal stable/minimumVersion del CLI.
- writeAtomic para outbox/seguimientos/recordatorios/enlaces/pedidos (funciones ya en
  store.js:38).
  *Mejor que ayer*: el bot ya no puede quedar mudo por un claude colgado ni por login
  caducado, y dos procesos ya no se pisan los json.

### Etapa 2 — "El conocimiento sale del código" (4-5 días)
- Tablas CENTRICAS/LEJANAS → `data/tarifario.json` (precios.js lo carga; `_test-precios.mjs`
  corre igual y además al guardar desde el panel).
- Vista **🧠 Conocimiento v1** en el panel: tarifario editable, persona.md editable, reglas
  con edición de texto (endpoint nuevo PUT /api/aprendizajes/:id) — hoy solo on/off en 2
  UIs con vocabulario distinto.
- `data/ajustes.json` + merge en config.js + vista **⚙️ Ajustes v1** (interruptor global,
  gating visible, ultimoClick).
  *Mejor que ayer*: Alejandro cambia un precio o apaga el bot completo sin tocar código ni
  reiniciar; por primera vez VE la persona de su bot.

### Etapa 3 — "Caminos v1" (2 semanas, el corazón)
- `caminos.js` + formato .md + índice + selección por turno (reemplaza
  activeAprendizajesText() en brain.js:55 detrás de un flag `CAMINOS_ON` para A/B con el
  juez: nota antes/después sobre los chats dorados; no se fija hasta igualar o superar).
- `migrar-reglas.mjs`: 68 reglas → ~20-30 caminos propuestos, aprobación en lote.
- TIPOS.CAMINO + token [[NOSE]] + pausa de tema + reanudación en caliente + push.
- Conflictos al guardar + git de data/caminos/ + edición conversacional.
- Métricas por camino (caminos-uso.jsonl + cruce con envios.jsonl) en la vista Conocimiento.
  *Mejor que ayer*: el bot pregunta lo que no sabe EN el momento, aprende al instante y esa
  venta no se enfría; el maletín sobrecargado (27-30 KB) baja a un prompt por turno con lo
  relevante.

### Etapa 4 — "Canal como enchufe" (1-1,5 semanas)
- `mensaje.js` (convId) + `turno.js` (el closure index.js:499-644 extraído con la interfaz
  Canal) + `canales/whatsapp/` (transporte.js = el index.js endurecido, casi sin tocar).
- identidad.json (absorbe enlaces.json); outbox con campo canal.
- El panel deja de re-extraer: consume los endpoints del bot (los 3 huérfanos
  GET /api/gym/lista, /api/dudas/chat, GET /api/control ganan consumidor o mueren).
  *Mejor que ayer*: mismo comportamiento, pero el sistema ya acepta un segundo canal; el
  panel y el bot dejan de contradecirse (comuna/precio calculados en UN solo lugar).

### Etapa 5 — "Instagram por la puerta oficial" (3-4 semanas, incluye esperas de Meta)
- **Gestión externa de Alejandro** (Guardián): crear la app en Meta, vincular la cuenta
  profesional de Instagram del negocio, permisos instagram_business_basic +
  instagram_business_manage_messages. Con Standard Access basta (cuenta propia con rol);
  sin App Review. Business Verification real: 3-14 días hábiles, a veces más.
- Worker CF `ig-buzon` (plantilla nueva pequeña en el maestro, patrón correo-worker):
  recibe webhook, guarda en D1, expone GET para el polling del Mac (timbre v2).
- `canales/instagram/adaptador.js` + política IG (ventana 24 h, sin typing, tope propio).
- Los caminos con `ambito: [instagram]` aplican solos; cotización/entrega idénticas (la
  identidad cruza por email/teléfono extraído cuando exista).
  *Mejor que ayer*: primer canal nuevo SIN tocar el cerebro ni el pipeline — la prueba de
  que dixdybot es multi-canal de verdad.

### Etapa 6 — "dixdybot producto" (continuo)
- **Promoción al maestro** (deuda doctrinal masiva: vivo 24 archivos/7.119 líneas vs
  maestro 12/1.912): subir TODO lo genérico a `DIXDY/whatsapp-bot/` (o renombrar a
  `dixdybot/`), datos del cliente SOLO en el clon (.env, data/, auth/, media/).
- Actualizar docs/24 (hoy documenta hasta la 2ª iteración) con este método.
- Cliente nuevo = clonar + .env + FORMULARIO-NEGOCIO.md → migrar-reglas.mjs inverso: sus
  primeros caminos nacen del formulario. Si se vende a terceros: API key por cliente
  (obligatorio por ToS) y presupuestar Haiku (~$27-40/mes por bot).

**Regla transversal de cada etapa**: prueba = `npm run check` + tests deterministas +
replay de dorados + nota del juez; huella con `actividad.py`; rollback = git revert (src y
data versionados); el bot vivo jamás se detiene más que el reinicio de launchd (~2 s de
reconexión, ya medidos).

---

## 5. Lo que NO se construye (doctrina DIXDY)

- **Ni bus de mensajes ni base de datos nueva**: jsonl + writeAtomic + Supabase existente.
  El volumen (decenas de chats/día) no justifica más, y el ledger append-only ya probó
  sobrevivir caídas.
- **Ninguna plataforma externa** (Chatwoot, Parlant, BuilderBot, Evolution): se copian sus
  modelos de datos (guidelines→caminos, Provider→Canal, Agent Bot→webhook futuro), no sus
  motores. El diferencial de dixdybot — pausa-y-aprende en caliente — no lo trae ninguna
  (verificado en el censo open source), así que adoptar plataforma sería cargar Rails o
  Python para igual construir lo importante a mano.
- **Ningún loop/cron nuevo**: los mismos launchd de hoy (bot, panel, aprender) + un
  healthcheck. Instagram entra por polling del patrón timbre, no por un daemon nuevo.
- **Ninguna API de Anthropic paralela**: llm.js es la única puerta; el fallback usa el
  brainApi que ya estaba escrito.

## 6. Riesgos y contingencias

1. **Baileys**: riesgo de ban residual (perfil solo-respuesta = el más bajo, nunca cero) y
   Bad MAC estructural (migración LID). Mitigación: gating intacto, sanación existente, y
   evaluar upgrade a 7.0.0-rc13 (mapeos LID) en sandbox con número de prueba + replays,
   NUNCA directo en producción. Plan B Cloud API documentado (§2.7).
2. **ToS Anthropic**: claude -p con Max para el bot del propio negocio es zona gris
   tolerada hoy, no un derecho; llm.js deja la conmutación a API a un flag de distancia y
   mide el costo real para decidir con números. Multi-cliente → API key por cliente, sin
   excepción.
3. **Latencia del aprendizaje en caliente** en rubro de urgencia: mitigada con respuesta
   enlatada inmediata + push + escalada a los 30 min + el bot sigue con los demás datos
   del mismo chat (pausa de tema, no de chat).
4. **Meta/Instagram**: tiempos de verificación no controlables (3-14 días o más); por eso
   la etapa 5 arranca el papeleo apenas la 4 esté en producción, y nada del resto depende
   de ella.
5. **Regresión por consolidar conocimiento** (68 reglas → caminos): el A/B con juez sobre
   chats dorados y el flag CAMINOS_ON hacen la transición medible y reversible; la nota
   4,0 del 22-jul es el listón a no bajar.
