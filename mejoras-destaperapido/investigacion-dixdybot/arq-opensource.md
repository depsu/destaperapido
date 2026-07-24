# dixdybot — Arquitectura apoyada en open source

**Ángulo:** máxima reutilización de proyectos vivos de la comunidad, mínimo código propio.
**Fecha:** 2026-07-23. **Base:** auditoría del bot vivo (`/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot`) + investigación verificada adversarialmente (informes en este mismo directorio).

---

## 0. Tesis

La investigación verificó un hecho incómodo y liberador a la vez: **ningún proyecto open source entrega el corazón del pedido** (el bucle "bot detecta que no sabe → pausa ese chat → pregunta al humano → aprende y crea el camino en caliente"). Ni Parlant, ni Chatwoot, ni LangGraph, ni el repo de ARIA lo traen llave en mano. Por lo tanto:

> **Se adopta open source para todo lo que NO es el corazón** (panel, laboratorio de calidad, CI conversacional, transporte de canales, formatos de datos), **y el corazón se construye pequeño**, como datos en archivos + `claude -p` como matcher/compilador, siguiendo modelos de datos ya probados por otros (Parlant, ARIA, Agent Skills, Decagon).

Eso cumple la doctrina DIXDY (no reinventar lo que ya existe: ni lo de la comunidad ni lo propio — launchd, avisos-worker, cola única, Supabase, envios.jsonl) y deja el diferencial comercial de dixdybot donde nadie lo vende.

---

## 1. Mapa de decisiones open source (la tabla honesta)

### 1.1 ADOPTAR como código (se instala o se forkea)

| Proyecto | Licencia / estado verificado | Rol en dixdybot |
|---|---|---|
| **Baileys** (WhiskeySockets) | MIT, 10.233★, push diario, en RC 7.0.0-rc13 desde sep-2025 | **Se queda** como transporte WhatsApp. Ya está en producción con sanación Bad MAC propia que la comunidad no tiene. Evaluar upgrade a rc13 (mapeos LID = causa raíz del Bad MAC) SOLO en sandbox con número secundario, nunca en caliente. |
| **wacrm** (ArnasDon) | MIT, 1.680★, 594 commits, push 21-jul-2026, "template, not a product" | **Base del panel nuevo.** Next.js 16 + Supabase (el stack exacto que Alejandro ya prefiere y el Supabase que ya paga), Kanban de deals ligado a conversaciones, tokens cifrados, y un **servidor MCP** para que Claude opere el CRM — o sea, la IA administra el panel del cliente sin UI, gratis. Se forkea y se le agregan las vistas propias (Caminos, Dudas, Config). |
| **vocero-crm** (kevinrivm) | MIT, 79★, 26 commits, en español, push jul-2026 | **El gimnasio soñado, ya escrito.** "Laboratorio de auto-evaluación": 6 clientes simulados (el decidido, el preguntón, el enojado…) contra el cerebro REAL en sandbox que jamás envía mensajes, juez LLM independiente con score 0-100, hallazgos con evidencia y delta histórico tras cada cambio. Legible entero en una tarde; se copia el patrón y buena parte del código. |
| **DeepEval** (confident-ai) | Apache-2.0, 17.061★, push 22-jul-2026 | **CI conversacional.** `ConversationSimulator` acepta un `model_callback` — se envuelve el cerebro `claude -p` ahí — y trae métricas multi-turno listas (`KnowledgeRetentionMetric`, `RoleAdherenceMetric`). Corre los escenarios dorados tras CADA cambio de camino o tarifario, antes de activar. Es Python: DIXDY ya vive de scripts Python. |
| **BuilderBot** (codigoencasa) | MIT, 2.960★, comunidad hispana, push 21-jul-2026 | **No se adopta el framework** (su motor de flujos por keywords no es nuestro cerebro), pero su monorepo `packages/` tiene `provider-baileys`, `provider-meta`, `provider-instagram` (vía Meta oficial), `provider-twilio`… — se **copia el contrato Provider** como interfaz de adapter, y cuando llegue la etapa Cloud API se cribbea su `provider-meta` (webhook, media, plantillas) en vez de escribirlo de cero. |

### 1.2 COPIAR el modelo/patrón, NO el motor

