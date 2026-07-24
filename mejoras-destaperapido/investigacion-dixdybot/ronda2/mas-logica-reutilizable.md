# Más lógica reutilizable — segundo barrido (dixdybot)

Fecha: 2026-07-23. Método: la cuota de búsqueda web de la sesión estaba agotada por el flujo
(200/200), así que este barrido se hizo con (1) **WebFetch de documentación oficial** (docs de
Anthropic en code.claude.com, mastra.ai, voltagent.dev, docs.langchain.com, ai-sdk.dev) y
(2) **API de GitHub vía `gh`** (estrellas, licencia SPDX, último push y LICENSE leídos el mismo
día — datos reales, no de artículos). Complementa al censo previo (Parlant, vocero-crm,
BuilderBot, claude-whatsapp, Chatwoot, HumanLayer, DeepEval, wacrm, OpenClaw): aquí va SOLO lo
no cubierto.

---

## (a) Frameworks de agentes TypeScript/JS para el runtime del bot

### Mastra (mastra-ai/mastra) — el que más aporta en memoria y pausa/reanuda
- URL: https://github.com/mastra-ai/mastra — 26.462 ⭐ | push 2026-07-23
- Licencia (LICENSE.md leído 2026-07-23): **Apache-2.0 el core**, carpetas `ee/` bajo licencia
  enterprise aparte (open-core estilo Onyx). Lo copiable es casi todo.
- **Memoria** (docs jul 2026): capas complementarias que son EXACTAMENTE los dolores del bot:
  - *Message History* con modelo **resource/thread** (resource = cliente, thread = conversación;
    el thread tiene dueño inmutable) — el modelo de datos para "un hilo por número de WhatsApp".
  - *Observational Memory*: agentes de fondo mantienen un "observation log" denso que
    **reemplaza el historial crudo cuando crece** — la respuesta de diseño al problema
    HISTORY_LIMIT (hoy 60 mensajes y pierde el trato en chats largos).
  - *Working Memory* (datos estructurados del cliente: nombre, dirección, preferencias) y
    *Semantic Recall* (recuperar mensajes viejos por significado).
  - *Memory processors* para filtrar/priorizar al armar el contexto. Storage: LibSQL, etc.
- **Workflows suspend/resume** (docs jul 2026): un paso llama `suspend({...})`, el estado se
  guarda como **snapshot en el storage y sobrevive reinicios y deploys**; se retoma con
  `run.resume({step, resumeData})` validado por `resumeSchema`, desde HTTP/eventos/timers;
  `createWorkflowStateReader()` para inspeccionar suspendidos. Es la mecánica formal de la
  "pausa-de-tema + pregunta al humano + retomar" de E3.
- Contra: asume LLM por API (`ANTHROPIC_API_KEY`, model router `anthropic/claude-*`), no
  `claude -p`. Adoptarlo entero sería otro framework al lado del cerebro; robarle el **modelo de
  datos de memoria** y el **snapshot suspend/resume** no exige adoptarlo.

### VoltAgent (VoltAgent/voltagent) — el MIT completo si se quiere copiar código literal
- URL: https://github.com/VoltAgent/voltagent — 10.119 ⭐ | **MIT** | push 2026-07-13
- TS puro: `Agent` + `Memory` con adaptadores durables (`LibSQLMemoryAdapter` → archivo .db
  local, perfecto para Mac mini), **supervisor + sub-agents**, workflow engine declarativo y
  **suspend/resume con `suspendSchema`/`resumeSchema` en Zod** (docs jul 2026): `suspend(reason,
  data)` guarda estado automáticamente, `execution.resume(data)` valida contra el schema.
  Anthropic soportado por config. Open-core suave: framework MIT, consola "VoltOps" comercial.
- Qué robar: al ser MIT, el **código del ciclo suspend/resume y de los memory adapters** se
  puede copiar literal al núcleo dixdybot sin adoptar el framework.

### LangGraph.js (langchain-ai/langgraphjs)
- URL: https://github.com/langchain-ai/langgraphjs — 3.132 ⭐ | MIT | push 2026-07-21
- En JS existen los checkpointers **MemorySaver / SqliteSaver (dev) / PostgresSaver (prod)**;
  cada conversación es un `thread_id` en la config; `interrupt()`/`Command` para
  human-in-the-loop; `Store` para memoria entre threads (docs.langchain.com, jul 2026).
