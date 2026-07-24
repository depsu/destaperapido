# dixdybot — Arquitectura "Núcleo Nuevo"

**Ángulo:** diseñar el producto correcto a 2-3 años (gateway de canales + cerebro + caminos + panel, multi-cliente y multi-rubro) y vaciar el bot viejo dentro del nuevo por estrangulamiento, sin que el bot vivo (que vende hoy) muera ni un día.

**Base:** auditorías del código vivo (`/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot`), investigación verificada (Baileys/Cloud API, Instagram, caminos/ARIA/Parlant, ToS de Claude Code, censo open source) y doctrina DIXDY (`docs/23`).

---

## 0. Resumen ejecutivo

El dixdybot nuevo es **un solo proceso "motor" que es el único escritor de datos**; panel, gimnasio y crons son clientes HTTP de su API. Los canales (WhatsApp hoy, Instagram mañana, y un canal simulador para entrenar) son adaptadores detrás de un contrato de 4 funciones con mensaje canónico y `contacto_id` cross-canal. El conocimiento del negocio vive en **caminos**: archivos markdown+frontmatter (uno por camino, versionados con git) que el matcher carga selectivamente (3-7 por turno), con un bucle **pausa-y-pregunta** que convierte cada hueco de conocimiento en un camino nuevo aprendido en caliente. El cerebro es un wrapper único de Claude (`cli` con la Max de Alejandro hoy, `api` Messages como destino del tráfico conversacional) con failover automático. La joya del tracking actual (ledger irreversible, dedup, `fechaISO`, `precioCoherente`, contrato Supabase del repartidor) sobrevive **intacta**. La migración son 6 etapas estranguladoras con flags de rollback de una línea; la Etapa 0 (2-3 días) ya paga: commitear los fixes vivos sin versionar, watchdog 401→push y rotación de logs.

---

## 1. Principios de diseño

1. **Un solo escritor.** El problema estructural #1 del vivo son 3 procesos escribiendo 17 archivos JSON con read-modify-write sin lock (incidentes reales 16 y 22-jul). En el núcleo nuevo, SOLO el motor escribe `data/`; todo lo demás pasa por su API HTTP en localhost. Cero locks, cero carreras, cero infra nueva (sin Redis, sin Postgres: archivos + HTTP, como ya hace dashboard.mjs pero con la flecha al revés).
2. **El canal es un detalle.** Ningún módulo del core ve un `jid`. Ve `conv_id` y `contacto_id`. El jid, el IGSID de Instagram o el "chat-sim-42" del gimnasio viven solo dentro de su adaptador.
3. **Números en datos, prosa en el modelo.** La lección más rentable del vivo (precios.js + candado `precioCoherente`: la nota del juez subió de 2,44 a 4,0 sobre todo por mover conocimiento del prompt a código). Se generaliza: toda cifra vive en el `datos:` de un camino; el modelo la cita, jamás la redacta ni la inventa.
4. **Conocimiento = archivos, no prompt.** Persona compacta (~2 KB) + caminos como archivos git-versionados (rollback estilo Decagon gratis) + carga selectiva por turno (estilo Agent Skills / Parlant) en vez del prompt plano de 27-30 KB con 68 reglas que hoy se diluyen.
5. **Lo irreversible se registra apenas sale.** El contrato de `envios.jsonl` (integracion.js:604-610) es sagrado y se conserva letra por letra en el ledger nuevo.
6. **Doctrina DIXDY.** Nada se construye al lado de lo que existe: avisos van por avisos-worker, lo pesado por la cola única del maestro, los procesos por launchd, el core se promueve al maestro (pagando la deuda de divergencia template↔vivo: 7.119 líneas vivas vs 1.912 en plantilla).
7. **Cada trasplante con vuelta atrás.** Cada etapa de migración se activa con un flag en config; revertir = 1 línea + reinicio (<5 s con KeepAlive de launchd).

---

## 2. Vista de pájaro

```
                       ┌──────────────────────────────────────────────────────┐
  WhatsApp (Baileys) ──┤  canales/wa-baileys  ─┐                              │
  WhatsApp Cloud API ──┤  canales/wa-cloud ────┤   (contrato Canal)           │
  Instagram DM ────────┤  canales/ig-graph ────┤                              │
  Gimnasio ────────────┤  canales/sim ─────────┘                              │
                       │            │ MensajeCanon                            │
                       │            ▼                                         │
                       │  MOTOR (único proceso escritor)                      │
                       │   canon → portero → política → extractor → selector  │
                       │   → [¿gap? → dudas/pausa] → cerebro → validadores    │
                       │   → outbox por canal → ledger                        │
                       │   (rama paralela: detector de confirmación → acciones)│
                       │            │                                         │
                       │   API HTTP localhost :8790  ← panel, gimnasio, crons │
                       └──────┬──────────┬──────────┬─────────────────────────┘
                              ▼          ▼          ▼
                        cerebro/     caminos/    acciones/
                        (claude -p   (*.md git)  (PDF, correo, Supabase
                         ó API)                   repartidor, seguimientos)
```

**Topología de procesos** (launchd, como hoy):
- `motor` — adaptadores de canal in-process + pipeline + API :8790 + panel estático. Único escritor de `data/`.
- Trabajos pesados con Claude (compilación masiva de caminos, juez nocturno, minería de chats) — se encolan en la **cola única del maestro** (`tareas.json`) y los toman las rondas launchd existentes; el resultado vuelve por la API del motor. No se crea ningún cron nuevo.
- avisos → `avisos-worker` existente (`scripts/avisar.py`, ruta por config, nunca hardcodeada como hoy en integracion.js:55).

