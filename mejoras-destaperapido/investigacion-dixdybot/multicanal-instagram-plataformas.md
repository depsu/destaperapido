# Investigación: bot multi-canal (WhatsApp + Instagram + futuro web/Messenger) en 2025-2026

Fecha: 2026-07-23 · Para: rediseño "dixdybot" (destaperapido.cl / DIXDY)
Contexto local: bot vivo en `/Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot`
(Node + Baileys, cerebro = `claude -p` local, sin API key).

---

## (a) Instagram: cómo se automatizan DMs legalmente

### La vía oficial: Instagram Messaging API de Meta

Hay **dos sabores** de la API oficial desde julio de 2024:

1. **Instagram API with Instagram Login** (lanzada 23-jul-2024): el negocio se loguea
   directo con su cuenta de Instagram. **Ya NO exige Página de Facebook vinculada.**
   Requisitos verificados en la doc de Meta
   (developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/messaging-api/):
   - Cuenta **profesional** de Instagram (Business o Creator).
   - Permisos: `instagram_business_basic` + `instagram_business_manage_messages`
     (los scopes viejos se deprecaron el 27-ene-2025).
   - **Webhooks obligatorios** para recibir: suscribirse a `messages`, `messaging_optins`,
     `messaging_postbacks`, `messaging_reactions`, `messaging_referrals`, `messaging_seen`.
   - Token de acceso de usuario Instagram del dueño de la cuenta.
2. **Instagram API with Facebook Login** (la vía clásica): exige cuenta Business
   vinculada a una Página de Facebook. Es la que usan Chatwoot y la mayoría de las
   plataformas hoy.

**Niveles de acceso** (clave para un negocio chico como destaperapido):
- **Standard Access**: si la app solo atiende TU propia cuenta profesional (o cuentas que
  administras), **NO necesita App Review**. Esto es exactamente el caso dixdybot: una app
  Meta propia sirviendo la cuenta del cliente que administras.
- **Advanced Access**: solo si la app sirve cuentas de terceros que no administras →
  App Review + Business Verification (demo funcional, grabaciones de pantalla; suele
  tardar 5-10 días hábiles). Sería necesario recién si DIXDY vende dixdybot como SaaS
  multi-tenant donde cada cliente conecta su propia cuenta.

**Reglas de conversación** (iguales en espíritu a WhatsApp):
- El bot **solo puede responder**: el usuario debe escribir primero (perfecto para el
  modelo "solo responde" que ya usa el bot de WhatsApp).
- **Ventana de 24 horas** para responder cada mensaje entrante.
- **Etiqueta `HUMAN_AGENT`**: extiende la respuesta hasta **7 días**, pero SOLO para
  respuestas humanas reales; requiere pedir el permiso "Human Agent" en App Review y
  **Meta audita cada uso** — usarla con el bot = revocación. (Fuente: doc Meta + guía
  ManyChat + artículo de Chatwoot sobre el human agent tag.)
- Tipos de mensaje soportados: texto (≤1000 bytes), links, hasta 10 imágenes, audio,
  video, PDF, stickers, reacciones, plantillas, posts propios. **Sin chats grupales.**
- **Divulgación de automatización**: la política de Meta pide que las experiencias
  automatizadas revelen al inicio que el usuario habla con un servicio automatizado
  (y al pasar de humano a bot).

### ¿Existe vía no oficial para Instagram y qué riesgo tiene?

Sí existen (instagrapi en Python, bots de navegador, y el bridge Matrix `mautrix-meta`
que "puppetea" la cuenta con las APIs privadas de Meta), pero el riesgo en 2025-2026 es
**mucho peor que en WhatsApp**:

- Cifras citadas por la industria (PostEngage, CreatorFlow, bot.space): herramientas
  aprobadas vía API oficial ⇒ tasa de suspensión **<0,5%/año**; automatización por
  navegador/no oficial ⇒ **15-30%/año**.
- **Meta ha emitido avisos DMCA contra librerías Python no oficiales** que envuelven el
  flujo web de Instagram.