- Qué robar: solo el concepto **checkpoint por thread_id** (pausar un flujo por chat y
  retomarlo tras el reinicio). El paradigma de grafo explícito pelea con el cerebro Claude
  libre que ya funciona; no adoptar el grafo.

### Vercel AI SDK (vercel/ai)
- URL: https://github.com/vercel/ai — 25.739 ⭐ | **Apache-2.0** (LICENSE leído) | push 2026-07-23
- Versión actual: **v7** (jul 2026). `ToolLoopAgent` (loop de tools con `stopWhen`,
  `prepareStep`, `runtimeContext` para settings por tenant) y — novedad relevante —
  **`HarnessAgent`** con patrones pre-hechos de harness (Claude Code, Codex, Pi).
  **No trae memoria/persistencia ni checkpoints propios** — deliberadamente.
- Qué robar: es la mejor **capa API delgada para la vía barata del failover E1** (90% del
  tráfico conversacional por Messages API con Haiku/Sonnet + caching, como recomendó el informe
  del cerebro): proveedor Anthropic + tool loop tipado en el mismo runtime Node, sin cargar un
  framework. La memoria queda donde debe: en dixdybot.

### Agno — NO existe en JS
- agno-agi/agno: 41.367 ⭐, Apache-2.0, pero **Python-only** (revisada la organización completa
  el 2026-07-23: el único repo TS es `agent-ui`, una interfaz). No aplica al runtime Node del
  bot. Dicho honestamente: no hay "Agno-JS".

---

## (b) Claude Agent SDK a fondo — ¿mejor cerebro que `claude -p` pelado?

Fuente: docs oficiales code.claude.com/docs/en/agent-sdk (+ /sessions), leídas 2026-07-23.

### Qué es y qué da sobre `claude -p`
- Paquetes: `claude-agent-sdk` (Python, 7.694 ⭐, MIT) y `@anthropic-ai/claude-agent-sdk`
  (TS, 1.650 ⭐ — **ojo: el repo TS no declara licencia OSS**; la doc dice que el uso se rige
  por los Commercial Terms de Anthropic). Ambos **empaquetan el binario nativo de Claude Code**
  (no requiere instalar el CLI aparte).
- API: `query(prompt, options)` async-iterable; en Python además `ClaudeSDKClient` que mantiene
  la sesión entre `query()` sin manejar IDs.
- **Sesiones** (la pieza que más le falta al bot actual): historial JSONL automático en
  `~/.claude/projects/<cwd-codificado>/<session-id>.jsonl`; `continue` (última sesión del
  directorio), `resume: session_id` (**una sesión persistente POR CHAT de WhatsApp — hoy el bot
  re-arma el historial a mano en cada invocación**), `forkSession` (ramificar para probar sin
  romper el hilo real — ideal para el gimnasio/replay), `persistSession:false` (TS),
  `listSessions()/getSessionMessages()/renameSession()/tagSession()`, y **`SessionStore`
  adapter** para mover transcripts a storage compartido (multi-host/serverless). Nota: la
  "V2 session API" (`createSession()`) fue **removida** en TS 0.3.142 — no basar diseño en ella.
- **Hooks en proceso** (callbacks, no scripts): `PreToolUse`, `PostToolUse`, `Stop`,
  `SessionStart`, `SessionEnd`, `UserPromptSubmit` — el guardián v2 y el logging del bot como
  funciones TS con acceso al estado del proceso.
- **Permisos**: `allowedTools`/`disallowedTools`/`permissionMode` + `canUseTool` programático —
  gate por herramienta y por mensaje (base técnica del "pausa y pregunta").
- **Subagents** (`agents: {AgentDefinition}` + tool `Agent`, mensajes con
  `parent_tool_use_id`) y **MCP in-process**; `settingSources` para cargar `.claude/` (skills,
  CLAUDE.md) — hereda el ecosistema de skills DIXDY.
- Costo por invocación en `ResultMessage.total_cost_usd`; mismos backends de auth que el CLI
  (API key, Bedrock `CLAUDE_CODE_USE_BEDROCK=1`, Vertex, Foundry) → **el plan de failover por
  variables de entorno del informe previo aplica sin cambios**.
