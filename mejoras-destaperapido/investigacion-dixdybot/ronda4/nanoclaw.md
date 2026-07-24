# nanoclaw (nanocoai/nanoclaw) — planos para dixdybot E1+E4

Licencia: **MIT** (LICENSE, "Copyright (c) 2026 Gavriel") — copiar patrones y hasta código con atribución es legal.
Clon leído: `/private/tmp/claude-501/-Users-alejandroriveracarrasco-SaSS-DIXDY-clientes-destaperapido/5acfd0ef-e8b4-49b2-965d-26a7a76d1c5b/scratchpad/clones/nanoclaw` (main, v2.1.53, + branch `channels` fetcheada para el adaptador WhatsApp).

Qué es: asistente personal multi-canal. Host Node (better-sqlite3) + agente en contenedor Docker (Bun + `@anthropic-ai/claude-agent-sdk`). Todo el IO host↔contenedor son **dos SQLite montados por sesión** (inbound.db / outbound.db), un escritor por archivo. Los canales NO viven en trunk: se instalan como **skills** que copian el adaptador desde la rama `channels` y agregan UNA línea de import al barrel.

---

## (a) Estructura completa (carpetas y responsabilidades)

```
src/                        HOST (proceso único Node)
  index.ts                  orquestador delgado: DB → migraciones → adapters → delivery polls → sweep → CLI socket
  router.ts                 inbound → messaging_group → gates → fanout a agentes → sesión → wake
  session-manager.ts        carpetas de sesión + escritura messages_in + adjuntos (inbox/outbox) + invariantes cross-mount
  delivery.ts               polls de salida (1s activos / 60s barrido), dedup, retries, acciones de sistema
  host-sweep.ts             mantenimiento: resetear 'processing' huérfanos, matar contenedores colgados (heartbeat)
  container-runner.ts       spawn de contenedor por sesión (mounts, imagen por grupo, dedup de wakes)
  circuit-breaker.ts        backoff si el host reinicia en loop
  command-gate.ts           clasifica slash-commands antes de llegar al contenedor (deny/filter/pass)
  claude-md-compose.ts      compone el CLAUDE.md del agente desde base + fragmentos de skills (cada spawn)
  channels/                 adapter.ts (CONTRATO), channel-registry.ts, chat-sdk-bridge.ts, cli.ts, ask-question.ts
  db/                       central v2.db: schema.ts (referencia), migrations/ (001..019+), sessions, messaging-groups,
                            container-configs (config de agente EN LA DB), session-db.ts (SQL de los DB por sesión)
  modules/                  módulos enchufables por hooks: typing, permissions (resolver de remitente + gates),
                            approvals, scheduling, interactive, agent-to-agent, self-mod, mount-security
  providers/                registro host-side de config de contenedor por proveedor LLM
  guard/                    especificaciones de guardia para acciones privilegiadas (allow/hold/deny + re-entrada aprobada)
  cli/                      `ncl` sobre unix socket (data/ncl.sock): CRUD de wirings, tasks, delivery-action
container/
  Dockerfile, entrypoint    imagen base; imagen por-grupo si el agente instala paquetes
  agent-runner/src/         RUNNER dentro del contenedor (Bun):
    poll-loop.ts            loop: lee messages_in → prompt → provider.query() → escribe messages_out
    formatter.ts            envuelve mensajes en XML; extrae routing
    providers/claude.ts     invocación del Agent SDK (resume, hooks, rotación de transcript)
    mcp-tools/              send_message, ask_user_question, scheduling, self-mod (servidor MCP propio)
    db/                     messages-in (RO), messages-out (escritor), session-state (continuation)
  skills/                   skills compartidas montadas RO en /app/skills
.claude/skills/add-*        CANALES Y FEATURES COMO SKILLS: add-whatsapp, add-telegram, add-slack, add-discord,
                            add-imessage, add-signal, add-matrix… cada una copia código + agrega 1 import + REMOVE.md
setup/, scripts/, docs/     wizard de instalación, utilidades, arquitectura (docs/architecture.md, db-session.md)
```

Patrón clave para dixdybot E6: **el trunk es genérico; cada canal/feature es una skill idempotente** con directivas `nc:` parseables (prompt/run/copy/append/dep) y un `REMOVE.md` para desinstalar. Eso ES "módulos administrables" sin panel: el instalador es un documento ejecutable.

## (b) Contrato del adaptador de canal — `src/channels/adapter.ts`

Interfaz `ChannelAdapter` (v2):

