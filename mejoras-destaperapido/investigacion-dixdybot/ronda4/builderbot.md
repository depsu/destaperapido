# builderbot (codigoencasa) — planos para la costura E4→E5 de dixdybot

- **Repo:** https://github.com/codigoencasa/builderbot (v1.3.10, monorepo pnpm+lerna)
- **Licencia:** MIT (Copyright 2022 Leifer Mendez) — `LICENSE.md` en la raíz del clon.
- **Clon leído:** `/private/tmp/claude-501/-Users-alejandroriveracarrasco-SaSS-DIXDY-clientes-destaperapido/5acfd0ef-e8b4-49b2-965d-26a7a76d1c5b/scratchpad/clones/builderbot`
- **Relevancia:** su `ProviderClass` corre el MISMO flujo sobre Baileys, Meta Cloud API, Twilio, Telegram, etc. Es exactamente la abstracción de canal que dixdybot necesita en E4 para que E5 (Meta oficial) sea enchufar.

Paquetes provider que existen (en `packages/`): provider-baileys, provider-meta, provider-twilio,
provider-wppconnect, provider-venom, provider-telegram, provider-evolution-api,
provider-facebook-messenger, provider-instagram, provider-gupshup, provider-voice (llamadas WA
con STT/TTS), provider-email, provider-web-whatsapp, provider-sherpa, provider-gohighlevel,
provider-tiktok. Con una sola interfaz. Eso valida el diseño: la interfaz correcta escala a
15+ canales sin tocar el core.

---

## (a) La interfaz Provider completa

**Archivo núcleo:** `packages/bot/src/provider/interface/provider.ts` (319 líneas).

```ts
abstract class ProviderClass<V = any>
    extends EventEmitterClass<ProviderEventTypes>
    implements ProviderHttpServer {

    public abstract globalVendorArgs: GlobalVendorArgs   // config del canal
    public vendor: Vendor<V>                             // el SDK nativo (socket Baileys, MetaCoreVendor…)
    public server: Polka                                 // ¡todo provider trae servidor HTTP!

    // — lo que cada canal DEBE implementar (solo 6 cosas) —
    protected abstract beforeHttpServerInit(): void
    protected abstract afterHttpServerInit(): void
    protected abstract busEvents(): Array<{ event; func }>   // mapa eventos-nativos → bus canónico
    protected abstract initVendor(): Promise<any>            // arranca el SDK, devuelve un emitter
    public abstract sendMessage<K>(userId: string, message: any, args?): Promise<K>
    public abstract saveFile(ctx: any, options?: { path: string }): Promise<string>

    // — lo que el core resuelve una sola vez —
    listenOnEvents(vendor)   // engancha busEvents() al vendor
    start(vendor, cb) / stop()
    inHandleCtx(fn)          // inyecta el bot en handlers HTTP propios
    dispatchInside(payload)  // inyectar un mensaje sintético al bus
    buildHTTPServer()        // polka + cors + json con captura de rawBody
    initAll(port, opts)      // orquesta: initVendor → listenOnEvents → beforeHttp → start → afterHttp
}
```

**Eventos canónicos** (`ProviderEventTypes` en `packages/bot/src/types.ts` L17-27):

```ts
{
  message:        [BotContext]                                  // mensaje entrante normalizado
  require_action: [{ title, instructions[], payload?: { qr?, code? } }]  // QR / pairing code
  notice:         [{ title, instructions[] }]                   // avisos operativos
  ready:          any                                           // canal conectado
  auth_failure:   any                                           // credenciales muertas
  host:           any                                           // identidad del propio bot ({ phone, ... })
}
```

El contrato de mensaje mínimo (`BotContext`, types.ts L84-92) es diminuto a propósito:

```ts
{ body: string; from: string; name?: string; host?: { phone }; [key: string]: any }
```

Todo lo demás (media, ubicación, ids nativos) viaja como campos extra del mismo objeto gracias
al index signature. El core (`packages/bot/src/core/coreClass.ts` L127-130) solo escucha
`'message'` y llama `handleMsg`; jamás ve nada específico del vendor.

**Detalle fino que vale oro:** `buildHTTPServer()` (provider.ts L245-261) captura los bytes
crudos del body en `req.rawBody` vía el hook `verify` de body-parser, ANTES del parseo JSON,
porque la verificación HMAC de Meta debe hacerse sobre los bytes exactos que Meta firmó
(re-serializar con `JSON.stringify` no es byte-idéntico). Está en la clase BASE, no en el
provider Meta: la infraestructura común anticipa la necesidad del canal oficial.

