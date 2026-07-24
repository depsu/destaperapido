# Auditoría de arquitectura — whatsapp-bot vivo (destaperapido)

**Código auditado:** `/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot` (commit `cf457ec`).
**Fecha:** 2026-07-23. **Alcance:** los 24 módulos de `src/` (≈7.119 líneas: 4.942 en `.js` + 2.177 en `.mjs`), `package.json`, `MANUAL.md`, `COORDINACION.md`, `ANALISIS-CEREBRO.md`, `bridge/`, `launchd/`, `data/`, `.env` (solo claves y valores operativos, sin secretos).

---

## 0. Resumen del sistema en una mirada

- **Stack:** Node ≥18, ESM, **3 dependencias** (`@whiskeysockets/baileys ^6.7.0`, `qrcode`, `qrcode-terminal`). Cero frameworks: HTTP con `node:http`, persistencia con JSONL/JSON a mano.
- **Tres procesos** que solo se hablan **por archivos en `data/`** (17 stores):
  1. **Bot** (`src/index.js`, launchd `com.dixdy.whatsapp-bot`, con `caffeinate`, KeepAlive).
  2. **Panel** (`src/dashboard.mjs`, 1.897 líneas, launchd `com.dixdy.whatsapp-dashboard`, :8789, ~50 endpoints).
  3. **Cron de aprendizaje** (`src/aprender.mjs`, launchd `com.dixdy.whatsapp-aprender`, cada hora).
- **Cerebro:** `claude -p` (BRAIN_MODE=cli, CLAUDE_MODEL=opus según `.env`), sin API key. Hay **4 implementaciones distintas** del spawn de `claude -p` (ver deuda D3).
- **Integración externa:** Python (`generar_cotizacion.py`/`enviar_cotizacion.py` del repo `cotizaciones-destape-rapido`, `bridge/entrega_bridge.py` → Supabase), avisos push con `avisar.py` del maestro DIXDY.
- **Valores operativos reales** (`.env`): `REPLY_DELAY_MS=30000`, `FOLLOWUP_DELAY_MS=12000`, `MAX_BOT_REPLIES_PER_CHAT=12`, `HISTORY_LIMIT=60`, `INTEGRACION_MODE=live`, `ULTIMO_CLICK=todo`, `BOT_PERSONA` de **10.599 caracteres** en una sola línea.

---

## (a) Mapa de módulos: responsabilidad y dependencias reales

### Proceso 1 — el bot (index.js)