- Identidad: `name`, `channelType` (clave semántica), `instance?` (N bots de la misma plataforma), `supportsThreads` (Discord/Slack=true; WhatsApp/Telegram=false → el router anula threadId).
- Ciclo de vida: `setup(config: ChannelSetup)`, `teardown()`, `isConnected()`.
- Salida: `deliver(platformId, threadId, OutboundMessage) → Promise<platformMsgId|undefined>`; opcionales `setTyping`, `syncConversations`, `resolveChannelName`, `subscribe`, `openDM`.
- `defaults?: ChannelDefaults` — declaración estática por contexto DM/grupo: `engageMode` ('pattern'|'mention'|'mention-sticky'), `engagePattern` (con token `{name}`), `threads`, `unknownSenderPolicy` ('strict'|'request_approval'|'public'), más `mentions: 'platform'|'dm-only'|'never'`.

`ChannelSetup` (lo que el host entrega al adaptador): `onInbound(platformId, threadId, InboundMessage)`, `onInboundEvent(event)` (transporte admin/CLI), `onMetadata(platformId, name?, isGroup?)`, `onAction(questionId, selectedOption, userId)` (respuesta a tarjeta/pregunta).

**Normalización del mensaje** (`InboundMessage`): `{ id, kind:'chat'|'chat-sdk', content: objeto JS (el host lo stringify-ea), timestamp, isMention?, isGroup? }`. La decisión de "¿me mencionaron?" es DEL ADAPTADOR (semántica de la plataforma); el router NO hace fallback por texto. El host estampa `instance` en `src/index.ts` — los adaptadores son ciegos a la instancia.

Registro: `registerChannelAdapter(type, { factory, defaults, containerConfig })`; la **factory devuelve `null` si faltan credenciales** y el canal queda apagado sin romper el boot.

## (c) Router / host — conversación→agente y aislamiento de sesiones (`src/router.ts`)

Pipeline `routeInbound(event)`:

1. **Interceptores** de módulos (primero que reclama, gana) — capturan respuestas de texto libre en flujos de aprobación multi-paso.
2. **Política de threads** del adaptador receptor (no-thread → threadId=null).
3. Lookup combinado `messaging_group + conteo de agentes` en UNA query; si no existe, **auto-crea solo si isMention** (chatter en grupos donde el bot está de oyente no toca la DB).
4. Sin wirings: si `denied_at` → drop silencioso; si no → `recordDroppedMessage(reason:'no_agent_wired')` + **channelRequestGate**: el módulo de permisos manda TARJETA al dueño ("¿conecto este chat?") y re-inyecta el evento vía `routeInbound` tras aprobar. Esto es exactamente la "pausa-y-pregunta al dueño" de nuestra E3.
5. `senderResolver` (hook) upserta el user namespaced (`phone:+56...`, `tg:123`).
6. **Fanout**: por cada agente cableado evalúa `engage_mode` ('pattern' regex / 'mention' / 'mention-sticky' = mención O sesión ya viva en ese thread), + `accessGate` + `senderScopeGate`. Si no engancha pero `ignored_message_policy='accumulate'` → guarda el mensaje con `trigger=0` (contexto silencioso, no despierta).
7. `resolveSession(agentGroupId, mgId, threadId, session_mode)` — modos `'shared'` (1 sesión por chat), `'per-thread'`, `'agent-shared'` (1 sesión para todo el agente). **Sesión = carpeta + par de DBs + contenedor propio**: aislamiento por filesystem, no por memoria.
8. `gateCommand` (slash admin) → deny escribe la negativa directo a messages_out sin despertar contenedor.
9. `writeSessionMessage(...)` con id namespaced `${msgId}:${agentGroupId}` (el mismo inbound aterriza en N DBs de sesión sin colisión de PK) → `wakeContainer` + typing.

Tabla de auditoría `dropped_messages` para TODO drop estructural o de política — nada se pierde en silencio.

## (d) inbound.db / outbound.db — esquema exacto, escritores, dedup, reinicios

Fuente: `src/db/schema.ts` (INBOUND_SCHEMA / OUTBOUND_SCHEMA), `src/session-manager.ts` (invariantes), `src/delivery.ts`, `src/host-sweep.ts`, `container/agent-runner/src/db/messages-out.ts`.

