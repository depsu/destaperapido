# Censo open source 2024-2026 para el rediseño "dixdybot"

Fecha: 2026-07-23. Método: búsquedas web + verificación de cada repo contra la API de GitHub
(`gh api repos/...`) el mismo día — estrellas, licencia SPDX y fecha del último push son datos
reales de la API, no de artículos. Donde la API devolvió `NOASSERTION` significa licencia
no estándar / open-core (hay que leer el LICENSE a mano antes de reutilizar código).

Contexto del rediseño: bot actual = Node + Baileys, cerebro `claude -p` sin API key, dashboard
Kanban local en :8789, gimnasio de entrenamiento y loop de aprendizaje. Meta: "dixdybot"
multi-canal (WhatsApp hoy, Instagram mañana), panel de configuración limpio, y entrenamiento
por "caminos" (si falta conocimiento → pausa el chat, pregunta al humano, aprende, crea el camino).

---

## (a) Bots de WhatsApp con LLM

### WhiskeySockets/Baileys — la base actual sigue siendo la correcta
- URL: https://github.com/WhiskeySockets/Baileys
- 10.233 ⭐ | MIT | último push 2026-07-22 (activísimo)
- Qué robar: nada nuevo — es lo que ya usa el bot. El dato importante del censo es que
  sigue siendo LA librería socket-based de referencia y está viva. No hay razón para migrar
  la capa de transporte de WhatsApp.

### evolution-foundation/evolution-api (ex EvolutionAPI/evolution-api)
- URL: https://github.com/EvolutionAPI/evolution-api (redirige a evolution-foundation)
- 9.028 ⭐ | licencia NOASSERTION (revisar: era Apache-2.0, hoy la API no la reporta estándar) | push 2026-07-14
- Node server que mantiene sesiones WhatsApp (usa Baileys por debajo) y expone REST API
  multi-instancia con API key. Enorme tracción 2025-2026, sobre todo con n8n.
- Qué robar: el patrón "sesión WhatsApp como servicio REST multi-instancia". Si dixdybot
  quiere servir a varios clientes DIXDY (destapando, fullfosas...) con UN solo proceso de
  sesiones y N cerebros, este es el diseño de referencia. OJO: n8n en sí es fair-code
  (Sustainable Use License), no open source OSI.

### devlikeapro/waha — WhatsApp HTTP API
- URL: https://github.com/devlikeapro/waha
- 7.073 ⭐ | Apache-2.0 | push 2026-07-22
- Igual que Evolution (REST sobre WhatsApp) pero con 3 motores conmutables (WEBJS/browser,
  NOWEB/Baileys-like, GOWS/whatsmeow). Core gratis, features Plus de pago.
- Qué robar: la idea de "motor conmutable" detrás de una misma API — mismo contrato HTTP,
  distinto backend según riesgo de ban. Documentación de webhooks muy limpia.

### codigoencasa/builderbot (ex bot-whatsapp) — comunidad hispana
- URL: https://github.com/codigoencasa/builderbot
- 2.960 ⭐ | MIT | push 2026-07-21
- Framework de bots WhatsApp en TypeScript con **abstracción de providers**: el mismo flujo
  corre sobre Baileys, Meta Cloud API, Twilio, Venom o WPPConnect sin tocar la lógica.
- Qué robar: **la interfaz Provider**. Es exactamente la costura que dixdybot necesita para
  "WhatsApp hoy, Instagram mañana": separar `canal.enviar()/canal.recibir()` de el cerebro.
  Comunidad en español (útil para el contexto chileno). Su modelo de "flows" es rígido
  (keyword-driven), no robarlo — el cerebro Claude ya es mejor.

### Otros verificados de la categoría
- **wwebjs/whatsapp-web.js** — 22.248 ⭐ | Apache-2.0 | push 2026-07-19. Basado en Puppeteer
  (pesado); no conviene migrar, solo referencia de API ergonómica.
- **tulir/whatsmeow** — 6.798 ⭐ | MPL-2.0 | push 2026-07-22. Librería Go multidevice; la
  opción si algún día se quiere un daemon de sesión ultra estable separado del cerebro Node.