| Módulo | Líneas | Responsabilidad | Depende de (imports reales) |
|---|---|---|---|
| `index.js` | 650 | **Orquestador-dios**: conexión Baileys, pairing por código, reconexión con backoff, dedup de mensajes, sanación Bad MAC, backfill de historial, presencia, recibos ✓✓, turno de respuesta completo (portero→contextos→cerebro→globos→typing→envío serializado), timer de 6s que dispara 4 subsistemas | baileys, `config`, `brain`, `entregas`, `precios`, `gating`, `integracion`, `faltantes`, `dudas`, `seguimiento`, `recordatorios`, `outbox`, `portero`, `store`, `enviar`, `quiet` |
| `config.js` | 208 | Parseo de `.env` sin libs; toda la config tipada + `withinBusinessHours()` | `node:fs` |
| `quiet.js` | 28 | Filtra el ruido de libsignal en stdout (estabilidad del stream) + timestamps en logs | — |
| `gating.js` | 225 | Estado por chat **en RAM** (historial, contador, timer, gen, typing), debounce con jitter, tope global 40/h·200/día, hidratación desde disco al arrancar | `config`, `store` |
| `store.js` | 532 | **Capa de persistencia**: conversaciones.jsonl, feedback, aprendizajes (jsonl + render .md), control.json (modo manual), etapas, archivados, datos-lead (ficha con merge manual>IA), envios.jsonl, estados.json (✓✓), presencia.json. Escritura atómica (`writeAtomic` con pid) | `config` |
| `brain.js` | 183 | Cerebro conmutable stub/cli/api; arma system prompt (persona + trato + reglas aprendidas + contexto); anti-inyección de roles; timeout 120s | `config`, `store`, `contacto` |
| `portero.js` | 40 | Filtro barato pre-LLM: ack ("gracias") → silencio; soporte de cliente antiguo → modo manual | — |
| `contacto.js` | 173 | pushName → nombre de pila + género (diccionarios locales) → bloque de trato para el prompt | `config` |
| `precios.js` | 492 | **Tarifario en código** (fuente única de precios), detección de comuna (con negación), cantidad y tiempo por regex, bloque de contexto con candado anti-invento, orden manual de IVA | `store` |
| `entregas.js` | 65 | Lee `entregas.json` del panel del repartidor, cruza por teléfono → contexto "no re-cotices" | `config` |
| `faltantes.js` | 134 | Qué falta para cotizar (ficha IA + rescate regex del historial) → bloque para que el bot lo pida | `store`, `config`, `precios` |
| `dudas.js` | 180 | **Buzón de dudas** (dudas.jsonl append-only con fold): el bot pregunta a Alejandro con opciones, la respuesta queda y no se repite; genera contexto de decisiones/encargos | `config`, `store` |
| `extraer.js` | 130 | Extractor IA de ficha/intención (JSON) sobre hasta 200 mensajes; gating barato (`valeAnalizar`); timeout 90s | `config` |
| `integracion.js` | 911 | **Motor de negocio**: orquesta extractor → merge ficha manual → normaliza fechas (fechaISO en español) → puertas (faltan datos / precio incoherente / último click) → cotización (PDF por Python + correo Resend + PDF por WhatsApp) → entrega (bridge → Supabase + aviso al repartidor). Dedup en RAM + envios.jsonl | `config`, `extraer`, `store`, `enviar`, `precios`, `dudas`, `faltantes` |
| `enviar.js` | 167 | **Envío robusto "en frío"**: resolverJid (calienta sesión Signal), enviarSeguro con typing, watchdog de ✓✓ (sana candado Bad MAC y reenvía 1 vez, umbrales 3min/30min según presencia) | `config`, `store` |
| `outbox.js` | 115 | Bandeja de salida persistente (`outbox.json`): el panel/recordatorios encolan, el bot drena cada 6s (máx 3/tick, reintentos, reconciliación anti-duplicado, PDF marcado apenas sale) | `config`, `store`, `enviar`, `gating` |
| `seguimiento.js` | 141 | Seguimiento único de leads tibios (~3h de silencio, ventana 9-21, máx 2/ronda), redactado por el cerebro | `config`, `brain`, `store`, `gating`, `enviar`, `integracion` |
| `recordatorios.js` | 151 | Recordatorios 💤 agendados desde el panel (texto o IA), auto-cancelación si el chat revive, salen por el outbox | `config`, `brain`, `store`, `outbox`, `enviar`, `integracion` |
| `calidad.js` | 344 | Notas 👍👎/1-5, juez IA (opus), replay 🎬 con actor IA, resumen semanal; `calificaciones.jsonl` | `config`, `store`, `brain`, `precios` |
| `link-qr.js` / `link-code.mjs` | 73/127 | Utilidades de vinculación (QR / código) | baileys |

### Proceso 2 — el panel

| Módulo | Líneas | Responsabilidad |
|---|---|---|
| `dashboard.mjs` | 1.897 | Servidor HTTP local (:8789): lista de chats + Kanban (etapa derivada por heurística), **ficha determinista propia** (regex de comuna/precio/teléfono/hora/respaldo, `fichaDeterminista` L358), merge con ficha IA (`mergeIA` L410), pedidos por chat (`jid#2`), enlaces chat↔entrega, entregas en vivo desde Supabase, cotizar/entregar manual, correos del lead, feedback/aprendizajes, dudas, calidad, gimnasio + replays. Sirve `web/dashboard.html` (191 KB) y `web/entrenar.html` |
| `aprender-core.mjs` | 126 | Destila feedback → reglas con `claude -p` (lo llaman el cron y el panel al instante) |
| `aprender.mjs` | 27 | Cron horario: `aprenderPendientes()` + `juezAuto(2)` |

### Piezas fuera de src/
- `bridge/entrega_bridge.py` (2,3 KB): stdin JSON → reusa `resumen_repartidor.py` + `sync_entregas_supabase.py` del repo de cotizaciones (ruta absoluta hardcodeada L17).
- Tests: 4 scripts manuales en la raíz (`_selftest.mjs`, `_smoke-brain.mjs`, `_test-precios.mjs` de 14 KB, `_test-calidad.mjs`). Sin framework ni CI.

---

## (b) Flujo completo de un mensaje entrante → respuesta