**inbound.db (escribe SOLO el host; el contenedor lo abre read-only):**
- `messages_in(id PK, seq UNIQUE, kind, timestamp, status 'pending|processing|completed|failed', process_after, recurrence, series_id, tries, trigger 0|1, platform_id, channel_type, thread_id, content JSON, source_session_id, on_wake)`
- `delivered(message_out_id PK, platform_message_id, status, delivered_at)` — el host anota aquí lo entregado para **no escribir jamás el archivo del contenedor**.
- `destinations(name PK, type 'channel|agent', …)` — mapa de destinos del agente, reescrito por el host en cada wake y consultado en vivo.
- `session_routing(id=1, channel_type, platform_id, thread_id)` — fila única con el chat actual.

**outbound.db (escribe SOLO el contenedor; el host lo abre readonly):**
- `messages_out(id PK, seq UNIQUE, in_reply_to, timestamp, deliver_after, recurrence, kind, platform_id, channel_type, thread_id, content JSON)`
- `processing_ack(message_id PK, status, status_changed)` — el contenedor marca procesado AQUÍ en vez de tocar messages_in.
- `session_state(key, value)` — guarda el session-id del SDK (la "continuation") para resume tras reinicio.
- `container_state(id=1, current_tool, tool_declared_timeout_ms, …)` — herramienta en vuelo, para que el sweep tolere Bash largos.

**Los 3 invariantes cross-mount** (header de `src/session-manager.ts`, oro puro):
1. `journal_mode=DELETE`, **no WAL** — el `-shm` mmapeado de WAL no se refresca host→guest (VirtioFS): el contenedor se congelaría en un snapshot viejo.
2. El host **abre-escribe-CIERRA en cada operación** — cerrar invalida el page cache del otro lado; una conexión larga congela la vista.
3. **Un escritor por archivo** — el unlink del journal DELETE no es atómico a través del mount; dos escritores corrompen.
Única excepción controlada: `writeOutboundDirect` (host escribe la negativa de un comando en outbound.db con `INSERT OR IGNORE` y **seq PAR**).

**seq par/impar**: host = pares (`nextEvenSeq`), contenedor = impares (`writeMessageOut` lee MAX(seq) de AMBAS DBs y toma el siguiente impar). No es solo anti-colisión: `seq` es el ID de mensaje que ve el agente (`send_message` devuelve seq; `edit/react` lo aceptan) y `getMessageIdBySeq` busca en ambas tablas — namespaces disjuntos = imposible resolver la fila equivocada.

**Dedup de entrega** (`src/delivery.ts`): dos polls (1s sesiones con contenedor corriendo, 60s todas las activas) llaman al mismo drenaje → `inflightDeliveries: Set<sessionId>` rechaza reentradas; luego filtra `getDueOutboundMessages` contra `getDeliveredIds` (tabla delivered); `markDelivered` es INSERT OR IGNORE; 3 intentos y `markDeliveryFailed`. El contador de intentos vive en RAM **a propósito**: reiniciar el host da una segunda oportunidad a lo fallado.

**Reinicios**: (i) contenedor arranca → `clearStaleProcessingAcks()` (recupera lo reclamado por un crash); (ii) host-sweep: si el contenedor NO corre y hay filas 'processing' → reset a pending con backoff exponencial y `tries++` (MAX 5 → failed); (iii) vida del contenedor = **mtime de un archivo `.heartbeat`** (no polls a DB), techo absoluto 30 min extendido por el timeout declarado del Bash en vuelo; (iv) corrupción de lectura cross-mount (Docker Desktop macOS): 10 errores seguidos "database disk image is malformed" → `process.exit(75)` y el sweep re-spawnea con mount fresco.

## (e) Invocación del Agent SDK y qué haríamos con `claude -p`

`container/agent-runner/src/poll-loop.ts` + `providers/claude.ts`:

- **Una query de larga vida por turno-batch, con streaming input**: `sdkQuery({ prompt: MessageStream })` donde MessageStream es un async-iterable push. Mientras la query está viva, un poll de 500ms **empuja los follow-ups al mismo stream** (`query.push`) en vez de re-spawnear el subproceso (~segundos) y recargar el transcript. El prompt-cache de Anthropic es server-side (TTL 5 min por prefijo), así que cerrar/reabrir dentro de 5 min igual pega cache.
- **Resume**: `options.resume: continuation`. La continuation se persiste en `session_state` **apenas llega el evento `init`** (no al final del turno) — un crash a mitad de turno no huerfanea la conversación. Keyed por proveedor (una continuation de Codex nunca se le pasa a Claude).
- **Sesión inválida**: regex `no conversation found|ENOENT.*\.jsonl|session.*not found` → limpiar continuation y partir fresco en el próximo intento.
- **Rotación de transcript** (`maybeRotateContinuation`): >12MB o >14 días → archivar resumen markdown a `conversations/` (hook PreCompact hace lo mismo en compactación) y renombrar el .jsonl para que el SDK parta sesión nueva. Sin esto, un hub longevo se cuelga recargando un transcript gigante y el sweep lo mata en loop.
- **Permisos**: `permissionMode:'bypassPermissions'` — el sandbox ES el contenedor (mounts RO/RW + egress lockdown + proxy OneCLI que inyecta credenciales en el wire; el token NUNCA entra al contenedor). `allowedTools` explícito + patrones `mcp__<server>__*`; `disallowedTools` para los builtins que colgarían headless (AskUserQuestion, plan mode…), con hook PreToolUse como defensa doble.
- **Protocolo de salida**: el agente debe envolver TODO en `<message to="destino">…</message>`; texto suelto = scratchpad. Si un turno termina sin bloques → **nudge automático** (`<system>Your response was not delivered…</system>`) una vez por turno. En sesiones de tarea rige "una sola puerta": solo la tool `send_message` entrega; el texto final va al run-log.
- **Rate limit**: el evento `rate_limit_event` del SDK es telemetría; SOLO `status:'rejected'` bloquea, y distingue `credits_required` (billing) de ventana transitoria.

**Para dixdybot E1 (`llm.js` puerta única con `claude -p`)** — igual: persistir session-id apenas se conozca y usar `--resume`; regex de sesión inválida → retry fresco; rotación por tamaño/edad del transcript con archivo-resumen; clasificación de errores (retryable/quota/billing) en la puerta; el protocolo `<message to>` + nudge es directamente portable (nuestro cerebro ya devuelve texto plano). Distinto: `claude -p` no tiene streaming-input ni hooks → no podemos empujar follow-ups a un turno vivo; lo compensamos como hoy (batch por invocación) y su patrón de "marcar processing → completar al result" calza igual. Sus MCP tools del runner (send_message/ask_user_question) equivalen a nuestras acciones estructuradas en la respuesta.

## (f) Baileys v7 (de ellos) vs 6.7.23 (nuestro) — `channels-branch/whatsapp.ts` (rama `channels`, `src/channels/whatsapp.ts`)

Pinean `@whiskeysockets/baileys@7.0.0-rc.9` y lo anotan como "last release, **unmaintained**". Lo que su adaptador resuelve y nosotros deberíamos robar:

1. **LID** (el motivo real del upgrade): WhatsApp está migrando a LIDs. v7 trae `remoteJidAlt`/`participantAlt` en cada mensaje + `sock.signalRepository.lidMapping.getPNForLID` + evento `lid-mapping.update`. Su `translateJid` resuelve SIEMPRE a JID de teléfono antes de emitir al router (cache local → altJid → signalRepository). Nuestro 6.7.23 no tiene nada de esto; cuando WhatsApp active LID en más chats, el enrutamiento por JID de nuestro CRM se rompe.
2. **Versión de WA Web** (`resolveWaWebVersion`): la versión hardcodeada de Baileys caduca en semanas → 405 en la capa Noise. Ellos scrapean `wppconnect.io/whatsapp-versions/` con fallback a `fetchLatestWaWebVersion`, y ABORTAN si ninguna responde. Robable HOY tal cual para 6.7.23.
3. **"Esperando el mensaje"**: doble mitigación — `getMessage` devuelve el mensaje desde `sentMessageCache` (256 entradas) o `proto.Message.create({})` para cortar la espera infinita; y `cachedGroupMetadata` devuelve la metadata **SIN traducir participantes** (traducir LID→phone con `addressingMode='lid'` desincronizaba la distribución de sender-keys — la causa raíz del síntoma que nosotros curamos a posteriori con la auto-sanación de enviar.js). La suya es prevención; la nuestra es cura. Copiar ambas.
4. **Reconexión**: en `connection.close`, si `reason !== DisconnectReason.loggedOut && !shuttingDown` → reconectar ya, con reintento a 5s. `loggedOut` → borrar `store/auth/` (creds muertas que van a 401 en loop y gatillan el cooldown de WhatsApp). En shutdown limpio → **NO tocar auth** (antes cada `systemctl restart` forzaba re-parear) y **no reconectar en paralelo**: un `connectSocket()` simultáneo con el exit trunca `creds.json` a 0 bytes. Gotcha extra v7: para pedir pairing code usar `state.creds.me` y no `creds.registered` (v7 no re-levanta el flag tras el restart 515 → pediría código nuevo, 401, y se auto-borra el auth).
5. **Cola de salida offline**: `outgoingQueue` cuando `!connected` o al fallar un send, flush al reconectar — nuestro bot pierde/reintenta distinto; esto es más simple y probado.
6. **fromMe en self-chat**: filtra ecos del bot vía `sentMessageCache` en vez de descartar todo `fromMe` (permite operar sobre el número personal del dueño).
7. Detección de mención tri-capa: `contextInfo.mentionedJid` (phone Y LID) → fallback a mención tipeada `@Nombre` con boundaries Unicode (el `\b` ASCII falla con `@José`) SOLO si no hay pills → todo apagado en modo "número compartido" (`ASSISTANT_HAS_OWN_NUMBER`), donde NADA es mención porque los DMs son para el humano.

