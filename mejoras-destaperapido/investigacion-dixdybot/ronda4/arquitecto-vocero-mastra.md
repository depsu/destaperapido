# Informe arquitecto — vocero-crm (laboratorio de auto-evaluación) + mastra (memoria observacional y suspend/resume)

Clones leídos en:
- `/private/tmp/claude-501/-Users-alejandroriveracarrasco-SaSS-DIXDY-clientes-destaperapido/5acfd0ef-e8b4-49b2-965d-26a7a76d1c5b/scratchpad/clones/vocero-crm`
- `/private/tmp/claude-501/-Users-alejandroriveracarrasco-SaSS-DIXDY-clientes-destaperapido/5acfd0ef-e8b4-49b2-965d-26a7a76d1c5b/scratchpad/clones/mastra`

Licencias:
- **vocero-crm: MIT** (LICENSE, Copyright (c) 2026 Kevin Belier). Copiar patrones y hasta código con atribución es libre.
- **mastra: Apache-2.0** en todo salvo los directorios `ee/` (`packages/core/src/auth/ee/`, `packages/server/src/server/auth/ee/`), que tienen licencia enterprise propia (LICENSE.md). Nada de lo extraído aquí toca `ee/`; `packages/memory` y `packages/core` declaran `"license": "Apache-2.0"` en sus package.json. Copiar el DISEÑO es libre; si se copiara código literal, mantener el aviso Apache.

---

## PARTE 1 — vocero-crm: el Laboratorio de auto-evaluación (→ gimnasio E3-E4)

Contexto del repo: CRM de WhatsApp multi-tenant en español (Next.js + Drizzle/Postgres), agente IA que responde por acciones JSON (`reply | update_lead | move_stage | handoff | none`) y un "Laboratorio" que corre clientes simulados contra el agente REAL en sandbox y lo califica.

### 1.1 Arquitectura del laboratorio (archivos concretos)

Todo el laboratorio son **3 archivos de servidor + 2 rutas API + 2 tablas**:

| Pieza | Archivo |
|---|---|
| Personas simuladas | `src/server/lab/personas.ts` |
| Runner (corrida + sandbox) | `src/server/lab/runner.ts` |
| Juez + score | `src/server/lab/judge.ts` |
| Prompt del juez | `src/server/ai/prompts.ts` (`buildJudgePrompt`) |
| Historial con delta | `src/app/api/lab/runs/route.ts` |
| Aplicar sugerencia del juez | `src/app/api/lab/suggestions/apply/route.ts` |
| Tablas | `src/lib/db/schema.ts` (`agent_test_run` L328, `agent_test_case` L352) |
| Candados sandbox | `src/server/ai/pipeline.ts` (`deliverReply` L209-254) y `src/server/inbox/send.ts` (L64) |

### 1.2 Cómo define los perfiles de cliente simulado

`src/server/lab/personas.ts`: **el cliente simulado NO usa LLM**. Son 6 personas con guion fijo (`script: string[]`) — determinismo total del lado del cliente; solo el agente evaluado es el real:

```ts
export type Persona = {
  key: string;           // "comprador_decidido", "pregunton_precios", "cliente_enojado",
                         // "fuera_de_kb", "pide_humano", "errores_modismos"
  label: string;
  description: string;
  phone: string;         // teléfono sintético estable (5210000000001...), jamás real
  contactName: string;   // "[Prueba] Comprador decidido"
  script: string[];      // líneas fijas que el "cliente" envía una a una
};
```

Las 6 personas cubren exactamente los modos de falla del juez: compra directa, mareo de precios, cliente enojado (tono), pregunta fuera del conocimiento, pide humano (debe escalar), y ortografía/modismos ("ke onda, si benden pintura?").

### 1.3 El runner: sandbox sobre el pipeline real

`src/server/lab/runner.ts`:
- `startRun()` inserta `agent_test_run` con `status:'running'`; el **lock de concurrencia es un índice parcial UNIQUE en BD** (`schema.ts` L344-347: `uniqueIndex("test_run_org_running_uq").on(organizationId).where(status='running')`) — máx. 1 corrida activa por organización, sin mutex en memoria.
- Corrida **fire-and-forget in-process** (sin cola externa), timeout global 10 min (`Promise.race`), progreso por SSE (`publish` del bus de eventos).
- `runConversation()` (L169-233): crea un **contacto sintético ARCHIVADO** (no aparece en listas ni genera leads) y una conversación con `isTest: true`; inyecta cada línea del guion como mensaje entrante y llama `runAgentTurn(convId)` — **el MISMO pipeline de producción**, secuencial y sin debounce; **corta al primer handoff**.
- Sandbox de doble candado: `pipeline.ts` `deliverReply` → si `conversation.isTest`, `persistTestOutbound` (persiste el mensaje saliente, JAMÁS toca la API de Meta); y además `send.ts` L64 **lanza** `SendError` si algo intenta enviar una conversación de test — cinturón y tirantes.