Numerado, con el módulo y dónde vive el estado (**RAM** vs **DISCO**):

1. **Llega el evento** `messages.upsert` (Baileys) → `handleMessage` (`index.js:434`). Se saltan `status@broadcast`, grupos (`IGNORE_GROUPS`), ecos `fromMe` en tipo "append" (`index.js:383`, fix del incidente 22-jul).
2. **Dedup por id** en `seenMsgIds` (**RAM**, Set con evicción 8000→2000, `index.js:443-449`). Un reinicio lo pierde (mitigado por la ventana de frescura del paso 5).
3. **Mensaje indescifrable** (stub CIPHERTEXT = Bad MAC): registra huella en el panel, sana la sesión Signal (`enviar.sanarSesion` borra `auth/session-*.json`, throttle 10 min) y a los 90s pide reenvío si no se recuperó (`index.js:457-459, 92-143`).
4. **Extracción de texto** (`extractText`, `index.js:57`): texto, caption, ubicación→link de Maps, adjuntos como etiqueta ("📷 Foto").
5. **Frescura**: solo se responde a mensajes de <120s (600s si vienen re-entregados tras una caída). Lo viejo solo se registra a **DISCO** (`recordMessage` → `conversaciones.jsonl`) sin efectos (`index.js:473-478`).
6. **Si escribió el dueño** (`fromMe`): `gating.onOwnerMessage` — cancela el timer pendiente, persiste, y activa **modo manual** en `control.json` (**DISCO**, compartido con el panel): TTL 30 min si fue un toque, pausa indefinida si lleva ≥3 mensajes (`OWNER_MANUAL_STICK_AFTER`, `gating.js:81-104`). Fin.
7. **Si escribió el cliente**: `gating.onClientMessage` — push al historial (**RAM**, ventana = max(HISTORY_LIMIT=60, EXTRACT_HISTORY_LIMIT=200)), `gen++` (invalida turnos anteriores), persiste a `conversaciones.jsonl` (**DISCO**). `index.js` guarda además `lastClientKey`, `clientNames`, `clientPhones` (**RAM**, Maps propios, `index.js:83-87`) y se suscribe a presencia.
8. **Debounce**: `scheduleReply` arma un timer con jitter ±30% — 30s la primera respuesta, 12s las siguientes; si el cliente está "escribiendo", re-chequea cada 3s hasta 10 veces (`gating.js:161-187`).
9. **Al disparar el timer** (`index.js:499`): captura `gen`; lanza **en paralelo y fire-and-forget** `procesarIntegracion` (paso 15) — deliberadamente desacoplada de la respuesta.
10. **Compuertas**: `canBotReply` (lee `isManual` de `control.json` **DISCO** en cada llamada + `ownerReplied`/`botReplies` **RAM** + tope global **RAM** ventana deslizante) → `withinBusinessHours` → **portero** (`portero.decidir`: "gracias" suelto = silencio; soporte = pasa a manual y calla).
11. **Armado del maletín** (los 4 contextos, `index.js:554-567`):
    - `contextoEntrega` (lee `entregas.json` del repartidor, **DISCO externo**, cruce por teléfono),
    - `contextoTarifario` (`precios.js`: comuna/cantidad/tiempo por regex sobre el historial RAM + respaldo de la ficha `datos-lead.json` **DISCO**; kit incompleto = cero precios; sin comuna = candado "PROHIBIDO dar números"; a la 2ª repregunta = abanico),
    - `contextoFaltantes` (solo si la ficha dice `quiere_cotizacion`),
    - `contextoDudas` (decisiones ya resueltas por Alejandro en `dudas.jsonl` **DISCO**).