- **open-wa/wa-automate-nodejs** — 3.633 ⭐ | NOASSERTION | push 2026-07-22.
- **wppconnect-team/wppconnect** — 3.364 ⭐ | NOASSERTION | push 2026-07-23.
- **noDiego/whatsapp-claude-gpt** — 59 ⭐ | sin licencia | push 2026-07-16. Bot
  wwebjs + Claude/GPT/Qwen con imágenes y TTS; chico pero mantenido; referencia de manejo
  multi-modelo, no base.
- **MuchoRio/Baileys-WA-Bot** — 0 ⭐ | MIT | push 2026-06-16. Apareció en búsquedas por SEO
  del README; sin comunidad, descartar.

---

## (b) CRM / inbox de conversaciones con IA y Kanban

### chatwoot/chatwoot — el estándar omnicanal
- URL: https://github.com/chatwoot/chatwoot
- 34.667 ⭐ | NOASSERTION (MIT + carpeta enterprise propietaria, open-core) | push 2026-07-23
- Inbox omnicanal real: WhatsApp (Cloud API), **Instagram**, email, web chat, Telegram, SMS.
  Trae "Captain", su agente IA integrado que aprende de help center y FAQs; etiquetas,
  vistas personalizadas, asignación, handoff humano.
- Qué robar: (1) el **modelo de datos conversación/inbox/contacto multi-canal** — está
  resuelto y probado a escala; (2) su integración Instagram vía Graph API oficial como mapa
  de ruta para el canal Instagram de dixdybot; (3) el patrón de handoff agente-IA → humano.
  Contra: Rails + Postgres + Redis, pesado para un Mac local; Captain es en parte enterprise.
  Es la referencia si dixdybot "se agranda", no para embeber mañana.

### ArnasDon/wacrm — plantilla CRM WhatsApp moderna
- URL: https://github.com/ArnasDon/wacrm
- 1.680 ⭐ | MIT | push 2026-07-21 | 594 commits, 4.4k forks
- Next.js 16 + Supabase + **Meta Cloud API** (oficial, no Baileys). Inbox compartido,
  contactos, **pipelines Kanban con deals vinculados a conversaciones**, broadcasts,
  automatizaciones no-code, asistente IA (OpenAI/Anthropic) con tokens cifrados, y hasta
  **servidor MCP** para que un asistente IA opere el CRM. Se presenta como "plantilla, no
  producto": fork, brandea, hostea.
- Qué robar: (1) el esquema Supabase de pipeline-Kanban-ligado-a-chat (dixdybot ya usa
  Supabase para entregas — encaja directo); (2) el MCP server del CRM como patrón para que
  Claude Code opere el panel; (3) UI del inbox como referencia de "panel limpio". MIT = se
  puede copiar código literal.

### kevinrivm/vocero-crm — el gemelo conceptual del gimnasio
- URL: https://github.com/kevinrivm/vocero-crm
- 79 ⭐ | MIT | push 2026-07-11 | 26 commits (proyecto joven, en español)
- Next.js 15 + Postgres/Drizzle + SSE. CRM WhatsApp self-hosted con agente IA y un
  **"Laboratorio de auto-evaluación"**: 6 clientes simulados conversan contra el agente REAL
  en sandbox (jamás envía mensajes reales), un **juez LLM independiente** puntúa 0-100 cada
  conversación, reporta alucinaciones y huecos de conocimiento con evidencia, sugiere parches
  al knowledge base y guarda historial con delta tras cada cambio.
- Qué robar: **el diseño completo del Laboratorio** — es el "gimnasio + juez opus + replay"
  del bot actual, pero sistematizado: score, hallazgos con evidencia, sugerencias aplicables
  y delta histórico. Como es MIT y chico (26 commits), se puede leer entero en una tarde y
  portar las ideas (o el código del lab) al gimnasio de dixdybot. Contra: usa Meta Cloud API
  y OpenRouter, no Baileys ni claude -p; y con 79 ⭐ el bus-factor es 1.