- **Legal (doc oficial, jul 2026)**: "Anthropic does not allow third party developers to offer
  claude.ai login or rate limits for their products, **including agents built on the Claude
  Agent SDK** — use API key". Confirma la zona gris del informe del cerebro: para uso propio del
  dueño es lo tolerado; para producto multi-cliente (E6), API key sí o sí.

### Veredicto (b)
Sí: el Agent SDK es un cerebro **estrictamente mejor** que `claude -p` artesanal para E1 —
sesión nativa por chat (resume), hooks/permisos en proceso, subagents, fork para entrenar,
costo por mensaje — con el MISMO failover. El costo del harness por mensaje sigue siendo el
mismo que el de `claude -p` (es el mismo harness), así que la recomendación previa se mantiene:
harness para lo agéntico, API delgada para lo conversacional masivo.

### Bots de atención/mensajería de la comunidad construidos con el Agent SDK (verificados 2026-07-23)
- **nanocoai/nanoclaw** — **30.316 ⭐ | MIT | push 2026-07-21**. El hallazgo grande del barrido
  (no cubierto ayer). Ver sección (e): es un asistente multicanal (WhatsApp vía **Baileys v7**,
  Telegram, Slack, iMessage…) cuyo cerebro es **el Claude Agent SDK dentro de un contenedor**.
- **raroque/boop-agent** — 1.221 ⭐ | MIT | push 2026-07-13. Agente personal por iMessage con
  runtime conmutable (Claude Agent SDK o Codex) — referencia de "cerebro conmutable".
- **cesarvcanal/whatsapp-agent-bridge** — 3 ⭐ | MIT | jul 2026. Chico pero es el patrón exacto:
  Express + Agent SDK, **cola por conversación, sesión por chat, allowlist** (en portugués).
- **padhu0626/Theron** — MIT, starter WAHA + Agent SDK ("fork, escribe tu prompt, escanea QR").
- **JungwooHur/paperclaw** — MIT, jul 2026: asistente de investigación por WhatsApp sobre
  NanoClaw (Agent SDK + aislamiento por contenedores).
- Otros menores: aviv-edri/whatsapp-personal-assistant (MIT), clfigueiredo/infra-agent
  (Agent SDK + Evolution API), MaxGomb/maxai-wa-agent (Green API), FujiwaraChoki/kairo.
- Ecosistema útil: **thedotmack/claude-mem** (88.288 ⭐, Apache-2.0 — memoria persistente entre
  sesiones vía hooks; referencia para la memoria del cerebro) y
  **codeany-ai/open-agent-sdk-typescript** (2.730 ⭐, MIT — reimplementación del Agent SDK sin
  dependencia del CLI; plan C si Anthropic cambiara el empaquetado).
- Honesto: NO encontré un bot de VENTAS/atención comercial grande y mantenido hecho con el
  Agent SDK; lo que existe son asistentes personales y starters. El nicho sigue abierto.

---

## (c) Claude Code Channels a fondo — ¿puede dixdybot SER un canal?

Fuente: docs oficiales https://code.claude.com/docs/en/channels y /channels-reference
(leídas 2026-07-23; la feature está en **research preview**).

### Qué es exactamente
Un canal es un **MCP server local por stdio** (Claude Code lo lanza como subproceso) que:
1. Declara la capability experimental **`claude/channel`** (con eso Claude Code registra el
   listener).
2. Emite **`notifications/claude/channel`** con `{content, meta}` → el evento entra al contexto
   como `<channel source="X" attr=...>texto</channel>` (cada key de `meta` = atributo).
3. Si es bidireccional, expone un **tool MCP `reply`** normal (chat_id + text) y usa
   `instructions` del server para decirle a Claude cómo rutear respuestas.
El runtime solo exige `@modelcontextprotocol/sdk` (sirve Node, Bun o Deno; **Bun solo lo usan
los plugins oficiales**). Canales oficiales: Telegram, Discord, iMessage + demo fakechat.
No hay canal WhatsApp oficial (el comunitario crisandrews/claude-whatsapp ya estaba censado).