## (b) Normalización del mensaje entrante (Baileys vs Meta)

**El truco central: eventos-como-body.** Cualquier entrada no-texto se convierte en un
sentinel string en `body` con `utils.generateRefProvider('_event_X_')`:

| entrada | body normalizado | extra en el ctx |
|---|---|---|
| texto | el texto | — |
| imagen/video/sticker | `_event_media_...` | meta: `url`, `fileData`, `caption`; baileys: el WAMessage entero |
| documento | `_event_document_` | ídem |
| nota de voz | `_event_voice_note_` | ídem |
| ubicación | `_event_location_` | meta: `latitude`, `longitude` |
| pedido de catálogo | `_event_order_` | `order.{catalog_id, product_items}` |
| llamada | `_event_call_` (solo baileys) | `call` |
| contactos | `_event_contacts_` (solo meta) | `contacts[]` |
| botón respondido | **el TITULO del botón como texto** | meta: `title_button_reply`, `payload` |
| lista respondida | el título/id de la fila como texto | meta: `title_list_reply` |

- **Baileys:** `packages/provider-baileys/src/bailey.ts` L463-753 (`busEvents()`): escucha
  `messages.upsert`, filtra `type !== 'notify'`, stubs corruptos (`Bad MAC`, `No session`,
  `absent`, `Invalid` — ¡el mismo problema Bad MAC que dixdybot resolvió con auto-sanación,
  builderbot solo lo descarta!), extrae texto de
  `ephemeralMessage ?? extendedTextMessage ?? conversation`, y sobrescribe `body` con el
  sentinel según el tipo de mensaje. Botones: L674-678
  (`buttonsResponseMessage.selectedDisplayText` → body). El payload arrastra el WAMessage
  crudo completo (`...messageCtx`).
- **Meta:** `packages/provider-meta/src/utils/processIncomingMsg.ts` (195 líneas): un `switch
  (message.type)` con 11 casos que construye un objeto `Message` limpio
  (`packages/provider-meta/src/types.ts` L158-185: `type, from, to, body, pushName, url,
  fileData, latitude/longitude, order, message_id, timestamp, fromMe, userId`). Para media
  resuelve la URL YA en la normalización (`getMediaUrl` contra Graph API con el jwtToken).
- **La media se abstrae con `saveFile(ctx)`, no en el evento:** el flujo recibe el sentinel
  `_event_media_` y si quiere el archivo llama `provider.saveFile(ctx)` — baileys
  descarga/desencripta (`downloadMediaMessage`, bailey.ts L1149-1159), meta hace GET a la URL
  firmada con Bearer (provider.ts L209-231). El binario nunca viaja por el bus.

**Lección para dixdybot E4:** normalizar el TIPO en un campo `tipo` explícito (no sentinel en
el texto — eso es herencia de su motor de keywords), pero copiar la separación
evento-ligero / media-bajo-demanda con un `guardarMedia(ctx)` por canal.

## (c) provider-meta: webhook, verificación, plantillas, ventana de 24h

**Archivos:** `packages/provider-meta/src/meta/core.ts` (315 L, el webhook),
`packages/provider-meta/src/meta/provider.ts` (1231 L, el envío),
`packages/provider-meta/src/utils/webhookSignature.ts` (45 L).

- **Verificación de alta (GET /webhook):** `core.ts` L163-185 — valida
  `hub.mode === 'subscribe' && hub.verify_token === verifyToken`, responde el `hub.challenge`,
  y **emite `ready` ahí**: para un canal webhook, "conectado" = "Meta verificó el endpoint".
- **Firma HMAC (POST /webhook):** `core.ts` L141-157 + `webhookSignature.ts`:
  `X-Hub-Signature-256` = `sha256=<hmac-hex>` sobre `req.rawBody` (los bytes crudos capturados
  por la clase base), comparación con `timingSafeEqual`, fallback a `JSON.stringify(body)` con
  warning explícito de que puede rechazar webhooks válidos. Opt-in vía `appSecret`.