### Otros verificados
- **frappe/crm** — 3.003 ⭐ | AGPL-3.0 | push 2026-07-22. Kanban de leads + integración
  WhatsApp vía Frappe; AGPL y ecosistema Frappe = fricción alta, solo referencia visual.
- **chaskiq/chaskiq** — 3.541 ⭐ | NOASSERTION | push 2026-06-30. Alternativa a Intercom en
  Rails; menos canal WhatsApp que Chatwoot; descartable.
- **Tiledesk/tiledesk** — 311 ⭐ | MIT | push 2026-07-06. Orquestación k8s, sobredimensionado.
- **sempicanha/crm-kanban-whatsapp** — extensión de navegador que pinta un Kanban sobre
  WhatsApp Web; curiosidad, no infraestructura.

---

## (c) Entrenamiento / coaching / testing de bots conversacionales

### confident-ai/deepeval — simulador de conversaciones + métricas multi-turno
- URL: https://github.com/confident-ai/deepeval
- 17.061 ⭐ | Apache-2.0 | push 2026-07-22
- Su **ConversationSimulator** genera conversaciones realistas usuario-falso ↔ bot real a
  partir de un escenario + descripción del usuario, vía `model_callback` (encaja con
  cualquier cerebro, incluido `claude -p` envuelto en una función). Métricas listas:
  ConversationCompleteness, TurnRelevancy, KnowledgeRetention, RoleAdherence, TopicAdherence.
  Docs: https://deepeval.com/docs/conversation-simulator
- Qué robar: la **test suite de diálogos como CI**: N escenarios dorados (cliente apurado,
  cliente que regatea, cliente que retoma a los 3 días) corridos automáticamente tras cada
  cambio de reglas/tarifario, con umbral de aprobación. Es la versión industrial del
  "correr tests tras cambiar precios" que ya existe en el bot.

### promptfoo/promptfoo — evals declarativos + red teaming
- URL: https://github.com/promptfoo/promptfoo
- 23.513 ⭐ | MIT | push 2026-07-22
- Evals en YAML, comparación de prompts, y **red teaming** (inyecciones, jailbreaks) — útil
  porque un bot público de WhatsApp recibe de todo. Qué robar: el formato declarativo de
  casos de prueba (YAML versionable en git, muy DIXDY) y el escáner de vulnerabilidades
  conversacionales antes de cada release del persona/tarifario.

### langfuse/langfuse — trazas, sesiones y colas de anotación humana
- URL: https://github.com/langfuse/langfuse
- 31.683 ⭐ | NOASSERTION (open-core, MIT con módulos ee) | push 2026-07-23
- Qué robar: dos patrones — (1) **sesiones**: cada conversación multi-turno como traza
  navegable con replay; (2) **annotation queues**: cola donde el humano puntúa/corrige
  mensajes uno a uno — es el "feedback 👍👎 por mensaje" del dashboard actual, pero con
  esquema de datos maduro. Autohostable con Docker; quizá pesado para el Mac, pero el
  esquema de datos es copiable.

### codeforequity-at/botium-core — "el Selenium de los chatbots"
- URL: https://github.com/codeforequity-at/botium-core
- 251 ⭐ | MIT | push 2026-05-20
- Scripting BotiumScript (convo files: give/expect) para test end-to-end de diálogos.
  Semi-dormido y pre-LLM; robar solo el formato `.convo.txt` (legible por no técnicos) si
  se quiere que Alejandro escriba casos de prueba a mano.

### Chainlit/chainlit — UI conversacional con feedback integrado
- URL: https://github.com/Chainlit/chainlit
- 12.325 ⭐ | Apache-2.0 | push 2026-06-11
- UI de chat en Python con feedback por mensaje incorporado. Referencia de UX, no base
  (el stack dixdybot es Node).

### Nota
Rasa X (la vieja UI de "coaching" de conversaciones) está discontinuada; no apareció nada
open source vivo que haga exactamente "pausa el chat y pregúntale al humano la regla" — esa
pieza (los "caminos") habrá que construirla; lo más cercano conceptual es HumanLayer (abajo)
y el handoff de Chatwoot.

