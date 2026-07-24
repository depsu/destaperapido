# Cómo manejan MEDIA los repos clonados y el bot actual → diseño del módulo `ingesta/` de dixdybot

**Fecha del análisis: 23-jul-2026.** Todo lo citado fue leído del código real en
`scratchpad/clones/` y del bot vivo en `~/SaSS/destaperapido/whatsapp-bot/`. Sin web.

---

## a) NanoClaw — descarga ansiosa, ruta de archivo al agente (nunca base64)

Fuentes: `clones/nanoclaw/channels-branch/whatsapp.ts` (líneas 570-624 y 840-944),
`clones/nanoclaw/src/session-manager.ts` (279-373),
`clones/nanoclaw/container/agent-runner/src/formatter.ts` (269-277). Leído 23-jul-2026.

1. **Descarga AL RECIBIR, en el adaptador** (`downloadInboundMedia`): recorre 4 tipos
   Baileys — `imageMessage→.jpg`, `videoMessage→.mp4`, `audioMessage→.ogg`,
   `documentMessage` (extensión propia) — y baja el binario con
   `downloadMediaMessage(msg, 'buffer', {}, { reuploadRequest: sock.updateMediaMessage })`.
   El `reuploadRequest` es la joya: si la URL del CDN expiró (típico tras reconexiones),
   Baileys le pide a WhatsApp **re-subir** el media en vez de perderlo ("Failed to fetch
   stream" pasa de irrecuperable a recuperable). Guarda en `DATA_DIR/attachments/`.
2. **Nombre de archivo = superficie de ataque**: `documentMessage.fileName` viaja E2E y
   Meta no puede sanearlo → un fileName con `..` escapa del directorio en `path.join`.
   Defensa: `isSafeAttachmentName()` y si falla, nombre generado `tipo-<timestamp>.<ext>`.
   En el lado sesión (`extractAttachmentFiles`): basename-check del messageId, `lstat`
   contra symlinks pre-plantados, contención por `realpath`, y escritura con flag `wx`
   (nunca sobreescribir, nunca seguir symlink).
3. **Fallo de descarga = nota de texto, jamás silencio**: `appendMediaFailureNote()` mete
   en el texto del mensaje que "llegó un media que no se pudo bajar", para que el agente
   sepa que existió. Un mensaje sin texto y sin adjuntos sí se descarta.
4. **Contrato hacia el agente**: el mensaje viaja con
   `attachments: [{type, name, localPath}]`; el binario con base64 solo existe un instante
   (adaptadores que mandan `data`) y session-manager lo baja a
   `inbox/<msgId>/<archivo>` y **borra el campo `data`** — el bus queda limpio de bytes.
5. **Lo que ve el modelo** (formatter.ts:277): texto inline
   `[image: foto.jpg — saved to /workspace/attachments/foto.jpg]` dentro del XML del
   mensaje. Es **RUTA, no base64**: el agente (Claude Code en contenedor) abre el archivo
   con su propia tool Read (multimodal) solo si lo necesita. Caption de imagen/video entra
   como texto del mensaje (`imageMessage?.caption`).

## b) Chatwoot — Attachment como fila + descarga en el webhook + transcripción cacheada

Fuentes: `clones/chatwoot/app/models/attachment.rb`, `db/schema.rb` (tabla `attachments`),
`app/services/whatsapp/incoming_message_base_service.rb` (100-161),
`incoming_message_service_helpers.rb` (2-4, 36-48),
`incoming_message_whatsapp_cloud_service.rb` (11-28),
`enterprise/app/services/messages/audio_transcription_service.rb`. Leído 23-jul-2026.

1. **Modelo**: tabla `attachments` = fila por adjunto ligada a `message` con
   `file_type` (enum de **13 tipos**: image, audio, video, file, location, fallback,
   share, story_mention, contact, ig_reel, ig_post, ig_story, embed), `external_url`,
   `coordinates_lat/long`, `fallback_title`, `extension`, `meta` jsonb. El binario vive en
   ActiveStorage (`has_one_attached :file`), no en la tabla. Mapeo WhatsApp→enum:
   image/sticker→image, audio/voice→audio, video→video, location→location,
   contacts→contact, resto→file.
2. **Descarga AL RECIBIR el webhook, no bajo demanda** (`attach_files` dentro de la
   transacción de crear el mensaje). Cloud API en **dos pasos**: GET
   `media_url(media_id)` con headers autenticados → devuelve URL temporal → `Down.download`
   de esa URL con los mismos headers. Si el primer paso da 401 → `authorization_error!`
   (token vencido, marca el canal). Conserva el `filename` original del payload. El
   `caption` pasa a ser `message.content`.
3. **Tipos sin binario**: location = fila con lat/long + `external_url` (sin archivo);
   contacts = una fila por teléfono con `meta {firstName,lastName}`; `reaction`,
   `ephemeral`, `request_welcome` se descartan; tipo `unsupported` persiste un mensaje
   placeholder ("revisa el teléfono") para no dejar la conversación sin rastro.
4. **Transcripción de audio (enterprise)**: job asíncrono → endpoint de transcripción de
   OpenAI (límite 25 MB decimal, `temperature: 0.0` para no alucinar en silencios).
   Resultado **cacheado en `attachment.meta.transcribed_text`** — idempotente, se paga una
   sola vez — y expuesto al buscador y al modelo (message.rb:278 junta los
   `transcribed_text` como contexto). Este es el patrón "media → texto anotado
   persistente" más maduro de los 8 repos.

## c) BuilderBot — sentinel de evento + descarga PEREZOSA; la asimetría Baileys/Meta

Fuentes: `clones/builderbot/packages/provider-baileys/src/bailey.ts` (615-643, 1131-1159),
`packages/provider-meta/src/utils/processIncomingMsg.ts`,
`packages/provider-meta/src/utils/mediaUrl.ts`,
`packages/provider-meta/src/meta/provider.ts` (209-249). Leído 23-jul-2026.

1. **Al llegar media, ninguno baja bytes**: ambos providers ponen un sentinel en el body
   (`_event_media_`, `_event_voice_note_`, `_event_document_`, `_event_location_`…) para
   que el motor de flujos dispare el keyword-matching. (Anti-patrón para dixdybot, ya
   anotado en planos-sintesis §3: tipo va en **campo propio**, no incrustado en el texto.)
2. **`saveFile` Baileys** (bailey.ts:1149): mimetype del propio mensaje → extensión →
   `downloadMediaMessage(ctx,'buffer')` (descifra E2E; SIN `reuploadRequest`, más frágil
   que nanoclaw) → escribe en `tmpdir()` u `options.path` con nombre generado → devuelve
   ruta absoluta. Solo corre si el desarrollador lo llama en su flow.
3. **`saveFile` Meta** (provider.ts:209): el webhook YA resolvió la URL temporal
   (`getMediaUrl(version, media_id, numberId, jwtToken)` en processIncomingMsg, una
   llamada Graph extra por media) y la dejó en `ctx.url`; saveFile hace GET con Bearer
   token y escribe. Extra: audio PCM de llamadas de voz → `pcmToWav`. Variante
   `saveBuffer` sin tocar disco. `catch → return 'ERROR'` como string (anti-patrón: se
   traga fallos).
4. **La diferencia de fondo Baileys vs Meta**: en Baileys el "puntero" al media es el
   mensaje completo (hace falta la lib para descifrar E2E y el CDN puede expirar → sin
   reupload se pierde); en Meta es un `media_id` re-canjeable por URL temporal con token.
   El contrato de dixdybot debe abstraer ambos con una ref opaca por canal.

## d) El bot ACTUAL (destaperapido, en producción) — etiqueta y bota

Fuentes: `~/SaSS/destaperapido/whatsapp-bot/src/index.js` (55-78), `src/gating.js`
(historial `{from, text}`), `src/link-code.mjs` (23-35, copia de extractText),
`data/conversaciones.jsonl` (log vivo 6-jul→23-jul-2026), `media/` de la instancia.
Verificado 23-jul-2026.

1. **Hoy los IGNORA (salvo caption y ubicación)**: `extractText()` devuelve el caption si
   existe; si no, un **placeholder de texto**: "📷 Foto", "🎥 Video",
   "📎 <fileName|Documento>", "🎤 Mensaje de voz" / "🎵 Audio", "🙂 Sticker",
   "👤 Contacto compartido". La única media aprovechada es la **ubicación** (→ link de
   Google Maps clickeable, que sí alimenta el flujo de entregas). **No hay ni un
   `downloadMediaMessage` en todo `src/`**; el directorio `media/` de la instancia viva
   contiene solo `ficha-bano.jpeg` (media SALIENTE del bot). El cerebro (`claude -p`)
   recibe el historial `{from, text}` y ve "📷 Foto" literal. No guarda, no describe, no
   transcribe: el binario se pierde para siempre (Baileys no lo re-entrega).
2. **Volumen real** (conversaciones.jsonl, ventana disponible 6→23-jul-2026, 17 días,
   1.530 msgs de clientes): **16 medias entrantes de clientes** — 6 fotos, 5 videos, 2
   notas de voz, 1 sticker, 2 contactos (1 de los 16 es del gimnasio de entrenamiento) —
   repartidas en **13 chats distintos**, más 3 ubicaciones (esas sí se usan). Es ~1% de
   los mensajes, pero concentrado en los momentos de mayor intención.
3. **Qué perdió el negocio (casos reales del log, fechados)**:
   - **20-jul 13:51** — cliente manda **video + foto** de dos estanques: "¿ustedes cuentan
     con equipos para vaciar estos estanques? considerando esa válvula de salida". El bot
     responde a los 60s: "Sí, tenemos equipo para vaciar ese tipo de estanque **con esa
     válvula**, sin problema" — **compromiso a ciegas sobre una válvula que jamás vio**
     (riesgo real: mandar camión sin el acople correcto). El trato siguió (2 estanques,
     Lo Blanco 600).
   - **21-jul 19:11** — Luis Saavedra, cotización de **30 baños químicos + 1 de
     discapacitados** para Estación Mapocho (4-5 sep): responde la pregunta clave del
     dueño con una **nota de voz**. La respuesta de uno de los negocios más grandes del
     log quedó en un audio que ni el bot, ni el panel, ni el loop de aprendizaje pueden
     leer; el hilo pasó a depender 100% del oído del dueño.
   - **22-jul 17:34** — cliente manda **video del problema** ("Si mira esta problema
     tengo"); el bot queda fuera de juego y el dueño contesta con audio propio.
   - Transversal: en un rubro donde **la foto del problema ES el input de cotización**
     (destapes, fosas, estanques), el bot no puede diagnosticar ni pre-cotizar con
     imagen; el panel/Kanban muestra "📷 Foto" sin thumbnail; y calidad/juez/replay (🎬)
     evalúan turnos donde falta justo la evidencia.

---

## Diseño del módulo `ingesta/` de dixdybot

Coherente con planos-sintesis §3 (`MensajeEntrante` con `tipo` en campo propio, nada de
sentinels; `guardarMedia` bajo demanda; **el binario nunca viaja por el bus**) y con los
requisitos: sencillez #1, modular-administrable por panel, cerebro Claude vía `llm.js` (E1).

### Archivos

```
src/ingesta/
  index.js            # orquestador: recibirMedia(msg) → guarda ya, anota async
  guardar.js          # ÚNICO que toca binarios; una función por canal
  anotar.js           # cache .anotacion.json + reemplazo del placeholder en el hilo
  procesadores/
    imagen.js         # visión Claude vía llm.js, prompt del rubro → 1-2 frases
    audio.js          # transcripción (proveedor por decidir: es plata → OK Alejandro)
    documento.js      # PDF → texto (pdftotext/nativo); otros → solo ficha
    video.js          # v1: solo ficha (duración, tamaño); v2 opcional: frame + imagen.js
  config.schema.json  # switches por tipo, límite MB, prompt por rubro (panel, E2)
```

### Contrato

1. **Del canal**: `MensajeEntrante { tipo:'media', subtipo:'imagen|audio|video|documento|
   sticker|contacto|ubicacion', caption?, refMedia }`. `refMedia` es **opaco por canal**:
   en Baileys el WAMessage completo (descifrado E2E lo hace la lib), en Meta el
   `media_id` (se canjea por URL temporal + Bearer). Ubicación y contacto NO pasan por
   ingesta: se colapsan a texto en el adaptador (como hoy), patrón Chatwoot
   "attachment sin binario".
2. **`guardar.js: guardarMedia(refMedia, convId, msgId) → {ruta, mime, bytes} | {error}`**
   — guarda en `data/media/<convId>/<msgId>.<ext>`; nombre SIEMPRE generado, jamás el
   fileName del cliente (lección nanoclaw: es attacker-controlled, path traversal).
   Baileys con `reuploadRequest` (lección nanoclaw contra CDN expirado). Se guarda
   **siempre y al recibir** (lección Chatwoot; el modelo perezoso de builderbot pierde el
   media si el proceso se reinicia antes de usarlo — inaceptable con Baileys).
3. **Procesador por subtipo → TEXTO ANOTADO** que reemplaza el placeholder en el hilo:
   - `[FOTO: dos estanques ~1.000L con válvula de bola en la salida inferior] (caption: …)`
   - `[AUDIO transcrito: "sí, confirmo, los 30 estándar y el de discapacitados"]`
   - `[DOCUMENTO plano.pdf: memoria de 2 páginas, pide 30 baños…]`
   - `[VIDEO recibido: 0:42, guardado — avisa al dueño si es clave]` (v1 no procesa video)
   Resultado cacheado en `<archivo>.anotacion.json` (patrón `transcribed_text` de
   Chatwoot: idempotente, se paga una vez; reanalizar/replay lo reutilizan gratis).
4. **El cerebro solo ve texto** (+ la ruta por si un agente con tools quiere mirar el
   archivo, patrón nanoclaw `[image: … — saved to <ruta>]`). Nunca base64 en el hilo ni
   en `conversaciones.jsonl`; el panel usa la ruta para thumbnail y player.
5. **Fallo = nota explícita, jamás silencio** (patrón `appendMediaFailureNote`):
   `[FOTO recibida pero no se pudo descargar — pídele que la reenvíe]` → el cerebro puede
   pedir el reenvío con naturalidad (encaja con el remedio Bad MAC ya existente).
6. **Escalones (doctrina DIXDY)**: guardar es barato y corre siempre (sensor); describir/
   transcribir es el juicio caro y corre según config y con debounce del gating — si la
   anotación tarda, el mensaje entra con `[FOTO: procesando…]` y el timbre re-dispara al
   cerebro cuando llega (mismo mecanismo del gating actual, cero loops nuevos).

### Flujo

```
canal (adaptador) ──MensajeEntrante{tipo:'media'}──► gating: placeholder al hilo
      │
      └─► ingesta.recibirMedia: guardar.js YA (disco) ──► procesadores/<subtipo> (async, vía llm.js)
                                                              │
                hilo/conversaciones.jsonl ◄── anotar.js: reemplaza placeholder por texto anotado
                                                              │
                timbre → cerebro responde VIENDO la descripción → calidad/juez/aprendizaje
                                                                  evalúan con la misma evidencia
```

### Encaje en el plan E0-E7

- **E0 (cinturón)**: solo `guardar.js` en el bot vivo (~40 líneas, Baileys +
  reuploadRequest). No cambia el comportamiento, pero **deja de perderse el binario** desde
  el día 1 — hoy cada media es irrecuperable.
- **Post-E1**: `imagen.js` (visión por `llm.js`, mismo failover suscripción→API) y
  `audio.js` (transcripción; requiere proveedor de pago → decisión de plata de Alejandro;
  Chatwoot usa el endpoint de OpenAI con límite 25 MB y temperature 0.0 como referencia).
  Con ~1 media/día medida, el costo de procesar es marginal.
- **E2**: `config.schema.json` → switches y prompt por rubro en la vista Ajustes
  (schema-driven). Imagen+audio ON por defecto; video OFF en v1.
- **E5**: `guardar.js` gana la rama Meta (`media_id`→URL+Bearer, dos pasos como Chatwoot,
  401→marcar canal). El resto del módulo no se toca: la ref opaca ya lo absorbe.