**Veredicto upgrade**: sí para E5/E4, principalmente por LID — pero v7 es un RC sin mantención, así que hacerlo como ellos: **pinear exacto, copiar sus 4 mitigaciones (versión WA, getMessage, metadata-sin-tocar, guard de pairing)** y mantener nuestra auto-sanación como red de seguridad. Los puntos 2, 4 y 5 son retro-portables a 6.7.23 hoy mismo sin upgrade.

## (g) Veredicto: las 5 piezas exactas a copiar

1. **`src/channels/adapter.ts`** (contrato completo: ChannelAdapter + ChannelSetup + InboundMessage con `isMention` resuelto por el adaptador + `ChannelDefaults` por contexto DM/grupo + factory-que-devuelve-null sin credenciales) → **E4 abstracción de canal**. Es el espejo exacto de lo que E4 necesita; adoptarlo casi literal (renombrando a nuestro dominio) y E5 (Meta Cloud) se vuelve "otra factory".
2. **`src/db/schema.ts` (INBOUND_SCHEMA/OUTBOUND_SCHEMA) + los 3 invariantes del header de `src/session-manager.ts` + la tabla `delivered` y el patrón de doble-poll con `inflightDeliveries` de `src/delivery.ts`** → **E4 un-solo-escritor**. Reemplaza (o disciplina) nuestros JSONL: el host nunca escribe el archivo del otro proceso; lo entregado se anota en un ledger propio (nuestro `envios.jsonl` ya es un proto-`delivered` — formalizarlo con status+platform_message_id+seq par/impar).
3. **`src/router.ts`** (engage_mode/sender_scope/ignored_message_policy='accumulate' con trigger=0, hooks `setSenderResolver`/`setAccessGate`/`registerMessageInterceptor`, y sobre todo `channelRequestGate`: tarjeta al dueño + replay del evento tras aprobar + `dropped_messages` como auditoría) → **E3 caminos** (condición→acción con pausa-y-pregunta) y **E6** (wiring chat↔agente por cliente como datos en DB, no código).
4. **`container/agent-runner/src/poll-loop.ts` + `providers/claude.ts`** (persistir continuation en el evento `init`, regex de sesión inválida → retry fresco, rotación de transcript 12MB/14d con archivo-resumen, protocolo `<message to="destino">` + nudge de re-envío, clasificación de rate-limit) → **E1 llm.js**, adaptado a `claude -p --resume`.
5. **`src/channels/whatsapp.ts` de la rama `channels`** (copiado en el clon a `channels-branch/whatsapp.ts`): `translateJid` LID→phone, `resolveWaWebVersion` con fallback wppconnect, `getMessage`+`sentMessageCache`, `cachedGroupMetadata` sin traducir, política de reconexión loggedOut-borra/shutdown-preserva, `outgoingQueue` → **E5 y endurecimiento inmediato del bot actual** (los fixes de versión-WA y reconexión sirven ya en 6.7.23).

Bonus estructurales (no código, arquitectura): (i) `container_configs` en la DB central materializado a `container.json` en cada spawn (`src/types.ts:14`, `src/container-runner.ts:132`) = **E2 ajustes schema-driven** administrables desde panel; (ii) canales/features como skills idempotentes con `REMOVE.md` (`.claude/skills/add-*`) = **E6 módulos por cliente**; (iii) composición de CLAUDE.md por fragmentos de skills (`src/claude-md-compose.ts`) = nuestra "IA madre → especialistas": el conocimiento del canal viaja como fragmento de texto, no como if en el código.