### 1.4 El juez (prompt completo y contrato)

`src/server/lab/judge.ts` + `src/server/ai/prompts.ts` `buildJudgePrompt` (L61-90):
- **UNA llamada de juez por conversación** (no por mensaje). Salida validada con Zod:

```ts
Verdict = { veredicto: "verde"|"amarillo"|"rojo",
            hallazgos: [{ tipo: "alucinacion"|"fuera_de_kb"|"debio_escalar"|"tono",
                          evidencia: string,                      // cita textual del transcript
                          sugerencia?: { pregunta, respuesta } }] }  // entrada P/R lista para el KB
```

- System prompt (resumen fiel): "Eres un evaluador de calidad independiente… Eres estricto: la alucinación (inventar datos que no están en el conocimiento) es la falla más grave" + el esquema JSON + reglas: tema no cubierto → `fuera_de_kb` (o `alucinacion` si afirmó datos concretos); pidió humano sin escalado → `debio_escalar`; `sugerencia` cuando una nueva P/R evitaría el problema.
- User prompt: `PERSONA SIMULADA` + `COMPORTAMIENTO CONFIGURADO` (perfil del agente) + `CONOCIMIENTO CONFIGURADO` (KB completo) + `TRANSCRIPT COMPLETO` etiquetado CLIENTE/AGENTE.
- Si el juez devuelve JSON inválido tras reintentos → caso `judge_failed`, **visible en el reporte y excluido del score**; la corrida continúa.
- Score 0-100 (`computeScore`): verde=1, amarillo=0.5, rojo=0; `judge_failed` fuera del denominador; `Math.round(100·puntos/juzgados)`.

### 1.5 Cómo persiste los deltas históricos

**No persiste el delta: lo calcula al leer.** `src/app/api/lab/runs/route.ts` GET: lista las últimas 50 corridas y para cada una busca hacia atrás la anterior con `status:'done'` y `score !== null` → `delta = run.score - prev.score`. Lo único persistido es `agent_test_run` (`score` entero, `startedAt/finishedAt`, `status`, `error`) y `agent_test_case` (`transcript` jsonb, `veredicto`, `hallazgos` jsonb, `conversationId`). Simple y suficiente: el historial de scores ES la serie; el delta es derivado.

### 1.6 Cierre del loop: hallazgo → conocimiento

`src/app/api/lab/suggestions/apply/route.ts`: la `sugerencia` del juez se aplica **con un click** creando la entrada `kind:'qa'` en `kb_entry` (el front deja editarla antes). El hallazgo del juez se convierte directamente en conocimiento del agente — exactamente el ciclo conocimiento-como-datos de E2.

### 1.7 Qué mejoraríamos con nuestro juez/replay existente

Lo que ya tenemos mejor en el gimnasio del bot (`/entrenar`, juez opus, replay 🎬, correcciones→reglas): evaluamos conversaciones **reales**, con nota 1-5 por conversación y correcciones que se destilan en reglas. Vocero solo evalúa guiones sintéticos.

Lo que vocero aporta y nos falta (robar para E3-E4):
1. **Regresión determinista**: personas guionadas fijas = mismo examen antes/después de cada cambio de reglas/precios/conocimiento → el delta del score mide el cambio, no el azar del cliente simulado. Hoy nuestro gimnasio depende de que Alejandro juegue al cliente.
2. **Score agregado 0-100 + delta vs corrida anterior**: una cifra por corrida, serie histórica; el delta se deriva al leer (no persistirlo).
3. **Hallazgos tipados con evidencia citada + sugerencia accionable**: nuestro juez da nota y comentario; el de vocero obliga `tipo` + `evidencia` (cita textual) + `sugerencia` en el formato exacto del conocimiento — un click y el hallazgo es una entrada más del KB.
4. **Candado sandbox en el EMISOR** (send lanza si `isTest`), no solo en el orquestador — en dixdybot: `enviar.js` debe rechazar jids de prueba, además de que el gimnasio no los enrute.
5. **Lock de corrida en el almacén** (índice único parcial), no en RAM — sobrevive reinicios del proceso.
6. Personas a copiar casi tal cual (adaptadas a rubro por cliente): decidido, pregunta-precios, enojado, fuera-de-conocimiento, pide-humano, modismos/faltas. Son genéricas multi-rubro: solo cambia el guion, no la maquinaria.

---

## PARTE 2 — mastra: Observational Memory y suspend/resume (→ E1 y E3)

### 2.1 Memoria resource/thread (el marco)

