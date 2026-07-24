# Informe ronda 4 — Planos para llm.js (E1 dixdybot)

Repos leídos de verdad (clones en `scratchpad/clones/`):

| Repo | Licencia | Qué es |
|---|---|---|
| `cesarvcanal/whatsapp-agent-bridge` (MIT, © 2026 César Canal) | MIT | Bridge mínimo WhatsApp→Claude Agent SDK: 3 archivos, cola por conversación + sesión por chat |
| `raroque/boop-agent` (MIT, © 2026 Chris Raroque, 1.2k ⭐) | MIT | Agente personal iMessage con runtime conmutable Claude SDK ↔ Codex, dispatcher→ejecutores, medición de costo |

Complemento: doc oficial del Claude Agent SDK TypeScript (`code.claude.com/docs/en/agent-sdk/typescript`). Versiones en uso: bridge `@anthropic-ai/claude-agent-sdk ^0.3.0`, boop `^0.1.0`.

---

## 1. whatsapp-agent-bridge — sesión por chat + cola por conversación

### (a) UNA sesión del Agent SDK por conversación

`src/agent.ts` (40 líneas, completo):

- **Almacenamiento del session_id:** `const sessoes = new Map<string, string>()` — mapa chatId→session_id **en RAM**. El SDK persiste el transcript en disco por defecto (`persistSession: true`), así que el id sigue siendo resumible tras un reinicio… pero el bridge lo pierde porque el Map muere con el proceso. **Lección para dixdybot: persistir el mapa jid→session_id en disco (JSONL), no en RAM.**
- **Creación:** no se crea explícitamente — la primera `query()` sin `resume` genera sesión nueva; el id llega en el primer evento del stream: `if (evento.type === "system" && evento.subtype === "init") sessoes.set(chatId, evento.session_id)` (agent.ts:31-33).
- **Resume:** `...(sessaoAnterior ? { resume: sessaoAnterior } : {})` en `options` (agent.ts:21). Eso es TODO el mecanismo de memoria: el SDK re-hidrata el historial completo desde su transcript en disco.
- **Expiración:** no hay — el bridge no expira sesiones (contexto crece hasta que el SDK compacte). dixdybot necesita política propia (p.ej. sesión nueva tras N días sin actividad, alineada con la ventana de 45d de `yaCotizado`).
- **Respuesta:** del evento `result`: `resposta = evento.subtype === "success" ? evento.result : ""` con fallback textual si viene vacío.
- Permisos mínimos por canal: `allowedTools: ["WebSearch","WebFetch"]`, `maxTurns: 8` — herramientas peligrosas "nem registradas".

### (b) Cola por conversación (serializa por chat, paraleliza entre chats)

`src/server.ts:30-37` — patrón **promise-chain por clave**:

```ts
const filas = new Map<string, Promise<void>>();
function enfileirar(chatId, tarefa) {
  const anterior = filas.get(chatId) ?? Promise.resolve();
  const proxima = anterior.then(tarefa).catch(err => console.error(...));
  filas.set(chatId, proxima);
}
```

- Mismo chat = orden FIFO estricto (cada tarea se encadena al `.then()` de la anterior); chats distintos = promesas independientes → paralelismo natural sin workers.
- El `.catch()` en la cadena evita que un error rompa la cola de ese chat.
- Detalle a mejorar en dixdybot: el Map nunca se limpia (leak leve) — borrar la entrada cuando la promesa asentada siga siendo la cola.
- Alrededor de la cola: **responder el webhook YA** (`res.sendStatus(200)` antes de procesar, server.ts:50 — proveedores tienen timeout corto), **dedupe** por `messageId` con Set acotado a 2000 con evicción por orden de inserción (server.ts:17-26), **allowlist** de números (silencio para el resto), ignorar `fromMe`. dixdybot ya tiene su libro anti-duplicados (`envios.jsonl`); el Set acotado sirve para el dedupe barato de webhooks en E5 (Meta reentrega).

---

## 2. boop-agent — el conmutador de runtime (nuestro llm.js) y la IA madre

### (c) Abstracción del cerebro: contrato `RuntimeRunRequest` → `RuntimeRunResult`

`server/runtimes/types.ts` define el contrato completo, agnóstico del backend:

```ts
RuntimeRunRequest = {
  prompt: string | (bloques texto/imagen base64),
  systemPrompt, model, reasoningEffort?,
  tools: RuntimeTool[],          // {namespace, name, description, inputSchema(zod), jsonSchema, handle()}
  allowedTools?, disallowedTools?, cwd?, abortController?,
  mode: "dispatcher" | "execution" | "background",
  onText?, onToolUse?, onToolResult?, onUsage?   // callbacks de streaming
}
RuntimeRunResult = { text, usage: UsageTotals }
```

`server/runtimes/index.ts` (21 líneas) es el conmutador entero: `switch (config.runtime) { case "claude": return runClaudeAgent(req); case "codex": return runCodexAppServerAgent(req); }`. Cada backend traduce el MISMO contrato:

- **`runtimes/claude.ts`:** agrupa `tools` por `namespace` y crea un **servidor MCP en-proceso por namespace** con `createSdkMcpServer({name, tools: tools.map(t => tool(name, desc, zodShape, handler))})` — así las herramientas propias entran al SDK sin proceso externo. Luego `query({prompt, options: {systemPrompt, model, mcpServers, allowedTools, disallowedTools, permissionMode: "bypassPermissions", abortController}})` y traduce el stream a los callbacks (`assistant`→onText/onToolUse, `user.tool_result`→onToolResult, `result`→onUsage).
- **`runtimes/codex-app-server.ts`:** mismo contrato sobre un proceso JSON-RPC por stdin/stdout; responde `item/tool/call` ejecutando el `handle()` del RuntimeTool y **declina** todo pedido de aprobación (`requestApproval → {decision:"decline"}`) — un backend nunca escala permisos por su cuenta.
- **NO usa `resume`:** boop es stateless por turno — reconstruye contexto con los últimos 10 mensajes desde Convex y los mete en el prompt (`interaction-agent.ts:341-366`, bloque `Prior turns:`). Es la estrategia opuesta al bridge; dixdybot hoy hace lo mismo (HISTORY_LIMIT=60). Con el SDK conviene sesión nativa + resume, con el historial propio como respaldo para el modo cli/api.

### Config del conmutador administrable (mapea a E2 conocimiento-como-datos)

`server/runtime-config.ts`: la elección runtime/modelo vive en un **settings store** (Convex) con cache TTL de 30s y fallback a env vars; `RUNTIME_ALIASES` ("anthropic"|"claude agent sdk"→"claude", "chatgpt"→"codex") y `MODEL_ALIASES` ("opus"→id completo) permiten cambiarlo **conversando** — `resolveDirectRuntimeSwitch()` (interaction-agent.ts:263-274) detecta "switch to codex" por regex y llama `setRuntimeProvider()`. Además el agente tiene tools `set_runtime`/`set_model`/`get_config` (self-tools) — el bot se auto-administra desde el chat, patrón directo para el panel de dixdybot.

**Snapshot por turno** (interaction-agent.ts:372-374): `const runtimeConfig = await getRuntimeConfig()` UNA vez al inicio del turno y se pasa a todo (dispatcher y sub-agentes) — un `set_model` a mitad de turno no parte el turno en dos cerebros distintos.

### (d) Errores, límites y costo

- **Errores del cerebro:** try/catch alrededor de `runAgentRuntime` con respuesta fija al usuario ("Sorry — I hit an error…") — sin reintentos ni failover (el runtime lo elige el usuario, no un failover automático). El hueco que dixdybot sí debe llenar.
- **Anti-respuesta-fantasma** (interaction-agent.ts:590-602): regex que detecta placeholders `"(no output)"/"no reply"` y los reemplaza por fallback honesto — el modelo a veces "pierde el hilo" tras ciclos de tools.
- **Medición de costo — el gotcha clave** (`server/usage.ts:76-141`): el `result` del SDK trae DOS campos: `msg.usage` (solo el turno FINAL, **subcuenta masivamente en corridas con tools**) y `msg.modelUsage` (agregado por modelo de TODA la query, camelCase). **Siempre preferir `modelUsage`**; puede traer VARIOS modelos por query (el CLI usa haiku para ruteo interno + el principal), por eso reportan el modelo pedido si aparece (con prefix-match porque el SDK expande alias a id con fecha) y si no, el de mayor volumen. `costUsd` sale de `msg.total_cost_usd` (estimación client-side). Para Codex calculan costo propio con tabla de precios.
- **Registro por turno** (interaction-agent.ts:604-622): `{source: "dispatcher", conversationId, turnId, runtime, billingMode, model, tokens in/out, cache r/w, costUsd, durationMs}` → tabla usageRecords. Ese es el esquema del ledger de costos de dixdybot (a JSONL).
- **`AbortController` por agente:** `running.set(agentId, abort)` (execution-agent.ts:128-129) — cancelación individual de sub-agentes.