- Meta mejoró su detección ML en 2025: el enforcement es más rápido y difícil de apelar;
  lo que en 2022 era una advertencia hoy es restricción inmediata.
- A diferencia de WhatsApp (donde un número quemado se reemplaza), en Instagram la
  cuenta ES el activo del negocio (seguidores, reseñas, contenido): **perderla no tiene
  reemplazo barato**. Conclusión: para Instagram, SOLO vía oficial.

---

## (b) Plataformas open source de bandeja/omnicanal (estado 2025-2026)

| Plataforma | ¿Viva? | Licencia | Instagram | Cerebro LLM propio |
|---|---|---|---|---|
| **Chatwoot** | Sí, muy activa | **MIT** el core; carpeta `enterprise/` propietaria (se puede borrar y queda 100% MIT) | Sí, **oficial** (incl. Instagram Business Login sin página de FB) | Sí: **Agent Bot API** — webhook saliente con cada mensaje, respondes por REST API |
| **Evolution API** | Sí, activa | Apache 2.0 **+ cláusulas de marca** (conservar logo/copyright, notificar uso visible al admin) | **Parcial/prometido**: docs y marketing lo listan, el README de GitHub NO lo confirma; históricamente "coming soon" | Sí: webhooks + integraciones nativas (Chatwoot, Typebot, n8n, Dify, OpenAI, RabbitMQ/Kafka/SQS, S3) |
| **Typebot** | Sí, activa | **FSL-1.1-Apache-2.0** (source-available; cada release pasa a Apache 2.0 a los 2 años). OJO: **WhatsApp es feature de pago incluso self-hosted** | No (WhatsApp Cloud API + web) | Sí: bloques webhook y endpoints OpenAI-compatibles |
| **Botpress** | v12 open source quedó **legacy**; el producto actual es **Botpress Cloud, cerrado** ($89-1.495/mes + AI spend) | v12 AGPL (abandonándose); Cloud propietario | Vía Cloud | En Cloud sí (GPT-4, Claude, custom); v12 self-host sin rumbo |
| **n8n** | Sí, muy activa | **Sustainable Use License** (fair-code): uso interno de empresa permitido gratis; prohibido revenderlo como SaaS | No es canal, es orquestador (nodos WhatsApp/Chatwoot/HTTP) | Sí, es su fuerte (nodos AI + HTTP a lo que sea) |
| **Matrix / mautrix-meta** | Sí, activa (v26.07, jul-2026, ~1000 commits) | **AGPL-3.0** | Sí pero **NO oficial** (puppeting de APIs privadas de Meta ⇒ mismo riesgo de ban que instagrapi) | Sí (bots Matrix), pero apilas complejidad: homeserver Synapse + bridges |

**Notas finas:**
- Chatwoot es la única de la lista con bandeja omnicanal REAL y madura (live chat, email,
  WhatsApp, Instagram DM, Messenger, Telegram) + handoff bot→humano integrado. Su
  **Agent Bot** es exactamente el enchufe que dixdybot necesita: Chatwoot POSTea eventos
  de conversación a tu `outgoing_url`, tu cerebro (Claude Code local, expuesto p.ej. por
  túnel) responde vía API. Sí tuvo un bug real con Instagram en 2025 (issue #12055:
  mensajes enviados desde la app de IG no aparecían en la bandeja desde el 25-jul-2025),
  señal de que la integración depende de Meta y a veces se rompe.
- Evolution API es la favorita del ecosistema brasileño no-oficial de WhatsApp (Baileys +
  Cloud API oficial en el mismo servidor, con conectores a Chatwoot/Typebot/n8n). Para
  Instagram NO es hoy una solución confiable: no aparece en el README oficial y la
  promesa lleva tiempo en "coming soon".
- Matrix como bus doméstico es elegante en papel (un protocolo, N bridges), pero para un
  negocio: bridge de Meta no oficial (riesgo de cuenta) + operar Synapse + AGPL. No para
  producción comercial con la cuenta de un cliente.