`packages/core/src/memory/types.ts` L39: `StorageThreadType = { id, title?, resourceId, createdAt, updatedAt, metadata? }` — **thread = una conversación; resource = el usuario/entidad dueño de todas sus conversaciones**. Toda opción de memoria lleva `scope: 'thread' | 'resource'`: `lastMessages` (cola cruda reciente), `semanticRecall` (búsqueda vectorial con scope), `workingMemory` (perfil vivo por thread o por resource). En dixdybot: thread = chat jid, resource = teléfono del cliente final (cruza WhatsApp + correo del mismo cliente en E4).

### 2.2 Observational Memory — la respuesta al HISTORY_LIMIT artesanal

Vive en `packages/memory/src/processors/observational-memory/` (~15.300 líneas; núcleo: `observational-memory.ts` 3712, `observer-agent.ts` 1691, `reflector-runner.ts` 1260, `processor.ts` 423, `constants.ts`, `types.ts`).

**¿Cómo decide resumir el historial crudo?** Por **presupuesto de tokens, no por número de mensajes** (nuestro HISTORY_LIMIT=60 corta por cantidad, ciego al tamaño). `constants.ts` `OBSERVATIONAL_MEMORY_DEFAULTS`:
- `observation.messageTokens: 30_000` — umbral: cuando los mensajes crudos pendientes superan 30k tokens, se observan. La decisión literal: `pendingTokens >= threshold` (`observational-memory.ts` L1026 y L2757 `shouldObserve`).
- `observation.bufferTokens: 0.2` + `bufferActivation: 0.8` — **buffering asíncrono**: cada 20% del umbral observa en background (fire-and-forget) y ACTIVA los chunks al 80%, de modo que el usuario nunca espera una resumida síncrona.
- `reflection.observationTokens: 40_000` — cuando las observaciones mismas superan 40k tokens, corre el Reflector.
- Modelo barato por defecto para ambos (`google/gemini-2.5-flash`) — el resumen no gasta el modelo caro; en dixdybot sería `claude -p` con haiku.

**Dos agentes de memoria** (misma "psique", dos roles):
- **Observer** (`observer-agent.ts`, `OBSERVER_EXTRACTION_INSTRUCTIONS`): convierte mensajes crudos en observaciones datadas línea a línea. Reglas de oro exportables tal cual: distinguir ASERCIONES del usuario ("tengo dos hijos" → hecho) de PREGUNTAS; marcar CAMBIOS DE ESTADO como superseding ("se cambió de A a B (ya no B)"); doble ancla temporal (cuándo se dijo + cuándo ocurre lo referido); "las aserciones del usuario son autoritativas".
- **Reflector** (`reflector-agent.ts` `buildReflectorSystemPrompt`): "You are the memory consciousness… reflections become the ENTIRE memory" — reorganiza/condensa las observaciones en una nueva **generación** cuando crecen demasiado, preservando todo lo importante.

**¿Dónde guarda el resumen?** En un **registro dedicado de storage**, no en el hilo de mensajes: `ObservationalMemoryRecord` (`packages/core/src/storage/types.ts` L1153-1274). Campos clave:
- `scope: thread|resource`, `threadId|null`, `resourceId` — un registro activo por resource (con secciones `<thread id="...">` para atribuir) o por thread.
- `activeObservations: string` — el resumen vivo que se inyecta.
- `bufferedObservationChunks[]` — observaciones hechas en background esperando activarse.
- Cursor `lastObservedAt` + `observedMessageIds[]` (salvaguarda anti-re-observación) — así sabe qué mensajes crudos ya fueron digeridos.
- Contadores: `totalTokensObserved`, `observationTokenCount`, `pendingMessageTokens`; flags `isObserving/isReflecting/isBufferingObservation/isBufferingReflection`; `generationCount` (cada reflexión = generación nueva); `config` JSON congelada.

**¿Cómo se inyecta?** `processor.ts` `ObservationalMemoryProcessor.processInputStep`: reemplaza el historial crudo ya observado por un bloque system `<observations>…</observations>` + un mensaje de continuación `<system-reminder>` (`OBSERVATION_CONTINUATION_HINT` en `constants.ts`: "continúa natural, no menciones memoria ni mensajes faltantes") para que el corte sea invisible. Las instrucciones `OBSERVATION_CONTEXT_INSTRUCTIONS` enseñan a resolver conflictos: **la observación más nueva supersede**, y las acciones planeadas cuya fecha ya pasó se asumen hechas.

**Los crudos no se pierden — recall:** cada grupo de observaciones lleva `range="startId:endId"` apuntando a los mensajes originales; la tool `recall` (`packages/memory/src/tools/om-tools.ts`) pagina de vuelta con niveles de detalle (low = truncado para escanear, `detail:"high"` + `partIndex` para el contenido exacto). Instrucciones en `constants.ts` `OBSERVATION_RETRIEVAL_INSTRUCTIONS`. En dixdybot los crudos YA viven en `conversaciones.jsonl` — solo falta el índice rango→offset.