### Cómo se extiende con un canal custom
Ejemplo oficial completo (~80 líneas): server MCP + HTTP local + `.mcp.json` + arrancar con
`claude --dangerously-load-development-channels server:X`. **Durante el preview, los canales
custom NO entran al allowlist** (que es curado por Anthropic; ni siquiera el marketplace
comunitario está permitido) → siempre requieren el flag de desarrollo. Seguridad: allowlist de
REMITENTES (gate por `message.from.id`, no por chat) porque un canal sin gate es un vector de
prompt injection.

### La joya: permission relay (spec oficial robable)
Capability `claude/channel/permission` → cuando Claude quiere usar una tool que requiere
aprobación, Claude Code emite `notifications/claude/channel/permission_request` con
`{request_id (5 letras a-z sin 'l', pensado para teclear desde el teléfono), tool_name,
description, input_preview}`; el humano contesta por el chat **"yes abcde" / "no abcde"** y el
server devuelve `notifications/claude/channel/permission {request_id, behavior: allow|deny}`.
El diálogo local sigue abierto y gana la primera respuesta. **Esto ES el diseño del "pausa el
chat y pregunta a Alejandro por WhatsApp" de E3, ya especificado por Anthropic** —
sanitización de campos incluida (v2.1.211+ neutraliza caracteres de dirección/invisibles).

### Veredicto (c): ¿dixdybot COMO canal de Claude Code?
Técnicamente sí y es barato (~100 líneas), y heredaría skills/MCP de la sesión. Pero como
runtime de producción hoy NO conviene por tres límites verificados en la doc:
1. **Preview + allowlist**: un canal custom vive detrás de `--dangerously-load-development-channels`
   y el contrato puede cambiar.
2. **Una sesión = una cola**: los eventos se encolan y "si llegan varios mientras Claude está
   ocupado, se entregan juntos y los maneja como grupo… para streams independientes
   concurrentes, corre sesiones separadas" (doc textual). Un bot de ventas con N clientes
   simultáneos mezclaría conversaciones en un solo contexto — exactamente lo que la sesión-por-chat
   debe evitar. (NanoClaw resuelve esto por fuera: host router + una sesión Agent SDK por grupo.)
3. Depende de una sesión interactiva abierta (login de suscripción, límites compartidos).
**Lo que sí se roba**: (i) el contrato notificación+reply-tool como interfaz interna de
canales de dixdybot (E4) — es más simple que inventar otro; (ii) el **permission relay completo**
para E3; (iii) opcional: un mini-canal "dixdybot-dev" para hablar con el bot desde la terminal
de Alejandro en desarrollo.

---

## (d) Motores de "knowledge base conversacional" — ¿aportan al almacén de caminos?

Verificados por API + LICENSE el 2026-07-23:

| Proyecto | ⭐ | Licencia real | Veredicto para dixdybot |
|---|---|---|---|
| langgenius/dify | 149.868 | **Apache-2.0 MODIFICADA**: prohíbe operar **multi-tenant** sin licencia comercial y quitar el logo del frontend | **Descartado**: E6 (dixdybot multi-cliente) ES multi-tenant → chocaría con la licencia. Además es una plataforma pesada (Docker, Python+Node) para lo que los caminos necesitan |
| infiniflow/ragflow | 85.720 | Apache-2.0 limpia | Sobra hoy. Única pieza tentadora: su parsing profundo de documentos (PDF/tablas) si algún día el conocimiento llegara en documentos del cliente. Infra pesada (Elasticsearch/Infinity) |
| onyx-dot-app/onyx | 31.099 | MIT + carpetas `ee/` enterprise | Sobra: es chat empresarial sobre conectores (Drive, Slack…); no modela reglas condición→acción |

**Veredicto (d)**: ninguno aporta al almacén de caminos. Los caminos de E3 son reglas
condición→acción versionadas en git con matching por turno — eso es Parlant (censo previo) +
archivos planos, no un pipeline RAG de documentos. Estos motores resuelven otro problema
(preguntas sobre corpus documental) y traen infra y licencias en contra.

---

## (e) Repos WhatsApp+Baileys con arquitectura limpia para robar estructura