- **Statuses:** `core.ts` L102-127 aplana `entry[].changes[].value.statuses[]` en una pasada
  O(S); el primer `failed` dispara un `notice` con el motivo (`Number(X): detalle del error`)
  y responde 400. Así es como te enteras de "fuera de ventana de 24h": como un status failed
  DESPUÉS de intentar, no antes.
- **Entrantes:** L191-305 — dispatch de eventos `calls` a un vendor de voz opcional; luego
  `Promise.all` sobre `value.messages[]`, cada uno normalizado y **encolado en un
  `queue-promise` con `concurrent: 1, interval: 100`** (provider.ts L58-62) antes de emitir
  `message` — serializa el procesamiento aunque el webhook traiga batch.
- **Salida:** TODO converge en `sendMessageMeta(body)` → cola → `sendMessageToApi` (POST
  `graph.facebook.com/{version}/{numberId}/messages`, provider.ts L1194-1229). Métodos ricos:
  sendText (preview_url auto-detectado por regex), sendButtons (máx 3, título recortado a 16
  chars — límite real de Meta), sendList, sendButtonUrl (cta_url), sendFlow (WhatsApp Flows),
  sendCatalog, sendReaction, sendLocationRequest, markAsRead, `typing(messageId, ms)` (el
  typing indicator de Meta requiere el wamid del mensaje ENTRANTE, no el número — asimetría
  clave vs Baileys donde `sendPresenceUpdate` va por jid).
- **Plantillas:** `sendTemplate(to, template, languageCode, components)` (provider.ts
  L700-716) — un método plano que arma `type: 'template'`. **NO hay modelado de la ventana de
  24h en ninguna parte** (verificado con grep: cero lógica de timestamps de última entrada, cero
  concepto "session/window"). Builderbot deja la ventana 100% al usuario: si envías texto libre
  fuera de ventana, la API falla y te llega el status `failed` por webhook. **Ese es el hueco
  que dixdybot debe cubrir como concepto de primera clase** (ver veredicto).
- **Gotcha copiable:** `prefixMap = { '549': '54', '521': '52' }` (provider.ts L50-53) — Meta
  entrega `from` argentino/mexicano con el 9/1 extra de móvil, pero para ENVIAR hay que
  quitárselo (`fixPrefixMetaNumber`). Sin esto, respondes a un número que no existe.
- **Gotcha negativo:** `sendMessageToApi` hace `catch (error) { return error }` (L1226-1228)
  — se traga el fallo y devuelve el error como si fuera respuesta. dixdybot NO debe copiar
  esto: en E4 el contrato de `enviar()` debe distinguir éxito/fallo (la ventana de 24h se
  detecta justamente en ese fallo).

## (d) Identidad de la conversación entre proveedores

**La clave es `from`: el número de teléfono pelado, normalizado por cada provider.**

- Baileys: `baileyCleanNumber(jid, true)` (`packages/provider-baileys/src/utils.ts` L19-32)
  quita `@s.whatsapp.net`. Los `@lid` (identificadores de privacidad de WA, tema 2024+) se
  resuelven a número real vía `remoteJidAlt` + un caché LID→PN dedicado de 1238 líneas
  (`packages/provider-baileys/src/lidCache.ts`, híbrido archivo+memoria) — bailey.ts L590-599
  y L831-876. Al ENVIAR, `resolveNumber` intenta LID→PN y si no puede envía al @lid directo.
- Meta: `message.from` del webhook, `parseMetaNumber` quita `+` y espacios
  (`packages/provider-meta/src/utils/number.ts`); los BSUID (`US.13491208...`, IDs
  business-scoped de Meta) pasan intactos porque Meta exige devolverlos sin tocar.
- Twilio: quita el prefijo `whatsapp:+` (`packages/provider-twilio/src/utils.ts` L2).

Todo el estado del core se indexa por ese `from`: `SingleState` es un
`Map<from, estado>` (`packages/bot/src/context/stateClass.ts`), la cola principal
(`queuePrincipal.clearQueue(from)`), la blacklist y los callbacks de idle. **No hay prefijo de
canal** — builderbot asume UN provider por proceso de bot, así que el teléfono basta.

**Para la decisión convId de dixdybot:** builderbot esquiva el problema multi-canal
(un proceso = un canal). Como dixdybot E4 quiere N canales sobre un solo cerebro y un
solo-escritor, la clave debe ser compuesta: `canal:idNativoNormalizado`
(ej. `wa-baileys:56912345678`, `wa-meta:56912345678`) con una tabla opcional de identidad que
una las dos cuando es la misma persona. La lección builderbot: cada canal normaliza SU id a
"teléfono pelado" antes de cruzarlo — la normalización vive en el canal, la identidad en el core.