12. **Cerebro** (`brain.getReply` → `brainCli`): system prompt = `BOT_PERSONA` (10.599 chars del `.env`) + bloque de trato (`contacto.js`) + **reglas aprendidas** (`aprendizajes.jsonl` **DISCO**, ~66 activas) + contextos + reglas de formato; transcript = últimos 60 mensajes con roles neutralizados (anti-inyección). `claude -p --model opus`, timeout 120s; si falla, **un** reintento a los 5s re-validando gen (`index.js:571-576`).
13. **Post-proceso**: `[[SILENCIO]]` → nada; re-chequeo `canBotReply`+gen; token `[[FOTO]]` → adjunta `FICHA_IMG`; split por `///` en máx 3 globos, sin punto final.
14. **Envío**: `enviarSerializado` (**cola global RAM**: una "persona" no tipea en 3 chats a la vez; pausa 1,5-4,5s entre turnos) → por globo: `simulateTyping` proporcional + `sock.sendMessage` → `onBotMessage` persiste el globo con su id y engancha el `waId` en `estados.json` (**DISCO**) para pintar ✓/✓✓. `countBotTurn` suma 1 al tope del chat (**RAM**). Presencia "online" solo transitoria.
15. **Rama de integración (paralela)** (`integracion.procesarIntegracion:694`): dedup por `enVuelo` (**RAM**) + `yaCotizado(45d)`/`yaDespachado(∞)` contra `envios.jsonl` (**DISCO**) → gating barato `valeAnalizar` (email o palabra de cierre) → **extractor IA** (`claude -p`, hasta 200 msgs) → merge con campos manuales de la ficha → `fechaISO` normaliza fechas en español → refresca `datos-lead.json` → puertas:
    - faltan datos → lo pedirá el propio bot vía `contextoFaltantes` (próximo turno);
    - precio no calza con `precioCoherente` (tarifario + precios dichos por el dueño) → **duda** al buzón con opciones (o aplica la respuesta previa);
    - todo calza + `ULTIMO_CLICK=todo` → duda "¿la mando?" (nada sale sin click);
    - confirmó entrega completa → duda "¿despacho?"; con `off` despacharía solo: PDF por Python, correo Resend, PDF por WhatsApp (`enviarSeguro`), `entrega_bridge.py` → Supabase, aviso al repartidor, `logEnvio` apenas sale lo irreversible.
16. **Recibos**: `messages.update` **y** `message-receipt.update` (los @lid llegan por el segundo) → `setEstadoStatus` (estados.json) + `confirmarEntrega` libera el watchdog de `enviar.js` (**RAM** Map `pendientes`).
17. **Timer de 6s** (`index.js:423-431`): drena outbox, corre el watchdog de ✓✓, seguimientos (throttle 5 min) y recordatorios (throttle 1 min).

### Estado: qué vive dónde

| RAM (se pierde al reiniciar) | DISCO (`data/`, sobrevive) |
|---|---|
| historial por chat (rehidratado al boot), `botReplies` (¡el tope 12 se resetea!), timers/gen, typing, `seenMsgIds`, tope global de envíos, cola de envío serializado, `pendientes` del watchdog, `enVuelo`, `clientNames/clientPhones/lastClientKey`, `estado` cotizado/despachado (respaldado por envios.jsonl) | `conversaciones.jsonl`, `control.json`, `etapas.json`, `archivados.json`, `datos-lead.json`, `envios.jsonl`, `estados.json`, `presencia.json`, `dudas.jsonl`, `feedback.jsonl`, `aprendizajes.jsonl(+md)`, `calificaciones.jsonl`, `outbox.json`, `seguimientos.json`, `recordatorios.json`, `enlaces.json`, `pedidos.json` |

---

## (c) Deuda técnica concreta

**D1. `index.js` es un módulo-dios (650 líneas).** Mezcla ciclo de vida de la conexión, pairing, dedup, sanación criptográfica, backfill, presencia, recibos y TODO el turno de respuesta en un closure de ~145 líneas (`index.js:499-644`). Cualquier cambio de canal (Instagram) obliga a reescribirlo: no hay frontera entre "transporte WhatsApp" y "lógica del turno".

**D2. Acoplamiento total al canal.** El `sock` de Baileys viaja crudo por `integracion.js`, `seguimiento.js`, `outbox.js`, `enviar.js` e `index.js`, y el `jid` de WhatsApp es la clave primaria de los 17 stores. No existe una abstracción "canal" ni "identidad de contacto" (el cruce teléfono↔jid se re-implementa en `entregas.js:16`, `dashboard.mjs:921 tel9`, `integracion.js:423`).

**D3. Cuatro spawns de `claude -p` distintos e inconsistentes:** `brain.js:102` (timeout 120s), `extraer.js:96` (90s, **sin** `--model`: hereda el default del CLI), `calidad.js:186` (150s), `aprender-core.mjs:28` (**sin timeout**: un claude colgado deja el cron/panel colgado). No hay un runner común con cola/limite de concurrencia: un burst de chats puede lanzar N procesos opus en paralelo.