### IA madre → especialistas (bonus: es el patrón pedido para dixdybot)

`interaction-agent.ts` + `execution-agent.ts`: el **dispatcher** ("You are a DISPATCHER, not a doer") tiene prohibido responder hechos del mundo (system prompt lo fuerza) y solo tiene tools de memoria/automatizaciones/borradores/`spawn_agent`; los built-ins peligrosos van en `disallowedTools: ["WebSearch","Bash","Read","Write",...]` — comentario literal: *"even with bypassPermissions the SDK can leak its built-ins if we only whitelist"* → **cinturón y tirantes: whitelist `mcp__ns__tool` + blacklist de built-ins, siempre**. El **ejecutor** recibe una tarea "crisp" (no el mensaje crudo), sus integraciones, y regla de seguridad: toda acción externa se guarda como **draft**; solo el `send_draft` del dispatcher (aprobado en conversación) comete — exactamente la "pausa-y-pregunta al dueño" de E3. Tool `send_ack` obligatoria antes de spawns lentos (UX de mensajería: el usuario ve algo en <2s).

---

## 3. Doc oficial Agent SDK TypeScript — lo que existe de verdad

`query({prompt, options}): AsyncGenerator<SDKMessage>` con `prompt: string | AsyncIterable<SDKUserMessage>` (modo streaming input habilita `interrupt()`, `setModel()`, `setPermissionMode()`, `setMcpServers()` en caliente).

Opciones relevantes para dixdybot:

| Opción | Uso en dixdybot |
|---|---|
| `resume: "<uuid>"` | retomar sesión del chat; `forkSession: true` = ramificar sin contaminar (ideal para el replay 🎬 del gimnasio) |
| `sessionId` / `persistSession` (default true) | fijar uuid propio / desactivar persistencia |
| `continue: true`, `resumeSessionAt: "<msg-uuid>"` | retomar la última / retomar en un punto (rollback de entrenamiento) |
| `listSessions()` / `getSessionMessages()` | inventario de sesiones desde el panel |
| `allowedTools` / `disallowedTools` | permisos por canal/rol |
| `permissionMode: 'default'\|'plan'\|'dontAsk'\|'bypassPermissions'` | + `canUseTool(request, {signal}) → 'approve'\|'deny'\|'ask'` — el gancho natural de los caminos E3 (pausa-y-pregunta) |
| `hooks: {SessionStart, ToolUse, ToolResult, UserMessage, ...}` | auditoría/telemetría sin tocar el loop |
| `maxTurns`, `maxBudgetUsd` | tope de vueltas y **tope de gasto en USD por query** (corta solo) |
| `abortController` / `q.close()` | cancelación |
| `mcpServers` + `createSdkMcpServer` | tools propias en-proceso |
| `settingSources: ['user'\|'project'\|'local']` | qué settings de Claude Code carga (boop usa `["project"]` solo en modo execution) |
| `systemPrompt: string \| {type:'preset', preset:'claude_code', append}` | persona del bot |

Mensajes: `system/init` trae `session_id`; `result` trae `total_cost_usd` (estimación client-side), `usage` {input/output/cache tokens}, `duration_ms` — y el no documentado-pero-real `modelUsage` agregado (ver gotcha de boop). `startup()` pre-calienta el subproceso (latencia del primer turno).

---

## 4. Diseño concreto: `llm.js` para dixdybot (E1)

Puerta única al cerebro. Contrato estilo boop (request/result + callbacks), cola estilo bridge, sesión por conversación persistida, failover por eventos tipados, costo medido siempre.