---

## (c) El patrón de arquitectura de los que lo hacen bien

Los nombres reales vienen de *Enterprise Integration Patterns* (Hohpe & Woolf,
enterpriseintegrationpatterns.com):

- **Channel Adapter**: componente por canal que habla el dialecto del canal (Baileys,
  Graph API de IG, widget web) y publica/consume mensajes de un canal interno.
- **Canonical Data Model / mensaje canónico**: TODOS los adaptadores traducen a un solo
  formato interno (`{conversation_id, contact, channel, direction, type, text, media,
  timestamp, metadata}`). El cerebro nunca ve JSON de Baileys ni de Meta.
- **Message Router**: decide a qué conversación/cola/humano va cada mensaje.
- **Messaging Gateway**: la fachada que expone "enviar/recibir" simple al resto del
  sistema, escondiendo la mensajería.
- **Message Bus**: la columna vertebral que une adaptadores, cerebro y paneles.
- En la práctica de los productos (Chatwoot, Twilio Conversations, los SaaS omnicanal):
  **adaptadores de ingreso → mensaje canónico en bandeja unificada (con resolución de
  identidad: mismo cliente en WhatsApp e IG = un contacto) → cerebro/agente → outbox por
  canal** que re-traduce al formato y a los límites de cada canal (ventana 24h, tipos de
  mensaje). El **outbox persistente** (transactional outbox) es lo que da reintentos y
  anti-duplicados — el bot actual YA lo tiene en embrión: `src/outbox.js`,
  `data/envios.jsonl` (libro anti-duplicados), `src/gating.js` (límites anti-ban por
  canal), `src/brain.js` (cerebro desacoplado), `src/store.js`.

Traducción a dixdybot: lo que hoy es "el bot de WhatsApp" se parte en (1) adaptador
WhatsApp (Baileys, con su gating anti-ban), (2) contrato canónico de mensaje, (3) cerebro
único (Claude Code + caminos/reglas del negocio, agnóstico del canal), (4) outbox por
canal con las reglas del canal (en IG: solo responder, 24h, disclosure de bot), (5) panel
que lee la bandeja unificada. Mañana Instagram = escribir SOLO el adaptador (2) contra la
Messaging API oficial; el resto no se toca.

---

## (d) Recomendación

**Construir un gateway de canales propio y delgado, con el patrón de (c) — y NO adoptar
una plataforma completa hoy.** Razones:

1. **El diferencial de dixdybot es el cerebro** (Claude Code local + caminos + pausa-y-
   aprende + gimnasio). Ninguna plataforma trae eso; todas lo tratan como un webhook
   externo. Adoptar Chatwoot/Botpress obliga a remodelar el Kanban, el gimnasio, los
   recordatorios 💤 y el enlace chat↔entrega que ya funcionan, para ganar principalmente
   una bandeja que ya existe en `:8789`.
2. **Doctrina DIXDY**: no reinventar NI adoptar infraestructura pesada al lado de los
   motores existentes. El costo real del gateway propio es pequeño: definir el mensaje
   canónico y partir `index.js` en adaptador vs cerebro vs outbox — refactor, no obra nueva.
3. **Instagram entra SOLO por la vía oficial**: app Meta propia + cuenta profesional del
   cliente + Standard Access (sin App Review mientras la app sirva cuentas que DIXDY
   administra) + webhook receptor (un Worker de Cloudflare puede recibirlo y encolarlo
   para el Mac, igual que el correo-worker). El adaptador IG es un cliente HTTP de la
   Graph API: mucho más simple que Baileys.
4. **Excepción que vale la pena vigilar**: si DIXDY llega a 5+ clientes con bandeja
   humana intensiva, **Chatwoot (MIT, borrando `enterprise/`) como bandeja** + dixdybot
   como Agent Bot vía webhook es el mejor matrimonio: Chatwoot pone los adaptadores
   oficiales de IG/Messenger/Telegram y el handoff a humanos; el cerebro sigue siendo
   tuyo. Es la única adopción que suma sin canibalizar el cerebro.