---

## (d) Comunidad Claude Code

### Hallazgo estructural: Claude Code Channels (marzo 2026)
- Anthropic lanzó "Channels" (research preview, Claude Code v2.1.80+, requiere Bun y
  suscripción Pro/Max): plugins de canal que puentean Telegram/Discord/iMessage con una
  sesión viva de Claude Code — el mensaje entra como evento, Claude lo procesa local con
  filesystem/MCP/git, responde por el mismo canal. Fuente:
  https://claudefa.st/blog/guide/development/claude-code-channels
- Implicancia para dixdybot: el patrón "cerebro = Claude Code local, sin API key" que hoy es
  artesanal (`claude -p`) ahora tiene un carril NATIVO. El rediseño debería mirar Channels
  como la arquitectura de largo plazo del cerebro.

### crisandrews/claude-whatsapp — canal WhatsApp oficial de la comunidad
- URL: https://github.com/crisandrews/claude-whatsapp
- 8 ⭐ | MIT | push 2026-06-09
- Plugin de canal WhatsApp para Claude Code **usando Baileys** (mismo stack que dixdybot),
  publicado en el marketplace oficial de plugins de Anthropic (primer canal WhatsApp
  comunitario revisado por Anthropic). El servidor sostiene la sesión linked-device y
  reenvía mensajes entrantes a la sesión como notificaciones; Claude actúa vía tools MCP:
  `reply, react, edit_message, download_attachment, status, unreplied, catch_up, list_groups`.
- Qué robar: **el contrato MCP de canal** (esa lista de tools ES la interfaz multi-canal que
  dixdybot necesita) y el manejo QR/transcripción de voz/control de acceso. Pocas estrellas
  pero con sello del marketplace oficial.

### RichardAtCT/claude-code-telegram
- URL: https://github.com/RichardAtCT/claude-code-telegram
- 2.736 ⭐ | sin licencia (¡ojo: no se puede copiar código legalmente!) | push 2026-03-30
- Bot Telegram con acceso remoto a Claude Code, persistencia de sesión. Robar ideas de
  session persistence y aprobación remota de tools, no código (sin LICENSE).

### Otros verificados
- **linuz90/claude-telegram-bot** — 451 ⭐ | MIT | push 2026-05-01. Colas de mensajes,
  botones interactivos, entrega de archivos vía MCP. MIT = copiable.
- **earlyaidopters/claudeclaw** — 160 ⭐ | sin licencia | push 2026-04-14. Claude Code CLI
  como bot personal de Telegram (voz, memoria, tareas programadas).
- **gokapso/claude-code-whatsapp** — 43 ⭐ | sin licencia | push 2026-01-20. Claude Code en
  WhatsApp con sandbox E2B por usuario (depende del SaaS Kapso).
- **dsebastien/whatsapp-claude-agent** — 39 ⭐ | MIT | push 2026-02-09. Puente simple
  WhatsApp ↔ Claude Code.
- **dashiz91/claude-code-whatsapp** — 5 ⭐ | MIT | push 2026-02-17.
- **hesreallyhim/awesome-claude-code** — 50.684 ⭐ | push 2026-07-23. El índice canónico de
  la comunidad; punto de partida para monitorear novedades (sección de integraciones).

### openclaw/openclaw — el gorila de la sala
- URL: https://github.com/openclaw/openclaw
- **383.851 ⭐** | licencia reportada MIT (la API dice NOASSERTION — verificar LICENSE) | push 2026-07-23
- Ex Clawdbot/Moltbot. Asistente personal self-hosted, local-first, con **gateway como plano
  de control** y 20+ canales (WhatsApp, Telegram, Signal, iMessage, Slack...; **Instagram NO
  está en la lista**). Multi-agente con aislamiento por canal/cuenta, cron jobs, webhooks,
  daemon macOS (`openclaw onboard --install-daemon`). Modelo-agnóstico vía API keys/OAuth de
  proveedor — NO usa `claude -p` local como cerebro.