**Almacenamiento** (sin DB nueva, doctrina "nativo primero"):
- `data/eventos-YYYY-MM.jsonl` — log de eventos append-only, fuente de verdad, rotado por mes (lección del bot.error.log de 53 MB).
- `data/estado.json` — snapshot del estado derivado (conversaciones, fichas, contadores anti-ban, dedup), escrito atómico tmp+rename (patrón store.js, que ya funciona). Al arrancar: cargar snapshot + re-reducir la cola del log. Los topes anti-ban y `seenMsgIds` dejan de vivir solo en RAM (hueco actual: cada reinicio resetea MAX_BOT_REPLIES_PER_CHAT=12 y el dedup de 600 s).
- `data/caminos/*.md` — repo git propio (historial, diff, rollback).
- `data/ledger.jsonl` — irreversibles (heredero directo de envios.jsonl, misma semántica).
- Escala futura: si el volumen multi-cliente duele, `node:sqlite` (Node ≥22.5; el Mac corre v22.18.0) como índice derivado reconstruible. No en v1.

---

## 3. Modelo canónico de datos

```jsonc
// contacto — la persona, cross-canal
{ "contacto_id": "p_01J...", "nombre": "María",
  "telefonos": ["+56912345678"],
  "identidades": [ {"canal":"wa","id":"56912...@s.whatsapp.net"},
                   {"canal":"ig","id":"IGSID-178..."} ],
  "ficha": { "comuna":"Puente Alto", "servicio":"destape", "direccion":null, "fecha":null } }

// conversacion — un hilo en un canal
{ "conv_id": "c_01J...", "canal": "wa", "canal_id": "56912...@s.whatsapp.net",
  "contacto_id": "p_01J...",
  "modo": "bot" | "manual" | "pausada_camino" | "pausada_duda",
  "etapa": "conociendo" | "cotizado" | "agendado" | "entregado" | "cobrado" | "perdido",
  "camino_activo": { "id":"agendar-entrega", "paso":2, "capturado":{"fecha":"2026-08-01"} } }

// mensaje canónico (evento msg_in / msg_out en eventos.jsonl)
{ "ev":"msg_in", "ts":..., "conv_id":"c_...", "autor":"cliente|bot|humano",
  "tipo":"texto|imagen|audio|pdf|ubicacion", "texto":"...", "media_ref":"media/ab12.jpg",
  "canal_meta":{...}, "entrega":{"ack":2} }

// evento de auditoría del turno (el "por qué dijo esto")
{ "ev":"turno", "conv_id":"c_...", "caminos_cargados":["precio-destape","politica-iva"],
  "camino_usado":"precio-destape", "modo_cerebro":"cli", "modelo":"opus",
  "ms":8400, "costo_usd":0.0, "validadores":{"precio":"ok"}, "decision":"responder" }
```

**Resolución de identidad:** el teléfono une identidades cuando existe (hoy es el cruce chat↔entrega en entregas.js); en Instagram no hay teléfono, así que (a) un camino estándar "capturar teléfono para coordinar" lo pide cuando la conversación avanza a agenda, y (b) el panel ofrece "es la misma persona" para merge manual. `enlaces.json` del vivo es el precedente directo.

---

## 4. Capa de canales

### 4.1 Contrato `Canal` (canales/canal.md)

```js
// Cada adaptador exporta exactamente esto:
export const canal = {
  nombre: 'wa',                       // wa | wa-cloud | ig | sim
  start(emit) {},                     // emite {tipo:'msg_in', msg: MensajeCanon} y {tipo:'salud', ...}
  async enviar(canal_id, salida) {},  // salida: {texto | media | pdf}; → {ok, canal_msg_id}
  capacidades() {},                   // {ventana_horas:24, puede_iniciar:false, largo_max, formatos, costo_por_msg}
  salud() {}                          // {conectado, ultimo_evento, detalle}
}
```

Toda la rareza del canal vive dentro del adaptador: reconexión, Bad MAC, acks, eco fromMe. El motor no sabe qué es un jid.