Primero lo honesto: el **top de estrellas "Baileys bot" de GitHub son bots "MD" de features**
(lyfe00011/whatsapp-bot 1.182⭐ sin licencia, SUBZERO-MD, RTXZY-MD, XLICON…) — monolitos
plugin-based sin separación canal/cerebro. Se revisaron y **se descartan** como fuente de
arquitectura (búsqueda GitHub 2026-07-23).

Lo que sí vale:

### nanocoai/nanoclaw — LA arquitectura de referencia del barrido
- 30.316 ⭐ | MIT | push 2026-07-21 | codebase deliberadamente chico ("un proceso y un puñado
  de archivos", en reacción explícita a las ~500k líneas de OpenClaw).
- Arquitectura (README, jul 2026):
  `apps de mensajería → host Node (router) → inbound.db → contenedor (Bun + Claude Agent SDK)
  → outbound.db → host (delivery) → apps`.
  - **Dos SQLite por sesión, cada uno con UN solo escritor** — sin IPC, sin stdin piping, sin
    contención (el mismo espíritu que `envios.jsonl` pero sistematizado).
  - Modelo de entidades **user → messaging group → agent group → session**; modelo de
    aislamiento configurable por canal (agente propio, agente compartido con conversaciones
    separadas, o sesión única multi-superficie).
  - **Adaptador WhatsApp = Baileys v7** (keystore migrable; LID mapping resuelto por mensaje).
  - Por agent-group: su propio `CLAUDE.md`, memoria, contenedor y mounts (multi-cliente E6 en
    miniatura); **templates de agentes** (instrucciones+MCP+skills sin secretos).
  - Canales y providers instalables por **skills** (`/add-whatsapp`, `/add-telegram`,
    `/add-codex`, `/add-ollama-provider`) — cerebro conmutable por grupo.
  - Credenciales vía **onecli** (onecli/onecli, 2.540 ⭐, Apache-2.0 — gateway de credenciales
    con vault para agentes).
- Qué robar: **el plano completo E1+E4** — desacople host/cerebro con colas SQLite un-escritor,
  sesión Agent SDK por chat/grupo (resuelve el límite "una sesión no multiplexa" de Channels),
  el modelo de entidades y el patrón de adaptadores de canal. MIT y legible en una tarde larga.
- Derivado: microclaw/microclaw (729 ⭐, MIT, Rust) — mismo diseño en un binario; solo referencia.

### Puentes minimalistas Baileys→agente (chicos pero con la costura correcta)
- **obirimensah05/whatsapp-bridge** — 2 ⭐ | MIT | push 2026-07-22. Baileys + Fastify + SQLite +
  **MCP**: WhatsApp expuesto como bridge self-hosted para agentes. La versión mínima del patrón.
- **AaronAbuUsama/whatsappd** — 1 ⭐ | MIT | jul 2026. "Un número de WhatsApp como canal de
  agente": daemon Baileys + tools de agente + sidecar HTTP.
- **zeative/zaileys** — 63 ⭐ | MIT | push 2026-07-19. Wrapper TS que simplifica la API de
  Baileys (y zaileys-mcp encima). Joven; mirar su superficie de API, no depender de él.
- **jeankassio/ZapToBox** — 153 ⭐ | MIT | nov 2025. REST multi-instancia con webhooks
  (mini-Evolution, MIT limpio).
- Señal de tendencia: proliferan **MCP servers de WhatsApp** (delltrak/wamcp "61 tools",
  kahflane/whatsapp-mcp "87 tools" MIT, gridmint/mcp-whatsapp) — "WhatsApp como set de tools
  MCP" es el patrón 2026, coherente con el contrato de canal del censo previo.
- Vivos pero descartables como arquitectura: KillovSky/Iris (213 ⭐ MIT, bot de features en
  portugués), neoxr/neoxr-bot (303 ⭐ MIT, plugin-based).

---

## Top-5 accionable

1. **NanoClaw (MIT, 30.3k ⭐)** — robar la arquitectura completa: host router + `inbound.db`/
   `outbound.db` (un escritor por archivo) + una sesión Claude Agent SDK por grupo/chat +
   adaptadores de canal (Baileys v7 incluido) + workspace por agente (CLAUDE.md/memoria/mounts).
   Es E0/E1/E4 — y el embrión de E6 — ya diseñado, en un codebase pensado para leerse entero.
2. **Claude Agent SDK como cerebro E1** — migrar de `claude -p` artesanal al SDK (TS o Python):
   `resume` por session_id = hilo persistente por cliente; hooks in-process (PreToolUse =
   guardián), `canUseTool`, `forkSession` para el gimnasio, `total_cost_usd` por mensaje;
   mismo failover por env vars. Cuidados: producto → API key (doc legal oficial jul 2026), el
   repo TS no trae licencia OSS (Commercial Terms), y la V2 session API ya fue removida.
3. **Permission relay de Channels como spec del "pausa y pregunta" (E3)** — copiar el diseño
   oficial: request_id de 5 letras tecleables, prompt con tool+descripción+preview, respuesta
   "yes/no <id>" por el mismo chat, primera respuesta gana, campos tratados como no confiables.
   No requiere usar Channels: es un protocolo de ~50 líneas sobre el WhatsApp de Alejandro.
4. **Mastra (Apache-2.0 core) como plano de memoria y pausa** — el modelo resource/thread +
   Observational/Working Memory + semantic recall es la solución de diseño al HISTORY_LIMIT;
   sus workflows suspend/resume con snapshot persistente son la pausa-de-tema formal.
   Alternativa para copiar código literal: **VoltAgent (MIT)** con suspendSchema/resumeSchema Zod.
5. **Vercel AI SDK v7 (Apache-2.0) como vía API delgada del failover** — `ToolLoopAgent` +
   proveedor Anthropic para el 90% conversacional barato (Haiku/Sonnet + caching), en el mismo
   runtime Node, sin memoria propia (la memoria vive en dixdybot). `HarnessAgent` como puente
   futuro si se mezclan harness.

## Lo que NO encontré (honestidad)
- No existe "Agno-JS": Agno es Python-only (verificado en la organización, jul 2026).
- No hay bots de atención COMERCIAL grandes y mantenidos sobre el Agent SDK — solo asistentes
  personales (NanoClaw, boop) y starters chicos; dixdybot seguiría siendo pionero en ese nicho.
- No hay canal WhatsApp OFICIAL en Channels, y los canales custom siguen fuera del allowlist
  del preview (jul 2026).
- Nada nuevo que implemente el ciclo completo "detecta hueco → pausa ese chat → pregunta →
  crea el camino": sigue siendo la parte original de dixdybot (el relay de Channels da el
  mecanismo de pregunta; Parlant/Mastra dan el almacén y la pausa).