```js
// llm.js — ÚNICO módulo que habla con un modelo. Nadie más importa SDK/spawn/fetch de IA.

// ── Config (E2: conocimiento-como-datos; editable desde panel, cache TTL 30s como boop)
// data/llm-config.json = {
//   modo: "cli" | "sdk" | "api",          // conmutador principal
//   modelo: "claude-sonnet-4-6",
//   fallbacks: ["cli", "plantilla"],       // cadena de degradación en orden
//   maxTurns: 8, maxBudgetUsd: 0.50,       // topes por turno
//   sesion: { ttlDias: 45 }                // expiración de sesión por chat
// }

// ── Contrato (el RuntimeRunRequest de boop, criollo)
// consultar({
//   conversacionId,            // jid — clave de sesión Y de cola
//   prompt,                    // string o bloques [{type:'text'|'image',...}]
//   sistema,                   // persona + tarifario por estado (ya en código)
//   herramientas,              // [{namespace, name, description, schema, handle}]
//   permitidas, prohibidas,    // whitelist mcp__ns__tool + blacklist built-ins (SIEMPRE ambas)
//   modo: 'vendedor'|'especialista'|'fondo',
//   preguntarDueno,            // (tool, input) => 'approve'|'deny'|'ask'  ← caminos E3
//   onTexto, onTool, onUso     // callbacks
// }) → { texto, uso: {modelo, inTok, outTok, cacheR, cacheW, costoUsd, duracionMs},
//        eventos: [ {tipo:'fallback', de:'sdk', a:'cli', causa:'timeout'} ... ] }

const sesiones = cargarJSONL('data/sesiones.jsonl');   // jid → {sessionId, ultimoUso}
                                                        // persistido: el bridge lo pierde en RAM; nosotros no
const colas = new Map();                                // cola promise-chain por jid (bridge server.ts:30)
function encolar(jid, tarea) {
  const ant = colas.get(jid) ?? Promise.resolve();
  const prox = ant.then(tarea).catch(e => log(jid, e));
  colas.set(jid, prox);
  prox.finally(() => { if (colas.get(jid) === prox) colas.delete(jid); }); // sin leak
  return prox;
}

async function consultar(req) {
  return encolar(req.conversacionId, async () => {
    const cfg = await configLLM();                      // snapshot POR TURNO (boop): un cambio
    const cadena = [cfg.modo, ...cfg.fallbacks];        // de modo a mitad de turno no parte el turno
    const eventos = [];
    for (const modo of cadena) {
      const t0 = Date.now();
      try {
        const r = await MOTORES[modo](req, cfg);        // switch de 3 casos, como runtimes/index.ts
        r.uso.duracionMs = Date.now() - t0;
        registrarUso({ ...r.uso, jid: req.conversacionId, modo, eventos }); // → data/uso-llm.jsonl
        return { ...r, eventos };
      } catch (err) {
        const causa = clasificar(err);                  // 'rate_limit'|'timeout'|'proceso'|'refusal'|'auth'
        eventos.push({ tipo: 'fallback', de: modo, causa });
        if (causa === 'auth') throw err;                // no degradar lo indegradable
        if (causa === 'rate_limit') await espera(err.retryAfter ?? 30_000);
      }
    }
    return { texto: PLANTILLA_DISCULPA, uso: USO_VACIO, eventos }; // último peldaño: respuesta fija
  });
}

const MOTORES = {
  // sdk — @anthropic-ai/claude-agent-sdk (destino E1)
  async sdk(req, cfg) {
    const ses = sesionVigente(req.conversacionId, cfg.sesion.ttlDias); // expira por TTL
    const mcp = porNamespace(req.herramientas).map(([ns, ts]) =>
      [ns, createSdkMcpServer({ name: ns, tools: ts.map(t => tool(t.name, t.description, t.schema, t.handle)) })]);
    let texto = '', uso = USO_VACIO, sid = ses?.sessionId;
    for await (const msg of query({ prompt: aPrompt(req.prompt), options: {
      systemPrompt: req.sistema, model: cfg.modelo,
      ...(sid ? { resume: sid } : {}),
      mcpServers: Object.fromEntries(mcp),
      allowedTools: req.permitidas, disallowedTools: req.prohibidas, // cinturón Y tirantes (boop)
      canUseTool: async ({tool_name, input}) => req.preguntarDueno?.(tool_name, input) ?? 'approve',
      maxTurns: cfg.maxTurns, maxBudgetUsd: cfg.maxBudgetUsd,
      abortController: req.abort,
    }})) {
      if (msg.type === 'system' && msg.subtype === 'init') sid = msg.session_id;
      if (msg.type === 'assistant') texto = extraerTexto(msg, req.onTexto, req.onTool);
      if (msg.type === 'result') uso = agregarUso(msg, cfg.modelo);   // modelUsage > usage (gotcha boop)
    }
    guardarSesion(req.conversacionId, sid);            // → sesiones.jsonl (a disco, no RAM)
    if (esPlaceholder(texto)) throw new ErrorLLM('placeholder');      // "(no output)" → siguiente motor
    return { texto, uso };
  },
  // cli — claude -p actual (lo que YA corre; queda como peldaño de failover y modo por defecto al migrar)
  async cli(req, cfg) { /* spawn claude -p con historial propio (HISTORY_LIMIT) como hoy */ },
  // api — Messages API directa (sin tools de fs, barato y sin subproceso; para clasificar/extraer)
  async api(req, cfg) { /* fetch /v1/messages con historial propio; uso desde response.usage */ },
};
```