- Qué robar: la **arquitectura gateway/canales/enrutamiento multi-agente** — es el diseño de
  referencia 2026 para "un cerebro, N canales" corriendo en un Mac. También su manejo de
  sesiones y daemon. Contra: es asistente personal, no bot de negocio con cotizador; y su
  masa (383k ⭐, cientos de features) es lo contrario de la doctrina DIXDY de no sumar
  infraestructura — se roba el plano, no el edificio.

---

## (e) Frameworks de agentes con guardrails / journeys

### emcie-co/parlant — LA pieza conceptual para los "caminos"
- URL: https://github.com/emcie-co/parlant
- 18.180 ⭐ | Apache-2.0 | push 2026-07-12 | v3.3.2 (abr 2026), 5.485 commits
- Python 3.10+. Motor de control de interacción para agentes de cara al cliente:
  - **Guidelines**: reglas condición→acción; el motor selecciona por turno SOLO las
    relevantes → puedes tener cientos sin degradar la adherencia (exactamente el problema
    del loop de aprendizaje actual: las reglas destiladas crecen y el prompt engorda).
  - **Journeys**: SOPs multi-turno adaptativos (saltar/revisitar estados según el cliente)
    — el equivalente formal de los "caminos" de dixdybot.
  - **Canned responses**: plantillas pre-aprobadas para momentos críticos (precios: cero
    alucinación de cifras — crítico para el tarifario).
  - Relationships entre guidelines, glossary, tools con matching contextual.
  - LLM-agnóstico (Anthropic soportado, LiteLLM para el resto). Widget React de chat oficial.
- Qué robar: como mínimo el **modelo mental completo** (guideline/journey/canned-response y
  el matcher por turno); como máximo, embeber el motor Python detrás del transporte Baileys
  existente. La tensión: Parlant asume LLM por API, no `claude -p` — habría que adaptar el
  backend de modelo o solo portar el diseño al cerebro actual.

### NVIDIA-NeMo/Guardrails
- URL: https://github.com/NVIDIA-NeMo/Guardrails
- 6.773 ⭐ | NOASSERTION (Apache-2.0 con partes) | push 2026-07-23
- Rails programables (Colang) para I/O de LLMs: filtros de entrada/salida, temas prohibidos.
- Qué robar: el patrón de rails de entrada/salida baratos ANTES del cerebro caro (muy
  alineado con la doctrina DIXDY de "sensor barato + umbral"). Colang en sí es demasiado.

### RasaHQ/rasa + CALM
- URL: https://github.com/rasahq/rasa
- CALM (flows con LLM) vive en **Rasa Pro**: código visible pero licencia de pago
  (Developer Edition gratis hasta 1.000 conversaciones/mes; Growth ~USD 35k/año).
- Veredicto: NO reutilizable en la práctica para DIXDY; solo referencia del concepto "flows
  como lógica de negocio + LLM como comprensión".

### humanlayer/humanlayer
- URL: https://github.com/humanlayer/humanlayer
- 11.140 ⭐ | NOASSERTION | push 2026-06-19
- OJO: pivoteó a herramienta para coding agents ("CodeLayer"). Pero su SDK original definió
  el patrón `require_approval` / contact-human-as-tool: **el agente pausa y contacta al
  humano por Slack/email cuando no sabe o necesita aprobación** — conceptualmente es EXACTO
  el flujo "falta un camino → pausa el chat → pregunta a Alejandro → aprende". Robar el
  patrón (tool de escalamiento con respuesta asíncrona que reanuda el hilo), no el repo.

### baptisteArno/typebot.io
- 10.181 ⭐ | NOASSERTION (open-core) | push 2026-07-15. Builder visual de flujos con canal
  WhatsApp. Referencia de UX de builder, pero el paradigma de árbol rígido es lo que dixdybot
  quiere evitar.