**D4. Detección de comuna duplicada y DIVERGENTE.** `precios.js:88 detectarComuna` (40 céntricas + lejanas; gana el match más reciente/largo; maneja la negación "no en Maipú") vs `dashboard.mjs:314 detectComuna` (lista distinta de 48 comunas que incluye Pirque; gana la PRIMERA mención; sin negación). El bot y el panel pueden mostrar comunas distintas para el mismo chat. Ídem precio: 3 regex distintas (`dashboard.mjs:329`, `integracion.js:246`, `seguimiento.js:42`).

**D5. Estado duplicado RAM/disco con semántica distinta.** (a) El historial vive en RAM y en `conversaciones.jsonl`; `seguimiento.js` usa el historial RAM (`getHistory`) pero `recordatorios.js` relee el disco — dos fuentes para lo mismo. (b) `names` (gating) y `clientNames` (index) son dos copias del pushName. (c) `botReplies` (tope por chat) es solo RAM: cada reinicio del bot (KeepAlive de launchd) regala 12 respuestas nuevas. (d) `estado` cotizado/despachado (Map) + `envios.jsonl`: el patrón correcto existe, pero conviven ambos.

**D6. Persistencia con dos niveles de robustez.** `store.js` escribe atómico (tmp+rename con pid, `store.js:38`), pero `outbox.json`, `seguimientos.json`, `recordatorios.json`, `enlaces.json` y `pedidos.json` usan `writeFileSync` directo y read-modify-write **sin lock entre procesos** (panel encola / bot reconcilia el mismo outbox.json; la carrera está reconocida y solo mitigada en `outbox.js:44-55`).

**D7. La configuración es un prompt.** `BOT_PERSONA` = 10.599 caracteres en UNA línea del `.env`: es a la vez persona, política comercial, manual de formato y reglas de venta. Las instrucciones del bot viven en TRES capas que pueden contradecirse — persona (.env), bloques de sistema (`precios.js`, `faltantes.js`, `dudas.js`) y ~66 reglas aprendidas (`aprendizajes.jsonl`) — y `ANALISIS-CEREBRO.md` §4 documenta los choques reales (reserva §4.2, recinto especial §4.3, dilución §4.1: reglas de IVA repetidas 5 veces, reglas corruptas generadas por el destilador, montos de ejemplo copiados como precios reales en la sim H4).

**D8. Documentación desfasada del vivo.** `MANUAL.md` dice espera de ~60s y tope 3-4 (real: 30s y 12), y apunta a `~/SaSS/DIXDY/whatsapp-bot` (el template maestro); el vivo diverge y está en `SaSS/destaperapido/whatsapp-bot` (`COORDINACION.md` lo admite: "promover al maestro" sigue pendiente).

**D9. Rutas absolutas hardcodeadas** a la máquina de Alejandro: `integracion.js:55` (`avisar.py`), `aprender-core.mjs:19` (`actividad.py`), `bridge/entrega_bridge.py:17` (scripts del repartidor). Un clon para otro cliente/máquina se rompe en silencio (los spawns fallan best-effort).

**D10. `dashboard.mjs` monolito (1.897 líneas) + `web/dashboard.html` (191 KB, una sola página).** Servidor, ~50 rutas, extracción determinista, heurística de Kanban, Supabase, pedidos `jid#2`, gimnasio y replays en un archivo; re-implementa lógica del bot (D4) en vez de consumirla.

**D11. Higiene:** `tmp/` acumula 129 `coti-*.json/pdf` sin limpieza (datos de clientes en texto plano), `bot.error.log` de 5,7 MB, 6 carpetas `auth.dañada-*`/backups en la raíz, `data/` con .bak sueltos. `.env.bak-*` con secretos junto al `.env`.

**D12. Sin tests automatizados del flujo.** Solo 4 scripts manuales en la raíz; nada cubre el turno completo, las carreras gen/outbox ni la integración (que ya produjo incidentes reales: duplicados 16-jul, pausas fantasma 22-jul — hoy parchados con guardas puntuales).

---

## (d) Qué es rescatable para el rediseño (dixdybot) y qué no

