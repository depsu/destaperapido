# Chatwoot — modelo de datos del inbox omnicanal (para dixdybot E4/E5)

**Repo:** https://github.com/chatwoot/chatwoot — clon en
`/private/tmp/claude-501/-Users-alejandroriveracarrasco-SaSS-DIXDY-clientes-destaperapido/5acfd0ef-e8b4-49b2-965d-26a7a76d1c5b/scratchpad/clones/chatwoot`

**Licencia:** MIT (Expat) para todo el repo SALVO `enterprise/` (licencia comercial propia,
`enterprise/LICENSE`). Ver `LICENSE` en la raíz. Robar patrones del código MIT es legítimo;
no copiar nada de `enterprise/`.

Todo lo citado abajo sale de `db/schema.rb` y `app/models` del clon (leído, no del README).

---

## (a) El triángulo Contact / ContactInbox / Conversation

Tres tablas, con `contact_inboxes` como pieza clave que nosotros NO tenemos:

**`contacts`** (`db/schema.rb:720`) — la PERSONA, agnóstica de canal:
`name, email, phone_number, identifier (id externo del negocio), additional_attributes jsonb,
custom_attributes jsonb, last_activity_at, blocked, account_id, company_id`.
Únicos por cuenta: `(email, account_id)`, `(identifier, account_id)`. Índice trigram GIN
sobre nombre/email/fono para búsqueda.

**`contact_inboxes`** (`db/schema.rb:705`) — la IDENTIDAD de esa persona EN UN CANAL:
```
contact_id, inbox_id, source_id (text NOT NULL), hmac_verified, pubsub_token
UNIQUE (inbox_id, source_id)   ← la llave de enrutamiento de todo lo entrante
```

**¿Qué es `source_id` por canal?** (`app/builders/contact_inbox_builder.rb:14-59` +
`app/services/instagram/webhooks_base_service.rb:15`):
- WhatsApp Cloud/360dialog: teléfono E164 **sin el `+`** (`wa_source_id` hace `delete('+')`).
- Twilio WhatsApp: `"whatsapp:+569..."`; Twilio SMS: E164 con `+`.
- Email: la dirección de correo. SMS: el teléfono.
- Instagram/Facebook: el IGSID/PSID que entrega Meta (`user['id']` del webhook) — un id
  opaco por página, NO el username.
- Web widget / API: `SecureRandom.uuid` (es una sesión, no una identidad real).

**Unificación de la misma persona en 2 canales**
(`app/builders/contact_inbox_with_contact_builder.rb`):
1. Entra un mensaje → busca `contact_inboxes` por `(inbox, source_id)`. Si existe, listo.
2. Si no: `find_contact` en cascada **identifier → email → phone_number** (y para Instagram,
   además busca contact_inboxes de canales FacebookPage con el mismo IGSID, líneas 84-96).
3. Si encuentra contacto, solo crea el `contact_inbox` nuevo colgado de él; si no, crea
   contacto + identidad. Maneja carrera con retry sobre `RecordNotUnique`.

O sea: **el contacto se unifica por datos duros compartidos (fono/email/identifier); cada
canal conserva su fila de identidad**. Y hay fusión manual explícita:
`app/actions/contact_merge_action.rb` reasigna conversations, messages (sender) y
contact_inboxes del duplicado al contacto base y hace deep_merge de atributos (el base gana).

**`conversations`** (`db/schema.rb:764`) — un hilo EN un canal (no cruza canales):
`account_id, inbox_id, contact_id, contact_inbox_id, display_id (único por cuenta), uuid,
status, assignee_id, assignee_agent_bot_id, team_id, priority, snoozed_until, waiting_since,
first_reply_created_at, last_activity_at, contact_last_seen_at, agent_last_seen_at,
additional_attributes, custom_attributes, campaign_id, sla_policy_id, cached_label_list`.
Reuso de hilo (`app/services/whatsapp/incoming_message_base_service.rb:115-128`): busca
conversaciones del CONTACTO (no solo de esa identidad — coexistencia da 2 source_ids) en el
inbox, reabre la no-resuelta o crea nueva; `inbox.lock_to_single_conversation` fuerza 1 hilo.

## (b) Inbox + Channel polimórfico

`inboxes` (`db/schema.rb:1034`) tiene `channel_id + channel_type` y
`belongs_to :channel, polymorphic: true` (`app/models/inbox.rb:61`). El inbox concentra el
COMPORTAMIENTO (greeting, horario laboral + timezone, auto-asignación, csat,
`lock_to_single_conversation`, `out_of_office_message`); el canal concentra el TRANSPORTE
y las CREDENCIALES. Una tabla por tipo de canal:

- **`channel_whatsapp`** (`db/schema.rb:677`): `phone_number` (unique), `provider`
  (`default`=360dialog | `whatsapp_cloud`), **`provider_config` jsonb** (api_key,
  business_account_id, webhook_verify_token, `source: embedded_signup`, calling_enabled…),
  `message_templates` jsonb + `message_templates_last_updated` (catálogo Meta cacheado).
- **`channel_instagram`** (`:573`): `instagram_id` (unique), `access_token`, `expires_at`
  (token que caduca → servicio de refresh, `app/models/channel/instagram.rb:74`).
- **`channel_facebook_pages`** (`:561`): `page_id`, `user_access_token`,
  `page_access_token`, `instagram_id` (el puente FB↔IG).
- **`channel_api`** (`:517`): webhook_url, identifier, hmac_token — canal genérico.

Patrón adapter limpio en `app/models/channel/whatsapp.rb:65-71 y 117-121`: el canal expone
`provider_service` (factory → `WhatsappCloudService` | `Whatsapp360DialogService`) y
**delega** `send_message / send_template / sync_templates / media_url` al provider. Cambiar
de proveedor = cambiar `provider` + `provider_config`, mismo esquema. Esto es exactamente la
forma de convivir Baileys ↔ Cloud API en E4→E5.

## (c) Message — comparado con nuestro conversaciones.jsonl

`messages` (`db/schema.rb:1140`, `app/models/message.rb`):

| Campo | Detalle |
|---|---|
| `message_type` | enum `incoming:0 / outgoing:1 / activity:2 / template:3` (`message.rb:87`) |
| `status` | enum `sent / delivered / read / failed` (`message.rb:103`) — los acks ✓✓ |
| `source_id` | **id externo del mensaje** (wamid de WA, mid de IG). Dedup de webhooks (`incoming_message_base_service.rb:36` + `lock_message_source_id!`) y correlación de acks/replies |
| `sender_type + sender_id` | **polimórfico**: Contact, User (humano), AgentBot, Captain::Assistant — quién escribió cada línea |
| `content_type` | text, cards, form, input_csat, sticker, voice_call… (widgets estructurados) |
| `content_attributes` | json con accessors declarados: `in_reply_to`, `in_reply_to_external_id`, `external_created_at`, `external_error`, `deleted`, `is_unsupported`, `external_echo`… (`message.rb:111`) |
| `additional_attributes` | `campaign_id`, `template_params` |
| `private` | boolean — notas internas invisibles al cliente, en el MISMO hilo |
| `external_source_ids` | jsonb (ej. id en Slack) — puentes a otros sistemas |

Lógica que regalan: `prevent_message_flooding` (tope de mensajes/minuto por conversación
contra loops de automatización, `message.rb:288`); `waiting_since` se setea con el entrante
y lo limpia la respuesta humana o del bot (`message.rb:339-360`); `human_response?`
distingue humano de bot **por sender_type**, incluyendo `external_echo` = respuesta escrita
desde la app nativa de WhatsApp (`message.rb:362`) — nuestro problema de "¿quién cotizó, el
bot o Alejandro?" (envios.jsonl vs from) lo resuelven en el dato, no cruzando archivos.

Nuestro `conversaciones.jsonl` (from/rol/texto/ts) NO tiene: source_id externo (dedup +
acks), status por mensaje, sender explícito bot/humano, tipo `activity` (nuestras tarjetas
de correo son esto), tipo `template`, notas privadas.

## (d) Ventana de 24h y plantillas de WhatsApp

**La ventana NO es un campo en el esquema: se calcula.**
`Conversations::MessageWindowService` (`app/services/conversations/message_window_service.rb`):
`can_reply?` = `Time.current < último_mensaje_ENTRANTE.created_at + ventana`, con ventana
por tipo de canal: WhatsApp 24h fija; Twilio solo si medium=whatsapp; FB/IG 24h o 7 días si
está el flag "human agent" de Meta; TikTok 48h; canal API configurable vía
`channel.additional_attributes['agent_reply_time_window']`. Un servicio puro de ~70 líneas.

**Plantillas — dos mitades:**
1. **Catálogo** cacheado en el canal: `channel_whatsapp.message_templates` jsonb +
   `message_templates_last_updated`; `sync_templates` after_create y refresco periódico
   (`app/services/whatsapp/providers/whatsapp_cloud_service.rb:36-38`).