### Instagram (el canal de mañana) — panorama honesto
- No existe un "Baileys de Instagram" mantenido y confiable en 2026. Opciones reales:
  1. **Meta Graph API oficial (Instagram Messaging)** — la vía de Chatwoot y wacrm; requiere
     cuenta business y app aprobada, pero es la única sin riesgo de ban.
  2. **mautrix/meta** — 406 ⭐ | AGPL-3.0 | push 2026-07-22. Puente Matrix para Messenger +
     Instagram DM (ingeniería inversa; riesgo de ban + AGPL).
  3. instagrapi y derivados (API privada Python): no oficiales, riesgo alto de baneo.
- Conclusión: para Instagram conviene diseñar el adaptador de canal contra la API oficial
  desde el día uno (patrón provider de BuilderBot / contrato MCP de claude-whatsapp).

---

## Tabla resumen (verificado contra GitHub API el 2026-07-23)

| Repo | ⭐ | Licencia | Último push | Pieza a robar |
|---|---|---|---|---|
| openclaw/openclaw | 383.851 | MIT* | 2026-07-23 | Arquitectura gateway + canales + multi-agente |
| chatwoot/chatwoot | 34.667 | open-core | 2026-07-23 | Modelo de datos inbox omnicanal; Instagram vía Graph API |
| langfuse/langfuse | 31.683 | open-core | 2026-07-23 | Sesiones con replay + annotation queues |
| promptfoo/promptfoo | 23.513 | MIT | 2026-07-22 | Evals YAML + red teaming del bot público |
| wwebjs/whatsapp-web.js | 22.248 | Apache-2.0 | 2026-07-19 | (solo referencia) |
| emcie-co/parlant | 18.180 | Apache-2.0 | 2026-07-12 | Guidelines/Journeys/Canned = los "caminos" |
| confident-ai/deepeval | 17.061 | Apache-2.0 | 2026-07-22 | ConversationSimulator + métricas multi-turno |
| Chainlit/chainlit | 12.325 | Apache-2.0 | 2026-06-11 | UX de feedback por mensaje |
| humanlayer/humanlayer | 11.140 | NOASSERTION | 2026-06-19 | Patrón "pausa y pregunta al humano" |
| WhiskeySockets/Baileys | 10.233 | MIT | 2026-07-22 | (base actual, sigue viva) |
| typebot.io | 10.181 | open-core | 2026-07-15 | UX de builder visual |
| evolution-api | 9.028 | NOASSERTION | 2026-07-14 | Sesiones WhatsApp multi-instancia como REST |
| devlikeapro/waha | 7.073 | Apache-2.0 | 2026-07-22 | Motores conmutables tras una misma API |
| tulir/whatsmeow | 6.798 | MPL-2.0 | 2026-07-22 | Daemon de sesión en Go (futuro) |
| NVIDIA-NeMo/Guardrails | 6.773 | NOASSERTION | 2026-07-23 | Rails I/O baratos antes del cerebro |
| chaskiq/chaskiq | 3.541 | NOASSERTION | 2026-06-30 | — |
| frappe/crm | 3.003 | AGPL-3.0 | 2026-07-22 | (referencia Kanban) |
| codigoencasa/builderbot | 2.960 | MIT | 2026-07-21 | Interfaz Provider multi-canal |
| RichardAtCT/claude-code-telegram | 2.736 | SIN licencia | 2026-03-30 | Ideas de sesión remota (no código) |
| mautrix/whatsapp | 1.843 | AGPL-3.0 | 2026-07-22 | (puente Matrix) |
| ArnasDon/wacrm | 1.680 | MIT | 2026-07-21 | Esquema Supabase Kanban↔chat + MCP server del CRM |
| linuz90/claude-telegram-bot | 451 | MIT | 2026-05-01 | Colas + botones + archivos vía MCP |
| mautrix/meta | 406 | AGPL-3.0 | 2026-07-22 | Puente Instagram DM (riesgoso) |
| codeforequity-at/botium-core | 251 | MIT | 2026-05-20 | Formato .convo legible por humanos |
| earlyaidopters/claudeclaw | 160 | SIN licencia | 2026-04-14 | claude CLI como bot con memoria |
| kevinrivm/vocero-crm | 79 | MIT | 2026-07-11 | Laboratorio de auto-evaluación completo |
| noDiego/whatsapp-claude-gpt | 59 | SIN licencia | 2026-07-16 | Manejo multi-modelo |
| gokapso/claude-code-whatsapp | 43 | SIN licencia | 2026-01-20 | — |
| dsebastien/whatsapp-claude-agent | 39 | MIT | 2026-02-09 | Puente simple |
| crisandrews/claude-whatsapp | 8 | MIT | 2026-06-09 | Contrato MCP de canal (marketplace oficial) |