### 4.2 `wa-baileys` (hoy)
Envuelve lo que ya está endurecido y probado: la capa de conexión de index.js (procesar `append`, saltar eco fromMe — fix del incidente 22-jul en index.js:383 —, stub CIPHERTEXT), `enviar.js` (envío en frío + auto-sanación Bad MAC + watchdog de doble check, HEAL_MS 180s/MAX_HEAL=1), `quiet.js` (+rotación de stderr, que hoy no filtra console.error), `link-code.mjs`. Se agrega lo que la auditoría marcó: **watchdog de 401 loggedOut** (hoy index.js:303-306 deja el proceso vivo pero ciego para siempre y nadie avisa — brecha #1) con push por avisos-worker, backup atómico nocturno de `auth/`, y Baileys **pineado a versión exacta** (hoy `^6.7.0` flotante; evaluar 7.0.0-rc13 con mapeos LID en el gimnasio antes de subir — el Bad MAC es causa LID según los issues #2234/#635 y las release notes de rc10).

### 4.3 `wa-cloud` (paralelo, trimestre)
Adaptador contra la Cloud API oficial de Meta. El webhook NO expone el Mac: un **Cloudflare Worker buzón** (mismo patrón que correo-worker: worker + cola + drenado local) recibe los webhooks de Meta, encola en D1/KV, y el motor drena por poll. Presupuesto con tarifas Chile verificadas (fila propia, no "Rest of LatAm"): utility US$0,02 (~CLP 19), marketing US$0,0889 (~CLP 83); respuestas en ventana de 24 h gratis **solo hasta el 30-sep-2026** — desde el 1-oct-2026 los mensajes de servicio se cobran a tarifa utility salvo ventanas CTWA de 72 h. Al volumen actual (~470 respuestas/mes) el peor caso post-octubre es ~CLP 9.000-15.000/mes: barato a cambio de cero Bad MAC, cero QR, acks confiables por webhook y ban-con-proceso en vez de ban arbitrario. Requisitos: Business Manager + número verificable (250 conversaciones iniciadas/día sin verificar — las respuestas no cuentan); Coexistence permite usar el mismo número que la app (limitaciones: sync 6 meses, sin grupos). **Gestión externa de Alejandro** (Guardián): abrir la cuenta Meta.
La estrategia dual Baileys+Cloud tras el mismo contrato es la arquitectura de Evolution API, imitada, no adoptada.

### 4.4 `ig-graph` (después)
Vía única legal: "Instagram API with Instagram Login" (desde jul-2024 no exige página de Facebook): cuenta profesional + `instagram_business_basic` + `instagram_business_manage_messages` + webhooks (mismo worker-buzón). Con app propia y cuentas administradas con rol basta **Standard Access sin App Review**; App Review + Business Verification (3-14 días hábiles) solo si dixdybot atiende cuentas de terceros. Reglas duras que el adaptador declara en `capacidades()`: solo responder (el usuario escribe primero), ventana 24 h, **jamás HUMAN_AGENT desde el bot** (auditado y revocable). Las vías no oficiales (instagrapi, mautrix-meta) quedan descartadas con cuentas de clientes. No existe un "Baileys de Instagram" confiable en 2026 (censo verificado); BuilderBot confirma que la costura correcta es un Provider por canal sobre la vía Meta oficial.

### 4.5 `sim` (el gimnasio es un canal)
El simulador habla el mismo contrato: los escenarios dorados y los clientes simulados entran por `start(emit)` como cualquier cliente real y ejercitan el pipeline COMPLETO (extractor, selector, cerebro, validadores, acciones en modo dry-run). Es el patrón "Laboratorio" de vocero-crm (MIT, legible en una tarde) hecho canal. Mata de raíz el defecto actual de que el gimnasio y el dashboard re-implementan la lógica del bot.

### 4.6 `politica.mjs` (gating por canal, config editable)
Generaliza gating.js: debounce, delays humanos, topes por hora/día, horario, auto-pausa por dueño — pero **por canal, persistido en estado.json y editable desde el panel dentro de rangos duros en código** (hoy 40/h y 200/día viven invisibles en .env). Incluye el interruptor global del bot y la vista global de pausas que hoy no existen.

---

## 5. Cerebro

### 5.1 Un solo wrapper, una sola cola
`cerebro/cerebro.mjs` reemplaza los **4 spawns dispersos** del vivo (brain.js 120s, extraer.js 90s sin --model, calidad.js 150s, aprender-core.mjs sin timeout) por una cola única con prioridades (`conversar > extraer > dudas/compilar > juez`), concurrencia 1-2, timeout y kill por tarea. Conserva la firma que funciona: `getReply(historia, contexto, pushName)` con modos `stub | cli | api`.

- **Modo `cli` (hoy):** `claude -p` con `CLAUDE_CODE_OAUTH_TOKEN` de `claude setup-token` (token oficial de 1 año; despertador ⏰ anual para renovarlo). Blindajes documentados: **jamás pasar `--bare`** (será default de `-p` y no lee OAuth), fijar `autoUpdatesChannel: stable` + `minimumVersion` (el CLI se auto-actualiza y puede romper el bot), medir cupo con `/usage` (se comparte con el uso interactivo de Alejandro).
- **Modo `api` (destino):** llamadas Messages delgadas. Postura ToS honesta (veredicto verificado): un bot comercial 24/7 no es "ordinary, individual usage"; la migración del ~90% conversacional a API **no es opcional, es el destino**. `claude -p` + Max queda para el trabajo agéntico de Alejandro: compilar caminos, entrenar, juez, migraciones. Si dixdybot se vende a terceros: **API key por cliente** (exigencia literal de la doc).
- **Failover automático:** parsear eventos `api_retry` tipados del stream-json (`rate_limit`, `overloaded`, `billing_error`, `oauth_org_not_allowed`) **y además** exit≠0 con stderr (el login expirado no llega por api_retry); circuit breaker → conmutar a `api` N minutos → push por avisos-worker. En `-p`, `ANTHROPIC_API_KEY` presente siempre gana: el failover es literalmente setear una env var.

**Costos estimados a volumen actual** (~4 chats/día, ~1.500 llamadas/mes, prompt ~8-10 K tokens con prefijo cacheado, salida ~300 tokens; precios vigentes jul-2026: Opus 4.8 $5/$25, Sonnet 5 $3/$15 con intro $2/$10 hasta 2026-08-31, Haiku 4.5 $1/$5, cache reads ~0,1x):
- Conversar en Opus 4.8 por API: ~US$25-40/mes. En Sonnet 5: ~US$10-20 (con intro ~US$8-15). Extractor en Haiku 4.5: <US$5.
- Juez nocturno por **Batches API (-50%)**: centavos.
- Con Max (cli): US$0 marginal en plata, pero consume el cupo compartido.
Todo estimación de orden de magnitud: el propio `total_cost_usd` de `claude -p` y `usage` de la API lo miden real desde la semana 1. La decisión Opus-vs-Sonnet la toma el gimnasio (A/B con juez), y la plata la decide Alejandro (Guardián).

### 5.2 Salida tipada (muere el token mágico)
`--json-schema` / `output_config.format` con contrato:

```jsonc
{ "tipo": "responder", "texto": "..." }
{ "tipo": "silencio", "motivo": "..." }                       // hereda [[SILENCIO]]
{ "tipo": "falta_camino", "pregunta_al_dueno": "...", "contexto": "..." }
```

Esto también mata la clase de bugs de parseRules (aprender-core.mjs:43-51) que convirtió `[]`, un fence ``` y un comentario meta en reglas de producción.

### 5.3 Ensamblador de prompt (`cerebro/prompt.mjs`)
Orden estable pensado para prompt caching en modo api (prefijo fijo primero):
1. `config/persona.md` compacta (~2 KB, presupuesto duro; prohibido contener cifras — lección "140 fantasma").
2. Capacidades y política del canal (del adaptador).
3. Índice de títulos de TODOS los caminos activos (~10-15 tokens c/u, estilo Agent Skills).
4. Cuerpo completo de los 3-7 caminos relevantes (selector) + camino activo con su paso.
5. Ficha del contacto + estado de entrega del repartidor (como hoy: "ya cerró, no re-cotices").
6. Últimos N mensajes (N=30 con extractor incremental; hoy 60 por HISTORY_LIMIT).
Resultado: ~6-10 KB por turno vs 27-30 KB planos actuales, y sin las 3 capas que hoy compiten (BOT_PERSONA de 10.599 chars vs bloques generados vs 68 reglas planas — el conflicto IVA vivo se vuelve imposible por construcción: la política vive en UN camino).
En modo api: `cache_control` al final del bloque estable (persona+índice); ojo mínimo cacheable (4096 tokens en Opus/Haiku 4.5, ~2K en Sonnet) — el prefijo se diseña para superarlo.

### 5.4 Extractor incremental (`cerebro/extractor.mjs`)
Conserva el prompt del vivo (pieza rescatable) pero deja de re-analizar 200 mensajes por turno: recibe la ficha previa + solo mensajes nuevos, y devuelve el delta. Corre en Haiku por api (o cli). **Su salida es LA ficha única** que consumen motor y panel: muere la detección duplicada de comuna (precios.js:88 vs dashboard.mjs:314 con listas distintas) y las 3 regex de precio en 3 módulos.

### 5.5 Seguridad
Los turnos conversacionales corren `claude -p` **sin herramientas** (solo texto→json): un cliente malicioso no puede inyectar prompts que toquen disco. Las únicas sesiones con tools contra la API del motor son las del Entrenador (§6.5), iniciadas por Alejandro.

---

## 6. Caminos — el corazón

### 6.1 Formato: un archivo markdown por camino

```markdown
---
id: precio-destape-domicilio
titulo: Precio de destape en domicilio
cuando: cliente pregunta precio de destape de alcantarillado en casa o depto
prioridad: normal            # critico = bloquea la accion si falta un dato requerido
estado: activo               # borrador | activo | apagado | vencido
vigencia: null               # o "hasta 2026-08-31" (resuelve los flip-flops tipo IVA)
requiere: [comuna]           # datos de ficha necesarios antes de la respuesta final
excluye: []                  # ids incompatibles       (relaciones estilo Parlant)
depende_de: []
datos:                       # CIFRAS Y HECHOS: el modelo los cita, jamás los redacta
  precio_centrica: 60000     # CLP neto
  precio_lejana: 75000
  incluye: "máquina eléctrica hasta 15 m"
respuesta_fija: null         # si existe, se envía literal (canned response)
escenarios: [precio-pte-alto, precio-sin-comuna]   # dorados ligados (gate al guardar)
origen: duda:d_4f2a          # trazabilidad: qué duda/corrección lo parió
creado: 2026-07-24T10:00:00Z
version: 3
---
## Qué hacer
1. Confirmar comuna (dato requerido: si falta, preguntarla).
2. Dar el precio de la tabla según zona, SIEMPRE neto + IVA aparte.
3. Ofrecer agendar hoy si es urgencia.
## Qué NO hacer
- No dar precio sin comuna. No prometer hora exacta sin confirmar.
```

Por qué este formato: lo edita un no-técnico desde un formulario del panel Y lo edita Claude conversando; git regala versionado+diff+rollback (Decagon cobra por eso); el modelo de datos es el de Parlant (condición→acción, relaciones, canned responses) sin adoptar su motor; el índice+cuerpo bajo demanda es Agent Skills nativo del stack `claude -p`.

### 6.2 Selector (`cerebro/selector.mjs`)
v1 determinista y barato: keywords del `cuando` + filtros por etapa/ficha + prioridad al `camino_activo`; empate de 2 candidatos con score similar → el cerebro recibe ambos y el patrón de clarificación pregunta corto. Si los caminos escalan a cientos (multi-cliente), v2: clasificador Haiku por api (~centavos). Registrar en el evento `turno` qué caminos se cargaron: es la métrica y el "por qué dijo esto".

### 6.3 Runtime del camino activo + patrones transversales (`caminos/runtime.mjs`)
La conversación lleva `camino_activo {id, paso, capturado}` persistido. Los **patrones de reparación se implementan UNA vez a nivel sistema** (arquitectura Rasa CALM, copiada, no su código comercial): corrección ("no, es en La Florida" → actualiza ficha y re-evalúa el paso), digresión (pregunta de otro tema → responde con otro camino y VUELVE al paso pendiente), clarificación (2 caminos candidatos → pregunta corta). Ningún camino individual reimplementa esto.

### 6.4 Pausa-y-pregunta (generaliza dudas.js — lo genuinamente original)
Nada open source entrega este bucle llave en mano (censo verificado; ARIA lo valida en producción en TikTok Pay con 150 M MAU). Detección en 3 puntos:
(a) el cerebro emite `falta_camino` tipado cuando no tiene camino ni dato para responder algo concreto (hoy jamás pausa: dice "el equipo confirma el valor" y la venta se enfría);
(b) checkpoints del motor antes de acciones (precio no coherente, dato faltante — los disparadores actuales de integracion.js:773-905);
(c) selector con score 0 en un mensaje con intención de negocio.

Flujo:
1. Conversación → `pausada_camino` (pausa POR conversación, persistida — patrón interrupt+checkpointer de LangGraph replicado sobre nuestros archivos, sin adoptar la librería). **Fallback honesto inmediato al cliente** (rubro de urgencia, no se le deja en visto): "Déjame confirmarlo con el equipo y te escribo en unos minutos 🙏".
2. Duda a `dudas.jsonl` + **push por avisos-worker** con deep link al panel. La UI ofrece: opciones sugeridas con acción ejecutable (patrón `accion:{endpoint,body}` del vivo, conservado), texto libre, y el selector "solo esta vez" vs "crear camino".
3. Respuesta de Alejandro → (a) borrador de respuesta para ESE chat con preview editable (patrón conservado del panel actual) y la conversación se reanuda; (b) si "crear camino": `caminos/compilador.mjs` destila el camino → **chequeo de conflictos** → guarda con `origen: duda:id` + commit git.
4. Timeout configurable (default 10 min): segundo fallback al cliente ("apenas lo confirme te aviso ¿te parece?") y recordatorio a las 2 h (módulo recordatorios existente). La duda nunca se repregunta: `respuestaPrevia` se generaliza — la respuesta queda como camino (global) o como excepción de esa conversación, ya no clavada al jid.

### 6.5 Edición conversacional — el Entrenador
Chat en el panel que es una sesión `claude -p` (Max, trabajo de Alejandro: ToS-limpio) **con tools apuntando a la API del motor**. "Desde agosto el destape sube a 65 lucas en céntricas" → localiza el camino, propone el diff (datos.precio_centrica 60000→65000 + vigencia), Alejandro toca Aplicar → `POST /api/caminos/:id` (valida esquema, corre conflictos, commit, corre escenarios ligados). Toda edición — panel, Entrenador o duda — pasa por esa MISMA puerta.

### 6.6 Conflictos (3 capas, al guardar — estilo ARIA)
1. Determinista: solapamiento de keywords del `cuando` + claves de `datos` con valores contradictorios + `excluye/depende_de` violados.
2. `claude -p` compara el camino nuevo contra los activos: ¿contradice? ¿duplica? ¿deja obsoleto? → muestra diff y pregunta cuál gana (el viejo puede quedar `vencido` con `vigencia`).
3. Regresión: los escenarios dorados ligados corren en el canal sim antes de activar.
Esto reemplaza el "NO repitas ni contradigas" dicho al mismo LLM que destila (única defensa actual, que dejó el conflicto IVA vivo 4 días y multiplicó 35 correcciones en 79 reglas).

### 6.7 Métricas por camino
Del evento `turno` + transiciones de etapa: usos, tasa de cierre post-uso, último uso, y lista de gaps (dudas sin camino + `falta_camino` emitidos). Tabla ordenable en el panel; los caminos sin uso en 60 días se proponen para archivo.

### 6.8 Arranque en frío
Job en la cola única (técnica Agent Workflow Memory, ICML 2025: inducir workflows desde trayectorias): `claude -p` lee BOT_PERSONA + aprendizajes.jsonl (68 activas) + precios.js + conversaciones.jsonl + envios.jsonl y propone **20-30 caminos en `borrador`**; Alejandro los aprueba en lote en el panel. Reglas de estilo puro → persona.md; cifras → `datos:`. La consolidación 68→~30 pendiente desde el 21-jul se hace aquí, una sola vez, con revisión humana.

---

## 7. Panel (uno solo, sobre la API del motor)

Muere la tríada dashboard.mjs (1.897 líneas, ~50 endpoints) + dashboard.html (191 KB) + entrenar.html: re-implementaban extracción y comuna por su cuenta. El panel nuevo es cliente puro de la API; si el motor cae, panel en solo-lectura (honesto).

| Vista | Qué se ve / qué se edita |
|---|---|
| **1. Bandeja** | Kanban con UNA taxonomía canónica (Conociendo→Cotizado→Agendado→Entregado→Cobrado + carril Perdido visible — hoy conviven 5 STAGES en dashboard.mjs:206 y 4 LIFE en dashboard.html:1927 y los perdidos desaparecen). Badges de canal (WA/IG/sim). Interruptor global del bot + resumen de pausas (nuevo). Dormidos 💤. |
| **2. Conversación** | Hilo canónico multi-canal, tarjetas de correo/cotización/entrega, ficha editable (lo manual gana a la IA — patrón conservado), acciones con preview editable antes de enviar (conservado), y **"por qué dijo esto"** por mensaje del bot (caminos cargados, camino usado, validadores, modo/modelo/costo — del evento `turno`). |
| **3. Cerebro** | persona.md editable con historial git; lista de caminos (crear/editar/borrador/apagar, diff de versiones, métricas, gaps); buzón de dudas; tarifas = vista tabular de los `datos:` de caminos (los precios POR FIN visibles y editables sin tocar código ni reiniciar). |
| **4. Entrenamiento** | Gimnasio integrado (canal sim): escenarios dorados, clientes simulados, nota del juez con delta histórico tras cada cambio (patrón vocero-crm); Entrenador (chat §6.5). **Una sola entrada de feedback**: seleccionar mensaje → corregir → el compilador propone destino (persona / camino nuevo / edición de camino / solo esta vez). Hoy hay 5 entradas y 2 UIs con vocabulario distinto. |
| **5. Operación** | Salud por canal (conectado, cierres del día, cola outbox, Bad MAC del día), política anti-ban editable en rangos seguros, integraciones (repartidor, correo, Supabase), log de avisos. Hoy todo esto es invisible en .env. |
| **6. Números** | Embudo único, cierres, y **plata real**: el evento `cobro {monto}` (§9) cierra la brecha del embudo económico. |

---

## 8. Entrenamiento y calidad

- **Escenarios dorados** (`gimnasio/escenarios/*.yml`): historia simulada + expectativas deterministas ("menciona $60.000", "NO dice IVA incluido", "pregunta comuna") + rúbrica blanda para el juez. Corren contra el motor real vía canal sim con acciones en dry-run.
- **Gates:** al guardar un camino corren sus escenarios ligados; suite completa nocturna (cola única; juez por Batches API a mitad de precio si modo api); antes de activar lotes (arranque en frío).
- **Juez:** hereda calidad.js (nota 1-5, actor/replay 🎬). Baseline medido para comparar: 2,44 (20-jul) → 2,65 (21-jul) → 4,0 (22-jul, n=2); embudo 59 chats → 12 cotizaciones → 6 entregas (50% cierre post-cotización).
- **Sombra (clave de la migración):** el motor genera EN PARALELO la respuesta del cerebro nuevo sin enviarla; el juez compara vivo vs sombra por turno; tablero de deltas en el panel. Muestreo 1 de cada 2-3 turnos para cuidar cupo Max.
- DeepEval (ConversationSimulator, métricas multi-turno) queda anotado como opción futura; el canal sim + juez propio lo cubre sin dependencia nueva.

---

## 9. Tracking punta a punta (la joya, intacta)

- **`ledger.mjs`** = envios.jsonl generalizado: `{ts, tipo: cotizacion|entrega|seguimiento|confirmacion|cobro, conv_id, contacto_id, canal, dedup_key, datos}`. Reglas conservadas literal: se escribe APENAS sale lo irreversible; dedup `yaCotizado` (45 días) / `yaDespachado` (∞). **Nuevo: evento `cobro {monto_real}`** — hoy el cobro es solo un estado en Supabase y el monto real no se registra en ninguna parte; el bridge lo trae del panel del repartidor o el panel lo pide al marcar Cobrado.
- **`acciones/`** envuelve las piezas puras rescatadas TAL CUAL: `fechaISO/fechaFinISO` (integracion.js:105-201, único juez de fechas en español), `precioCoherente` (integracion.js:277-294, generalizado para validar contra los `datos:` de caminos ± IVA), `construirConfigCotizacion`, `construirEntrega`, PDF + Resend + correo-worker.
- **Contrato Supabase INTOCADO:** `entrega {id, fecha, informado_at, data jsonb, card_html, eliminado}` con upsert idempotente por id vía `entrega_bridge.py` (solo se saca la ruta absoluta hardcodeada de las líneas 16-18 a config) y `entrega_estado` escrito por el repartidor fluyendo de vuelta al Kanban y al prompt. El panel del repartidor no nota el cambio de sistema.
- **Desacople conservado:** la rama de integración corre suscrita a `msg_in`, no a la respuesta del bot (herencia de index.js:509): aunque el cerebro calle o el chat esté en manual, una confirmación del cliente dispara el análisis, con guardias anti-doble-disparo (enVuelo + dedup persistente).
- **Deudas saldadas:** TODA salida pasa por el outbox del canal (muere el envío directo de seguimiento.js); muere la doble contabilidad RAM+disco; `prepararEntrega` sigue construyendo sin enviar (integracion.js:641-660) — esa costura ES el multi-canal.

---

## 10. Despliegue

| | **Mac mini de Alejandro (hoy)** | **VPS Linux (mañana/producto)** |
|---|---|---|
| Pros | Ya corre todo: launchd, Max, Tailscale, scripts Python del maestro, Chrome con logins; costo $0; doctrina-compliant | Uptime real; Claude Code es first-class en Linux (Ubuntu 20.04+, 4 GB, repos firmados); systemd; aislado de la vida doméstica |
| Contras | Punto único doméstico (luz/internet/updates de macOS); cupo Max compartido con el uso interactivo | Sin Keychain (credenciales JSON 0600); **la vía suscripción en un servidor comercial es exactamente lo que los ToS desaconsejan** → en VPS el cerebro conversacional va por API key sí o sí |
| Veredicto | **Quedarse aquí durante toda la migración** | Migrar cuando dixdybot tenga 2+ clientes; gracias a §5.1 es un cambio de `.env`, no de código |

- **Fallback del cerebro:** cadena `cli(Max) → api(ANTHROPIC_API_KEY)` automática (§5.1) + aviso push al conmutar + presupuesto mensual API con alerta (plata = pregunta al Guardián).
- **Webhooks sin exponer el Mac:** worker-buzón en Cloudflare (patrón correo-worker existente), motor drena por poll; Tailscale ya cubre el acceso remoto al panel (patrón del panel actual en el iPhone).
- **Backups:** `auth/` de Baileys atómico nocturno, `data/` + repo git de caminos con rsync/rclone cifrado (destino lo decide Alejandro), logrotate.

---

## 11. Multi-cliente / multi-rubro

- **Core en el maestro:** `DIXDY/dixdybot/` con CERO datos de cliente — paga la deuda señalada por la auditoría (regla de promoción incumplida a escala: 24 archivos/7.119 líneas vivas vs 12/1.912 en template). docs/24 se reescribe (v3) describiendo este sistema.
- **Instancia por cliente:** `clientes/X/dixdybot/` = `config/` (negocio.yml: rubro, canales, integraciones, políticas; persona.md; acciones habilitadas) + `data/` (caminos, eventos, ledger). Sin código. Nada del core sabe qué es un "destape": el rubro vive en persona + caminos + acciones declaradas (`config/acciones.yml` — para destaperapido: cotizar-pdf, entrega-supabase, correo).
- **Orquestación:** dixdybot se suma a las **rondas multi-cliente launchd existentes** (correo/ads/scout) — no nace un orquestador nuevo.
- **Identidad del cerebro por cliente:** con Alejandro operando, cli/api según §5; vendido a terceros, API key del cliente (ToS) — y ahí el costo API es un renglón del precio del servicio.
- **Prueba de generalidad (Etapa 5):** segundo cliente piloto de OTRO rubro montado solo con config + caminos nuevos; si exige tocar código del core, el core está mal y se corrige ahí.

---

## 12. Plan de migración (estrangulamiento, el vivo nunca muere)

Cada etapa tiene flag de rollback en config (`cerebro: nuevo|viejo`, `transporte: adapter|vivo`, `panel: nuevo|viejo`); revertir = 1 línea + reinicio.

### Etapa 0 — Cimientos que ya pagan (días 1-3) ✅ entregable en días
Cirugías pequeñas AL VIVO que el núcleo hereda:
1. **Commitear los fixes sin versionar** de src/index.js y src/quiet.js (los arreglos del 21/22-jul que sostienen producción están fuera de git — riesgo crítico y gratis de cerrar).
2. **`salud.mjs` + avisos:** watchdog que detecta 401 loggedOut/socket ciego/proceso caído y hace push por avisos-worker (brecha #1: hoy el bot puede quedar mudo para siempre sin que nadie sepa). Entregable visible: Alejandro recibe push si el bot muere.
3. Rotación de logs (bot.error.log llegó a 53 MB en 5 días) + backup atómico nocturno de `auth/` y `data/`.
4. Rutas absolutas fuera del código (integracion.js:55, aprender-core.mjs:19, entrega_bridge.py:16-18 → .env/config).
5. Fijar el CLI: `autoUpdatesChannel: stable` + `minimumVersion`; generar `claude setup-token`; pin exacto de Baileys.

### Etapa 1 — El motor nace leyendo al vivo (semanas 1-2, solo-lectura, riesgo cero)
- `motor` v0 TAILEA los archivos del vivo (conversaciones.jsonl, envios.jsonl, dudas.jsonl, estados) y los proyecta al modelo canónico (guardando `canal_id`=jid: siempre hay vuelta atrás). No escribe nada del vivo.
- Panel nuevo v0 (Bandeja + Conversación + "por qué dijo esto" parcial) en :8790, conviviendo con el viejo en :8789. Alejandro compara lados con datos reales.
- **Arranque en frío de caminos** (§6.8): 20-30 borradores propuestos; aprobación en lote.

### Etapa 2 — Cerebro nuevo en sombra (semanas 2-4)
- `cerebro/` + `prompt.mjs` + `selector` corriendo EN SOMBRA sobre turnos reales (muestreo 1/2-3): genera sin enviar; el juez compara contra la respuesta del vivo; tablero de deltas.
- Gimnasio nuevo (canal sim) con dorados extraídos de chats reales.
- **Gate de switch:** sombra ≥ nota del vivo 5 días seguidos Y 0 regresiones en dorados → index.js pasa a llamar al cerebro nuevo (un import; brain.js queda de fallback con flag).
- Primer trasplante: el vivo sigue siendo transporte+panel; el cerebro ya es el nuevo.

### Etapa 3 — Pausa-y-pregunta en vivo + panel completo (mes 2)
- `caminos/dudas.mjs` reemplaza dudas.js: `falta_camino` activo, pausas por conversación, push, crear-camino con conflictos. Se apaga el buzón viejo.
- Acciones al pipeline nuevo por pasos (cotizar → entregar → seguimiento), conservando fechaISO/precioCoherente/ledger y el contrato Supabase byte a byte. El orquestador de integracion.js muere aquí.
- Panel: vistas Cerebro + Entrenamiento + Operación + Números. Checklist de los ~50 endpoints viejos → casa nueva; al completarse, se apaga dashboard.mjs.

### Etapa 4 — Transporte como adapter + segundo canal (meses 2-3)
- La capa Baileys se envuelve en `canales/wa-baileys` (aquí muere index.js: partido en adapter + motor). Outbox único para TODAS las salidas.
- `wa-cloud` en paralelo con número de pruebas/Coexistence vía worker-buzón (cuenta Meta = gestión externa de Alejandro). Presupuesto con tarifas Chile reales y el cambio de oct-2026 provisionado.
- `ig-graph`: app Meta con Standard Access, cuenta administrada propia; identidad cross-canal con captura de teléfono + merge manual.

### Etapa 5 — Producto (mes 3+)
- Promoción del core al maestro (`DIXDY/dixdybot/`), docs/24 v3, destaperapido queda como primera instancia.
- Segundo cliente piloto de otro rubro (prueba de generalidad §11).
- Si se vende a terceros: API key por cliente + decisión VPS.

### Qué vive y qué muere (mapa archivo por archivo)

| Vivo (src/) | Destino | Suerte |
|---|---|---|
| index.js (650 líneas) | canales/wa-baileys/conexion.mjs + motor (pipeline) | **muere partido** (Etapa 4) |
| enviar.js | canales/wa-baileys/enviar.mjs | vive casi igual |
| outbox.js | motor/outbox.mjs (por canal) | vive generalizado |
| gating.js | motor/politica.mjs (config por canal, persistido) | vive |
| quiet.js, portero.js, contacto.js | wa-baileys/ y motor/canon.mjs | viven |
| store.js | motor/estado.mjs (patrón tmp+rename) | vive el patrón |
| brain.js | cerebro/cerebro.mjs (cola única, failover, json-schema) | reescrito conservando getReply |
| extraer.js | cerebro/extractor.mjs (incremental) | el prompt vive; el re-análisis de 200 msgs muere |
| precios.js (492) | data/caminos/*.md `datos:` + validador precioCoherente | tablas migran a datos; el candado vive |
| integracion.js (911) | funciones puras → acciones/; orquestador → pipeline; dudas → caminos/dudas.mjs | **el orquestador muere** (Etapa 3) |
| dudas.js | caminos/dudas.mjs (global, no por-jid) | evoluciona |
| seguimiento.js, recordatorios.js, entregas.js, faltantes.js | acciones/ (todo por outbox; cruce por contacto_id) | viven saneados |
| calidad.js, aprender.mjs, aprender-core.mjs | gimnasio/juez.mjs + caminos/compilador.mjs | evolucionan (parseRules muere) |
| dashboard.mjs (1.897) + web/dashboard.html (191 KB) + entrenar.html | panel/ nuevo sobre la API | **mueren** (Etapa 3) |
| bridge/entrega_bridge.py | acciones/bridge/ (ruta por config; contrato intacto) | vive |
| link-code.mjs, link-qr.js | canales/wa-baileys/ | viven |
| BOT_PERSONA (.env, 10.599 chars) | config/persona.md (~2 KB) + caminos | **muere** (Etapa 2) |
| data/envios.jsonl | data/ledger.jsonl (misma semántica + cobro) | vive renombrado |
| data/aprendizajes.jsonl (68 reglas) | data/caminos/*.md | migra y muere (Etapa 1-2) |

---

## 13. Riesgos principales y contramedidas

1. **La sombra consume cupo Max** (2 generaciones/turno) → muestrear, correr comparaciones en valle, medir con total_cost_usd//usage; si aprieta, sombra en modo api (~US$10-20/mes temporal).
2. **Baileys se degrada durante la migración** (Bad MAC 2.631 casos solo el 22-jul) → Etapa 0 blinda salud+backup; evaluación de 7.0.0-rc13 (mapeos LID) en el gimnasio, nunca directo a producción; wa-cloud en paralelo como salida estructural.
3. **ToS de la vía cli** → postura honesta: conversacional→api como destino (costo conocido y bajo), cli para el trabajo de Alejandro; el failover ya existe desde la Etapa 2, así que un enforcement sorpresivo de Anthropic degrada, no mata.
4. **Migración de identidad** (jid→conv_id) → la proyección guarda `canal_id` original; toda tabla es reversible.
5. **Disciplina de único escritor** (el panel no puede volver a escribir archivos) → los endpoints del motor son la única API; el panel viejo se apaga solo cuando el checklist de paridad esté en cero.
6. **Alejandro no programa** → cada etapa termina en algo que ÉL usa (push de salud, panel comparable, tablero de sombra, buzón de dudas con push); las decisiones que se le piden son solo diseño/plata (Guardián v2).

---

## 14. Fuentes

- Código vivo: `/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/src/` (24 módulos listados en disco), `bridge/entrega_bridge.py`, `web/dashboard.html`, `data/` (jsonl citados). Node v22.18.0; Baileys `^6.7.0`.
- Auditorías e investigación verificada (hallazgos y veredictos): informes hermanos en este mismo directorio (`auditoria-arquitectura-bot`, `conexion-baileys`, `cerebro-entrenamiento`, `auditoria-ux-panel`, `integraciones-tracking`, `canales-whatsapp-2026`, `multicanal-instagram-plataformas`, `caminos-estado-del-arte`, `cerebro-claude-code-vs-api`, `censo-open-source`).
- Doctrina y maestro: `/Users/alejandroriveracarrasco/SaSS/DIXDY/docs/23-doctrina-dixdy.md`, `docs/24-whatsapp-bot-autoresponder.md`, `correo-worker/`, `avisos-worker/`.
- Referencias externas clave: github.com/WhiskeySockets/Baileys · developers.facebook.com/docs/whatsapp/pricing (modelo per-message desde 01-jul-2025; cambio mensajes de servicio 01-oct-2026 vía quali-d.com/chakrahq.com) · developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login · github.com/emcie-co/parlant · arxiv.org/abs/2507.17131 (ARIA) · decagon.ai/blog/from-sops-to-agent-operating-procedures · rasa.com/docs/learn/concepts/calm · arxiv.org/abs/2409.07429 (Agent Workflow Memory) · platform.claude.com/docs/en/agents-and-tools/skills (Agent Skills) · code.claude.com/docs/en/headless · code.claude.com/docs/en/legal-and-compliance · code.claude.com/docs/en/authentication · github.com/kevinrivm/vocero-crm · github.com/codigoencasa/builderbot · github.com/chatwoot/chatwoot · precios API vigentes jul-2026 (referencia claude-api: Opus 4.8 $5/$25, Sonnet 5 $3/$15 intro $2/$10 hasta 2026-08-31, Haiku 4.5 $1/$5, cache reads ~0,1x, Batches −50%).