## (e) Ciclo de vida: socket con estado vs webhook sin estado

- **Baileys** (`bailey.ts` L298-456): `initVendor()` crea el socket, maneja
  `connection.update`; reconexión con **backoff exponencial** (1s→30s cap, máx 10 intentos,
  lista blanca de códigos reconectables incl. 429/5xx, `shouldReconnect` L1161-1178 +
  `delayedReconnect` L1180-1219 que cierra el socket viejo antes de recrear —
  `ws.close()` + `end()` para evitar el error `xml-not-well-formed`); `loggedOut` → borra el
  directorio de sesión y rearranca; QR/pairing-code → `require_action`; conexión abierta →
  `ready` + `host`. Además: caches NodeCache para retries/dispositivos/mensajes (el
  `getMessage` desde caché arregla el "this message can take a while" de iOS), handlers de
  SIGINT/SIGTERM/uncaughtException con `cleanup()`.
- **Meta** (`meta/provider.ts` L123-143): `initVendor()` es casi un no-op — instancia
  `MetaCoreVendor` (un EventEmitter), registra `GET/POST /webhook` y resuelve al tiro. No hay
  reconexión porque no hay conexión. `ready` sale cuando Meta verifica el webhook;
  `host` sale en `afterHttpServerInit` consultando el perfil por Graph API (con un mapa de
  errores 401/403/timeout → avisos legibles, L92-120).

**Cómo lo esconde:** el template method `initAll` de la clase base ejecuta la MISMA secuencia
para ambos (`initVendor → listenOnEvents(busEvents) → beforeHttpServerInit → start →
afterHttpServerInit`), y los 6 eventos canónicos absorben la diferencia semántica:
`ready` significa "listo para conversar" sea socket abierto o webhook verificado;
`require_action` solo existe de facto en canales no oficiales (QR); `auth_failure` cubre
tanto sesión Baileys muerta como token Meta inválido. El core y los flujos no distinguen.
Que TODO provider traiga servidor HTTP (Baileys lo usa solo para servir el QR en `/`) es lo
que hace uniforme la forma: **canal = emitter de 6 eventos + servidor HTTP + sendMessage +
saveFile.**

## (f) VEREDICTO: la interfaz `Canal` mínima de dixdybot (E4)

Copiar el esqueleto de builderbot (6 eventos + pocos métodos abstractos + template method de
arranque) y agregar lo que builderbot NO tiene: tipo de mensaje explícito, resultado de envío
honesto, y **plantillas + ventana-24h de primera clase**. JSDoc concreto (estilo del bot vivo,
CommonJS/ESM sin TS):

