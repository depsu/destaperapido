# BIBLIOTECA DE PLANOS — dixdybot (síntesis ronda 4)

Síntesis de los 6 informes de lectura de código real (clones en `scratchpad/clones/`,
informes completos en `scratchpad/informes4/*.md`). Cada pieza cita repo + archivo real del
clon. Organizado por etapa del plan revisado
(`mejoras-destaperapido/investigacion-dixdybot/ronda2/plan-revisado.md`).

## Fuentes y licencias

| Repo | Licencia | Aporta principalmente a |
|---|---|---|
| nanocoai/**nanoclaw** | MIT (© 2026 Gavriel) | E1, E4 un-solo-escritor, E5 Baileys v7, E6 skills |
| emcie-co/**parlant** | Apache-2.0 | E3 caminos (esquema + motor) |
| kevinbelier/**vocero-crm** | MIT (© 2026 Kevin Belier) | E3-E4 gimnasio, E2 loop juez→KB |
| mastra-ai/**mastra** | Apache-2.0 (salvo `ee/`, no tocado) | E1 memoria, E3 pausa-y-pregunta |
| codigoencasa/**builderbot** | MIT (© 2022 Leifer Mendez) | E4 interfaz Canal, E5 webhook Meta |
| raroque/**boop-agent** | MIT (© 2026 Chris Raroque) | E1 conmutador/costo, E3 madre→especialistas |
| cesarvcanal/**whatsapp-agent-bridge** | MIT (© 2026 César Canal) | E1 cola+sesión, E5 dedupe webhook |
| chatwoot/**chatwoot** | MIT salvo `enterprise/` (no copiar de ahí) | E4 modelo de datos, E5 ventana/plantillas |

Todo lo listado es copiable (patrones y hasta código) con atribución; en Apache-2.0,
conservar el aviso si se copia código literal. Nada extraído toca `ee/` ni `enterprise/`.

---

# E1 — llm.js: puerta única al cerebro (prioridad #1)

## Piezas adoptadas

1. **Contrato único request→result con conmutador de motores** — boop
   `server/runtimes/types.ts` + `runtimes/index.ts`: `RuntimeRunRequest {prompt, systemPrompt,
   tools, allowed/disallowedTools, callbacks} → {text, usage}` y un switch por
   `config.runtime`. El resto del bot llama `consultar()` y jamás sabe qué motor respondió.
2. **Cola por conversación (promise-chain por jid)** — bridge `src/server.ts:30-37`: FIFO
   estricto por chat, paralelismo natural entre chats, sin workers; se le agrega limpieza del
   Map al asentarse (leak que el bridge tiene). Es además la semilla del un-solo-escritor E4:
   la cola ES el escritor único por chat.
3. **Sesión por conversación con `resume`, persistida APENAS llega el `init`** — bridge
   `src/agent.ts:14-33` (captura de `session_id` en el evento `system/init`) + nanoclaw
   `container/agent-runner/src/providers/claude.ts` (persistir la continuation en el evento
   `init`, no al final del turno: un crash a mitad de turno no huerfanea la conversación;
   keyed por proveedor). Almacén: `data/sesiones.jsonl` con TTL (45d, alineado a
   `yaCotizado`) — nunca en RAM como el bridge.
4. **Regex de sesión inválida → retry fresco** — nanoclaw `providers/claude.ts`:
   `no conversation found|ENOENT.*\.jsonl|session.*not found` → limpiar continuation y
   partir sesión nueva.
5. **Rotación de transcript** — nanoclaw `maybeRotateContinuation`: >12MB o >14 días →
   archivar resumen markdown y renombrar el .jsonl para forzar sesión nueva. Sin esto un
   chat longevo se cuelga recargando un transcript gigante.
6. **Protocolo `<message to="destino">` + nudge** — nanoclaw `poll-loop.ts`: todo lo
   entregable va envuelto; texto suelto = scratchpad; turno sin bloques → nudge automático
   una vez. Portable directo a `claude -p`.
7. **Costo SIEMPRE medido, con el gotcha `modelUsage`** — boop `server/usage.ts:76-141`:
   preferir `msg.modelUsage` (agregado por modelo de TODA la query, puede traer varios
   modelos) sobre `msg.usage` (solo el turno final, subcuenta con tools); `costUsd` de
   `total_cost_usd`. Ledger por turno (boop `interaction-agent.ts:604-622`):
   `{fuente, conversacionId, turnId, modo, modelo, inTok, outTok, cacheR, cacheW, costoUsd,
   duracionMs}` → `data/uso-llm.jsonl` (el `llm-metricas.jsonl` con fecha 19-ago del plan).
8. **Permisos cinturón y tirantes** — boop `interaction-agent.ts:556-569` (comentario
   literal: con `bypassPermissions` el SDK puede filtrar built-ins si solo hay whitelist):
   whitelist `mcp__ns__tool` Y blacklist de built-ins (`WebSearch, Bash, Read, Write…`),
   siempre ambas.
9. **Tools propias como servidores MCP en-proceso** — boop `runtimes/claude.ts:32-71`:
   `createSdkMcpServer` + `tool(name, desc, zodShape, handler)` por namespace — así
   cotizar/despachar/tarifario entran al SDK sin proceso externo, y de paso cumplen el
   requisito "contratos MCP-compatibles" del plan.
10. **Anti-respuesta-fantasma** — boop `interaction-agent.ts:590-602`: regex de placeholders
    `(no output)/no reply` tras ciclos de tools = fallo → degradar al siguiente motor.
11. **Config snapshot por turno** — boop `runtime-config.ts` + `interaction-agent.ts:372`:
    settings store con cache TTL 30s + alias (`opus`→id completo) + UN snapshot al inicio
    del turno para que un cambio a mitad de turno no parta el turno en dos cerebros.
12. **Memoria por presupuesto de tokens, no por número de mensajes** — mastra
    `observational-memory.ts` L2757 (`shouldObserve: pendingTokens >= 30_000`) +
    `constants.ts` (buffering 20%/80%: observa en background temprano, activa tarde, nunca
    bloquea la respuesta) + continuation-hint invisible tras el corte
    (`OBSERVATION_CONTINUATION_HINT`). Registro propio `om-records.jsonl`
    (`packages/core/src/storage/types.ts` L1153: `{scope, activeObservations,
    lastObservedAt, observedMessageIds, generationCount}`); crudos recuperables con índice
    rango→offset sobre `conversaciones.jsonl` (patrón `om-tools.ts` recall).
13. **Capacidades del SDK a usar** — doc oficial: `resume`/`forkSession` (replay del
    gimnasio sin contaminar la sesión real), `canUseTool → 'approve'|'deny'|'ask'` (gancho
    E3), `maxTurns` y `maxBudgetUsd` como topes duros por turno, hooks de auditoría.

## Diseño de referencia

El pseudocódigo completo y cerrado de `llm.js` (cola + snapshot + cadena de motores +
clasificación de error + ledger) está en `informes4/agent-sdk-boop-bridge.md` §4. Contrato:

```js
consultar({ conversacionId, prompt, sistema, herramientas, permitidas, prohibidas,
            modo: 'vendedor'|'especialista'|'fondo', preguntarDueno, onTexto, onTool, onUso })
  → { texto, uso: {modelo, inTok, outTok, cacheR, cacheW, costoUsd, duracionMs},
      eventos: [{tipo:'fallback', de:'sdk', a:'cli', causa:'timeout'}, …] }
```

## Decisiones de conflicto (E1)

- **Memoria: `resume` del SDK (bridge/nanoclaw) vs historial reconstruido (boop) vs memoria
  observacional (mastra).** No son alternativas, son capas por motor: el modo `sdk` usa
  sesión nativa con `resume` (resuelve de raíz el HISTORY_LIMIT); los peldaños `cli`/`api`
  del failover siguen necesitando historial propio — y ESE historial cambia de "últimos 60
  mensajes" a corte por presupuesto de tokens (barato: contar tokens en vez de mensajes).
  La maquinaria completa Observer/Reflector de mastra (dos llamadas haiku en background)
  solo se construye si E1 descarta el Agent SDK — regla del plan: una vía, no ambas.
- **Dónde vive el session_id: RAM (bridge) vs tabla persistida (nanoclaw).** Persistido en
  JSONL, escrito en el momento del evento `init` (timing de nanoclaw, almacén nuestro).
- **Failover: ninguno de los dos repos lo tiene** (boop deja elegir motor al usuario, bridge
  no degrada). La cadena `sdk→cli→api→plantilla` recorrida por clasificación de error tipado
  (`rate_limit` espera y reintenta; `auth` NO degrada; placeholder degrada) es diseño propio
  — ver "lo genuinamente nuestro".

---

# E2 — Conocimiento-como-datos + ajustes schema-driven

## Piezas adoptadas

1. **Config del agente vive en el almacén y se materializa por arranque** — nanoclaw
   `src/types.ts` (container_configs en la DB central) + `src/container-runner.ts:132`
   (materializado a `container.json` en cada spawn). Traducción dixdybot: `ajustes.json`
   editable desde panel, snapshot materializado al inicio de cada turno/proceso — el panel
   edita datos, nunca código.
2. **Settings store con cache TTL + alias + snapshot por turno** — boop
   `runtime-config.ts`: el mismo patrón para `llm-config.json` (modo, modelo, fallbacks,
   topes) y cualquier ajuste caliente.
3. **Cifras desde datos, jamás del modelo** — parlant `canned_response_generator.py`:
   plantillas Jinja2 con fields que llenan las tools
   (`tool_call.result.canned_response_fields`), la regla de prompt de oro *"en desviación
   cuantitativa la plantilla tiene razón"* (L2110-2117), y modo CANNED_STRICT con fallback
   fijo si no hay match (nunca sale texto libre). Refuerza nuestro tarifario-en-datos: el
   precio viene de `precios.buscar`, la plantilla lo renderiza, el modelo solo redacta
   campos marcados como generativos.
4. **Lifecycle de una regla nueva: clasificar ANTES de activar** — parlant
   `core/evaluations.py:59-135` + `services/indexing/behavioral_change_evaluation.py:102-170`:
   al crear una regla desde el panel, una evaluación LLM previa responde ¿es continua?
   ¿depende del cliente? ¿es solo-tool? y esas propiedades quedan en metadata, decidiendo
   cómo se evalúa después. Retirar = `enabled:false` (soft-disable), nunca borrar.
5. **Versionado de esquema barato** — anti-lección de parlant (11 TypedDicts por versión):
   un campo `schema_version` en cada JSONL + funciones upgrade encadenadas. La idea sí, la
   maquinaria no.
6. **Cierre del loop juez→conocimiento con un click** — vocero
   `src/app/api/lab/suggestions/apply/route.ts`: la `sugerencia {pregunta, respuesta}` del
   juez se convierte en entrada del KB con un botón (editable antes de guardar). El gimnasio
   alimenta el conocimiento; el conocimiento es datos.
7. **Conocimiento como fragmentos de texto componibles** — nanoclaw
   `src/claude-md-compose.ts`: el prompt del agente se compone por fragmentos aportados por
   módulos/skills en cada arranque. Es la forma técnica de "IA madre → especialistas":
   el saber de cada dominio viaja como fragmento, no como if en el código.

## Decisiones de conflicto (E2)

- **¿Dónde viven los ajustes: DB (nanoclaw/boop) vs archivos (nuestro)?** Archivos
  JSON/YAML en el clon (git = historial y rollback gratis, doctrina DIXDY), con los DOS
  patrones robados encima: snapshot materializado por turno (nanoclaw) y cache TTL con
  alias (boop). DB solo si el panel multi-usuario lo exigiera en E6.

---

# E3 — Caminos (condición→acción con pausa-y-pregunta) + gimnasio

Es la etapa con más planos: parlant da el modelo de datos y el motor; mastra la pausa;
nanoclaw y boop el relay con el dueño; vocero el gimnasio.

## Piezas adoptadas — modelo de datos y motor

1. **Regla = frase condición→acción + gobierno** — parlant
   `src/parlant/core/guidelines.py:47-67`: `{condicion, accion?, enabled, tags,
   criticality, priority, track, metadata (continuous, espera_del_cliente…),
   composition_mode}`. Es el esquema base de la regla dixdybot; `accion: null` = regla
   observacional (disparador).
2. **Camino = grafo de pasos con tools por paso** — parlant
   `src/parlant/core/journeys.py:59-98`: `Journey {triggers: [reglas], root_id}` +
   `JourneyNode {accion, tools habilitadas SOLO en este paso}` + `JourneyEdge {source,
   target, condicion NL}`; máx UNA transición sin condición por paso (`sdk.py` ~1495).
3. **LA joya: proyección camino→reglas** — parlant
   `src/parlant/core/journey_guideline_projection.py:38-151`: cada par (arista, nodo
   destino) se convierte en una regla transitoria con id parseable
   (`journey_node:<nodo>:<arista>`) y `metadata.follow_ups` = las aristas salientes.
   Resultado: **un solo motor evalúa reglas sueltas Y pasos de camino** — el camino no es
   un runtime aparte, es azúcar sobre reglas. Simplifica E3 de raíz.
4. **Vocabulario de relaciones** — parlant `src/parlant/core/relationships.py:43-115`:
   `prioridad_sobre` (PRIORITY), `depende_de` (DEPENDENCY / DEPENDENCY_ANY con group_id
   OR), `implica` (ENTAILMENT), DISAMBIGUATION (2+ activas → preguntar al cliente cuál),
   REEVALUATION (corrió la tool → re-evaluar la regla). Subconjunto útil en el YAML.
5. **Resolver determinista post-LLM con explicabilidad** — parlant
   `src/parlant/core/engines/alpha/relational_resolver.py:15-34,112-153`: loop (máx 3) de
   dependencias con Kahn topológico → priorización relacional → prioridad numérica →
   entailment; y CADA decisión guardada como `Resolution {kind, descripción humana,
   counterparts}` — "esta regla no disparó porque X tuvo prioridad" — que es exactamente lo
   que el panel del dueño necesita mostrar. Kahn son 20 líneas; networkx no se copia.
6. **Estado del camino persistido por conversación** — parlant `core/sessions.py:243-246` +
   `engine.py:1464-1517`: camino activo si su trigger matcheó O hay path vivo;
   `journey_paths {camino_id: [pasos…]}` + `applied_guideline_ids` persistidos → en
   dixdybot van en `conversaciones.jsonl` por chat.
7. **Shape del JSON de avance** — parlant `journey_next_step_selection.py:43-49`:
   `{journey_continues, current_step_completed, applied_condition_id}` con rationale ANTES
   del booleano — mismo shape para la respuesta de `claude -p` sobre el camino activo.
8. **YAML de camino dixdybot** — propuesta completa en `informes4/parlant.md` §g: camino
   con `dominio` (agente especialista de la IA madre), `disparadores`, `pasos` con
   `espera_del_cliente`/`continua`/`modo_respuesta`/`herramientas`/`respuestas` (plantillas
   con campos origen tool), paso `tipo: pausa-dueno` con `timeout_horas` y
   `respuesta_espera`, `transiciones` (máx una sin condición) y `relaciones`.

## Piezas adoptadas — pausa-y-pregunta al dueño

9. **Snapshot de suspensión que sobrevive reinicios** — mastra
   `packages/core/src/workflows/types.ts` L380 (`WorkflowRunState {context por paso,
   suspendedPaths, resumeLabels, suspendPayload}`) + `handlers/step.ts` L359 (`suspend()`
   valida el payload — LA PREGUNTA AL DUEÑO — contra el schema del paso) + `workflow.ts`
   L3974 (`_resume`: carga por id, exige status suspended, auto-detecta el paso desde
   `suspendedPaths`, valida la respuesta del dueño contra el schema, re-ejecuta sin repetir
   pasos ya corridos). En dixdybot: snapshot JSONL `{camino_id, jid, status:'suspended',
   context, suspendedPaths, suspendPayload, timestamp}` — nada en RAM.
10. **Tarjeta al dueño + re-inyección del evento aprobado** — nanoclaw `src/router.ts`
    (`channelRequestGate`): la pregunta viaja como tarjeta, la aprobación re-inyecta el
    evento original por el mismo pipeline; todo drop queda auditado en `dropped_messages`.
    Es el patrón runtime del permission relay del plan (código de 5 letras por WhatsApp).
11. **Drafts: solo lo aprobado comete** — boop `execution-agent.ts:104-106`: toda acción
    externa del especialista se guarda como draft; únicamente el `send_draft` aprobado en
    conversación la ejecuta. Con `canUseTool → 'ask'` (SDK) como gancho en modo sdk.
12. **IA madre → especialistas** — boop `interaction-agent.ts:28-146`: dispatcher con
    prohibición explícita de responder hechos del mundo, tool `send_ack` obligatoria antes
    de trabajo lento (UX mensajería: algo visible en <2s — en WhatsApp: mensaje corto +
    typing), `spawn_agent` con tarea crisp (no el mensaje crudo). El campo `dominio` del
    YAML de camino asigna cada camino a su especialista.

## Piezas adoptadas — gimnasio

13. **Personas guionadas SIN LLM** — vocero `src/server/lab/personas.ts`: 6 guiones fijos
    (decidido, pregunta-precios, enojado, fuera-de-conocimiento, pide-humano,
    modismos/faltas) = examen de regresión determinista; el delta mide el cambio de reglas,
    no el azar del cliente simulado. Genéricas multi-rubro: por cliente solo cambia el
    guion.
14. **Juez de UNA llamada con veredicto tipado** — vocero `src/server/lab/judge.ts` +
    `src/server/ai/prompts.ts` (`buildJudgePrompt`): `{veredicto: verde|amarillo|rojo,
    hallazgos: [{tipo: alucinacion|fuera_de_kb|debio_escalar|tono, evidencia (cita
    textual), sugerencia {pregunta, respuesta}}]}`; `judge_failed` visible y fuera del
    score; alucinación = la falla más grave.
15. **Score 0-100 con delta derivado al leer** — vocero `src/app/api/lab/runs/route.ts`:
    verde=1, amarillo=0.5; el delta se calcula contra la corrida anterior al LEER, nunca se
    persiste. La serie histórica ES la tabla de corridas.
16. **Sandbox de doble candado** — vocero `pipeline.ts` (`deliverReply` persiste sin enviar
    si `isTest`) + `send.ts` L64 (el EMISOR lanza error si es test): en dixdybot,
    `enviar.js` rechaza jids de prueba además de que el gimnasio no los enrute.
17. **Replay sin contaminar** — SDK `forkSession: true` para re-jugar conversaciones reales
    (backtesting patrón Fin del plan) sin tocar la sesión viva.

## Decisiones de conflicto (E3)

- **Matcher: batches especializados de parlant vs UNA llamada.** Parlant paga decenas de
  llamadas LLM por turno (batches de 1-5 guidelines, 3 reintentos) a cambio de precisión —
  inviable con `claude -p` en costo y latencia. dixdybot evalúa TODO en una llamada por
  turno: reglas del dominio activo + camino vivo (paso actual + follow_ups) en un solo
  prompt, respuesta en un solo JSON (`{reglas_aplican: [{id, razon, aplica}], camino:
  {sigue, paso_completado, transicion_elegida}, respuesta|plantilla_id}`), y la taxonomía
  de parlant (observacional/accionable/ya-aplicada/continua) entra como CAMPOS del schema,
  no como batches. El resolver determinista corre después, gratis.
- **Pausa-y-pregunta: mastra vs nanoclaw vs boop.** Complementarios por capa, no
  excluyentes: mastra es el ALMACENAMIENTO (snapshot suspendido persistido, sobrevive
  reinicios), nanoclaw es el TRANSPORTE (tarjeta + re-inyección del evento aprobado; en
  dixdybot: push con código de 5 letras, respuesta por panel o WhatsApp), boop es la
  SEMÁNTICA (draft que solo comete aprobado; `canUseTool → 'ask'` en modo sdk). Se adoptan
  las tres en su capa.
- **Gimnasio: personas sintéticas (vocero) vs conversaciones reales (nuestro).** Se SUMAN:
  vocero aporta la regresión determinista antes/después de cada cambio (lo que hoy falta —
  el gimnasio depende de que Alejandro juegue al cliente); lo nuestro conserva el
  entrenamiento sobre chats reales con correcciones→reglas. El juez único gana el formato
  tipado de vocero (tipo + evidencia citada + sugerencia aplicable).

---

# E4 — Abstracción de canal + un-solo-escritor

## Piezas adoptadas — la interfaz Canal

1. **Esqueleto builderbot, probado en 15+ canales** —
   `packages/bot/src/provider/interface/provider.ts`: solo 6 miembros abstractos
   (initVendor, busEvents, sendMessage, saveFile, before/afterHttpServerInit) + 6 eventos
   canónicos (message/ready/require_action/auth_failure/notice/host) + template method
   `initAll`. `ready` = socket abierto (Baileys) o webhook verificado (Meta);
   `require_action` solo existe en canales QR. El core jamás ve el vendor.
2. **Refinamientos nanoclaw** — `src/channels/adapter.ts`: factory que devuelve `null` si
   faltan credenciales (canal apagado sin romper el boot); `isMention` resuelto POR el
   adaptador (semántica de plataforma, el router no adivina); `defaults` declarativos por
   contexto DM/grupo.
3. **La interfaz Canal mínima de dixdybot** — JSDoc completo en `informes4/builderbot.md`
   §f. Núcleo:
   - `MensajeEntrante {convId, canal, idNativo, tipo explícito
     ('texto'|'media'|'boton'|…), texto, msgIdNativo, ts, crudo}` — tipo en campo propio,
     NO sentinel en el texto (el sentinel de builderbot es herencia de su motor de
     keywords); botón/lista colapsan al título como texto (eso sí se copia: el cerebro
     queda agnóstico de botones).
   - `ResultadoEnvio {ok, msgIdNativo?, motivo: 'fuera_de_ventana'|'auth'|'rate'|…}` —
     anti-patrón a NO copiar: builderbot hace `catch(e){return e}` y se traga los fallos.
   - `ventana(convId) → {abierta, expiraTs}` y `enviarPlantilla(convId, nombre, idioma,
     vars)` de PRIMERA CLASE (ningún repo las pone en el contrato — hueco confirmado en
     builderbot; el plan ya lo exigía).
   - Evento `estado_envio {msgIdNativo, estado: entregado|leido|fallido, motivo}` — los ✓✓
     reales del panel.
   - `escribiendo(convId, msgIdNativo)` acepta ambos porque la asimetría es real: Baileys
     teclea por jid, Meta exige el wamid del mensaje ENTRANTE.
   - `guardarMedia(msg)` bajo demanda: el binario nunca viaja por el bus (builderbot
     saveFile).
4. **Adaptación gradual**: `CanalWaBaileys` envuelve `enviar.js` + el listener actual sin
   tocar el cerebro; `ventana()` responde siempre `{abierta: true}`. En E5, `CanalWaMeta`
   es "otra factory".

## Piezas adoptadas — un-solo-escritor y datos

5. **Los 3 invariantes del un-solo-escritor** — nanoclaw header de
   `src/session-manager.ts` + `src/db/schema.ts`: (i) un escritor por archivo, (ii) el
   proceso que no es dueño JAMÁS escribe el archivo del otro — lo suyo se anota en un
   ledger propio (tabla `delivered` en SU db), (iii) namespaces de secuencia disjuntos
   (seq par host / impar contenedor) para que dos escritores nunca colisionen ni resuelvan
   la fila equivocada. Traducción: `envios.jsonl` se formaliza como ledger `delivered` con
   `{message_out_id, platform_message_id, status, delivered_at}`.
6. **Dedup de entrega** — nanoclaw `src/delivery.ts`: `inflightDeliveries: Set` contra
   polls concurrentes, filtrar pendientes contra el ledger, marcar con INSERT OR IGNORE,
   3 intentos y `markDeliveryFailed`; contador de intentos en RAM a propósito (reiniciar =
   segunda oportunidad).
7. **El esquema de 5 tablas** — chatwoot `db/schema.rb` + `app/models`, veredicto en
   `informes4/chatwoot.md` §f:
   - `contactos` (persona, agnóstica de canal; únicos por teléfono/email/identifier)
   - `identidades` — LA pieza que no tenemos (ContactInbox, `schema.rb:705`):
     `{contacto_id, canal_id, source_id}` con **UNIQUE (canal_id, source_id)** — la llave
     de enrutamiento de todo lo entrante; al crear identidad nueva, cascada
     identifier→email→teléfono para unificar a la persona
     (`contact_inbox_with_contact_builder.rb`); fusión de duplicados reasignando todo
     (`contact_merge_action.rb`).
   - `canales` `{tipo, config{} (credenciales/provider), plantillas{}, bot_activo,
     horario}` (provider_config jsonb de chatwoot).
   - `conversaciones` `{estado ('pendiente_bot'|'abierta'|'resuelta'|'dormida'), asignado
     ('bot'|'humano'), snoozed_until, waiting_since, first_reply_at}` — handoff bot↔humano
     COMO DATOS (`conversation.rb:83,174,289`: pending=bot, `bot_handoff!`), y de regalo
     los recordatorios dormidos y las métricas de espera del Kanban.
   - `mensajes` `{tipo ('entrante'|'saliente'|'actividad'|'plantilla'), remitente_tipo
     ('contacto'|'bot'|'humano'), source_id_externo (wamid → dedup de webhooks +
     correlación de acks), estado ('enviado'|'entregado'|'leido'|'fallido'), privado}`
     (`message.rb:87-115`) — resuelve EN el dato el "¿quién cotizó, el bot o Alejandro?"
     que hoy cruza archivos; + anti-flood por mensajes/minuto (`message.rb:288`).
   Solo el un-solo-escritor escribe estas 5 tablas; paneles/Kanban/repartidor leen.
8. **Identidad thread/resource** — mastra `packages/core/src/memory/types.ts` L39:
   thread = conversación-en-un-canal, resource = cliente-final dueño de todos sus threads.
   Mapea a conversacion/contacto del esquema anterior y prepara E6.
9. **Endurecimiento Baileys HOY (retro-portable a 6.7.23)** — builderbot `bailey.ts`
   L1161-1219 (backoff exponencial 1s→30s cap, máx 10 intentos, lista blanca de códigos
   reconectables incl. 429/5xx, cerrar el socket viejo antes de recrear) + nanoclaw
   `channels-branch/whatsapp.ts` (loggedOut→borrar auth / shutdown limpio→PRESERVAR auth y
   NO reconectar en paralelo — trunca creds.json a 0 bytes; `resolveWaWebVersion` scrape
   wppconnect + fallback contra el 405 por versión WA vencida; `getMessage` desde
   `sentMessageCache`; `cachedGroupMetadata` SIN traducir participantes — la PREVENCIÓN del
   "esperando el mensaje" que complementa nuestra auto-sanación-cura). Alimenta también el
   circuit breaker de E0.

## Decisiones de conflicto (E4)

- **Contrato de canal: builderbot vs nanoclaw.** Esqueleto de builderbot (la evidencia:
  15+ canales sobre la misma interfaz) + los 3 refinamientos de nanoclaw (factory-null,
  isMention del adaptador, defaults por contexto) + lo que ninguno tiene (ventana,
  enviarPlantilla, ResultadoEnvio honesto, estado_envio). Ambos MIT.
- **Persistencia: SQLite un-escritor (nanoclaw) vs JSONL disciplinado (nuestro) vs
  Postgres (chatwoot/vocero).** Se queda JSONL con la disciplina de nanoclaw formalizada
  (un escritor por archivo, ledger delivered, secuencias disjuntas) y los CAMPOS de
  chatwoot; SQLite de nanoclaw queda como cantera si el JSONL muestra contención
  (ratificado por el plan). Postgres no: escala que no tenemos, dependencia que la doctrina
  evita.
- **Clave de conversación: teléfono pelado sin prefijo (builderbot) vs compuesto.**
  Compuesto `canal:idNativo` (`wa-baileys:569…`, `wa-meta:569…`) + tabla `identidades` para
  unificar a la persona — builderbot esquiva el problema porque asume un canal por proceso;
  dixdybot quiere N canales sobre un cerebro. La lección que sí se copia: la normalización
  del id vive EN el canal, la identidad en el core.
- **Ventana de 24h: no modelarla (builderbot) vs calcularla (chatwoot).** Chatwoot:
  `can_reply?` calculado del último mensaje ENTRANTE con duración por tipo de canal
  (servicio puro ~70 líneas, `message_window_service.rb`), NUNCA persistida como campo. El
  core consulta `ventana()` ANTES de enviar; el "enviar-y-ver-si-falla" de builderbot queda
  solo como red de seguridad (motivo `fuera_de_ventana` → degradar a plantilla y
  registrar).
- **Serialización de entrada: cola concurrent:1 de builderbot-Meta.** No se copia como
  pieza aparte — ese rol lo cumple nuestra cola por conversación (E1) + el un-solo-escritor
  detrás de `enviar()`.

---

# E5 — Canales oficiales de Meta

## Piezas adoptadas

1. **Webhook Meta completo, robable tal cual (MIT)** — builderbot
   `packages/provider-meta/src/meta/core.ts` + `utils/webhookSignature.ts` +
   `provider.ts:249-260`: (i) verificación de alta GET (`hub.mode`/`verify_token`/responder
   `challenge`, L163-185) con `ready` emitido ahí; (ii) firma HMAC `X-Hub-Signature-256`
   con `timingSafeEqual` sobre `req.rawBody` — los bytes crudos capturados en el hook
   `verify` de body-parser ANTES del parseo (re-serializar no es byte-idéntico), y en la
   clase BASE, no en el provider; (iii) `extractStatus` que aplana `statuses[]` y convierte
   `failed` en aviso → alimenta nuestro evento `estado_envio`. Va al Worker `meta-buzon` de
   la pre-etapa.
2. **Higiene de webhook** — bridge `src/server.ts:17-59`: responder 200 ANTES de procesar
   (timeout corto del proveedor), dedupe por `messageId` con Set acotado a 2000 y evicción
   por inserción (Meta reentrega), allowlist con silencio.
3. **Plantillas en dos mitades** — chatwoot: catálogo cacheado en el canal
   (`channel_whatsapp.message_templates` jsonb + `sync_templates` periódico) + uso viajando
   EN el mensaje (`template_params` validado con JSON-schema, `message.rb:48-63`). Árbol de
   decisión al enviar (`send_on_whatsapp_service.rb:8-13`): hay template_params →
   plantilla; si no, `can_reply?` → mensaje de sesión; si no → `failed` con
   `external_error` visible en el hilo.
4. **Convivencia Baileys↔Cloud como factory de provider** — chatwoot
   `app/models/channel/whatsapp.rb:65,117`: el canal delega
   `send_message/send_template/sync_templates/media_url` a un `provider_service`
   intercambiable; cambiar de proveedor = cambiar `provider` + `provider_config`, mismo
   esquema. Es el molde para que la migración Coexistence sea un cambio de config, no de
   arquitectura (recordando la regla del plan: en el MISMO número el corte es
   Baileys→Cloud, no convivencia).
5. **Gotchas Meta puntuales** — builderbot `provider.ts`: `prefixMap {549→54, 521→52}` +
   `fixPrefixMetaNumber` (solo si llega tráfico ARG/MEX); typing por wamid del entrante
   (`typing_indicator` vía markAsRead, L1151-1180); botones máx 3 con título ≤16 chars
   (límite real de Meta).
6. **Baileys v7 / LID** — nanoclaw `channels-branch/whatsapp.ts`: `translateJid` LID→phone
   vía `remoteJidAlt`/`signalRepository.lidMapping` + evento `lid-mapping.update`; pairing
   gate por `creds.me` (no `creds.registered`). Mientras Baileys siga vivo como rampa de
   clientes nuevos, el upgrade se hace como ellos: pinear exacto 7.0.0-rc.9 (RC sin
   mantención) + copiar sus mitigaciones + conservar nuestra auto-sanación como red.

## Decisiones de conflicto (E5)

- **Cómo enterarse del fuera-de-ventana: status failed a posteriori (builderbot) vs cálculo
  a priori (chatwoot).** Ya decidido en E4: calcular antes, degradar a plantilla; el status
  failed queda como confirmación y auditoría, no como mecanismo.
- **Identidad WA Cloud: fono sin `+` (chatwoot wa_source_id) vs jid.** Cada canal normaliza
  su `source_id` propio (`wa-baileys` = jid, `wa-meta` = fono sin `+`) y la tabla
  `identidades` los une a la misma persona — así la migración Coexistence conserva TODO el
  historial del cliente aunque cambie el source_id.

---

# E6 — Multi-cliente clon-por-cliente

## Piezas adoptadas

1. **Módulos como skills idempotentes con desinstalador** — nanoclaw `.claude/skills/add-*`:
   cada canal/feature es una skill con directivas parseables que copia código + agrega UNA
   línea de import al barrel + `REMOVE.md` para revertir. Es "módulos administrables por
   cliente" sin plataforma: el instalador es un documento ejecutable — calza exacto con la
   doctrina DIXDY de clones + promoción al maestro.
2. **Persona/conocimiento por cliente componible por fragmentos** — nanoclaw
   `src/claude-md-compose.ts`: el prompt del bot de cada cliente se compone de base +
   fragmentos de los módulos activos, en cada arranque.
3. **Wiring por cliente como datos, no código** — nanoclaw `src/router.ts`:
   `engage_mode/sender_scope/accumulate` son columnas del almacén; conectar un chat nuevo
   pasa por la tarjeta al dueño (channelRequestGate), no por editar código.
4. **Una ronda activa por cliente, lock en el almacén** — vocero `schema.ts` L344: índice
   UNIQUE parcial (`WHERE status='running'`) — sobrevive reinicios del proceso; nada de
   mutex en RAM. Patrón para gimnasio, rondas y cualquier trabajo por cliente.
5. **resource = cliente-final** — mastra: el mismo cliente en WhatsApp + Instagram + correo
   es UN resource con N threads; la tabla `identidades` de E4 lo materializa.
6. **Credenciales por canal en config{}** — chatwoot `provider_config` jsonb: cada clon
   lleva sus credenciales en su `.env.local`/config, mismo esquema en todos.
7. **API key por cliente con expiración** — ratificado por la doc legal del Agent SDK
   (producto para terceros = API key obligatoria; boop/bridge lo confirman) — ya estaba en
   el plan.

## Decisiones de conflicto (E6)

- **Multi-tenancy: organización-en-DB (vocero/chatwoot) vs clon-por-cliente (nuestro).**
  Clon-por-cliente se mantiene (doctrina DIXDY: aislamiento por filesystem, datos del
  cliente solo en su clon — el mismo aislamiento que nanoclaw logra con carpetas de sesión).
  De los multi-tenant solo se roban los patrones puntuales (lock por índice parcial,
  config por canal), no la arquitectura.

---

# LOS 5 PLANOS DE ORO

1. **La proyección camino→reglas de Parlant**
   (`journey_guideline_projection.py:38-151`): cada arista+nodo del camino se convierte en
   una regla transitoria con `follow_ups` — un solo motor evalúa reglas sueltas Y pasos de
   camino; el camino es azúcar sobre reglas, no un runtime aparte. Reduce E3 (el corazón
   del plan) a UN evaluador + UN resolver determinista explicable (Kahn + Resolution con
   porqué humano para el panel). Con la decisión clave: todo en UNA llamada por turno, la
   taxonomía de Parlant como campos del schema, jamás sus batches.

2. **llm.js queda completamente especificado** juntando 4 fuentes: contrato
   request→result + conmutador + costo por `modelUsage` + ledger por turno (boop), cola
   promise-chain por conversación (bridge), session_id persistido en el evento `init` +
   regex de sesión inválida + rotación de transcript (nanoclaw), y
   `resume`/`forkSession`/`canUseTool`/`maxBudgetUsd` (doc SDK). Lo único que ningún repo
   trae — el failover tipado `sdk→cli→api→plantilla` — es diseño propio y es exactamente el
   seguro que el vaivén de Anthropic exige. Pseudocódigo cerrado en
   `informes4/agent-sdk-boop-bridge.md` §4.

3. **La interfaz Canal definitiva**: esqueleto builderbot (6 eventos canónicos + 6 métodos,
   probado en 15+ canales) + factory-null/isMention/defaults de nanoclaw + lo que ningún
   repo modela y dixdybot exige: `ventana()` calculada a lo chatwoot, `enviarPlantilla()`
   de primera clase y `ResultadoEnvio` honesto. Hace de E5 "otra factory" y el webhook Meta
   (verifyToken + HMAC-sobre-rawBody + extractStatus) se copia tal cual de
   provider-meta (MIT). JSDoc completo en `informes4/builderbot.md` §f.

4. **El plano de datos: disciplina nanoclaw + esquema chatwoot.** Un escritor por archivo,
   lo del otro proceso se anota en ledger propio (`delivered`), secuencias disjuntas,
   dedup con Set en vuelo + 3 reintentos; y las 5 tablas de chatwoot (contactos /
   identidades con UNIQUE(canal, source_id) / canales / conversaciones con estado-handoff /
   mensajes con source_id externo, estado ✓✓ y remitente bot|humano) como upgrade directo
   de `conversaciones.jsonl` + `envios.jsonl`. Resuelve EN el dato el dedup de webhooks,
   los acks reales, el "¿quién cotizó?" y el handoff bot↔humano.

5. **La pausa-y-pregunta al dueño en 3 capas** (el diferenciador de mercado según el plan):
   snapshot suspendido persistido con la pregunta como payload validado por schema y resume
   que sobrevive reinicios sin repetir pasos (mastra `WorkflowRunState`/`_resume`), tarjeta
   al dueño + re-inyección del evento aprobado por el pipeline normal (nanoclaw
   `channelRequestGate`), y la semántica draft-que-solo-comete-aprobado + `canUseTool →
   'ask'` (boop). Tres repos, tres capas, cero contradicción: almacenamiento, transporte y
   semántica.

(Mención de honor: el gimnasio de vocero — personas guionadas sin LLM + juez tipado con
evidencia citada + sugerencia aplicable con un click + score con delta derivado + candado
sandbox en el emisor — es el upgrade completo de nuestro gimnasio y el gate que deja
desplegar E3 con juez ≥4,0.)

---

# LO QUE NINGÚN REPO RESUELVE (lo genuinamente nuestro)

1. **Failover automático de cerebro** `sdk→cli→api→plantilla` con clasificación de error
   tipado (rate_limit espera, auth no degrada, placeholder degrada) y cada salto como
   evento en el ledger. boop deja elegir motor al usuario; bridge no degrada; nanoclaw solo
   clasifica rate-limits. Nadie más vive de la gracia de `claude -p` con suscripción — este
   seguro es nuestro y es la prioridad #1.
2. **La economía suscripción-primero**: modo `cli` con suscripción como peldaño barato +
   medición con fecha (llm-metricas antes del 19-ago) para presupuestar. Todos los repos
   asumen API key desde el día uno.
3. **Aprendizaje en caliente desde conversaciones reales con reanudación**: corrección del
   dueño → regla destilada → aplicada en vivo reversible → la conversación pausada se
   REANUDA con lo aprendido. Vocero cierra el loop desde guiones sintéticos; parlant
   clasifica reglas nuevas; nadie aprende de producción y retoma el chat pausado.
4. **Ventana-24h y plantillas DENTRO del contrato del canal** con degradación automática
   (calcular → si igual falla, plantilla de re-apertura + evento). Chatwoot la calcula como
   servicio aparte; builderbot la ignora; nadie la pone en la interfaz.
5. **La migración Coexistence del número VIVO con fecha** (Baileys→Cloud del mismo número
   antes del 30-sep, identidades que conservan el historial al cambiar el source_id).
   Builderbot trata cada provider como proceso aparte; ningún repo migra un número en
   producción.
6. **El dueño no-técnico en iPhone como primera superficie**: tarjetas + diff + Aprobar sin
   canvas, permission relay por WhatsApp con código de 5 letras y "primera respuesta gana",
   respuesta enlatada inmediata + escalada 30 min. Mastra suspende workflows para
   desarrolladores; nanoclaw tarjetea a un usuario técnico; nadie diseña para un gásfiter
   con el teléfono en la mano.
7. **La doble muralla de precios**: tarifario fuera del LLM (ya vivo) + validador
   `precioCoherente` POST-generación. Parlant llega hasta "la plantilla tiene razón";
   nuestro validador de salida no existe en ningún repo — y tras el exploit del chatbot de
   Meta, se vende como diferencial de seguridad.
8. **Clon-por-cliente con promoción al maestro** (doctrina DIXDY): los aprendizajes de un
   cliente suben al libro maestro y los clientes nuevos nacen con ellos. Las skills de
   nanoclaw instalan features; ninguna arquitectura leída modela una FLOTA de clientes que
   aprende en red.