| Fuente | Qué se copia | Por qué no se adopta el motor |
|---|---|---|
| **Parlant** (emcie-co, Apache-2.0, 18.180★, v3.3.2) | El **esquema de los caminos**: guidelines condición→acción, journeys multi-turno, relaciones `depende_de`/`excluye`/`implica`, canned responses para cifras, y la carga en el prompt de SOLO lo relevante al turno (attention dilution: hasta 85% de caída de precisión con prompts saturados, verificado en sus docs). | Es un servidor Python que asume LLM por API; usarlo con `claude -p` exige escribir un `NLPService` custom = doble infraestructura. Su valor está en el modelo de datos, que es libre de copiar (Apache-2.0). |
| **Agent Skills** (estándar abierto de Anthropic) | El **formato de archivo** de cada camino: carpeta con `CAMINO.md` = frontmatter YAML + cuerpo markdown, divulgación progresiva (títulos de ~30-50 tokens al inicio, cuerpo solo al activarse). Es **nativo del stack `claude -p`** que ya usamos: resuelve gratis la "carga selectiva de 3-5 caminos por turno". | No hay motor que adoptar: es un formato. |
| **ARIA** (arXiv:2507.17131, en producción en TikTok Pay, 150M+ MAU) | El **bucle de adquisición**: detectar gap → preguntar al experto → repositorio timestampeado → resolver conflictos por comparación entre reglas. | El repo público (github.com/yf-he/aria) es un volcado de 1 commit, no un runtime mantenido. |
| **AWM — Agent Workflow Memory** (ICML 2025, arXiv:2409.07429) | La técnica de **arranque en frío**: inducir workflows desde trayectorias pasadas (+24,6% / +51,1% éxito relativo en Mind2Web/WebArena). Aplicado: minar `conversaciones.jsonl` + `envios.jsonl` + las 68 reglas + BOT_PERSONA con `claude -p` para proponer los primeros 25-35 caminos que Alejandro aprueba en lote. | Es un paper con código de investigación; la minería aquí es un prompt bien hecho. |
| **LangGraph** (MIT) | El patrón `interrupt()` + `Command(resume)` + **checkpointer persistente**: el estado pausado vive en disco y sobrevive reinicios. Se replica con `control.json` + `dudas.jsonl` que ya existen. | Adoptar la librería = nueva runtime de grafos para algo que outbox+jsonl ya hacen (doctrina DIXDY). |
| **Rasa CALM** (Rasa Pro, licencia comercial) | Los **conversation patterns transversales** implementados UNA vez a nivel sistema, no por camino: corrección de datos a mitad de flujo, digresión y vuelta, clarificación entre dos caminos candidatos. | El código es propietario; la arquitectura está documentada públicamente. |
| **Decagon AOPs** (comercial, 70-80% deflexión) | **Versionado con rollback instantáneo**: como los caminos son archivos markdown/YAML, `git` regala historial, diff y revert. Cada cambio de camino = commit. | Es un SaaS cerrado. |
| **OpenClaw** (383.851★, licencia NOASSERTION) | El **plano** "un cerebro, N canales, gateway como plano de control, daemon en Mac local". | Es asistente personal (no bot de negocio), sin Instagram, sobre API keys, licencia no estándar. "Se roba el plano, no el edificio". |
| **Evolution API** (Apache-2.0 con cláusulas extra de marca) | La **idea del transporte dual**: Baileys y Cloud API oficial tras la misma interfaz interna. | Cláusulas de licencia incómodas, arrastra su propia DB, Instagram lleva años en "coming soon", y seguiríamos manteniendo nuestros parches Baileys igual. |
| **EIP** (Hohpe & Woolf) | Los nombres y contratos: **Channel Adapter → Canonical Data Model → bus → transactional outbox por canal**. El bot actual ya tiene el embrión (outbox.js + envios.jsonl + gating.js + brain.js desacoplado — verificado en disco). | Es un catálogo de patrones, no software. |

### 1.3 NO adoptar (y por qué, con veredictos verificados)