2. **Uso** viaja EN el mensaje: `message.additional_attributes['template_params']` =
   `{name, category, language, namespace, processed_params}` validado con **JSON-schema en
   el modelo** (`TEMPLATE_PARAMS_SCHEMA`, `message.rb:48-63`).

El árbol de decisión al enviar (`app/services/whatsapp/send_on_whatsapp_service.rb:8-13`):
`template_params presentes → send_template; si no, can_reply? → mensaje de sesión; si no →
status: :failed + external_error "outside messaging window"`. El fallo queda registrado en
el propio mensaje, visible en el hilo.

## (e) Handoff bot ↔ humano

Formalizado en TRES lugares, todos datos (no ifs regados):

1. **`conversation.status`**: `open / resolved / pending / snoozed` (`conversation.rb:83`).
   **`pending` = el bot está a cargo.** Al crear: `determine_conversation_status` →
   `:pending` si `inbox.active_bot?` (`conversation.rb:289-296`). El traspaso es
   `bot_handoff!` (`conversation.rb:174`): `open!` + setear `waiting_since` + evento
   `CONVERSATION_BOT_HANDOFF`. Mensaje entrante sobre conversación resuelta la reabre a
   `pending` si hay bot activo, a `open` si no (`message.rb:424-434`).
2. **`agent_bot_inboxes`** (`app/models/agent_bot_inbox.rb`): junction bot↔inbox con
   `status active/inactive` — el interruptor "bot encendido en este canal". Nuestro modo
   manual global pasaría a ser por-canal y por-conversación.
3. **Asignación dual** en la conversación: `assignee_id` (User) y `assignee_agent_bot_id`,
   con `assignee_type` virtual que resuelve AgentBot > User (`conversation.rb:204-214`).
   Más `team_id`, `conversation_participants` y `mentions` para el lado humano.

Bonus que ya nos calzan: `snoozed_until` = nuestros recordatorios 💤 con fecha;
`waiting_since` + `first_reply_created_at` = métricas de espera del Kanban gratis.

## (f) Veredicto: esquema mínimo dixdybot para E4 (multi-canal, un-solo-escritor)

Cinco archivos/tablas (sirve JSONL por tabla o SQLite; nombres propuestos):

1. **`contactos`** — persona única multi-canal:
   `id, nombre, telefono (E164 con +), email, identifier, atributos{}, bloqueado,
   last_activity_at`. Únicos: telefono, email, identifier.
2. **`identidades`** (el ContactInbox, LA pieza a robar) —
   `id, contacto_id, canal_id, source_id`. **UNIQUE (canal_id, source_id)**.
   source_id: WA Baileys = jid, WA Cloud = fono sin `+`, IG = IGSID. TODO mensaje entrante
   se enruta por esta llave; al crear identidad nueva se busca contacto existente por
   telefono → email → identifier (cascada del builder).
3. **`canales`** (inbox+channel aplanado; sin SQL polimórfico no hace falta separarlos) —
   `id, tipo ('wa_baileys'|'wa_cloud'|'instagram'), nombre, config{}` (credenciales +
   provider, el `provider_config` de chatwoot), `plantillas{}, plantillas_sync_at,
   bot_activo` (el agent_bot_inbox.status), `horario{}, timezone`.
4. **`conversaciones`** —
   `id, canal_id, contacto_id, identidad_id, estado ('pendiente_bot'|'abierta'|'resuelta'|
   'dormida'), asignado ('bot'|'humano'), snoozed_until, waiting_since, first_reply_at,
   last_activity_at, atributos{}`. display_id secuencial por cliente para hablar de "la #143".
5. **`mensajes`** —
   `id, conversacion_id, canal_id, tipo ('entrante'|'saliente'|'actividad'|'plantilla'),
   remitente_tipo ('contacto'|'bot'|'humano'), texto, contenido_tipo,
   atributos_contenido{} (in_reply_to, error_externo, template_params…),
   source_id_externo (wamid/mid; único por canal → dedup de webhooks y correlación de acks),
   estado ('enviado'|'entregado'|'leido'|'fallido'), privado, ts`.

Reglas robadas: la ventana de 24h se CALCULA del último entrante (servicio puro estilo
MessageWindowService), nunca se persiste; la plantilla viaja en el mensaje y el catálogo
vive en el canal; el handoff es `estado` + `asignado` en la conversación más `bot_activo`
en el canal; anti-flood por conversación/minuto antes de escribir. El un-solo-escritor de
E4 escribe estas 5 tablas; todo lo demás (paneles, Kanban, repartidor) lee.