### Rescatable TAL CUAL (piezas maduras, endurecidas por incidentes reales)
- **`enviar.js`** — envío en frío robusto: calentar sesión, watchdog de ✓✓ con presencia, sanación Bad MAC con reenvío único. Es conocimiento anti-ban pagado con incidentes; solo necesita recibir un "canal" en vez del sock.
- **`outbox.js`** — cola de salida persistente con reconciliación anti-duplicado y goteo. Es el patrón correcto para "cualquier proceso externo envía por el canal del bot".
- **`dudas.js`** — **el embrión exacto de los "caminos"**: el bot detecta que no sabe, pausa esa acción, pregunta al humano con opciones + acción ejecutable, y la respuesta queda guardada y no se repite (`respuestaPrevia`). El rediseño debe generalizarlo (hoy solo cubre precio/cotizar/entrega), no reinventarlo.
- **`precios.js` como PATRÓN** — "los números viven en código, el modelo redacta": kit comuna+cantidad+tiempo calculado por el sistema, candado anti-invento, abanico a la 2ª repregunta. Los datos son de destaperapido; la arquitectura (tarifario-como-config + detectores + bloque generado) es el corazón de un "camino de precios" reutilizable.
- **`gating.js` (los conceptos)** — debounce con jitter, generación `gen` para invalidar turnos, tope por chat + tope global, auto-pausa cuando el dueño interviene (con umbral de takeover). Portable a cualquier canal.
- **`portero.js`, `contacto.js`, `quiet.js`** — pequeños, puros, sin acoplamientos.
- **`extraer.js` (el prompt)** — el schema del extractor con sus reglas anti-precio-ancla/IVA/fechas es conocimiento destilado valioso; el mecanismo de spawn se unifica (D3).
- **`store.js` (las primitivas)** — JSONL append-only + fold, escritura atómica, patrón "manual gana sobre IA" (`conManual`). Para multi-canal conviene una capa única, pero estas primitivas son la base.
- **`aprender-core.mjs` y `calidad.js`** — el loop feedback→regla y el trío juez/actor/replay son directamente la infraestructura de entrenamiento del dixdybot (con el runner unificado y consolidación de reglas pendiente).
- **`bridge/entrega_bridge.py`** — el patrón "puente stdin-JSON que reusa el ecosistema" es doctrina DIXDY bien aplicada (solo parametrizar la ruta).

### Rescatable CON CIRUGÍA
- **`integracion.js` (911 líneas)** — dentro hay funciones puras excelentes y testeadas (`construirConfigCotizacion`, `construirEntrega`, `construirCuerpoCorreo`, `fechaISO`, `precioCoherente`) que deben extraerse como unidades; el orquestador `procesarIntegracion` (extraer→puertas→acciones) hay que partirlo en pipeline de pasos declarativos — es donde nacerán los "caminos".
- **`index.js`** — rescatar la lógica (frescura, ecos append, serialización, recibos duales) pero separada en: adaptador-WhatsApp / gestor-de-turno / scheduler. Tal cual, no.
- **`brain.js`** — la costura stub/cli/api y el armado del prompt sí; el runner se unifica con los otros 3 (D3).

### NO rescatable para el rediseño
- **`dashboard.mjs` + `web/dashboard.html`** como están: el panel nuevo debe consumir una API sobre la MISMA lógica del bot (matar la extracción duplicada D4), no llevar la suya.
- **`BOT_PERSONA` monolítica en `.env`**: descomponer en persona corta + políticas en código/caminos + reglas consolidadas (~66→~30 como propone `ANALISIS-CEREBRO.md` §4.1). La config-como-prompt de 10 KB es la causa raíz de la dilución.
- **El acoplamiento jid/sock como identidad global** (D2): multi-canal exige contacto-con-identidades (wa:…, ig:…) desde el día 1.
- **Los 17 stores sueltos con doble nivel de robustez** (D6): el rediseño necesita una capa de estado única (aunque siga siendo archivos), con lock/atомicidad pareja entre procesos.

### Veredicto
El sistema está **mucho mejor de lo que su forma sugiere**: casi cada rareza es una cicatriz documentada de un incidente real (los comentarios son una bitácora excepcional). Lo que está agotado no es la lógica sino la **topología**: un orquestador-dios, un canal cableado en todas partes, tres capas de instrucciones al modelo y lógica duplicada entre bot y panel. El rediseño dixdybot debería ser una **reorganización con trasplantes** (enviar/outbox/dudas/gating/precios-patrón/aprendizaje casi intactos detrás de interfaces de canal y de estado), no una reescritura desde cero.