5. **WhatsApp**: seguir con Baileys (ya operativo, con gating), sabiendo que la salida de
   emergencia es la Cloud API oficial: desde el 1-jul-2025 Meta cobra **por mensaje** y
   las conversaciones **iniciadas por el cliente son gratis dentro de la ventana de 24h**
   — o sea, un bot que SOLO responde saldría ≈ $0 en la API oficial. Ese dato baja mucho
   el costo de migrar si un número cae.
6. **No usar** vías no oficiales de Instagram (instagrapi, mautrix-meta) con cuentas de
   clientes: riesgo de suspensión 15-30%/año vs <0,5% oficial, DMCA de Meta a esas libs,
   y la cuenta IG del cliente es irremplazable.

### Piezas concretas que ya existen y se reusan
- `src/outbox.js` + `data/envios.jsonl` → outbox canónico multi-canal (agregar campo `channel`).
- `src/gating.js` → política por canal (WhatsApp: anti-ban; IG: ventana 24h + disclosure).
- `src/brain.js` / `aprender-core.mjs` → cerebro y loop de caminos, sin tocar.
- `correo-worker` (patrón DIXDY) → molde para el webhook receptor de IG en Cloudflare.

---

## Fuentes principales

- https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/messaging-api/ (requisitos, permisos, webhooks, 24h, tipos de mensaje, disclosure)
- https://developers.facebook.com/docs/instagram-platform/overview/ (Standard vs Advanced Access, App Review)
- https://help.manychat.com/hc/en-us/articles/14281199732892 (ventanas 24h/7 días, human_agent)
- https://www.chatwoot.com/hc/user-guide/articles/1745225158-what-is-human-agent-tag-in-instagram-messenger-channel
- https://github.com/chatwoot/chatwoot + https://github.com/chatwoot/chatwoot/blob/develop/enterprise/LICENSE (MIT core + enterprise propietario)
- https://developers.chatwoot.com/api-reference/agentbots/create-an-agent-bot y https://www.chatwoot.com/hc/user-guide/articles/1677497472-how-to-use-agent-bots (Agent Bot webhook)
- https://github.com/chatwoot/chatwoot/issues/12055 (bug Instagram jul-2025)
- https://github.com/EvolutionAPI/evolution-api (canales reales: Baileys + Cloud API; licencia Apache 2.0 + cláusulas de marca; sin IG confirmado en README)
- https://doc.evolution-api.com/v2/en/get-started/introduction (Instagram/Messenger "coming soon")
- https://github.com/baptisteArno/typebot.io (FSL-1.1-Apache-2.0; WhatsApp de pago self-hosted)
- https://docs.n8n.io/sustainable-use-license/ y https://community.n8n.io/t/clarification-on-license-using-n8n-for-internal-whatsapp-ai-chatbot-non-resale-use/215777
- https://www.lindy.ai/blog/botpress-pricing y https://chatimize.com/reviews/botpress/ (Botpress v12 vs Cloud, precios 2025)
- https://github.com/mautrix/meta (bridge Meta AGPL-3.0, activo v26.07) y https://github.com/mautrix/instagram (deprecado a favor de mautrix-meta)
- https://www.enterpriseintegrationpatterns.com/patterns/messaging/ChannelAdapter.html (Channel Adapter, Message Bus, Canonical Data Model, Messaging Gateway)
- https://postengage.ai/blog/instagram-automation-ban-risk-truth y https://www.bot.space/blog/the-dangers-of-unofficial-instagram-dm-apis-why-theyll-get-you-banned (riesgo no oficial, DMCA)
- https://www.ycloud.com/blog/whatsapp-api-pricing-update y https://respond.io/blog/whatsapp-business-api-pricing (pricing por mensaje 1-jul-2025, servicio gratis en ventana 24h)
- Código local: /Users/alejandroriveracarrasco/SaSS/destaperapido/whatsapp-bot/src/{outbox.js,gating.js,brain.js,store.js,aprender-core.mjs}