Decisiones y su fuente:

1. **Cola por conversación dentro de llm.js** (bridge `server.ts:30-37`) — serializa turnos del mismo chat, paraleliza chats; con limpieza del Map. Aplica a E1 ya y prepara E4 (un-solo-escritor: la cola ES el escritor único por chat).
2. **Sesión por chat con `resume`, id persistido en JSONL con TTL** (bridge `agent.ts` + doc oficial `resume`/`persistSession`) — memoria nativa del SDK en modo sdk; en cli/api se sigue reconstruyendo historial (boop `interaction-agent.ts:341`) para que el contrato no cambie entre modos. `forkSession: true` para el gimnasio/replay sin contaminar la sesión real.
3. **Conmutador = switch de 3 casos sobre un contrato único** (boop `runtimes/index.ts` + `types.ts`) — el resto del bot llama `consultar()` y no sabe qué motor respondió. Config en datos con alias y snapshot por turno (boop `runtime-config.ts`, `interaction-agent.ts:372`).
4. **Failover por eventos tipados** — lo que ni bridge ni boop tienen: cadena `sdk→cli→api→plantilla` recorrida por clasificación de error (`rate_limit` espera y reintenta el mismo peldaño una vez; `auth` no degrada; placeholder de boop cuenta como fallo). Cada salto queda como evento en el resultado Y en el ledger → el panel muestra "hoy 3 turnos degradaron a cli".
5. **Costo SIEMPRE medido** (boop `usage.ts` + doc `total_cost_usd`/`maxBudgetUsd`) — agregación por `modelUsage` (no `usage`, subcuenta con tools), registro por turno a `data/uso-llm.jsonl` con el esquema de boop (fuente, jid, turnId, modo, modelo, tokens, cache, costo, duración), y `maxBudgetUsd` como tope duro por turno.
6. **Permisos: whitelist + blacklist juntas** (boop `interaction-agent.ts:556-569`) — el vendedor jamás ve `Bash/Read/Write/WebSearch`; los especialistas (E3+) reciben su whitelist por dominio. `canUseTool → 'ask'` conecta con pausa-y-pregunta (E3): el tool queda pendiente hasta OK del dueño por WhatsApp/panel.
7. **IA madre → especialistas = dispatcher + spawn_agent con drafts** (boop `interaction-agent.ts` + `execution-agent.ts:104-106`) — para E3/E6: el vendedor despacha, el especialista redacta, solo el flujo aprobado comete; `send_ack` antes de trabajo lento (en WhatsApp: mensaje corto + typing).

Riesgos anotados: el SDK factura como Claude Code (API key) — el modo `cli` con suscripción sigue siendo el barato mientras tanto; `modelUsage` no está en la doc pública (boop lo lee con cast) — tratarlo como opcional con fallback a `usage`; versiones del SDK se mueven rápido (0.1→0.3 entre estos dos repos) — fijar versión en package.json.