\* licencia según el sitio del proyecto; la API de GitHub reporta NOASSERTION — leer LICENSE.

---

## Top-5: vale la pena mirar en serio

1. **Parlant (emcie-co/parlant)** — Apache-2.0, 18.2k ⭐, activo. Es el único framework que
   formaliza exactamente el concepto de "caminos": journeys adaptativos + guidelines con
   matching por turno + respuestas enlatadas para precios. Aunque no se adopte el motor
   (asume LLM por API, no `claude -p`), su modelo de datos es el plano para el rediseño.

2. **vocero-crm (kevinrivm/vocero-crm)** — MIT, chico y en español. Su "Laboratorio de
   auto-evaluación" (clientes simulados vs agente real en sandbox + juez LLM con score,
   evidencia y delta histórico) es el gimnasio de dixdybot ya diseñado por otra persona.
   26 commits: se lee entero en una tarde y se saquea con licencia MIT.

3. **Claude Code Channels + crisandrews/claude-whatsapp** — la señal de arquitectura más
   importante del censo: Anthropic hizo NATIVO el patrón "mensajería → sesión Claude Code
   local" (mar 2026), y ya existe un canal WhatsApp comunitario sobre Baileys en el
   marketplace oficial, con un contrato MCP de canal (reply/react/unreplied/catch_up)
   directamente reutilizable como interfaz multi-canal de dixdybot.

4. **DeepEval (confident-ai/deepeval)** — Apache-2.0, 17k ⭐. ConversationSimulator +
   métricas multi-turno = la test suite de diálogos que convierte el entrenamiento en algo
   confiable: escenarios dorados corridos tras cada cambio de reglas, con umbral de
   aprobación antes de desplegar el cerebro nuevo.

5. **wacrm (ArnasDon/wacrm)** — MIT, 1.7k ⭐, activo. La plantilla más directa del "panel de
   configuración limpio": Next.js + Supabase (stack que el proyecto ya usa para entregas),
   Kanban de deals ligado a conversaciones, tokens cifrados y un MCP server para que Claude
   opere el CRM. Copiable pieza a pieza por ser plantilla y no producto.

Menciones: **OpenClaw** (robar el plano gateway/canales, no el edificio — y ojo: NO tiene
Instagram), **BuilderBot** (interfaz Provider multi-canal, MIT, comunidad hispana),
**HumanLayer** (el patrón "pausa y pregunta al humano" que los caminos necesitan),
**Chatwoot** (mapa de ruta Instagram oficial + handoff), **promptfoo** (red teaming del bot
público), **Langfuse** (annotation queues para el feedback por mensaje).

## Lo que NO encontré (honestidad del censo)
- Ningún proyecto open source vivo que implemente exactamente "el bot detecta que le falta
  conocimiento, pausa ESE chat, pregunta al humano la regla y crea el camino en caliente".
  Las piezas existen por separado (handoff de Chatwoot/vocero, contact-human de HumanLayer,
  journeys de Parlant), pero el ciclo completo habrá que construirlo — es la parte
  genuinamente original de dixdybot.
- Ningún "Baileys de Instagram" confiable: el canal Instagram tendrá que ser Graph API
  oficial (como Chatwoot/wacrm) o un puente riesgoso (mautrix/meta, instagrapi).
- Estrellas de OpenClaw (383k) verificadas por API; la cifra de "347k" que circula en
  artículos ya quedó corta. Su licencia exacta requiere leer el LICENSE (API: NOASSERTION).