```js
/**
 * @typedef {Object} MensajeEntrante — evento canónico, lo ÚNICO que ve el cerebro
 * @property {string} convId       — `${canal.id}:${idNativoNormalizado}` (ej. "wa-baileys:56912345678")
 * @property {string} canal        — "wa-baileys" | "wa-meta" | "telegram" | ...
 * @property {string} idNativo     — teléfono pelado / chat_id, normalizado POR el canal
 * @property {'texto'|'media'|'documento'|'audio'|'ubicacion'|'boton'|'orden'|'llamada'|'contacto'} tipo
 * @property {string} texto        — cuerpo; para botón/lista: el título elegido (patrón builderbot)
 * @property {string} [nombre]     — pushName
 * @property {string} [msgIdNativo]— wamid / key.id (Meta lo exige para typing y replies)
 * @property {number} ts           — epoch ms
 * @property {{lat:number,lng:number}} [ubicacion]
 * @property {Object} [crudo]      — payload nativo, SOLO para saveMedia/debug, nunca para lógica
 */

/**
 * @typedef {Object} ResultadoEnvio
 * @property {boolean} ok
 * @property {string}  [msgIdNativo]
 * @property {'fuera_de_ventana'|'auth'|'rate'|'desconocido'} [motivo] — NO tragarse el error
 *           (anti-patrón builderbot: sendMessageToApi hace `catch(e){return e}`)
 */

/**
 * Interfaz Canal — E4. Un objeto por canal; el core solo conoce esto.
 * Eventos que DEBE emitir (EventEmitter): 'mensaje' (MensajeEntrante), 'listo',
 * 'accion_requerida' ({titulo, instrucciones, qr?|codigo?}), 'fallo_auth', 'aviso',
 * 'estado_envio' ({msgIdNativo, estado:'entregado'|'leido'|'fallido', motivo?})  ← builderbot
 * solo lo loguea como notice; dixdybot lo necesita para los ✓✓ reales del panel.
 */
class Canal extends EventEmitter {
  /** @type {string} p.ej. "wa-baileys" — prefijo de convId */ id
  /** ¿El canal exige plantillas fuera de la ventana de servicio? (Meta sí, Baileys no) */
  soportaPlantillas = false
  /** Horas de ventana de respuesta libre; Infinity en canales no oficiales */
  ventanaHoras = Infinity

  /** Arranca (socket o webhook). Reconexión/backoff es problema INTERNO del canal. */
  async iniciar() {}
  async detener() {}

  /** @param {string} convId  @param {{texto?, mediaPath?, botones?, replyA?}} m
   *  @returns {Promise<ResultadoEnvio>} */
  async enviar(convId, m) {}

  /** PRIMERA CLASE (builderbot lo deja al usuario y por eso duele):
   *  @param {string} convId @param {string} nombre @param {string} idioma
   *  @param {Array} variables  @returns {Promise<ResultadoEnvio>} */
  async enviarPlantilla(convId, nombre, idioma, variables) {}

  /** ¿Puedo escribir texto libre ahora? El core la consulta ANTES de enviar.
   *  Implementación: ts del último MensajeEntrante por convId (el un-solo-escritor
   *  ya persiste eso en conversaciones.jsonl) vs ventanaHoras.
   *  @returns {{abierta: boolean, expiraTs?: number}} */
  ventana(convId) {}

  /** Descarga el binario de un MensajeEntrante con tipo media/documento/audio.
   *  @returns {Promise<string>} path absoluto */
  async guardarMedia(msg, opts) {}

  /** Cortesías humanas; no-op si el canal no las tiene.
   *  OJO asimetría real: Baileys teclea por jid, Meta por msgIdNativo entrante. */
  async escribiendo(convId, msgIdNativo) {}
  async marcarLeido(convId, msgIdNativo) {}
}
```

**Reglas de core que completan el plano:**
1. El core decide `enviar` vs `enviarPlantilla` consultando `canal.ventana(convId)` —
   nunca "enviar y ver si falla" (que es el modus operandi builderbot vía statuses failed).
2. Si `enviar()` devuelve `motivo: 'fuera_de_ventana'` igual (reloj desincronizado), el core
   degrada a plantilla de re-apertura y registra el evento — cierre del loop.
3. El adaptador E4 sobre el bot vivo: envolver `enviar.js` + el listener de Baileys actual en
   `CanalWaBaileys` sin tocar el cerebro; `ventana()` responde siempre `{abierta: true}`.
   En E5, `CanalWaMeta` = webhook (copiar verificación + HMAC-sobre-rawBody + statuses de
   `core.ts` de provider-meta, que es código MIT maduro) + Graph API.
4. El un-solo-escritor de E4 vive DETRÁS de `enviar()`: los canales no escriben JSONL;
   emiten y devuelven, el core persiste (builderbot hace lo mismo con `database.save` en
   `coreClass.sendProviderAndSave`).

## Piezas robables directas (MIT, con atribución en comentario)

1. `webhookSignature.ts` completo (HMAC + timingSafeEqual + extracción case-insensitive) — E5.
2. El hook `verify` de body-parser para `rawBody` (provider.ts L249-260) — E5.
3. `verifyToken` middleware (core.ts L163-185) — E5.
4. `extractStatus` aplanador de statuses (core.ts L102-127) — E5, alimenta 'estado_envio'.
5. `prefixMap` 549→54 / 521→52 y `fixPrefixMetaNumber` — E5 si llega tráfico ARG/MEX.
6. Lista de códigos reconectables + backoff exponencial con cierre del socket viejo
   (bailey.ts L1161-1219) — endurecer el CanalWaBaileys de E4.
7. Patrón botón→texto (el título del botón entra al cerebro como si el cliente lo hubiera
   escrito) — E4, mantiene el cerebro `claude -p` agnóstico de botones.