## Fuentes
- https://code.claude.com/docs/en/agent-sdk — overview, capacidades, legal/branding (leída 2026-07-23)
- https://code.claude.com/docs/en/agent-sdk/sessions — continue/resume/fork, JSONL, SessionStore (2026-07-23)
- https://code.claude.com/docs/en/channels — canales, allowlist, enterprise, preview (2026-07-23)
- https://code.claude.com/docs/en/channels-reference — contrato de canal custom + permission relay (2026-07-23)
- https://mastra.ai/docs/memory/overview y https://mastra.ai/docs/workflows/suspend-and-resume (2026-07-23)
- https://voltagent.dev/docs/ y https://voltagent.dev/docs/workflows/suspend-resume/ (2026-07-23)
- https://docs.langchain.com/oss/javascript/langgraph/persistence (2026-07-23)
- https://ai-sdk.dev/docs/agents/overview — AI SDK v7, ToolLoopAgent, HarnessAgent (2026-07-23)
- GitHub API (gh, 2026-07-23): nanocoai/nanoclaw, mastra-ai/mastra, VoltAgent/voltagent,
  langchain-ai/langgraphjs, vercel/ai, agno-agi/*, langgenius/dify, infiniflow/ragflow,
  onyx-dot-app/onyx, anthropics/claude-agent-sdk-{python,typescript}, thedotmack/claude-mem,
  codeany-ai/open-agent-sdk-typescript, raroque/boop-agent, cesarvcanal/whatsapp-agent-bridge,
  padhu0626/Theron, JungwooHur/paperclaw, zeative/zaileys, obirimensah05/whatsapp-bridge,
  AaronAbuUsama/whatsappd, jeankassio/ZapToBox-Whatsapp-Api, onecli/onecli, microclaw/microclaw