- **Chatwoot** (34.667★, open-core): la mejor bandeja omnicanal viva, pero Rails+Postgres+Redis para un negocio de 1 operador es un elefante, su agente "Captain" es parcialmente enterprise (verificado: vive bajo `enterprise/app/services/captain`), y el canal Instagram "llave en mano" es del Cloud de ellos — self-hosted igual exige crear TU app de Meta. **Queda en el mapa de ruta**: si dixdybot escala a 5+ clientes con atención humana, dixdybot se enchufa como **Agent Bot** (webhook + REST) sin tirar nada de lo construido.
- **Typebot**: FSL-1.1 y cobra la integración WhatsApp incluso self-hosted. **Botpress**: v12 legacy, el producto real es Cloud cerrado. **n8n**: SUL permite uso interno pero es infra nueva que no aporta nada que launchd + scripts no hagan ya.
- **whatsapp-web.js / WPPConnect / WAHA**: mismo protocolo reverse-engineered, mismos bans (whatsapp-web.js #3250: cuentas bloqueadas con 7 msg/hora), sin nuestra sanación Bad MAC. Cambiar de librería no oficial = mismo riesgo, cero ganancia.
- **mautrix-meta (AGPL, 406★) / instagrapi para Instagram**: violan ToS de Meta; con cuentas de clientes es inaceptable (las cifras de "15-30% de suspensión" resultaron humo de marketing, pero el riesgo de checkpoint/bloqueo es real y documentado). **Instagram va SOLO por la API oficial.**
- **Claude Code Channels + crisandrews/claude-whatsapp** (MIT, sobre Baileys): el carril oficial existe desde mar-2026 (v2.1.80+, Telegram/Discord/iMessage) y hay canal WhatsApp comunitario — pero es research preview, exige `--dangerously-load-development-channels`, el plugin tiene 8★, y las tools reales son 52 (reply, react, download_attachment; "unreplied"/"catch_up" NO existen). **Se vigila como futuro carril oficial; no se apuesta producción de ventas ahí.** Su contrato MCP de canal sí sirve de referencia para nuestro adapter.
- **HumanLayer**: deprecado por sus propios autores; solo se hereda el patrón "contact-human-as-tool".
- **Repos sin licencia** (RichardAtCT/claude-code-telegram 2.736★, claudeclaw, gokapso/claude-code-whatsapp): ideas sí, código no.

---

## 2. Arquitectura general

```
                      ┌────────────────────────────────────────────────┐
                      │                PANEL (fork de wacrm)           │
                      │  Next.js+Supabase · vistas: Kanban / Ficha /   │
                      │  Caminos / Dudas / Conocimiento / Entrenar /   │
                      │  Config / Embudo $ · + servidor MCP del CRM    │
                      └───────────────▲────────────────▲───────────────┘
                                      │ API local :8790│ Supabase (entregas, deals)
┌──────────────┐   mensaje canónico   │                │
│ CANALES      │  ┌────────────────┐  │   ┌────────────┴───────────┐
│ wa-baileys ──┼─▶│ NÚCLEO (turno) │──┼──▶│ INTEGRACIONES (la joya)│
│ wa-cloud ────┼─▶│ gating·portero │  │   │ pipeline: extraer →    │
│ instagram ───┼─▶│ store·identidad│  │   │ validar → cotizar/PDF/ │
└──────▲───────┘  └───────┬────────┘  │   │ correo → entrega →     │
       │                  │           │   │ Supabase → repartidor  │
       │ outbox por canal │ CEREBRO   │   └───────────┬────────────┘
       │ (transactional)  ▼           │               │ envios.jsonl (libro mayor)
┌──────┴─────────┐ ┌──────────────────┴─┐             ▼
│ cerebro/claude │ │ CAMINOS (archivos) │      ┌──────────────┐
│ .mjs — UN solo │ │ caminos/<slug>/    │      │ CALIDAD      │
│ spawn claude -p│ │ CAMINO.md (YAML+md)│      │ lab vocero + │
│ cola+timeout+  │ │ selector por turno │      │ DeepEval CI +│
│ failover API   │ │ pausa-y-pregunta   │      │ juez actual  │
└────────────────┘ └────────────────────┘      └──────────────┘
     launchd (com.dixdy.*) · avisos-worker (push) · actividad.py · git (versionado caminos)
```

Todo sigue siendo **procesos locales en el Mac comunicados por archivos en `data/`** (es el bus que ya existe y funciona; doctrina DIXDY). Lo que cambia: un solo wrapper de cerebro, caminos como archivos versionados, adapters con contrato, y el panel deja de re-implementar lógica para **consumir una API del núcleo**.

---

## 3. Capa de canales

### 3.1 Contrato de adapter (copiado de BuilderBot Provider, ~80 líneas propias)

```js
// canales/adapter.d.ts (contrato)
interface CanalAdapter {
  nombre: 'wa' | 'wa-cloud' | 'ig';
  on(evento: 'mensaje', cb: (m: MensajeCanonico) => void): void;
  enviar(conv_id: string, salida: SalidaCanonica): Promise<{ok: boolean, id_externo?: string}>;
  salud(): { conectado: boolean, detalle?: string };   // para heartbeat
}
```

**Mensaje canónico** (Canonical Data Model — la clave deja de ser el jid):

```jsonc
{ "id": "wa:3EB0...",                  // id externo prefijado por canal
  "conv_id": "wa:56912345678@s.whatsapp.net",
  "canal": "wa",                        // wa | wa-cloud | ig
  "dir": "in",                          // in | out
  "tipo": "texto",                      // texto|imagen|pdf|audio|ubicacion
  "texto": "hola, precio baño químico?",
  "media": null, "ts": 1753238000,
  "meta": { "pushName": "Juan", "jid": "..." } }     // lo específico del canal va aquí
```

**Identidad** (`data/identidades.json`, generaliza `enlaces.json`): `{ persona_id, telefono?, ig_username?, conv_ids: [], nombre? }`. El teléfono sigue siendo el cruce chat↔entrega en WhatsApp; en Instagram (sin teléfono) el cruce va por `persona_id` + enlaces manuales/automáticos — exactamente el hueco que la auditoría de integraciones ya señaló.

### 3.2 WhatsApp hoy: Baileys endurecido (sobrevive)

`index.js` (650 líneas) se parte en dos: `canales/wa-baileys.mjs` (socket, reconexión con backoff, sanación Bad MAC, stub CIPHERTEXT, salto del eco fromMe — los fixes del 21/22-jul **hoy sin commitear**) y `nucleo/turno.mjs` (el closure de ~145 líneas del turno de respuesta, ahora agnóstico de canal). `enviar.js`, `outbox.js`, `quiet.js` sobreviven casi tal cual dentro del adapter.

### 3.3 WhatsApp mañana: Cloud API oficial (Plan B ya presupuestado)

Adapter `canales/wa-cloud/` como **webhook en un Worker de Cloudflare** (infra que DIXDY ya opera: avisos-worker, ga4-worker, correo-worker) que encola el mensaje canónico; el Mac lo drena (polling barato o Tailscale). Código base: `provider-meta` de BuilderBot (MIT). Datos verificados que mandan aquí:

- Tarifas **Chile tiene fila propia** (no "Rest of LatAm"): utility/auth **US$0,02 (~CLP 19)**, marketing **US$0,0889 (~CLP 83)**. El costo mensual estimado sigue < CLP 10.000 al volumen actual.
- Respuestas dentro de la ventana de 24h **gratis hoy, PERO solo hasta el 30-sep-2026**: desde el 1-oct-2026 los mensajes de servicio se cobran a tarifa utility (salvo ventanas de 72h por click-to-WhatsApp). Recalcular en septiembre con las tarifas que Meta publique.
- **Coexistence** (global desde may-2025): el mismo número puede vivir en la app WhatsApp Business y en la API — es la rampa de salida de Baileys sin cambiar de número. Límite: sincroniza solo 6 meses de chats, sin grupos.
- "Cero ban" es falso en sentido estricto: hay enforcement escalonado con avisos y apelación — pero no el ban arbitrario de las librerías no oficiales.

Primer uso real (bajo riesgo): **avisos utility al repartidor** y estados de entrega por webhook, mientras Baileys sigue llevando la venta. Conmutación gradual por conversación.

### 3.4 Instagram: solo la vía oficial

Adapter `canales/instagram/` contra la **Instagram API with Instagram Login** (desde jul-2024 no exige Página de Facebook): cuenta profesional + `instagram_business_basic` + `instagram_business_manage_messages` + webhooks. Con **Standard Access basta** si la cuenta tiene ROL en la app de Meta de DIXDY (App Review + Business Verification solo si dixdybot se vende a terceros — y la verificación real tarda 3-14 días hábiles, a veces más). Reglas duras: el bot SOLO responde, ventana de 24h, y **jamás usar HUMAN_AGENT desde el bot** (Meta lo audita y lo revoca). El mismo webhook-Worker del punto 3.3 recibe ambos canales de Meta.

---

## 4. Cerebro: Claude Code con fallback (y la letra chica honesta)

### 4.1 `cerebro/claude.mjs` — UN solo wrapper (mata 4 implementaciones divergentes)

Hoy hay 4 spawns distintos de `claude -p` (brain.js 120s, extraer.js 90s sin `--model`, calidad.js 150s, aprender-core.mjs SIN timeout) sin cola compartida. El wrapper único:

- **Cola con concurrencia 2** (semáforo nativo, sin dependencia) y timeout por clase de tarea (`responder: 120s, extraer: 90s, juez: 150s, compilar-camino: 300s`).
- `--output-format stream-json` y manejo de `system/api_retry` con categorías tipadas (`rate_limit, overloaded, billing_error, oauth_org_not_allowed`) **más** exit-code+stderr (un "Login expired" no llega por api_retry).
- **Failover en cascada**: (1) `claude -p` con suscripción Max (CLAUDE_CODE_OAUTH_TOKEN de `claude setup-token`, dura 1 año — el `/login` normal caduca y mata sesiones desatendidas); (2) si límite/caída → mismo binario con `ANTHROPIC_API_KEY` (en modo `-p` la key siempre gana si está presente — documentado); (3) si todo cae → respuesta enlatada honesta ("déjame confirmarlo y te escribo en unos minutos") + pausa del chat + push por avisos-worker.
- **Blindaje contra el futuro** (verificado en doc oficial): `--bare` será el default de `-p` y NO lee OAuth (exigiría API key) → fijar `autoUpdatesChannel: stable` + `minimumVersion`, jamás pasar `--bare`, y test de humo diario del wrapper.
- Log de costo/uso por invocación (`total_cost_usd` viene en el JSON de salida).

### 4.2 Honestidad sobre términos y costos

- La página legal de Claude Code dice que los límites Pro/Max asumen "uso ordinario e individual" y que quien construye productos/servicios (incl. Agent SDK — y la doc hoy enmarca `claude -p` como "the Agent SDK via the CLI") **debería usar API key**; enforcement posible sin aviso. Un bot 24/7 del propio dueño es **zona gris tolerada hoy** (no hay casos documentados de baneo del CLI oficial a bajo volumen; los lockouts de ene-2026 fueron contra herramientas de terceros), no un derecho.
- Plan económico: hoy Max = costo marginal $0 (pero consume el cupo compartido con el uso interactivo de Alejandro). El fallback API con **Haiku 4.5 delgado + caching ≈ US$27-40/mes** a 300 invocaciones/día; Sonnet ≈ US$80-120/mes. **Si dixdybot se vende a terceros: API key por cliente, obligatorio por la doc.** La arquitectura del wrapper hace que esa migración sea cambiar una variable de entorno, no un rediseño.

---

## 5. Caminos — el corazón (lo único que se construye de verdad)

### 5.1 Formato: Agent Skills + esquema Parlant, versionado con git

Cada camino es una carpeta `caminos/<slug>/CAMINO.md`:

```markdown
---
id: cotizar-bano-quimico-mensual
condicion: "cliente pide precio de baño químico para obra/evento por un mes o más"
ambito: { canales: [todos], servicios: [bano-quimico] }
usa_datos: [tarifario.banos.mensual, tarifario.recargo_lejanas]   # cifras: NUNCA redactadas por el modelo
relaciones: { depende_de: [detectar-comuna], excluye: [cotizar-evento-corto] }
prioridad: 50
status: activo            # activo | off | retirado
vigencia: { desde: 2026-07-25, hasta: null }
origen: { tipo: duda, chat: "wa:5691...", fecha: 2026-07-25 }   # duda | mineria | manual
---
Si el cliente pide baño químico por un mes o más:
1. Confirma comuna ANTES de dar precio (si falta, ejecuta el camino detectar-comuna).
2. Cotiza SIEMPRE valor mensual (el plazo elige la tarifa, no multiplica).
3. El valor sale de usa_datos; tú redactas alrededor de la cifra, nunca la inventas.
Si pide factura: los valores del tarifario son NETOS, suma IVA y dilo explícito.
```

- **Cifras y tarifario** siguen en `precios.js` (patrón probado "números en código, el modelo redacta" — la mejora medible del bot vino de ahí, no del loop de reglas). Los caminos referencian datos por clave (`usa_datos`), estilo canned responses de Parlant.
- **Git = versionado Decagon**: cada alta/edición/retiro es un commit; rollback = revert; el historial que hoy no existe (status on/off sin historia) sale gratis.
- **Métricas** en archivo aparte `caminos/metricas.json` (para no ensuciar diffs): `{ id: {usos, cotizaciones, cierres, ultima_vez} }`.

### 5.2 Selección por turno (anti-dilución)

Dos etapas, como Parlant/Agent Skills: (1) **filtro duro en código** por `status/vigencia/ambito` (canal, servicio detectado, etapa del embudo); (2) **matcher barato**: el índice de títulos+condiciones (~30-50 tokens por camino) se pasa a `claude -p --model haiku` que devuelve los 3-5 relevantes; solo esos cuerpos entran al prompt del turno. Muere el prompt de 27-30 KB con 68 reglas planas para todos los chats; nace: persona corta (~2 KB) + caminos del turno + datos duros + contexto. La resolución de conflictos residual es determinista: `prioridad` + `relaciones.excluye`.

### 5.3 Pausa-y-pregunta en caliente (generalización de `dudas.js`)

`dudas.js` (180 líneas) ya hace el 80%: pausa la acción, pregunta con opciones ejecutables (`accion:{endpoint,body}`), guarda `respuestaPrevia` y no repregunta. Lo que se generaliza:

1. **El cerebro también dispara dudas**, no solo el motor de integración: se le da la herramienta de output `[[DUDA: pregunta | opcion A | opcion B]]` para cuando detecta hueco de conocimiento (hoy dice "el equipo confirma el valor" y la venta se enfría).
2. Al dispararse: el chat entra a `pausado_por_conocimiento` en `control.json` (persistente, sobrevive reinicios — patrón checkpointer de LangGraph sin LangGraph), el cliente recibe el fallback honesto **("dame unos minutos y te confirmo")** — obligatorio en rubro de urgencia —, y Alejandro recibe **push por avisos-worker** (`python3 scripts/avisar.py`, ya existe, hoy el bot no lo usa).
3. Alejandro responde desde el panel (o con texto libre). La respuesta va a `cerebro/compilar-camino`: `claude -p` la destila a un `CAMINO.md` candidato.
4. **Chequeo de conflictos (patrón ARIA)**: antes de guardar, `claude -p` compara el candidato contra los caminos de ámbito solapado → `{compatible | contradice: [ids] | duplica: [ids]}`. Si contradice, el panel muestra el diff y Alejandro elige; el perdedor queda `retirado` con timestamp (así no se repite el caso IVA: 3 vueltas en 4 días con la persona del .env aún contradiciendo a 7 reglas activas).
5. Regresión antes de activar: los escenarios dorados corren con DeepEval/laboratorio (ver §7). Si pasan → `status: activo`, commit, el chat se despausa y responde. **Timeout**: si Alejandro no contesta en N minutos, el chat queda en manual y el push se re-escala.
6. **Global por defecto, excepción por chat**: la respuesta crea camino global salvo que se marque "solo este chat" (hoy `respuestaPrevia` es por-jid y el conocimiento nunca se generaliza — ese es el bug conceptual que se corrige).
7. El destilador corrupto se blinda: `compilar-camino` valida contra JSON-schema del frontmatter; nada de `parseRules` que convierte "```" en regla activa (pasó en producción, se apagó a mano el 21-jul).

### 5.4 Edición conversacional y arranque en frío

- **Edición conversacional**: el panel tiene el chat "Entrenador" (o directamente Claude Code vía el **MCP del wacrm**): "los fines de semana largos el retiro es el martes" → mismo pipeline compilar→conflictos→regresión→commit. Alejandro nunca edita YAML.
- **Arranque en frío (AWM)**: un job en la **cola única de DIXDY** (`tareas.json`, no un cron nuevo) mina `conversaciones.jsonl` (59 chats con bot), `envios.jsonl` (30 eventos), las 68 reglas activas, BOT_PERSONA y ANALISIS-CEREBRO.md → propone 25-35 caminos con evidencia (qué chats lo justifican). Alejandro aprueba en lote desde el panel. Las 68 reglas se clasifican: fusionada-en-camino / dato-al-tarifario / retirada. La persona de 10.406 chars queda en ~2 KB de identidad y tono.

---

## 6. Panel: fork de wacrm (MIT) sobre el Supabase existente

`dashboard.mjs` (1.897 líneas, ~50 endpoints) + `web/dashboard.html` (191 KB) **mueren** — la auditoría fue explícita: re-implementan la extracción del bot en vez de consumirla (comuna distinta bot vs panel, 3 regex de precio). El reemplazo:

- **Núcleo expone API local** (`:8790`, ~15 endpoints): conversaciones, ficha (LA extracción del bot, única), caminos CRUD+conflictos, dudas, control (pausas, interruptor global), config, métricas. Poca lógica: lee los mismos `data/*.jsonl` con los mismos módulos del bot.
- **Panel = wacrm forkeado** (Next.js+Supabase+Tailwind — el stack que el CLAUDE.md global de Alejandro ya exige; pnpm) con vistas:
  1. **Hoy / Kanban** — las 4 columnas actuales (Cotizando→Por confirmar→Por entregar→Cobrado) + badge 🔶 "pausado: falta conocimiento" + sección Dormidos. Una sola taxonomía de etapas (muere la dualidad STAGES/LIFE).
  2. **Dudas** — buzón global con opciones ejecutables (patrón conservado: la acción corre antes de marcar resuelta).
  3. **Caminos** — lista con métricas (usos/cotizaciones/cierres), editor de texto (¡hoy no se puede editar una regla!), on/off, historial git, botón "probar en sandbox", lista de gaps (dudas sin camino resultante).
  4. **Conocimiento** — persona corta editable + tarifario VISIBLE y editable (hoy: invisible en `precios.js`; guardar = regresión automática antes de aplicar).
  5. **Entrenar** — el laboratorio (§7), unificado con el resto (muere el `prompt()` nativo y la pseudo-pestaña).
  6. **Config** — gating anti-ban (topes 40/h, 200/día, horario), repartidor, canales conectados y su salud, interruptor global del bot, vista global de pausas (hoy inexistente).
  7. **Embudo $** — pactado vs cobrado por entrega (evento `cobro`, §8).
- Config editada → `data/config.json`; el bot la relee por turno (recarga en caliente sin reinicio).
- El **servidor MCP de wacrm** queda para que Claude Code opere el CRM por texto — administración conversacional gratis.
- Acceso iPhone: mismo Tailscale de hoy.

---

## 7. Entrenamiento y calidad

- **Laboratorio (copiado de vocero-crm, MIT)**: 6 clientes simulados tipificados del rubro (apurado con emergencia, preguntón de precios, el que regatea, el confundido de comuna, el de factura, el enojado) contra el cerebro real en sandbox; juez independiente (el `calidad.js` actual, 344 líneas, sobrevive) con score y hallazgos con evidencia; **delta histórico tras cada cambio** de camino/tarifario — la métrica que ya mostró 2,44→2,65→4,0 se vuelve sistemática.
- **CI conversacional (DeepEval, Apache-2.0)**: `calidad/escenarios/*.yml` (los dorados: cotización estándar, IVA/factura, comuna lejana, fecha rara, retiro, reagenda) corren vía `ConversationSimulator` con `model_callback` = wrapper del cerebro, métricas `KnowledgeRetention`/`RoleAdherence` + asserts propios (el precio emitido ∈ tarifario — reutiliza `precioCoherente`). **Gate obligatorio antes de activar cualquier camino** — la pieza que la auditoría marcó como inexistente ("al activar una regla nada verifica que no rompa lo de ayer").
- **Una sola entrada de feedback**: las 5 entradas actuales convergen en un endpoint que produce **propuestas de camino** (no reglas planas), con el pipeline de §5.3. El replay 🎬 y los 👍👎 sobreviven.

---

## 8. Tracking punta a punta (la joya se conserva entera)

- **Sobreviven tal cual**: `envios.jsonl` (libro mayor append-only, dedup `yaCotizado` 45d / `yaDespachado` ∞, escritura apenas sale lo irreversible), el contrato Supabase de 2 tablas (`entrega` con card_html renderizado en Python + `entrega_estado` del repartidor que vuelve al Kanban y al prompt), `bridge/entrega_bridge.py` (upsert idempotente; se le quita la ruta absoluta hardcodeada → `.env`), la costura `prepararEntrega` construye-pero-no-envía (el llamador elige canal — ya es multi-canal de nacimiento), outbox con goteo anti-ban e idempotencia del PDF.
- **Se parte**: `integracion.js` (911 líneas) → pipeline de pasos explícitos (`extraer → validar → decidir → ejecutar → registrar`), conservando **intactas** sus funciones puras: `fechaISO`/`fechaFinISO` (líneas 105-201, único juez de fechas en español), `precioCoherente` (277-294, candado anti-invento), `construirConfigCotizacion`, `construirEntrega`. Deuda que muere: `seguimiento.js` deja de enviar directo y pasa por outbox.
- **Nuevo — evento `cobro`**: hoy el cobro es solo un estado en Supabase y el embudo económico no se registra en ninguna parte. Un paso del bridge (o el poller existente) escribe `cobros.jsonl`: `{entrega_id, monto_pactado, monto_cobrado, fecha, caminos:[ids]}`.
- **Métricas por camino**: cada turno registra `caminos_usados` en la meta del mensaje; `integracion` los copia al evento de `envios.jsonl`; un paso del launchd de aprendizaje (ya existe: `com.dixdy.whatsapp-aprender`) agrega a `caminos/metricas.json`. Embudo por camino: usos → cotizaciones → cierres → cobrado.

---

## 9. Despliegue: Mac mini vs VPS, y el watchdog que falta

| | **Mac mini (recomendado hoy)** | **VPS Linux** |
|---|---|---|
| Ecosistema DIXDY | Ya montado: 17 plists launchd, scripts, avisos-worker, Tailscale, perfiles Chrome, cola única | Habría que reconstruirlo (systemd, credenciales, bridges) = reinventar infra, anti-doctrina |
| Claude Code | Max ya pagada, Keychain cifrado, `setup-token` 1 año | Primera clase (Ubuntu 20.04+, 4 GB, repos firmados) pero credenciales en JSON 0600 y cupo Max compartido igual |
| Riesgos | Corte de luz/internet del local; se mitiga con UPS + heartbeat | Uptime superior; pero la sesión Baileys y el humano (Alejandro) siguen en Chile igual |
| Costo | $0 marginal | ~US$10-20/mes + horas de migración |

**Decisión**: Mac mini ahora; todo config-driven para que un VPS sea posible cuando dixdybot sea multi-cliente (momento en que además tocará API key por cliente y quizá Chatwoot). **Watchdog externo (brecha #1, entregable en días)**: el bot hace POST de heartbeat cada 5 min al **avisos-worker existente** (Cloudflare); un cron del worker avisa al celular si hay silencio >15 min o si el último estado fue `401 loggedOut` — hoy un 401 deja el proceso vivo pero ciego para siempre y NADIE se entera. Fallback de cerebro: cascada del §4.1.

---

## 10. Plan de migración (el bot vende hoy; nada lo apaga)

Cada etapa deja el sistema funcionando; el flip de cada pieza tiene rollback (git / variable de entorno / plist).

- **Etapa 0 — "Asegurar la caja" (1-2 días, entregable YA):**
  1. **Commitear lo que está suelto** (verificado hoy: `src/index.js`, `src/quiet.js`, `src/dashboard.mjs`, `web/*.html` modificados y `src/recordatorios.js` NUNCA commiteado — los fixes anti-408/eco-fromMe del 21/22-jul viven solo en disco).
  2. Fijar Baileys **exacto** 6.7.23 en package.json (hoy `^6.7.0`; jamás saltar a 7.0.0-rc13 sin sandbox).
  3. Backup atómico de `auth/` (tar horario con rotación; 4 corrupciones de sesión en julio lo justifican).
  4. **Heartbeat → avisos-worker** + alerta 401/silencio (§9).
  5. Rotación de logs (53 MB en 5 días en la era mala; `bot.error.log` sin rotación).
  6. Persistir el tope `MAX_BOT_REPLIES_PER_CHAT` en `control.json` (hoy en RAM, se resetea con cada KeepAlive) y actualizar MANUAL.md a los valores reales (30s/12, no 60s/3-4).
- **Etapa 1 — Cerebro único (≈1 semana):** `cerebro/claude.mjs` (cola, timeouts, failover, `setup-token`, pin de canal/versión, log de costo); brain.js/extraer.js/calidad.js/aprender-core lo consumen. Escritura atómica tmp+rename (de `store.js`) para los 5 archivos que hoy usan `writeFileSync` directo (outbox, seguimientos, recordatorios, enlaces, pedidos). **Cero cambio de comportamiento visible.**
- **Etapa 2 — Caminos v1, solo lectura (≈1-2 semanas):** minería AWM por la cola única → 25-35 caminos propuestos con evidencia → aprobación en lote → prompt nuevo (persona 2 KB + selector + datos duros). Validación **en sombra**: laboratorio vocero + DeepEval sobre los dorados comparando prompt viejo vs nuevo; flip por variable `CAMINOS=1` con rollback instantáneo. Resuelve de paso el conflicto IVA vivo.
- **Etapa 3 — Pausa-y-pregunta (≈1 semana):** generalizar `dudas.js` (§5.3): duda de conocimiento del cerebro, push avisos-worker, compilar-camino + conflictos ARIA + regresión + commit, timeout honesto. **Aquí nace el dixdybot que Alejandro pidió.**
- **Etapa 4 — Panel nuevo (2-3 semanas, en paralelo):** API local del núcleo; fork de wacrm con las vistas 3/2/4/6 primero (Caminos, Dudas, Conocimiento, Config — lo que HOY no existe); el dashboard viejo sigue sirviendo Kanban/ficha hasta que sus vistas nuevas lo superen (coexisten leyendo los mismos data/, como hoy). `dashboard.mjs` muere al final, no al principio.
- **Etapa 5 — Cloud API en paralelo (este trimestre):** cuenta Meta + Coexistence; webhook-Worker Cloudflare; primero avisos utility al repartidor (~CLP 19) y estados por webhook; la venta sigue en Baileys. Recalcular costos en septiembre (cambio del 1-oct-2026).
- **Etapa 6 — Instagram (cuando Alejandro lo pida):** app Meta de DIXDY, Standard Access, adapter `ig` sobre el mismo Worker; identidad por `persona_id` sin teléfono. El núcleo no cambia: eso es lo que compró la Etapa 2-4.
- **Etapa 7 — Producto:** promoción del template `dixdybot/` al maestro (hoy la divergencia template↔vivo es 12 archivos/1.912 líneas vs 24/7.119 — la regla DIXDY incumplida a escala); config por cliente; API key por cliente para terceros; Chatwoot como bandeja si hay 5+ clientes con humanos.

---

## 11. Qué sobrevive y qué muere (archivo por archivo)

**Sobreviven casi tal cual** (con líneas de hoy): `enviar.js` (167 — sanación Bad MAC + watchdog ✓✓), `outbox.js` (115 — transactional outbox), `gating.js` (225 — jid→conv_id), `portero.js` (40), `contacto.js` (173), `store.js` (532 — su patrón atómico se propaga), `precios.js` (492 — capa de datos duros), `dudas.js` (180 — generalizado a conocimiento), `calidad.js` (344 — juez del laboratorio), `aprender-core.mjs` (126 — renace como compilar-camino con schema estricto), `quiet.js` (28), `extraer.js` (130 — su prompt sobrevive; su spawn pasa al wrapper), `bridge/entrega_bridge.py` (ruta absoluta → .env), `entregas.js` (65), `recordatorios.js` (151 — commitearlo primero), `seguimiento.js` (141 — su envío directo pasa por outbox), `envios.jsonl` y el contrato Supabase completos.

**Se parten**: `index.js` (650) → adapter wa-baileys + orquestador de turno; `integracion.js` (911) → pipeline de pasos, con `fechaISO` (105-201), `precioCoherente` (277-294), `construirConfigCotizacion`, `construirEntrega` intactas.

**Mueren**: `dashboard.mjs` (1.897) y `web/dashboard.html` (191 KB) → panel wacrm + API del núcleo; `BOT_PERSONA` de 10.406 chars en una línea del .env → persona corta en archivo + caminos; las 68 reglas planas de `aprendizajes.jsonl` → caminos con ámbito (migradas por la minería); la detección de comuna duplicada (`precios.js:88` vs `dashboard.mjs:314`) y las 3 regex de precio → un solo `nucleo/dominio.mjs`.

---

## 12. Riesgos que quedan (sin maquillaje)

1. **Ban de Baileys**: impredecible (issue #1869: 5 bots en una semana, dos con 3+ años). Mitigado (solo-responde, gating, Etapa 0) pero nunca cero; el seguro es la Etapa 5 lista para conmutar.
2. **ToS de Anthropic**: la zona gris del bot en Max puede cerrarse sin aviso; el wrapper hace del failover a API un switch, y el costo está presupuestado (US$27-40/mes Haiku).
3. **Meta 1-oct-2026**: los mensajes de servicio dejan de ser gratis; recalcular antes de conmutar la venta a Cloud API.
4. **wacrm es template, no producto**: adaptarlo es trabajo real (semanas, no días) — por eso el dashboard viejo no muere hasta la Etapa 4 tardía.
5. **El matcher de caminos agrega una llamada por turno**: latencia +1-3 s con Haiku; se mide en el laboratorio y, si duele, el índice cabe en el prompt principal (estilo Agent Skills puro).
6. **Instagram para terceros** exige App Review + Business Verification de duración incierta (3-14 días hábiles o más): empezar el papeleo de la app de Meta en la Etapa 5, no en la 6.

---

## Fuentes principales

Código vivo: `/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/src/` (conteos y git status verificados hoy). Informes hermanos en este directorio: `auditoria-arquitectura-bot.md`, `conexion-baileys.md`, `cerebro-entrenamiento.md`, `auditoria-ux-panel.md`, `integraciones-tracking.md`, `canales-whatsapp-2026.md`, `multicanal-instagram-plataformas.md`, `caminos-estado-del-arte.md`, `cerebro-claude-code-vs-api.md`, `censo-open-source.md`. Repos: github.com/emcie-co/parlant · github.com/kevinrivm/vocero-crm · github.com/ArnasDon/wacrm · github.com/confident-ai/deepeval · github.com/WhiskeySockets/Baileys · github.com/codigoencasa/builderbot · github.com/chatwoot/chatwoot · github.com/openclaw/openclaw · github.com/crisandrews/claude-whatsapp. Docs: code.claude.com/docs/en/{headless,authentication,legal-and-compliance} · developers.facebook.com/docs/whatsapp/pricing · platform.claude.com/docs/en/agents-and-tools/agent-skills/overview · enterpriseintegrationpatterns.com · arxiv.org/abs/2507.17131 (ARIA) · arxiv.org/abs/2409.07429 (AWM). Doctrina: `/Users/alejandroriveracarrasco/SaSS/DIXDY/docs/23-doctrina-dixdy.md`, `docs/24-whatsapp-bot-autoresponder.md`.