### 2.3 Suspend/resume de workflows con snapshot (→ plano de la pausa-de-tema E3)

**Esquema del snapshot** — `WorkflowRunState` (`packages/core/src/workflows/types.ts` L380-405):
```ts
{ runId, status,                            // 'suspended' entre otros
  context: { input, [stepId]: SerializedStepResult },  // resultado de CADA paso ya corrido
  serializedStepGraph,                       // el grafo del flujo, serializado DENTRO del snapshot
  suspendedPaths: { [stepId]: number[] },    // qué paso(s) quedaron parados y en qué ruta
  resumeLabels: { [label]: {stepId, foreachIndex} },  // nombres amigables para reanudar
  waitingPaths, requestContext, value/state, timestamp, tracingContext }
```

**Cómo se suspende** — `handlers/step.ts` L359-390: el step recibe una función `suspend(payload, {resumeLabel})`; valida el payload contra el **schema de suspend del step** (`validateStepSuspendData`), anota `suspendedPaths[step.id] = executionPath` y registra el label. El payload es **la pregunta al dueño** (en vocero-dixdybot: "¿doy este descuento?"). El snapshot completo se persiste con `persistWorkflowSnapshot` en el storage (`workflow.ts` L2413, `handlers/entry.ts` L206) — snapshot inicial ya en `createRun` (estado 'pending').

**Cómo sobrevive reinicios** — TODO el estado vive en el snapshot persistido, nada en RAM. `_resume` (`workflow.ts` L3974-4110):
1. `loadWorkflowSnapshot({workflowName, runId})` desde storage; exige `status === 'suspended'`.
2. Resuelve el paso: por `label` → `snapshot.resumeLabels[label]`, o **auto-detección** desde `suspendedPaths` (incluye workflows anidados vía `suspendPayload.__workflow_meta.path`); si hay varios suspendidos, exige especificar.
3. Valida `resumeData` (la respuesta del dueño) contra el schema de resume del step.
4. Rehidrata `stepResults` desde `snapshot.context`, mezcla `snapshot.requestContext`, retoma el tracing (`snapshot.tracingContext`) y re-ejecuta desde la ruta suspendida — los pasos ya corridos no se repiten porque su resultado está en `context`.

---

## Qué se copia como DISEÑO (no dependencia) → etapa de dixdybot

1. **E1 (llm.js):** presupuesto por tokens en vez de HISTORY_LIMIT por mensajes; contexto = `activeObservations` + cola cruda reciente + continuation-hint invisible. Plano: `constants.ts` (umbrales y los 3 prompts de contexto), `observational-memory.ts` L2757 (`shouldObserve`).
2. **E1/E2:** registro de memoria por cliente-final como JSONL propio (`om-records.jsonl`) con los campos de `ObservationalMemoryRecord` que aplican: `{scope, jid|telefono, activeObservations, lastObservedAt, observedMessageIds, observationTokenCount, generationCount}`. Plano: `packages/core/src/storage/types.ts` L1153.
3. **E1:** Observer/Reflector como dos llamadas `claude -p` baratas en background (el patrón buffering 20%/80% = observa temprano, activa tarde, nunca bloquees la respuesta). Plano: `observer-agent.ts` (reglas de extracción), `reflector-agent.ts` (condensación por generaciones).
4. **E3 (caminos con pausa-y-pregunta):** snapshot de camino en JSONL: `{camino_id, jid, status:'suspended', context (pasos ya hechos), suspendedPaths, suspendPayload (pregunta al dueño), resumeLabels, timestamp}`; resume = cargar por id, validar la respuesta del dueño contra el schema del paso, re-ejecutar desde `suspendedPaths`. Plano: `workflows/types.ts` L380, `handlers/step.ts` L359, `workflow.ts` L3974.
5. **E3-E4 (gimnasio):** personas guionadas deterministas + juez de UNA llamada con veredicto tipado (`tipo/evidencia/sugerencia`) + score 0-100 con delta derivado al leer + candado sandbox en el emisor + lock de corrida en disco. Plano: `src/server/lab/{personas,runner,judge}.ts` y `src/server/ai/prompts.ts` de vocero-crm (MIT — se puede copiar código directamente con atribución).
6. **E2 (conocimiento-como-datos):** la `sugerencia {pregunta, respuesta}` del juez aplicable con un click al KB (`suggestions/apply/route.ts`) — el gimnasio alimenta el conocimiento, cerrando el loop.
7. **E4/E6 (multi-cliente):** el par thread/resource de `memory/types.ts` L39 como identidad canónica: thread=canal-conversación, resource=cliente-final; y el lock por índice único parcial de vocero como patrón para "una corrida/ronda activa por cliente".
